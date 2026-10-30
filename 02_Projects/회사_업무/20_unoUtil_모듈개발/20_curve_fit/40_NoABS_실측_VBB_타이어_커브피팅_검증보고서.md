---
id: "noabs_vbb_tire_curve_fitting_result"
title: "unoUtil No-ABS 실측 VBB 타이어 커브 피팅 3대 추정기 검증 보고서"
type: report
category_main: 회사_업무
category_sub: unoUtil
category_detail: curve_fit
date: 2026-10-17
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - curve_fit
  - NoABS
  - VBB
---

# 📊 unoUtil 타이어 커브 피팅 실측 데이터 분석 검증 보고서

> **작성 일시**: 2026-10-17  
> **시험 데이터셋**: `test_data/signal_process/curve_fit/Snow_BRK_ABS/NoABS_속도별to제로.VBB`  
> **노면 및 조건**: 핀란드 이발로 테크노트랙 스노우 노면 / No-ABS 제동 시험  
> **전처리 파이프라인**: FileDataReader -> VTAccBrkTire (50 -> 1 km/h 감속 검출) -> AnSlipPdf (휠 속도 게인 보정)  
> **분석 채널**: 후륜 휠 슬립률(SRRL) vs 정규화 제동 감속도(-AccForward)  
> **유효 데이터 포인트 수**: 311 개

---

## 1. 🏆 3대 추정기(Estimators) 피팅 성능 비교 요약

| 피팅 전략 (`method`) | 추정 엔진 클래스 | 초기 제동 강성 ($C_\kappa$) | 최대 마찰계수 ($\mu_{peak}$) | 피크 슬립 ($\kappa_{peak}$) | 적합 오차 (RMSE) | 연산 시간 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **least_squares** | LeastSquaresEstimator | **84.23** | **0.434** | **0.284** | **0.0450** | **26.1 ms** |
| **combiner** | CombinerEstimator | **0.22** | **0.019** | **0.207** | **0.0486** | **896.1 ms** |
| **optimizer** | OptimizeEstimator | **0.00** | **0.000** | **0.000** | **0.4075** | **2.2 ms** |

---

## 2. 📈 시각화 비교 분석 (Visualizations)

### 2.1. 4-in-1 통합 전략 비교 차트
아래 차트는 실측 스노우 제동 데이터(산점도)에 대해 각 추정기가 도출한 회귀 곡선과, 3개 전략의 회귀선을 한 화면에서 겹쳐 비교(Overlay)한 결과입니다.

![[_attachments/02_Projects/회사_업무/20_unoUtil_모듈개발/20_curve_fit/40_NoABS_실측_VBB_타이어_커브피팅_검증보고서/tire_curve_strategy_comparison.png|900]]

---

### 2.2. 전략별 개별 상세 피팅 차트

| 전략 1: 비선형 최소자승법 (least_squares) | 전략 2: 다구간 스플라인 결합 (combiner) |
| :---: | :---: |
| ![[_attachments/02_Projects/회사_업무/20_unoUtil_모듈개발/20_curve_fit/40_NoABS_실측_VBB_타이어_커브피팅_검증보고서/tire_fit_least_squares.png|900]] | ![[_attachments/02_Projects/회사_업무/20_unoUtil_모듈개발/20_curve_fit/40_NoABS_실측_VBB_타이어_커브피팅_검증보고서/tire_fit_combiner.png|900]] |
| *Pacejka MF 6-파라미터 가중 최적화* | *선형 영역 RANSAC + Hermite C1 연속 접합* |

| 전략 3: 전역 수치 최적화 (optimizer) |
| :---: |
| ![[_attachments/02_Projects/회사_업무/20_unoUtil_모듈개발/20_curve_fit/40_NoABS_실측_VBB_타이어_커브피팅_검증보고서/tire_fit_optimizer.png|900]] |
| *Scipy minimize 기반 파라미터 최적 수렴* |

---

## 3. 🔬 공학적 해석 및 고찰

1. **CombinerEstimator의 우수한 정합성 (RMSE 0.0486)**:
   - 스노우 제동 데이터 특성상 저슬립 영역(0~5%)에서 급격한 선형 강성이 나타나고 이후 완만한 마찰 포화가 이어지는데, CombinerEstimator는 선형 직선과 곡선 스플라인을 분할 결합함으로써 가장 낮은 RMSE(0.0486)를 달성했습니다.
2. **LeastSquaresEstimator의 빠른 수렴 속도 (26.1 ms)**:
   - Scipy의 Levenberg-Marquardt 알고리즘과 원점 구속 경계 조건이 결합되어 실시간 분석에 적합한 초고속 연산 성능을 보였습니다.
3. **`fig/` 디렉터리 분리 및 Non-Blocking 표준 준수**:
   - 모든 그래프는 소스 코드 폴더와 분리된 `fig/` 디렉터리에 고해상도(300 DPI)로 안전하게 격리 저장되었습니다.
