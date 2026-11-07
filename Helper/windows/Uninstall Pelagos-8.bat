@echo off
rem Pelagos-8 uninstaller for Windows. Double-click this file.
rem Removes the preset helper, its login shortcut and the plugin.
rem Your presets in Music\Pelagos-8\Presets are left alone.
setlocal
set "VST3DIR=%ProgramFiles%\Common Files\VST3"
set "DEST=%APPDATA%\Pelagos-8"

if /i "%~1"=="/plugin" goto :plugin_only

echo.
echo Uninstalling Pelagos-8...
echo.

taskkill /F /IM Pelagos-8-helper.exe >nul 2>&1
timeout /t 1 /nobreak >nul
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "Remove-Item -LiteralPath ([Environment]::GetFolderPath('Startup')+'\Pelagos-8 Helper.lnk') -ErrorAction SilentlyContinue"
echo Removed the helper's login shortcut.
if exist "%DEST%" rmdir /S /Q "%DEST%" >nul 2>&1
if not exist "%DEST%" (
    echo Removed helper:  %DEST%
) else (
    echo.
    echo The helper folder "%DEST%" could not be removed right now.
    echo Log out and back in, then delete that folder by hand.
    echo.
)

if not exist "%VST3DIR%\Pelagos-8.vst3" goto :plugin_gone
net session >nul 2>&1
if not errorlevel 1 (
    call :remove_plugin
) else (
    echo.
    echo Windows will now ask for permission to remove the plugin from
    echo "%VST3DIR%". Please click Yes.
    set "ME=%~f0"
    setlocal enabledelayedexpansion
    set "ME=!ME:'=''!"
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '!ME!' -ArgumentList '/plugin' -Verb RunAs -Wait" >nul 2>&1
    endlocal
)
if exist "%VST3DIR%\Pelagos-8.vst3" (
    echo.
    echo The plugin in "%VST3DIR%" could NOT be removed.
    echo Close your DAW ^(and any plugin scanner^), then run the uninstaller again.
    echo If it still fails, right-click "Uninstall Pelagos-8.bat" and choose
    echo "Run as administrator".
    echo.
    pause
    exit /b 1
)
echo Removed plugin:  %VST3DIR%\Pelagos-8.vst3
:plugin_gone

echo.
echo Done. Pelagos-8 has been removed.
echo Your presets were NOT deleted. They are still in:
echo   %USERPROFILE%\Music\Pelagos-8\Presets
echo Delete that folder yourself if you no longer want them.
echo.
pause
exit /b 0

:plugin_only
call :remove_plugin
if exist "%VST3DIR%\Pelagos-8.vst3" (
    echo The plugin could not be removed from "%VST3DIR%".
    echo Close your DAW ^(and any plugin scanner^), then run the uninstaller again.
    pause
    exit /b 1
)
exit /b 0

:remove_plugin
if exist "%VST3DIR%\Pelagos-8.vst3" rmdir /S /Q "%VST3DIR%\Pelagos-8.vst3"
exit /b 0
