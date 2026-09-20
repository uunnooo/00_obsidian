# 🧭 hndl_test 조종안정성 커브피팅 및 선회 거동 해석 모듈 매뉴얼 (hndl_test.md)

## 📌 1. 개요 및 목적 (Overview)
`hndl_test` 모듈은 실차 조종안정성(Handling) 주행 시험 데이터를 기반으로 차량의 **언더스티어 곡선(Understeer Curve, US-curve) 및 정상 상태 선회 응답 곡선(Steady-State Curve, SS-curve)을 추정하는 고성능 비선형 커브피팅, B-스플라인 보간 및 머신러닝 기하 예측 엔진**을 구현합니다.

차량 조종안정성 평가 시 횡가속도가 한계 한계점에 도달할수록 차량의 거동은 극도의 비선형성을 띠게 됩니다. 
본 모듈은 초반 선형 구간에서는 유연한 **B-Spline(스플라인) 보간**을 가동하고, 횡한계 85% 이상의 극한 영역에서는 요레이트 변동 왜곡을 방어하기 위해 **의사결정 나무(Random Forest)의 트레이닝 깊이를 영리하게 제어 스무딩**하며, 최종 선회력 한계는 **타이어 매직포뮬러(Magic Formula) 그리드 서치 최적화**를 통해 수학적으로 완벽하게 피팅 평활화해 줍니다.

---

## 🛠️ 2. 핵심 API 명세 (API Specifications)

### 2.1. 글로벌 조종안정성 분석 함수 명세

| 함수명 | 입력 파라미터 | 설명 |
| :--- | :---: | :--- |
| `SP_CurveFit_RF(df_raw)` | `df_raw` | B-Spline 스무더와 깊이가 제어된 Random Forest 수치 예측 모델을 가우시안 무빙 평균으로 이중 융합하여 정밀한 언더스티어 평가 피팅선 도출 |
| `SP_CurveFit_MF(df)` | `df` | US-curve와 SS-curve 점군을 대상으로 비선형 Magic Formula 수식(4-파라미터 A, B, C, D)에 근거한 그리드 서치 및 최소제곱 최적화 추정 수행 |

---

## 📋 3. 입력 파라미터 상세 정의 (Arguments)

1. **`df_raw` / `df` (`pd.DataFrame` - 필수)**:
   - 횡가속도(Lateral Acceleration), 요레이트(Yaw Rate), 조향각(Steering Angle) 채널이 포함된 주행 시계열 데이터프레임입니다.

---

## 💻 4. 실무 활용 예제 (Multi-case Examples)

### 4.1. [시나리오 1] B-Spline 및 Random Forest 융합 언더스티어 곡선(US-Curve) 피팅
```python
import numpy as np
import pandas as pd
from unoUtil.vehicle.hndl_test import SP_CurveFit_RF

# 1. 조향각 대비 횡가속도 계측 가상 핸들링 스윕 데이터 빌드
np.random.seed(42)
lat_acc = np.linspace(0, 0.9, 500)
steer_angle = 15.0 * lat_acc + 5.0 * (lat_acc ** 3) + np.random.normal(0, 0.02, len(lat_acc))
df_hndl = pd.DataFrame({"LatAcc": lat_acc, "SteerAngle": steer_angle})

# 2. 고성능 융합 스무딩 피팅 기동
fitted_steer = SP_CurveFit_RF(df_raw=df_hndl)
print(f"📊 피팅 완료! 피팅 포인트 수: {len(fitted_steer)}")
```

### 4.2. [시나리오 2] Magic Formula 그리드 서치 기반 선회 비선형 4-파라미터 최적화 추정
```python
from unoUtil.vehicle.hndl_test import SP_CurveFit_MF

# 횡슬립각 대비 코너링포스 관계 데이터프레임 빌드
df_slip_force = pd.DataFrame({
    "SlipAngle": np.linspace(-10, 10, 100),
    "CorneringForce": 1200 * np.sin(1.8 * np.arctan(1.1 * np.linspace(-10, 10, 100)))
})

# 매직포뮬러 4-파라미터(A, B, C, D) 수치 추정 최적화 기동
optimal_params, df_fitted_mf = SP_CurveFit_MF(df=df_slip_force)

print(f"🎯 최적 추정된 Magic Formula 계수: {optimal_params}")
# Output: [A_peak, B_stiffness, C_shape, D_curvature] 수치 어레이 반환
```

### 4.3. [시나리오 3] Non-blocking 시각화 및 자동 저장 연동
```python
# 피팅 결과 등고 및 타점 비교 차트 무중단 저장
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.scatter(df_hndl["LatAcc"], df_hndl["SteerAngle"], alpha=0.3, label="Raw Data")
ax.plot(df_hndl["LatAcc"], fitted_steer, "r-", lw=2, label="RF-Spline Fit")
ax.legend()

fig.savefig("./test_output/handling_understeer_curve.png", dpi=200, bbox_inches="tight")
plt.close(fig)  # 백그라운드 무중단 메모리 회수

print("💾 조종안정성 한계 거동 피팅 그래프 저장이 완료되었습니다.")
```
