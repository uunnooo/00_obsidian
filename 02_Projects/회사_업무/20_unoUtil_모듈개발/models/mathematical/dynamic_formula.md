# 🏎️ dynamic_formula (2자유도 횡운동 지배 수식)

## 📌 개요
`dynamic_formula.py`는 실차 조향각과 주행 속도로부터 정상 상태 요레이트(Yaw Rate)를 추정하고, 실측 계측 신호와의 오차 제곱합(RSS) 목적 함수를 계산하는 **차량 동역학 수식 모듈**입니다.

---

## 🛠️ 주요 함수 및 인터페이스

| 함수명 | 설명 | 비고 |
| :--- | :--- | :--- |
| `calc_unit_yaw_rate(Params, X)` | 조향각과 차속 기반 이론적 정상 상태 요레이트 연산 | 구 `UnitYawRate` 호환 |
| `calc_objective_unit_yaw_rate(Params, ModelFunc, X, Y, plot, save)` | 모델 연산 결과와 실측 요레이트 간 잔차 제곱합(RSS) 산출 | 구 `ObjectiveFunc_UnitYawRate` 호환 |

---

## 💡 사용 예시 (Usage Example)

```python
import numpy as np
from unoUtil.models.mathematical import calc_unit_yaw_rate

# 입력 매트릭스 [조향각, 차속]
inputs = np.array([
    [2.0, 60.0],
    [4.0, 80.0],
    [5.0, 100.0]
])

# 스케일 파라미터 [vel_unit, angr_unit]
params = [1.0, 1.0]
yaw_rates = calc_unit_yaw_rate(params, inputs)
```
