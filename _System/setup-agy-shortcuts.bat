@echo off
chcp 65001 > nul
powershell -ExecutionPolicy Bypass -File "%~dp0setup-agy-shortcuts.ps1"
pause
