#!/bin/bash
# Package the LIRA-8 patch into Camomile's official Windows x64 VST3 binaries.
# Output: LIRA-8-Windows-x64.zip in the current directory.
set -euo pipefail
PLUG="$(cd "$(dirname "$0")/../LIRA-8_Plugin/LIRA-8" && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
curl -sLo "$WORK/cam.zip" \
  "https://github.com/pierreguillot/Camomile/releases/download/v1.0.8-beta10/Camomile-Win64.zip"
unzip -q "$WORK/cam.zip" -d "$WORK"
cp -r "$WORK/Camomile/Camomile.vst3" "$WORK/LIRA-8.vst3"
mv "$WORK/LIRA-8.vst3/Contents/x86_64-win/Camomile.vst3" \
   "$WORK/LIRA-8.vst3/Contents/x86_64-win/LIRA-8.vst3"
mkdir -p "$WORK/LIRA-8.vst3/Contents/Resources/abs"
cp "$PLUG/LIRA-8.pd" "$PLUG/LIRA-8.txt" "$WORK/LIRA-8.vst3/Contents/Resources/"
cp "$PLUG"/abs/*.pd "$WORK/LIRA-8.vst3/Contents/Resources/abs/"
(cd "$WORK" && zip -qr LIRA-8-Windows-x64.zip LIRA-8.vst3)
cp "$WORK/LIRA-8-Windows-x64.zip" .
echo "Wrote LIRA-8-Windows-x64.zip"
echo "NOTE: the .lira preset buttons (NEW/SAVE/SAVE_AS/LOAD) do not work on"
echo "Windows (macOS-only helper); everything else is expected to work."
