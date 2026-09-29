# 🧭 CurveCombiner 스플라인 곡선 통합 기하 피팅 엔진 매뉴얼 (curve_combiner.md)

## 📌 1. 개요 및 목적 (Overview)
`curve_combiner` 모듈은 타이어의 기하학적 비선형 슬립 성능 곡선(Magic Formula)과 주행 궤적의 완벽한 접선 연속성을 확보하기 위한 **초고도 스플라인 곡선 피팅, 에르미트 보간(Hermite Spline) 및 프레넬 적분 기반 클로소이드 곡선 연결(Clothoid Connector) 통합 결합 분석 엔진(`CurveCombiner`)**을 제공합니다.

차량 횡력 및 선회력 한계를 분석할 때, 순수 비선형 타이어 거동 해석 곡선(MF)과 물리 직선 차선 모델을 임의로 이어붙이면 결합점에서 곡률(Curvature)이 불연속적으로 튀어 물리 정합성이 파괴됩니다. 
본 모듈은 연결부에서의 곡률 연속성($G^2$ 연속)을 확보하기 위해 **클로소이드 오일러 스플라인 보간 및 조각적 3차 PCHIP 평활화 알고리즘**을 이중 결합하여 설계되어, 사내 현수 역학 설계 및 선회 차선 추정 파이프라인에서 독보적인 기하 변환 성능을 자랑합니다.

---

## 🛠️ 2. 핵심 API 명세 (API Specifications)

### 2.1. `CurveCombiner` 하위 컴포넌트 클래스 목록

| 클래스명 | 역할 및 주요 메서드 설명 |
| :--- | :--- |
| `BaseSpline` | 자식 곡선 연결 컴포넌트들의 기본 상위 스플라인 클래스 (`fit()`, `plot(save)`) |
| `GradientSmoother` | 미분 경사도의 국부적인 센서 노이즈를 제어하기 위한 `smooth_grad()` 전처리 스무더 |
| `TransitionFinder` | 곡선과 직선의 물리적 한계 경계선 변곡점을 자동 검출하는 `find_transition_point()` 엔진 |
| `LineMaker` | 계측 원시 점군에서 직선 최적화 기울기와 오프셋을 추출하는 `find_init_line()` 피터 |
| `HermiteConnector` | 세그먼트 간의 안전 슬라이딩 연속 연결을 지원하는 `fit_hermite_safe()` 조각 보간기 |
| `ClothoidConnector` | 프레넬 적분(Fresnel Integral) 최적화로 두 곡선 사이 곡률 연속성을 보정하는 `fit()` 및 `predict()` 엔진 |
| `PchipSmoother` | 연결부가 여전히 미세하게 불연속적일 때 1/10 밀도로 조각 3차 에르미트 보간을 수행하는 Pchip 스무더 |
| `CurveCombiner` | **[최상위 통합 지휘자]** 단계별 피팅 프로세스 전체 연쇄 기동 및 3D/2D 정합 곡선 빌드 수행 (`fit()`, `plot()`) |

---

## 📋 3. 입력 파라미터 상세 정의 (Arguments)

1. **`x_raw` / `y_raw` (`np.ndarray` - 필수)**:
   - 기하학적으로 결합하고 평활화할 원시 센서 계측 X, Y 궤적 평면 좌표 데이터군입니다.
2. **`mf_w` / `wg` (`float` - 선택)**:
   - 타이어 매직포뮬러 피팅 가중치와 가우시안 경사도 평활화 가중 팩터입니다.
3. **`clothoid_val` (`bool` - 선택, 기본값: `True`)**:
   - 접합부에 프레넬 클로소이드 연속 완화 곡선(Transition Curve)을 결합하여 가중 곡률 연속성을 확보할지 여부입니다.

---

## 💻 4. 실무 활용 예제 (Multi-case Examples)

### 4.1. [시나리오 1] CurveCombiner를 이용한 MF 타이어 모델 곡선과 직선 차선의 기하 접합 피팅
```python
import numpy as np
from unoUtil.signal_process.curve_fit.CurveCombiner.curve_combiner import CurveCombiner

# 1. 2차원 원시 곡선 궤적 데이터 빌드 (Magic Formula s자 곡선 형태와 직선 영역 합성)
np.random.seed(42)
x_test = np.linspace(-10, 50, 1000)
# 비선형 곡선 부분과 직선 부분이 합성된 형상에 노이즈 추가
y_test = 20.0 * np.tanh(x_test / 5.0) + 0.5 * x_test + np.random.normal(0, 0.1, len(x_test))

# 2. 통합 결합 분석 엔진 기동
combiner = CurveCombiner()

# 3. 단계별 기하 적합 적합(fit) 수행 (직선 추출 -> Hermite -> Pchip)
combiner.fit(
    x_raw=x_test,
    y_raw=y_test,
    mf_w=0.8,
    wg=1.2,
    inter=10,
    x_end=45.0,
    target_ratio_pos_x=0.9,
    target_ratio_neg_x=0.1,
    target_ratio_pos_y=0.9,
    target_ratio_neg_y=0.1,
    clothoid_val=True,   # 클로소이드 완화 곡선 연속 결합 가동!
    plot_steps=False,
    print_score=True
)

print("📐 기하학적 곡률 연속 스플라인 결합 곡선 빌드가 완료되었습니다.")
```

### 4.2. [시나리오 2] 접선 연속 결합 궤적 차트 렌더링 및 무중단 자동 저장
```python
# 2D 연속 결합 피팅선과 원시 점군 대조 플롯 이미지 저장 자동 분기
combiner.plot(
    xlabel="Track Position X (m)",
    ylabel="Track Lateral Y (m)",
    title="Technoring Lateral Track Spline Combination",
    save=True  # default 시각화 폴더로 Non-blocking 저장 처리
)

print("💾 스플라인 정합 곡선 시각화 차트 파일 저장이 완료되었습니다.")
```

### 4.3. [시나리오 3] HermiteConnector 독립 기동을 통한 두 궤적 간의 안전 구간 Hermite 보간
```python
from unoUtil.signal_process.curve_fit.CurveCombiner.curve_combiner import HermiteConnector

# 두 궤적 사이의 단절 영역을 기울기 m0, m1 연속성을 확보하며 보간
# fit_hermite_safe 수동 기동 테스트
interpolated_points = HermiteConnector.fit_hermite_safe(
    x=np.linspace(5.0, 15.0, 100),
    x0=5.0, x1=15.0,
    y0=2.3, y1=8.7,
    m0=0.1, m1=0.8,  # 양 경계점의 접선 기울기 지정
    alpha=0.5,
    plot=False
)

print(f"🛡️ 에르미트 보간 성공! 보간된 내부 지점 수: {len(interpolated_points)}")
```
