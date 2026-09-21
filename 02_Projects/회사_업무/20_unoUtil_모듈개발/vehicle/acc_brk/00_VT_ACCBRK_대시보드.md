---
id: "work_root_20260910"
title: "VT_ACCBRK 통합 실차 성능 분석 시스템 대시보드"
type: project
category_main: 회사_업무
category_sub: VT_ACCBRK
date: 2026-09-10
priority: 높음
manager: uno
status: 진행중
tags:
  - 회사_업무
  - VT_ACCBRK
  - ACCBRK
  - unoUtil
  - 개발도구
  - 대시보드
  - MOC
aliases:
  - VT_ACCBRK_대시보드
  - ACCBRK_대시보드
  - unoUtil
  - unoUtil_대시보드
  - unoUtil허브
  - 260911_VT_ACCBRK_수정_및_점검_종합_보고서
  - 260911_unoUtil_수정_및_점검_종합_보고서
---

# 🏎️ VT_ACCBRK 통합 실차 가감속/제동 성능 분석 시스템 대시보드

> [!ABSTRACT] 📊 시스템 개요
> 본 대시보드는 실차 제동 및 가속 시험 데이터를 정밀 가공하여 기술적 인사이트를 도출하는 **VT_ACCBRK 모듈군**의 전체 아키텍처와 기술 문서들을 종합 관리하는 마스터 포털입니다.  
> **개별 분석(Tire) → 통합 및 보정(Project) → 검증 및 시각화(Plotters)**로 연결되는 전체 분석 파이프라인을 총괄합니다.

---

## 🏛️ 1. 시스템 아키텍처 및 데이터 흐름

```mermaid
graph TD
    subgraph "최상위 자동화 배치 파이프라인 (Master Pipeline)"
        VT["vt_acc_brk.py (VTAccBrk)"]
    end

    subgraph "핵심 비즈니스 분석 엔진 (Core Classes)"
        PJT["vt_acc_brk_project.py (VTAccBrkProject)"]
        TIRE["vt_acc_brk_tire.py (VTAccBrkTire)"]
        CORR["correct.py (Correct)"]
    end

    subgraph "6대 전문 물리 분석기 (Sub-Analyzers)"
        MEM["base_memory.py (BaseMemory)"]
        AN1["an_acceleration.py"]
        AN2["an_split_speed.py"]
        AN3["an_slip_pdf.py"]
        AN4["an_mu_drop.py"]
        AN5["an_skewness.py"]
        AN6["an_response.py"]
    end

    subgraph "시각화 및 리포팅 유틸리티 (Visualization & Reporting)"
        FUNC["func_acc_brk.py"]
        PLT1["plotter_tire.py (PlotterTire)"]
        PLT2["plotter_project.py (PlotterProject)"]
        EXCEL["excel.py (Excel)"]
    end

    VT --> PJT
    VT --> TIRE
    VT --> CORR
    PJT --> CORR
    PJT --> PLT2
    TIRE --> MEM & AN1 & AN2 & AN3 & AN4 & AN5 & AN6
    TIRE --> PLT1
    TIRE --> FUNC
    PLT1 & PLT2 --> EXCEL
```

## 📅 1. 프로젝트 주요 버전 이력 (Changelog 타임테이블)

| 버전 | 날짜 | 작업자 | 핵심 수정 및 개발 내역 (Changelog) | 상태 |
| :---: | :---: | :---: | :--- | :---: |
| **v2.4** | 2026-09-21 | uno &<br/>Gemini | 📂 가감속/제동 표준 폴더 내 brk_test.py, parsing_pattern.py 및 .md 파일 legacy/ 격리 수용<br/>🔌 제동 동역학 핵심 모듈 내의 레거시 Import 구문 전수 정제<br/>📝 base_memory.py 내 logger.debug f-string 개행문자 \n 전수 소거로 콘솔 한 줄 정렬 완료 | ✅ 완료 |
| **v2.3** | 2026-09-18 | uno | 🧪 14개 핵심 제동 모듈 전수 단독 자가 구동 성공 (Exit 0)<br/>🐛 13대 실차 데이터 파이프라인 런타임 결함 (PP_Slip 튜플 언패킹, SR 인덱스 등) 완전 수정 | ✅ 완료 |
| **v2.2** | 2026-09-18 | uno | 📢 print() 문 전면 퇴출 및 VT_ACCBRK 계층형 LOGGER 표준 전역 이식<br/>🛡️ 시각화 논블로킹(plt.close) 원칙 전면 준수 | ✅ 완료 |
| **v2.1** | 2026-09-18 | uno | 🚀 KDE 5000pt 샘플링 속도 10~30배 단축, VisuShrink C-엔진 일원화, compresslevel=5 최적화 | ✅ 완료 |
| **v2.0** | 2026-09-11 | uno | 🏎️ VBOX 30만 행 데이터 한계 해제 및 db4 1D Wavelet 가속도 복원 필터 도입<br/>💾 엑셀 인메모리 세션 공유로 70개 차트 원자적 저장 완료 | ✅ 완료 |

---

## 🚀 2. 핵심 분석 및 보정 파이프라인 모듈
* 🚀 **[[10_VT_ACCBRK|VT_ACCBRK 마스터 자동화 파이프라인]]**: 전체 평가 세션 원클릭 분석 및 YAML 설정 마스터 기술 백서
* 🛠️ **[[12_VT_ACCBRK_PROJECT|VT_ACCBRK_PROJECT 통합 취합 및 성능 보정]]**: 다중 타이어 취합, 콘트롤 타이어 시계열 선형 보간 엔진, 지연 로딩(`restore=False`)
* 🏎️ **[[11_VT_ACCBRK_TIRE|VT_ACCBRK_TIRE 단일 타이어 동역학 분석]]**: Wavelet 가속도 복원, 구간 자동 탐지, 6대 전문 서브 분석 모듈
* ⚙️ **[[20_VT_ACCBRK_SUB_ANALYZERS|VT_ACCBRK 6대 전문 물리 분석기]]**: 대역별 가속, 구간 속도 분할, 슬립속도 PDF, Mu-Drop 노면 대응, 왜도, 응답성 등
* 📐 **[[21_CORRECT|환경 및 콘트롤 타이어 보정 알고리즘 (correct.py)]]**: 시계열 선형 보간 기반 정지수/역수 지수 산출 및 상대 성능 지수(Index) 정규화 (구 Cal_Control 완전 통합)

---

## 🎨 3. 알고리즘 & 시각화 플로터
* 📊 **[[31_PLOTTER_PROJECT|통합 프로젝트 시각화 플로터]]**: 콘트롤 타이어 시계열 변화, 타이어 간 비교 차트 생성
* 📈 **[[30_PLOTTER_TIRE|단일 타이어 상세 시각화 플로터]]**: 슬립 PDF 분포 곡선, Mu-drop 시점 포착 시각화
* 🔧 **[[22_Func_ACCBRK|공통 수치 연산 및 유틸리티 함수군]]**: 시계열 필터링, 데이터 추출 및 보조 연산
* ⚡ **[[41_실차_제동_시계열_신호처리_및_고속_동역학_최적화_아키텍처|실차 제동 시계열 신호처리 및 고속 동역학 최적화 아키텍처]]**: C-백엔드 1D Wavelet, 적응형 KDE, Mu-Drop k-means++, 인메모리 캐시 보존 및 compresslevel=5 이론
* 📢 **[[42_실차_평가_시스템_엔터프라이즈_로깅_및_모니터링_아키텍처|실차 평가 시스템 엔터프라이즈 로깅 및 모니터링 아키텍처]]**: Print 배제 원칙, I/O 논블로킹, 계층형 LOGGER 네임스페이스 및 무중단 시각화 가이드
* 🏎️ **[[43_차세대_실차_가속제동_통합_컨테이너_및_환경보정_아키텍처|차세대 실차 가속·제동 동역학 통합 컨테이너 및 다중 환경 보정 아키텍처]]**: 비파괴 슬림 피클링(98.5% 절감), 온디맨드 자동 복원 프록시, CORRECT 시계열 과녁 보정 및 13대 실차 결함 방어 엔지니어링

---

## 📖 4. 사용자 매뉴얼 및 엔지니어링 표준
* 📖 **[[90_ACCBRK_사용자매뉴얼|VT_ACCBRK 실무 사용자 매뉴얼]]**: 3단계 분석 공정 및 함수별 매개변수 가이드
* 📘 **[[Gemini_Python_코드_생성_규칙|Python 코드 품질 및 작성 가이드라인]]**: docstring 전수화, `# region` 자가 구동 테스트, 옵시디언 동기화 프로토콜

---

