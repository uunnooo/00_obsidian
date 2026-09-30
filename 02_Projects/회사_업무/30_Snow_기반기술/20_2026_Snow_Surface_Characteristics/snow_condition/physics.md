# ❄️ snow_condition.physics 기술 매뉴얼

이 문서는 스노우 노면 환경의 대기 기상 역학, 포화/과포화 수증기압, 타이어 1륜 접지압, 그리고 설면 압축률 기반 밀도 역추정 유틸리티 함수의 명세 및 사용법을 정의합니다.

---

## 1. 📌 핵심 개요

눈길(Snow) 노면의 마찰 특성은 외기 온도뿐만 아니라 얼음 표면 대비 **수증기 과포화도(Supersaturation)** 및 타이어 하중에 의해 눈이 다져지는 **압축률(Compaction Ratio)**에 의해 결정적인 영향을 받습니다. 본 모듈은 Sonntag(1990) 공식을 적용하여 노면 물리 해석의 기초 수치들을 벡터 연산으로 고속 제공합니다.

---

## 2. 🧮 핵심 물리 공식 및 API

### 2.1 `calc_saturation_vapor_pressure(temp_c)`
* **공식**:
  $$e_{\text{sat, water}} = 6.112 \times \exp\left(\frac{17.62 \cdot T}{243.12 + T}\right) \quad (\text{hPa})$$
  $$e_{\text{sat, ice}} = 6.112 \times \exp\left(\frac{22.46 \cdot T}{272.62 + T}\right) \quad (\text{hPa})$$
* **반환값**: `Tuple[e_sat_water, e_sat_ice]`

### 2.2 `calc_supersaturation(temp_c, rh_water, **kwargs)`
* **역할**: 대기 온도와 물 기준 상대습도로부터 실제 수증기압($VP$), 절대습도($AH$), 얼음 기준 상대습도($RH_{\text{ice}}$), 과잉 절대습도($AH_{\text{excess}}$) 산출.
* **반환값**: `pd.DataFrame` (`WB-AH`, `WB-AH_Excess` 등)

### 2.3 `calc_contact_pressure(wheel_load_kg=400.0, contact_area_m2=0.03)`
* **역할**: 타이어 1륜당 수직 하중과 접지면적으로부터 접지압(kPa) 계산.

### 2.4 `estimate_snow_density(initial_height_mm, penetrated_height_mm, wheel_load_kg=400.0, contact_area_m2=0.03)`
* **역할**: 차량 주행 전/후 적설 깊이 변화로부터 압축비($h_1 / h_2$) 및 눈의 초기 밀도/압설 후 밀도를 역추정.

---

## 3. 💡 실무 사용 예제

```python
from snow_condition.physics import calc_supersaturation, estimate_snow_density

# 1. 영하 10도, 상대습도 95% 조건의 절대습도 및 과포화도 계산
df_sat = calc_supersaturation(-10.0, 95.0)
print(f"절대습도: {df_sat['WB-AH'].iloc[0]:.3f} g/m³")
print(f"과잉수분량: {df_sat['WB-AH_Excess'].iloc[0]:.3f} g/m³")

# 2. 적설 8.7mm에서 타이어 통과 후 2.5mm로 압설된 경우 밀도 역추정
snow_info = estimate_snow_density(8.7, 2.5, wheel_load_kg=400.0)
print(f"압축률: {snow_info['compaction_ratio']}배")
print(f"추정 압설 밀도: {snow_info['est_compacted_density_kg_m3']} kg/m³")
```
