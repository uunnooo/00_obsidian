# 📘 SnowCorrectionPlotter (스노우 보정 모델 시각화 전담 플로터)

## 📌 개요
`SnowCorrectionPlotter`는 스노우 노면 환경 보정 모델의 검증 그래픽 시각화를 전담하는 클래스입니다.
`SnowCorrectionModel`의 동적 특성 인자 리스트(`x_cols`) 및 목표 인자(`y_col`)와 유기적으로 연동되어, 축 라벨, 범례, 타이틀 및 컬러바를 전달된 컬럼명에 맞추어 100% 동적으로 자동 렌더링합니다.

> 🏷️ **규칙 준수 (No Redundant Prefix Law)**:
> 클래스명에 이미 `Plotter` 역할이 명확히 담겨 있으므로, 내부 메서드에 불필요한 `plot_` 접두사를 붙이지 않고 목적어와 행위 중심의 직관적 명칭(`delta_prediction_scatter`, `correction_map` 등)을 단일 표준(SSOT)으로 사용합니다.

---

## ⚙️ 주요 차트 렌더링 메서드

### 1. `delta_prediction_scatter(df_diff=None, model_name=None, save=False, close=True)`
* **차트**: [Figure 1] 실측 성능 차분($\Delta Y$, 예: $\Delta\text{BrkDist}$) vs 예측 차분 산점도
* **기능**:
  * 모델의 목표 컬럼명(`diff_y_col`)을 동적으로 반영하여 축 라벨 및 지표 표기.
  * $R^2$ 결정계수 및 MAE 오차를 표기하며 45도 이상선($y=x$) 대비 예측 정확도를 검증합니다.

### 2. `scatter_restoration(df_comp=None, data=None, overplot=True, show_connection=True, save=False, close=True)`
* **차트**: [Figure 2] 1차 기준(Ref) 대비 2차 원본(Raw)과 보정본(Corrected) 일치도 복원 산점도
* **기능**:
  * `overplot=True` (기본값): 단일 축에 $y=x$ 이상선과 함께 2nd Raw(붉은 원)와 2nd Corrected(파란 사각)를 동시에 오버플랏하고, 수직 가이드 점선으로 대각선 수렴 궤적을 직관적으로 제시합니다.
  * `overplot=False`: 기존 1행 2열 서브플롯(좌: 보정 전, 우: 보정 후)으로 나란히 비교합니다.

### 2-1. `scatter_restoration_comparison(data, model_names=None, col_dist=None, show_connection=True, show_trendline=True, save=False, close=True)`
* **차트**: [Figure 2-Multi] 여러 후보 머신러닝 모델(RF, SVR, KNN 등)의 1차(Ref) vs 2차(Raw/Corr) 실차 제동거리 복원 수렴도 산점도 Side-by-Side 비교
* **기능**:
  * `model_names`: 비교할 모델 리스트 (기본값: `['Random Forest', 'SVR', 'KNN Regressor']`).
  * 1행 N열 서브플롯으로 구성되며, $X, Y$ 공통 축 범위로 스케일을 완전 일치화.
  * $y=x$ 완전 일치선(검은 파선), 2nd Raw(붉은 원), 2nd Corr(푸른 사각), 수렴 이동 화살표(화살촉 벡터), 보정 전/후 선형 추세선(Trendline) 동시 렌더링.
  * 각 서브플롯 상단 타이틀에 모델별 $\text{MAE}$ 개선율($\%$), $R^2$ 개선폭, 타이어 순위 보존도(Kendall $\tau$) 자동 계산 및 표기.
  * 윈도우 파일 잠금(`OSError [Errno 22]`) 방어 저장 헬퍼(`_safe_savefig`) 탑재.

### 3. `scatter_overplot(data, x_col=None, y_col=None, ...)`
* **차트**: 임의의 환경 인자(절대습도, 기온, 침하 깊이 등) 대비 1차 시험(1st)과 2차 시험(2nd)의 성능 분포 산점도 오버플랏
* **기능**: 모델의 첫 번째 인자(`x_cols[0]`)와 목표 인자(`y_col`)를 기본 채택하며, 전체 시험 차수별 데이터 분포와 군집 특성을 한 그래프에서 직접 겹쳐서 비교 분석합니다.

### 4. `correction_map(x_col=None, y_col=None, x_range=(-3, 3), y_range=(-1.5, 1.5), v_range=None, show_scatter=True, grid_size=60, model_name=None, save=False, close=True)`
* **차트**: [Figure 3] 환경 인자 $X_1$ 차분 vs $X_2$ 차분 성능 보정량 2D 등고선(Contour) 맵 (단일 표준 통합 보정맵)
* **기능**:
  * 모델의 `x_cols`에서 $X_1$과 $X_2$를 동적으로 선택 (또는 명시적 지정).
  * `v_range`: 컬러바 색상 범위를 고정하여, 모델 간(방법 1 vs 방법 2) 동일한 색상이 동일한 제동거리 보정량을 의미하도록 1:1 비교 스케일 일치화.
  * `show_scatter=True`: 모델 학습에 사용된 실제 차분 데이터 포인트(방법 1: 1차-2차 차분, 방법 2: 동일 스펙 중심화 편차)를 등고선 위에 반투명 산점도로 오버플랏하여 데이터 기반 곡면임을 입증.
  * 3개 이상의 다변량 피처가 존재할 경우, 미선택 인자는 기준값인 `0.0`으로 고정하여 2차원 단면 등고선 그리드를 정밀 평가합니다.
  * 등고선과 컬러바를 통해 환경 변화에 따른 목표 성능 가감량을 직관적으로 제시합니다.

### 4-1. `correction_map_comparison(model_names=None, x_col=None, y_col=None, x_range=(-3.5, 3.5), y_range=(-2.5, 2.5), v_range=None, show_scatter=True, grid_size=70, save=False, close=True)`
* **차트**: [Figure 3-Multi] 여러 머신러닝 회귀 모델(Random Forest, SVR, KNN 등)의 2D 등고선 보정 맵을 나란히(Side-by-Side) 동일 컬러바로 렌더링
* **기능**:
  * `model_names`: 비교 대상 모델 리스트 (기본값: `['Random Forest', 'SVR', 'KNN Regressor']`).
  * 단일 공통 컬러바(Colorbar) 및 공통 등고선 레벨(levels) 적용으로 모델 간 곡면 거동을 왜곡 없이 1:1 직접 대조.
  * 실제 차분 데이터 산점도 오버레이 및 (0,0) 기준점 별표(`★`) 동시 표기.
  * 모델별 $R^2$ 점수 및 물리적 특성 부제목 자동 라벨링.

### 5. `delta_braking_bar(df_comp=None, title=None, save=False, close=True)`
* **차트**: 타이어 세트별 보정 전 편차 대비 보정 후 편차 0 수렴 바차트

### 6. `residual_dependency(data=None, factor_col=None, raw_col=None, corr_col=None, save=False, close=True)`
* **차트**: 노면 환경 인자($X$)에 대한 목표 성능($Y$) 회귀선 기울기(Slope)가 0으로 소거되는 효과 검증

### 7. `tire_subsets_comparison(data, req_no=None, tire_set=None, style='trend', save=False, close=True)`
* **차트**: [Figure 4] 의뢰번호 및 타이어 세트별 1차(Ref), 2차 원본(2nd_Raw), 2차 보정본(2nd_Corr) 성능 비교 차트
* **기능**:
  * `req_no`만 지정 시: 해당 의뢰번호 내의 모든 타이어 세트를 서브플롯 그리드로 일괄 렌더링
  * `req_no`와 `tire_set` 둘 다 지정 시: 해당 특정 타이어 세트 단일 플롯으로 상세 렌더링
  * `style='trend'`: 1st(Ref) 기준 수평선, 1st->2nd Raw 변화선(붉은 점선), 1st->2nd Corr 복원선(푸른 실선) 및 개별 Run 산점도와 오차 개선율(%) 표기
  * `style='bar'`: 1st vs 2nd_Raw vs 2nd_Corr 3열 바차트 형식
