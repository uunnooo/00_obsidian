---
id: "post_process_dashboard_20260918"
title: "post_process (신호 후처리 패키지) 대시보드"
type: resource
category_main: 회사_업무
category_sub: 개발대시보드
date: 2026-09-18
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - 신호처리
  - post_process
  - 대시보드
  - MOC
project_link: "[[unoUtil]]"
---

# 📶 post_process (신호 후처리 및 정제 패키지) 대시보드

> [!ABSTRACT] 🛠️ 패키지 개요
> 기존의 단일 모놀리식 파일(`_UnoPP_.py`)을 **단일 책임 원칙(SRP)**에 따라 4대 전문 서브모듈로 분할하고, 100% 무중단 하위 호환성을 제공하는 차세대 실차 신호 후처리 패키지입니다.

```mermaid
flowchart TD
    PP["signal_process.post_process"] --> F["🌊 filters<br/>(Zero-phase MA & SOS)"]
    PP --> R["⏱️ resample<br/>(비수치 보존 리샘플링/병합)"]
    PP --> O["🛡️ outliers<br/>(다변량 이상치 & 연속구간)"]
    PP --> S["📐 scaler<br/>(MinMax / Standard / Robust)"]
```

---

## 📦 4대 핵심 서브모듈 구성 및 링크

1. 🌊 **[[filters|filters (Zero-Phase 이동평균 필터)]]**:
   - `moving_average` (`SP_MovingAverage`): 위상 지연 없는 양방향 필터
   - `moving_average_fast` (`SP_HighSpeed_MovingAverage`): 고속 SOS 필터
2. ⏱️ **[[resample|resample (비수치 보존 리샘플링)]]**:
   - `resample_data` (`SP_Resample`), `interpolate_data` (`SP_Interpolation`), `merge_data` (`SP_Merge`)
3. 🛡️ **[[outliers|outliers (이상치 정제 및 연속구간)]]**:
   - `remove_outliers` (`SP_RMOutlier`): Percentile, Z-score, iForest, Extended IF
   - `find_continuous_interval` (`SP_FindContinue`): 제동 등 유효 구간 색출
4. 📐 **[[scaler|scaler (데이터 정규화)]]**:
   - `scale_data` (`SP_Normal`): MinMax, StandardScaler, RobustScaler

## 📅 1. 프로젝트 주요 버전 이력 (Changelog 타임테이블)

| 버전 | 날짜 | 작업자 | 핵심 수정 및 개발 내역 (Changelog) | 상태 |
| :---: | :---: | :---: | :--- | :---: |
| **v2.4** | 2026-09-21 | uno &<br/>Gemini | 📂 _UnoPP_.py, ExtendedIsolationForest.py 및 .md 파일 post_process/legacy/ 격리 수용<br/>🔌 outliers.py 등 내부 구버전 임포트 구문 제거 및 V2.0 순수 API 연계 수술<br/>🔌 상위 제동 엔진 내부에서 _UnoPP_ 가리키던 Import 구문 전면 정화 | ✅ 완료 |
| **v2.0** | 2026-09-18 | uno | ⏱️ 단일 거대 _UnoPP_.py 모듈을 filters, resample, outliers, scaler 4대 모듈로 완벽 재편<br/>🔌 sys.modules 래퍼 주입으로 구버전 코드 무중단 호환성 완전 부활 | ✅ 완료 |

---

## 📚 관련 영구 공학 지식 레퍼런스
* 📡 **[[25_실차_신호처리_및_시계열_데이터_정제_공학|실차 신호처리 및 시계열 데이터 정제 공학]]**
* 🏗️ **[[26_대규모_파이썬_패키지_모듈화_및_무중단_하위호환_아키텍처|대규모 파이썬 패키지 모듈화 및 무중단 하위호환 아키텍처]]**
* 🧭 **상위 허브**: [[00_unoUtil_모듈개발_대시보드]]

---

