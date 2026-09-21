# ❄️ surface_condition_twin.py 로컬 개발 매뉴얼

이 모듈은 수집된 실시간 노면 상태 데이터(센서 변위, 눈 침하 깊이, 노면 온도)를 시공간(Spatial-Temporal) 차원의 3차원 디지털 트윈 격자로 확장 구축하고, 임의의 시각과 위치 VBOX GPS 좌표 상의 노면 값을 보간하여 1:1 결합해 내기 위한 클래스 및 컨테이너 모듈입니다.

---

## 🏛️ 1. API 명세 및 상세 설계

### 1.1 `SurfaceGridSnapshot`
특정 계측 시점(Timestamp)에서의 2D/3D 노면 공간 격자 맵 및 보간 연산기(RegularGridInterpolator)를 품은 격자 보관 컨테이너 클래스입니다.
* **주요 메서드**:
  * `query(pos_yx)`: 주어진 횡/종방향 (Y, X) 좌표 배열에 대응되는 눈 침하 깊이(평균/좌/우), 온도차(평균/센서별) 보간값을 산출합니다.

### 1.2 `calc_calibrated_sensor_offsets(df_raw)`
계측 센서 지그의 기구적 장착 오차(Out vs Tire)를 수학적으로 수평 정렬하여 순수한 눈의 눌림량(침하 깊이)을 산출합니다.
* **인자**:
  * `df_raw (pd.DataFrame)`: 원시 노면 계측 데이터프레임
* **반환값**:
  * `pd.DataFrame`: 센서 물리적 마운트 오프셋이 평탄 정렬된 데이터프레임
* **하위 호환성 에일리어스**:
  * `calibrate_sensor_offsets`

### 1.3 `calc_single_snapshot(df_group, method)`
단일 계측 스윕(Sweep)의 점(Point) 데이터로부터 2D/3D 트랙 전역 격자 맵을 예측하고, `SurfaceGridSnapshot` 인스턴스를 구축합니다.
* **보간 방식**: `Hybrid` (Convex Hull 내부는 Scipy Cubic Spline, 외부는 Random Forest), `RF`, `KNN`, `Linear` 중 스위칭 지원
* **하위 호환성 에일리어스**:
  * `fit_single_snapshot`
  * `calc_surface_grid` / `fit_surface_grid`

### 1.4 `calc_digital_twin(df_surface, group_col, method)`
전체 노면 데이터를 기반으로 날짜(Date) 및 오전/오후(Period: am/pm) 세션을 자동 감지하고 분류하여, 세션별 시공간 3D 디지털 트윈 스냅샷 시리즈를 형성합니다.
* **하위 호환성 에일리어스**:
  * `build_digital_twin`

### 1.5 `get_surface_condition(target_time, pos_x, pos_y, ...)`
실차 제동 시험이 일어난 정확한 타임스탬프와 VBOX GPS 좌표 `(PosX, PosY)`를 받아, 해당 일자/세션의 디지털 트윈 보간기에 질의하여 당시의 정밀한 눈 침하 깊이(`char_height`) 및 노면 온도차(`char_temp`)를 1:1 매칭 산출합니다.
* **인자**:
  * `target_time (pd.Timestamp)`: 제동 발생 시점
  * `pos_x`, `pos_y` (float): VBOX 주행 위치 ($m$)
  * `full` (bool): True인 경우 TempOut, TempTire, HeightLeft, HeightRight까지 포함한 6개 튜플을 산출
* **하위 호환성 에일리어스**:
  * `query_surface_condition`

### 1.6 `plot_surface_snapshot(snapshot_idx, title, save, close)`
특정 스냅샷의 2차원 공간 격자 등고선 맵(눈 침하 깊이 및 온도차 분포)을 플로팅합니다.
* **인자**:
  * `save (Union[bool, str, Path])`: 저장 다형성 제어 파라미터
  * `close (bool)`: 시각화 자원 해제 및 Non-blocking 여부 (기본값: `True`)
* **반환값**:
  * `Tuple[plt.Figure, Any]`

---

## 💻 2. 실무 활용 예제

```python
import pandas as pd
from Snow_braking_relate_condition.surface_condition_twin import SurfaceConditionTwin

# 1. 디지털 트윈 객체 생성 및 해상도 격자(X: 5, Y: 9) 설정
twin = SurfaceConditionTwin(nx=5, ny=9)

# 2. 노면 로우 데이터 입력 및 시공간 스냅샷 자동 구축
df_surface_raw = pd.read_pickle("./df_surface_raw.pkl")
twin.calc_digital_twin(df_surface_raw, method='RF')

# 3. 특정 제동 런 순간의 시공간 노면값 정밀 보간 결합 쿼리
test_time = pd.Timestamp("2026-01-15 10:15:00")
est_h, est_t = twin.get_surface_condition(
    target_time=test_time,
    pos_x=120.0,
    pos_y=65.0
)
print(f"매칭된 눈 침하 깊이: {est_h:.2f} mm, 노면 온도차: {est_t:.2f} ℃")

# 4. 2D 트랙 등고선 격자 맵 플로팅 및 저장
fig, axes = twin.plot_surface_snapshot(
    snapshot_idx=0,
    save=True,  # 사내 기본 첨부 폴더에 저장
    close=True  # 자원 해제 및 백그라운드 구동(Non-blocking)
)
```
