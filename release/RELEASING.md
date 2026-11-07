# Cutting a Pelagos-8 release

End users get one zip per platform from the GitHub Releases page. Each zip
holds `Pelagos-8/` with the VST3, the preset helper, a double-click
installer, `README.txt`, the manual PDF and the licence. `tools/package_release.sh`
builds that layout from a compiled engine bundle; `.github/workflows/release.yml`
runs it on macOS, Windows and Linux runners.

## Identity

`Pelagos-8_Plugin/Pelagos-8/Pelagos-8.txt` carries `code Pel8;`. The upstream
LIRA-8 plugin uses `code Lira;` with the same manufacturer code, so shipping
`Lira` would collide with Mike Moreno's plugin in users' DAWs. The dev plugin on
the maintainer's Mac keeps `LirD` (see `tools/deploy_dev.sh`).

## Steps

1. Commit everything the workflow needs: `.github/workflows/release.yml`,
   `tools/package_release.sh`, `release/README-*.txt`, `Helper/macos/*`,
   `Helper/windows/*`, `Helper/linux/*`, `engine/patches/*`,
   `docs/Pelagos-8_Manual.pdf`. CI checks out committed files only.
2. Push, then run the workflow once by hand (Actions > Release > Run workflow)
   and read the Windows and Linux logs. Those two toolchains have never been
   exercised with this fork; macOS has (locally, Xcode 26.6, universal).
3. Tag and push: `git tag v1.0.0 && git push origin v1.0.0`. The workflow
   attaches `Pelagos-8-v1.0.0-macos-arm64-x86_64.zip`,
   `Pelagos-8-v1.0.0-windows-x64.zip` and `Pelagos-8-v1.0.0-linux-x64.zip`
   to a draft release. Publish the release.
4. Install the macOS zip on a clean user account and run through
   `release/README-macos.txt` before announcing.

## Local macOS build (what CI does, by hand)

```bash
engine/fetch_camomile.sh          # clone + git am patches + universal build
VERSION=v1.0.0 tools/package_release.sh macos \
  engine/camomile/build/Camomile_artefacts/Release/VST3/Camomile.vst3 dist
```

`fetch_camomile.sh` exports `MACOSX_DEPLOYMENT_TARGET=10.13` because JUCE's
juceaide bootstrap ignores the CMake deployment target and fails to compile
against the macOS 15+ SDKs otherwise.

## Preset helper

The helper sources are `Helper/lira_dialog_helper.m` (macOS, build with
`clang -fobjc-arc -framework Cocoa -O2 -arch arm64 -arch x86_64
-mmacosx-version-min=10.13 -o Helper/macos/Pelagos-8-helper Helper/lira_dialog_helper.m`),
`Helper/windows/lira_helper_win.c` (build with
`x86_64-w64-mingw32-gcc -O2 -municode -mwindows -o Helper/windows/Pelagos-8-helper.exe
Helper/windows/lira_helper_win.c -lcomdlg32 -lshlwapi`) and
`Helper/linux/pelagos8-helper.py`. All three watch the same token files in
`/tmp` (`C:\tmp` on Windows) and keep presets in `Music/Pelagos-8/Presets`.
Rebuild and commit the binaries whenever the sources change.
