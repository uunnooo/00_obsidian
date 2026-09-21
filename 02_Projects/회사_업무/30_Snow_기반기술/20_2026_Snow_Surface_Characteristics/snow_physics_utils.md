# ❄️ snow_physics_utils.py 로컬 개발 매뉴얼

이 모듈은 스노우 노면 물리, 기상 역학 및 타이어 접지압 기반의 다양한 물성치를 계산하기 위한 기상/물리 전용 유틸리티 클래스/함수 집합입니다.

---

## 🏛️ 1. API 명세 및 상세 설계

### 1.1 `calc_saturation_vapor_pressure(temp_c)`
온도($^\circ\text{C}$)에 따른 물(Water)과 얼음(Ice) 표면에서의 포화수증기압(hPa)을 Sonntag 1990 근사식을 통해 산출합니다.
* **인자**:
  * `temp_c (Union[float, np.ndarray, pd.Series])`: 외기 또는 노면 온도 ($^\circ\text{C}$)
* **반환값**:
  * `Tuple`: (물 표면 포화수증기압, 얼음 표면 포화수증기압)

### 1.2 `calc_supersaturation(temp_c, rh_water)`
온도와 물 기준 상대습도로부터 실제 수증기압, 절대습도(AH), 얼음 표면 기준 상대습도 및 과잉 절대습도(AH_Excess, 과포화 수분량 $g/m^3$)를 계산합니다.
* **인자**:
  * `temp_c (Union[float, np.ndarray, pd.Series])`: 온도 ($^\circ\text{C}$)
  * `rh_water (Union[float, np.ndarray, pd.Series])`: 상대습도 (%, 0~100)
* **반환값**:
  * `pd.DataFrame`: 기상 물리 분석용 데이터프레임

### 1.3 `calc_contact_pressure(wheel_load_kg, contact_area_m2)`
타이어의 1륜당 수직 하중과 접지 면적을 바탕으로 가해지는 물리 접지압(kPa)을 산출합니다.
* **인자**:
  * `wheel_load_kg (float)`: 수직 하중 (kg, 기본값: 400.0)
  * `contact_area_m2 (float)`: 접지 면적 ($m^2$, 기본값: 0.03)
* **반환값**:
  * `float`: 타이어 접지압 (kPa)

### 1.4 `estimate_snow_density(initial_height_mm, penetrated_height_mm, wheel_load_kg, contact_area_m2)`
자연 적설 깊이와 타이어 압설 후 침하 두께 간의 질량 보존 법칙($\rho_1 \cdot h_1 = \rho_2 \cdot h_2$)을 이용하여, 눈의 압축률과 초기 눈 밀도($kg/m^3$)를 역추정합니다.
* **인자**:
  * `initial_height_mm (float)`: 압설 전 자연 적설 깊이 (mm)
  * `penetrated_height_mm (float)`: 압설 후 잔여 두께 또는 순수 침하 깊이 (mm)
* **반환값**:
  * `Dict[str, float]`: 접지압, 압축률, 역추정 초기/압축 밀도를 포함하는 사전

---

## 💻 2. 실무 활용 예제

```python
import numpy as np
from Snow_braking_relate_condition.snow_physics_utils import calc_supersaturation, estimate_snow_density

# 1. 기상 데이터로부터 과포화 습도 계산
temps = np.array([-10.0, -5.0])
rhs = np.array([95.0, 90.0])
df_weather_physics = calc_supersaturation(temps, rhs)
print(df_weather_physics[['WB-AH', 'WB-AH_Excess']])

# 2. 실차 시험 노면 눌림량으로부터 눈 밀도 추정
density_metrics = estimate_snow_density(initial_height_mm=8.7, penetrated_height_mm=2.5)
print(f"추정 초기 눈 밀도: {density_metrics['est_initial_density_kg_m3']} kg/m³")
```
