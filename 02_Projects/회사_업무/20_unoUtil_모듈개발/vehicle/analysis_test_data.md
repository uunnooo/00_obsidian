# 🧭 AnalysisTestData 시험 데이터 상대 성능 지수 산출 엔진 매뉴얼 (analysis_test_data.md)

## 📌 1. 개요 및 목적 (Overview)
`analysis_test_data` 모듈은 실차 주행 시험(제동, 소음, 승차감 등) 진행 중 노면 온도 및 환경 변화로 인해 발생하는 성능 드리프트를 보정하기 위해, **컨트롤 타이어(Control Tire)의 성능 변화를 선형 보간(Linear Interpolation)**하고 시험 타이어(Test Tire)의 **상대 성능 지수(Index, %)**를 산출하는 전문 분석 엔진입니다. 또한 다회차 시험 데이터를 다차원 피벗하여 지표 중심의 비교표와 요약 통계표를 자동 빌드합니다.

v2 아키텍처에서는 기존의 `print()` 기반 로깅을 전면 퇴출하고 **`LOGGER("AnalysisTestData")`** 계층형 로거를 도입하였으며, 8대 표준 동사(`calc_performance`, `calc_compare`) 체계로 정비되었습니다.

---

## 🛠️ 2. 핵심 함수 및 API 명세 (API Specifications)

| 함수명 (8대 표준 동사) | v1 오리지널 레거시 별칭 | 주요 인자 규격 (헝가리안 배제) | 반환값 | 알고리즘 특성 |
| :--- | :--- | :--- | :---: | :--- |
| **`calc_performance`** | `make_performance_df` | `data: pd.DataFrame, target_col: str, name_col: str, test_seq='Datetime', refer_kwd='c'` | `pd.DataFrame` | 컨트롤 타이어 간 성능 변화를 선형 보간하여 시점별 기준값(`adj_`) 산출 및 상대 성능 지수(`per_`, %) 계산 |
| **`calc_compare`** | `make_compare_df` | `dfs: List[pd.DataFrame], comp_cols: List[str], sel_cols: List[str], del_cols=[]` | `Tuple[compare_df, stat_df]` | 가로 열로 비교 기준(회차, 타이어셋)을 언스택(Unstack)하고 세로 행으로 지표(Metric)를 정렬한 다차원 비교표 및 통계표 생성 |

---

## 🎯 3. v1 레거시 하위 호환성 단일 기준 원칙 (Single Baseline Law)
* **v1 오리지널 레거시 호환 100% 보장**:
  - `make_performance_df`, `make_compare_df` 별칭을 모듈 레벨에서 100% 유지합니다.
  - 구버전 헝가리안 인자(`df_input`, `str_result_col`, `str_name_col`, `str_test_seq`, `str_refer_kwd`, `list_dfs`, `list_comp_cols`, `list_sel_cols`, `list_del_cols`)는 `**kwargs` 흡수 패턴을 통해 신규 표준 인자로 무중단 자동 변환됩니다.
* **과도기적 미완성 코드의 레거시 취급 배제**:
  - v2 개발 과정 중의 임시 파라미터나 불필요한 별칭은 남기지 않고 단일 표준 형태로 정합되었습니다.

---

## 💻 4. 실무 활용 3대 다변화 시나리오 (Multi-case Examples)

### 4.1. [시나리오 1] `calc_performance` 컨트롤 타이어 선형 보정 및 지수 산출
```python
import pandas as pd
from unoUtil.vehicle.analysis_test_data import calc_performance

# 1. 시험 결과 데이터프레임 구성 (C1 -> T1 -> C2 순서)
df_raw = pd.DataFrame({
    "tireSet": ["c1", "t_01", "c2"],
    "Datetime": pd.date_range("2026-03-17 09:00", periods=3, freq="h"),
    "BrkDist": [40.0, 42.0, 41.0]
})

# 2. 제동거리(BrkDist) 선형 보정 수행
df_perf = calc_performance(
    data=df_raw,
    target_col="BrkDist",
    name_col="tireSet",
    refer_kwd="c"
)
print(df_perf[["tireSet", "adj_BrkDist", "per_BrkDist"]])
# t_01의 예상 컨트롤 성능은 40.5m, 상대 성능 지수는 (40.5 / 42.0) * 100 = 96.43%
```

### 4.2. [시나리오 2] `calc_compare` 다차원 비교표 및 통계 요약 산출
```python
from unoUtil.vehicle.analysis_test_data import calc_compare

# 1. 비교표 및 통계 요약표 일괄 빌드
comp_df, stat_df = calc_compare(
    dfs=[df_perf],
    comp_cols=["tireSet"],
    sel_cols=["BrkDist", "per_BrkDist"]
)
print("📊 지표 중심 비교표:\n", comp_df)
print("📈 통계 요약표:\n", stat_df)
```

### 4.3. [시나리오 3] v1 레거시 별칭 및 인자 흡수 호환성 검증
```python
from unoUtil.vehicle.analysis_test_data import make_performance_df

# 구버전 함수명 및 헝가리안 인자로 안전하게 호출
df_legacy = make_performance_df(
    df_input=df_raw,
    str_result_col="BrkDist",
    str_name_col="tireSet"
)
print("🎉 v1 레거시 호환 정상:", "per_BrkDist" in df_legacy.columns)
```

---
**Last Updated**: 2026-09-26  
**Module**: `unoUtil.vehicle.analysis_test_data`  
**Standard**: unoUtil Clean Architecture v2.0
