---
id: "vault_main_dashboard"
title: "Second Brain 종합 메인 대시보드"
type: resource
category_main: 일상
category_sub: 대시보드
date: 2026-09-10
status: 진행중
tags:
  - 대시보드
  - 홈
  - 세컨드브레인
  - PARA
---
# 🛸 UNO Second Brain 통합 메인 대시보드

> ⚡ **Quick Jump**: [📅 1. 오늘 포커스](#-1-오늘-나의-포커스--할-일-today-at-a-glance) · [📈 2. 트레이딩 스냅샷](#-2-나스닥-선물-트레이딩-퀵-스냅샷-trading-snapshot) · [🎯 3. 프로젝트](#-3-진행-중인-핵심-프로젝트-active-projects) · [💼 4. 회의록/업무](#-4-최근-업무-회의록--업무-기록-work--meetings) · [📥 5. 인박스](#-5-00_inbox-빠른-생각--미분류-메모-inbox-zero-routine) · [📊 6. 볼트 통계](#-6-볼트-전체-지식-통계-vault-statistics)

> [!ABSTRACT] 🚀 초고속 핫링크 (Quick Access)
> [[01_Daily/2026-09-10|📅 오늘 데일리 (2026-09-10)]] ｜ [[03_Areas/트레이딩/00_트레이딩_통계_대시보드|📈 매매 통계 대시보드]] ｜ [[02_Projects/00_프로젝트_통합_대시보드|🎯 프로젝트 허브]] ｜ [[11_파동_매매원칙_오답노트|🧠 오답노트 & 10계명]] ｜ [[PARA_SETUP_GUIDE|🧭 시스템 구축 가이드]]

---

## 📅 1. 오늘 나의 포커스 & 할 일 (Today at a Glance)

```dataviewjs
const todayStr = moment().format("YYYY-MM-DD");
const dailyPage = dv.page(`01_Daily/${todayStr}`);

if (dailyPage) {
  dv.paragraph(`> [!FOCUS] 🎯 **오늘의 1순위 핵심 목표 (Focus)**
> ### **${dailyPage.focus || "설정된 목표 없음"}**
> 🔗 [[01_Daily/${todayStr}|오늘 데일리 노트 바로가기]]`);
} else {
  dv.paragraph(`> [!WARNING] ⚠️ 오늘(${todayStr}) 데일리 노트가 아직 생성되지 않았습니다.
> QuickAdd(Ctrl+P -> QuickAdd)나 템플릿으로 오늘 데일리를 생성하세요.`);
}
```

> [!NOTE]- 📋 오늘 꼭 끝내야 할 긴급 태스크 (Today Tasks) [클릭하여 펼치기]
> ```dataview
> TASK
> FROM "01_Daily"
> WHERE !completed AND file.day = date(today)
> ```

---

## 📈 2. 나스닥 선물 트레이딩 퀵 스냅샷 (Trading Snapshot)

```dataviewjs
const trades = dv.pages('"03_Areas/트레이딩/20_2026_매매일지"')
  .where(p => p.type === "trade");

const total = trades.length;
const wins = trades.where(p => p.status === "Win").length;
const losses = trades.where(p => p.status === "Loss").length;
const be = trades.where(p => p.status === "BE").length;
const winRate = (wins + losses) > 0 ? ((wins / (wins + losses)) * 100).toFixed(1) : 0;
const ruleOk = trades.where(p => p.rule_followed === true).length;
const ruleRate = total > 0 ? ((ruleOk / total) * 100).toFixed(1) : 0;

dv.paragraph(`
| 🎯 누적 거래수 | 🟢 승리 (Win) | 🔴 패배 (Loss) | ⚪ 본절 (BE) | 🏆 전체 승률 | 🛡️ 원칙 준수율 |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **${total} 회** | **${wins} 회** | **${losses} 회** | **${be} 회** | **${winRate}%** | **${ruleRate}%** |
`);
```

> [!NOTE]- 🕒 최근 5개 매매일지 일람 [클릭하여 펼치기]
> ```dataview
> TABLE WITHOUT ID
>   file.link AS "매매일지",
>   date AS "일자",
>   time AS "시간",
>   position AS "포지션",
>   pred_wave_pattern AS "예측 파동",
>   status AS "결과",
>   final_diag AS "진단"
> FROM "03_Areas/트레이딩/20_2026_매매일지"
> SORT date DESC, time DESC
> LIMIT 5
> ```
> 
> 👉 *더 자세한 분석 및 패턴별 통계는 [[03_Areas/트레이딩/00_트레이딩_통계_대시보드|📈 트레이딩 종합 통계 대시보드]]를 확인하세요.*

---

## 🎯 3. 진행 중인 핵심 프로젝트 (Active Projects)

> [!NOTE]- 🚀 진행 중인 핵심 프로젝트 목록 [클릭하여 펼치기]
> ```dataview
> TABLE WITHOUT ID
>   file.link AS "프로젝트명",
>   category_sub AS "세부 분야",
>   date AS "시작일",
>   status AS "상태"
> FROM "02_Projects"
> WHERE type = "project" AND status = "진행중"
> SORT date DESC
> LIMIT 5
> ```

---

## 💼 4. 최근 업무 회의록 & 업무 기록 (Work & Meetings)

> [!NOTE]- 📑 최근 업무 및 회의록 일람 [클릭하여 펼치기]
> ```dataview
> TABLE WITHOUT ID
>   file.link AS "문서 / 회의록",
>   date AS "일자",
>   priority AS "우선순위",
>   manager AS "담당자",
>   status AS "상태"
> FROM "03_Areas/회사_업무"
> WHERE type = "meeting" OR category_main = "회사_업무"
> SORT date DESC
> LIMIT 5
> ```

---

## 📥 5. 00_Inbox 빠른 생각 & 미분류 메모 (Inbox Zero Routine)

> [!NOTE]- 📥 미분류 인박스 메모 일람 [클릭하여 펼치기]
> ```dataview
> TABLE WITHOUT ID
>   file.link AS "미분류 메모",
>   file.mtime AS "최근 수정일"
> FROM "00_Inbox"
> WHERE file.name != "UnoWork_Notion" AND file.name != "Uno_Notion"
> SORT file.mtime DESC
> LIMIT 5
> ```

---

## 📊 6. 볼트 전체 지식 통계 (Vault Statistics)

> [!NOTE]- 📊 볼트 6대 폴더별 통계치 [클릭하여 펼치기]
> ```dataviewjs
> const inbox = dv.pages('"00_Inbox"').length;
> const daily = dv.pages('"01_Daily"').length;
> const projects = dv.pages('"02_Projects"').length;
> const areas = dv.pages('"03_Areas"').length;
> const resources = dv.pages('"04_Resources"').length;
> const archives = dv.pages('"05_Archives"').length;
> const totalNotes = inbox + daily + projects + areas + resources + archives;
> 
> dv.paragraph(`
> * 📥 **00_Inbox**: ${inbox}개
> * 📅 **01_Daily**: ${daily}개
> * 🎯 **02_Projects**: ${projects}개
> * 🔄 **03_Areas**: ${areas}개
> * 📚 **04_Resources**: ${resources}개
> * 🗄️ **05_Archives**: ${archives}개
> * 🧠 **전체 보관 지식 및 문서**: **총 ${totalNotes}개**
> `);
> ```
