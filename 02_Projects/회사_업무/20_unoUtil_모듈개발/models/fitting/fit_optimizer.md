# ⚙️ fit_optimizer (수치 최적화 및 베이지안 파라미터 추정 엔진)

## 📌 개요
`fit_optimizer.py`는 Scipy의 `minimize` 및 Scikit-Optimize의 가우시안 프로세스 베이지안 최적화(`gp_minimize`)를 결합하여, 임의의 물리/수학적 모델의 최적 계수를 역추정하는 **범용 비선형 최적화 추정기**입니다.

Grid Search, Random Search, Bayesian Optimization 등 3대 초깃값 탐색 파이프라인을 내장하여 국소 최적해(Local Minima) 함정을 회피합니다.

---

## 🛠️ 주요 클래스

| 클래스명 | 설명 | 비고 |
| :--- | :--- | :--- |
| `MinimizeEstimator` | 수치 최적화 및 베이지안 전역 탐색 통합 추정기 클래스 | 구 `FitMinimizeOptimization` 호환 |

---

## 💡 사용 예시 (Usage Example)

```python
import numpy as np
from unoUtil.models.fitting import MinimizeEstimator
from unoUtil.models.mathematical import TireMagicFormula

# 타겟 모델 함수 지정
estimator = MinimizeEstimator(ModelFunction=TireMagicFormula, disp=False)

# 최적 파라미터 탐색 및 피팅
# estimator.fitWithParams(...)
```
