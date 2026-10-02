# 📘 스노우 노면 특성 데이터 선처리 모듈 (`preprocessor.py`)

## 1. 개요 및 목적
* **모듈명**: `unoUtil.snow_condition.preprocessor`
* **역할**: 스노우 제동 및 노면 평가 데이터셋을 기온 구간(정상 기온 vs 이상 기온), 강설 여부(눈 제외 vs 눈 포함), 타이어 카테고리별 시나리오에 따라 사전에 정제/필터링하는 전용 선처리 모듈.
* **설계 원칙**: 
  - 보정 모델(`SnowCorrectionModel`, `SnowSlopeModel`) 내부의 하드코딩 필터링을 완전히 배제하고, 단일 책임 원칙(SRP)에 따라 데이터 선처리를 완벽히 분리함.
  - 모델의 범용성(Generalizability)을 극대화함.

---

## 2. 주요 함수 명세

### `filter_snow_conditions`
```python
def filter_snow_conditions(
    data: pd.DataFrame,
    temp_col: str = 'cd_test_temp',
    temp_range: Optional[Tuple[float, float]] = (-25.0, 0.0),
    temp_mode: str = 'in_range',
    weather_col: Optional[str] = 'SNOW_WEATHER',
    snowfall_mode: str = 'all',
    category_col: Optional[str] = 'TIRE_CATEGORY',
    tire_category: str = 'All',
    dropna_cols: Optional[List[str]] = None,
    copy: bool = True
) -> pd.DataFrame:
```

#### 파라미터 설명
* `data` (`pd.DataFrame`): 원본 스노우 평가 데이터프레임.
* `temp_col` (`str`): 기온 컬럼명 (기본값: `'cd_test_temp'`).
* `temp_range` (`Optional[Tuple[float, float]]`): 기온 정상 범위 기준 (기본값: `(-25.0, 0.0)`).
* `temp_mode` (`str`):
  * `'in_range'`: $-25.0^\circ\text{C} \le T \le 0.0^\circ\text{C}$ (정상 기온 범위)
  * `'out_of_range'`: $T < -25.0^\circ\text{C}$ 또는 $T > 0.0^\circ\text{C}$ (이상 기온 영역)
  * `'all'`: 기온 필터 미적용
* `weather_col` (`Optional[str]`): 강설/기상 컬럼명 (기본값: `'SNOW_WEATHER'`).
* `snowfall_mode` (`str`):
  * `'all'`: 전체 기상 조건 포함
  * `'exclude_snow'`: 눈이 내리는 시험 제외 (맑음/흐림 등만 포함)
  * `'snow_only'`: 눈이 내리는 시험만 포함
* `category_col` (`Optional[str]`): 타이어 카테고리 컬럼명 (기본값: `'TIRE_CATEGORY'`).
* `tire_category` (`str`): 타이어 카테고리 필터링 (`'All'`, `'Studless'`, `'Stud'`, `'All Weather'`).
* `dropna_cols` (`Optional[List[str]]`): 필수 결측치(NaN) 제거 컬럼 리스트.
* `copy` (`bool`): Deepcopy 여부 (기본값: `True`).

---

## 3. 사용 예시 (Usage Example)

```python
import pandas as pd
from unoUtil.snow_condition import filter_snow_conditions

df_raw = pd.read_pickle("raw_snow_data.pkl")

# 시나리오 1: 정상 기온(-25~0℃) + 눈 오는 날 제외 + Studless 타이어
df_clean = filter_snow_conditions(
    df_raw,
    temp_range=(-25.0, 0.0),
    temp_mode='in_range',
    snowfall_mode='exclude_snow',
    tire_category='Studless',
    dropna_cols=['char_brk_dist', 'cd_test_temp', 'cd_test_ah']
)

# 시나리오 2: 이상 기온(T > 0℃ 또는 T < -25℃) + 전체 날씨
df_outliers = filter_snow_conditions(
    df_raw,
    temp_range=(-25.0, 0.0),
    temp_mode='out_of_range',
    snowfall_mode='all'
)
```
