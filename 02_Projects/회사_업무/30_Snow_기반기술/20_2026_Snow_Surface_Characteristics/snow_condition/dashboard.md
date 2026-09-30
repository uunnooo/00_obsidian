# 📊 snow_condition.dashboard 기술 매뉴얼

이 문서는 3D 시공간 노면 디지털 트윈 객체(`SurfaceConditionTwin`)의 데이터를 기반으로, 특정 시험 일자 및 세션의 노면 침하 및 온도 변화를 4차원(3D 공간 + 시간)으로 연속 보간하여 브라우저에서 동적으로 재생하는 **`dashboard`** 모듈의 명세 및 사용법을 정의합니다.

---

## 1. 📌 핵심 개요

노면 상태는 시험 시간 경과에 따라 지속적으로 변화합니다. `create_surface_animation_figure`는 Plotly 3D Surface 및 애니메이션 프레임을 자동 생성하여, 타임라인 슬라이더 조작 및 Play/Pause 버튼을 통해 노면 다져짐 현상을 인터랙티브하게 관찰할 수 있도록 지원합니다.

---

## 2. 🛠️ 핵심 API

### `create_surface_animation_figure(twin_or_interpolator, date=None, period=None, channel='height', interval_minutes=5, ...)`
* **역할**: Plotly 기반 3D 노면 서피스 애니메이션 객체 생성.
* **주요 인자**:
  * `twin_or_interpolator`: `SurfaceConditionTwin` 인스턴스
  * `date`: 대상 일자 (None 시 첫 번째 일자)
  * `period`: `'am'` 또는 `'pm'`
  * `channel`: `'height'` (노면 침하 깊이 mm) 또는 `'temp'` (노면 온도차 ℃)
  * `interval_minutes`: 시간 보간 간격 (분 단위, 기본값 5분)
* **반환값**: `plotly.graph_objs.Figure`

---

## 3. 💡 실무 사용 예제

```python
from snow_condition.surface_twin import SurfaceConditionTwin
from snow_condition.dashboard import create_surface_animation_figure

# 1. 디지털 트윈 구축
twin = SurfaceConditionTwin()
twin.build_digital_twin(df_surface_raw)

# 2. 3D 인터랙티브 애니메이션 피규어 생성
fig = create_surface_animation_figure(twin, channel='height', interval_minutes=10)

# 3. 브라우저 표시 또는 HTML 저장
fig.write_html("./reports/surface_4d_animation.html")
```
