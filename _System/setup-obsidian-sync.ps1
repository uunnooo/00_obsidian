# ==============================================================================
# Antigravity CLI - Obsidian Wiki Sync Global Registration Script
# ==============================================================================

$ErrorActionPreference = "Stop"

# 1. Detect Obsidian Vault Path
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VaultRoot = Split-Path -Parent $ScriptDir

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  [Antigravity CLI] Obsidian Wiki Sync Registration" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "[1/4] Vault Path: $VaultRoot" -ForegroundColor Green

# 2. Register Environment Variable and Cache File
try {
    [Environment]::SetEnvironmentVariable("OBSIDIAN_VAULT", $VaultRoot, "User")
    Write-Host "[2/4] Environment variable 'OBSIDIAN_VAULT' registered." -ForegroundColor Green
} catch {
    Write-Warning "Could not set environment variable. Falling back to cache file."
}

$GeminiHome = Join-Path $env:USERPROFILE ".gemini"
if (-not (Test-Path $GeminiHome)) {
    New-Item -ItemType Directory -Path $GeminiHome -Force | Out-Null
}

$CachePath = Join-Path $GeminiHome "antigravity_obsidian_vault.txt"
[System.IO.File]::WriteAllText($CachePath, $VaultRoot, [System.Text.UTF8Encoding]::new($false))
Write-Host "[2/4] Cache file created: $CachePath" -ForegroundColor Green

# 3. Prepare Global Config Skills (~/.gemini/config/skills/)
$GlobalConfigSkills = Join-Path $GeminiHome "config\skills"
if (-not (Test-Path $GlobalConfigSkills)) {
    New-Item -ItemType Directory -Path $GlobalConfigSkills -Force | Out-Null
}

$SourceSkillDir = Join-Path $VaultRoot ".agent\skills\obsidian-wiki-sync"
$TargetSkillDir = Join-Path $GlobalConfigSkills "obsidian-wiki-sync"

# 4. Junction / Copy Skill
Write-Host "[3/4] Registering global skill..." -ForegroundColor Yellow
if (Test-Path $SourceSkillDir) {
    if (Test-Path $TargetSkillDir) {
        Remove-Item -Path $TargetSkillDir -Recurse -Force | Out-Null
    }
    
    $linked = $false
    try {
        New-Item -ItemType Junction -Path $TargetSkillDir -Target $SourceSkillDir -Force | Out-Null
        Write-Host "[4/4] Junction link created successfully!" -ForegroundColor Green
        $linked = $true
    } catch {
        Copy-Item -Path $SourceSkillDir -Destination $TargetSkillDir -Recurse -Force
        Write-Host "[4/4] Skill copied successfully!" -ForegroundColor Green
    }
} else {
    Write-Error "Skill source directory not found: $SourceSkillDir"
}

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Setup complete! Now you can say in ANY folder:" -ForegroundColor White
Write-Host "   - '내가 이제까지 진행한거 정리해줘'" -ForegroundColor Yellow
Write-Host "   - '오늘 작업 옵시디언에 기록해줘'" -ForegroundColor Yellow
Write-Host "   - '방금 공부한 내용 위키에 업데이트해줘'" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan
