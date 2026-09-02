# Path A: Camomile fork (custom JUCE editor, Pd engine unchanged)
- `./fetch_camomile.sh` clones + patches + builds Camomile v1.0.8-beta10 (VST3, arm64).
- Dev plugin identity: LIRA-8-DEV (4-char code LirD) in ~/Library/Audio/Plug-Ins/VST3,
  packaged with the current patch from LIRA-8_Plugin/LIRA-8.
- AU target needs full Xcode (legacy Rez step); VST3 suffices for development.
- Phase 2+: standalone target for self-screenshotting, custom editor (front = Lyra-8
  hardware look, sequencer = 303-style fader slots), console button removal,
  param-flood send-on-change fix.
