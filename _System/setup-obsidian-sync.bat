@echo off
chcp 65001 > nul
echo [Antigravity CLI] 옵시디언 전역 동기화 스킬 등록 중...
powershell -ExecutionPolicy Bypass -File "%~dp0setup-obsidian-sync.ps1"
pause
