# ⚙️ `fit_least_squares` — Scipy 비선형 최소자승법 피팅 엔진

## 📌 개요
`fit_least_squares`는 Scipy의 `least_squares` 알고리즘을 기반으로, 타이어 특성 곡선(Pacejka Magic Formula 등)에 대한 **가중치 마스크(Weight Mask), 경계 조건(Bounds), 강건 손실 함수(Huber, Soft L1)**를 지원하는 적응형 비선형 피팅 추정기 모듈입니다.

---

## 🛠️ 주요 클래스: `EstimatorLeastSquares` (구 `EstimatorMF`)

### 1. 주요 기능
* **가중치 적응형 피팅 (`wm`, `wg`)**: 변곡점이나 피크 구간 등 특정 슬립 범위에 가중치($\times 10, \times 20$)를 부여하여 고정밀 피팅 지원.
* **강건 손실 함수 (`loss`)**: 계측 노이즈 및 이상치(Outlier)에 강인한 `soft_l1`, `huber` 손실 적용.
* **구조화된 결과 (`LeastSquaresResult`)**: 최적 파라미터(`params`), `rmse`, `cost`, `predict` 함수 캡슐화.

### 2. 사용 예시
```python
from unoUtil.models.fitting import EstimatorLeastSquares

est = EstimatorLeastSquares()
# 0.1 ~ 0.2 슬립율 구간에 20배 가중치 부여
res = est.fit(slip, force, wm=lambda x: (x >= 0.1) & (x <= 0.2), wg=20.0)

print(f"최적 파라미터: {res.params}")
print(f"RMSE 오차: {res.rmse:.4f}")
est.plot(title="MF Weighted Fit")
```

---

## 🛡️ 100% 무중단 하위 호환성
* `EstimatorMF` $\equiv$ `EstimatorLeastSquares`
* `fit_mf_ax` $\rightarrow$ 종가속도/제동력 L-BFGS-B 최적화 호환 함수
