---
id: "WORK_STATUS_20260923"
title: "2026-09-23 스노우 제동 보정 머신러닝 엔진 고도화 및 위키 지식화 작업 일지"
type: daily_note
category_main: 회사_업무
category_sub: SnowSurface
date: 2026-09-23
status: 완료
tags:
  - 회사_업무
  - SnowSurface
  - 머신러닝
  - 하이퍼파라미터튜닝
  - 지식화
project_link: "[[00_2026_Snow_Surface_Characteristics_대시보드]]"
---

# 📋 [2026-09-23] 스노우 제동 차분 머신러닝 보정 엔진 고도화 및 자동화 파이프라인 완성 보고

## 1. 🎯 작업 개요 및 목표
* **배경**: 
  - `b_combine_surface_performance_spec.py` 이후 제동-노면-기상 통합 데이터(1,964행)를 바탕으로 환경 요인을 분리·보정하는 차분 머신러닝 엔진의 사용성, 안정성, 하이퍼파라미터 튜닝 체계의 부재 개선 필요.
  - Decision Tree 평가 시 발생했던 $R^2$ 음수(-1.03) 과적합 원인 규명 및 지식화.
  - 사용자가 장기적으로 알고리즘과 모듈 사용법을 잊지 않고 활용할 수 있도록 위키 지식화 및 자동 마크다운(.md) 보고서 생성 체계 구축.
* **핵심 달성 목표**:
  1. 원스톱 데이터 적재 API (`load_combined_data`) 신설.
  2. 5-Fold 교차검증 기반 하이퍼파라미터 오토 튜닝(`auto_tune=True`) 및 수동 튜닝(`model_params`) 구현.
  3. 종합 분석 결과 마크다운(.md) 보고서 자동 생성 함수(`save_report_md`) 구현 (사내 다형성 `save` 표준 준수).
  4. 파이썬 표준 규격(`PYTHON_CODE_AGENT.md`) 100% 충족 (Google Style Docstrings, PEP 484 타입 힌트, 레거시 kwargs 완벽 흡수).

---

## 2. 🚀 주요 개발 및 수정 내역

### 2.1. 원스톱 데이터 로더 신설: `load_combined_data()`
* **위치**: `Snow_braking_relate_condition/snow_braking_performance.py`
* **역할**: 파일 경로(str, Path) 또는 DataFrame을 인수로 받아 무결성을 검증하고, 플랫폼 버퍼(`self.df_combined`)에 적재하며, `is_performance_matched = True` 플래그를 자동으로 활성화하여 재매칭 연산 낭비를 방지.
```python
sbp = SnowBrakingPerformance(name="SnowPlatform_2026")
df_combined = sbp.load_combined_data(r"D:\uno\...\1. df_combine_test_surface_spec.pkl")
```

### 2.2. 하이퍼파라미터 수동/오토 튜닝 인터페이스 완비
* **위치**: `Snow_braking_relate_condition/correction_engine.py`, `snow_braking_performance.py`
* **원인 규명 및 해결 ($R^2 < 0$ 문제)**:
  - 단일 Decision Tree의 깊이 미제한으로 인해 학습 데이터 95쌍에 과적합(Overfitting)되어 검증 세트에서 베이스라인 평균 예측보다 못한 오차 발생.
  - 5-Fold CV (`GridSearchCV`) 기반 오토 튜닝을 도입하여 `max_depth=2`, `min_samples_leaf=3` 제약을 부여함으로써 **$R^2 = +0.4492$로 양수 정상 회복**.
* **오토 튜닝 탐색 공간 (Grid Search Spaces)**:
  - **KNN Regressor**: `n_neighbors=[3, 4, 5, 7, 9, 11]`, `weights=['uniform', 'distance']`, `p=[1, 2]`
  - **Random Forest**: `n_estimators=[50, 80, 100, 150]`, `max_depth=[3, 4, 5, None]`, `min_samples_leaf=[1, 2, 3]`
  - **Ridge**: `alpha=[0.01, 0.1, 1.0, 10.0, 50.0]`
  - **SVR**: `C=[1.0, 5.0, 10.0, 30.0]`, `epsilon=[0.01, 0.05, 0.1, 0.2]`
* **수동/오토 튜닝 호출**:
```python
# [오토 튜닝 모드] 5-Fold CV로 각 모델 최적 파라미터 자동 탐색
metrics = sbp.train_correction_model(model_type='KNN Regressor', auto_tune=True, cv=5)

# [수동 튜닝 모드] 원하는 파라미터 직접 주입
metrics = sbp.train_correction_model(
    model_type='KNN Regressor',
    model_params={'n_neighbors': 7, 'weights': 'uniform', 'p': 1}
)
```

### 2.3. 종합 분석 결과 마크다운(.md) 보고서 생성기: `save_report_md()`
* **위치**: `Snow_braking_relate_condition/snow_braking_performance.py`
* **특징**:
  - `save=True` (기본값): `D:\uno\1. 2026\2. 25-26_Outdoor_Loop2\0. db\Snow_Correction_Report.md` 자동 저장.
  - `save=디렉토리경로`: 해당 디렉토리 내에 `Snow_Correction_Report.md` 결합 저장.
  - `save=파일경로`: 지정된 파일 경로 그대로 저장.
  - `save=False`: 파일 저장을 생략하고 마크다운 문자열 반환.
  - 보고서 내용:
    1. 데이터 규모 메타데이터 (1,964행 × 48열, 95쌍 차분 데이터)
    2. 모델별 결정계수($R^2$), 수정 $R^2$, MAE, MSE, Auto-Tune 최적 파라미터 표
    3. 표준 기준 환경(Reference Conditions: `char_height`=5.13mm, `cd_test_ah`=1.97g/m³)
    4. 타이어 세트별(C1~C3, T1~T5) 보정 전 vs 후 평균, 표준편차 및 산포 감소율(Std Red.) 표
    5. 생성된 3D 보정 맵 및 잔차 분석 플롯의 마크다운 링크 매핑

---

## 3. 📊 최종 학습 성능 및 산출물 검증 결과

### 3.1. 머신러닝 알고리즘별 성능 비교
| 머신러닝 모델 | 결정계수 ($R^2$) | 수정 $R^2$ (Adj. $R^2$) | 평균 절대 오차 (MAE) | 탐색된 최적 하이퍼파라미터 |
| :--- | :---: | :---: | :---: | :--- |
| **Random Forest** | **0.4927** | **0.4293** | **0.5702 m** | `{'max_depth': 3, 'min_samples_leaf': 3, 'n_estimators': 80}` |
| **Decision Tree** | **0.4492** | **0.3804** | **0.5941 m** | `{'max_depth': 2, 'min_samples_leaf': 3}` *(음수 오차 완전 탈피)* |
| **KNN Regressor** | **0.4234** | **0.3513** | **0.5782 m** | `{'n_neighbors': 7, 'p': 1, 'weights': 'uniform'}` |
| **Ridge** | **0.4134** | **0.3400** | **0.6168 m** | `{'alpha': 10.0}` |
| **Linear Regression** | **0.4077** | **0.3337** | **0.6100 m** | 기본 최소자승법 |
| **SVR** | **0.3850** | **0.3081** | **0.5873 m** | `{'C': 5.0, 'epsilon': 0.01}` |

### 3.2. 최종 생성 산출물 목록
* **종합 마크다운 보고서**: `D:\uno\1. 2026\2. 25-26_Outdoor_Loop2\0. db\Snow_Correction_Report.md`
* **보정 완료 데이터셋**: `D:\uno\1. 2026\2. 25-26_Outdoor_Loop2\0. db\1. df_combine_test_surface_spec_corrected.pkl`
* **플랫폼 세션 영속화 객체**: `D:\uno\1. 2026\2. 25-26_Outdoor_Loop2\0. db\snow_platform_2026.pkl`
* **3D 등고선 보정 맵**:
  - KNN: `D:\uno\1. 2026\2. 25-26_Outdoor_Loop2\4. Figure\3D_Braking_Correction_Map_KNN.png`
  - RF: `D:\uno\1. 2026\2. 25-26_Outdoor_Loop2\4. Figure\3D_Braking_Correction_Map_RF.png`
  - Linear: `D:\uno\1. 2026\2. 25-26_Outdoor_Loop2\4. Figure\3D_Braking_Correction_Map_Linear.png`
* **검증 플롯**:
  - 잔차 의존성 소거: `Residual_Dependency_Height.png`, `Residual_Dependency_AH.png`
  - 타이어 세트별 박스플롯: `Spec_Boxplot_TireSet.png`
  - 모델별 종합 성능 비교: `Correction_Models_Performance_Comparison.png`

---

## 4. 🧭 향후 계획
1. `c_plot_correction_verification.py` 스크립트 점검 및 현대화.
2. 타이어 고유 사양(컴파운드, 패턴, 규격)별 제동거리 보정 효과 및 순위 역전(Rank Inversion) 정밀 분석.
