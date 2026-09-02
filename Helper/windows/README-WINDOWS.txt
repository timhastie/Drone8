LIRA-8 V2 - Windows x64 (full build: synth + preset SAVE/LOAD)

INSTALL (two steps)
  1. Copy the LIRA-8.vst3 FOLDER (the whole folder) into:
       C:\Program Files\Common Files\VST3\
  2. Double-click install_helper.bat
     This installs the small LIRA-8 preset helper (shows the Save/Load
     dialogs and manages your preset files). It runs in the background,
     starts automatically at login, and uses no meaningful CPU.

  Then start Ableton (rescan plugins if needed).

PRESETS
  NEW / SAVE / SAVE_AS / LOAD and the < > arrows on the plugin work like
  on the Mac. Preset files live in:  Music\LIRA-8\Presets\*.lira
  .lira files are cross-platform - you can copy them between Mac and PC.

NOTES
  - The helper watches C:\tmp (it creates the folder). If your DAW runs
    from a different drive than C:, presets may not connect - tell us.
  - If a Save/Load dialog opens behind Ableton, check the taskbar.
  - Untested-on-real-hardware notice: this is the first Windows build;
    everything is expected to match the Mac version, but if anything
    misbehaves, the file C:\tmp\lira_helper.log helps diagnose it.

Engine: Camomile v1.0.8-beta10 (official Windows release binaries).
