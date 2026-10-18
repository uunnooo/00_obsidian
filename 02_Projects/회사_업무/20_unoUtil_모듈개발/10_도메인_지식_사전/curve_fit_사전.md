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
