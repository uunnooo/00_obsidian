$ErrorActionPreference = "Stop"
$VAULT_ROOT = "F:/00_obsidian"
$UNOWORK_ROOT = "$VAULT_ROOT/00_Inbox/UnoWork_Notion/Export-0295bf93-9709-4df7-b5b5-bad98689c117/개인 페이지 & 공유된 페이지"
$UNO_ROOT = "$VAULT_ROOT/00_Inbox/Uno_Notion/Export-ee36c2a2-6acc-4949-9b03-78a1efec0cc1/개인 페이지 & 공유된 페이지"

function Strip-Tags($html) {
    if ([string]::IsNullOrWhiteSpace($html)) { return "" }
    $clean = $html -replace '<script[\s\S]*?</script>', ''
    $clean = $clean -replace '<style[\s\S]*?</style>', ''
    $clean = $clean -replace '<[^>]+>', ''
    $clean = [System.Net.WebUtility]::HtmlDecode($clean)
    return $clean.Trim()
}

# CSV 파일을 읽어서 깔끔한 Markdown Table 문자열로 변환하는 함수
function Convert-CsvToMdTable($csvPath) {
    if (-not (Test-Path $csvPath)) { return "" }
    try {
        $csvData = Import-Csv -Path $csvPath -Encoding UTF8
        if ($csvData.Count -eq 0) { return "" }
        $cols = $csvData[0].PSObject.Properties.Name
        $sb = [System.Text.StringBuilder]::new()
        $sb.AppendLine("| " + ($cols -join " | ") + " |") | Out-Null
        $sb.AppendLine("| " + (($cols | ForEach-Object { ":---" }) -join " | ") + " |") | Out-Null
        foreach ($row in $csvData) {
            $vals = $cols | ForEach-Object {
                $v = $row.$_
                if ($v) { $v.ToString().Replace('|', '\|').Replace("`n", " ") } else { "" }
            }
            $sb.AppendLine("| " + ($vals -join " | ") + " |") | Out-Null
        }
        return $sb.ToString()
    } catch {
        return ""
    }
}

# 노션 HTML을 완벽하게 파싱하여 인라인 CSV 테이블 및 메타데이터 속성까지 모두 복원하는 엔진
function Convert-NotionHtmlAdvanced($html, $currentHtmlDir, $attachSubDir = "회사_업무") {
    # 1. Title
    $title = "Untitled"
    if ($html -match '<h1 class="page-title"[^>]*>([\s\S]*?)</h1>') {
        $title = Strip-Tags $matches[1]
    }

    # 2. Date
    $date = (Get-Date).ToString("yyyy-MM-dd")
    if ($html -match '<time datetime="([^"]+)"') {
        $date = $matches[1].Substring(0, 10)
    }

    # 3. 노션 데이터베이스 속성(Properties) 추출 (빈 문서처럼 보이는 원인 해결!)
    $propsList = [System.Collections.Generic.List[string]]::new()
    if ($html -match '<table class="properties">([\s\S]*?)</table>') {
        $propRows = [regex]::Matches($matches[1], '<tr class="property-row[^"]*">([\s\S]*?)</tr>')
        foreach ($pr in $propRows) {
            $thMatch = [regex]::Match($pr.Groups[1].Value, '<th[^>]*>([\s\S]*?)</th>')
            $tdMatch = [regex]::Match($pr.Groups[1].Value, '<td[^>]*>([\s\S]*?)</td>')
            if ($thMatch.Success -and $tdMatch.Success) {
                $propName = Strip-Tags $thMatch.Groups[1].Value
                $propVal = Strip-Tags $tdMatch.Groups[1].Value
                if ($propName -and $propVal) {
                    $propsList.Add("- **$propName**: $propVal")
                }
            }
        }
    }

    # 4. Body 추출
    $body = $html
    if ($html -match '<div class="page-body">([\s\S]*?)</div></article>') {
        $body = $matches[1]
    }

    # 5. 인라인 CSV 링크를 실제 데이터 테이블로 직접 치환! (가장 핵심 버그 수정!)
    # 예: <a href="TestItem%20%EC%BD%94%EB%93%9C%ED%91%9C...csv"><code>...csv</code></a>
    $body = [regex]::Replace($body, '<a href="([^"]+\.csv)"><code>([^<]+)</code></a>', {
        param($m)
        $relHref = [System.Uri]::UnescapeDataString($m.Groups[1].Value)
        $csvFullPath = [System.IO.Path]::GetFullPath([System.IO.Path]::Combine($currentHtmlDir, $relHref))
        $tableName = [System.IO.Path]::GetFileNameWithoutExtension($relHref) -replace '\s+[0-9a-f]{32}$', ''
        
        $mdTable = Convert-CsvToMdTable $csvFullPath
        if ($mdTable) {
            return "`n`n### 📊 $tableName`n`n$mdTable`n`n"
        } else {
            return "`n`n*[데이터 테이블: $tableName]*`n`n"
        }
    })

    # 6. 토글 details/summary 태그 예쁘게 변환
    $body = [regex]::Replace($body, '<details[^>]*>\s*<summary[^>]*>([\s\S]*?)</summary>([\s\S]*?)</details>', {
        param($m)
        $summaryText = Strip-Tags $m.Groups[1].Value
        $innerContent = $m.Groups[2].Value
        return "`n`n> [!NOTE]- 📁 $summaryText`n> " + ($innerContent.Trim() -replace "`n", "`n> ") + "`n`n"
    })

    # 7. Headings
    $body = [regex]::Replace($body, '<h1[^>]*>([\s\S]*?)</h1>', { param($m) "`n`n# " + (Strip-Tags $m.Groups[1].Value) + "`n`n" })
    $body = [regex]::Replace($body, '<h2[^>]*>([\s\S]*?)</h2>', { param($m) "`n`n## " + (Strip-Tags $m.Groups[1].Value) + "`n`n" })
    $body = [regex]::Replace($body, '<h3[^>]*>([\s\S]*?)</h3>', { param($m) "`n`n### " + (Strip-Tags $m.Groups[1].Value) + "`n`n" })

    # 8. Images
    $body = [regex]::Replace($body, '<figure class="image"[^>]*>[\s\S]*?<img[^>]*src="([^"]+)"[^>]*>[\s\S]*?</figure>', {
        param($m)
        $src = [System.Uri]::UnescapeDataString($m.Groups[1].Value)
        $fn = [System.IO.Path]::GetFileName($src)
        $target = "_attachments/$attachSubDir/$fn"
        return "`n`n![[$target|650]]`n`n"
    })

    # 9. Simple Table
    $body = [regex]::Replace($body, '<table class="simple-table"[^>]*>([\s\S]*?)</table>', {
        param($m)
        $tHtml = $m.Groups[1].Value
        $trMatches = [regex]::Matches($tHtml, '<tr[^>]*>([\s\S]*?)</tr>')
        $rows = [System.Collections.Generic.List[string]]::new()
        foreach ($tr in $trMatches) {
            $cellMatches = [regex]::Matches($tr.Groups[1].Value, '<(?:th|td)[^>]*>([\s\S]*?)</(?:th|td)>')
            $cells = [System.Collections.Generic.List[string]]::new()
            foreach ($c in $cellMatches) {
                $cells.Add(((Strip-Tags $c.Groups[1].Value) -replace '\|', '\|'))
            }
            if ($cells.Count -gt 0) {
                $rows.Add("| " + ($cells -join " | ") + " |")
            }
        }
        if ($rows.Count -eq 0) { return "" }
        $header = $rows[0]
        $colCount = [regex]::Matches($header, '\|').Count - 1
        $dividers = [System.Collections.Generic.List[string]]::new()
        for ($k = 0; $k -lt $colCount; $k++) { $dividers.Add(":---") }
        $divRow = "| " + ($dividers -join " | ") + " |"
        $allRows = [System.Collections.Generic.List[string]]::new()
        $allRows.Add($header)
        $allRows.Add($divRow)
        for ($r = 1; $r -lt $rows.Count; $r++) { $allRows.Add($rows[$r]) }
        return "`n`n" + ($allRows -join "`n") + "`n`n"
    })

    # 10. Inlines & Callouts
    $body = [regex]::Replace($body, '<blockquote[^>]*>([\s\S]*?)</blockquote>', {
        param($m)
        $q = (Strip-Tags $m.Groups[1].Value) -replace "`n", "`n> "
        return "`n`n> [!NOTE]`n> " + $q + "`n`n"
    })
    $body = [regex]::Replace($body, '<aside class="[^"]*callout[^"]*"[^>]*>([\s\S]*?)</aside>', {
        param($m)
        $c = (Strip-Tags $m.Groups[1].Value) -replace "`n", "`n> "
        return "`n`n> [!TIP]`n> " + $c + "`n`n"
    })
    $body = [regex]::Replace($body, '<li[^>]*>([\s\S]*?)</li>', { param($m) "`n* " + (Strip-Tags $m.Groups[1].Value) })
    $body = [regex]::Replace($body, '<strong[^>]*>([\s\S]*?)</strong>', { param($m) "**" + (Strip-Tags $m.Groups[1].Value) + "**" })
    $body = [regex]::Replace($body, '<em[^>]*>([\s\S]*?)</em>', { param($m) "*" + (Strip-Tags $m.Groups[1].Value) + "*" })
    $body = [regex]::Replace($body, '<code[^>]*>([\s\S]*?)</code>', { param($m) "``" + (Strip-Tags $m.Groups[1].Value) + "``" })
    $body = $body -replace '<hr[^>]*\/?>', "`n`n---`n`n"
    $body = [regex]::Replace($body, '<p[^>]*>([\s\S]*?)</p>', {
        param($m)
        $p = Strip-Tags $m.Groups[1].Value
        if ($p) { "`n`n$p`n`n" } else { "`n" }
    })

    $body = Strip-Tags $body
    $body = [regex]::Replace($body, '\n{3,}', "`n`n").Trim()

    if ($title -eq "Untitled" -or $title -eq "제목 없음") {
        if ($body -match '(?m)^#+\s*(.+)$') {
            $title = $matches[1].Trim()
        }
    }

    # 속성 블록 결합
    $propsBlock = ""
    if ($propsList.Count -gt 0) {
        $propsBlock = "### 📋 상세 속성 및 조건`n`n" + ($propsList -join "`n") + "`n`n---`n`n"
    }

    $finalBody = if ($propsBlock) { $propsBlock + $body } else { $body }

    return @{ Title = $title; Date = $date; Body = $finalBody }
}

Write-Host "=== STARTING ADVANCED NOTION RE-MIGRATION & INLINE EMBEDDING ==="

# 1. 실차 평가 데이터 프레임 완벽 복원
$targetDoc = "$VAULT_ROOT/04_Resources/회사_실차평가_데이터프레임/실차_평가_데이터_프레임.md"
$srcHtml = "$UNOWORK_ROOT/실차 평가 데이터 프레임 1b5ea7294d6580469c73c2b02dd471d4.html"
if (Test-Path $srcHtml) {
    $html = [System.IO.File]::ReadAllText($srcHtml, [System.Text.Encoding]::UTF8)
    $res = Convert-NotionHtmlAdvanced $html (Split-Path $srcHtml) "회사_업무"
    $md = "---`nid: `"work_dataframe_master`"`ntitle: `"실차 평가 데이터 프레임 규격서`"`ntype: resource`ncategory_main: 회사_업무`ncategory_sub: 실차평가데이터`ndate: $($res.Date)`nstatus: 완료`ntags:`n  - 데이터프레임`n  - 실차평가`n  - 코드표`n---`n`n# 🚗 $($res.Title)`n`n$($res.Body)`n"
    [System.IO.File]::WriteAllText($targetDoc, $md, [System.Text.Encoding]::UTF8)
    Write-Host "FIXED: 실차_평가_데이터_프레임.md with INLINE TABLES!"
}

# 2. 2025 Snow 기반기술 & 설질변화 유형 및 목표 테이블 복원
$snowMasterDoc = "$VAULT_ROOT/02_Projects/2025_Snow_기반기술/2025_Snow_기반기술.md"
$snowSrcHtml = "$UNOWORK_ROOT/2025 Snow 기반기술 1b4ea7294d6580abbf25dbf9ed03429a.html"
if (Test-Path $snowSrcHtml) {
    $html = [System.IO.File]::ReadAllText($snowSrcHtml, [System.Text.Encoding]::UTF8)
    $res = Convert-NotionHtmlAdvanced $html (Split-Path $snowSrcHtml) "회사_업무"
    $md = "---`nid: `"work_snow2025_master`"`ntitle: `"2025 Snow 기반기술 프로젝트 로드맵`"`ntype: project`ncategory_main: 회사_업무`ncategory_sub: Snow기반기술`ndate: $($res.Date)`nstatus: 진행중`ntags:`n  - Snow기반기술`n  - 노면특성`n  - 프로젝트`n---`n`n# ❄️ $($res.Title)`n`n$($res.Body)`n"
    [System.IO.File]::WriteAllText($snowMasterDoc, $md, [System.Text.Encoding]::UTF8)
    Write-Host "FIXED: 2025_Snow_기반기술.md with INLINE TABLES!"
}

# 3. 2025 Snow 세부 문서들 (온도별 -1~-3, 설질변화 등)의 속성 및 내용 전면 복원
$snowSubDir = "$UNOWORK_ROOT/2025 Snow 기반기술"
if (Test-Path $snowSubDir) {
    Get-ChildItem -Path $snowSubDir -Recurse -Filter "*.html" | ForEach-Object {
        $html = [System.IO.File]::ReadAllText($_.FullName, [System.Text.Encoding]::UTF8)
        $res = Convert-NotionHtmlAdvanced $html (Split-Path $_.FullName) "회사_업무"
        $cleanTitle = $res.Title -replace '[\\/:*?"<>|]', '_' -replace '\s+', '_'
        if ($cleanTitle.Length -gt 60) { $cleanTitle = $cleanTitle.Substring(0, 60) }
        if ([string]::IsNullOrWhiteSpace($cleanTitle) -or $cleanTitle -eq "제목_없음" -or $cleanTitle -eq "Untitled") {
            $cleanTitle = ($_.BaseName -replace '\s+[0-9a-f]{32}$', '') -replace '[\\/:*?"<>|]', '_' -replace '\s+', '_'
        }
        $targetFile = "$VAULT_ROOT/02_Projects/2025_Snow_기반기술/${cleanTitle}.md"
        $md = "---`nid: `"snow_sub_$cleanTitle`"`ntitle: `"$($res.Title)`"`ntype: project`ncategory_main: 회사_업무`ncategory_sub: Snow기반기술`ndate: $($res.Date)`nstatus: 진행중`ntags:`n  - Snow기반기술`n---`n`n# ❄️ $($res.Title)`n`n$($res.Body)`n"
        [System.IO.File]::WriteAllText($targetFile, $md, [System.Text.Encoding]::UTF8)
        Write-Host "Updated Snow SubDoc: $cleanTitle.md"
    }
}

# 4. 분석 일정 마스터 및 세부 문서 인라인 테이블 복원
$schedHtml = "$UNOWORK_ROOT/분석 일정 1ceea7294d6580b29a5ad150c92e2cab.html"
$schedTarget = "$VAULT_ROOT/03_Areas/회사_업무/분석_일정/분석_일정.md"
if (Test-Path $schedHtml) {
    $html = [System.IO.File]::ReadAllText($schedHtml, [System.Text.Encoding]::UTF8)
    $res = Convert-NotionHtmlAdvanced $html (Split-Path $schedHtml) "회사_업무"
    $md = "---`nid: `"work_schedule_master`"`ntitle: `"연간 시험 및 데이터 분석 일정`"`ntype: meeting`ncategory_main: 회사_업무`ncategory_sub: 분석일정`ndate: $($res.Date)`nstatus: 진행중`ntags:`n  - 분석일정`n  - 업무계획`n---`n`n# 📅 $($res.Title)`n`n$($res.Body)`n"
    [System.IO.File]::WriteAllText($schedTarget, $md, [System.Text.Encoding]::UTF8)
    Write-Host "FIXED: 분석_일정.md with INLINE TABLES!"
}

# 5. 빅데이터 분석기사 루트 문서 인라인 복원
$bigDataRootHtml = Get-ChildItem -Path $UNO_ROOT -Filter "*빅데이터*.html" | Select-Object -First 1
if ($bigDataRootHtml) {
    $html = [System.IO.File]::ReadAllText($bigDataRootHtml.FullName, [System.Text.Encoding]::UTF8)
    $res = Convert-NotionHtmlAdvanced $html (Split-Path $bigDataRootHtml.FullName) ""
    $md = "---`nid: `"bigdata_root_doc`"`ntitle: `"빅데이터 분석기사 개요 및 커리큘럼`"`ntype: project`ncategory_main: 자기계발`ncategory_sub: 빅데이터분석기사`ndate: $($res.Date)`nstatus: 진행중`ntags:`n  - 빅데이터분석기사`n---`n`n# 📚 $($res.Title)`n`n$($res.Body)`n"
    [System.IO.File]::WriteAllText("$VAULT_ROOT/02_Projects/자격증_빅데이터분석기사/01_빅데이터분석기사_개요.md", $md, [System.Text.Encoding]::UTF8)
    Write-Host "FIXED: 01_빅데이터분석기사_개요.md with INLINE CONTENT!"
}

Write-Host "`n=== ALL FIXES COMPLETED 100% AUTOMATICALLY! ==="
