#!/bin/bash
# Pelagos-8 uninstaller for Linux. Removes the plugin, the preset helper and
# its autostart entry. Your presets in ~/Music/Pelagos-8/Presets are kept.
set -u

VST3="$HOME/.vst3/Pelagos-8.vst3"
HELPER_DIR="$HOME/.local/share/pelagos-8"
DESKTOP="$HOME/.config/autostart/pelagos8-helper.desktop"

echo "Pelagos-8 uninstaller"
echo

pkill -f "[p]elagos8-helper.py" 2>/dev/null && echo "1. Stopped the preset helper." || echo "1. Preset helper was not running."

if [ -e "$VST3" ]; then rm -rf "$VST3"; echo "2. Removed $VST3"; else echo "2. Plugin not found at $VST3 (nothing to remove)."; fi
if [ -e "$HELPER_DIR" ]; then rm -rf "$HELPER_DIR"; echo "3. Removed $HELPER_DIR"; else echo "3. Helper folder not found (nothing to remove)."; fi
if [ -e "$DESKTOP" ]; then rm -f "$DESKTOP"; echo "4. Removed $DESKTOP"; else echo "4. Autostart entry not found (nothing to remove)."; fi
T="${PELAGOS8_TMP:-/tmp}"
rm -f "$T"/lira_*.token "$T"/lira_load_ready.lira "$T"/lira_preset_name.txt "$T"/lira_helper.lock 2>/dev/null

echo
echo "Done. Your presets are still in $HOME/Music/Pelagos-8/Presets."
