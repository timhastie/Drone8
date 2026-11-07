#!/bin/bash
# Deploy the Path A fork build + current patch to the Pelagos-8-DEV VST3.
# The bundle is named Pelagos-8-DEV so it can live next to an installed release
# (Pelagos-8.vst3, code Pel8); Camomile loads <bundle name>.pd/.txt.
# ALWAYS use this script - the dev config MUST carry "code LirD;" or the
# plugin's VST3 class ID collides with the legacy production LIRA-8 ("Lira")
# and Ableton hides it from the browser.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEV="$HOME/Library/Audio/Plug-Ins/VST3/Pelagos-8-DEV.vst3"
BIN="$ROOT/engine/camomile/build/Camomile_artefacts/Release/VST3/Camomile.vst3/Contents/MacOS/Camomile"
SRC="$ROOT/Pelagos-8_Plugin/Pelagos-8"

cp "$BIN" "$DEV/Contents/MacOS/Pelagos-8-DEV"
cp "$SRC/Pelagos-8.pd" "$DEV/Contents/Resources/Pelagos-8-DEV.pd"
sed 's/^code Pel8;/code LirD;/' "$SRC/Pelagos-8.txt" > "$DEV/Contents/Resources/Pelagos-8-DEV.txt"
grep -q "^code LirD;" "$DEV/Contents/Resources/Pelagos-8-DEV.txt" || { echo "FATAL: code is not LirD"; exit 1; }
rsync -a --delete "$SRC/abs/" "$DEV/Contents/Resources/abs/"
codesign --force --deep -s - "$DEV"
echo "Pelagos-8-DEV deployed (code LirD, signed)"
