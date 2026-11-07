Pelagos-8 for Windows  (Windows 10 or 11, 64-bit)

WHAT IS IN THIS FOLDER
  Pelagos-8.vst3               the instrument (VST3 plugin, a folder)
  Pelagos-8-helper.exe         a small background program that shows the
                               preset Save / Load windows for the plugin
  Install Pelagos-8.bat        the installer
  Uninstall Pelagos-8.bat      the uninstaller
  Pelagos-8_Manual.pdf         the manual
  License.txt

INSTALL
  1. Close your DAW first.
  2. Unzip the download: right-click the zip, choose "Extract All".
  3. Open the unzipped Pelagos-8 folder and double-click
     "Install Pelagos-8.bat".
  4. If Windows shows "Windows protected your PC" or "Open File - Security
     Warning", see SECURITY below.
  5. Windows asks once for permission to copy the plugin: a dialog titled
     "Windows Command Processor" asks "Do you want to allow this app to make
     changes to your device?". Click Yes.
  6. When the window says "Done", press any key to close it.
  7. Open your DAW. Pelagos-8 is in its list of VST3 instruments.
     If it is missing, ask the DAW to rescan its plugins.

SECURITY (happens once)
  Pelagos-8 is not registered with Microsoft, so Windows is cautious at first.
  "Windows protected your PC": click the small "More info" text, then click
    the "Run anyway" button that appears.
  If instead you see "Open File - Security Warning" ("The publisher could not
    be verified"): click Run.
  If Windows Defender removes Pelagos-8-helper.exe: open Windows Security >
    Virus & threat protection > Protection history, click the Pelagos-8-helper
    entry, click Actions > Restore. Then under Virus & threat protection
    settings > Manage settings > Exclusions > Add or remove exclusions, add
    the unzipped Pelagos-8 folder as a Folder exclusion, then add a second
    Folder exclusion: type  %APPDATA%\Pelagos-8  in the folder box. Run the
    installer again.
  The installer clears the "downloaded from the internet" mark from the plugin
  and the helper, so you will not be asked about them again.

PRESETS
  Your presets are text files ending in .lira, kept in  Music\Pelagos-8\Presets
  in your user folder. The same files work on Windows, Mac and Linux.
  The Save / Load buttons on the plugin open windows through the helper,
  which starts by itself every time you log in. If a Save / Load window seems
  not to appear, look for it on the taskbar behind your DAW.

UNINSTALL
  Close your DAW, then double-click "Uninstall Pelagos-8.bat". Your presets
  are kept.

HELP
  If something does not work, report it at github.com/timhastie/Drone8/issues
  with a screenshot of the installer window.
