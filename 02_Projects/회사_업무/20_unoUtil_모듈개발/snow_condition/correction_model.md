# 📘 SnowCorrectionModel (스노우 노면 환경 차분 머신러닝 보정 엔진)

## 📌 개요
`SnowCorrectionModel`은 동일 타이어 1차(Ref) vs 2차(Corr) 반복 평가 간의 환경 인자(노면 침하 깊이 차분 $\Delta\text{Height}$, 대기 절대습도 차분 $\Delta\text{AH}$)와 실측 제동거리 차분($\Delta\text{BrkDist}$) 간의 상관관계를 6대 머신러닝 회귀 알고리즘으로 학습하고, 임의의 시험 데이터를 기준 환경 또는 1차 시험 수준으로 정규화 보정하는 코어 엔진입니다.

**컴포지션 패턴(Composition Pattern)**에 따라 수치 정량 검증기(`self.validator = SnowCorrectionValidator`)와 시각화 플로터(`self.plot = SnowCorrectionPlotter`)를 합성 장착하여 단일 객체에서도 직관적으로 모든 기능을 위임 호출할 수 있습니다.

---

## 🏛️ 아키텍처 및 책임 분리

```
                    ┌───────────────────────────────┐
                    │      SnowCorrectionModel      │
                    │   (Core Engine: ML & Corr)    │
                    └───────┬───────────────┬───────┘
                            │               │
             .validator ┌───▼───┐       ┌───▼───┐ .plot
                        │Validator│     │Plotter│
                        └───────┘       └───────┘
```

1. **`SnowCorrectionModel`**: 차분 데이터셋 생성, 6종 ML 회귀 학습, 예측, 데이터프레임 일괄 보정, 모델 영속화(Joblib).
2. **`SnowCorrectionValidator`**: 1차 vs 2차 정밀 대조표 산출, 오차 축소율(Error Reduction, %) 수치 분석.
3. **`SnowCorrectionPlotter`**: Figure 1(차분 산점도), Figure 2(복원율 산점도), Figure 3(등고선 보정 맵), 편차 바차트 등 그래픽 렌더링.

---

## ⚙️ 주요 API 규격

### 1. `calc_difference_dataset(data, ...)`
* **설명**: 동일 의뢰/타이어 1st vs 2nd 반복 시험 간의 환경 및 제동거리 차분($\Delta$) 데이터셋을 Run 평균 매칭 방식으로 구축합니다.
* **반환값**: `pd.DataFrame` (차분 데이터셋)

### 2. `train_models(df_diff=None)`
* **설명**: 6대 회귀 모델(Random Forest, KNN, SVR, Ridge, Lasso, ElasticNet)을 동시 학습하고 결정계수($R^2$), MAE, RMSE 지표를 산출하여 최적 모델을 자동 선정합니다.
* **반환값**: `Dict[str, Dict[str, float]]` (모델별 평가 지표)

### 3. `correct_dataframe(data, out_col='char_brk_dist_corr', reference_condition=None)`
* **설명**: 제동 데이터프레임의 제동거리를 학습된 모델을 통해 환경 보정합니다.
  * 기준 환경(`reference_condition`) 지정 시: 해당 환경 기준으로 전체 일괄 정규화.
  * 미지정 시: 각 의뢰/타이어별 1차 시험 환경을 기준으로 2차 시험 제동거리를 상대 차감 보정.
* **반환값**: `pd.DataFrame`

---

## 💻 사용 예시 (컴포지션 패턴)

```python
from unoUtil.snow_condition import SnowCorrectionModel

# 1. 모델 인스턴스화
model = SnowCorrectionModel()

# 2. 차분 데이터셋 구축 및 모델 학습
df_diff = model.calc_difference_dataset(df_raw)
metrics = model.train_models(df_diff)

# 3. 보정 적용
df_corrected = model.correct_dataframe(df_raw)

# 4. 검증기 네임스페이스 접근 (Validator)
df_comp = model.validator.calc_corrected_comparison_table(df_corrected)

# 5. 플로터 네임스페이스 접근 (Plotter)
model.plot.plot_delta_prediction_scatter(df_diff, close=True)
model.plot.plot_scatter_restoration(df_comp, close=True)
model.plot.plot_correction_map(close=True)
```
