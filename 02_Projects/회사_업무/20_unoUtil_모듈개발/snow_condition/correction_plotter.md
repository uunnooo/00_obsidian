# 📘 SnowCorrectionPlotter (스노우 보정 모델 시각화 전담 플로터)

## 📌 개요
`SnowCorrectionPlotter`는 스노우 노면 환경 보정 모델의 검증 그래픽 시각화를 전담하는 클래스입니다.
`SnowCorrectionModel`의 동적 특성 인자 리스트(`x_cols`) 및 목표 인자(`y_col`)와 유기적으로 연동되어, 축 라벨, 범례, 타이틀 및 컬러바를 전달된 컬럼명에 맞추어 100% 동적으로 자동 렌더링합니다.

보고서 및 논문 규격의 4대 핵심 차트(Figure 1, Figure 2, Figure 3, Figure 4)와 편차 바차트, 잔차 의존성 소거 산점도를 생성합니다.

---

## ⚙️ 주요 차트 렌더링 메서드

### 1. `plot_delta_prediction_scatter(df_diff=None, model_name=None, save=False, close=True)`
* **차트**: [Figure 1] 실측 성능 차분($\Delta Y$, 예: $\Delta\text{BrkDist}$) vs 예측 차분 산점도
* **기능**:
  * 모델의 목표 컬럼명(`diff_y_col`)을 동적으로 반영하여 축 라벨 및 지표 표기.
  * $R^2$ 결정계수 및 MAE 오차를 표기하며 45도 이상선($y=x$) 대비 예측 정확도를 검증합니다.

### 2. `plot_scatter_restoration(df_comp=None, data=None, overplot=True, show_connection=True, save=False, close=True)`
* **차트**: [Figure 2] 1차 기준(Ref) 대비 2차 원본(Raw)과 보정본(Corrected) 일치도 복원 산점도
* **기능**:
  * `overplot=True` (기본값): 단일 축에 $y=x$ 이상선과 함께 2nd Raw(붉은 원)와 2nd Corrected(파란 사각)를 동시에 오버플랏하고, 수직 가이드 점선으로 대각선 수렴 궤적을 직관적으로 제시합니다.
  * `overplot=False`: 기존 1행 2열 서브플롯(좌: 보정 전, 우: 보정 후)으로 나란히 비교합니다.

### 3. `plot_1st_2nd_scatter_overplot(data, x_col=None, y_col=None, ...)`
* **차트**: 임의의 환경 인자(절대습도, 기온, 침하 깊이 등) 대비 1차 시험(1st)과 2차 시험(2nd)의 성능 분포 산점도 오버플랏
* **기능**: 모델의 첫 번째 인자(`x_cols[0]`)와 목표 인자(`y_col`)를 기본 채택하며, 전체 시험 차수별 데이터 분포와 군집 특성을 한 그래프에서 직접 겹쳐서 비교 분석합니다.

### 4. `plot_correction_map(model_name=None, feat_x=None, feat_y=None, x_range=(-3, 3), y_range=(-2, 2), grid_size=10, save=False, close=True)`
* **차트**: [Figure 3] 환경 인자 $X_1$ 차분 vs $X_2$ 차분 성능 보정량 2D 등고선(Contour) 맵
* **기능**:
  * 모델의 `x_cols`에서 $X_1$과 $X_2$를 동적으로 선택 (또는 명시적 지정).
  * 3개 이상의 다변량 피처가 존재할 경우, 미선택 인자는 기준값인 `0.0`으로 고정하여 2차원 단면 등고선 그리드를 정밀 평가합니다.
  * 등고선과 컬러바를 통해 환경 변화에 따른 목표 성능 가감량을 직관적으로 제시합니다.

### 5. `plot_delta_braking_bar(df_comp=None, title=None, save=False, close=True)`
* **차트**: 타이어 세트별 보정 전 편차 대비 보정 후 편차 0 수렴 바차트

### 6. `plot_residual_dependency(data=None, factor_col=None, raw_col=None, corr_col=None, save=False, close=True)`
* **차트**: 노면 환경 인자($X$)에 대한 목표 성능($Y$) 회귀선 기울기(Slope)가 0으로 소거되는 효과 검증

### 7. `plot_tire_subsets_comparison(data, req_no=None, tire_set=None, style='trend', save=False, close=True)`
* **차트**: [Figure 4] 의뢰번호 및 타이어 세트별 1차(Ref), 2차 원본(2nd_Raw), 2차 보정본(2nd_Corr) 성능 비교 차트
* **기능**:
  * `req_no`만 지정 시: 해당 의뢰번호 내의 모든 타이어 세트를 서브플롯 그리드로 일괄 렌더링
  * `req_no`와 `tire_set` 둘 다 지정 시: 해당 특정 타이어 세트 단일 플롯으로 상세 렌더링
  * `style='trend'`: 1st(Ref) 기준 수평선, 1st->2nd Raw 변화선(붉은 점선), 1st->2nd Corr 복원선(푸른 실선) 및 개별 Run 산점도와 오차 개선율(%) 표기
  * `style='bar'`: 1st vs 2nd_Raw vs 2nd_Corr 3열 바차트 형식
