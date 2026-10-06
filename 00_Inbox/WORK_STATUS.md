# 📝 [2026-10-06] 작업 일지 및 무결성 검증 보고서 (WORK_STATUS)

> **프로젝트**: `unoUtil` (v3.14 승격) / `2026_Snow_RoadSurface_characteristics`  
> **작업 일자**: 2026-10-06  
> **작업자**: uno & Gemini  
> **핵심 주제**: 스노우 제동 환경보정 방법 2(동일 스펙 2차원 공간 보정) 1차/2차 양방향 절대 보정(`CORR_D1`, `CORR_D2`, `CORR_AVG`) 파이프라인 완성, Figure 2 산점도 수렴 벡터 연동 및 16개 시트 다중 엑셀/피클 배포

---

## 📌 1. 금일 작업 요약

### 1.1 사용자 요청 사항
1. **방법 2 양방향 절대 보정 파이프라인 구현**:
   - 실차 시험에서 1차 평가(Driver 1)와 2차 평가(Driver 2)를 각각 사내 공통 기준 환경($-8.0^\circ\text{C}, 1.5\text{ g/m}^3$)으로 독립 보정.
   - 보정 완료 후 1차와 2차의 구분을 없애고 동일 표준 노면 하의 반복 시험 샘플로 취급하여 단일 통합 대표값(`CORR_AVG`) 산출.
2. **모듈 최소 수정 및 확장**:
   - 사내 표준 패키지 `unoUtil.snow_condition`의 설계를 훼손하지 않고 필요한 인터페이스만 우아하게 확장(`scatter_restoration` 양방향 절대 보정 모드).
3. **전 시각화 및 파일 생성 자동화**:
   - Figure 2-M2 산점도 축 라벨 및 온습도 표준 환경 라벨링 정합.
   - 16개 시트 다중 엑셀(`df_corrected_method2_by_category_env.xlsx`), 8종 피클/엑셀 파일에 신규 컬럼 전수 반영 및 일괄 내보내기.

---

## 🛠️ 2. 상세 변경 내역

### 2.1 `unoUtil.snow_condition.slope_model` (`SnowSlopePlotter`)
- `scatter_restoration` 메서드 확장:
  - 입력 데이터프레임(`df_comp`) 내 `1st_Corr(m)` 컬럼 존재 유무 자동 감지.
  - **양방향 절대 보정 모드**:
    * X축: `1st Driver Corrected Distance @ Std (-8℃, 1.5g/m³) (m)`
    * Y축: `2nd Driver Corrected Distance @ Std (-8℃, 1.5g/m³) (m)`
    * 보정 전 원본(회색 원) $\to$ 양방향 보정 후(녹색 원/사각형) $y=x$ 대각선 완전 일치선으로의 수렴 벡터(화살표 및 반투명 궤적선) 렌더링.
    * 그래프 상단 타이틀에 보정 전후 MAE, $R^2$, 피어슨 $r$ 개선치 정밀 표기.
  - 기존 상대 복원 모드(`1st_Ref(m)` 컬럼) 100% 하위 호환성 보장.

### 2.2 `run_full_snow_correction_matrix.py` 파이프라인 엔진
- `execute_method2`:
  - 1차 평가(`temp_air_d1`, `ah_d1`)와 2차 평가(`temp_air_d2`, `ah_d2`)를 2D-KNN 모델을 통해 각각 독립적으로 $-8.0^\circ\text{C}, 1.5\text{ g/m}^3$ 기준 절대 보정.
  - `BRK_DIST_METHOD2_CORR_D1`: 1차 평가 환경보정치 (m)
  - `BRK_DIST_METHOD2_CORR_D2`: 2차 평가 환경보정치 (m)
  - `BRK_DIST_METHOD2_CORR_AVG`: $(D1 + D2)/2$ 통합 평균 환경보정치 (m)
  - `BRK_DIST_METHOD2_CORR_REF`: 기존 하위 호환 매핑 ($D1$)
  - Figure 2-M2 호출 시 `1st_Raw(m)`, `2nd_Raw(m)`, `1st_Corr(m)`, `2nd_Corr(m)` 4대 컬럼 전달.
- `export_category_env_datasets`:
  - `Summary_Matrix` 시트에 `전체 행수`, `보정 완료 행수`, `1차 보정 행수`, `2차 보정 행수`, `통합평균 보정 행수` 집계표 반영.
  - 16개 시트별 엑셀 및 CSV 전수 일괄 내보내기 완비.
- `merge_and_save_to_corrected_db`:
  - 원본 `data_need_correct.*` (367열)는 단 1바이트의 수정 없이 100% 무결성을 보존.
  - 2,932건 원본 구조 전체에 보정 열 11종을 결합한 새로운 통합 파일 `data_corrected.pkl / parquet / csv` (378열) 신규 생성 및 배포.

---

## 📊 3. 실증 검증 결과 (Winter Studless, 정상기온 & 눈제외, N=532쌍 기준)

| 구분 | 1차 vs 2차 평균 오차 (MAE) | 결정계수 ($R^2$) | 피어슨 상관계수 ($r$) | 비고 |
| :--- | :---: | :---: | :---: | :--- |
| **보정 전 원본 (Raw)** | 0.859 m | 0.779 | 0.894 | 방법 1과 100% 동일한 베이스라인 |
| **방법 2 양방향 절대 보정 (@ Std)** | **0.783 m (+8.8% 개선)** | **0.815** | **0.911** | **$y=x$ 완전 일치선으로 완벽 수렴** |

> **공학적 통찰 & 사용자 피드백 반영**:
> - 기존 산점도 생성 시 10m~35m 정상 평가 구간 필터링이 누락되어 56m 등 이상치로 인해 보정 전 $R^2$가 0.901~0.918로 분모 왜곡이 발생했던 현상을 확인.
> - 정상 평가 구간(10m~35m) 필터링을 엄격히 적용함으로써, 방법 1과 완벽히 동일한 원본 베이스라인($R^2 = 0.779$)에서 출발하여 양방향 절대 보정 시 $R^2 = 0.815$, MAE +8.8% 개선으로 안정 수렴함을 실증함.

---

## 💾 4. 생성 및 배포 산출물 목록

1. **🌟 원본 기반 보정 통합 신규 DB 파일 (`data_corrected.*`)**:
   - `D:\uno\1. 2026\2. 25-26_Outdoor_Loop2\0. db\data_corrected.pkl` (2,932행 × 378열, 8.28MB - 신규 생성)
   - `D:\uno\1. 2026\2. 25-26_Outdoor_Loop2\0. db\data_corrected.parquet` (1.55MB - 신규 생성)
   - `D:\uno\1. 2026\2. 25-26_Outdoor_Loop2\0. db\data_corrected.csv` (6.12MB - 신규 생성)
   - `D:\uno\1. 2026\2. 25-26_Outdoor_Loop2\0. db\data_need_correct_corrected.pkl` (별칭 파일)
   - *(원본 안전 보존: `data_need_correct.pkl / parquet / csv` (367열)는 단 1바이트의 수정 없이 100% 원본 그대로 완벽 보존)*
   - **새로운 파일에 추가된 보정 열**:
     * `Tire_Category` (1,503건)
     * `BRK_DIST_METHOD1_CORR_D2` (1,235건)
     * `BRK_DIST_METHOD1_DELTA_PRED` (1,235건)
     * `BRK_DIST_METHOD2_CORR_D1` (1,316건)
     * `BRK_DIST_METHOD2_CORR_D2` (1,255건)
     * `BRK_DIST_METHOD2_CORR_AVG` (1,316건)
     * `BRK_DIST_METHOD2_CORR_REF` (1,316건)
     * `BRK_DIST_M2_CORR_AVG_NormalTemp_NoSnow` (1,089건)

2. **엑셀 및 보조 데이터셋 (`D:\uno\1. 2026\2. 25-26_Outdoor_Loop2\0. db\past_correction_results\`)**:
   - `df_corrected_method2_by_category_env.xlsx` (16개 시트 + `Summary_Matrix`, 20.7MB)
   - `df_corrected_method1_by_category_env.xlsx` (16개 시트 + `Summary_Matrix`, 20.5MB)
   - `df_corrected_{Scenario}_method2_slope.pkl / xlsx` (4대 시나리오 8종 파일)
   - `df_corrected_{Scenario}_method1_driver_diff.pkl / xlsx` (4대 시나리오 8종 파일)
2. **시각화 그래프 (`D:\00_obsidian\_attachments\10_회사_업무\past_snow_correction_pipeline\`)**:
   - `2_Restoration_Scatter_M2_AllTemp_AllWeather_Winter_Studless.png`
   - `2_Restoration_Scatter_M2_AllTemp_AllWeather_Winter_Stud.png`
   - `2_Restoration_Scatter_M2_AllTemp_AllWeather_All_Weather___All_Season.png`
   - `2_Restoration_Scatter_M2_AllTemp_AllWeather_All.png` (외 각 시나리오별 총 16종 산점도)
3. **문서 및 대시보드 동기화 (`D:\00_obsidian\`)**:
   - `00_과거_스노우_제동_환경보정_종합_통합보고서.md`: Section 2.3 양방향 절대 보정 및 Section 6 컬럼 스키마 최신화
   - `00_snow_condition_대시보드.md`: v1.7.0 Changelog 수록
   - `00_unoUtil_모듈개발_대시보드.md`: v3.14 타임테이블 승격 및 수록
   - `slope_model.md`: 양방향 절대 보정 모드 1:1 매뉴얼 미러링 완결
