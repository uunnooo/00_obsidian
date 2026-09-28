# 🚲 `bicycle_model` — 차량 2자유도 자전거 모델 (Bicycle Model)

## 📌 개요
`bicycle_model`은 차량동역학(Vehicle Dynamics) 분야의 국제 표준 규격인 **2자유도 자전거 모델(2-DoF Bicycle Model 또는 Single-Track Model)**에 기반하여, 조향각(Steering Angle)과 차속(Velocity)으로부터 정상 상태 요레이트(Steady-state Yaw Rate)를 해석하고 목적함수 RSS를 연산하는 모듈입니다.

---

## 📐 지배 방정식 (Governing Equations)

저속 및 선형 선회 영역에서 차량의 정상 상태 요레이트 $r$은 아커만 기하 및 차량 제원에 따라 다음과 같이 수식화됩니다:

$$r = \left(\frac{\delta}{V \cdot \text{vel\_unit}}\right) \cdot \text{angr\_unit}$$

여기서:
* $\delta$: 전륜 조향각 (Steering Angle)
* $V$: 전진 차속 (Vehicle Velocity, $V > 1.0\text{ m/s}$ 이상치 마스크 적용)
* $\text{vel\_unit}, \text{angr\_unit}$: 단위계 환산 및 교정 스케일 계수

---

## 🛠️ 주요 함수 및 인터페이스

### 1. `calc_bicycle_yaw_rate(Params, X)`
조향각과 속도 행렬로부터 이론적 요레이트를 계산합니다.

* **인자**:
  * `Params` (`List[float]`): 환산 계수 `[vel_unit, angr_unit]`
  * `X` (`np.ndarray`): `[N, 2]` 행렬 (1열: 조향각, 2열: 차속)
* **반환**: `np.ndarray` (정상 상태 요레이트 배열)

### 2. `calc_objective_bicycle_yaw_rate(Params, ModelFunc, X, Y, plot=False, save=None)`
실측 계측 요레이트 $Y$와의 오차 제곱합(RSS) 목적 함수를 계산합니다.

### 3. `BicycleModel` (클래스)
자전거 모델을 객체지향적으로 캡슐화한 클래스입니다.
* `model = BicycleModel(vel_unit=1.0, angr_unit=1.0)`
* `model.predict(steering, velocity)`
* `model.evaluate(steering, velocity, measured_yaw)`

---

## 🛡️ 100% 무중단 하위 호환성 별칭
* `calc_unit_yaw_rate` $\equiv$ `calc_bicycle_yaw_rate`
* `UnitYawRate` $\equiv$ `calc_bicycle_yaw_rate`
* `calc_objective_unit_yaw_rate` $\equiv$ `calc_objective_bicycle_yaw_rate`
* `ObjectiveFunc_UnitYawRate` $\equiv$ `calc_objective_bicycle_yaw_rate`
