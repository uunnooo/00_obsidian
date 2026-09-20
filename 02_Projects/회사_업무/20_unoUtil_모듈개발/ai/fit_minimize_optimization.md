---
id: "fit_minimize_optimization_20260920"
title: "fit_minimize_optimization (통합 비선형 최적화 추정 엔진) 상세 매뉴얼"
type: resource
category_main: 회사_업무
category_sub: 개발매뉴얼
date: 2026-09-20
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - 매뉴얼
  - AI
  - 기계학습
  - 최적화
  - Bayesian
project_link: "[[unoUtil]]"
---

# 🏗️ fit_minimize_optimization (통합 비선형 최적화 추정 엔진) 상세 매뉴얼

> [!ABSTRACT] 📌 개요
> Scipy minimize(동역학 수치 최소화) 및 Scikit-Optimize 베이지안 최적화(Gaussian Process) 알고리즘을 유기적으로 래핑하여, 비선형 거동 및 3자유도 강성 계수를 정밀 역산출해 내는 Scikit-Learn 스타일의 고성능 최적화 추정기(MinimizeEstimator) 클래스 모듈입니다.
> 
> * **상위 대시보드**: [[00_unoUtil_모듈개발_대시보드]]

---

## 1. ⚙️ 코어 아키텍처 및 최소화 원리

비선형 최적화는 초기 초깃값 선택에 따라 지역 극소점(Local Minima)에 갇히는 고질적인 문제(수렴 실패)가 발생합니다.  
본 모듈은 이 문제를 타파하기 위해 **초기 탐색용 3대 지능형 튜닝 알고리즘**을 완전히 내장하고 있습니다:

1. **그리드 서치 (`fitWithGrid`)**: 지정 범위 내의 모든 이산 격점 조합을 연산 (가장 안전하나 대용량 시 병목 발생).
2. **랜덤 서치 (`fitWithRandom`)**: 무작위 범위 샘플링을 통한 파라미터 조합 연산 (고속 탐색 강점).
3. **베이지안 최적화 (`fitWithBayesian`)**: 가우시안 프로세스(Gaussian Process, GP)로 오차 감소 방향을 확률적으로 예측 수립하며 최단 시간에 전역 최적해(Global Optima)로 수렴.

---

## 2. ⚙️ 주요 API 및 메서드 명세

### `MinimizeEstimator(ModelFunction, params=None, ...)`
* **기능**: 타겟 수학 모델과 추정기를 바인딩하여 목적 비용 객체를 생성합니다.

#### 주요 메서드:
* **`fitWithParams(X, Y, Params, ...)`**: 수동 초깃값 `Params`를 사용해 즉각 최적화를 개시하고 오버레이 예측 플롯을 도출합니다.
* **`fitWithGrid(X, Y, param_list, ...)`**: 다차원 격점 병렬 스레드 풀 연산으로 구득한 최적 초깃값으로부터 최종 scipy 최적화를 수행합니다.
* **`fitWithRandom(X, Y, param_list, n_iter=20, ...)`**: 무작위 추출 병렬 수치 연산으로 초깃값을 구한 후 최종 최적화를 수행합니다.
* **`fitWithBayesian(X, Y, param_bounds, n_calls=20, ...)`**: 베이지안 최적화 연동을 기동하여 최단 에포크 내 전역 최적 계수를 도출하고, Convergence 오차 수렴 감쇠 그래프를 출력합니다.
* **`inverse(Y) -> np.ndarray`**: 최적화 수립된 계수를 바탕으로 특정 목적값 `Y`를 충족하기 위해 필요한 입력값 `X`를 고속 역산(`scipy.optimize.fsolve` 비선형 연립식 기법)합니다.
* **`predict(X) -> np.ndarray`**: 수렴 계수를 모델 수식에 대입하여 추정값 벡터를 연산합니다.

---

## 💻 3. 호출 예제 (Usage Example)

```python
import numpy as np
from skopt.space import Real
from unoUtil.ai.fit_minimize_optimization import MinimizeEstimator
from unoUtil.ai.dynamic_model import tire_magic_formula

# 1. 독립 변수 및 실제 측정된 마찰력 준비
x_slip = np.linspace(0.0, 0.25, 50)
y_actual_force = tire_magic_formula([11.5, 1.65, 1.1, 0.1], x_slip) + np.random.normal(0, 0.01, len(x_slip))

# 2. 타이어 수식과 함께 추정기 싱글톤 초기화
estimator = MinimizeEstimator(ModelFunction=tire_magic_formula)

# 3. 베이지안 탐색 상하한 규격 수립
# 각 파라미터 영역 정의: [Bx, Cx, Dx, Ex]
bounds = [Real(1.0, 15.0), Real(1.0, 2.0), Real(0.5, 1.5), Real(-0.2, 0.5)]

# 4. 베이지안 최적화 가동 및 최종 피팅 완료
best_params, rss_error, fit_x, fit_y = estimator.fitWithBayesian(
    X=x_slip,
    Y=y_actual_force,
    param_bounds=bounds,
    n_calls=15,
    n_jobs=4,
    plot=True,
    save=True,  # 차트 이미지 물리 디스크 자동 저장
    close=True
)

print(f"최종 수렴 완료된 최적 파라미터 조합: {best_params}")
print(f"오차 제곱합(RSS): {rss_error:.6f}")

# 5. 역추정(Inverse) 수행: 0.8g 제동력을 생성하기 위해 필요한 타이어 슬립율 역산
target_g = 0.8
req_slip = estimator.inverse(target_g)
print(f"목표 제동력 {target_g}g 도달을 위해 도출된 필요 슬립율: {req_slip[0]:.4f}")
```

---

## 4. 📝 이중 동기화 프로토콜 준수사항
- 이 매뉴얼 파일(`fit_minimize_optimization.md`)은 동일 로컬 디렉터리(`unoUtil/ai/`) 내에 1:1 대응하여 보관되며, 최종 작업 완료 선언 시 옵시디언 볼트로 일괄 배치 동기화 처리됩니다.
