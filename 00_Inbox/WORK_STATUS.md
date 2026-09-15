# 📌 제동 성능 자동 분석 프로젝트 (Braking_AutoBuild) 작업 진행 현황 및 아키텍처

---

## 📅 작업 완료 요약 (2026년 9월 15일 화요일 기준)

사용자의 피드백 및 고도화 요구사항을 100% 반영하여, **데이터 분리 저장(`0. db`), 넘버링 시각화(`2. fig`), Wet/Dry 노면 기준 독립 집계, 슬로프 차트 텍스트 겹침 완벽 해결, 90도 수직 회전 라벨링, 엑셀 시트 내 고해상도 차트 자동 첨부 및 A열 슬림 폭 최적화**를 완벽하게 구축하고 전 파이프라인 검증을 완료하였습니다.

---

## 📁 디렉토리 아키텍처 (Clean Separation)

```text
D:\uno\1. 2026\1. BRK\Autobuild IW01_EV3\
├── 0. db/                                      # [DB] 기본 데이터베이스 및 캐시 저장소
│   ├── df_result_summary.gzip                  # 메타데이터/기상/GPS 병합 요약 캐시 (Pickle)
│   ├── df_result_summary.csv                   # 스프레드시트 호환 요약 CSV
│   └── list_obj_tires.gzip                     # 초단위 원시 제동 프로파일 객체 캐시
├── 2. fig/                                     # [FIG] 분석 흐름 순서대로 넘버링된 고해상도 차트 (총 21개)
│   ├── 01_01_Baseline_Performance_lane1.png    # [테마 1] Lane별 및 Wet/Dry 서페이스별 베이스라인
│   ├── ...                                     # 01_05_Wet, 01_06_Dry 분리 집계 차트
│   ├── 02_01_Control_Tire_vs_Temperature_Analysis.png # [테마 2] 노면온도 감인성(m/°C) 회귀선
│   ├── 03_01_Raw_Distance_vs_Index_Analysis_With_Temp.png # [테마 3] 실측거리 vs 지수 역전 진단
│   ├── 04_01_Recalibration_MethodA_vs_MethodB_Slope.png # [테마 4] 슬로프 차트 (라벨 겹침 제로 슬롯 배정)
│   ├── 04_06_MethodB_Recalibrated_Performance_Wet.png   # [테마 4] Wet 종합 랭킹 차트
│   ├── 04_07_MethodB_Recalibrated_Performance_Dry.png   # [테마 4] Dry 종합 랭킹 차트
│   ├── 05_01 ~ 05_04_Cross_Spec_Comparison_*.png        # [테마 5] 교차 대조 (X라벨 90도 회전 가독성 확보)
│   ├── 06_01_Braking_Spatial_Scatter_Analysis.png       # [테마 6] GPS 2D 제동 진입 좌표 분포
│   └── 06_02_Braking_Centroid_Deviation_Analysis.png   # [테마 6] 프로젝트별 중심점 편차 QC
└── EV3_IW01_Integrated_Braking_Analysis_Report.xlsx    # [MASTER EXCEL] 7개 시트 통합 마스터 리포트 (차트 내장)
```

---

## 🏛️ 신규 모듈화 아키텍처 구성 (`EV3_IW01/`)

| 번호 | 모듈 파일명 | 핵심 기능 및 주요 변경사항 | 주요 산출물 (Chart / Sheet) |
| :---: | :--- | :--- | :--- |
| **00** | [`00_EV3_IW01_make_result.py`](file:///D:/uno/Python/Projects/Braking_AutoBuild/EV3_IW01/00_EV3_IW01_make_result.py) | 원시 제동 시험 데이터 파싱, 기상 DB(대기/노면온도) 병합 및 `0. db` 자동 캐싱 | `0. db/df_result_summary.gzip` |
| **10** | [`10_EV3_IW01_analysis.py`](file:///D:/uno/Python/Projects/Braking_AutoBuild/EV3_IW01/10_EV3_IW01_analysis.py) | **총괄 분석 오케스트레이터 (Wrapper)**: 6대 모듈, `0. db` 로드, `2. fig` 저장, 통합 엑셀 마스터 빌더 원클릭 제어 | 파이프라인 총괄 관제 |
| **20** | [`20_EV3_IW01_surface_and_control_baseline.py`](file:///D:/uno/Python/Projects/Braking_AutoBuild/EV3_IW01/20_EV3_IW01_surface_and_control_baseline.py) | **[테마 1] 노면 및 로컬 콘트롤 기준 편차 분석**: Wet과 Dry를 절대로 섞지 않고 `Wet 통합`, `Dry 통합` 독립 집계 | `01_01_` ~ `01_06_`<br>Sheet: `Surface_Ctrl_Baseline` (이미지 2종) |
| **21** | [`21_EV3_IW01_temperature_sensitivity.py`](file:///D:/uno/Python/Projects/Braking_AutoBuild/EV3_IW01/21_EV3_IW01_temperature_sensitivity.py) | **[테마 2] 노면온도 의존성 및 감인성 분석**: 1차 선형 회귀 기울기($m \text{ [m/°C]}$) 및 피어슨 $r$ | `02_01_`<br>Sheet: `Temperature_Sensitivity` (이미지 1종) |
| **22** | [`22_EV3_IW01_discordance_diagnosis.py`](file:///D:/uno/Python/Projects/Braking_AutoBuild/EV3_IW01/22_EV3_IW01_discordance_diagnosis.py) | **[테마 3] 실측 거리 vs 지수 역전 현상 진단**: Discordant Pair 색출, 온도 보정 타당성 규명 | `03_01_`<br>Sheet: `Discordance_Diagnosis` (이미지 1종) |
| **23** | [`23_EV3_IW01_anchor_recalibration.py`](file:///D:/uno/Python/Projects/Braking_AutoBuild/EV3_IW01/23_EV3_IW01_anchor_recalibration.py) | **[테마 4] 공통 앵커(`EXT-2026-00147`) 재보정 (Method B)**: 슬로프 차트 동순위 Y슬롯 분리(글자 겹침 원천 차단), Wet/Dry 종합 랭킹 분리 | `04_01_` ~ `04_07_`<br>Sheet: `Anchor_Recalibration` (이미지 3종) |
| **24** | [`24_EV3_IW01_cross_spec_repeatability.py`](file:///D:/uno/Python/Projects/Braking_AutoBuild/EV3_IW01/24_EV3_IW01_cross_spec_repeatability.py) | **[테마 5] 동일 스펙 교차 의뢰서 반복 시험 대조**: X축 라벨 90도 수직 회전 및 하단 여백 확보(겹침 해소) | `05_01_` ~ `05_04_`<br>Sheet: `Cross_Spec_Repeatability` (이미지 1종) |
| **25** | [`25_EV3_IW01_spatial_gps_qc.py`](file:///D:/uno/Python/Projects/Braking_AutoBuild/EV3_IW01/25_EV3_IW01_spatial_gps_qc.py) | **[테마 6] 제동 진입 위치 GPS 공간 품질 QC**: 중심점(Centroid) 편차, 주행 일관성 진단 | `06_01_`, `06_02_`<br>Sheet: `Spatial_GPS_QC` (이미지 2종) |
| **30** | [`30_EV3_IW01_export_integrated_excel.py`](file:///D:/uno/Python/Projects/Braking_AutoBuild/EV3_IW01/30_EV3_IW01_export_integrated_excel.py) | **통합 엑셀 마스터 리포트 빌더**: 총 7개 시트 생성, A열 너비 슬림화(제목행 배제), 시트별 고해상도 차트 자동 삽입 | `EV3_IW01_Integrated_Braking_Analysis_Report.xlsx` |

---

## 🔬 주요 개선 사항 및 반영 결과

1. **Wet/Dry 서페이스 단위 독립 집계 (종합 Overall 평균 배제):**
   - 레인 집계 및 마스터 랭킹 시 물리적 마찰 메커니즘이 전혀 다른 Wet과 Dry를 한데 섞어 평균내지 않고, `Wet 통합`과 `Dry 통합`으로 엄격히 분리하여 왜곡을 원천 차단.
2. **슬로프 차트 라벨 겹침 원천 해결 (Slot Allocation):**
   - 동일 스펙 중복 등장 문제: `Dynamic_Label`(몰드/패턴/마크) 단위로 중복 데이터를 통합 집계.
   - 동순위 텍스트 겹침 문제: 순위가 같더라도 물리적 Y좌표 슬롯(`Y_Slot_A`, `Y_Slot_B`)을 1:1로 고르게 분리하고, 텍스트 라벨에 실제 순위(`#11`, `#24`)를 명확히 표기함으로써 가독성과 정확성을 동시 확보.
3. **교차 스펙 X축 라벨 가독성 개선:**
   - 긴 스펙명으로 인한 겹침 현상을 `rotation=90` 수직 회전 및 `subplots_adjust(bottom=0.30)` 여백 확보로 깔끔하게 정리.
4. **마스터 엑셀 리포트 고도화:**
   - 시트별 고해상도 분석 차트 10종 자동 배치 (`openpyxl.drawing.image.Image`).
   - A열 너비 자동 계산 시 상단 안내/제목행을 제외하고 본문 기준 최적 너비(10~22)로 고정하여 A열 비정상 확대 버그 원천 해결.

---

## 🚀 파이프라인 원클릭 실행 방법

```python
# D:\uno\Python\Projects\Braking_AutoBuild\EV3_IW01\10_EV3_IW01_analysis.py 실행
from EV3_IW01.10_EV3_IW01_analysis import run_ev3_iw01_analysis_pipeline

results = run_ev3_iw01_analysis_pipeline(
    list_group_cols=['TestTireMold', 'TestTirePTN', 'TestTireMark'],  # 동적 그룹화 계층
    plot=False,     # Figure 메모리 정리 (저장 후 plt.close() 실행)
    save=True,      # 2. fig 폴더에 넘버링된 21개 차트 저장
    excel=True,     # 루트 폴더에 시트별 차트가 삽입된 통합 엑셀 마스터 리포트 빌드
    b_print_log=True
)
```
