# 🗺️ snow_condition.surface_interpolator 기술 매뉴얼

이 문서는 스노우 노면 계측 센서 데이터로부터 3D 공간 격자 보간 모델을 구축(`fit`)하고, 실차 제동 시험 묶음(`Date`, `ReqNo`, `TestOrder`)의 최초 시작 시각을 감지하여 12:30 경계 쪼개짐 없이 안전하게 노면 침하량과 노면온도를 보간 결합(`transform`)하는 **`SnowSurfaceInterpolator`** 모듈의 명세 및 사용법을 정의합니다.

---

## 1. 📌 핵심 개요: Cond_ID 최우선 정방향 계층 구조와 시공간 보정
 
노면 계측 데이터와 실차 제동 성능 간의 시공간 보정은 **"동일한 시기 및 동일한 노면 물리 컨디션"**을 보장하는 **세션(Session, `Cond_ID`)** 단위로 엄격히 격리되어 수행되어야 합니다.
 
* **정방향 계층 구조 (Cond_ID ➔ Sweep/Snapshot)**:
  * 물리적 최상위 단위는 트랙터 노면 정비(Preparing)로 리셋되는 **노면 세션(`Cond_ID`: 날짜_오전/오후/종일)**입니다.
  * `SnowSurfaceInterpolator.fit()`은 데이터프레임의 `Cond_ID`를 최우선 기준으로 세션을 먼저 분할한 뒤, 각 세션 내부에서 `TestTireSet`(또는 측정 시간차) 단위로 스냅샷을 구축하여 세션 간 경계 혼입 및 데이터 오염을 100% 원천 차단합니다.
* **학습된 세션 레지스트리(`session_registry`) 기반 지능형 결합 (`transform`)**:
  * 제동 평가는 한 번 시작하면 여러 타이어(`T1`, `T2`, `C1` 등)를 연속해서 평가합니다.
  * `Date + ReqNo + TestOrder`의 **최초 시작 시각(`min(Datetime)`)**을 감지하여 12:30 경계 시각 쪼개짐을 방지합니다.
  * 특히, 해당 일자에 등록된 노면 세션(`all`, `am`, `pm`) 메타데이터를 기반으로 단일 세션일(예: `2026-01-14_all`)은 시험 시각과 무관하게 노면 세션과 1:1 완벽 매칭됩니다.
 
---
 
## 2. 🛠️ 핵심 클래스 및 API
 
### `SnowSurfaceInterpolator`
 
| 메서드명 | 역할 | 주요 인자 | 반환값 |
| :--- | :--- | :--- | :--- |
| `fit(data, height_col=None, temp_col=None, cond_id_col=None, method='RF')` | 전처리된 노면 특성 컬럼 및 세션 식별자 기반 3D 공간 격자 스냅샷 맵 구축 | `data: pd.DataFrame`, `height_col: str`, `temp_col: str`, `cond_id_col: str` | `self` (메서드 체이닝) |
| `transform(data, time_col=None, pos_x_col=None, pos_y_col=None)` | 제동 시험 묶음 최초 시작 시각 감지 ➔ 12:30 쪼개짐 없는 `test_cond_id` 자동 생성 및 노면 침하량(`char_height`), 노면온도(`char_temp`) 결합 | `data: pd.DataFrame` | `pd.DataFrame` (결합 완료 데이터셋) |
| `fit_transform(df_surface, df_test)` | `fit`과 `transform`을 한 번에 실행 | `df_surface`, `df_test` | `pd.DataFrame` |
| `get(timestamp, pos_x, pos_y, full=False, cond_id=None)` | 특정 일시/좌표 상의 노면 침하량 및 노면온도 1:1 보간 쿼리 | `timestamp`, `pos_x`, `pos_y`, `full: bool`, `cond_id: Optional[str]` | `Tuple[float, float]` (기본) |
| `plot(idx=0, save=False, close=True)` | 특정 스냅샷의 2D 등고선 노면 침하 및 온도 맵 시각화 | `idx: int`, `save: Union[bool, str, Path]`, `close: bool` | `Tuple[plt.Figure, Any]` |
| `summary()` | 구축된 세션별 스냅샷 요약 테이블 반환 | 없음 | `pd.DataFrame` |
 
### 전역 유틸리티 함수
 
| 함수명 | 역할 | 주요 인자 | 반환값 |
| :--- | :--- | :--- | :--- |
| `classify_surface_condition(dt, session_calendar=None)` | 타임스탬프로부터 세션 구분(am/pm/all) 및 Cond_ID 자동 판별 (하드코딩 배제된 범용 헬퍼) | `dt: Any`, `session_calendar: Optional[Dict]` | `Dict[str, Any]` (`date`, `preparing`, `cond`, `cond_id`) |

---

## 3. 💡 실무 사용 예제

### 실차 제동 시험 데이터프레임 원스톱 결합 (권장)

```python
import pandas as pd
from unoUtil.snow_condition import SnowSurfaceInterpolator

# 1. 노면 보간기 객체 초기화 및 학습 (전처리 완료된 컬럼명 명시)
interp = SnowSurfaceInterpolator()
interp.fit(
    df_surface,
    height_col='char_height',
    temp_col='char_temp',
    cond_id_col='Cond_ID',
    method='RF'
)
print(interp.summary())

# 2. 제동 데이터프레임에 안전하게 test_cond_id 자동 부여 및 노면 침하량/온도 결합 (단 1줄!)
df_combined = interp.transform(df_brk)

# 3. 결과 확인 (char_height, char_temp, test_cond_id 자동 결합 확인)
print(df_combined[['infor_REQ_NO', 'test_order', 'test_cond_id', 'char_height', 'char_temp']].head())
```

### 단일 시점 및 좌표 질의

```python
test_time = "2026-01-15 10:15:00"
est_depth, est_temp = interp.get(test_time, pos_x=120.5, pos_y=68.2)
print(f"보간 노면 눈 침하 깊이: {est_depth:.2f} mm, 노면 온도차: {est_temp:.2f} ℃")
```

### 격자 맵 시각화

```python
# 노면 맵 시각화 및 논블로킹 저장
fig, axes = interp.plot(idx=0, save="./reports/surface_map_0.png", close=True)
```
