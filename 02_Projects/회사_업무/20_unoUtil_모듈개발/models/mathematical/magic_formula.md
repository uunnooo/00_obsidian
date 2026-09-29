# 📐 magic_formula (Pacejka Magic Formula 지배 방정식 SSOT)

## 📌 개요
`magic_formula.py`는 실차 타이어 및 횡/종방향 차량 동역학 시뮬레이션의 근간이 되는 **Pacejka Magic Formula(매직 포뮬러)** 지배 수식의 **단일 진실 공급원(SSOT, Single Source of Truth)** 모듈입니다.

기존에 `ai`, `signal_process/curve_fit`, `vehicle/hndl_test` 등 여러 도메인에 흩어져 있던 동일 수식 연산 코드를 단일 코어 함수(`calc_magic_formula`)로 완전 통합하여, 수식 모델링과 파라미터 규격의 일관성을 100% 보장합니다.

---

## ⚙️ 수식 원리 및 물리적 의미

$$y(x) = D \cdot \sin\left(C \cdot \arctan\left(B \cdot x_p - E \cdot (B \cdot x_p - \arctan(B \cdot x_p))\right)\right) + S_v$$
$$(단, x_p = x + S_h)$$

* **$x$ (Slip Input)**: 입력 슬립 변수 (제동 시 Slip Ratio $0 \sim 1$, 선회 시 Slip Angle $\text{rad}$ 또는 $\text{deg}$).
* **$B$ (Stiffness Factor, 강성 계수)**: 원점 부근의 타이어 종/횡력 강성 기울기(Cornering/Braking Stiffness)를 결정.
* **$C$ (Shape Factor, 형상 계수)**: 비선형 곡선의 형태와 점근 거동을 제어 (일반적으로 $1.0 \sim 1.8$).
* **$D$ (Peak Factor, 피크 계수)**: 노면 최대 마찰 한계 한도를 결정 ($D = \mu \cdot F_z$).
* **$E$ (Curvature Factor, 곡률 계수)**: 피크 도달 후 하강 곡률 및 비선형성을 제어 ($E \le 1.0$).
* **$S_h, S_v$ (Shift Factors, 오프셋)**: 플라이스티어, 캠버 스러스트 등으로 인한 원점 편차 보정 계수.

---

## 🛠️ 주요 함수 및 인터페이스

| 함수명 | 설명 | 비고 |
| :--- | :--- | :--- |
| `calc_magic_formula(x, B, C, D, E, Sh, Sv)` | 6-파라미터 표준 매직 포뮬러 코어 벡터 연산 | SSOT 코어 엔진 |
| `calc_tire_magic_formula(Params, X, plot, save)` | `[B, C, D, E]` 파라미터 배열 기반 연산 및 비차단 차트 시각화 | 구 `TireMagicFormula` 호환 |
| `magic_formula(x, B, C, D, E, Sh, Sv)` | 기존 커브 결합기(CurveCombiner) 인터페이스 호환 래퍼 | 100% 하위 호환 |
| `magic_formula_mu(x, Fz, B, C, mu, E, Sh, Sv)` | 수직하중($F_z$)과 마찰계수($\mu$) 기반 $D = \mu F_z$ 피크 연산 래퍼 | 하중 의존성 모델 |
| `calculate_fx(Bx, Ex, Dx, Cx, x)` | 파라미터 개별 지정형 제동력/감속도 연산 래퍼 | 구 `calculate_Fx` 호환 |

---

## 💡 사용 예시 (Usage Example)

```python
import numpy as np
from unoUtil.models.mathematical import calc_magic_formula, calc_tire_magic_formula

# 1. 단일 코어 수식 직접 연산 (슬립율 0 ~ 0.3)
slip = np.linspace(0.0, 0.3, 100)
force = calc_magic_formula(slip, B=10.0, C=1.3, D=1.1, E=0.1)

# 2. 파라미터 리스트 및 플롯 시각화
params = [10.0, 1.3, 1.1, 0.1]
force_arr = calc_tire_magic_formula(params, slip, plot=False)
```
