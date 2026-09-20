# 🧭 ExtendedIsolationForest 이상치 필터링 엔진 매뉴얼 (extended_isolation_forest.md)

## 📌 1. 개요 및 목적 (Overview)
`extended_isolation_forest` 모듈은 실차 주행 및 데이터 전처리 단계에서 고주파 계측 센서 노이즈, 통신 음영 튀는 값, 그리고 비이상적인 운전자 조작 데이터를 정교하게 색출하기 위한 **확장 아일레이션 포레스트(Extended Isolation Forest, EIF) 다변량 이상치(Anomaly) 탐지 엔진**을 제공합니다.

기존의 표준 Isolation Forest 알고리즘은 변수의 직교 축을 기준으로만 무작위 분할을 수행하기 때문에, 데이터가 사선 방향이나 구형으로 뭉쳐 있을 때 가짜 전단 경계면이 발생하는 심각한 **'그물망 노이즈(Artifact)'** 문제를 지니고 있었습니다. 
본 모듈은 임의의 무작위 법선 벡터를 지닌 **초평면(Hyperplane) 분할 기법**을 적용하여 이 문제를 원천 해결하였으며, 10만 포인트 이상의 가감속/제동 이상치 데이터를 다차원 공간 상에서 왜곡 없이 탐지해 냅니다.

---

## 🛠️ 2. 핵심 API 명세 (API Specifications)

### 2.1. `ExtendedIsolationForest` 클래스 인터페이스

| 메서드명 | 타입 | 설명 |
| :--- | :---: | :--- |
| `__init__(n_estimators, max_samples, contamination, random_state)` | 생성자 | 트리 개수, 샘플 수, 이상치 오염 비율 및 일관된 시드 번호를 통해 EIF 트리 모델 초기화 |
| `fit(arr_input_x)` | `Method` | 다차원 초평면 무작위 분할을 통해 다수의 EIF 의사결정 트리 군을 자율 학습하여 빌드 |
| `_build_tree(arr_x, int_current_depth)` | 비공개 Method | 재귀적 구조 분할을 통해 무작위 경사 초평면 기반 단일 격리 트리 형성 |
| `_path_length(arr_row, dict_tree, int_depth)` | 비공개 Method | 입력된 데이터 행이 단말 노드에 고립될 때까지 거치는 평균 탐색 경로 길이 산출 |
| `decision_function(arr_x)` | `Method` | 데이터가 고립되기 쉬운 정도를 0~1 사이의 이상치 스코어(Anomaly Score)로 환산하여 반환 (1에 가까울수록 이상치) |
| `predict(arr_x)` | `Method` | 오염 임계치(`contamination`)에 따른 정량 이진 분류 실행 (이상치는 `-1`, 정상치는 `1`로 매핑하여 반환) |
| `plot()` | `Method` | 2차원 공간 상에 이상치 스코어의 전역 등고선(Contour Map)과 타점을 비블로킹 시각화 렌더링 |

---

## 📋 3. 입력 파라미터 상세 정의 (Arguments)

1. **`n_estimators` (`int` - 선택, 기본값: `100`)**:
   - 격리할 의사결정 트리의 개수입니다. 트리가 많아질수록 이상치 경계면이 부드러워지고 정확해집니다.
2. **`contamination` (`float` - 선택, 기본값: `0.05`)**:
   - 전체 데이터셋에서 존재할 것으로 예상되는 이상치의 정량적 비율(오염도, 0~0.5 사이)입니다.
3. **`max_samples` (`Union[int, float]` - 선택, 기본값: `'auto'`)**:
   - 개별 트리를 학습할 때 무작위 복원 추출할 서브 샘플의 개수입니다.

---

## 💻 4. 실무 활용 예제 (Multi-case Examples)

### 4.1. [시나리오 1] 주행 중 튀는 속도(Velocity) 센서 이상치 고속 탐지 및 predict
```python
import numpy as np
import pandas as pd
from unoUtil.signal_process.post_process.extended_isolation_forest import ExtendedIsolationForest

# 1. 2차원 속도-가속도 계측 데이터 가상 생성 및 튀는 노이즈 주입
np.random.seed(42)
normal_data = np.random.normal(size=(500, 2))
anomalies = np.random.uniform(low=-4, high=4, size=(20, 2))  # 임의 아웃라이어
X = np.vstack([normal_data, anomalies])

# 2. EIF 엔진 기동 및 학습
eif = ExtendedIsolationForest(n_estimators=100, contamination=0.04, random_state=42)
eif.fit(X)

# 3. 이상치 판정 수행
predictions = eif.predict(X)  # Normal = 1, Anomaly = -1
print(f"🎯 탐지된 총 이상치 포인트 수: {np.sum(predictions == -1)}개")
```

### 4.2. [시나리오 2] 의사결정 함수(decision_function)를 활용한 타점별 이상치 스코어 정밀 검수
```python
# 각 데이터별 정량적 고립도 스코어 계산
anomaly_scores = eif.decision_function(X)

# 스코어가 가장 높은 상위 5개 위험 타점 추출
top_danger_indices = np.argsort(anomaly_scores)[-5:]
print(f"🚨 최상위 위험 타점 번호: {top_danger_indices}")
print(f"📉 해당 타점들의 이상치 스코어: {anomaly_scores[top_danger_indices]}")
```

### 4.3. [시나리오 3] 이상치 전역 분포 등고선 맵 시각화 및 무중단 저장
```python
# 내장된 plot 메서드를 기동하여 무중단 2D 등고선 컬러맵 생성
eif.plot()

# matplotlib Non-blocking 수동 해제 파이프라인
import matplotlib.pyplot as plt
fig = plt.gcf()
fig.savefig("./test_output/eif_anomaly_contour.png", dpi=200, bbox_inches='tight')
plt.close(fig)  # 백그라운드 메모리 즉시 회수

print("💾 이상치 바운딩 등고선 맵 저장이 완벽하게 완료되었습니다.")
```
