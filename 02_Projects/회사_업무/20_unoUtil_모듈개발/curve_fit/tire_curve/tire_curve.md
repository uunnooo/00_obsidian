---
id: "tire_curve"
aliases:
  - TireCurve
  - 타이어 특성 곡선
  - 타이어 피팅 총괄 클래스
tags:
  - unoUtil
  - curve_fit
  - tire_curve
  - TireCurve
  - MagicFormula
  - SSOT
created: 2026-09-29
updated: 2026-09-29
version: v3.3
---

# 🛞 unoUtil.curve_fit.tire_curve (TireCurve) 기술 매뉴얼

> **패키지 경로**: `unoUtil.curve_fit.tire_curve.tire_curve` (`from unoUtil.curve_fit import TireCurve`)  
> **역할**: 타이어 종/횡방향 비선형 특성 곡선 피팅 총괄 클래스 (단일 진실 공급원 - SSOT)  
> **설계 패턴**: 모델 주입(Model Injection) 및 전략 패턴(Strategy Pattern)

---

## 📌 1. 개요 및 설계 철학

`TireCurve`는 실차 시험 계측 데이터(슬립율, 슬립각, 제동/구동력, 코너링포스, 횡가속도)로부터 타이어의 고유 물리적 특성치(강성, 피크 마찰, 피크 슬립)를 도출하는 **통합 커브 피팅 클래스**입니다.

과거 사내에 산재해 있던 `CurveCombiner`, `fit_mf_ax`, `estimatorMF`, `MinimizeEstimator` 등의 피팅 모듈들을 **`TireCurve` 단 하나의 인터페이스로 완전 흡수 통합**하였습니다.

```mermaid
flowchart TD
    Data["실측 계측 데이터 (slip, force/mu)"] --> TC["TireCurve(direction='longitudinal' / 'lateral')"]

    subgraph Strategies [피팅 전략 (method)]
        LS["'least_squares': Scipy 비선형 최소자승 (가중치/Huber)"]
        CC["'combiner': 다구간 스플라인 결합 (CurveCombiner 파이프라인)"]
        OPT["'optimizer': 베이지안/전역 수치 최적화"]
        AX["'ax': 종가속도 특화 피팅"]
    end

    TC --> Strategies
    Strategies --> Result["통합 결과 도출: stiffness, peak_value, peak_slip, plot()"]
```

---

## 🚀 2. 주요 사용법

### 1) 기본 최소자승 피팅 (`least_squares`)
```python
import numpy as np
from unoUtil.curve_fit import TireCurve

slip = np.linspace(0.0, 0.3, 100)
force = 1.1 * np.sin(1.3 * np.arctan(10.0 * slip))

tire = TireCurve(direction='longitudinal', method='least_squares')
tire.fit(slip, force)

print(f"제동 강성: {tire.stiffness:.2f}")
print(f"피크 마찰: {tire.peak_value:.2f}")
print(f"피크 슬립: {tire.peak_slip:.3f}")
tire.plot()
```

### 2) 다구간 스플라인 결합 피팅 (`combiner`)
```python
# 별도 모듈을 찾을 필요 없이 method만 지정하면 CurveCombiner 파이프라인 자동 구동!
tire = TireCurve(method='combiner')
tire.fit(slip, force)
```

---

## 📊 3. 주요 속성 및 메서드

| 프로퍼티 / 메서드 | 타입 | 설명 |
| :--- | :--- | :--- |
| `stiffness` | `float` | 제동/코너링 초기 강성 ($B \cdot C \cdot D$) |
| `peak_value` | `float` | 최대 마찰계수 또는 최대 발생 힘 ($D$) |
| `peak_slip` | `float` | 피크 마찰 발생 슬립 위치 ($\kappa_{peak}$ 또는 $\alpha_{peak}$) |
| `fitted_params` | `np.ndarray` | 최적화 추정 파라미터 `[B, C, D, E, Sh, Sv]` |
| `predict(x)` | `method` | 임의의 슬립 입력에 대한 모델 예측값 연산 |
| `plot(save=None)` | `method` | 산점도 및 적합 곡선 비차단 시각화 |
