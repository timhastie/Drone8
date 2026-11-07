@echo off
rem Pelagos-8 installer for Windows 10 / 11 (64-bit). Double-click this file.
rem
rem   1. installs the preset helper to %APPDATA%\Pelagos-8 and makes it start at login
rem   2. creates %USERPROFILE%\Music\Pelagos-8\Presets
rem   3. copies Pelagos-8.vst3 into C:\Program Files\Common Files\VST3
rem      (step 3 needs administrator rights, so Windows will ask once)
rem
rem All paths are taken from this file's own folder, not the current directory.
setlocal
set "HERE=%~dp0"
set "VST3DIR=%ProgramFiles%\Common Files\VST3"
set "DEST=%APPDATA%\Pelagos-8"
set "PRESETS=%USERPROFILE%\Music\Pelagos-8\Presets"

if /i "%~1"=="/plugin" goto :plugin_only

echo.
echo Installing Pelagos-8...
echo.

if not exist "%HERE%Pelagos-8.vst3\Contents\x86_64-win\Pelagos-8.vst3" goto :missing
if not exist "%HERE%Pelagos-8-helper.exe" goto :missing

rem Remove the "downloaded from the internet" mark from the unzipped files so
rem SmartScreen does not stop the helper and the plugin after they are installed.
powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-ChildItem -LiteralPath '%HERE%Pelagos-8.vst3' -Recurse -Force | Unblock-File -ErrorAction SilentlyContinue; Unblock-File -LiteralPath '%HERE%Pelagos-8-helper.exe','%HERE%Install Pelagos-8.bat','%HERE%Uninstall Pelagos-8.bat' -ErrorAction SilentlyContinue" >nul 2>&1

rem --- 1. preset helper (runs as you, no admin needed) ---
taskkill /F /IM Pelagos-8-helper.exe >nul 2>&1
taskkill /F /IM LIRA-8-helper.exe >nul 2>&1
timeout /t 1 /nobreak >nul
if not exist "%DEST%" mkdir "%DEST%"
copy /Y "%HERE%Pelagos-8-helper.exe" "%DEST%\Pelagos-8-helper.exe" >nul
if errorlevel 1 (
    echo Could not copy the helper to "%DEST%".
    goto :fail
)
powershell -NoProfile -ExecutionPolicy Bypass -Command "Unblock-File -LiteralPath '%DEST%\Pelagos-8-helper.exe' -ErrorAction SilentlyContinue" >nul 2>&1
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$su=[Environment]::GetFolderPath('Startup');" ^
  "Remove-Item -LiteralPath ($su+'\LIRA-8 Helper.lnk') -ErrorAction SilentlyContinue;" ^
  "$s=(New-Object -ComObject WScript.Shell).CreateShortcut($su+'\Pelagos-8 Helper.lnk');" ^
  "$s.TargetPath='%DEST%\Pelagos-8-helper.exe';$s.WorkingDirectory='%DEST%';$s.Save()"
start "" "%DEST%\Pelagos-8-helper.exe"
echo Helper installed:  %DEST%\Pelagos-8-helper.exe
echo                    (starts by itself every time you log in)

rem --- 2. preset folder ---
if not exist "%PRESETS%" mkdir "%PRESETS%"
echo Presets folder:    %PRESETS%

rem --- 3. plugin (needs admin) ---
net session >nul 2>&1
if not errorlevel 1 (
    call :copy_plugin
) else (
    echo.
    echo Windows will now ask for permission to copy the plugin into
    echo "%VST3DIR%". Please click Yes.
    set "ME=%~f0"
    setlocal enabledelayedexpansion
    set "ME=!ME:'=''!"
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '!ME!' -ArgumentList '/plugin' -Verb RunAs -Wait" >nul 2>&1
    endlocal
)
if not exist "%VST3DIR%\Pelagos-8.vst3\Contents\x86_64-win\Pelagos-8.vst3" (
    echo.
    echo The plugin was NOT copied to "%VST3DIR%".
    echo Close your DAW ^(and any plugin scanner^), then run the installer again.
    echo If it still fails, right-click "Install Pelagos-8.bat" and choose
    echo "Run as administrator".
    goto :fail
)
echo Plugin installed:  %VST3DIR%\Pelagos-8.vst3

echo.
echo Done. Pelagos-8 is installed.
echo Quit and reopen your DAW, then look for Pelagos-8 in its VST3 instruments.
echo (If it does not show up, ask your DAW to rescan its plugins.)
echo.
pause
exit /b 0

:plugin_only
rem Elevated child: only the plugin copy. Prints and waits only on failure.
call :copy_plugin
if not exist "%VST3DIR%\Pelagos-8.vst3\Contents\x86_64-win\Pelagos-8.vst3" (
    echo The plugin could not be copied to "%VST3DIR%".
    echo Close your DAW ^(and any plugin scanner^), then run the installer again.
    echo If it still fails, right-click "Install Pelagos-8.bat" and choose
    echo "Run as administrator".
    pause
    exit /b 1
)
exit /b 0

:copy_plugin
if not exist "%VST3DIR%" mkdir "%VST3DIR%"
if exist "%VST3DIR%\Pelagos-8.vst3" rmdir /S /Q "%VST3DIR%\Pelagos-8.vst3"
xcopy "%HERE%Pelagos-8.vst3" "%VST3DIR%\Pelagos-8.vst3\" /E /I /Y /Q >nul
exit /b 0

:missing
echo Could not find Pelagos-8.vst3 and Pelagos-8-helper.exe next to this installer.
echo Please unzip the whole download first (right-click the zip, "Extract All"),
echo then double-click the installer inside the unzipped Pelagos-8 folder.
:fail
echo.
pause
exit /b 1
