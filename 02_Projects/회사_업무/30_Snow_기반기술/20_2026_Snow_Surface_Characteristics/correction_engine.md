# ❄️ correction_engine.py 로컬 개발 매뉴얼

이 모듈은 차분법(Difference Method) 기반 머신러닝 스노우 제동 성능 보정 모델을 학습하고 검증하며, 다양한 환경 조건 변화량에 대한 제동거리 영향도 예측 및 실측 제동거리 일괄 정규화 보정을 담당하는 클래스입니다.

---

## 🏛️ 1. API 명세 및 상세 설계

### 1.1 `calc_difference_dataset(df_combined, feature_cols, target_col, ...)`
동일한 의뢰번호 및 타이어 세트 내의 1차 vs 2차 반복 평가 데이터 간 차분(Delta)을 구해, 타이어 고유 성질(컴파운드, 패턴)의 영향은 $0$으로 소거하고 순수하게 환경 변화와 제동거리 변화 간의 전달 함수만을 추출한 차분 데이터셋을 생성합니다.
* **인자**:
  * `df_combined (pd.DataFrame)`: 결합 및 매칭이 완료된 원본 데이터프레임
  * `feature_cols (Optional[List[str]])`: 차분을 적용할 환경 변수 리스트 (기본값: `['char_height', 'cd_test_ah']`)
  * `target_col (str)`: 목표 제동거리 변수명 (기본값: `'char_brk_dist'`)
* **반환값**:
  * `pd.DataFrame`: 타이어 실력이 상쇄된 순수 환경-제동차분 데이터프레임
* **하위 호환성 에일리어스**:
  * `extract_difference_dataset`

### 1.2 `calc_trained_models(df_diff, test_size, n_estimators, max_depth, random_state)`
추출된 차분 데이터셋을 활용하여 다양한 머신러닝 회귀 후보 모델들(Random Forest, KNN, Decision Tree, Ridge/Linear Regression, SVR)을 과적합 깊이 규제 및 하이퍼파라미터 제어를 바탕으로 학습시키고 평가 메트릭($R^2$, MAE, MSE, Adjusted $R^2$)을 반환합니다.
* **인자**:
  * `df_diff (Optional[pd.DataFrame])`: 차분 데이터프레임 (생략 시 내부 캐시 데이터 사용)
* **반환값**:
  * `Dict[str, Dict[str, float]]`: 모델별 검증 통계 지표 사전
* **하위 호환성 에일리어스**:
  * `train_models`

### 1.3 `calc_delta_braking(delta_features, model_name)`
환경 조건의 변화량(Delta)을 바탕으로 예측되는 제동거리 변화량($\Delta\text{BrkDist}$, m)을 산출합니다.
* **인자**:
  * `delta_features (Union[Dict, pd.DataFrame, np.ndarray])`: 환경 편차 정보
* **반환값**:
  * `np.ndarray`: 예측된 제동거리 차이값 (m)
* **하위 호환성 에일리어스**:
  * `predict_delta_braking`

### 1.4 `calc_corrected_braking_distance(raw_dist, current_condition, reference_condition, ...)`
단일 제동 시험 건의 실측 제동거리를 기준 정규화 노면/기상 조건으로 정규화 보정한 제동거리를 산출합니다.
* **보정식**: $D_{\text{corr}} = D_{\text{raw}} - \Delta D_{\text{pred}}(\text{Current} - \text{Reference})$
* **하위 호환성 에일리어스**:
  * `correct_braking_distance`

### 1.5 `calc_corrected_dataframe(df, reference_condition, raw_dist_col, out_col, ...)`
전체 제동 데이터프레임의 제동거리 데이터 전체에 대해 일괄 보정을 처리하고 신규 컬럼을 바인딩합니다.
* **하위 호환성 에일리어스**:
  * `correct_dataframe`

### 1.6 `plot_3d_correction_map(model_name, resolution, title, save, close)`
눈 침하 깊이 차이 vs 절대습도 차이에 따라 달라지는 제동거리 변화량($\Delta\text{BrkDist}$)을 3D 등고선 등치선 맵으로 시각화합니다.
* **인자**:
  * `save (Union[bool, str, Path])`: 저장 다형성 제어 파라미터
  * `close (bool)`: 메모리 해제 및 GUI Non-blocking 구동 여부 (기본값: `True`)
* **반환값**:
  * `Tuple[plt.Figure, plt.Axes]`

---

## 💻 2. 실무 활용 예제

```python
import pandas as pd
from Snow_braking_relate_condition.correction_engine import SnowCorrectionEngine

# 1. 보정 엔진 초기화
engine = SnowCorrectionEngine(primary_model_name='Random Forest')

# 2. 결합 데이터셋으로부터 차분 데이터 추출 및 머신러닝 학습
df_combined = pd.read_pickle("./df_combined.pkl")
df_diff = engine.calc_difference_dataset(df_combined)
metrics = engine.calc_trained_models(df_diff)

# 3. 기준 환경 세팅 및 일괄 노이즈 걷어내기(보정)
engine.set_reference_conditions({'char_height': 3.0, 'cd_test_ah': 1.5})
df_corrected = engine.calc_corrected_dataframe(df_combined, out_col='char_brk_dist_corr')

# 4. 차분 보정 등고선 맵 작성 및 저장
fig, ax = engine.plot_3d_correction_map(
    model_name='KNN Regressor',
    save=True,  # 사내 기본 첨부 저장소에 저장
    close=True  # 자원 해제
)
```
