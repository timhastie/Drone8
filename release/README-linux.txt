Pelagos-8 for Linux (VST3 instrument, 64-bit x86)

WHAT IS IN THIS FOLDER
  Pelagos-8.vst3            the instrument
  install-pelagos-8.sh      installs everything for you
  uninstall-pelagos-8.sh    removes it again (your presets are kept)
  pelagos8-helper.py        small background program that shows the preset
                            Save / Load windows (the plugin cannot do that itself)
  Pelagos-8_Manual.pdf      the manual
  License.txt

INSTALL
  1. Unzip the download. Keep all the files together in one folder.
  2. Open a Terminal in that folder (in your file manager: right-click the
     folder and choose "Open in Terminal", or drag the folder onto the
     Terminal icon).
  3. Type this and press Enter:

        bash install-pelagos-8.sh

  4. Read what it prints. If it says python3 or tkinter is missing, copy the
     one-line command it shows, run it, then run step 3 again.
     (Debian/Ubuntu:  sudo apt install python3 python3-tk
      Fedora:         sudo dnf install python3 python3-tkinter
      Arch:           sudo pacman -S python tk)
  5. Start your DAW (Reaper, Bitwig, Ardour, ...) and rescan plugins. Add
     "Pelagos-8" as a VST3 instrument. If the DAW does not find it, add
     the folder  ~/.vst3  to its VST3 search paths and rescan.

IF SOMETHING WILL NOT RUN
  - "Permission denied": you double-clicked the file or typed
    ./install-pelagos-8.sh. Use the command from step 3 instead
    (bash install-pelagos-8.sh); it needs no special permission.
  - Your file manager asks "Run in Terminal / Display / Cancel" when you
    double-click the .sh file: choose "Run in Terminal".
  - Your DAW is installed as a Flatpak or Snap: the preset buttons
    (NEW / SAVE / LOAD / < >) will not work, and the DAW may not find the
    plugin, because it runs in a sandbox that cannot see the folders the
    helper uses. Install the DAW from its normal download (.deb, .rpm,
    .tar.gz or AppImage) instead.
  - Nothing is signed. There is no virus warning on Linux, but the plugin is
    an unknown program to your system; the installer only writes into your
    own home folder (~/.vst3, ~/.local/share/pelagos-8, ~/.config/autostart,
    ~/Music/Pelagos-8). It never asks for your password.

PRESETS
  NEW / SAVE / SAVE AS / LOAD and the < > arrows on the plugin save and load
  preset files. They live in:   ~/Music/Pelagos-8/Presets/*.lira
  .lira files are plain text and work on Mac, Windows and Linux: you can copy
  them between computers.
  The Save / Load window is opened by the helper, which starts automatically
  when you log in. If no window appears, log out and in again, or open a
  Terminal and run:

        nohup python3 ~/.local/share/pelagos-8/pelagos8-helper.py >/dev/null 2>&1 &

  You can close that Terminal afterwards; the helper keeps running.
  If a Save / Load window opens behind your DAW, look in your taskbar.

UNINSTALL
  Open a Terminal in this folder and type:   bash uninstall-pelagos-8.sh
  Your presets in ~/Music/Pelagos-8/Presets stay where they are.

WHERE THINGS GO
  Plugin     ~/.vst3/Pelagos-8.vst3
  Helper     ~/.local/share/pelagos-8/pelagos8-helper.py
  Autostart  ~/.config/autostart/pelagos8-helper.desktop
  Presets    ~/Music/Pelagos-8/Presets
  Log        /tmp/lira_helper.log   (helps if something misbehaves)

Engine: Camomile v1.0.8-beta10 (JUCE + Pure Data), built for Linux x86-64.

HELP
  If something does not work, report it at github.com/timhastie/Drone8/issues
  with a screenshot of the installer window.
