# 📘 SnowCorrectionModel (스노우 노면 환경 차분 머신러닝 보정 엔진)

## 📌 개요
`SnowCorrectionModel`은 동일 타이어 1차(Ref) vs 2차(Corr) 반복 평가 간의 환경 인자(노면 침하 깊이, 표면 온도, 대기 절대습도 등 자유로운 N개 인자 리스트)와 목표 성능 인자(실측 제동거리 등) 간의 차분($\Delta$) 상관관계를 6대 머신러닝 회귀 알고리즘으로 학습하고, 임의의 시험 데이터를 기준 환경 또는 1차 시험 수준으로 정규화 보정하는 다변량 머신러닝 코어 엔진입니다.

동적 특성 인자 리스트(`x_cols: List[str]`), 목표 인자(`y_col: str`), 그리고 실측 센서 데이터 결측치(`NaN`) 자동 드롭 및 All NaN 안전 가드(`missing_strategy='drop'`)가 내장되어 있어, 실험 조건 및 센서 조합이 바뀌어도 코드 수정 없이 유연하게 적응합니다.

**컴포지션 패턴(Composition Pattern)**에 따라 수치 정량 검증기(`self.validator = SnowCorrectionValidator`)와 시각화 플로터(`self.plot = SnowCorrectionPlotter`)를 합성 장착하여 단일 객체에서도 직관적으로 모든 기능을 위임 호출할 수 있습니다.

---

## 🏛️ 아키텍처 및 책임 분리

```
                    ┌───────────────────────────────┐
                    │      SnowCorrectionModel      │
                    │   (Core Engine: ML & Corr)    │
                    │   - x_cols: List[str] (N-dim) │
                    │   - y_col: str                │
                    │   - missing_strategy='drop'   │
                    └───────┬───────────────┬───────┘
                            │               │
             .validator ┌───▼───┐       ┌───▼───┐ .plot
                        │Validator│     │Plotter│
                        └───────┘       └───────┘
```

1. **`SnowCorrectionModel`**: N개 특성 인자 리스트 기반 차분 데이터셋 생성, 결측치 자동 필터링, 6종 ML 회귀 학습, 다형성 예측(`predict_delta`), 데이터프레임 일괄 보정, 모델 영속화(Joblib).
2. **`SnowCorrectionValidator`**: 1차 vs 2차 정밀 대조표 산출, 오차 축소율(Error Reduction, %) 수치 분석.
3. **`SnowCorrectionPlotter`**: Figure 1(차분 산점도), Figure 2(복원율 산점도), Figure 3(등고선 보정 맵), 편차 바차트 등 그래픽 렌더링 (축 라벨 및 범례가 `x_cols`, `y_col`에 따라 동적 자동 반영).

---

## ⚙️ 주요 API 규격

### 1. `__init__(x_cols=None, y_col='char_brk_dist', target_model='Random Forest', missing_strategy='drop', ...)`
* **인자**:
  * `x_cols (Optional[List[str]])`: 학습에 사용할 입력 특성 인자 컬럼명 리스트 (기본값: `['char_height', 'cd_test_ah']`).
    * 기온, 노면온도, 절대습도 등 임의의 조합 및 3개 이상 피처 전달 가능.
  * `y_col (str)`: 보정 대상 목표 성능 컬럼명 (기본값: `'char_brk_dist'`).
  * `target_model (str)`: 주력 보정 모델명 (기본값: `'Random Forest'`).
  * `missing_strategy (str)`: 결측치 처리 전략 (`'drop'` 기본, NaNs 행 자동 감지 및 제거).

### 2. `calc_difference_dataset(data, ...)`
* **설명**: 동일 의뢰/타이어 1st vs 2nd 반복 시험 간의 환경 및 제동거리 차분($\Delta$) 데이터셋을 Run 평균 매칭 방식으로 구축합니다.
* **보안 & 결측치 처리**: `x_cols`와 `y_col`의 결측치(NaN)를 자동 감지하여 드롭하며, All NaN 컬럼이나 0행 데이터 유입 시 명시적 `ValueError`를 발생시켜 모델 오류를 사전 차단합니다.
* **반환값**: `pd.DataFrame` (차분 데이터셋, 컬럼명: `diff_{col}`)

### 3. `train_models(df_diff=None)`
* **설명**: 6대 회귀 모델(Random Forest, KNN, SVR, Ridge, Lasso, ElasticNet)을 동시 학습하고 결정계수($R^2$), MAE, RMSE 지표를 산출하여 최적 모델을 자동 선정합니다.
* **반환값**: `Dict[str, Dict[str, float]]` (모델별 평가 지표)

### 4. `predict_delta(*args, **kwargs)`
* **설명**: 임의의 환경 인자 변화량($\Delta X$)에 대응하는 성능 변화량($\Delta Y$)을 유연하게 예측합니다.
* **다형성 지원**:
  * 스칼라 순서 전달: `model.predict_delta(1.2, -0.3)`
  * 딕셔너리 전달: `model.predict_delta({'char_height': 1.2, 'cd_test_ah': -0.3})`
  * 1D / 2D NumPy 배열: `model.predict_delta(np.array([[1.2, -0.3]]))`
  * Pandas DataFrame: `model.predict_delta(df_diff[['diff_char_height', 'diff_cd_test_ah']])`
* **반환값**: `float` 또는 `np.ndarray`

### 5. `correct_dataframe(data, out_col='char_brk_dist_corr', reference_condition=None)`
* **설명**: 제동 데이터프레임의 성능 수치를 학습된 모델을 통해 환경 보정합니다.
  * 기준 환경(`reference_condition`) 지정 시: 해당 환경 기준으로 전체 일괄 정규화.
  * 미지정 시: 각 의뢰/타이어별 1차 시험 환경을 기준으로 2차 시험 제동거리를 상대 차감 보정.
* **반환값**: `pd.DataFrame`

---

## 💻 사용 예시

### 예시 1: 커스텀 환경 인자 리스트 (기온, 절대습도) 및 결측치 방어
```python
from unoUtil.snow_condition import SnowCorrectionModel

# 1. 기온과 절대습도를 X 인자로 설정
model = SnowCorrectionModel(
    x_cols=['cd_test_temp', 'cd_test_ah'],
    y_col='char_brk_dist',
    missing_strategy='drop'
)

# 2. 차분 데이터셋 생성 (결측치 자동 드롭) 및 학습
df_diff = model.calc_difference_dataset(df_raw)
metrics = model.train_models(df_diff)

# 3. 보정 적용 및 검증
df_corrected = model.correct_dataframe(df_raw)
df_comp = model.validator.calc_corrected_comparison_table(df_corrected)

# 4. 시각화 (축 라벨에 cd_test_temp, cd_test_ah 자동 반영)
model.plot.plot_delta_prediction_scatter(df_diff, close=True)
model.plot.plot_correction_map(close=True)
```

### 예시 2: 3개 이상 피처 (다변량) 확장
```python
# 노면 침하 깊이, 노면 온도, 대기 절대습도 3대 인자 동시 반영
model_3d = SnowCorrectionModel(
    x_cols=['char_height', 'char_temp', 'cd_test_ah'],
    y_col='char_brk_dist'
)
df_diff_3d = model_3d.calc_difference_dataset(df_raw)
model_3d.train_models(df_diff_3d)

# 3개 인자 다형성 예측
delta_dist = model_3d.predict_delta(2.0, -1.5, 0.4)
```
