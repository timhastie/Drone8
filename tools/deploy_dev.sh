#!/bin/bash
# Deploy the Path A fork build + current patch to the LIRA-8-DEV VST3.
# ALWAYS use this script - the DEV config MUST carry "code LirD;" or the
# plugin's VST3 class ID collides with production LIRA-8 ("Lira") and
# Ableton hides it from the browser.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEV="$HOME/Library/Audio/Plug-Ins/VST3/LIRA-8-DEV.vst3"
BIN="$ROOT/engine/camomile/build/Camomile_artefacts/Release/VST3/Camomile.vst3/Contents/MacOS/Camomile"
SRC="$ROOT/LIRA-8_Plugin/LIRA-8"

cp "$BIN" "$DEV/Contents/MacOS/LIRA-8-DEV"
cp "$SRC/LIRA-8.pd" "$DEV/Contents/Resources/LIRA-8-DEV.pd"
sed 's/^code Lira;/code LirD;/' "$SRC/LIRA-8.txt" > "$DEV/Contents/Resources/LIRA-8-DEV.txt"
grep -q "^code LirD;" "$DEV/Contents/Resources/LIRA-8-DEV.txt" || { echo "FATAL: code is not LirD"; exit 1; }
rsync -a --delete "$SRC/abs/" "$DEV/Contents/Resources/abs/"
codesign --force --deep -s - "$DEV"
echo "LIRA-8-DEV deployed (code LirD, signed)"
