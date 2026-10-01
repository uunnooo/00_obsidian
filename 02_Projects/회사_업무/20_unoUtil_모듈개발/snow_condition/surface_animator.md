---
id: "surface_animator_20261001"
title: "surface_animator 상세 매뉴얼"
type: resource
category_main: 회사_업무
category_sub: 개발매뉴얼
date: 2026-10-01
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - snow_condition
  - surface_animator
  - 애니메이션
  - 4D시각화
  - 매뉴얼
project_link: "[[00_unoUtil_모듈개발_대시보드]]"
---

# 📊 snow_condition.surface_animator 기술 매뉴얼

이 문서는 3D 시공간 노면 디지털 트윈 객체(`SurfaceConditionTwin`)의 데이터를 기반으로, 특정 시험 일자 및 세션의 노면 침하 및 온도 변화를 4차원(3D 공간 + 시간)으로 연속 보간하여 브라우저에서 동적으로 재생하는 **`surface_animator`** 모듈의 명세 및 사용법을 정의합니다.

---

## 1. 📌 핵심 개요

노면 상태는 시험 시간 경과 및 기상 변화에 따라 지속적으로 변화합니다. `SurfaceAnimator` 클래스 및 `create_surface_animation_figure` 함수는 Plotly 3D Surface 및 애니메이션 프레임을 자동 생성하여, 타임라인 슬라이더 조작 및 Play/Pause 버튼을 통해 노면 다져짐 현상을 인터랙티브하게 관찰할 수 있도록 지원합니다.

---

## 2. 🛠️ 핵심 API

### 1) 클래스: `SurfaceAnimator(twin_or_interpolator=None)`
* **역할**: 디지털 트윈 객체를 주입받아 4D 애니메이션 피규어를 생성하는 시각화 전담 클래스.
* **주요 메서드**:
  * `create_figure(twin_or_interpolator=None, date=None, period=None, channel='height', interval_minutes=5, ...)`
    * 시간에 따른 3D 서피스 변화 Plotly Figure 반환.

### 2) 모듈 함수: `create_surface_animation_figure(twin_or_interpolator, date=None, period=None, channel='height', interval_minutes=5, ...)`
* **역할**: Plotly 기반 3D 노면 서피스 애니메이션 객체 단독 생성 함수.
* **주요 인자**:
  * `twin_or_interpolator`: `SurfaceConditionTwin` 인스턴스
  * `date`: 대상 일자 (None 시 첫 번째 일자)
  * `period`: `'am'` 또는 `'pm'`
  * `channel`: `'height'` (노면 침하 깊이 mm) 또는 `'temp'` (노면 온도차 ℃)
  * `interval_minutes`: 시간 보간 간격 (분 단위, 기본값 5분)
  * `cmap`: 컬러맵 (기본값 `'Viridis'`)
  * `duration`: 프레임 전환 시간 (ms 단위, 기본값 150ms)
  * `z_range`: Z축 고정 범위 `(z_min, z_max)`
* **반환값**: `plotly.graph_objs.Figure`

---

## 3. 💡 실무 사용 예제

### 방법 A: `SurfaceAnimator` 클래스 활용
```python
from unoUtil.snow_condition.surface_twin import SurfaceConditionTwin
from unoUtil.snow_condition.surface_animator import SurfaceAnimator

# 1. 디지털 트윈 구축
twin = SurfaceConditionTwin()
twin.build_digital_twin(df_surface_raw)

# 2. 애니메이터 인스턴스 생성 및 피규어 렌더링
animator = SurfaceAnimator(twin)
fig = animator.create_figure(channel='height', interval_minutes=10)

# 3. HTML 파일 저장 및 브라우저 열기
fig.write_html("./reports/surface_4d_height_animation.html")
```

### 방법 B: 모듈 함수 직접 호출
```python
from unoUtil.snow_condition.surface_twin import SurfaceConditionTwin
from unoUtil.snow_condition.surface_animator import create_surface_animation_figure

# 1. 디지털 트윈 구축
twin = SurfaceConditionTwin()
twin.build_digital_twin(df_surface_raw)

# 2. 3D 인터랙티브 애니메이션 피규어 생성
fig = create_surface_animation_figure(twin, channel='temp', interval_minutes=10)

# 3. 브라우저 표시
fig.show()
```
