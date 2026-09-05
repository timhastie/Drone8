# LIRA-8 sequencer generator toolchain

The sequencer overlay, per-lane clocks, filter/mod pages, preset
persistence and most of the main canvas of `Pelagos-8.pd` (~7,400 objects)
are **generated**, not hand-written. To change the sequencer, edit the
generator and regenerate — do not hand-edit the generated block.

## Files
- `generate_sequencer.py` — the generator (evolution of gen1..gen23).
  Reads `base.pd`, applies base edits (receives, geometry re-flows),
  emits all overlay widgets/engines/dispatch tables, writes `work.pd`.
- `pd_parse.py` — minimal .pd parser used for validation (index-range
  checks, geometry queries). Import its `parse()` via exec of the text
  before "cvs=parse".
- `base.pd` — snapshot of Pelagos-8.pd *before* the generated block
  (post-vibrato, pre-sequencer). The generator's input.

## Regenerating
```bash
python3 generate_sequencer.py   # reads base.pd, writes work.pd
cp work.pd ../Pelagos-8_Plugin/Pelagos-8/Pelagos-8.pd
```
Then deploy: copy Pelagos-8.pd (and any changed abs/*.pd) into all FIVE
installed bundles and ad-hoc re-sign each:
/Library/Audio/Plug-Ins/{Components,VST3,VST}/LIRA-8.* and
~/Library/Audio/Plug-Ins/{VST3,VST}/LIRA-8.*, then
`codesign --force --deep -s - <bundle>`; validate with
`auval -v aumu Lira PIGU`; fully restart Ableton.

## Testing headless
Pd (brew cask "pd") runs the whole engine without a host:
`pd -nogui -noaudio -noprefs -path abs Pelagos-8.pd harness.pd`, where the
harness sends `; playhead position <ppq> 0 0`, `; playhead bpm <n>`,
`; playhead playing <0|1>` and probes via appended `[r]`→`[print]`
objects. The pristine patch prints 8 benign "float: no such object"
errors.

## Hard-won gotchas (violate these and the patch breaks silently)
- Pd connects are positional: append objects only at the end; connect
  lines must appear after the objects they reference.
- Trigger outlets fire right-to-left; a `t f` outlet into `[f]`'s left
  inlet overwrites-and-outputs — use a `b` outlet to read a store.
- `$0` does not expand inside message boxes — compose targets with
  `makefilename \$0-%s` into an argless settable `[s]`.
- iemgui `label <float>` messages are silently dropped — labels must be
  symbols ("x2", "1/4").
- iemgui `color` messages use 24-bit encoding (-1-0xRRGGBB); the file
  format's stored colors are legacy 18-bit. They are not interchangeable.
- Camomile re-raises all label components on every `gui redraw`; any
  labeled decoration must be parked off-canvas while the overlay is
  open. cnv panels and JUCE labels never intercept clicks.
- Camomile playhead sends `bpm` (never `tempo`), `playing`, and
  `position <ppq> <samples> <secs>` every block.
- Preset system: save fan is obj 558 in lira.preset.pd (outlet 5 clear,
  4 capture bangs, 3 write); the load route chain is extended from
  route-53's reject outlet.
