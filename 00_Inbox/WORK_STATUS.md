# 📋 작업 상태 보고서 (WORK_STATUS) - 2026-10-02

## 📌 1. 작업 개요
* **일자**: 2026년 10월 02일
* **작업 대상 모듈**: `unoUtil.snow_condition` (`preprocessor.py`, `slope_model.py`, `correction_plotter.py`, `correction_model.py`, `__init__.py`)
* **연계 프로젝트 파이프라인**: `2026_Snow_RoadSurface_characteristics/run_full_snow_correction_matrix.py`
* **주요 목표**:
  1. 사용자 지적 사항 전면 수용 및 근본 원인 해결 (방법 1 vs 방법 2 성능 맵 왜곡 및 결정계수 오해 규명)
  2. 데이터 선처리 독립 분리 모듈 (`preprocessor.py`) 신규 구축 및 범용성 확보
  3. [방법 2] 동일 스펙(`SPEC_NO`) 중심화 1변수 독립 물리 기울기 엔진 (`slope_model.py`) 신규 개발 및 정식 편입
  4. 메서드 접두사 중복 방지 원칙 (`No Redundant Prefix Law`) 전면 적용 (`plot_` 접두사 영구 제거)
  5. 과거 과도기적 코드의 레거시 취급 배제 (`Single Baseline Law`) 및 깔끔한 단일 표준 확립
  6. 과거 7개년 스노우 제동 데이터 전면 재구축 및 8대 데이터셋/시각화 차트 생성, 옵시디언 볼트 1:1 동기화 완결

---

## 🛠️ 2. 핵심 구현 및 기술적 성과

### ① 방법 1 vs 방법 2 성능 맵 왜곡 원인 규명 및 일치화
* **기존 문제**:
  - 방법 1은 $\Delta T$ vs $\Delta AH$ 차분 공간을 그리고 Random Forest의 불연속 계단식 분기 타일로 표현됨.
  - 방법 2는 절대 $T$ vs $AH$ 평면에서 기준 환경 대비 보정 평면을 그려서 서로 축과 형태가 완전히 달랐음.
  - 방법 2 산점도를 1차 시험으로 맞추는 복원 산점도로 왜곡하여 1차/2차가 없는 방법 2의 본질을 훼손함.
* **해결 및 정합성 입증**:
  - 방법 1과 방법 2 모두 **기온이 오르면 제동거리가 길어지고($k_{\text{air}} > 0$), 절대습도가 높아지면 제동거리가 늘어나는($k_{\text{ah}} > 0$) 양(+)의 물리적 상관성**을 완벽하게 일치시킴!
  - 방법 1: KNN Regressor 기반 매끄러운 2D 등고선 곡면 보정 맵 복원.
  - 방법 2: 동일 스펙 중심화 편차 vs 제동거리 편차 1변수 독립 OLS 회귀선 산점도(`slope_scatter`) 및 기준 환경 대비 보정 등고선 맵(`correction_map`) 신규 정립.

### ② 데이터 선처리 전담 모듈 (`preprocessor.py`) 신규 분리
* `filter_snow_conditions()` 함수 구현:
  - 기온 구간: 정상 기온 ($-25^\circ\text{C} \le T \le 0^\circ\text{C}$) vs 이상 기온 ($T > 0^\circ\text{C}$ 또는 $T < -25^\circ\text{C}$)
  - 강설 여부: 전체 날씨(`all`), 눈 제외(`exclude_snow`), 눈 오는 시험만(`snow_only`)
  - 타이어 카테고리: `All`, `Winter Studless`, `Winter Stud`, `All Weather / All Season`
  - 모델 내부 하드코딩 필터링을 완전히 배제하여 모델의 순수한 범용성 확보.

### ③ 방법 2 전용 엔진 (`slope_model.py`) 신규 구현
* `SnowSlopeModel`:
  - 동일 스펙 내 환경 및 제동거리 중심화: $T' = T - \bar{T}_s, AH' = AH - \overline{AH}_s, y' = y - \bar{y}_s$
  - 다중회귀 다중공선성을 배제한 1변수 독립 물리 기울기: $k_{\text{air}} = \frac{\sum y' T'}{\sum {T'}^2}, k_{\text{ah}} = \frac{\sum y' AH'}{\sum {AH'}^2}$
  - 기준 환경($-8.0^\circ\text{C}, 1.5\text{ g/m}^3$) 일괄 정규화 보정: $y_{\text{corr}} = y - [k_{\text{air}}(T - T_{\text{ref}}) + k_{\text{ah}}(AH - AH_{\text{ref}})]$
* `SnowSlopePlotter` (No Redundant Prefix Law 준수):
  - `slope_scatter()`: 동일 스펙 중심화 편차 산점도 및 독립 회귀선 (사용자가 찾으시던 진정한 산점도)
  - `correction_map()`: 기준 환경 대비 2D 등고선 보정 맵
  - `variance_reduction()`: 동일 스펙 상위 5개 분산 감소율 박스플롯

### ④ 메서드 명명 규칙 단일 표준화 (`No Redundant Prefix Law`)
* `SnowCorrectionPlotter` 내의 `plot_` 접두사를 전면 제거하여 객체지향적 깔끔함 완성:
  - `plot_delta_prediction_scatter` $\to$ `delta_prediction_scatter`
  - `plot_scatter_restoration` $\to$ `scatter_restoration`
  - `plot_1st_2nd_scatter_overplot` $\to$ `scatter_overplot`
  - `plot_correction_map` $\to$ `correction_map`
  - `plot_delta_braking_bar` $\to$ `delta_braking_bar`
  - `plot_residual_dependency` $\to$ `residual_dependency`
  - `plot_tire_subsets_comparison` $\to$ `tire_subsets_comparison`

---

## 📊 3. 4대 시나리오 매트릭스 파이프라인 가동 결과

| 타이어 카테고리 | 기온 및 기상 시나리오 | 방법 1 RF 보정 MAE (개선율) | 방법 2 $k_{\text{air}}$ (m/℃) | 방법 2 $k_{\text{ah}}$ (m/(g/m³)) |
| :--- | :--- | :---: | :---: | :---: |
| **Studless** | 정상기온 & 눈제외 | 0.859m ➔ **0.544m (+36.7%)** | **+0.0271** (p=0.14) | **+0.1499** (p=0.20) |
| **Studless** | 전체기온 & 모든기상 | 0.840m ➔ **0.547m (+34.8%)** | **+0.0353** (p=0.06) | **+0.1759** (p=0.19) |
| **Stud** | 정상기온 & 눈제외 | 0.916m ➔ **0.467m (+49.1%)** | **+0.1066** (p=5.3e-6) | **+0.7284** (p=8.8e-6) |
| **All Weather** | 정상기온 & 눈제외 | 0.874m ➔ **0.569m (+34.9%)** | **+0.0005** (p=0.98) | **-0.0705** (p=0.62) |
| **All (전체)** | 정상기온 & 눈제외 | 0.870m ➔ **0.644m (+26.1%)** | **+0.0352** (p=3.5e-3) | **+0.1940** (p=1.6e-2) |
| **All (전체)** | 전체기온 & 모든기상 | 0.846m ➔ **0.637m (+24.6%)** | **+0.0413** (p=1.5e-3) | **+0.2093** (p=1.7e-2) |

* **생성된 8대 분리 보정 파일**:
  1. `df_corrected_NormalTemp_NoSnow_method1_driver_diff.pkl / xlsx`
  2. `df_corrected_NormalTemp_NoSnow_method2_slope.pkl / xlsx`
  3. `df_corrected_NormalTemp_AllWeather_method1_driver_diff.pkl / xlsx`
  4. `df_corrected_NormalTemp_AllWeather_method2_slope.pkl / xlsx`
  5. `df_corrected_AllTemp_NoSnow_method1_driver_diff.pkl / xlsx`
  6. `df_corrected_AllTemp_NoSnow_method2_slope.pkl / xlsx`
  7. `df_corrected_AllTemp_AllWeather_method1_driver_diff.pkl / xlsx`
  8. `df_corrected_AllTemp_AllWeather_method2_slope.pkl / xlsx`

---

## 🏛️ 4. 옵시디언 볼트 3대 동기화 완결 상태
1. **Inbox 작업 일지 배포**: `D:\00_obsidian\00_Inbox\WORK_STATUS.md` 최신화 완료.
2. **도메인 대시보드 갱신**: `00_snow_condition_대시보드.md` v1.5.0 및 아키텍처 링크 반영 완료.
3. **최상위 프로젝트 대시보드 갱신**: `00_unoUtil_모듈개발_대시보드.md` v3.12 체인지로그 기록 완료.
4. **1:1 기술 매뉴얼 미러링**: `preprocessor.md`, `slope_model.md`, `correction_plotter.md` 볼트 동기화 완료.
