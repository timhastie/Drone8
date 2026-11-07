#!/bin/bash
# Pelagos-8 installer for macOS (12 and newer, Apple Silicon and Intel).
# Double-click this file. It installs for the current user only, no password needed.
#
# What it does:
#   1. removes the "downloaded from the internet" flag from the shipped files
#   2. copies Pelagos-8.vst3 into ~/Library/Audio/Plug-Ins/VST3
#   3. stops any running preset helper, then copies the new one into
#      ~/Library/Application Support/Pelagos-8
#   4. registers the helper to start at login (LaunchAgent) and starts it now
#   5. creates ~/Music/Pelagos-8/Presets
#
# Testing note: PELAGOS8_SKIP_LAUNCHCTL=1 skips the launchctl calls in steps 3 and 4
# (used when running the script against a fake $HOME).
set -e
trap 'echo; echo "Something went wrong at the step above, so Pelagos-8 was not fully installed."; echo "The steps printed above it did complete; the ones after it did not."; echo "Take a screenshot of this window and report it at github.com/timhastie/Drone8/issues"; echo; read -p "Press Return to close" _' ERR

HERE="$(cd "$(dirname "$0")" && pwd)"
LABEL="com.timhastie.pelagos8.helper"
OLD_LABEL="com.pigula.lira8.helper"
VST3_DIR="$HOME/Library/Audio/Plug-Ins/VST3"
HELPER_DIR="$HOME/Library/Application Support/Pelagos-8"
AGENTS_DIR="$HOME/Library/LaunchAgents"
PLIST="$AGENTS_DIR/$LABEL.plist"
PRESETS="$HOME/Music/Pelagos-8/Presets"
UID_NUM="$(id -u)"

echo
echo "Installing Pelagos-8..."
echo

if [ ! -d "$HERE/Pelagos-8.vst3" ] || [ ! -f "$HERE/Pelagos-8-helper" ]; then
    echo "Could not find Pelagos-8.vst3 and Pelagos-8-helper next to this installer."
    echo "Please unzip the whole download first, then double-click the installer"
    echo "inside the unzipped Pelagos-8 folder."
    echo
    echo "If macOS just asked \"Terminal would like to access files in your Downloads"
    echo "folder\" and you clicked Don't Allow, that is the reason. Open"
    echo "System Settings > Privacy & Security > Files and Folders > Terminal,"
    echo "switch on Downloads Folder, then double-click the installer again."
    echo
    read -p "Press Return to close" _ || true
    exit 1
fi

# 1. Clear the quarantine flag from the shipped items only, so macOS lets the
#    plugin and helper run. (Not the whole folder: the user may have put these
#    files straight into ~/Downloads.)
xattr -dr com.apple.quarantine "$HERE/Pelagos-8.vst3" "$HERE/Pelagos-8-helper" "$HERE"/*.command 2>/dev/null || true

# 2. The plugin.
mkdir -p "$VST3_DIR"
rm -rf "$VST3_DIR/Pelagos-8.vst3"
cp -R "$HERE/Pelagos-8.vst3" "$VST3_DIR/Pelagos-8.vst3"
xattr -dr com.apple.quarantine "$VST3_DIR/Pelagos-8.vst3" 2>/dev/null || true
echo "Plugin installed:  $VST3_DIR/Pelagos-8.vst3"

# 3. The preset helper. Stop an earlier copy first (and its KeepAlive agent),
#    then remove the old binary so the new one gets a fresh file.
if [ -z "$PELAGOS8_SKIP_LAUNCHCTL" ]; then
    launchctl bootout "gui/$UID_NUM/$LABEL" >/dev/null 2>&1 || true
fi
pkill -x Pelagos-8-helper >/dev/null 2>&1 || true
mkdir -p "$HELPER_DIR"
rm -f "$HELPER_DIR/Pelagos-8-helper"
cp "$HERE/Pelagos-8-helper" "$HELPER_DIR/Pelagos-8-helper"
chmod +x "$HELPER_DIR/Pelagos-8-helper"
xattr -d com.apple.quarantine "$HELPER_DIR/Pelagos-8-helper" 2>/dev/null || true
echo "Helper installed:  $HELPER_DIR/Pelagos-8-helper"

# 4. Start the helper at login. The path must be the real absolute path, no "~".
mkdir -p "$AGENTS_DIR"
cat > "$PLIST" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$LABEL</string>
    <key>ProgramArguments</key>
    <array>
        <string>$HELPER_DIR/Pelagos-8-helper</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
PLIST

if [ -z "$PELAGOS8_SKIP_LAUNCHCTL" ]; then
    # The earlier copy was booted out in step 3; load this one (one retry).
    sleep 1
    if launchctl bootstrap "gui/$UID_NUM" "$PLIST" >/dev/null 2>&1 \
       || { sleep 2; launchctl bootstrap "gui/$UID_NUM" "$PLIST" >/dev/null 2>&1; }; then
        echo "Helper started. It will start by itself every time you log in."
    else
        echo
        echo "NOTE: the helper could not be started right now. Everything is installed,"
        echo "and the helper will start by itself the next time you log in. If you want"
        echo "it now, log out and back in, or restart your Mac."
        echo
    fi
else
    echo "(launchctl skipped: PELAGOS8_SKIP_LAUNCHCTL is set)"
fi

# 5. Preset folder.
mkdir -p "$PRESETS"
echo "Presets folder:    $PRESETS"

# An old LIRA-8 helper uses the same message files and would fight with this one.
if pgrep -x lira_dialog_helper >/dev/null 2>&1 || [ -f "$AGENTS_DIR/$OLD_LABEL.plist" ]; then
    echo
    echo "WARNING: an older LIRA-8 preset helper (lira_dialog_helper) is on this Mac."
    echo "It uses the same message files as Pelagos-8 and the two will get in each"
    echo "other's way. To stop it, paste these two lines into Terminal:"
    echo
    echo "  launchctl bootout gui/$UID_NUM/$OLD_LABEL"
    echo "  rm -f \"$AGENTS_DIR/$OLD_LABEL.plist\""
    echo
fi

echo
echo "Done. Pelagos-8 is installed."
echo "macOS may now show a notice that an item was added that can run in the"
echo "background. That is the Pelagos-8 preset helper. Leave it switched on."
echo
echo "Quit and reopen your DAW, then look for Pelagos-8 in its VST3 instruments."
echo "(If it does not show up, ask your DAW to rescan its plugins.)"
echo
read -p "Press Return to close" _ || true
