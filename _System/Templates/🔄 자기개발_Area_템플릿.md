<%*
// ==========================================
// 🛡️ [안전 가드] 템플릿 원본 보호
// ==========================================
if (tp.file.folder(true) === "_System/Templates") {
    new Notice("⚠️ 템플릿 원본 파일에서는 실행할 수 없습니다!", 4000);
    return;
}

const todayStr = tp.date.now("YYYY-MM-DD");
const dateShort = tp.date.now("YYMMDD");

// 1. 자기개발 주제/목표 입력
const titleInput = await tp.system.prompt("자기개발 주제 또는 관리 영역 제목을 입력하세요:", "데이터분석_역량강화");
const areaTitle = titleInput ? titleInput.trim().replace(/\s+/g, '_') : "자기개발_목표";

// 2. 세부 분류 입력
const subInput = await tp.system.prompt("세부 분류 (예: AI_데이터분석, 영어회화, 건강관리):", "AI_데이터분석");
const categorySub = subInput ? subInput.trim() : "일반";

// 3. 목표일(Target Date) 입력
const targetInput = await tp.system.prompt("목표 달성 예정일 (YYYY-MM-DD):", todayStr);
const targetDate = targetInput ? targetInput.trim() : todayStr;

// 4. 자동 작명 및 이동
const newFileName = `${areaTitle}`;
await tp.file.rename(newFileName);
-%>
---
id: "<% dateShort %>_<% areaTitle %>"
title: "<% areaTitle %>"
type: area
category_main: 자기개발
category_sub: <% categorySub %>
topic: "<% areaTitle %>"
date: <% todayStr %>
target_date: <% targetDate %>
achieved_date: ""
status: 진행중 # [대기, 진행중, 완료, 보류]
progress: "0%"
satisfaction: 3 # [1~5 만족도 점수]
tags:
  - 자기개발
  - Area
  - <% categorySub %>
aliases:
  - <% areaTitle %>
---

# 🔄 <% areaTitle %> (Area 관리 대시보드)

> [!ABSTRACT] 🎯 핵심 운영 목표 및 지속 관리 기준
> • **관리 주제**: <% areaTitle %> (<% categorySub %>)
> • **최종 목표일**: <% targetDate %>
> • **달성일**: (미완료)
> • **현재 진도/목표율**: 0%
> • **핵심 지향점**: 지속적인 역량 강화 및 루틴 체화

---

## 🎯 1. 세부 마일스톤 및 목표 관리표 (Milestones)

| 세부 단계 / 마일스톤 | 목표일 | 달성일 | 목표율/진도 | 주요 내용 및 비고 |
| :--- | :---: | :---: | :---: | :--- |
| **1단계: 계획 수립 및 기초 학습** | <% todayStr %> | <% todayStr %> | 100% | 기본 교재 확보 및 학습 루틴 세팅 |
| **2단계: 핵심 역량 강화 및 실습** | <% targetDate %> | - | 0% | 실전 과제 수행 및 이론 정립 |
| **3단계: 최종 목표 달성 및 평가** | <% targetDate %> | - | 0% | 공인 평가 응시 또는 목표 달성 |

---

## 📚 2. 관련 지식 리소스 및 참고 자료 (Resources & References)

* 🔗 **연관 지식 위키**: [[04_Resources/]]
* 📑 **외부 참고 자료 / 도서**: 
* 💡 **핵심 노하우 요약**: 

---

## 📈 3. 누적 실행 및 진도 기록 (Progress Log)

* **<% todayStr %>**:
  * 자기개발 목표 설정 및 Area 관리 대시보드 생성.

---

## 🌟 4. 목표 달성도 및 회고 (Satisfaction & Review)

* **현재 목표율 / 달성률**: `0%`
* **자기 만족도 점수**: `3 / 5`
* **총평 및 성장 회고 (KPT)**:
  * **Keep (잘한 점 & 지속할 습관)**: 
  * **Problem (어려웠던 점 & 보완할 장애물)**: 
  * **Try (다음 주기에 시도할 개선 행동)**: 
