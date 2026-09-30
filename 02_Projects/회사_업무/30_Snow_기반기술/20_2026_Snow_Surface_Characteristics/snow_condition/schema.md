# 📋 snow_condition.schema 기술 매뉴얼

이 문서는 스노우 노면 특성 및 실차 제동 성능 분석 시스템의 **단일 진실 공급원(SSOT, Single Source of Truth) 공식 컬럼 스키마**와 이기종 데이터 일괄 정규화 함수(`harmonize_snow_dataframe`)의 명세 및 사용법을 정의합니다.

---

## 1. 📌 핵심 개요

다양한 계측 장비(VBOX, Dewesoft), 연구원별 수기 엑셀, 레거시 스크립트 등에서 파편화되었던 수많은 컬럼명(`ReqNo`, `TestTireSet`, `HeightDiffAver`, `WB-AH` 등)을 단 하나의 표준 명칭 체계로 확립하고, 시스템 내부로 들어오는 단일 관문(Single-Gate)에서 일괄 정규화합니다.

---

## 2. 🔤 공식 표준 컬럼 규격 (SSOT Schema)

### 2.1 4대 패밀리 주요 컬럼

| 그룹 | 표준 컬럼명 (SSOT) | 파이썬 상수 | 설명 |
| :--- | :--- | :--- | :--- |
| **메타데이터** | `infor_REQ_NO` | `COL_REQ_NO` | 시험 의뢰서 고유 번호 |
| | `infor_TIRE_SET` | `COL_TIRE_SET` | 타이어 세트 식별자 (C1, T1 등) |
| | `infor_CTB_COMPOUND` | `COL_CTB_COMPOUND` | 캡트레드 컴파운드 |
| | `infor_PATTERN` | `COL_PATTERN` | 트레드 패턴명 |
| **주행/트랙** | `test_date` | `COL_TEST_DATE` | 시험 일자 (YYYY-MM-DD) |
| | `test_period` | `COL_TEST_PERIOD` | 시험 세션 (`am`, `pm`, `종일`) |
| | `test_order` | `COL_TEST_ORDER` | 시험 차수 (`1st`, `2nd`) |
| | `test_pos_x`, `test_pos_y` | `COL_POS_X`, `COL_POS_Y` | 트랙 2D 직교 좌표 (m) |
| **특성/성능** | `char_brk_dist` | `COL_BRK_DIST` | 실측 제동거리 (m) |
| | `char_height` | `COL_HEIGHT` | 노면 눈 침하 깊이 / 눌림량 (mm) |
| | `char_temp` | `COL_TEMP` | 노면 온도차 (℃) |
| **기상 인자** | `cd_test_ah` | `COL_TEST_AH` | 시험 중 절대습도 (g/m³) |
| | `cd_test_temp` | `COL_TEST_TEMP` | 시험 중 외기온도 (℃) |
| **보정 지표** | `char_brk_dist_corr` | `COL_BRK_DIST_CORR` | 환경 보정된 제동거리 (m) |
| | `char_brk_dist_diff` | `COL_BRK_DIST_DIFF` | 1차 대비 2차 제동거리 차분 ($\Delta D$, m) |
| | `char_height_diff` | `COL_HEIGHT_DIFF` | 노면 침하 깊이 차분 ($\Delta H$, mm) |
| | `cd_test_ah_diff` | `COL_AH_DIFF` | 절대습도 차분 ($\Delta \text{AH}$, g/m³) |

---

## 3. 🛠️ API 레퍼런스

### `harmonize_snow_dataframe(data, copy=True, **kwargs)`
* **역할**: 입력 데이터프레임 내 레거시 컬럼을 공식 표준 컬럼명으로 치환하고, `run1`/`run2`를 `1st`/`2nd`로 정합합니다.
* **인자**:
  * `data (pd.DataFrame)`: 원본 데이터프레임
  * `copy (bool)`: 원본 데이터 보존 여부 (기본값: True)
  * `**kwargs`: 구버전 레거시 인자 `df_input` 자동 흡수
* **반환값**: `pd.DataFrame`: 100% 표준화된 데이터프레임

---

## 4. 💡 실무 사용 예제

```python
import pandas as pd
from snow_condition.schema import harmonize_snow_dataframe, COL_BRK_DIST, COL_HEIGHT

# 레거시 컬럼이 포함된 데이터프레임 로드
df_raw = pd.DataFrame({
    'ReqNo': ['R2026_01'],
    'TestTireSet': ['C1'],
    'TestOrder': ['run1'],
    'BrkDist': [24.5],
    'HeightDiffAver': [2.8],
    'WB-AH': [1.2]
})

# 단 1회 정규화 호출
df_std = harmonize_snow_dataframe(df_raw)

# 정식 표준 컬럼으로 안전하게 조회
print(df_std['infor_REQ_NO'].iloc[0])  # 'R2026_01'
print(df_std[COL_BRK_DIST].iloc[0])     # 24.5
print(df_std['test_order'].iloc[0])     # '1st'
```
