---
id: "graphics_plotters_surface_3d"
title: "surface_3d (3D 노면/타이어 곡면 그리드 생성 및 시각화)"
type: project
category_main: 회사_업무
category_sub: unoUtil
topic: surface_3d
date: 2026-09-18
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - graphics
  - plotters
  - surface_3d
  - 3D시각화
aliases:
  - "_Analysis3D_"
  - "Analysis3D"
  - "surface_3d"
  - "unoUtil.convenienceFunction._Analysis3D_"
---

# 🌐 surface_3d (3D 노면/타이어 곡면 그리드 생성 및 시각화)

> [!ABSTRACT] 📐 모듈 개요
> 흩어져 있는 1차원 $x, y, z$ 계측 포인트(예: 눈 깊이 변동량, 노면 온도, 제동거리/성능)를 다변량 보간 및 머신러닝 회귀를 통해 **정규 2D 격자(Grid)로 보간**하고, 3차원 입체 곡면(Surface Plot) 및 등고선(Contour)으로 렌더링하는 시각화 모듈입니다.  
> 과거 `unoUtil.convenienceFunction._Analysis3D_` 모듈이 본 위치로 정식 이관되었으며, **무중단 하위 호환성(Zero Breaking Change) 브릿지**가 완비되어 있습니다.

---

## 🏛️ 1. 패키지 위치 및 임포트 규격

### 최신 표준 임포트 (PEP 8 권장)
```python
from unoUtil.graphics.plotters.surface_3d import make_3dSurfaceGridArray, plot_3dSurfaceGridArray
# 또는 패키지 레벨
from unoUtil.graphics import surface_3d
```

### 레거시 호환 임포트 (동적 브릿지 자동 라우팅)
```python
# 구버전 코드가 그대로 동작함 (sys.modules 프록시 매핑)
from unoUtil.convenienceFunction._Analysis3D_ import make_3dSurfaceGridArray, plot_3dSurfaceGridArray
import unoUtil.convenienceFunction._Analysis3D_ as Analysis3D
```

---

## ⚙️ 2. 핵심 함수 API 명세

### `make_3dSurfaceGridArray(x, y, z, **kwargs)`
1차원 $x, y, z$ 좌표 시계열을 입력받아 지정된 해상도의 정규 2D 그리드 및 $z$ 곡면 행렬을 산출하고 3D 시각화를 수행합니다.

#### 주요 입력 파라미터 (Args)
| 파라미터명 | 타입 | 기본값 | 설명 및 활용 |
| :--- | :---: | :---: | :--- |
| `x`, `y`, `z` | `Series` / `array` | 필수 | 1차원 독립 변수 $x$, $y$ 및 종속 관측 변수 $z$ |
| `method` | `str` | `'linear'` | 2D 보간 알고리즘 (`'linear'`, `'cubic'`, `'nearest'`, `'knn'`, `'rf'`, `'rbf'`, `'mlp'`) |
| `interval` | `float` | `0.01` | 격자 생성 기본 간격 |
| `xInterval`, `yInterval` | `float` | `interval` | $x, y$ 축 개별 격자 해상도 |
| `xSpace`, `ySpace` | `int` | `False` | `linspace` 개수 기반 균등 격자 분할 시 지정 |
| `norm` | `str` | `'per'` | $z$축 정규화 방식 (`'per'` = 평균 대비 %, `'index'` = 인덱스화, `'minmax'` = MinMax 스케일링, `False` = 원시값) |
| `std` | `bool` | `False` | 입력 $x, y, z$를 0~1 표준 스케일링 적용 여부 |
| `view` | `list` | `[50, -91]` | 3D 차트 기본 뷰 각도 `[elev, azim]` (고도각, 방위각) |
| `plot` | `bool` | `True` | 시각화 렌더링 수행 여부 |
| `cmap` | `str` | `'viridis'` | Matplotlib 컬러맵 (`'viridis'`, `'jet'`, `'bwr'`, `'summer'`) |
| `contour` / `con` | `bool` | `True` | 3D 곡면 하단 바닥면에 2D 등고선(Contour) 투영 여부 |
| `dot` | `bool` | `True` | 원시 계측 관측점(Scatter Dot) 중첩 표시 여부 |

#### 반환값 (Returns)
* 생성된 격자 좌표 배열 `xi`, `yi`, 보간된 표면 높이 배열 `zi`, 렌더링된 Matplotlib `fig, ax` 객체 등을 포함한 결과 딕셔너리.

---

### `plot_3dSurfaceGridArray(x, y, z, **kwargs)`
격자 배열이 이미 준비되어 있거나 래핑된 조건에서 3차원 Surface 및 Wireframe 차트를 렌더링하는 전용 플로터입니다.

---

## 🛡️ 3. 하위 호환성 (Zero Breaking Change) 아키텍처

1. **프록시 모듈 브릿지 (`unoUtil/convenienceFunction/_Analysis3D_.py`)**:
   - 신규 `surface_3d.py`의 핵심 함수를 `__all__`로 재노출하여 레거시 스크립트의 `import` 구문을 무중단 지원.
2. **패키지 레벨 가상 바인딩 (`unoUtil/__init__.py`)**:
   ```python
   try:
       from unoUtil.graphics.plotters import surface_3d
       sys.modules['unoUtil.convenienceFunction._Analysis3D_'] = surface_3d
       sys.modules['unoUtil.utils._Analysis3D_'] = surface_3d
       setattr(utils, '_Analysis3D_', surface_3d)
   except Exception:
       pass
   ```
   - 인터프리터 메모리 상에 `unoUtil.convenienceFunction._Analysis3D_` 네임스페이스를 동적 등록하여 하위 호환 100% 보장.

---

## 🔗 연계 시스템 및 위키 문서
* 🎨 **[[graphics/00_graphics_대시보드|graphics 패키지 통합 대시보드]]**
* 🏛️ **[[00_unoUtil_PEP8_표준화_총괄_가이드|unoUtil v2.0 PEP 8 표준화 총괄 가이드]]**
* ❄️ **[[31_스노우_노면_디지털트윈_및_제동성능_보정_위키|스노우 노면 디지털 트윈 및 제동성능 보정 위키]]**
