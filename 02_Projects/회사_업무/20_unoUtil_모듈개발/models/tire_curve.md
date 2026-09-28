# 🛞 `TireCurve` — 타이어 특성 곡선 통합 모델링 및 비선형 피팅 클래스

## 📌 개요
`TireCurve`는 타이어의 종방향(제동/구동력, $F_x$) 및 횡방향(코너링포스, $F_y$) 특성 곡선을 해석하고 피팅하는 **단일 진실 공급원(SSOT) 총괄 클래스**입니다.  
소프트웨어 공학의 **전략 패턴(Strategy Pattern) 및 의존성 주입(Dependency Injection)**을 기반으로 설계되어, 특정 수식이나 알고리즘에 종속되지 않고 임의의 타이어 수학 모델과 최적화 전략을 결합하여 분석할 수 있습니다.

---

## 🏛️ 아키텍처 및 전략 패턴

```mermaid
flowchart TD
    subgraph Math_Registry [공학 지배 방정식 (Models)]
        MF["magic_formula (기본 Pacejka MF)"]
        FIALA["fiala_model (확장 가능)"]
        CUSTOM["사용자 정의 함수 (x, *params)"]
    end

    subgraph TireCurve_Engine [TireCurve 통합 엔진]
        TC["TireCurve(model, direction, method, params, bounds)"]
    end

    subgraph Fitting_Strategies [최적화 알고리즘 (Methods)]
        LS["least_squares (Scipy 최소자승법, 가중치/Huber loss)"]
        CB["combiner (다구간 직선 결합 + Hermite 스플라인)"]
        OPT["optimizer / bayesian (전역 파라미터 탐색)"]
        AX["ax (가속도 L-BFGS-B 특화)"]
    end

    Math_Registry --> TC
    Fitting_Strategies --> TC
    TC --> Result["TireCurve 분석 결과 (stiffness, peak_value, peak_slip, plot)"]
```

---

## ⚙️ 주요 파라미터 (`__init__`)

| 파라미터 | 타입 | 기본값 | 설명 |
| :--- | :--- | :--- | :--- |
| `model` | `str \| Callable` | `'magic_formula'` | 적용할 수학 모델 ('magic_formula' 또는 사용자 함수 `f(x, *params)`) |
| `direction` | `str` | `'longitudinal'` | 모델링 방향 (`'longitudinal'`: 종방향 제동/구동, `'lateral'`: 횡방향 코너링) |
| `method` | `str` | `'least_squares'` | 기본 피팅 전략 (`'least_squares'`, `'combiner'`, `'optimizer'`, `'ax'`) |
| `params` | `List[float] \| None` | `None` | 초기 파라미터. `None`이면 모델 레지스트리의 최적 기본값 자동 로드 |
| `bounds` | `Tuple \| None` | `None` | 파라미터 탐색 경계 `(lower_bounds, upper_bounds)` |
| `name` | `str` | `'TireCurve'` | 인스턴스 식별 명칭 |

---

## 🚀 빠른 시작 (Quick Start)

### 1. 종방향 제동 데이터 피팅 (Pacejka MF)
```python
from unoUtil.models import TireCurve

# 인스턴스 생성 및 피팅
tire = TireCurve(direction='longitudinal', method='least_squares')
tire.fit(slip_ratio, braking_force)

# 물리 특성치 추출
print(f"제동 강성 (C_kappa): {tire.stiffness:.2f} N/-")
print(f"최대 마찰계수/피크 힘: {tire.peak_value:.2f}")
print(f"피크 발생 슬립율: {tire.peak_slip:.3f}")

# 예측 및 시각화
predicted_force = tire.predict(new_slip_ratios)
tire.plot(save="braking_curve.png")
```

### 2. 다구간 직선 결합 전략 (CurveCombiner 파이프라인)
```python
# 초기 슬립 선형 구간과 MF 곡선을 Hermite/Clothoid로 결합
tire_cb = TireCurve(method='combiner')
tire_cb.fit(slip_ratio, braking_force)
tire_cb.plot()
```

### 3. 사용자 정의 수학 모델 주입 (확장성)
```python
import numpy as np
from unoUtil.models import TireCurve

# 사용자 정의 3차 다항식 모델
def my_poly_model(x, a, b, c):
    return a * x**3 + b * x + c

tire_custom = TireCurve(model=my_poly_model, params=[1.0, 5.0, 0.0])
tire_custom.fit(slip_ratio, force)
```

---

## 🛡️ 물리 특성치 프로퍼티 (Domain Properties)

* **`tire.stiffness`**: 원점 부근의 타이어 강성 ($B \cdot C \cdot D$)
  * 종방향: 제동/구동 강성 ($C_\kappa$)
  * 횡방향: 코너링 강성 ($C_\alpha$)
* **`tire.peak_value`**: 최대 피크 힘 또는 최대 마찰계수 ($D$)
* **`tire.peak_slip`**: 최대력이 발생하는 슬립율 또는 슬립각 좌표
* **`tire.result`**: 최적화 엔진의 상세 수렴 결과 (cost, rmse, success 등)
