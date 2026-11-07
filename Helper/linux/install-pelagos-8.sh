#!/bin/bash
# Pelagos-8 installer for Linux (VST3 + preset helper). Run from the unzipped
# Pelagos-8 folder:   bash install-pelagos-8.sh
set -u

HERE="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_SRC="$HERE/Pelagos-8.vst3"
HELPER_SRC="$HERE/pelagos8-helper.py"

VST3_DIR="$HOME/.vst3"
HELPER_DIR="$HOME/.local/share/pelagos-8"
HELPER="$HELPER_DIR/pelagos8-helper.py"
AUTOSTART_DIR="$HOME/.config/autostart"
DESKTOP="$AUTOSTART_DIR/pelagos8-helper.desktop"
PRESETS="$HOME/Music/Pelagos-8/Presets"

echo "Pelagos-8 installer"
echo

[ -d "$PLUGIN_SRC" ] || { echo "ERROR: Pelagos-8.vst3 was not found next to this script ($HERE)."; exit 1; }
[ -f "$HELPER_SRC" ] || { echo "ERROR: pelagos8-helper.py was not found next to this script ($HERE)."; exit 1; }

# --- python3 + tkinter check -------------------------------------------------
tk_hint() {
    local id="" like=""
    if [ -r /etc/os-release ]; then
        id="$(. /etc/os-release; echo "${ID:-}")"
        like="$(. /etc/os-release; echo "${ID_LIKE:-}")"
    fi
    case " $id $like " in
        *debian*|*ubuntu*|*mint*|*pop*)  echo "sudo apt install python3 python3-tk" ;;
        *fedora*|*rhel*|*centos*|*nobara*) echo "sudo dnf install python3 python3-tkinter" ;;
        *arch*|*manjaro*|*endeavouros*)  echo "sudo pacman -S python tk" ;;
        *suse*)                          echo "sudo zypper install python3 python3-tk" ;;
        *) echo "install python3 and its tkinter package (python3-tk on Debian/Ubuntu, python3-tkinter on Fedora, tk on Arch)" ;;
    esac
}

# Prefer the system interpreter (the distro's tkinter package installs into it),
# so the autostart entry does not depend on a pyenv/conda shim that may vanish.
PYTHON3=/usr/bin/python3
[ -x "$PYTHON3" ] || PYTHON3="$(command -v python3 2>/dev/null || true)"

PY_OK=1
if [ -z "$PYTHON3" ]; then
    PY_OK=0
    PYTHON3=python3
    echo "WARNING: python3 is not installed. The preset Save/Load helper needs it."
    echo "         Install it with:   $(tk_hint)"
    echo "         then run this installer again."
elif ! "$PYTHON3" -c "import tkinter" >/dev/null 2>&1; then
    PY_OK=0
    echo "WARNING: python3 is installed but tkinter is missing. The preset Save/Load dialogs need it."
    echo "         Install it with:   $(tk_hint)"
    echo "         then run this installer again."
fi
echo

# --- plugin ------------------------------------------------------------------
mkdir -p "$VST3_DIR"
rm -rf "$VST3_DIR/Pelagos-8.vst3"
cp -R "$PLUGIN_SRC" "$VST3_DIR/Pelagos-8.vst3" || { echo "ERROR: could not copy the plugin to $VST3_DIR"; exit 1; }
echo "1. Plugin installed:      $VST3_DIR/Pelagos-8.vst3"

# --- helper ------------------------------------------------------------------
mkdir -p "$HELPER_DIR"
cp "$HELPER_SRC" "$HELPER" || { echo "ERROR: could not copy the helper to $HELPER_DIR"; exit 1; }
chmod +x "$HELPER"
echo "2. Preset helper installed: $HELPER"

# --- autostart at login ------------------------------------------------------
mkdir -p "$AUTOSTART_DIR"
cat > "$DESKTOP" <<EOF
[Desktop Entry]
Type=Application
Name=Pelagos-8 Preset Helper
Comment=Shows the Save/Load preset dialogs for the Pelagos-8 plugin
Exec=$PYTHON3 "$HELPER"
Terminal=false
NoDisplay=true
X-GNOME-Autostart-enabled=true
EOF
echo "3. Autostart entry written: $DESKTOP"

# --- presets folder ----------------------------------------------------------
mkdir -p "$PRESETS"
echo "4. Presets folder:        $PRESETS"

# --- (re)start the helper now ------------------------------------------------
pkill -f "[p]elagos8-helper.py" 2>/dev/null && sleep 0.5
if [ "$PY_OK" = 1 ]; then
    if command -v setsid >/dev/null 2>&1; then
        setsid nohup "$PYTHON3" "$HELPER" >/dev/null 2>&1 < /dev/null &
    else
        nohup "$PYTHON3" "$HELPER" >/dev/null 2>&1 < /dev/null &
    fi
    disown 2>/dev/null || true
    sleep 0.5
    if pgrep -f "[p]elagos8-helper.py" >/dev/null 2>&1; then
        echo "5. Preset helper is running (it will also start automatically when you log in)."
    else
        echo "5. WARNING: the preset helper did not start. See /tmp/lira_helper.log"
    fi
else
    echo "5. Preset helper NOT started (python3/tkinter missing, see above)."
fi

echo
echo "Done. Start your DAW, rescan plugins, and look for Pelagos-8 under VST3 instruments."
