---
id: "guide_20261013_cross_pc_ssot_sync"
title: "70_크로스 PC 단일 SSOT 연동 및 원클릭 동기화 가이드"
type: resource
category_main: 지식
category_sub: AI_에이전트
topic: 크로스PC_SSOT_동기화
date: 2026-10-13
status: 완료
tags:
  - AI에이전트
  - Antigravity
  - 크로스PC
  - SSOT
  - 위키동기화
  - 거버넌스
aliases:
  - "크로스_PC_단일_SSOT_연동_가이드"
  - "70_크로스_PC_단일_SSOT_연동_및_원클릭_동기화_가이드"
  - "Cross_Device_SSOT_Pointer_Guide"
---

# 🖥️ 70_크로스 PC 단일 SSOT 연동 및 원클릭 동기화 가이드

> [!ABSTRACT] 📖 문서 개요
> 사무실, 재택, 노트북 등 복수의 컴퓨터를 오가며 Antigravity(Gemini CLI) 에이전트를 운용할 때, **기기 간 규칙 충돌을 원천 차단하고 기기 간 동기화되는 옵시디언 볼트(`D:\00_obsidian`)를 단일 진실 공급원(SSOT)으로 전적으로 위임하는 크로스 PC 아키텍처 및 원클릭 셋업 가이드**입니다.

---

## 🧭 1. 배경 및 문제 구조 (Why Cross-Device SSOT?)

### ① 동기화의 사각지대: 로컬 C드라이브 vs 옵시디언 볼트
* 옵시디언 볼트 내부(`D:\00_obsidian\.agents\`)의 마스터 룰북([`AGENTS.md`](file:///d:/00_obsidian/AGENTS.md)) 및 코딩 헌장([`PYTHON_CODE_AGENT.md`](file:///d:/00_obsidian/.agents/rules/PYTHON_CODE_AGENT.md))은 Git이나 클라우드를 통해 모든 기기 간에 100% 실시간 동기화됩니다.
* 반면, 각 컴퓨터의 로컬 홈 디렉토리(`C:\Users\<계정>\.gemini\GEMINI.md`)는 기기 간에 동기화되지 않는 **개별 PC 고유 파일**입니다.

### ② 과거 규칙 잔재로 인한 에이전트 간섭 문제
* 만약 과거 어떤 PC의 로컬 `GEMINI.md`에 *"00_Inbox에 WORK_STATUS.md 일지를 자동 배포한다"*는 구버전 규칙이 남아 있다면,
* 에이전트 구동 시 해당 로컬 파일이 `<RULE[user_global]>`로 최우선 주입되어, 볼트 내 최신 헌장("WORK_STATUS 생성 원천 금지")과 **충돌(간섭)**을 일으키고 원치 않는 임시 파일이 계속 생성되는 사태가 발생합니다.

---

## ⚙️ 2. Antigravity 내부 로딩 우선순위 메커니즘

Antigravity 엔진은 다중 환경에서 규칙과 스킬을 아래의 위계질서로 로드합니다:

```mermaid
flowchart TD
    subgraph Rules_Injection [규칙 로딩 구조]
        R1["1. 로컬 머신 전역 규칙\n(~/.gemini/GEMINI.md)\n<RULE[user_global]>"]
        R2["2. 워크스페이스 마스터 규칙\n(D:/00_obsidian/AGENTS.md)\n<RULE[workspace]>"]
        R1 -.->|"이중 주입 (충돌 가능성)"| R2
    end

    subgraph Skills_Priority [스킬 우선순위 (Priority)]
        S1["🥇 1순위: 워크스페이스 스킬\n(D:/00_obsidian/.agents/skills/*)"]
        S2["🥈 2순위: 로컬 머신 전역 스킬\n(~/.gemini/config/skills/*)"]
        S3["🥉 3순위: Antigravity 내장 스킬"]
        S1 -->|"오버라이드 (항상 최우선)"| S2 --> S3
    end
```

1. **스킬(Skills)은 옵시디언이 무조건 1순위**:
   * 워크스페이스(`D:\00_obsidian\.agents\skills\*`)에 정의된 스킬은 로컬 머신의 스킬보다 우선순위가 항상 높으므로(Priority 1), 컴퓨터를 변경해도 볼트 스킬이 무조건 우선 실행됩니다.
2. **규칙(Rules)은 로컬과 볼트가 동시에 주입됨**:
   * 로컬 `GEMINI.md`와 볼트 `AGENTS.md`가 둘 다 프롬프트에 들어가므로, **로컬 `GEMINI.md`에 세부 규칙을 적어두면 볼트 최신 규칙과 반드시 불일치가 발생**합니다.

---

## 🏛️ 3. 해결책: 크로스 PC 단일 SSOT 연동 원칙 (Cross-Device SSOT Pointer Law)

### ① 로컬 파일의 단순 위임 포인터화
* 각 컴퓨터의 로컬 `~/.gemini/GEMINI.md`에는 개별 업무 규칙이나 파이썬 룰을 절대 적지 않습니다.
* 오직 **"모든 규칙과 스킬은 옵시디언 볼트(D:\00_obsidian)를 100% 따른다"는 단순 포인터(위임장)**로만 유지합니다.

### ② 옵시디언 GUI 앱 실행 불필요 원칙
* 에이전트는 옵시디언 프로그램의 실행 여부와 무관하게 **로컬 디스크 파일 시스템(`D:\00_obsidian\.agents\...`)을 직접 읽어서 동작**합니다.
* 따라서 옵시디언 앱을 켤 필요가 없으며, Git/동기화 툴을 통해 볼트 폴더만 디스크에 존재하면 즉시 가동됩니다.

---

## 🚀 4. 원클릭 동기화 스킬: `cross-device-agent-setup`

새로운 컴퓨터나 다른 PC로 이동했을 때, 수동으로 파일을 편집할 필요 없이 에이전트 대화창에 한마디만 입력하면 로컬 포인터 설정이 1초 만에 완료됩니다.

### ① 실전 트리거 키워드
* **`"옵시디언과 동기화해줘"`**
* **`"셋업 옵시디언과 동기화 해줘"`**
* **`"옵시디언 동기화해줘"`**
* **`"옵시디언 셋업해줘"`**
* **`"컴퓨터 바뀌었어"`**

### ② 4단계 자동화 파이프라인
```mermaid
flowchart LR
    A["1. 사용자 홈 경로\n(~/.gemini/) 감지"] --> B["2. 표준 SSOT 포인터\nGEMINI.md 덮어쓰기"]
    B --> C["3. 옵시디언 볼트\n룰북/스킬 4종 무결성 검증"]
    C --> D["4. 파이썬 환경\n(unoBase) 정합 보고"]
```

1. **사용자 홈 디렉토리 감지**: 현재 머신의 `%USERPROFILE%\.gemini\` 폴더 확인 (부재 시 자동 생성).
2. **표준 SSOT 포인터 배포**: 로컬 `GEMINI.md`를 표준 위임 템플릿으로 원클릭 덮어쓰기.
3. **볼트 무결성 검증**: 마스터 룰북([`AGENTS.md`](file:///d:/00_obsidian/AGENTS.md)), 코딩 헌장([`PYTHON_CODE_AGENT.md`](file:///d:/00_obsidian/.agents/rules/PYTHON_CODE_AGENT.md)), 스킬 4종 로드 상태 전수 점검.
4. **완료 보고**: "이 컴퓨터에서도 옵시디언 최신 규칙과 스킬이 100% 단일 적용됩니다" 안내.

---

## 📋 5. 표준 로컬 포인터 템플릿 규격 (`~/.gemini/GEMINI.md`)

```markdown
# 🧭 글로벌 포인터 (SSOT 옵시디언 볼트 단일 위임)

본 머신의 Antigravity 에이전트는 기기 간 동기화되는 **옵시디언 볼트(`D:\00_obsidian`)**의 규칙과 스킬을 단일 진실 공급원(SSOT)으로 전적으로 따릅니다.
로컬 머신에 세부 규칙을 분산 중복 관리하지 않으며, 모든 거버넌스 헌장과 전문 스킬은 볼트 내부 파일을 실시간 참조하여 집행합니다:

- 🏛️ **마스터 볼트 룰북**: `D:\00_obsidian\AGENTS.md`
- 🐍 **글로벌 파이썬 코딩 헌장**: `D:\00_obsidian\.agents\rules\PYTHON_CODE_AGENT.md`
- 🛠️ **전역 에이전트 전문 스킬 허브**: `D:\00_obsidian\.agents\skills\`
  - `code-audit-obsidian-docs` (코드 품질 감사 및 단일 대시보드 동기화)
  - `obsidian-inbox-processor` (인박스 정리 및 Inbox Zero 달성)
  - `obsidian-wiki-sync` (세션 지식 위키 스마트 병합)
  - `cross-device-agent-setup` (새 PC 환경 원클릭 로컬 포인터 셋업)

## 🔄 핵심 기본 행동 원칙
1. **임시 상태 파일 생성 원천 금지 (No Standalone Status Files Law)**:
   - `WORK_STATUS.md` 등의 임시 파일을 `00_Inbox`나 개별 프로젝트 폴더에 절대 생성하지 않습니다.
   - 모든 작업 내역과 변경점은 오직 해당 프로젝트의 마스터 대시보드(`00_*_대시보드.md`) 상단 타임테이블(Changelog)과 당일 데일리 노트에만 직접 기록(Upsert)합니다.
2. **코드 매뉴얼 격리 보존 (Code Manual Isolation Law)**:
   - 개별 모듈 1:1 매뉴얼(`.md`)은 소스 코드 저장소(`unoUtil/` 등) 내부에만 단독 보관하며, 옵시디언 볼트로 복사/미러링하지 않습니다.
```

---

## 🔗 6. 연관 문서 및 거버넌스 링크
* 🏠 **[[AGENTS.md]]**: 제6장 크로스 PC 단일 SSOT 연동 원칙 (Cross-Device SSOT Pointer Law)
* 🛠️ **[[D:\00_obsidian\.agents\skills\cross-device-agent-setup\SKILL.md|cross-device-agent-setup (스킬 정의서)]]**
* 🧭 **[[00_AI_에이전트_시스템_통합_색인]]**: AI 에이전트 시스템 전체 MOC
* 📖 **[[10_AI_에이전트_명령어_및_스킬_가이드]]**: 전역 자연어 트리거 치트시트
* 🧠 **[[30_Antigravity_CLI_옵시디언_위키_동기화_매뉴얼]]**: 볼트 위키 스마트 병합 시스템
