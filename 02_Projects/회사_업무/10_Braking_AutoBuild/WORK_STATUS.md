# 📌 제동 성능 자동 분석 프로젝트 (Braking_AutoBuild) 작업 진행 현황 및 아키텍처

---

## 📅 작업 완료 요약 (2026년 9월 17일 목요일 기준)

사용자의 피드백 및 엔지니어링 고도화 요구사항을 100% 반영하여 11대 테마, 13대 전문 분석 모듈, 12개 시트 통합 엑셀 마스터 리포트 및 **83종 고해상도 시각화 생태계**를 완성하였습니다:

1. **[테마 1: Surface_Ctrl_Baseline 차트 실측거리 병기 고도화]**:
   - `20_EV3_IW01_surface_and_control_baseline.py`의 막대 차트(`01_01`~`01_06`) 레이블을 `{지수}% ({실측거리}m)` 포맷(예: `105.2% (30.17m)`)으로 변경하여 직관성 극대화.
   - X축 마진을 동적으로 확장하여 텍스트 잘림 현상 원천 방지.
2. **[테마 5 개편: 콘트롤 vs 테스트 타이어 재현성(Repeatability) 완전 분리]**:
   - `24_EV3_IW01_cross_spec_repeatability.py` 모듈에서 콘트롤 타이어(세션 간 반복성 및 세션 내 C1 vs C2 드리프트)와 테스트 타이어(Method A/B 교차 의뢰서 일관성)를 명확히 분리하여 4종 차트(`05_01`~`05_04`)로 개편.
3. **[테마 7: 8회 반복 제동 순차 성능 변화 (용어 표준화 완료)]**:
   - `26_EV3_IW01_run_degradation.py` 모듈 구축. 1회당 1행 마스터 런 DB(`df_result_runs`, 240행) 기반 8회 연속 제동 추세선 및 변동 기울기(m/run), CV%, 최대 편차폭(Spread) 산출.
   - 사용자 피드백 반영: '열화/내구성' 용어 전면 배제 ➔ **'반복 횟수별 성능 변화'**, **'성능 변동량'**, **'변동 기울기'**, **'후반 밀림 경향(Fade 경향)'**, **'초고안정형'**으로 전면 개편.
   - 노면별 4종 분리 및 몰드-패턴-마킹(`Dynamic_Label`) 라벨 순 정렬 차트(`07_01`, `07_02`, `07_03` 총 9종 차트).
4. **[테마 8: 노면별 Mu-Drop 손실거리 및 환경 보정 왜곡 진단]**:
   - `27_EV3_IW01_mudrop_analysis.py` 모듈 구축. 실측 손실거리 vs 환경 보정 손실거리 분리 표기.
   - 콘트롤 타이어의 지수 100% 고정에 따른 '분모 0 왜곡(Zero-denominator Artifact)' 메커니즘을 공학적으로 규명하고 주석 명시.
   - 노면별 취약성 순위(Lane 4 > Lane 1 > Lane 7 > Lane 8) 및 노면별 단독 차트 4종(`08_01`~`08_04`) 생성.
5. **[테마 9: 속도 구간별 성능 분할 & 감속도 차이(Δg) vs 상대지수 상관성 분석]**:
   - `28_EV3_IW01_speed_zone_analysis.py` 모듈 구축 및 대규모 고도화:
     - 고속(100~50 km/h) vs 저속(50~0 km/h) 제동거리 분할 비율($\approx 63\% : 37\%$) 및 감속도 변화율($\Delta g = g_{low} - g_{high}$) 프로파일링.
     - **[신규 상관분석 엔진]**: 고속 대비 저속 감속도 차이($\Delta g$)와 시험 의뢰서 내 기준품 대비 상대 성능지수(Index, %) 간의 4대 노면별 피어슨 상관분석($r$, $R^2$, $p$-value, 선형 회귀식) 구축.
     - **[물리 메커니즘 규명]**:
       - Lane 7 (Dry 아스팔트, $r = +0.529, R^2 = 0.280, p = 0.0424 < 0.05$): 통계적으로 유의미한 양(+)의 상관관계 입증 (후반 정지 직전까지 블록 강성과 점착 마찰을 유지하여 감속도를 끌어올린 스펙이 전체 제동거리를 효과적으로 단축).
       - Lane 4 (Wet 저마찰, $r = -0.347, R^2 = 0.120, p = 0.0825 < 0.10$): 통계적 경향 음(-)의 상관성 규명 (고속 수막 슬립으로 감속도가 무너진 타이어일수록 저속에서 접지력을 회복해도 $\Delta g$만 벌어지고 고속 손실을 만회하지 못함).
       - Lane 1 (Wet 고마찰, $r = -0.123$): 비유의.
       - Lane 8 (Dry, $r = +0.513$): 양(+)의 경향성.
     - **[차트 사실주의(Fact-Only) 적용]**: 사용자 피드백을 반영하여 차트 내부 의견/소견 텍스트 박스를 완전 삭제하고, 순수 정량 통계 수치만 콤팩트하게 표기하여 데이터 포인트와의 시각적 간섭 제로화.
     - **[신규 차트 5종 추가]**: 4대 노면 2x2 종합 산점도(`09_05_Speed_Zone_AccDiff_vs_Index_Correlation.png`) 및 노면별 단독 4종(`09_05_AccDiff_vs_Index_lane1 ~ lane8.png`) 생성 (테마 9 차트 총 9종).
     - **[엑셀 시트 섹션 2 신설]**: `Speed_Zone_Analysis` 시트에 상대 성능지수 컬럼 추가, 스펙 하이라이트 서식 적용 및 하단에 상관분석 통계 요약표 구축.
6. **[테마 10: 표면 기여도 의뢰번호 라벨링 및 4대 스펙군 하이라이트 구축]**:
   - `29_EV3_IW01_surface_contribution.py` 모듈 고도화:
     - **[의뢰번호 병기 라벨링]**: 동일 규격 반복 시험 간 혼선을 방지하기 위해 Y축 라벨을 `[TestReqNo] Dynamic_Label (TireSet)` 포맷으로 전면 개편.
     - **[4대 주력 스펙군 하이라이트]**:
       - `1st-IW01`: 선명한 블루 (`#1f77b4` / 엑셀 `#D9E1F2`, 폰트 `002060`)
       - `2nd-IW01`: 선명한 오렌지 (`#e67e22` / 엑셀 `#FCE4D6`, 폰트 `C65911`)
       - `2nd-QW01A`: 선명한 그린 (`#27ae60` / 엑셀 `#E2EFDA`, 폰트 `375623`)
       - `2nd-QW01B`: 선명한 레드 (`#c0392b` / 엑셀 `#FADBD8`, 폰트 `900C3F`)
       - 기준품 `ex-MC-AP7`: 다크 네이비, 수입품 `ex-PI-CW3`: 퍼플
     - **[시각화 13종 유지 및 무결성 확보]**: 100% 누적 바 차트, 감속도 레벨 대조, Mu-Drop 기여율, 의뢰서별 속도 감속도 프로파일 13종 완벽 지원.
7. **[테마 11: 타이어 스펙별 고속 vs 저속 성능 분할 및 전 노면 종합 대조 매트릭스]**:
   - `32_EV3_IW01_tire_speed_zone_analysis.py` 모듈 구축.
   - 25개 전수 스펙 기준 제동거리, 고속/저속 감속도, $\Delta g$, 유지율 및 4대 노면 종합 매트릭스(`Tire_Speed_Zone_Analysis` 시트 및 차트 5종 `11_01`~`11_05`) 완성.
8. **[통합 엑셀 마스터 리포트 12개 시트 & 83종 차트 생태계 완성]**:
   - `EV3_IW01_Integrated_Braking_Analysis_Report.xlsx`에 12개 데이터 시트 구축 및 83종 고해상도 차트 전수 자동 임베딩.
   - `10_EV3_IW01_Integrated_Braking_Analysis_Report.md` 마크다운 기술 백서에 45개 이상 산출 근거 표 및 83종 차트 완벽 임베딩.
   - 옵시디언 볼트(`D:\00_obsidian`) 어태치먼트 폴더에 83종 차트 100% 이중 동기화 완료.

---

## 📁 디렉토리 아키텍처 (Clean Separation)

```text
D:\uno\1. 2026\1. BRK\Autobuild IW01_EV3\
├── 0. db/                                             # [DB] 데이터베이스 및 고속 압축 캐시 저장소
│   ├── df_result_summary.gzip                         # 세션 단위 요약 캐시 (Pickle Gzip)
│   ├── df_result_summary.csv                          # 스프레드시트 호환 세션 요약 CSV
│   ├── df_result_runs.gzip                            # 제동 1회당 1행 마스터 런 DB 캐시
│   ├── df_result_runs.csv                             # 240개 전수 런 상세 CSV
│   └── list_obj_tires.gzip                            # 초단위 원시 제동 프로파일 객체 캐시
├── 2. fig/                                            # [FIG] 11대 테마 83종 고해상도 차트 저장소
│   ├── 01_01 ~ 01_06_Baseline_Performance_*.png        # [테마 1] Lane별 및 서페이스별 베이스라인 (실측거리 병기, 6종)
│   ├── 02_01_Control_Tire_vs_Temperature_Analysis.png # [테마 2] 노면온도 감인성(m/°C) 회귀선 (1종)
│   ├── 03_01_Raw_Distance_vs_Index_Analysis_With_Temp.png # [테마 3] 실측거리 vs 지수 역전 진단 (1종)
│   ├── 04_01_Recalibration_MethodA_vs_MethodB_Slope.png # [테마 4] 슬로프 차트 (라벨 겹침 제로, 1종)
│   ├── 04_06 ~ 04_07_MethodB_Recalibrated_*.png        # [테마 4] Wet/Dry 종합 랭킹 차트 (2종)
│   ├── 05_01 ~ 05_04_Cross_Spec_Comparison_*.png       # [테마 5] 콘트롤 vs 테스트 타이어 재현성 분리 차트 (4종)
│   ├── 06_01 ~ 06_05_Braking_Spatial_*.png            # [테마 6] GPS 2포인트 시작/정지 공간 QC 및 요 거동 (5종)
│   ├── 07_01_Run_Trend_*.png (4종)                    # [테마 7] 노면별 8회 런 순차 제동거리 추세선 (4종)
│   ├── 07_02_Spec_Degradation_Slope_Comparison.png    # [테마 7] 스펙별 성능 변동 기울기 & 편차폭 종합 (1종)
│   ├── 07_03_Lane_Degradation_*.png (4종)             # [테마 7] 노면별 타이어 세트 변동 기울기 & 편차폭 (4종)
│   ├── 08_01 ~ 08_04_MuDrop_Analysis_*.png (4종)      # [테마 8] 노면별 Mu-Drop 실측/보정 대조 & 왜곡 진단 (4종)
│   ├── 09_01 ~ 09_04_Speed_Zone_Analysis_*.png (4종)   # [테마 9] 고속 vs 저속 구간 분할 & 감속도 변화율 (4종)
│   ├── 09_05_Speed_Zone_AccDiff_vs_Index_Correlation.png # [테마 9 신규] 4대 노면 2x2 감속도차이 vs 상대지수 상관성 종합 차트 (1종)
│   ├── 09_05_AccDiff_vs_Index_lane1 ~ lane8.png (4종) # [테마 9 신규] 노면별 단독 감속도차이 vs 상대지수 상관성 차트 (4종)
│   ├── 10_01_Surface_Speed_Contribution_Ratio.png     # [테마 10] 노면별 고속 vs 저속 성능 기여도(비율) 100% 누적 가로막대 (1종)
│   ├── 10_02_Surface_Deceleration_Level_Comparison.png# [테마 10] 고속 vs 저속 감속도 레벨 대조 & 속도 구간별 감속도 변화량 (1종)
│   ├── 10_03_Surface_MuDrop_Impact_Contribution.png   # [테마 10] Mu-Drop 손실 기여율 100% 누적 막대 & 영향도 등급 대조 (1종)
│   ├── 10_04_Surface_Speed_Acc_Profile_By_Req.png     # [테마 10] 의뢰서별 속도 구간 감속도 프로파일 2x2 서브플롯 (1종)
│   ├── 10_04_Speed_Acc_lane1 ~ lane8.png (4종)        # [테마 10] 노면별 단독 의뢰서 감속도 프로파일 (4종)
│   ├── 10_05_Surface_MuDrop_Ratio_Comparison.png     # [테마 10] 노면별 전수 타이어 Mu-Drop 손실 기여율 2x2 서브플롯 (1종)
│   ├── 10_05_MuDrop_Ratio_lane1 ~ lane8.png (4종)     # [테마 10] 노면별 단독 타이어 세트 Mu-Drop 손실 기여율 (4종)
│   ├── 11_01 ~ 11_04_Tire_Spec_Speed_Zone_*.png (4종)  # [테마 11] 타이어 스펙별 고속 vs 저속 노면별 복합 차트 (4종)
│   └── 11_05_Tire_Spec_Speed_Zone_Overall_Comparison.png # [테마 11] 4대 노면 타이어 스펙별 Δg 2x2 종합 대조 차트 (1종)
├── EV3_IW01_Integrated_Braking_Analysis_Report.xlsx   # [MASTER EXCEL] 12개 시트 통합 마스터 리포트 (차트 83종 내장)
└── EV3_IW01_Integrated_Braking_Analysis_Report.md     # [MASTER MD] 옵시디언 이중 동기화 마크다운 리포트
```

---

## 🏛️ 신규 모듈화 아키텍처 구성 (`EV3_IW01/`)

| 번호 | 모듈 파일명 | 핵심 엔지니어링 역할 및 담당 테마 | 주요 산출물 (Chart / Sheet) |
| :---: | :--- | :--- | :--- |
| **00** | [`00_EV3_IW01_make_result.py`](file:///D:/uno/Python/Projects/Braking_AutoBuild/EV3_IW01/00_EV3_IW01_make_result.py) | 원시 제동 시험 데이터 파싱, 기상 DB(대기/노면온도) 병합 및 캐싱 | `0. db/df_result_summary.gzip` |
| **10** | [`10_EV3_IW01_analysis.py`](file:///D:/uno/Python/Projects/Braking_AutoBuild/EV3_IW01/10_EV3_IW01_analysis.py) | **총괄 오케스트레이터 (Wrapper)**: 13대 모듈 로드, 83개 차트 저장, 엑셀/마크다운 마스터 빌더 원클릭 제어 | 파이프라인 통합 관제 |
| **20** | [`20_EV3_IW01_surface_and_control_baseline.py`](file:///D:/uno/Python/Projects/Braking_AutoBuild/EV3_IW01/20_EV3_IW01_surface_and_control_baseline.py) | **[테마 1] 노면 및 로컬 콘트롤 편차 분석**: Wet/Dry 독립 분리, 막대에 실측거리 `(xx.xx m)` 병기 | `01_01_` ~ `01_06_`<br>Sheet: `Surface_Ctrl_Baseline` (6종) |
| **21** | [`21_EV3_IW01_temperature_sensitivity.py`](file:///D:/uno/Python/Projects/Braking_AutoBuild/EV3_IW01/21_EV3_IW01_temperature_sensitivity.py) | **[테마 2] 노면온도 의존성 및 감인성 분석**: 1차 선형 회귀 기울기($m \text{ [m/°C]}$) 및 피어슨 $r$ | `02_01_`<br>Sheet: `Temperature_Sensitivity` (1종) |
| **22** | [`22_EV3_IW01_discordance_diagnosis.py`](file:///D:/uno/Python/Projects/Braking_AutoBuild/EV3_IW01/22_EV3_IW01_discordance_diagnosis.py) | **[테마 3] 실측 거리 vs 지수 역전 현상 진단**: Discordant Pair 색출, 온도 보정 타당성 규명 | `03_01_`<br>Sheet: `Discordance_Diagnosis` (1종) |
| **23** | [`23_EV3_IW01_anchor_recalibration.py`](file:///D:/uno/Python/Projects/Braking_AutoBuild/EV3_IW01/23_EV3_IW01_anchor_recalibration.py) | **[테마 4] 공통 앵커(`EXT-2026-00147`) 재보정 (Method B)**: 슬로프 차트 동순위 Y슬롯 분리(글자 겹침 원천 차단), Wet/Dry 종합 랭킹 분리 | `04_01_` ~ `04_07_`<br>Sheet: `Anchor_Recalibration` (3종) |
| **24** | [`24_EV3_IW01_cross_spec_repeatability.py`](file:///D:/uno/Python/Projects/Braking_AutoBuild/EV3_IW01/24_EV3_IW01_cross_spec_repeatability.py) | **[테마 5 개편] 콘트롤 vs 테스트 타이어 재현성 분리 평가**: 세션 간/세션 내 C1 vs C2 편차 및 Method A/B 수렴성 검증 | `05_01_` ~ `05_04_`<br>Sheet: `Cross_Spec_Repeatability` (4종) |
| **25** | [`25_EV3_IW01_spatial_gps_qc.py`](file:///D:/uno/Python/Projects/Braking_AutoBuild/EV3_IW01/25_EV3_IW01_spatial_gps_qc.py) | **[테마 6] 제동 시작/정지 GPS 2포인트 공간 QC 및 요(Yaw) 거동**: 횡방향(X)/종방향(Y) 분할 진단, 요 모션 무관성 입증 | `06_01_` ~ `06_05_`<br>Sheet: `Spatial_GPS_QC` (5종) |
| **26** | [`26_EV3_IW01_run_degradation.py`](file:///D:/uno/Python/Projects/Braking_AutoBuild/EV3_IW01/26_EV3_IW01_run_degradation.py) | **[테마 7] 반복 횟수별 성능 변화 분석**: 제동 1회당 1행 마스터 DB(`df_result_runs`, 240행), 런 추세선, 변동 기울기, 편차폭 정량화 | `07_01_` ~ `07_03_` (9종)<br>Sheet: `Run_Degradation` |
| **27** | [`27_EV3_IW01_mudrop_analysis.py`](file:///D:/uno/Python/Projects/Braking_AutoBuild/EV3_IW01/27_EV3_IW01_mudrop_analysis.py) | **[테마 8] 노면별 Mu-Drop 손실거리 및 환경 보정 왜곡 진단**: 실측 vs 보정 손실거리 대조, 콘트롤 분모 0 왜곡 규명 | `08_01_` ~ `08_04_` (4종)<br>Sheet: `MuDrop_Analysis` |
| **28** | [`28_EV3_IW01_speed_zone_analysis.py`](file:///D:/uno/Python/Projects/Braking_AutoBuild/EV3_IW01/28_EV3_IW01_speed_zone_analysis.py) | **[테마 9] 속도 구간별 성능 분할 & 감속도 차이(Δg) vs 상대지수 상관성 분석**: 고속/저속 구간 분할, 감속도 변화율, 노면별 상관성 분석 2x2 종합 및 단독 차트 | `09_01_` ~ `09_05_` (9종)<br>Sheet: `Speed_Zone_Analysis` |
| **29** | [`29_EV3_IW01_surface_contribution.py`](file:///D:/uno/Python/Projects/Braking_AutoBuild/EV3_IW01/29_EV3_IW01_surface_contribution.py) | **[테마 10] 노면별 기여율, 감속도 레벨 차이, Mu-Drop 영향도 및 의뢰서별 속도 프로파일 대조**: 의뢰번호 병기 라벨링 및 4대 주력 스펙군 시각 하이라이트 | `10_01_` ~ `10_05_` (13종)<br>Sheet: `Surface_Contribution` |
| **32** | [`32_EV3_IW01_tire_speed_zone_analysis.py`](file:///D:/uno/Python/Projects/Braking_AutoBuild/EV3_IW01/32_EV3_IW01_tire_speed_zone_analysis.py) | **[테마 11 신규] 타이어 스펙별 고속 vs 저속 성능 분할 및 감속도 프로파일 종합 분석**: 25개 전수 스펙 기준 제동거리, 고속/저속 감속도, $\Delta g$, 유지율 및 4대 노면 종합 매트릭스 | `11_01_` ~ `11_05_` (5종)<br>Sheet: `Tire_Speed_Zone_Analysis` |
| **30** | [`30_EV3_IW01_export_integrated_excel.py`](file:///D:/uno/Python/Projects/Braking_AutoBuild/EV3_IW01/30_EV3_IW01_export_integrated_excel.py) | **통합 엑셀 마스터 리포트 빌더**: 12개 시트 생성, A열 슬림화, 고해상도 차트 83종 전수 자동 삽입 | `EV3_IW01_Integrated_Braking_Analysis_Report.xlsx` |
| **31** | [`31_EV3_IW01_export_integrated_markdown.py`](file:///D:/uno/Python/Projects/Braking_AutoBuild/EV3_IW01/31_EV3_IW01_export_integrated_markdown.py) | **통합 마크다운 마스터 리포트 빌더**: 45개+ 산출 근거 표 + 83개 차트 수록, 볼트 온디맨드 이중 동기화(`sync_obsidian`) | `10_EV3_IW01_Integrated_Braking_Analysis_Report.md` |
