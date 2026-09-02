#!/bin/bash
# Fetch + patch Camomile v1.0.8-beta10 for the LIRA-8 custom-editor fork (Path A).
# All fork changes live in engine/patches/*.patch (git format-patch series).
set -euo pipefail
cd "$(dirname "$0")"
[ -d camomile ] || git clone --depth 1 --branch v1.0.8-beta10 \
  --recurse-submodules --shallow-submodules \
  https://github.com/pierreguillot/Camomile.git camomile
cd camomile
if ! git log --oneline -1 | grep -q LiraSkin; then
  git -c user.name=lira -c user.email=lira@local am ../patches/*.patch
fi
cmake -B build -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release -DCMAKE_POLICY_VERSION_MINIMUM=3.5
cmake --build build --parallel 8
echo "BUILD OK: build/Camomile_artefacts/Release/{VST3,Standalone}"
