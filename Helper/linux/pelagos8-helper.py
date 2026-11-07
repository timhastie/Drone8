#!/usr/bin/env python3
"""Pelagos-8 preset dialog helper - Linux port of Helper/lira_dialog_helper.m

The plugin cannot open file dialogs itself, so it writes small token files to
/tmp and this background helper answers them: it shows Save/Load dialogs
(tkinter) and steps through the preset library in ~/Music/Pelagos-8/Presets.

Protocol (identical to the macOS helper):
  plugin -> helper   <tmp>/lira_save_req.token, lira_saveas_req.token,
                     lira_load_req.token, lira_prev_req.token,
                     lira_next_req.token, lira_new_req.token,
                     lira_current_save.lira (the captured state)
  helper -> plugin   <tmp>/lira_load_ready.lira, lira_preset_name.txt,
                     lira_load_ready.token, lira_save_done.token

Env overrides (for testing): PELAGOS8_TMP (default /tmp),
PELAGOS8_PRESETS (default ~/Music/Pelagos-8/Presets).
Dependencies: python3 and tkinter only (tkinter is imported lazily, so the
non-dialog paths work headless too).
"""
import os
import re
import sys
import time

TMP = os.environ.get("PELAGOS8_TMP") or "/tmp"
PRESETS = os.environ.get("PELAGOS8_PRESETS") or os.path.expanduser("~/Music/Pelagos-8/Presets")
POLL_SECONDS = 0.03
LOG_CAP_BYTES = 1048576

READY_FLAG_TEXT = b"ready 1;\n"


def tmp_path(name):
    return os.path.join(TMP, name)


def log(msg):
    try:
        with open(tmp_path("lira_helper.log"), "a", encoding="utf-8") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + "[Pelagos-8 Helper] " + msg + "\n")
    except OSError:
        pass


def remove(path):
    try:
        os.remove(path)
    except OSError:
        pass


def put_bytes(path, data):
    """Atomic write (like NSString writeToFile:atomically:): write <path>.new,
    then rename over.  Retries around the plugin's polling reads."""
    tmpf = path + ".new"
    for _ in range(20):
        try:
            with open(tmpf, "wb") as f:
                f.write(data)
            os.replace(tmpf, path)
            return True
        except OSError:
            time.sleep(0.005)
    log("put_bytes failed: " + path)
    remove(tmpf)
    return False


def write_empty(name):
    return put_bytes(tmp_path(name), b"")


def read_bytes(path):
    try:
        with open(path, "rb") as f:
            return f.read()
    except OSError:
        return None


def base_name(path):
    # like NSString stringByDeletingPathExtension on the last path component
    return os.path.splitext(os.path.basename(path))[0]


def ensure_presets_dir():
    try:
        os.makedirs(PRESETS, exist_ok=True)
    except OSError as e:
        log("cannot create presets folder %s: %s" % (PRESETS, e))


def natural_key(name):
    # Finder/Explorer-style ordering: case-insensitive, digit runs by value.
    return [(0, int(t)) if t.isdigit() else (1, t.lower())
            for t in re.split(r"(\d+)", name)]


class Helper(object):
    def __init__(self):
        self.is_busy = False
        self.current_preset_name = ""
        # Same startup sequence and order as the macOS helper.
        remove(tmp_path("lira_load_req.token"))
        write_empty("lira_load_ready.token")
        remove(tmp_path("lira_save_req.token"))
        remove(tmp_path("lira_saveas_req.token"))
        write_empty("lira_save_done.token")
        remove(tmp_path("lira_new_req.token"))
        remove(tmp_path("lira_prev_req.token"))
        remove(tmp_path("lira_next_req.token"))
        log("Watching triggers (Save, Save As, Load, Prev, Next, New) in %s; presets in %s"
            % (TMP, PRESETS))

    # --- preset library ---------------------------------------------------
    def all_preset_paths_sorted(self):
        ensure_presets_dir()
        try:
            files = os.listdir(PRESETS)
        except OSError:
            return []
        lira = [f for f in files
                if os.path.splitext(f)[1] == ".lira"
                and os.path.isfile(os.path.join(PRESETS, f))]
        lira.sort(key=natural_key)
        return [os.path.join(PRESETS, f) for f in lira]

    def step_preset_by_offset(self, offset):
        presets = self.all_preset_paths_sorted()
        if not presets:
            return
        current_index = 0
        cur = self.current_preset_name.lower()
        for i, p in enumerate(presets):
            if base_name(p).lower() == cur:
                current_index = i
                break
        next_index = (current_index + offset) % len(presets)
        target = presets[next_index]
        base = base_name(target)
        self.current_preset_name = base
        content = read_bytes(target)
        if content is not None:
            put_bytes(tmp_path("lira_load_ready.lira"), content)
            put_bytes(tmp_path("lira_preset_name.txt"), (base + ";\n").encode("utf-8"))
            put_bytes(tmp_path("lira_load_ready.token"), READY_FLAG_TEXT)
            log("Stepped to preset [%d/%d]: %s" % (next_index + 1, len(presets), base))

    # --- polling ----------------------------------------------------------
    def poll_triggers(self):
        if self.is_busy:
            return

        new_req = tmp_path("lira_new_req.token")
        if os.path.exists(new_req):
            remove(new_req)
            self.current_preset_name = ""
            return

        prev_req = tmp_path("lira_prev_req.token")
        if os.path.exists(prev_req):
            remove(prev_req)
            write_empty("lira_load_ready.token")
            self.step_preset_by_offset(-1)
            return

        next_req = tmp_path("lira_next_req.token")
        if os.path.exists(next_req):
            remove(next_req)
            write_empty("lira_load_ready.token")
            self.step_preset_by_offset(1)
            return

        load_req = tmp_path("lira_load_req.token")
        if os.path.exists(load_req):
            remove(load_req)
            write_empty("lira_load_ready.token")
            remove(tmp_path("lira_load_ready.lira"))
            self.is_busy = True
            self.handle_load_dialog()
            return

        saveas_req = tmp_path("lira_saveas_req.token")
        if os.path.exists(saveas_req):
            remove(saveas_req)
            write_empty("lira_load_ready.token")
            self.is_busy = True
            self.handle_save_as_dialog()
            return

        save_req = tmp_path("lira_save_req.token")
        if os.path.exists(save_req):
            remove(save_req)
            if len(self.current_preset_name) > 0:
                self.handle_quick_overwrite_save()
            else:
                self.is_busy = True
                self.handle_save_as_dialog()
            return

    # --- actions ----------------------------------------------------------
    def handle_quick_overwrite_save(self):
        file_path = os.path.join(PRESETS, self.current_preset_name + ".lira")
        content = read_bytes(tmp_path("lira_current_save.lira"))
        if content is not None:
            ensure_presets_dir()
            if put_bytes(file_path, content):
                log("Overwrote existing preset: " + file_path)
        else:
            log("quick save: lira_current_save.lira missing")

    def _tk_root(self):
        import tkinter  # lazy: headless paths never need it
        root = tkinter.Tk()
        root.withdraw()
        try:
            root.attributes("-topmost", True)
        except Exception:
            pass
        root.update()
        return root

    def handle_load_dialog(self):
        ensure_presets_dir()
        result_path = None
        try:
            from tkinter import filedialog
            root = self._tk_root()
            try:
                result_path = filedialog.askopenfilename(
                    parent=root,
                    title="Select a Pelagos-8 Preset (.lira)",
                    initialdir=PRESETS,
                    filetypes=[("Pelagos-8 Presets", "*.lira"), ("All files", "*")])
            finally:
                root.destroy()
        except Exception as e:
            log("Load dialog unavailable: %r" % (e,))
        log("Load result: %s" % (result_path or "CANCELLED"))

        if result_path and isinstance(result_path, str):
            base = base_name(result_path)
            content = read_bytes(result_path)
            if content is not None:
                self.current_preset_name = base
                put_bytes(tmp_path("lira_load_ready.lira"), content)
                put_bytes(tmp_path("lira_preset_name.txt"), (base + ";\n").encode("utf-8"))
                put_bytes(tmp_path("lira_load_ready.token"), READY_FLAG_TEXT)
                log("Loaded preset %s successfully." % base)
        self.is_busy = False

    def handle_save_as_dialog(self):
        ensure_presets_dir()
        default_name = (self.current_preset_name + ".lira") if self.current_preset_name else "MyPreset.lira"
        result_path = None
        try:
            from tkinter import filedialog
            root = self._tk_root()
            try:
                result_path = filedialog.asksaveasfilename(
                    parent=root,
                    title="Save Pelagos-8 Preset As",
                    initialdir=PRESETS,
                    initialfile=default_name,
                    defaultextension=".lira",
                    filetypes=[("Pelagos-8 Presets", "*.lira"), ("All files", "*")])
            finally:
                root.destroy()
        except Exception as e:
            log("Save As dialog unavailable: %r" % (e,))
        log("Save As result: %s" % (result_path or "CANCELLED"))

        if result_path and isinstance(result_path, str):
            if not result_path.endswith(".lira"):
                result_path += ".lira"
            base = base_name(result_path)
            content = read_bytes(tmp_path("lira_current_save.lira"))
            if content is not None:
                self.current_preset_name = base
                put_bytes(result_path, content)
                # Run the load handshake so the plugin displays the new name.
                put_bytes(tmp_path("lira_load_ready.lira"), content)
                put_bytes(tmp_path("lira_preset_name.txt"), (base + ";\n").encode("utf-8"))
                put_bytes(tmp_path("lira_load_ready.token"), READY_FLAG_TEXT)
                log("Saved As & Loaded preset %s successfully to %s" % (base, result_path))
            else:
                log("save as: lira_current_save.lira missing")
        self.is_busy = False


def acquire_single_instance():
    """One helper per <tmp>; a second copy exits quietly."""
    try:
        import fcntl
        fd = os.open(tmp_path("lira_helper.lock"), os.O_RDWR | os.O_CREAT, 0o644)
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return fd
    except OSError:
        return None


def main():
    try:
        os.makedirs(TMP, exist_ok=True)
    except OSError:
        pass
    try:
        if os.path.getsize(tmp_path("lira_helper.log")) > LOG_CAP_BYTES:
            remove(tmp_path("lira_helper.log"))
    except OSError:
        pass
    if acquire_single_instance() is None:
        log("another helper already owns %s; exiting" % TMP)
        return 0
    ensure_presets_dir()
    helper = Helper()
    while True:
        try:
            helper.poll_triggers()
        except Exception as e:
            log("poll error: %r" % (e,))
            helper.is_busy = False
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    sys.exit(main())
