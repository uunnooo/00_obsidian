---
id: "unoutil_project_hub"
title: "unoUtil 사내 파이썬 통합 프레임워크 개발 프로젝트"
type: project
category_main: 회사_업무
category_sub: unoUtil
date: 2026-09-10
status: 진행중
tags:
  - 회사_업무
  - unoUtil
  - 파이썬
  - 개발도구
  - 대시보드
  - MOC
aliases:
  - unoUtil_모듈개발_대시보드
  - unoUtil개발허브
---

# 💼 unoUtil 사내 파이썬 통합 프레임워크 개발 프로젝트

> [!ABSTRACT] 🛠️ 프레임워크 개요
> **unoUtil**은 사내 실차 시험 계측 데이터 수집, 신호 전처리, 동역학 물리 분석, 시험 환경 보정, 그리고 시각화 리포팅을 표준화하기 위한 사내 통합 파이썬 라이브러리 개발 프로젝트입니다.

---

## 📦 패키지 서브모듈 구조 및 현황

```text
📂 unoUtil/
├── 🏎️ vehicleTest/             # 실차 시험 종합 분석 패키지 (Active)
│   └── 🏁 ACCBRK/             # 실차 가감속 / 제동 성능 정밀 분석 엔진
│       ├── 00_VT_ACCBRK_대시보드.md
│       ├── 10_VT_ACCBRK.md (통합 파이프라인)
│       ├── 11_VT_ACCBRK_TIRE.md (단일 타이어 분석)
│       ├── 12_VT_ACCBRK_PROJECT.md (취합 및 보정)
│       ├── 20_VT_ACCBRK_SUB_ANALYZERS.md (7대 전문 서브 분석기)
│       ├── 21_CORRECT.md (환경 및 콘트롤 성능 보정)
│       ├── 22_Func_ACCBRK.md (공통 연산 유틸리티)
│       ├── 30_PLOTTER_TIRE.md / 31_PLOTTER_PROJECT.md (시각화 플로터)
│       └── 90_ACCBRK_사용자매뉴얼.md (실무 사용자 매뉴얼)
├── 🛰️ gpsProcessing/          # GNSS / VBOX 공간 데이터 및 WGS84 좌표 투영 엔진 (Active)
│   ├── 00_gpsProcessing_대시보드.md (통합 허브 & MOC)
│   └── 10_GPStoXYCord.md (WGS84 타원체 벡터화 투영 엔진)
└── 🔧 (확장 예정 모듈)         # readDataFile, convenienceFunction, unoAI, Lateral 등
```

---

## 🚀 1. 핵심 활성 모듈: VT_ACCBRK & gpsProcessing

### 🏎️ 1.1 VT_ACCBRK (실차 가감속 / 제동 분석 엔진)
* 🏎️ **[[00_VT_ACCBRK_대시보드|VT_ACCBRK 통합 실차 성능 분석 시스템 대시보드]]**
  * **전체 파이프라인**: [[10_VT_ACCBRK]]
  * **개별 물리 분석**: [[11_VT_ACCBRK_TIRE]]
  * **프로젝트 취합 및 선형 보간**: [[12_VT_ACCBRK_PROJECT]]
  * **서브 분석 모듈**: [[20_VT_ACCBRK_SUB_ANALYZERS]]
  * **시각화 플로터**: [[31_PLOTTER_PROJECT]], [[30_PLOTTER_TIRE]]
  * **보정 알고리즘**: [[21_CORRECT]]
* 📜 **품질 혁신 및 체인지로그**: [[00_VT_ACCBRK_대시보드#5-버전-이력-및-주요-품질-혁신-내역-changelog--quality-audit|VT_ACCBRK v2.0 대규모 리팩토링 및 품질 혁신 내역]]

### 🛰️ 1.2 gpsProcessing (공간 데이터 처리 및 좌표 변환 엔진)
* 🛰️ **[[00_gpsProcessing_대시보드|gpsProcessing 공간 데이터 처리 및 평면 좌표계 투영 엔진 대시보드]]**
  * **핵심 투영 엔진**: [[10_GPStoXYCord]] (WGS84 타원체 정밀 벡터화, 기존 대비 5.9배 고속화, 0.06mm 정밀도)
  * **데이터 방어 필터**: VBOX 종료 시점 0.0 노이즈 격리 및 DataFrame 인덱스 100% 보존
  * **트랙 좌표계 정렬**: 테크노링 직선 제동로 기준점 및 회전각($\theta = -0.4^\circ$) 표준화


---

## 📐 2. 개발 및 엔지니어링 표준

* 📘 **[[Gemini_Python_코드_생성_규칙|Python 코드 품질 및 작성 가이드라인]]**
  * Type Hinting 전수 적용
  * Google Style Docstring 표준
  * `# region Test` 기반 단위 검증 코드 필수 탑재
  * 옵시디언 기술 문서 실시간 이중 동기화 프로토콜 준수
