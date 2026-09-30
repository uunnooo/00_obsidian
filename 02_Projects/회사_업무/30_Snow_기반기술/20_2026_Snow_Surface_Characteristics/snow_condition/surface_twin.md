# 🗺️ snow_condition.surface_twin 기술 매뉴얼

이 문서는 스노우 노면 6채널 센서 계측 데이터의 지그 장착 오차 자동 보정, 2D 공간 격자 머신러닝 보간, 그리고 시간 축 연속 보간을 통한 **3D 시공간 디지털 트윈(Spatial-Temporal Digital Twin)** 모듈의 명세 및 사용법을 정의합니다.

---

## 1. 📌 핵심 개요

노면 계측 차량의 센서 지그는 차량 좌/우, 높이 센서 간 미세한 장착 편차가 발생합니다. `SurfaceConditionTwin`은 차량 외측 레퍼런스 높이 센서와 주행 타이어부 센서 간의 차분을 계산하여 **노면 눈 침하 깊이(Penetration Depth, $H$)** 및 **노면 온도차($\Delta T$)**를 원점 대칭 구간($[-3.0, +3.0]\,\text{mm}$, $[-3.0, +3.0]\,^\circ\text{C}$)으로 복원합니다. 또한 불규칙한 주행 궤적 계측점을 고해상도 직교 격자 맵으로 변환하고 임의의 제동 시험 시각/좌표와 1:1 시공간 보간 매칭을 수행합니다.

---

## 2. 🛠️ 핵심 클래스 및 API

### `SurfaceConditionTwin`

| 메서드명 | 역할 | 주요 인자 | 반환값 |
| :--- | :--- | :--- | :--- |
| `build_digital_twin(data, method='RF')` | 원본 노면 데이터로부터 센서 오프셋 보정 및 시공간 스냅샷 구축 | `data: pd.DataFrame`, `method: str` | `int` (스냅샷 개수) |
| `get_surface_condition(timestamp, pos_x, pos_y, full=False)` | 특정 일시/좌표 상의 노면 침하량 및 노면온도 시공간 보간 쿼리 | `timestamp`, `pos_x`, `pos_y`, `full: bool` | `Tuple[float, float]` (기본) |
| `plot_surface_snapshot(idx=0, save=False, close=True)` | 특정 스냅샷의 2D 등고선 노면 침하 및 온도 맵 시각화 | `idx: int`, `save: Union[bool, str, Path]`, `close: bool` | `Tuple[plt.Figure, Any]` |
| `get_session_summary()` | 세션별 스냅샷 요약 테이블 생성 | 없음 | `pd.DataFrame` |

---

## 3. 💡 실무 사용 예제

```python
import pandas as pd
from snow_condition.surface_twin import SurfaceConditionTwin

# 1. 디지털 트윈 객체 초기화
twin = SurfaceConditionTwin()

# 2. 노면 계측 데이터 적재 및 디지털 트윈 구축
num_snaps = twin.build_digital_twin(df_surface_raw, method='RF')
print(f"생성된 디지털 트윈 스냅샷 수: {num_snaps}개")

# 3. 실차 제동 시험 시점과 위치에서의 노면 조건 1:1 보간 쿼리
test_time = "2026-01-15 10:15:00"
est_depth, est_temp = twin.get_surface_condition(test_time, pos_x=120.5, pos_y=68.2)
print(f"보간 노면 눈 침하 깊이: {est_depth:.2f} mm")
print(f"보간 노면 온도차: {est_temp:.2f} ℃")

# 4. 노면 맵 시각화 및 논블로킹 저장
fig, axes = twin.plot_surface_snapshot(idx=0, save="./reports/surface_map_0.png", close=True)
```
