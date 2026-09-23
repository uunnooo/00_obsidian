# ❄️ correction_engine.py 로컬 개발 매뉴얼

이 모듈은 차분법(Difference Method) 기반 머신러닝 스노우 제동 성능 보정 모델을 학습하고 검증하며, 다양한 환경 조건 변화량에 대한 제동거리 영향도 예측, 실측 제동거리 일괄 정규화 보정, 그리고 종합 대조 데이터 테이블 생성 및 핵심 검증 시각화(4대 차트) 생성을 전담하는 핵심 엔진 클래스입니다.

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

### 1.2 `train_models(df_diff, test_size, model_params=None, auto_tune=False, cv=5, ...)`
추출된 차분 데이터셋을 활용하여 다양한 머신러닝 회귀 후보 모델들(Random Forest, KNN, Decision Tree, Ridge/Linear Regression, SVR)을 과적합 규제 및 하이퍼파라미터 제어를 바탕으로 학습시키고 평가 메트릭($R^2$, MAE, MSE, Adjusted $R^2$)을 산출합니다.
* **인자**:
  * `df_diff (Optional[pd.DataFrame])`: 차분 데이터프레임 (생략 시 내부 캐시 데이터 사용)
  * `model_params (Optional[Dict[str, Any]])`: 특정 모델에 직접 주입할 수동 하이퍼파라미터 딕셔너리
  * `auto_tune (bool)`: 5-Fold 교차검증(`GridSearchCV`)을 가동하여 각 모델의 최적 하이퍼파라미터를 자동 탐색 (기본값: `False`)
  * `cv (int)`: 교차검증 Fold 수 (기본값: `5`)
* **반환값**:
  * `Dict[str, Dict[str, float]]`: 모델별 검증 통계 지표 사전

### 1.3 `calc_corrected_comparison_table(df, model_name, feature_cols, target_col, save, ...)`
의뢰번호, 타이어 세트별 1st와 2nd 시험의 원래 제동거리, 보정 제동거리, 예측 변화량, 기상/노면 환경 요인을 종합 대조하는 분석 데이터프레임을 생성 및 다형성 저장합니다.
* **비즈니스 로직**:
  * **1st 시험**: 베이스라인 기준이므로 원래 제동거리를 그대로 유지 ($D_{\text{corr}} = D_{\text{raw}}$, $\Delta D_{\text{pred}} = 0$)
  * **2nd 시험**: 환경 차분에 따른 모델 예측 델타를 반영하여 1st 기준 상태로 정규화 ($D_{\text{corr}} = D_{\text{raw}} - \Delta D_{\text{pred}}$)
  * 1st만 단독 존재하는 시험 건도 누락 없이 수록하여 전수 추적성 보장
* **인자**:
  * `df (Optional[pd.DataFrame])`: 분석 대상 통합 데이터프레임
  * `model_name (Optional[str])`: 차분 예측 모델명 (기본값: 대표 모델)
  * `save (Union[bool, str, Path])`: 저장 다형성 제어 (`.xlsx`, `.csv`, `.pkl` 자동 판별)
* **반환값**:
  * `pd.DataFrame`: 의뢰번호, 세트, run, 원래_제동거리(m), 보정_제동거리(m), 예측변화량(m), 환경인자 등으로 구성된 대조 테이블

### 1.4 `plot_delta_prediction_scatter(df_diff, model_name, title, save, close)`
차분 예측 모델의 학습 적합도를 실측 제동거리 차분치 vs 예측 차분치($y=x$ 기준선) 산점도로 검증 시각화합니다. (검증 슬라이드 Figure 1)

### 1.5 `plot_delta_braking_bar(df_diff, title, save, close)`
동일 타이어의 반복 시험 간 제동거리 차이($\Delta\text{BrkDist} = \text{2nd} - \text{1st}$)를 타이어 세트별 막대 그래프(양수: Crimson, 음수: DodgerBlue)로 시각화합니다.

### 1.6 `plot_scatter_restoration(df, model_name, title, save, close)`
1차(Reference) vs 2차(Actual: 빨강 / Corrected: 파랑) 제동거리 산점도 및 Adjusted $R^2$ 복원 성능을 시각화합니다. (검증 슬라이드 Figure 2)

### 1.7 `plot_3d_correction_map(model_name, shift_min_zero, resolution, ...)`
환경 인자 변화량에 따른 제동거리 변화량 2D 등고선 보정 맵을 생성합니다. (검증 슬라이드 Figure 3, 슬라이드 6번 표준)
* **표준 사양**:
  * X(눈 눌림 깊이), Y(절대습도) 최솟값을 0으로 일치 (`shift_min_zero=True`)
  * Z(제동거리 변화량)는 음수~양수 실측 원시 차분 유지
  * 10x10 격자 상 KNN 거리 가중치 3차원 보간
  * 컬러바 눈금 1단위 정수, 등고선 3단계(`[-1.0, 0.0, 1.0]`) 정수 라벨링

### 1.8 `plot_tire_subsets_comparison(df, req_no, model_name, save, close)`
특정 의뢰서 내 주요 타이어 세트(C1, C2, T1, T2)별 실측치(Raw 1st, 2nd)와 환경 차분 예측치(Predict 2nd)를 2x2 서브플롯으로 비교 시각화합니다. (검증 슬라이드 Figure 4)

---

## 💻 2. 실무 활용 예제

```python
from pathlib import Path
import pandas as pd
from Snow_braking_relate_condition.correction_engine import SnowCorrectionEngine

# 1. 보정 엔진 초기화 및 데이터 준비
engine = SnowCorrectionEngine(primary_model_name='Random Forest')
df_combined = pd.read_pickle("1. df_combine_test_surface_spec.pkl")

# 2. 차분 데이터 추출 및 다중 모델 학습
df_diff = engine.calc_difference_dataset(df_combined)
metrics = engine.train_models(df_diff)

# 3. 보정 대조 종합 데이터 테이블 생성 및 엑셀 저장
df_table = engine.calc_corrected_comparison_table(
    df=df_combined,
    save=Path("./output/corrected_comparison_table.xlsx")
)

# 4. 핵심 검증 차트 생성 및 Non-blocking 저장
engine.plot_delta_prediction_scatter(save=True, close=True)
engine.plot_scatter_restoration(df=df_combined, save=True, close=True)
engine.plot_3d_correction_map(model_name='KNN Regressor', shift_min_zero=True, save=True, close=True)
engine.plot_tire_subsets_comparison(df=df_combined, req_no='25RD110006EF', save=True, close=True)
```
