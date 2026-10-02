# 📘 동일 스펙 독립 물리 기울기 보정 모듈 (`slope_model.py`)

## 1. 개요 및 목적
* **모듈명**: `unoUtil.snow_condition.slope_model`
* **핵심 클래스**: `SnowSlopeModel`, `SnowSlopePlotter`
* **역할**: 
  - [방법 2] 동일 스펙(`SPEC_NO`)의 반복 시험 데이터로부터 기온($k_{\text{air}}$) 및 절대습도($k_{\text{ah}}$)의 **개별 독립 물리 기울기**를 통계적으로 산출함.
  - 다중회귀 다중공선성 왜곡을 원천 배제한 1변수 독립 OLS 중심화 공식을 적용함.
  - 사전에 정의된 표준 기준 환경($-8.0^\circ\text{C}, 1.5\text{ g/m}^3$)으로 전 데이터셋의 제동거리를 일괄 정규화(보정)함.
  - No Redundant Prefix Law(메서드 접두사 중복 방지 원칙)에 따라 `plot_` 접두사를 전면 배제한 전문 플로터(`SnowSlopePlotter`)를 컴포지션으로 합성 제공함.

---

## 2. 수학적 및 물리적 원리

### 1) 동일 스펙 내 중심화 (Within-Spec Centering)
동일 스펙 $s$ 내의 평균 환경 및 제동거리를 차감하여 순수 환경 편차를 분리:
$$T'_{i} = T_i - \bar{T}_s, \quad AH'_{i} = AH_i - \overline{AH}_s, \quad y'_i = y_i - \bar{y}_s$$

### 2) 독립 물리 기울기 산출 (Independent OLS Slopes)
$$k_{\text{air}} = \frac{\sum y'_i T'_i}{\sum {T'_i}^2}, \quad k_{\text{ah}} = \frac{\sum y'_i AH'_i}{\sum {AH'_i}^2}$$

### 3) 기준 환경 일괄 보정 (Standard Reference Normalization)
표준 기준 환경($T_{\text{ref}} = -8.0^\circ\text{C}$, $AH_{\text{ref}} = 1.5\text{ g/m}^3$) 대비:
$$y_{\text{corr}} = y - \left[ k_{\text{air}} (T - T_{\text{ref}}) + k_{\text{ah}} (AH - AH_{\text{ref}}) \right]$$

---

## 3. 클래스 및 메서드 명세

### `SnowSlopeModel`
```python
class SnowSlopeModel:
    def __init__(
        self,
        spec_col: str = 'infor_SPEC_NO',
        temp_col: str = 'cd_test_temp',
        ah_col: str = 'cd_test_ah',
        dist_col: str = 'char_brk_dist',
        ref_temp: float = -8.0,
        ref_ah: float = 1.5,
        min_spec_count: int = 2
    )
```

* `calc_independent_slopes(data: pd.DataFrame) -> Dict[str, float]`:
  동일 스펙 데이터셋으로부터 독립 물리 기울기($k_{\text{air}}, k_{\text{ah}}$) 및 유의확률($p$-value)을 산출함.
* `predict_delta(temp, ah) -> Union[float, np.ndarray]`:
  기준 환경 대비 제동거리 오프셋 추정.
* `correct_dataframe(data: pd.DataFrame, out_col: Optional[str] = None) -> pd.DataFrame`:
  기준 환경으로 전 데이터셋 일괄 보정.
* `self.plot`: 전문 플로터 `SnowSlopePlotter` 합성.

### `SnowSlopePlotter` (No Redundant Prefix Law 준수)
* `slope_scatter(save=False, close=True, **kwargs)`:
  동일 스펙 중심화 편차 vs 제동거리 편차 산점도 및 독립 회귀 직선 2분할 렌더링.
* `correction_map(t_range=(-18, 0), ah_range=(0.5, 3.5), save=False, close=True, **kwargs)`:
  기준 환경($-8^\circ\text{C}, 1.5\text{ g/m}^3$) 대비 2D 등고선 보정 맵 렌더링.
* `variance_reduction(data, top_n=5, save=False, close=True, **kwargs)`:
  동일 스펙 상위 N개에 대해 보정 전 vs 보정 후 제동거리 분산 감소 박스플롯 렌더링.

---

## 4. 사용 예시 (Usage Example)

```python
import pandas as pd
from unoUtil.snow_condition import SnowSlopeModel

# 1. 모델 인스턴스 생성
model_m2 = SnowSlopeModel(
    spec_col='infor_SPEC_NO',
    temp_col='cd_test_temp',
    ah_col='cd_test_ah',
    dist_col='char_brk_dist',
    ref_temp=-8.0,
    ref_ah=1.5
)

# 2. 동일 스펙 독립 기울기 산출
slopes = model_m2.calc_independent_slopes(df_clean)
print(f"k_air: {slopes['k_air']:+.4f} m/℃, k_ah: {slopes['k_ah']:+.4f} m/(g/m³)")

# 3. 기준 환경 일괄 보정
df_corrected = model_m2.correct_dataframe(df_clean, out_col='char_brk_dist_corr_m2')

# 4. 전문 시각화 호출 (plot_ 접두사 없음)
fig_scatter, _ = model_m2.plot.slope_scatter(save="1_Method2_Slope_Scatter.png")
fig_map, _ = model_m2.plot.correction_map(save="3_Method2_Contour_Map.png")
fig_var, _ = model_m2.plot.variance_reduction(df_corrected, save="4_Method2_Variance.png")
```
