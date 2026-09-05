#!/bin/bash
# Package the Pelagos-8 patch into Camomile's official Windows x64 VST3 binaries.
# Output: Pelagos-8-Windows-x64.zip in the current directory.
set -euo pipefail
PLUG="$(cd "$(dirname "$0")/../Pelagos-8_Plugin/Pelagos-8" && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
curl -sLo "$WORK/cam.zip" \
  "https://github.com/pierreguillot/Camomile/releases/download/v1.0.8-beta10/Camomile-Win64.zip"
unzip -q "$WORK/cam.zip" -d "$WORK"
cp -r "$WORK/Camomile/Camomile.vst3" "$WORK/Pelagos-8.vst3"
mv "$WORK/Pelagos-8.vst3/Contents/x86_64-win/Camomile.vst3" \
   "$WORK/Pelagos-8.vst3/Contents/x86_64-win/Pelagos-8.vst3"
mkdir -p "$WORK/Pelagos-8.vst3/Contents/Resources/abs"
cp "$PLUG/Pelagos-8.pd" "$PLUG/Pelagos-8.txt" "$WORK/Pelagos-8.vst3/Contents/Resources/"
cp "$PLUG"/abs/*.pd "$WORK/Pelagos-8.vst3/Contents/Resources/abs/"
HELPER="$(cd "$(dirname "$0")/../Helper/windows" && pwd)"
if [ ! -f "$HELPER/LIRA-8-helper.exe" ]; then
  x86_64-w64-mingw32-gcc -O2 -municode -mwindows -o "$HELPER/LIRA-8-helper.exe" \
    "$HELPER/lira_helper_win.c" -lcomdlg32 -lshlwapi
fi
cp "$HELPER/LIRA-8-helper.exe" "$HELPER/install_helper.bat" "$HELPER/README-WINDOWS.txt" "$WORK/"
(cd "$WORK" && zip -qr Pelagos-8-Windows-x64.zip Pelagos-8.vst3 LIRA-8-helper.exe install_helper.bat README-WINDOWS.txt)
cp "$WORK/Pelagos-8-Windows-x64.zip" .
echo "Wrote Pelagos-8-Windows-x64.zip (full build incl. preset helper)"
