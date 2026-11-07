#!/bin/bash
# Package a built Camomile-fork VST3 plus the Pelagos-8 patch, helper and docs
# into one release zip that end users unzip and install.
#
#   tools/package_release.sh <macos|windows|linux> <path/to/built/Camomile.vst3> <outdir>
#
# Env: VERSION  release label (default: git describe --tags --always)
#      ARCH     architecture label in the zip name (default: detected / x64)
#
# Output: <outdir>/Pelagos-8-<VERSION>-<platform>-<arch>.zip containing
#   Pelagos-8/Pelagos-8.vst3            the plugin (engine binary + patch + abs/)
#   Pelagos-8/<platform installer>      Install ... (.command / .bat / .sh)
#   Pelagos-8/helper files              the preset dialog helper
#   Pelagos-8/README.txt                short install notes for that platform
#   Pelagos-8/Pelagos-8_Manual.pdf      the manual
#   Pelagos-8/License.txt
set -euo pipefail

PLATFORM="${1:?platform: macos|windows|linux}"
BUILT="${2:?path to built Camomile.vst3}"
OUT="${3:?output directory}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/Pelagos-8_Plugin/Pelagos-8"
VERSION="${VERSION:-$(git -C "$ROOT" describe --tags --always 2>/dev/null || echo dev)}"

[ -d "$BUILT" ] || { echo "FATAL: $BUILT is not a directory"; exit 1; }
[ -d "$ROOT/release" ] || { echo "FATAL: $ROOT/release (platform READMEs) missing"; exit 1; }
mkdir -p "$OUT"; OUT="$(cd "$OUT" && pwd)"

WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT
PKG="$WORK/Pelagos-8"; mkdir -p "$PKG"
V="$PKG/Pelagos-8.vst3"
cp -R "$BUILT" "$V"

case "$PLATFORM" in
  macos)
    BIN="$V/Contents/MacOS/Camomile"
    [ -f "$BIN" ] || { echo "FATAL: $BIN missing"; exit 1; }
    mv "$BIN" "$V/Contents/MacOS/Pelagos-8"
    PL="$V/Contents/Info.plist"
    plutil -replace CFBundleExecutable  -string Pelagos-8 "$PL"
    plutil -replace CFBundleName        -string Pelagos-8 "$PL"
    plutil -replace CFBundleDisplayName -string Pelagos-8 "$PL"
    plutil -replace CFBundleIdentifier  -string com.timhastie.pelagos8 "$PL"
    RES="$V/Contents/Resources"
    ARCH="${ARCH:-$(lipo -archs "$V/Contents/MacOS/Pelagos-8" | tr ' ' '-')}"
    ;;
  windows)
    DLL="$V/Contents/x86_64-win/Camomile.vst3"
    [ -f "$DLL" ] || { echo "FATAL: $DLL missing"; exit 1; }
    mv "$DLL" "$V/Contents/x86_64-win/Pelagos-8.vst3"
    RES="$V/Contents/Resources"
    ARCH="${ARCH:-x64}"
    ;;
  linux)
    SO="$V/Contents/x86_64-linux/Camomile.so"
    [ -f "$SO" ] || { echo "FATAL: $SO missing"; exit 1; }
    mv "$SO" "$V/Contents/x86_64-linux/Pelagos-8.so"
    RES="$V/Contents/Resources"
    ARCH="${ARCH:-x64}"
    ;;
  *) echo "FATAL: unknown platform $PLATFORM"; exit 1 ;;
esac

# The patch: Camomile loads <bundle name>.pd / <bundle name>.txt from Resources.
mkdir -p "$RES/abs"
rm -f "$RES/Camomile.pd" "$RES/Camomile.txt"
cp "$SRC/Pelagos-8.pd" "$SRC/Pelagos-8.txt" "$RES/"
cp "$SRC"/abs/*.pd "$RES/abs/"
grep -q "^code Pel8;" "$RES/Pelagos-8.txt" || { echo "FATAL: Pelagos-8.txt must carry 'code Pel8;' (release identity)"; exit 1; }

# Platform installer + preset helper
case "$PLATFORM" in
  macos)
    cp "$ROOT/Helper/macos/Pelagos-8-helper" "$PKG/"
    cp "$ROOT/Helper/macos/Install Pelagos-8.command" "$ROOT/Helper/macos/Uninstall Pelagos-8.command" "$PKG/"
    chmod +x "$PKG/Pelagos-8-helper" "$PKG"/*.command
    ;;
  windows)
    cp "$ROOT/Helper/windows/Pelagos-8-helper.exe" "$ROOT/Helper/windows/Install Pelagos-8.bat" "$ROOT/Helper/windows/Uninstall Pelagos-8.bat" "$PKG/"
    ;;
  linux)
    cp "$ROOT/Helper/linux/pelagos8-helper.py" "$ROOT/Helper/linux/install-pelagos-8.sh" "$ROOT/Helper/linux/uninstall-pelagos-8.sh" "$PKG/"
    chmod +x "$PKG"/*.sh "$PKG"/*.py
    ;;
esac

cp "$ROOT/release/README-$PLATFORM.txt" "$PKG/README.txt"
cp "$ROOT/docs/Pelagos-8_Manual.pdf" "$PKG/"
cp "$ROOT/License.txt" "$PKG/"

if [ "$PLATFORM" = macos ] && command -v codesign >/dev/null; then
  codesign --force --deep -s - "$V"
  codesign --force -s - "$PKG/Pelagos-8-helper"
fi

ZIP="$OUT/Pelagos-8-$VERSION-$PLATFORM-$ARCH.zip"
rm -f "$ZIP"
(cd "$WORK" && zip -qr "$ZIP" Pelagos-8)
echo "Wrote $ZIP"
unzip -l "$ZIP" | tail -1
