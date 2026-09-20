# 🧭 surface_3d 3차원 노면 및 타이어 곡면 그리드 시각화 매뉴얼 (surface_3d.md)

## 📌 1. 개요 및 목적 (Overview)
`surface_3d` 모듈은 타이어 노면 접지압, 실차 노면 변형 거동 및 3차원 계측 그리드 데이터를 3D 공간 위에 입체적으로 표현하기 위한 **3차원 표면 격자 그리드 생성, 시각화 및 다중 선형 회귀 분석(Regression3D) 엔진**을 구현합니다.

복잡한 다변량 센서 데이터를 2차원 평면에만 그리면 실제 계측 필드에서의 운동역학적 왜곡과 센서 눌림량의 공간적 상호작용을 한눈에 식별하기 어렵습니다. 
본 모듈은 임의로 수집된 X, Y, Z 데이터를 수치 격자망으로 정형화하는 격자 보간 알고리즘(`make_3dSurfaceGridArray`)을 탑재하였으며, Matplotlib 3D mplot3d 엔진을 활용한 고성능 와이어프레임 표면 시각화를 무중단으로 생성해 냅니다.

---

## 🛠️ 2. 핵심 API 명세 (API Specifications)

### 2.1. 글로벌 3D 시각화 함수 명세

| 함수명 | 입력 파라미터 | 설명 |
| :--- | :---: | :--- |
| `make_3dSurfaceGridArray(x, y, z)` | `x`, `y`, `z` | 불규칙하게 흐트러져 있는 1차원 데이터 군을 2차원 Meshgrid 평면 격자 구조로 자동 보간 및 정형화하여 그리드 배열 반환 |
| `plot_3dSurfaceGridArray(x, y, z, **kwargs)` | `x`, `y`, `z`, `**kwargs` | 격자 보간된 배열을 기반으로 Matplotlib 3D 축 위에 렌더링하고, 무중단 규칙에 따라 save/close를 수동 처리하여 피규어 반환 |
| `Regression3D(X1, X2, y)` | `X1`, `X2`, `y` | 3차원 평면 격자 데이터에 대한 다중 선형 회귀 평면 추정 및 회귀식 계수 산출 |

---

## 📋 3. 입력 파라미터 상세 정의 (Arguments)

1. **`x` / `y` / `z` (`np.ndarray` / `pd.Series` - 필수)**:
   - 3D 격자 축을 구성할 독립변수 2개(`x`, `y`)와 종속 수치변수 1개(`z` - 예: 접지압, 노면 눌림량)의 1차원 배열군입니다.
2. **`**kwargs` (선택 - 시각화 무중단 공통 인자)**:
   - `plot` (`bool` - 기본값 `True`): 시각화 3D 창 생성 여부.
   - `save` (`Union[bool, str, Path]` - 기본값 `False`): 다형성 이미지 저장 경로 제어 플래그.
   - `close` (`bool` - 기본값 `True`): 생성 후 백그라운드에서 메모리 해제 및 프로세스 블로킹 차단 여부.

---

## 💻 4. 실무 활용 예제 (Multi-case Examples)

### 4.1. [시나리오 1] 타이어 접지 형상 데이터의 3D 표면 격자망(Meshgrid) 연산 및 추출
```python
import numpy as np
from unoUtil.graphics.plotters.surface_3d import make_3dSurfaceGridArray

# 타이어 접지 폭(X) 및 접지 장(Y), 그리고 압력 센서 수치(Z) 모의 데이터
x_press = np.linspace(-50, 50, 100)
y_press = np.linspace(-100, 100, 100)
X, Y = np.meshgrid(x_press, y_press)
Z = 3.5 * np.exp(-((X/30)**2 + (Y/60)**2))  # 가우스 분포 압력 프로파일

# 3차원 표면 격자 데이터 정형화 실행
X_grid, Y_grid, Z_grid = make_3dSurfaceGridArray(X.flatten(), Y.flatten(), Z.flatten())

print(f"📐 3D 격자망 빌드 완료! Grid Shape: {Z_grid.shape}")
```

### 4.2. [시나리오 2] Non-blocking 3D 시각화 및 디폴트 자동 저장 (plot_3dSurfaceGridArray)
```python
from unoUtil.graphics.plotters.surface_3d import plot_3dSurfaceGridArray

# 3D 와이어프레임 렌더링 기동 및 무중단 자동 저장 설정
fig, ax = plot_3dSurfaceGridArray(
    x=X.flatten(),
    y=Y.flatten(),
    z=Z.flatten(),
    plot=True,
    save=True,      # default 이미지 디렉터리로 저장 자동 분기
    close=True      # RAM 해제 및 백그라운드 무인 실행 보장 (show 비활성화)
)

print("💾 3D 노면 격자 피규어 생성 및 무중단 저장 절차가 완료되었습니다.")
```

### 4.3. [시나리오 3] Regression3D 함수를 활용한 접지압 선형 회귀 평면 추정
```python
from unoUtil.graphics.plotters.surface_3d import Regression3D

# 노지 접지 계측 데이터에 선형 경사면 모델 적용
X1_data = np.random.rand(100)
X2_data = np.random.rand(100)
y_noise = 2.0 * X1_data + 3.0 * X2_data + 1.0 + np.random.normal(0, 0.1, 100)

# 회귀 모델 평면 분석 실행
intercept, coef_1, coef_2 = Regression3D(X1_data, X2_data, y_noise)

print(f"📈 3차원 추정 평면 수식: Z = {coef_1:.2f} * X1 + {coef_2:.2f} * X2 + {intercept:.2f}")
```
