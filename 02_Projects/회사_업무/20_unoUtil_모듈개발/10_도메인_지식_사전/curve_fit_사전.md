---
id: "unoutil_dict_curve_fit"
title: "curve_fit 모듈 사전"
type: resource
category_main: 회사_업무
category_sub: unoUtil_사전
date: 2026-10-18
status: 상시운용
tags:
  - 회사_업무
  - unoUtil
  - unoUtil_사전
  - curve_fit
  - 커브피팅
  - Pacejka
  - 에르미트스플라인
aliases:
  - "curve_fit_사전"
  - "curve_fit 모듈 사전"
---

# 📖 curve_fit 모듈 사전 (Domain Engineering Guide)

> 📌 **전용 사전 바로가기**: [[tire_curve_사전|🛞 tire_curve 모듈 사전 (TireCurve 객체 구조 & 과도기 위상 싱크)]]
>
> ⚡ **Quick Jump**: [🎯 1. 설계 철학](#-1-설계-철학-및-모듈-개요) · [📚 2. 배경 지식](#-2-배경-지식-및-이론-지식-허브) · [🏗️ 3. 아키텍처](#️-3-아키텍처-및-데이터-파이프라인) · [🚀 4. 실전 워크플로우](#-4-실전-워크플로우-및-종합-스니펫) · [🛠️ 5. 트러블슈팅](#️-5-트러블슈팅-및-튜닝-노하우)

> [!ABSTRACT] 🎯 도메인 개요
> 타이어의 슬립율(종방향) 및 슬립각(횡방향)에 따른 마찰 특성 곡선을 수학적으로 피팅하고, **초기 선형 영역과 후반 한계 영역을 매끄럽게 접합(Hermite Blending)하여 고정밀 타이어 특성 곡선을 도출하는 차세대 3계층 비선형 회귀 프레임워크**입니다.

---

## 🎯 1. 설계 철학 및 모듈 개요

### 1.1. 탄생 배경과 목적
* **기존 방식의 한계**: 타이어 도메인(`tire_curve`)과 순수 수학적 피팅 코드가 결합되어 있어 모델 변경 및 최적화 전략 교체가 어려웠음. 복합 스플라인 결합 시 5분 이상 소요되는 심각한 속도 병목 존재.
* **해결 과제**: "데이터(x, y)와 모델 주입" 기반의 3계층 아키텍처 확립, 3대 범용 추정기(`LeastSquares`, `Optimize`, `Combiner`) 프로토콜 통일, 에르미트 접합 2D 탐색 다운샘플링(5분 $\to$ **0.05초** 단축).
* **핵심 가치**: 타이어 공학 지식(원점 구속, 초기 강성 $B \cdot C \cdot D$)과 범용 수학 회귀 엔진의 완전한 분리(Decoupling).

### 1.2. 아키텍처 설계 사상
* **Base Estimator Protocol**: 모든 추정기에 `__init__(model_func)`, `.fit(x, y)`, `.predict(x)`, `self.rmse`, `.plot(save, close=False)`, `is_fitted` 규격 100% 강제.
* **의존성 주입 (Dependency Injection)**: `CombinerEstimator` 내부의 특정 수식 하드코딩을 배제하고, 외부에서 임의의 선형/비선형 모델을 자유롭게 주입받아 복합 모델(`Predictor`)을 도출.
* **단일 기준 불변 원칙 (Single Baseline Law)**: 과도기적 레거시(`CurveCombiner`, `fit_mf_ax` 등)를 전면 배제하고 `TireCurve` 단일 파사드 클래스로 단일화.

---

## 📚 2. 배경 지식 및 이론 (지식 허브)

> [!NOTE] 🧠 공학 이론 및 알고리즘 위키 링크 (Knowledge Atomization)
> *비선형 회귀 및 타이어 전단 마찰 이론은 `04_Resources`에 영구 보존되어 있습니다.*

* 📄 **메타 추정기 및 에르미트 블렌딩**: [[40_비선형_회귀_메타_추정기_및_에르미트_블렌딩_아키텍처|비선형 회귀 메타 추정기 및 에르미트 블렌딩 아키텍처 (SSOT)]]
* 📄 **제동 시작점 및 초기 과도 4-랜드마크 복원 공학**: [[31_실차_제동_시작점_자동_탐지_및_과도응답_슬립_복원_공학|실차 제동 시작점 자동 탐지, L0~L3 위상 정합 및 정상 피팅 분리 공학]]
* 📄 **타이어 전단력 및 접지 마찰**: [[10_Tire_Shear_Force|타이어 접지면 전단력 및 마찰 특성]]
* 📄 **Pacejka MF 수식 규격**: [[12_차량_시스템_제동성능과_마찰계수_상관관계|Pacejka Magic Formula 및 마찰계수 상관관계]]
* 📄 **차량 제동 시뮬레이션**: [[10_차량_제동_동역학_시뮬레이션|타이어 슬립 곡선 기반 제동 동역학 시뮬레이션]]

---

## 🏗️ 3. 아키텍처 및 데이터 파이프라인

### 3.1. 3계층 메타 아키텍처 다이어그램

```mermaid
flowchart TD
    subgraph Layer1 [1계층: 도메인 파사드 (Domain Facade)]
        TC["TireCurve (cf_tire.py)\n(method: constrained_mf | split_blend | combiner | least_squares | optimize)"]
        LM["calc_brk_transient_landmarks\n(L0→L1→L2→L3 위상 정합, K_pk & dmu/dt 산출, L0~L3 본체 분리)"]
        BW["calc_bin_density_weights\n(구간 밀도 역가중치 w_i ∝ N_b^-0.65)"]
        KInit["calc_initial_stiffness\n(RANSAC 원점 통과 초기 탄성 강성 K 추정)"]
    end

    subgraph Layer2 [2계층: 범용 수학 추정기 (Estimators Protocol)]
        LS["LeastSquaresEstimator\n(Scipy Huber/Loss 비선형)"]
        OP["OptimizeEstimator\n(Scipy minimize / L-BFGS-B)"]
        CB["CombinerEstimator\n(에르미트 2D 탐색 스플라인 합성)"]
    end

    subgraph Layer3 [3계층: 순수 수식 SSOT (models/)]
        MF["magic_formula.py\n(magic_formula / constrained_magic_formula + Snow Wedge)"]
        Linear["선형 초기 구간 (y = K * x)"]
    end

    TC --> LM
    TC --> BW
    TC --> KInit
    TC --> Layer2
    Layer2 --> Layer3
```

### 3.2. 핵심 서브모듈 역할 분담표

| 파일명 | 담당 클래스 / 함수 | 핵심 책임 및 역할 |
| :--- | :--- | :--- |
| `cf_tire.py` | `TireCurve`, `calc_brk_transient_landmarks`, `calc_bin_density_weights`, `calc_initial_stiffness`, `plot_tire_set_curve_comparison` | 타이어 도메인 최상위 파사드 (5대 피팅 엔진, 제동 초기 4-랜드마크 위상 정합 및 `L0~L3` 과도 데이터 분리, 구간 밀도 역가중치, 스노우 웻지 보정, 제외 데이터 마커 분리 및 포함/제외 비교 시각화) |
| `magic_formula.py` | `magic_formula`, `constrained_magic_formula` | 표준 4파라미터 Pacejka MF 및 초기 강성 구속($B = \frac{K}{C \cdot D}$) 3파라미터 Pacejka MF 수식 SSOT |
| `least_squares_estimator.py` | `LeastSquaresEstimator` | Scipy `curve_fit` 기반 잔차 제곱합 최소화 및 이상치 방어(Huber Loss) |
| `optimize_estimator.py` | `OptimizeEstimator` | 경계 조건(Bounds) 및 구속 조건을 갖는 범용 파라미터 최적화기 |
| `combiner_estimator.py` | `CombinerEstimator` | 전반 선형 구간과 후반 곡선 구간의 최적 접합점 탐색 및 $C^1$ 연속 에르미트 스플라인 합성 |

---

## 🚀 4. 실전 워크플로우 및 종합 스니펫

```python
"""
TireCurve를 활용한 실차 타이어 슬립-마찰계수 다중 모델 피팅 (해법 C & 해법 A-v2)
"""
from pathlib import Path
from unoUtil.curve_fit import TireCurve, calc_brk_transient_landmarks, plot_tire_set_curve_comparison

# 1. 해법 C (2단계 강성 구속 단일 MF + L0~L3 과도 루프 분리 + 고슬립 스노우 웻지) 정식 피팅
tc_cmf = TireCurve(
    tire=tire,
    method="constrained_mf",
    filter_deadzone=True,
    filter_transient=True,
    balance_bins=True,
    enable_wedge=True,
).fit()

# 2. 해법 A-v2 (사용자 제안 2D 분포 분할 시그모이드 블렌딩) 피팅
tc_sb = TireCurve(tire=tire, method="split_blend").fit()

# 3. 핵심 물리 파라미터 및 초기 과도 랜드마크 지표 추출
print(f"[Constrained MF] K={tc_cmf.stiffness:.2f}, Peak Mu={tc_cmf.peak_value:.3f}, RMSE={tc_cmf.rmse:.4f}")
if tc_cmf.transient_landmarks is not None:
    lm = tc_cmf.transient_landmarks
    print(f"[Transient Landmarks] k_L1={lm['k_L1_med']:.3f}, K_pk={lm['K_pk_med']:.2f}, dmu/dt={lm['dmu_dt_med']:.2f} g/s")

# 4. 검증 시각화 차트 자동 저장 (제외 데이터 ✕/△ 분리 표시 + 초기 포함/제외 곡선 동시 오버레이)
tc_cmf.plot(save=Path("reports/tire_curve_fit.png"), binned=True, compare_unfiltered=True, close=True)
```

---

## 🛠️ 5. 트러블슈팅 및 튜닝 노하우

### 5.1. 초기 슬립 구간 역기울기 및 음수 슬립 결함
* **증상**: 노이즈로 인해 슬립율 0 부근에서 기울기가 음수로 계산되거나 원점을 통과하지 않는 현상.
* **조치**: `TireCurve(force_origin=True)`를 활성화하여 $(0, 0)$ 원점 구속 조건을 걸고, 초기 5샘플 구간에 최소자승 가중치 10배(`sample_weight`)를 부여.

### 5.2. Combiner 피팅 연산 지연 시
* **증상**: 대용량 시계열(10만 포인트 이상) 입력 시 에르미트 탐색이 지연되는 현상.
* **조치**: 내부 최적화가 적용된 다운샘플링 인자 `downsample_bins=200`을 명시하여 0.05초 이내 고속 근사 연산 유지.

### 5.3. 제동 시작점 타행 감속 오판 및 Ax_onset 기반 이상치 판정 (v3.42)
* **증상**: 운전자가 제동 전 엑셀을 밟아 가속하던 구간이나 타행 주행(-0.02~-0.04g) 구간을 제동 시작점으로 오판하여 시작점이 1.5초 이상 앞당겨지거나, 운전자 진입 타이밍(Δt) 편차로 정상 런이 아웃라이어로 잘려나가는 결함.
* **조치**:
  1. **평형 기저선 0 근처 강제**: 가속 구간(Ax > 0.03g)을 기저선 탐색에서 원천 배제하고 Ax <= 0.01g 범위에서 base_mean 및 safe_std를 산출.
  2. **Min Jerk 피크 및 노이즈 밴드 Onset**: 유압 제동 급강하 피크(-4.5 ~ -5.0 g/s)로부터 과거로 거슬러 올라가며 Jerk >= -0.30 g/s 및 Ax <= base_mean + 2*std인 변곡점 Onset을 정밀 포착.
  3. **양방향 윈도우 탐색**: 운전자가 1차 속도 기준점을 통과한 직후(미래 0.8초)에 밟은 런까지 포괄하도록 과거 1.2초 ~ 미래 0.8초 양방향 탐색 적용.
  4. **Ax_onset 기준 아웃라이어 판정**: 진입 시간차(Δt) 대신 시작점 가속도가 0 근처 평형 밴드(-0.09g ~ +0.025g)를 유지하는지로 불량 런을 자동 선별.

### 5.4. Combiner 초기 선형 구간 부재 및 원점 직선 보정 (v3.42)
* **증상**: CombinerEstimator 실행 시 `ind_end_line == 0` 조기 탈출문으로 인해 LineMaker 직선 생성이 스킵되고 순수 매직포뮬러 곡선만 렌더링되거나 원점에서 평평해지는 결함.
* **조치**:
  1. `ind_end_line == 0` 조기 탈출문을 걷어내고, 저슬립 대역(0~2%)에서 `LineMaker`가 항상 RANSAC/ODR 직선을 추출하도록 파이프라인 가동.
  2. `HermiteConnector` / `ClothoidConnector`를 통해 초기 직선과 후반 곡선을 완화 결합하고, 원점(0, 0)과 직선 시작점 사이를 선형 연장하여 원점에서 솟구치는 굵은 선형 강성 직선을 완벽 복원.

---

## 🔬 6. 실차 계측 데이터 MF 한계 극복: 해법 C (`constrained_mf`) & 해법 A-v2 (`split_blend`) 정식 엔진 탑재 (v3.44 ~ v3.45 완결)

### 6.1. 실차 데이터에서 표준 MF 최적화가 무너지는 3대 메커니즘
1. **데이터 제어 집중 몰림 (Data Clumping)**:
   - ABS/TCS 제어로 인해 전체 데이터의 80~90%가 피크 슬립($10 \sim 25\%$) 주변에 집중되어, 최소자승법(Least Squares)이 초반 저슬립($0 \sim 3\%$)의 탄성 강성선을 완전히 무시하고 원점에서 $y \approx 0.13g$로 붕 떠버림.
2. **초반 기울기와 피크 폭의 수학적 양립 불가**:
   - $B$를 키워 원점 기울기($B \cdot C \cdot D$)를 맞추면 $\arctan(Bx)$가 $x < 0.01$에서 조기 포화($\pi/2$)되어 피크가 사각 박스처럼 왜곡됨.
3. **가속 초기 지연 및 극저속 휠스핀 노이즈**:
   - 출발 직후 극저속($V < 8\,\text{km/h}$) 구간에서 분모 $V$가 작아 슬립율이 $100 \sim 278\%$로 폭주하므로, `TireCurve._extract_data_from_tire`에서 가속 시 $V \ge 8.0\,\text{km/h}$, 제동 시 $V \ge 3.0\,\text{km/h}$ 및 $0 < x \le 1.0$ 스마트 필터링을 기본 적용함.

### 6.2. 해법 C (`method="constrained_mf"`) — 2단계 강성 구속 단일 Magic Formula
1. **1단계 (`calc_initial_stiffness`)**: 저슬립 탄성 영역($0 \le x \le 0.035$)에서 원점 구속 RANSAC(상위 분위수 탄성 엔벨로프 추종)으로 초기 탄성 강성 $K = \frac{dy}{dx}\big|_{x=0}$를 확정합니다.
2. **2단계 (`constrained_magic_formula`)**: MF 수식의 등식 제약 $B = \frac{K}{C \cdot D}$를 주입하여 3파라미터($C, D, E$) 단일 MF를 최적화합니다:
   $$y(x) = D \cdot \sin \left( C \cdot \arctan \left( \frac{K}{CD} x - E \left( \frac{K}{CD} x - \arctan\left(\frac{K}{CD} x\right) \right) \right) \right)$$

### 6.3. 해법 A-v2 (`method="split_blend"`) — 사용자 제안 2D 분포 분할 시그모이드 블렌딩
- **기존 해법 A(v1)의 Hump(불룩함) 원인**: 전 대역 데이터를 한꺼번에 피팅하여 초반($x=0$)에서 $0.13g$로 붕 뜬 오염된 MF 곡선과 직선 $K \cdot x$를 블렌딩하면서 $x \approx 0.04 \sim 0.08$ 전이부가 데이터 구름 상단으로 불룩 솟구침.
- **해법 A-v2 해결 메커니즘**:
  1. 1D 히스토그램 KDE 밀도 능선으로부터 제어 클러스터 진입 변곡점 $x_{\text{kde\_onset}}$을 자동 포착합니다.
  2. 고슬립 클러스터 영역($x \ge x_{\text{kde\_onset}}$) 데이터만으로 순수 4파라미터 MF($y_{\text{MF\_high}}$)를 독립 피팅합니다.
  3. 저슬립 탄성 직선 $y_{\text{line}}(x) = K \cdot x$와 고슬립 순수 MF $y_{\text{MF\_high}}(x)$가 교차하는 지점을 전이점 $x_{\text{trans}}$로 확정하고, 시그모이드 가중치 $w(x) = \frac{1}{1 + \exp(-(x - x_{\text{trans}})/\tau)}$로 매끄럽게 블렌딩하여 전이부 Hump를 원천 제거합니다:
     $$y(x) = (1 - w(x)) \cdot (K \cdot x) + w(x) \cdot y_{\text{MF\_high}}(x)$$

---

## 🛑 7. 제동 초기 과도 응답 4-랜드마크(`L0~L3`) 위상 정합, 본체 피팅 분리 및 고슬립 스노우 웻지 고도화 (v3.46 완결)

### 7.1. 제동 초기 4-랜드마크(`L0 → L1 → L2 → L3`) 위상 정합 및 2대 물리 지표 (`calc_brk_transient_landmarks`)
- **4-랜드마크 정의**:
  - `L0` ($s=0$): 제동 시작점 (`find_brake_start_point` Onset, $\kappa \approx 0, \mu \approx 0$)
  - `L1` ($s=1$): 휠 관성 토크($I_w\dot{\omega}_w$) 불감대 종료 및 차체 감속도 발현 변곡점 ($\mu \ge 0.035\text{g}$, 평균 $\Delta t_{L1} \approx 50 \sim 80\,\text{ms}$, $\kappa_{L1} \approx 2.2 \sim 2.6\%$)
  - `L2` ($s=2$): 초기 과도 1차 최대 마찰 피크 ($\mu_{L2} \approx 0.43 \sim 0.45\text{g}$)
  - `L3` ($s=3$): 1차 ABS 감압 해제 골짜기 (정상 상태 ABS 사이클링 진입점)
- **초기 응답 2대 지표 동시 산출**:
  - **피크-코드 강성 ($K_{\text{pk}} = \mu_{L2}/\kappa_{L2}$)**: 휠 관성 딜레이($\kappa_{L1}$)와 순수 탄성 기울기($K_{\text{build}}$)가 결합된 슬립 축 실효 초기 강성.
  - **시간축 마찰 빌드업 속도 ($d\mu/dt = \Delta\mu_{10\to 90\%}/\Delta t$)**: 휠속도 노이즈와 무관하게 순수 종가속도(`Ax`)와 시간(`Time`)만으로 평가하는 응답 속도 지표.

### 7.2. 초기 과도 루프(`L0~L3`) 전체 분리 후 정상 상태(`L3~`) 본체 피팅 원칙 (`filter_deadzone=True`, `filter_transient=True`)
- **물리적 분리 사유**: 초반 기울기를 잡기 위해 복원한 `L0 → L3` 구간은 ① `L0 → L1` 관성 불감대($\mu < 0.035\text{g}$ 바닥 수평선)와 ② `L1 → L3` 1차 과도 스파이크($\mu \approx 0.43 \sim 0.45\text{g}$ 저슬립 상단 군집)로 구성되어, 실제 제동 거리의 $90\%$ 이상을 차지하는 `L3` 이후 정상 상태($\mu \approx 0.36 \sim 0.40\text{g}$)와 영역대가 다름.
- **이원화 파이프라인**:
  1. `L0 → L3` 데이터는 오직 **초기 종방향 강성($K_{x0}$) 및 과도 응답 지표($K_{\text{pk}}, d\mu/dt$) 추출에만 사용**하고 `self.deadzone_data`(`L0~L1`) 및 `self.transient_data`(`L1~L3`)로 분리 보관.
  2. 본체 커브 피팅(`constrained_mf`, `split_blend`, `combiner`, `least_squares`)은 **`L0~L3`를 완전히 제거한 `L3` 이후 정상 제동 데이터만으로 수행**하여 피팅 오차(RMSE)를 **$18.5\% \sim 23.7\%$ 대폭 절감**.
- **시각화 분리 표시 (`compare_unfiltered=True`)**:
  - 정상 피팅 데이터: 차속(`Vel`) 컬러맵 원형 마커(`●`)
  - 제외 데이터 ① (`deadzone_data`, `L0~L1`): 빨간색 `✕` 마커 (`#e41a1c`)
  - 제외 데이터 ② (`transient_data`, `L1~L3`): 주황색 빈 삼각형 `△` 마커 (`#ff7f00`)
  - 초기 과도 포함 Fit (보라색 파선 `--`) vs 초기 과도 제외 최종 Fit (빨간색 실선 `—`) 동시 오버레이 비교 지원.

### 7.3. 고슬립($\kappa > 0.25$) 이격 해소: 구간 밀도 역가중치(`calc_bin_density_weights`) & 스노우 웻지(`enable_wedge=True`)
- ABS 제어 집중($85\%$ 이상이 $\kappa < 0.25$)으로 인한 고슬립 과소 대표를 역거듭제곱 가중치($w_i \propto N_b^{-0.65}$)로 보정하고, 스노우 노면 고슬립 눈 쐐기(Snow Wedge) 재상승 항($+ W_{\text{snow}} \cdot \max(0, \kappa - \kappa_{\text{valley}})$)을 결합하여 $\kappa \in [0.25, 0.60]$ 구간의 하향 이격(Gap)을 완전히 해소함.

### 7.4. 스노우 제동(`Snow_ACC_BRK` 40→5 kph) 초기 과도 포함 vs 제외 정량 비교 요약
| 타이어 세트 | 정상 피팅 (`L3~`) | 제외① 데드존 (`L0~L1`, `✕`) | 제외② 과도루프 (`L1~L3`, `△`) | 초기강성 $K_{\text{pk}}$ / $d\mu/dt$ | 초기 과도 포함 (`L1~L3` 포함) $\mu_{\text{peak}}$ / RMSE | **초기 과도 제외 (`L0~L3` 제거) $\mu_{\text{peak}}$ / RMSE** | **RMSE 감소율** |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **C1** | 2,788 pts | 97 pts | 208 pts | 4.86 / 3.09 g/s | 0.368 (@16.5%) / 0.0651 | **0.366 (@17.5%) / 0.0522** | **-19.8%** |
| **T1** | 2,730 pts | 101 pts | 209 pts | 5.29 / 3.08 g/s | 0.384 (@16.9%) / 0.0715 | **0.383 (@17.7%) / 0.0555** | **-22.4%** |
| **T2** | 1,954 pts | 54 pts | 145 pts | 4.46 / 3.24 g/s | 0.404 (@22.9%) / 0.0739 | **0.420 (@30.0%) / 0.0564** | **-23.7%** |
| **C2** | 3,228 pts | 121 pts | 263 pts | 5.83 / 3.19 g/s | 0.389 (@17.0%) / 0.0729 | **0.388 (@18.0%) / 0.0594** | **-18.5%** |

---

## 🔗 8. `VTAccBrkTire.curve_fit` 공식 서브 분석기 통합 및 프로젝트 콘트롤 보정 동기화 (v3.48 / `cf_tire` v4.5 완결)

### 8.1. `fit()`(파라미터 추정) vs `predict(x, interval)`(곡선 생성) 책임 분리 및 `df` 표준 스키마
- **`fit(...)`**: 입력된 `VTAccBrkTire` 객체(또는 단독 데이터프레임)로부터 유효 슬립-가속도 샘플을 추출(`df_raw`)하고, 선택된 6대 최적화 메서드(`'robust'`, `'binning'`, `'two_stage'`, `'ransac'`, `'lsq'`, `'custom'`)로 Magic Formula 파라미터(`B, C, D, E, Sh, Sv`) 및 물리 지표(`peak_mu`, `peak_slip`, `stiffness`)를 추정한 뒤 기본 구간 $[0.0, 1.0]$ ($\Delta\kappa = 0.005$, 201 pts) 예측 곡선을 `self.df`에 생성합니다.
- **`predict(x=None, interval=0.005, update_df=False)`**:
  - `x=None`: 기본 $[0.0, 1.0]$ 구간을 `interval` 간격으로 생성하여 예측.
  - `x=[start, end]` (2-원소 구간 튜플/리스트): `[start, end]` 구간을 `interval` 간격으로 등간격 격자화하여 예측.
  - `x=np.ndarray` (3개 이상 원소 배열): 전달된 슬립률 배열 위치에서 직접 예측값 산출.
- **`curve_fit.df` 시계열 스키마**: `['Slip', 'Acc']` (컨트롤 보정 후 `['Slip', 'Acc', 'corr_mean_Acc', 'corr_curve_Acc']` 자동 확장).

### 8.2. 휠스피드 부재 시 자동 Skip 및 시험 모드·차량 구동방식(`TestVehicleLayout`) 기반 슬립 축 자동 결정
1. **휠스피드/슬립 채널 부재 시 Graceful Skip**: 원시 계측 데이터에 휠스피드(`WheelSpeed_*`) 또는 슬립(`WheelSlip_*`) 채널이 존재하지 않으면 에러 없이 `is_fitted = False` 상태로 안전하게 건너뛰어 기존 가감속/제동 파이프라인의 무중단 실행을 보장합니다.
2. **시험 모드(`brk`/`acc`) 및 구동방식(`TestVehicleLayout`) 연동 슬립 축 자동 선택 (`_resolve_slip_series`)**:
   - **사용자 명시 (`col_slip`)**: 단일 컬럼명, 리스트(유효 채널 평균), 또는 `'front'`/`'rear'`/`'all'` 키워드 지정 시 최우선 적용.
   - **제동 (`mode='brk'`)**: 기본값 **전륜축 (`'front'`: `WheelSlip_FL`, `WheelSlip_FR` 중 유효 채널 평균)**.
   - **가속 (`mode='acc'`)**: `tire.infor.result` 내 `TestVehicleLayout` (`Layout`, `DriveType` 등) 메타데이터를 자동 조회하여 **`RWD`/`FR`/`MR`/`RR`이면 후륜축(`'rear'`: `RL`/`RR`), `AWD`/`4WD`이면 4륜 전체(`'all'`), `FWD`/`FF` 또는 미지정 시 전륜축(`'front'`)** 을 자동 선택합니다 (`col_slip_used` 속성에 기록).

### 8.3. 프로젝트 콘트롤 타이어 보정(`Correct.run`) 동기화 및 다중 타이어 비교 시각화
- **콘트롤 게인($G_i$) 자동 동기화 ([[30_실차_가감속_성능변화_분석_및_보정_시스템#7. 🎯 비선형 마찰 곡선(Magic Formula)의 콘트롤 게인 스케일링 동형성 법칙 (Control Gain Scaling Isomorphism)|콘트롤 게인 스케일링 동형성 법칙]])**:
  - `VTAccBrkProject`에서 `Correct.run()` 수행 시, 각 타이어의 `mean_Acc` 대비 보정 가속도(`corr_mean_Acc`, `corr_curve_Acc`) 비율인 콘트롤 게인 $G_i$를 산출하여 `tire.curve_fit.df` (`corr_mean_Acc`, `corr_curve_Acc`), `tire.curve_fit.df_raw`, 그리고 `tire.curve_fit.params` (`corr_D`, `corr_peak_mu`, `corr_stiffness`) 및 프로젝트 요약표(`corr_cf_peak_mu`, `index_cf_peak_mu`, `corr_cf_stiffness`, `index_cf_stiffness`, `corr_cf_D`)에 일괄 반영합니다.
- **시각화 인터페이스**:
  - 단일 타이어: `tire.plot.curve_fit(detail=False)` (기본 산점도 + MF 피팅 곡선) 및 `tire.plot.curve_fit_detail()` (6-패널 종합 진단 대시보드).
  - 프로젝트 다중 비교: `project.plot.compare_curve_fit(corr='mean', xlim=(0.0, 1.0), show_scatter=False, show_peak=True)`를 통해 $0 \sim 1.0$ 전 구간에서 보정된 타이어별 MF 마찰 곡선과 Peak $\mu$ 마커를 한눈에 오버레이 비교합니다.


