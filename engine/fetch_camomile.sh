#!/bin/bash
# Fetch + patch Camomile v1.0.8-beta10 for the LIRA-8 custom-editor fork (Path A).
# All fork changes live in engine/patches/*.patch (git format-patch series).
set -euo pipefail
cd "$(dirname "$0")"
[ -d camomile ] || git clone --depth 1 --branch v1.0.8-beta10 \
  --recurse-submodules --shallow-submodules \
  https://github.com/pierreguillot/Camomile.git camomile
cd camomile
# Apply the series only when the clone carries fewer commits past the tag
# than there are patch files (re-running git am on a patched tree fails).
NPATCH=$(ls ../patches/*.patch | wc -l | tr -d ' ')
if [ "$(git rev-list --count v1.0.8-beta10..HEAD)" -lt "$NPATCH" ]; then
  git -c user.name=lira -c user.email=lira@local am ../patches/*.patch
fi
# JUCE's juceaide bootstrap ignores CMAKE_OSX_DEPLOYMENT_TARGET and fails on
# the macOS 15+ SDKs ("CGWindowListCreateImage is unavailable") unless the
# deployment target reaches it through the environment.
if [ "$(uname)" = Darwin ]; then export MACOSX_DEPLOYMENT_TARGET=10.13; fi
cmake -B build -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release -DCMAKE_POLICY_VERSION_MINIMUM=3.5
cmake --build build --parallel 8
echo "BUILD OK: build/Camomile_artefacts/Release/{VST3,Standalone}"
