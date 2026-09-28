# 🎯 fit_magic_formula (매직 포뮬러 비선형 최적 피팅 엔진)

## 📌 개요
`fit_magic_formula.py`는 실차 시험 계측 산점도 데이터(슬립율-제동력, 슬립각-코너링포스, 감속도-슬립)로부터 Pacejka Magic Formula의 비선형 계수들을 역추정하는 **적응형 최적화 피팅 엔진**입니다.

기존 `signal_process/curve_fit`의 `estimatorMF`와 `ai`의 `fit_mf_ax`를 단일 엔진으로 통합하여, 가중치 부여, 수직하중($F_z$) 연동 모드, 강건 손실(Huber loss), 경계 조건(Bounds) 탐색을 완벽히 지원합니다.

---

## 🛠️ 주요 클래스 및 함수

| 클래스/함수명 | 설명 | 비고 |
| :--- | :--- | :--- |
| `EstimatorMF` | Scipy `least_squares` 기반 적응형 비선형 피팅 추정기 | 구 `estimatorMF` 호환 |
| `MFResult` | 최적화 파라미터, MSE/RMSE, 잔차, 예측 함수를 캡슐화한 결과 데이터클래스 | 구조화된 결과 반환 |
| `fit_mf_ax(x, actual_Fx, initial_params, bounds, plot, save)` | 종가속도/제동력 데이터 전용 L-BFGS-B 최적화 피팅 함수 | 구 `optimize_and_plot` 호환 |

---

## 💡 사용 예시 (Usage Example)

```python
import numpy as np
from unoUtil.models.fitting import EstimatorMF

# 계측 슬립 및 제동력 데이터
slip = np.array([0.02, 0.05, 0.08, 0.12, 0.18, 0.25])
force = np.array([0.25, 0.60, 0.95, 1.05, 1.02, 0.98])

# EstimatorMF 피팅 수행
estimator = EstimatorMF()
result = estimator.fit(slip, force, robust=True)

print(f"피팅 성공: {result.success}")
print(f"추정 파라미터: {result.params}")
print(f"RMSE: {result.rmse:.4f}")
```
