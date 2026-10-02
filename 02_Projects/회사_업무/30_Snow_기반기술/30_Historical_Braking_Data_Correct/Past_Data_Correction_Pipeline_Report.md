# 🧭 과거 7개년 스노우 제동 데이터 이발로 노면 차분 보정 종합 리포트

> **분석 대상**: 과거 7개년 이발로 야외 제동 데이터 (`TEST_PG == 'IVALO'` & `TEST_METHOD_NAME == 'HK-Outdoor'`, 총 1,503건)
> **핵심 인자**: `노면온도(BRK_TEMP_SURFACE)` + `Sonntag 물리 절대습도(AH, g/m³)`
> **타이어 분류**: `SEASON` 결측치 291건 100% 구제 분류 (스펙/패턴명 역추적)

---

## 🏆 1. [방법 1] Driver 1 vs Driver 2 정밀 차분 머신러닝 보정 요약

| 타이어 카테고리 | 유효 페어수 | 보정 전 MAE | 보정 전 상관계수($r$) | **RF 보정 후 MAE** | **RF 오차개선율** | **보정 후 상관계수($r$)** | 선형 Ridge 개선율 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Winter Studless** | 613건 | 0.814m | 0.8733 | **0.515m** | **+36.70%** | **0.9520** | +14.91% |
| **Winter Stud** | 97건 | 0.889m | 0.7402 | **0.437m** | **+50.88%** | **0.9229** | +6.26% |
| **All Weather / All Season** | 496건 | 0.846m | 0.9308 | **0.586m** | **+30.69%** | **0.9665** | +6.95% |
| **All** | 1,221건 | 0.839m | 0.9117 | **0.629m** | **+25.04%** | **0.9527** | +11.10% |

### 📌 방법 1 주요 시각화 결과물:
- **Figure 1 (예측값 vs 실제 차분 산점도)**:
  - [Winter Studless](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/1_Diff_Actual_vs_Predicted_Method1_Winter_Studless.png)
  - [Winter Stud](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/1_Diff_Actual_vs_Predicted_Method1_Winter_Stud.png)
- **Figure 2 (1차 vs 2차 복원 산점도 오버플랏)**:
  - [Winter Studless](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/2_Restoration_Scatter_Method1_Winter_Studless.png)
  - [Winter Stud](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/2_Restoration_Scatter_Method1_Winter_Stud.png)
- **Figure 3 (2D 등고선 노면 반응 맵)**:
  - [Winter Studless Contour Map](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/3_Response_Surface_Contour_Method1_Winter_Studless.png)
  - [Winter Stud Contour Map](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/3_Response_Surface_Contour_Method1_Winter_Stud.png)

---

## 🏆 2. [방법 2] 동일 스펙 고정효과 공통 기울기(Slope) 보정 요약

| 타이어 카테고리 | 스펙수 / 시험수 | 노면온도 기울기 ($eta_{	ext{surf}}$) | 절대습도 기울기 ($eta_{	ext{ah}}$) | 보정 전 산포($\sigma$) | 보정 후 산포($\sigma$) | **동일스펙 산포감소율** | **1차시험 복원개선율** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Winter Studless** | 132종 / 355건 | -0.0452 (p=7.2e-02) | **+0.5526** (p=3.4e-05) | 1.077m | 1.019m | **+5.42%** | **+4.94%** |
| **Winter Stud** | 37종 / 99건 | -0.2192 (p=5.0e-02) | **+1.7712** (p=1.8e-03) | 1.864m | 1.867m | **-0.17%** | **+2.12%** |
| **All Weather / All Season** | 124종 / 339건 | +0.0353 (p=1.9e-01) | **-0.1451** (p=3.6e-01) | 1.398m | 1.385m | **+0.95%** | **+0.86%** |
| **All** | 298종 / 806건 | -0.0119 (p=5.5e-01) | **+0.3529** (p=1.6e-03) | 1.322m | 1.302m | **+1.52%** | **+1.47%** |

### 📌 방법 2 주요 시각화 결과물:
- **Figure 1 (스펙 내 편차 회귀선)**:
  - [Winter Studless](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/1_Within_Spec_Residual_Method2_Winter_Studless.png)
- **Figure 2 (스펙 내 반복 시험 복원 산점도)**:
  - [Winter Studless](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/2_Restoration_Scatter_Method2_Winter_Studless.png)
  - [Winter Stud](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/2_Restoration_Scatter_Method2_Winter_Stud.png)
- **Figure 3 (2D 등고선 노면 반응 맵)**:
  - [Winter Studless Standard Map](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/3_Response_Surface_Contour_Method2_Winter_Studless.png)
  - [Winter Stud Standard Map](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/3_Response_Surface_Contour_Method2_Winter_Stud.png)
- **Figure 4 (스펙별 분산 축소 박스플롯)**:
  - [Winter Studless Variance Reduction](file:///D:/00_obsidian/_attachments/10_회사_업무/past_snow_correction_pipeline/4_Spec_Distribution_Reduction_Method2_Winter_Studless.png)

---

## 💾 3. 생성 및 분리 저장된 보정 데이터 파일 안내

1. **방법 1 보정 데이터셋 (Driver 1 vs Driver 2 정밀 차분 보정)**:
   - 피클 파일: `D:\uno\1. 2026\2. 25-26_Outdoor_Loop2\0. db\past_correction_results\df_corrected_method1_driver_diff.pkl`
   - 엑셀 파일: `D:\uno\1. 2026\2. 25-26_Outdoor_Loop2\0. db\past_correction_results\df_corrected_method1_driver_diff.xlsx`
   - 신규 추가된 보정 컬럼: `BRK_DIST_METHOD1_CORR_D2` (Driver 2 제동거리 보정값), `BRK_DIST_METHOD1_DELTA_PRED` (예측 차분량)

2. **방법 2 보정 데이터셋 (동일 스펙 공통 기울기 보정)**:
   - 피클 파일: `D:\uno\1. 2026\2. 25-26_Outdoor_Loop2\0. db\past_correction_results\df_corrected_method2_slope.pkl`
   - 엑셀 파일: `D:\uno\1. 2026\2. 25-26_Outdoor_Loop2\0. db\past_correction_results\df_corrected_method2_slope.xlsx`
   - 신규 추가된 보정 컬럼: `BRK_DIST_METHOD2_CORR_REF` (이발로 표준 노면 -8℃, 1.5g/m³ 환산값), `BRK_DIST_METHOD2_CORR_TO_1ST` (동일 스펙의 1회차 시험 환경 환산값)

---
**보고서 발행 일자**: 2026-10-02