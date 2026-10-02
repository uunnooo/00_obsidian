# 🧭 과거 7개년 스노우 제동 데이터 이발로 노면 차분 보정 종합 리포트

> **분석 대상**: 과거 7개년 이발로 야외 제동 데이터 (`TEST_PG == 'IVALO'` & `TEST_METHOD_NAME == 'HK-Outdoor'`, 총 1,503건)  
> **핵심 환경 인자**: `대기온도(temp_air, ℃)` + `Sonntag 물리 절대습도(ah, g/m³)`  
> **사내 표준 통합 모듈**: `unoUtil.snow_condition.SnowCorrectionModel` 단일 엔진 적용  
> **타이어 분류**: `SEASON` 결측치 291건 100% 구제 분류 (스펙/패턴명 역추적)

---

## 🏆 1. [방법 1] Driver 1 vs Driver 2 정밀 차분 머신러닝 보정 (Random Forest)

당일 동일 의뢰 내 1차(Driver 1) vs 2차(Driver 2) 시험 간의 환경 차이($\Delta T, \Delta AH$)에 따른 제동거리 변동량($\Delta y$)을 학습하여 2차 시험값을 1차 시험 환경 기준으로 정밀 복원합니다.

| 타이어 카테고리 | 유효 페어수 | 보정 전 MAE | 보정 전 상관계수($r$) | **RF 보정 후 MAE** | **RF 오차개선율** | **보정 후 상관계수($r$)** | RF 모델 결정계수($R^2$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Winter Studless** | 542쌍 | 0.811m | 0.8941 | **0.535m** | **+34.03%** | **0.9542** | **0.5949** |
| **Winter Stud** | 96쌍 | 0.849m | 0.7776 | **0.375m** | **+55.79%** | **0.9576** | **0.7662** |
| **All Weather / All Season** | 415쌍 | 0.848m | 0.9283 | **0.557m** | **+34.33%** | **0.9691** | **0.5765** |
| **All (통합)** | 1,053쌍 | 0.846m | 0.9114 | **0.642m** | **+24.14%** | **0.9531** | **0.4756** |

### 📌 방법 1 주요 시각화 결과물 (링크를 클릭하여 확인 가능):
- **Figure 1 (예측값 vs 실제 차분 산점도)**:
  - [Winter Studless](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/1_Diff_Actual_vs_Predicted_Method1_Winter_Studless.png)
  - [Winter Stud](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/1_Diff_Actual_vs_Predicted_Method1_Winter_Stud.png)
  - [All Weather / All Season](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/1_Diff_Actual_vs_Predicted_Method1_All_Weather.png)
  - [All (통합)](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/1_Diff_Actual_vs_Predicted_Method1_All.png)
- **Figure 2 (1차 vs 2차 복원 산점도 오버플랏)**:
  - [Winter Studless](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/2_Restoration_Scatter_Method1_Winter_Studless.png)
  - [Winter Stud](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/2_Restoration_Scatter_Method1_Winter_Stud.png)
  - [All Weather / All Season](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/2_Restoration_Scatter_Method1_All_Weather.png)
  - [All (통합)](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/2_Restoration_Scatter_Method1_All.png)
- **Figure 3 (2D 등고선 노면 반응 맵)**:
  - [Winter Studless Contour Map](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/3_Response_Surface_Contour_Method1_Winter_Studless.png)
  - [Winter Stud Contour Map](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/3_Response_Surface_Contour_Method1_Winter_Stud.png)
  - [All Weather Contour Map](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/3_Response_Surface_Contour_Method1_All_Weather.png)
  - [All Contour Map](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/3_Response_Surface_Contour_Method1_All.png)

---

## 🏆 2. [방법 2] 동일 스펙 중심화 2차원 공간 보정 (러프 평활화 2D-KNN)

동일 스펙(`SPEC_NO`, 최소 2회 이상 반복 시험)의 고유 평균 편차($\Delta T_i, \Delta AH_i \to \Delta y_i$)를 학습하여, 사내 공통 표준 환경($-8.0^\circ\text{C}, 1.5\text{ g/m}^3$) 기준으로 전수 절대 보정합니다. 국소 아일랜드(과적합)를 배제하기 위해 **광역 평활화 파라미터($k=15\sim 50$, `weights='uniform'`)**를 적용하여 완만하고 물리적으로 타당한 노면 반응면을 생성했습니다.

| 타이어 카테고리 | 스펙수 / 시험수 | 최적 평활화 ($k$, 가중치) | 보정 전 산포($\sigma_{\text{raw}}$) | **보정 후 산포($\sigma_{\text{corr}}$)** | **스펙 내 산포감소율** | **상위10종 잔차 수렴율(Shrink)** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Winter Stud** | 28종 / 72건 | $k=15$, uniform | 1.611m | **1.364m** | **+15.36%** | **+43.18%** |
| **Winter Studless** | 106종 / 284건 | $k=35$, uniform | 1.466m | **1.418m** | **+3.32%** | **+2.15%** |
| **All Weather / All Season** | 88종 / 243건 | $k=35$, uniform | 1.340m | **1.362m** | **-1.62%** | **+0.91%** |
| **All (통합)** | 222종 / 599건 | $k=50$, uniform | 1.437m | **1.447m** | **-0.69%** | **+0.70%** |

### 📌 방법 2 주요 시각화 결과물 (링크를 클릭하여 확인 가능):
- **Figure 1 (스펙 내 편차 회귀/잔차 산점도)**:
  - [Winter Stud](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/1_Within_Spec_Residual_Method2_Winter_Stud.png)
  - [Winter Studless](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/1_Within_Spec_Residual_Method2_Winter_Studless.png)
  - [All Weather / All Season](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/1_Within_Spec_Residual_Method2_All_Weather.png)
  - [All (통합)](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/1_Within_Spec_Residual_Method2_All.png)
- **Figure 2 (스펙 내 반복 시험 복원 산점도)**:
  - [Winter Stud](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/2_Restoration_Scatter_Method2_Winter_Stud.png)
  - [Winter Studless](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/2_Restoration_Scatter_Method2_Winter_Studless.png)
  - [All Weather / All Season](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/2_Restoration_Scatter_Method2_All_Weather.png)
  - [All (통합)](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/2_Restoration_Scatter_Method2_All.png)
- **Figure 3 (2D-KNN 광역 평활화 러프 등고선 보정 맵)**:
  - [Winter Stud Rough Map](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/3_Response_Surface_Contour_Method2_Winter_Stud.png)
  - [Winter Studless Rough Map](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/3_Response_Surface_Contour_Method2_Winter_Studless.png)
  - [All Weather Rough Map](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/3_Response_Surface_Contour_Method2_All_Weather.png)
  - [All Rough Map](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/3_Response_Surface_Contour_Method2_All.png)
- **Figure 4 (스펙별 분산 축소 박스플롯)**:
  - [Winter Stud Variance Reduction](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/4_Spec_Distribution_Reduction_Method2_Winter_Stud.png)
  - [Winter Studless Variance Reduction](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/4_Spec_Distribution_Reduction_Method2_Winter_Studless.png)
  - [All Weather Variance Reduction](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/4_Spec_Distribution_Reduction_Method2_All_Weather.png)
  - [All Variance Reduction](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/4_Spec_Distribution_Reduction_Method2_All.png)

---

## 💾 3. 생성 및 영속화 완료된 통합 보정 데이터 파일 안내

* **저장 위치**: `D:\uno\1. 2026\2. 25-26_Outdoor_Loop2\0. db\past_correction_results\`

1. **통합 16개 시나리오 엑셀 파일 (전수 수록, 20.6 MB)**:
   - 파일명: `df_corrected_unified_snow_matrix.xlsx`
   - 구성: 16개 개별 시나리오 시트 + `Summary_Unified_Comparison` 종합 대조표
   - 보정 컬럼:
     - `BRK_DIST_METHOD1_CORR_D2`: 방법 1 (Driver 1 환경 기준 Driver 2 복원 제동거리)
     - `BRK_DIST_METHOD2_CORR_REF`: 방법 2 (사내 표준 -8℃, 1.5g/m³ 기준 절대 정규화 제동거리)

2. **통합 피클 파일 (31.3 MB)**:
   - 파일명: `df_corrected_unified_snow_matrix.pkl`
   - Python 분석 및 후속 머신러닝 모델링용 고속 딕셔너리 포맷

---
**보고서 갱신 일자**: 2026-10-02 (통합 단일 엔진 `SnowCorrectionModel` 및 광역 평활화 2D-KNN 전면 반영 완료)