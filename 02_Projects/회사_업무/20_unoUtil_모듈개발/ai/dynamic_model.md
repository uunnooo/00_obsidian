---
id: "dynamic_model_20260920"
title: "dynamic_model (차량 요레이트 및 타이어 비선형 동역학 수식 모델러) 상세 매뉴얼"
type: resource
category_main: 회사_업무
category_sub: 개발매뉴얼
date: 2026-09-20
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - 매뉴얼
  - AI
  - 동역학
  - 타이어
  - 요레이트
project_link: "[[unoUtil]]"
---

# 🌦️ dynamic_model (차량 요레이트 및 타이어 비선형 동역학 수식 모델러) 상세 매뉴얼

> [!ABSTRACT] 📌 개요
> 타이어 비선형 슬립 성능을 예측하는 Pacejka 수식 모델과, 전진 속도 및 조향 조건에 따른 이론적 정상 상태 요레이트(Yaw Rate) 물리 방정식을 통합 전개하는 정밀 공학 동역학 지배 수식 시뮬레이션 모듈입니다.
> 
> * **상위 대시보드**: [[00_unoUtil_모듈개발_대시보드]]

---

## 1. ⚙️ 동역학 물리 방정식 명세

### 1.1. Pacejka 타이어 제동력 공식
$$F_x = D_x \cdot \sin\left(C_x \cdot \arctan\left(B_x \cdot x - E_x \cdot \left(B_x \cdot x - \arctan(B_x \cdot x)\right)\right)\right)$$
- 입력 슬립 비율 $x$에 대해 피크 마찰 계수 $D_x$, 강성 계수 $B_x$, 형상 $C_x$ 및 곡률 $E_x$ 상수를 활용해 물리 제동 성능 곡선을 산출합니다.

### 1.2. 정상 상태 요레이트 공식 (Unit Yaw Rate Model)
$$r_{ss} = \left(\frac{\delta}{V \cdot v_{unit}}\right) \cdot a_{unit}$$
- 조향각 $\delta$(Steering Angle)와 차속 $V$(Velocity)의 조합으로부터 가변 단위 보정인자 $v_{unit}$, $a_{unit}$를 곱하여 수치 요레이트($deg/s$ 또는 $rad/s$)를 계산합니다.
- 차속이 극소값($1.0$ kph 이하)으로 유입될 시 분모가 $0$이 되어 발산하는 현상을 차단하기 위해 **이상값 제로화 방어 마스크 수식**이 하드웨어 수준으로 기입되어 있습니다.

---

## 2. ⚙️ 주요 API 및 메서드 명세

### 2.1. `TireMagicFormula(Params, X, plot=False, ...)`
* **기능**: 타이어 마찰 성능 Pacejka 곡선을 연산합니다. 입력 `X`는 스칼라, 넘파이 어레이, 판다스 시리즈 형태를 가리지 않고 유연하게 수용하여 보정 연산합니다.
* **하위 호환 별칭**: `tire_magic_formula`

### 2.2. `UnitYawRate(Params, X)`
* **기능**: 조향각과 차속 매트릭스로부터 유도 요레이트 궤적을 연산합니다.
* **하위 호환 별칭**: `unit_yaw_rate`

### 2.3. `ObjectiveFunc_UnitYawRate(Params, ModelFunc, X, Y, plot=False, ...)`
* **기능**: 추정 시뮬레이션 요레이트와 실주행 계측 자이로 요레이트 신호 `Y` 간의 RSS 누적 오차를 구득하고 렌더링 그래프를 다형성 출력(`save=True` 연동)합니다.

---

## 💻 3. 호출 예제 (Usage Example)

```python
import numpy as np
import pandas as pd
from unoUtil.ai.dynamic_model import TireMagicFormula, UnitYawRate, ObjectiveFunc_UnitYawRate

# 1. 타이어 비선형 마찰 포화 특성 스칼라 연산
slip_scalar = 0.08
force_scalar = TireMagicFormula(Params=[12.0, 1.6, 1.1, 0.1], X=slip_scalar)
print(f"단일 슬립 0.08에서의 제동 마찰 지수: {force_scalar[0]:.4f}")

# 2. 3행의 차량 거동 매트릭스 [Steering, Velocity] 준비 및 요레이트 연산
# 1행은 0.5kph 극저속 정지 상태 (0나누기 방어 마스크 활성화)
drive_matrix = np.array([
    [1.5, 0.5],
    [2.0, 60.0],
    [3.0, 100.0]
])
estimated_yaw_rates = UnitYawRate(Params=[1.0, 1.0], X=drive_matrix)
print(f"계산 완료된 요레이트 시뮬레이션 결과: {estimated_yaw_rates}")

# 3. 실측 요레이트와의 오차 RSS 평가 및 overlay 차트 디폴트 저장
Y_measured = np.array([0.0, 0.033, 0.030])
rss_error = ObjectiveFunc_UnitYawRate(
    Params=[1.0, 1.0],
    ModelFunc=UnitYawRate,
    X=drive_matrix,
    Y=Y_measured,
    plot=True,
    save=True,  # 디폴트 폴더에 자동 차트 저장
    close=True
)
print(f"요레이트 최종 RSS 연산 오차합: {rss_error:.6f}")
```

---

## 4. 📝 이중 동기화 프로토콜 준수사항
- 이 매뉴얼 파일(`dynamic_model.md`)은 동일 로컬 디렉터리(`unoUtil/ai/`) 내에 1:1 대응하여 보관되며, 최종 작업 완료 선언 시 옵시디언 볼트로 일괄 배치 동기화 처리됩니다.
