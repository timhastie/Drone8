Pelagos-8 for macOS  (macOS 12 or newer, Apple Silicon and Intel Macs)

WHAT IS IN THIS FOLDER
  Pelagos-8.vst3                 the instrument (VST3 plugin)
  Pelagos-8-helper               a small background program that shows the
                                 preset Save / Load windows for the plugin
  Install Pelagos-8.command      the installer
  Uninstall Pelagos-8.command    the uninstaller
  Pelagos-8_Manual.pdf           the manual
  License.txt

INSTALL
  1. Close your DAW first.
  2. Double-click "Install Pelagos-8.command".
  3. If macOS refuses to open it, follow SECURITY below, then double-click
     it again.
  4. A Terminal window shows what is being installed. If macOS asks whether
     Terminal may access your Downloads folder, click Allow. When the window
     says "Done", press Return, then close the Terminal window. No password
     is needed.
  5. Open your DAW. Pelagos-8 is in its list of VST3 instruments.
     If it is missing, ask the DAW to rescan its plugins.

SECURITY (happens once, on the first install)
  Pelagos-8 is not registered with Apple, so macOS blocks the installer once.
  macOS 15 or newer: the message has no "Open" button. Click Done, then open
    System Settings > Privacy & Security, scroll down to the Security section
    and click "Open Anyway" next to "Install Pelagos-8.command". Enter your
    Mac login password or Touch ID, then click "Open Anyway" (or "Open") in
    the message that follows. Do this right after the message appeared; the
    button disappears after a while. If it is gone, double-click the installer
    again to bring it back.
  macOS 12, 13, 14: right-click (or Control-click) the installer, choose Open,
    then click Open in the message.
  While installing, macOS may ask: "Terminal would like to access files in
    your Downloads folder". Click Allow (or OK). If you clicked Don't Allow,
    open System Settings > Privacy & Security > Files and Folders > Terminal,
    switch on Downloads Folder, then double-click the installer again.
  After the install, macOS shows a notification that an item was added that
    can run in the background. That is the Pelagos-8 preset helper. Leave it
    switched on (System Settings > General > Login Items & Extensions >
    Allow in the Background) or the Save / Load buttons will do nothing.
  The installer clears the same block from the plugin and the helper, so your
  DAW will load them without further questions.

PRESETS
  Your presets are text files ending in .lira, kept in  Music/Pelagos-8/Presets
  in your home folder. The same files work on Mac, Windows and Linux.
  The Save / Load buttons on the plugin open windows through the helper,
  which starts by itself every time you log in.

UNINSTALL
  Double-click "Uninstall Pelagos-8.command". Your presets are kept.

HELP
  If something does not work, report it at github.com/timhastie/Drone8/issues
  with a screenshot of the installer window.
