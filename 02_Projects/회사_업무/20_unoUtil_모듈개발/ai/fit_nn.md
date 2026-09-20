---
id: "fit_nn_20260920"
title: "fit_nn (인공신경망 회귀 모델 설계 및 그리드 탐색) 상세 매뉴얼"
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
  - 딥러닝
project_link: "[[unoUtil]]"
---

# 🤖 fit_nn (인공신경망 회귀 모델 설계 및 그리드 탐색) 상세 매뉴얼

> [!ABSTRACT] 📌 개요
> Scikit-Learn과 TensorFlow Keras 프레임워크를 연동하여 완전 연결 신경망(Fully-Connected Neural Network, MLP) 회귀 모듈을 구축하고, 하이퍼파라미터 교차 검증 그리드 탐색(GridSearchCV)을 자동으로 수행하는 정밀 성능 피팅 유틸리티입니다.
> 
> * **상위 대시보드**: [[00_unoUtil_모듈개발_대시보드]]

---

## 1. ⚙️ 주요 API 규격

### 1.1. `create_model(hidden_neurons=12, activation='relu', learning_rate=0.01, beta=0.9)`
* **기능**: Keras Sequential API를 기반으로 2층 MLP 회귀 신경망을 빌드하고 컴파일하여 반환합니다.
* **매개변수**:
  - `hidden_neurons (int)`: 은닉층 Dense 레이어의 뉴런 개수. 기본값 `12`.
  - `activation (str)`: 은닉층 활성화 함수 명칭 (예: `'relu'`).
  - `learning_rate (float)`: Adam 옵티마이저 학습률. 기본값 `0.01`.
  - `beta (float)`: Adam 옵티마이저의 beta_1(모멘텀) 매개변수. 기본값 `0.9`.

### 1.2. `fitNN(x, y, hidden_neurons=12, test_size=0.2, ...)`
* **기능**: 독립 변수 `x`와 종속 변수 `y`를 훈련/검증 셋으로 분할한 후 KerasRegressor 객체로 래핑하여 하이퍼파라미터 조합 탐색을 시행합니다.
* **매개변수**:
  - `x (np.ndarray)`: 입력 독립 피처 행렬 데이터.
  - `y (np.ndarray)`: 실제 측정 타겟 값 벡터 데이터.
  - `test_size (float)`: 검증용 테스트 데이터의 비율 (0.0~1.0). 기본값 `0.2`.
  - `plot (bool)`: 피팅 완료 후 테스트 셋 오버레이 비교 차트 시각화 활성화 여부.
  - `save (str | Path | bool, optional)`: 시각화 플롯 파일 디렉토리 또는 전체 경로 및 다형성 활성화 여부.
  - `close (bool)`: 플롯 메모리 즉시 반환 여부 (시각화 무중단 원칙 기본값 `True`).
  - `**kwargs (Any)`: 구버전 레거시 매핑 연동 (`x_data`, `y_data`, `flag_plot` 자동 위임 흡수).
* **반환값**: 최적 적합 탐색이 완료된 KerasRegressor 최적 추정 모델(`grid_search_result.best_estimator_`).
* **하위 호환 별칭**: `fit_nn`

---

## 💻 2. 호출 예제 (Usage Example)

```python
import numpy as np
from unoUtil.ai.fit_nn import fitNN, fit_nn

# 1. 가상 마찰계수 비선형 Mock 주행 계측 데이터 생성
x = np.linspace(-2.0, 2.0, 100).reshape(-1, 1)
y = 3.5 * (x ** 2) - 1.2 * x + np.random.normal(0, 0.1, len(x))

# 2. 인공신경망 그리드 최적화 모델 피팅 수행 (TensorFlow 설치 환경에서만 가동)
try:
    best_estimator = fitNN(
        x=x,
        y=y,
        hidden_neurons=24,
        test_size=0.15,
        plot=True,
        save=True,  # DEFAULT_SAVE_DIR 디렉토리에 자동 차트 저장
        close=True
    )
    print("모델 피팅 최적화 성공!")
except ImportError as e:
    print(f"TensorFlow 부재로 가동이 차단되었습니다: {e}")
```

---

## 3. 📝 이중 동기화 프로토콜 준수사항
- 이 매뉴얼 파일(`fit_nn.md`)은 동일 로컬 디렉터리(`unoUtil/ai/`) 내에 1:1 대응하여 보관되며, 최종 작업 완료 선언 시 옵시디언 볼트로 일괄 배치 동기화 처리됩니다.
