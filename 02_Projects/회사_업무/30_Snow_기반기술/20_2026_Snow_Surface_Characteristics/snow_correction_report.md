# ❄️ Snow 제동 성능 및 환경 요인 보정 종합 분석 보고서

- **생성 일시**: `2026-09-29 16:14:17`
- **플랫폼 명칭**: `SnowPlatform_2026_Pipeline`
- **통합 데이터 규모**: 1,964 행 × 48 개 특성 (동일 타이어 반복 차분 쌍: 95 쌍)

---

## 1. 📊 차분 머신러닝 보정 모델 평가 결과

- **입력 환경 특성 (Features)**: `char_height` (노면 눈 침하 깊이 차이), `cd_test_ah` (절대습도 차이)
- **목표 예측 변수 (Target)**: `char_brk_dist` (동일 타이어 반복 시험 간 제동거리 변동분)
- **채택된 대표 보정 모델**: `Random Forest`

| 모델명 (Model Name) | 결정계수 (R²) | 수정 R² (Adj. R²) | 평균 절대 오차 (MAE) | 평균 제곱 오차 (MSE) | 최적 파라미터 (Best Params) |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Ridge** | `0.4084` | `0.3345` | `0.6107 m` | `0.6573 m²` | `-` |
| **Linear Regression** | `0.4077` | `0.3337` | `0.6100 m` | `0.6581 m²` | `-` |
| **SVR** | `0.4065` | `0.3323` | `0.5589 m` | `0.6595 m²` | `-` |
| **Random Forest** | `0.5121` | `0.4511` | `0.5177 m` | `0.5422 m²` | `-` |
| **KNN Regressor** | `0.5417` | `0.4844` | `0.4966 m` | `0.5092 m²` | `-` |
| **Decision Tree** | `-1.0293` | `-1.2830` | `0.8247 m` | `2.2548 m²` | `-` |

---

## 2. 🎯 표준 기준 환경 조건 (Reference Conditions)

개별 시험의 환경 요인을 정규화하기 위한 기준점(Zero-Delta 좌표계)입니다:

- **기준 char_height**: `5.13 mm`
- **기준 cd_test_ah**: `1.97 g/m³`

---

## 3. 🧪 타이어 세트별 보정 전 vs 후 성능 통계 (산포 정화 분석)

| 타이어 세트 (`infor_TIRE_SET`) | 시험 런 수 | 원본 제동거리 평균 (m) | 원본 표준편차 (m) | 보정 제동거리 평균 (m) | 보정 표준편차 (m) | 산포 감소율 (Std Red.) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `C1` | 341 | 17.45 | 1.31 | 17.48 | 1.27 | **+2.5%** |
| `C2` | 293 | 17.39 | 1.31 | 17.43 | 1.24 | **+5.2%** |
| `C3` | 215 | 17.43 | 1.27 | 17.28 | 1.17 | **+8.3%** |
| `T1` | 344 | 17.97 | 2.37 | 17.99 | 2.24 | **+5.7%** |
| `T2` | 300 | 17.37 | 1.41 | 17.38 | 1.36 | **+3.7%** |
| `T3` | 247 | 17.27 | 1.24 | 17.19 | 1.13 | **+8.9%** |
| `T4` | 212 | 17.39 | 1.20 | 17.24 | 1.19 | **+1.2%** |
| `T5` | 12 | 17.10 | 0.48 | 17.09 | 0.48 | -0.3% |

---

## 4. 🖼️ 주요 시각화 산출물 및 검증 플롯 목록

- **머신러닝 보정 모델별 종합 성능 비교 차트**: [Correction_Models_Performance_Comparison.png](file:///D:/00_obsidian/_attachments/10_회사_업무/snow_correction_verification/Correction_Models_Performance_Comparison.png)
- **KNN Regressor 3D 등고선 환경 보정 맵**: [3D_Braking_Correction_Map_KNN.png](file:///D:/00_obsidian/_attachments/10_회사_업무/snow_correction_verification/3D_Braking_Correction_Map_KNN.png)
- **Random Forest 3D 등고선 환경 보정 맵**: [3D_Braking_Correction_Map_RF.png](file:///D:/00_obsidian/_attachments/10_회사_업무/snow_correction_verification/3D_Braking_Correction_Map_RF.png)
- **Linear Regression 3D 등고선 환경 보정 맵**: [3D_Braking_Correction_Map_Linear.png](file:///D:/00_obsidian/_attachments/10_회사_업무/snow_correction_verification/3D_Braking_Correction_Map_Linear.png)
- **노면 침하 깊이 잔차 의존성 소거 검증 차트**: [Residual_Dependency_Height.png](file:///D:/00_obsidian/_attachments/10_회사_업무/snow_correction_verification/Residual_Dependency_Height.png)
- **절대습도 잔차 의존성 소거 검증 차트**: [Residual_Dependency_AH.png](file:///D:/00_obsidian/_attachments/10_회사_업무/snow_correction_verification/Residual_Dependency_AH.png)
- **타이어 세트별 보정 전 vs 후 제동거리 박스플롯**: [Spec_Boxplot_TireSet.png](file:///D:/00_obsidian/_attachments/10_회사_업무/snow_correction_verification/Spec_Boxplot_TireSet.png)

---
*(본 보고서는 SnowBrakingPerformance 마스터 모듈의 `save_report_md()` 함수에 의해 자동 생성되었습니다.)*
