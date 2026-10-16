@echo off
setlocal EnableExtensions
cd /d "%~dp0"
echo ChatGPT Exporter Personal - standalone build
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Build.ps1"
set "RC=%ERRORLEVEL%"
echo.
if "%RC%"=="0" (
  echo SUCCESS - find dist\ChatGPT_Exporter_Personal.user.js
) else (
  echo FAILED - open build.log and share it if needed.
)
echo.
pause
exit /b %RC%
