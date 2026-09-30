# 📈 snow_condition.correction_model 기술 매뉴얼

이 문서는 스노우 실차 제동 평가에서 동일 타이어 반복 평가 간에 발생하는 노면 눈 침하량($\Delta H$) 및 대기 절대습도($\Delta \text{AH}$) 편차에 따른 제동거리 변화량($\Delta D$)을 머신러닝으로 정밀 학습하고, 3D 등고선 보정 맵을 시각화하는 **`SnowCorrectionModel`** 모듈의 명세 및 사용법을 정의합니다.

---

## 1. 📌 핵심 개요

자연 환경에서 수행되는 눈길 제동 평가는 시험이 진행됨에 따라 트랙이 지속적으로 다져져 눈 침하 깊이가 얕아지거나 기온/습도 변화로 인해 마찰력이 변동합니다. `SnowCorrectionModel`은 동일 의뢰/타이어 세트의 1차(Ref)와 2차(Corr) 시험 간의 차분($\Delta$) 데이터를 추출하여, 순수 환경 변화에 의한 제동거리 변동분을 6대 회귀 머신러닝(RF, KNN, SVR, Ridge, Lasso, ElasticNet)으로 학습하고, 2차 시험 제동거리를 1차 기준 환경으로 완벽히 차감 보정합니다.

---

## 2. 🛠️ 핵심 클래스 및 API

### `SnowCorrectionModel` (구 `SnowCorrectionEngine`)

| 메서드명 | 역할 | 주요 인자 | 반환값 |
| :--- | :--- | :--- | :--- |
| `calc_difference_dataset(data)` | 동일 타이어 1차/2차 반복 시험 간의 환경 및 제동거리 차분($\Delta$) 데이터셋 구축 | `data: pd.DataFrame` | `pd.DataFrame` (차분 데이터프레임) |
| `train_models(df_diff=None)` | 6종 머신러닝 모델을 학습하고 $R^2$, MAE, RMSE 지표를 산출하여 최적 모델 선정 | `df_diff: Optional[pd.DataFrame]` | `Dict[str, Dict[str, float]]` (평가지표) |
| `set_reference_conditions(conditions)` | 보정에 적용할 기준 환경 프로파일(노면 깊이, 절대습도 등) 등록 | `conditions: Dict[str, float]` | `None` |
| `predict_delta(diff_height, diff_ah)` | 특정 노면 침하차 및 절대습도차에 따른 제동거리 변화량($\Delta D$) 예측 | `diff_height`, `diff_ah` | `Union[float, np.ndarray]` |
| `correct_dataframe(data, reference_condition=...)` | 기준 환경 기반 일괄 정규화 또는 1st 대비 2nd 상대 환경 차분 차감 보정 | `data`, `reference_condition`, `out_col` | `pd.DataFrame` (`char_brk_dist_corr` 추가) |
| `plot_model_comparison(save=False)` | 모델별 $R^2$ 및 MAE 성능 비교 바차트 시각화 | `save`, `close` | `Tuple[plt.Figure, Any]` |
| `plot_correction_map(save=False)` | $\Delta H$ vs $\Delta \text{AH}$에 따른 $\Delta D$ 3D/2D 등고선 보정 맵 시각화 | `x_range`, `y_range`, `shift_min_zero`, `save`, `close` | `Tuple[plt.Figure, plt.Axes]` |
| `save_models()`, `load_models()` | 학습된 모델 및 평가지표의 pkl/joblib 영구 저장 및 복원 | `save_dir`, `filepath` | `Path`, `bool` |

---

## 3. 💡 실무 사용 예제

```python
import pandas as pd
from snow_condition.correction_model import SnowCorrectionModel

# 1. 모델 인스턴스 초기화
engine = SnowCorrectionModel()

# 2. 통합 제동 데이터로부터 차분(Delta) 데이터셋 구축
df_diff = engine.calc_difference_dataset(df_combined)

# 3. 6종 머신러닝 모델 학습 및 최적 모델 자동 선정
metrics = engine.train_models()
print(f"최적 선정 모델: {engine.best_model_name} (R²={metrics[engine.best_model_name]['r2']:.4f})")

# 4. 3D 등고선 보정 맵 시각화
fig, ax = engine.plot_correction_map(save="./reports/correction_map.png", close=True)

# 5. 전체 데이터셋 환경 편차 보정 적용
df_corrected = engine.correct_dataframe(df_combined)
print(df_corrected[['infor_TIRE_SET', 'test_order', 'char_brk_dist', 'char_brk_dist_corr']].head())
```
