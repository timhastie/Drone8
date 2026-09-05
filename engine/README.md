# Path A: Camomile fork (custom JUCE editor, Pd engine unchanged)
- `./fetch_camomile.sh` clones + patches + builds Camomile v1.0.8-beta10 (VST3, arm64).
- Dev plugin identity: LIRA-8-DEV (4-char code LirD) in ~/Library/Audio/Plug-Ins/VST3,
  packaged with the current patch from Pelagos-8_Plugin/Pelagos-8.
- AU target needs full Xcode (legacy Rez step); VST3 suffices for development.
- Phase 2+: standalone target for self-screenshotting, custom editor (front = Lyra-8
  hardware look, sequencer = 303-style fader slots), console button removal,
  param-flood send-on-change fix.

## Skin (LiraSkin.hpp)

All widget painting is intercepted in the fork (`Source/LiraSkin.hpp` +
`PluginEditorObject.cpp` paint bodies). Style is chosen from each widget's
declared Pd colors + geometry, so the Pd patch stays the single source of
truth for layout/behavior:

- vsl/hsl: recessed slot + ridged fader cap (black cap on light panels,
  silver cap on dark pages)
- tgl: <=11px -> LED lamp; dark bg -> rounded step pad (green glow when on);
  light bg -> rocker switch
- bng: metal push button; dark-on-dark ("ghost" arrow bangs) -> faint ring
- radio: segmented switch strip
- cnv: full plates get gradient+vignette; label bars get gloss; small/thin
  cnv (masks, bracket lines) stay exact flat fills

## Screenshot loop

Run the packaged Standalone with `LIRA_SNAPSHOT=/path/out.png` (and optional
`LIRA_SNAPSHOT_TICKS=n`, 25ms/tick) - it renders the editor, saves a PNG and
quits. To capture a sequencer page, append a `pd liraopen` subpatch to the
packaged Camomile.pd: loadbang -> delay 600 -> `s $0-s-sq-open` (or -pgp,
-pgf, -pgm, -pgm2). processBlock has a channel adapter so a stereo device
can host the 22-out patch (Pd time keeps advancing; no OOB channels).
