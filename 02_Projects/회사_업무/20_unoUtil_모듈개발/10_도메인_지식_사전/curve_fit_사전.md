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
* 📄 **타이어 전단력 및 접지 마찰**: [[10_Tire_Shear_Force|타이어 접지면 전단력 및 마찰 특성]]
* 📄 **Pacejka MF 수식 규격**: [[12_차량_시스템_제동성능과_마찰계수_상관관계|Pacejka Magic Formula 및 마찰계수 상관관계]]
* 📄 **차량 제동 시뮬레이션**: [[10_차량_제동_동역학_시뮬레이션|타이어 슬립 곡선 기반 제동 동역학 시뮬레이션]]

---

## 🏗️ 3. 아키텍처 및 데이터 파이프라인

### 3.1. 3계층 메타 아키텍처 다이어그램

```mermaid
flowchart TD
    subgraph Layer1 [1계층: 도메인 파사드 (Domain Facade)]
        TC["TireCurve (cf_tire.py)\n(원점 구속, 초기 강성 B*C*D 물리 파라미터 제어)"]
    end

    subgraph Layer2 [2계층: 범용 수학 추정기 (Estimators Protocol)]
        LS["LeastSquaresEstimator\n(Scipy Huber/Loss 비선형)"]
        OP["OptimizeEstimator\n(Scipy minimize / L-BFGS-B)"]
        CB["CombinerEstimator\n(에르미트 2D 탐색 스플라인 합성)"]
    end

    subgraph Layer3 [3계층: 순수 수식 SSOT (models/)]
        MF["magic_formula.py (Pacejka MF)"]
        Linear["선형 초기 구간 수식"]
    end

    TC --> Layer2
    Layer2 --> Layer3
```

### 3.2. 핵심 서브모듈 역할 분담표

| 파일명 | 담당 클래스 / 함수 | 핵심 책임 및 역할 |
| :--- | :--- | :--- |
| `cf_tire.py` | `TireCurve` | 타이어 도메인 최상위 파사드 (원점 구속, 물리 파라미터 추출) |
| `least_squares_estimator.py` | `LeastSquaresEstimator` | Scipy `curve_fit` 기반 잔차 제곱합 최소화 및 이상치 방어(Huber Loss) |
| `optimize_estimator.py` | `OptimizeEstimator` | 경계 조건(Bounds) 및 구속 조건을 갖는 범용 파라미터 최적화기 |
| `combiner_estimator.py` | `CombinerEstimator` | 전반 선형 구간과 후반 곡선 구간의 최적 접합점 탐색 및 $C^1$ 연속 에르미트 스플라인 합성 |

---

## 🚀 4. 실전 워크플로우 및 종합 스니펫

```python
"""
TireCurve를 활용한 타이어 슬립-마찰계수 비선형 피팅
"""
from pathlib import Path
import numpy as np
from unoUtil.curve_fit import TireCurve

# 1. 실측 슬립율(x) 및 마찰계수(y) 데이터 준비
slip_ratio = np.linspace(0, 0.5, 100)
mu_raw = 1.1 * np.sin(np.arctan(15 * slip_ratio)) + np.random.normal(0, 0.02, 100)

# 2. TireCurve 피팅 실행 (에르미트 합성 전략 적용)
tc = TireCurve(model="magic_formula", method="combiner")
tc.fit(slip_ratio, mu_raw)

# 3. 핵심 물리 파라미터 추출
print(f"피팅 RMSE: {tc.rmse:.4f}")
print(f"최대 마찰계수 (Mu_Peak): {tc.peak_mu:.3f} (at slip={tc.peak_slip:.3f})")
print(f"초기 제동 강성 (B*C*D): {tc.initial_stiffness:.2f}")

# 4. 검증 시각화 차트 자동 저장 (Non-blocking)
fig, ax = tc.plot(
    save=Path("reports/tire_curve_fit.png"),
    close=True,
)
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

## 🔬 6. 실차 계측 데이터 MF 한계 극복 3대 전략 및 해법 C (2026-10-19 신규 확립)

### 6.1. 실차 데이터에서 표준 MF 최적화가 무너지는 3대 메커니즘
1. **데이터 제어 집중 몰림 (Data Clumping)**:
   - ABS/TCS 제어로 인해 전체 데이터의 80~90%가 피크 슬립($10 \sim 25\%$) 주변에 집중되어, 최소자승법(Least Squares)이 초반 저슬립($0 \sim 3\%$)의 탄성 강성선을 완전히 무시하고 원점에서 $y pprox 0.13g$로 붕 떠버림.
2. **초반 기울기와 피크 폭의 수학적 양립 불가**:
   - $B$를 키워 원점 기울기($B \cdot C \cdot D$)를 맞추면 $rctan(Bx)$가 $x < 0.01$에서 조기 포화($\pi/2$)되어 피크가 사각 박스처럼 왜곡됨.
3. **가속 초기 지연 (Chassis & Drivetrain Compliance)**:
   - 휠이 먼저 돌고 차체가 뒤늦게 반응하여 $x \in [0, 0.03]$ 대역에서 가속도가 0 근처에 머무는 지연 현상.

### 6.2. 3대 대안 실증 비교 분석 및 결론
| 피팅 모델 | 초기 강성 ($K$) | 피크 마찰 ($\mu_{\max}$) | 피크 슬립 ($S_{	ext{peak}}$) | 전체 오차 (RMSE) | 판정 및 특이사항 |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Baseline (기존 표준 MF)** | $0.62\,	ext{g/s}$ | $0.181\,	ext{g}$ | $0.291$ | 0.0235 | ❌ 초기 강성 붕괴, 원점에서 붕 뜸 |
| **해법 A (시그모이드 블렌딩)** | **$4.84\,	ext{g/s}$** | **$0.181\,	ext{g}$** | **$0.291$** | **0.0248** | ⚠️ 전이부($x pprox 0.05$)에서 상단 불룩함(Hump) 발생 |
| **해법 B (격자 빈 중앙값 MF)** | $0.59\,	ext{g/s}$ | $0.181\,	ext{g}$ | $0.279$ | 0.0237 | ❌ 저슬립 데이터 희소로 중앙값이 $0.14g$로 과대 왜곡 |
| **해법 C (2단계 강성 구속 MF)** | **$4.70\,	ext{g/s}$** | **$0.176\,	ext{g}$** | **$0.350 	o 0.28$** | **0.0252** | 🏆 **최우수 공식 모델**: 원점 정합 + 데이터 정중앙 관통 |

### 6.3. 해법 C (Two-Stage Constrained MF) 공식 수식
1. **1단계**: 저슬립 대역($x \le 0.035$)에서 RANSAC 강건 회귀로 원점 통과 초기 강성 $K = rac{dy}{dx}ig|_{x=0}$ 확정
2. **2단계**: MF 수식의 등식 제약 $B = rac{K}{C \cdot D}$를 주입하여 3파라미터($C, D, E$) 단일 MF 최적화:
   $$y(x) = D \cdot \sin \left( C \cdot rctan \left( rac{K}{CD} x - E \left( rac{K}{CD} x - rctan\left(rac{K}{CD} xight) ight) ight) ight)$$

### 6.4. 사용자 제안 2D 분포 분할 알고리즘 (해법 A 고도화 미래 방향)
- 2D 데이터 밀도 능선(Ridge)에서 곡률 변곡점($x_{\text{trans}}$)을 탐색하여,
- 저슬립 탄성부($x < x_{\text{trans}}$)는 $K \cdot x$ 직선, 곡선부($x \ge x_{\text{trans}}$)는 순수 고슬립 데이터만으로 MF를 독립 피팅한 뒤 블렌딩하여 불룩함(Hump)을 원천 차단하는 차세대 분할 구조.
