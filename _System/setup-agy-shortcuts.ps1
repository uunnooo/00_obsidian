# ==============================================================================
# Antigravity CLI - agy & agy-safe PowerShell Profile Registration Script
# ==============================================================================

$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  [Antigravity CLI] agy & agy-safe Shortcut Registration" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Target profile paths (PowerShell 7 and Windows PowerShell 5.1)
$ProfilePaths = @(
    (Join-Path $env:USERPROFILE "Documents\PowerShell\Microsoft.PowerShell_profile.ps1"),
    (Join-Path $env:USERPROFILE "Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1")
)

$ShortcutBlock = @"

# ==============================================================================
# UTF-8 Console Encoding Setup (터미널 한글 깨짐 방지)
# ==============================================================================
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding  = [System.Text.Encoding]::UTF8
`$OutputEncoding           = [System.Text.Encoding]::UTF8

# >>> Antigravity CLI (agy) Shortcuts >>>
# 1. agy (Full Auto / YOLO Mode - 모든 권한 자동 승인)
function agy {
    `$agyCmd = (Get-Command agy.exe -ErrorAction SilentlyContinue).Source
    if (-not `$agyCmd) { `$agyCmd = "`$env:LOCALAPPDATA\agy\bin\agy.exe" }
    & `$agyCmd --dangerously-skip-permissions @args
}

# 2. agy-safe (Safe Mode - 읽기/탐색 프리패스, 쓰기/명령어 사용자 승인)
function agy-safe {
    `$agyCmd = (Get-Command agy.exe -ErrorAction SilentlyContinue).Source
    if (-not `$agyCmd) { `$agyCmd = "`$env:LOCALAPPDATA\agy\bin\agy.exe" }
    & `$agyCmd @args
}

# 3. agy-raw (순정 바이너리 모드)
function agy-raw {
    `$agyCmd = (Get-Command agy.exe -ErrorAction SilentlyContinue).Source
    if (-not `$agyCmd) { `$agyCmd = "`$env:LOCALAPPDATA\agy\bin\agy.exe" }
    & `$agyCmd @args
}
# <<< Antigravity CLI (agy) Shortcuts <<<
"@

foreach ($prof in $ProfilePaths) {
    try {
        $parentDir = Split-Path -Parent $prof
        if (-not (Test-Path $parentDir)) {
            New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
        }

        $existingContent = ""
        if (Test-Path $prof) {
            $existingContent = [System.IO.File]::ReadAllText($prof, [System.Text.Encoding]::UTF8)
        }

        # Check if already present
        if ($existingContent -match "Antigravity CLI \(agy\) Shortcuts") {
            # Replace existing block
            $existingContent = [System.Text.RegularExpressions.Regex]::Replace(
                $existingContent,
                "(?ms)# >>> Antigravity CLI \(agy\) Shortcuts >>>.*?# <<< Antigravity CLI \(agy\) Shortcuts <<<",
                $ShortcutBlock.Trim()
            )
            [System.IO.File]::WriteAllText($prof, $existingContent, [System.Text.UTF8Encoding]::new($false))
            Write-Host "[OK] Updated shortcuts in: $prof" -ForegroundColor Green
        } else {
            # Append block
            $newContent = ($existingContent.TrimEnd() + "`r`n" + $ShortcutBlock).TrimStart()
            [System.IO.File]::WriteAllText($prof, $newContent, [System.Text.UTF8Encoding]::new($false))
            Write-Host "[OK] Registered shortcuts in: $prof" -ForegroundColor Green
        }
    } catch {
        Write-Warning "Failed to update $prof : $_"
    }
}

# 2. Create CMD wrappers in agy bin directory if available
$agyBinDir = "$env:LOCALAPPDATA\agy\bin"
if (Test-Path $agyBinDir) {
    try {
        $safeCmd = "@echo off`r`n`"%~dp0agy.exe`" %*"
        [System.IO.File]::WriteAllText((Join-Path $agyBinDir "agy-safe.cmd"), $safeCmd, [System.Text.Encoding]::ASCII)
        Write-Host "[OK] Created agy-safe.cmd in: $agyBinDir" -ForegroundColor Green
    } catch {
        Write-Warning "Could not write to $agyBinDir : $_"
    }
}

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Setup Complete! You can now use in PowerShell:" -ForegroundColor White
Write-Host "   - agy      : Auto-approves all permissions (YOLO)" -ForegroundColor Yellow
Write-Host "   - agy-safe : Asks for review on write/execute (Safe)" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan
