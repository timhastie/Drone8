#!/bin/bash
# Fetch + patch Camomile v1.0.8-beta10 for the LIRA-8 custom-editor fork (Path A).
set -euo pipefail
cd "$(dirname "$0")"
[ -d camomile ] || git clone --depth 1 --branch v1.0.8-beta10 \
  --recurse-submodules --shallow-submodules \
  https://github.com/pierreguillot/Camomile.git camomile
cd camomile
# Makefile-generator fix: ARCHS_STANDARD is Xcode-only; build arm64 dev
python3 - <<'PY'
s=open('CMakeLists.txt').read()
s=s.replace('set(CMAKE_OSX_ARCHITECTURES "$(ARCHS_STANDARD)" CACHE STRING "" FORCE)',
            'set(CMAKE_OSX_ARCHITECTURES "arm64" CACHE STRING "" FORCE)')
s=s.replace('set(CMAKE_OSX_DEPLOYMENT_TARGET "10.9"','set(CMAKE_OSX_DEPLOYMENT_TARGET "10.13"')
open('CMakeLists.txt','w').write(s)
PY
cmake -B build -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release -DCMAKE_POLICY_VERSION_MINIMUM=3.5
cmake --build build --parallel 8 || true   # AU target fails without full Xcode (Rez); VST3 builds
ls Plugins/Camomile.vst3 && echo "BUILD OK (VST3)"
