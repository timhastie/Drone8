@echo off
rem LIRA-8 preset helper installer: copies the helper to %APPDATA%\LIRA-8,
rem adds a Startup shortcut so it runs at login, and starts it now.
set DEST=%APPDATA%\LIRA-8
if not exist "%DEST%" mkdir "%DEST%"
copy /Y "%~dp0LIRA-8-helper.exe" "%DEST%\LIRA-8-helper.exe" >nul
powershell -NoProfile -Command ^
  "$s=(New-Object -ComObject WScript.Shell).CreateShortcut([Environment]::GetFolderPath('Startup')+'\LIRA-8 Helper.lnk');" ^
  "$s.TargetPath='%DEST%\LIRA-8-helper.exe';$s.Save()"
start "" "%DEST%\LIRA-8-helper.exe"
echo LIRA-8 helper installed and started. It will run automatically at login.
echo (To remove: delete "%DEST%" and the "LIRA-8 Helper" shortcut in shell:startup)
pause
