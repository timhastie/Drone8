#!/bin/bash
# Pelagos-8 uninstaller for macOS. Double-click this file.
# Removes the plugin, the preset helper and its login item.
# Your presets in ~/Music/Pelagos-8/Presets are left alone.
#
# Testing note: PELAGOS8_SKIP_LAUNCHCTL=1 skips the launchctl call.
set -e
trap 'echo; echo "Something went wrong at the step above, so Pelagos-8 was not fully removed."; echo "The steps printed above it did complete; the ones after it did not."; echo "Take a screenshot of this window and report it at github.com/timhastie/Drone8/issues"; echo; read -p "Press Return to close" _' ERR

LABEL="com.timhastie.pelagos8.helper"
VST3="$HOME/Library/Audio/Plug-Ins/VST3/Pelagos-8.vst3"
HELPER_DIR="$HOME/Library/Application Support/Pelagos-8"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
UID_NUM="$(id -u)"

echo
echo "Uninstalling Pelagos-8..."
echo

if [ -z "$PELAGOS8_SKIP_LAUNCHCTL" ]; then
    launchctl bootout "gui/$UID_NUM/$LABEL" >/dev/null 2>&1 || true
fi
pkill -x Pelagos-8-helper >/dev/null 2>&1 || true

rm -f "$PLIST"
echo "Removed login item."
rm -rf "$HELPER_DIR"
echo "Removed helper:  $HELPER_DIR"
rm -rf "$VST3"
echo "Removed plugin:  $VST3"

echo
echo "Done. Pelagos-8 has been removed."
echo "Your presets were NOT deleted. They are still in:"
echo "  $HOME/Music/Pelagos-8/Presets"
echo "Delete that folder yourself if you no longer want them."
echo
read -p "Press Return to close" _ || true
