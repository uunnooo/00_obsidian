# 🗂️ 제동 성능 자동 분석 및 보정 시스템 위키 (Braking AutoBuild Wiki)
> [!info] **문서 정보**
> * **최종 수정일:** 2026-09-15 (화요일)
> * **태그:** #Braking #VehicleDynamics #DataEngineering #ExcelAutomation #EV3_IW01
> * **관련 가이드:** [[WORK_STATUS]] | [[EV3_IW01_Integrated_Braking_Analysis_Report.xlsx]]

이 위키는 기아 **`EV3_IW01`** 프로젝트 제동 평가 데이터의 기상 보정, 공통 앵커 캘리브레이션, 그리고 제동 시작점 GPS QC 정합성의 전체 공학적 거동 원리와 시스템 사상을 정립한 마스터 위키 노트입니다.

---

## 📁 디렉토리 아키텍처 및 데이터 흐름

```text
D:\uno\1. 2026\1. BRK\Autobuild IW01_EV3\
├── 0. db/                                      # [DB] 기본 데이터베이스 및 캐시 저장소
│   ├── df_result_summary.gzip                  # 메타데이터/기상/GPS 병합 요약 캐시 (Pickle)
│   ├── df_result_summary.csv                   # 스프레드시트 호환 요약 CSV
│   └── list_obj_tires.gzip                     # 초단위 원시 제동 프로파일 객체 캐시
├── 2. fig/                                     # [FIG] 분석 흐름 순서대로 넘버링된 고해상도 차트 (총 21개)
│   ├── 01_01 ~ 01_06_Baseline_Performance_*.png # [테마 1] Lane별 및 Wet/Dry 서페이스별 베이스라인
│   ├── 02_01_Control_Tire_vs_Temperature_Analysis.png # [테마 2] 노면온도 감인성(m/°C) 회귀선
│   ├── 03_01_Raw_Distance_vs_Index_Analysis_With_Temp.png # [테마 3] 실측거리 vs 지수 역전 진단
│   ├── 04_01_Recalibration_MethodA_vs_MethodB_Slope.png # [테마 4] 슬로프 차트 (라벨 겹침 제로)
│   ├── 04_06_MethodB_Recalibrated_Performance_Wet.png   # [테마 4] Wet 종합 랭킹 차트
│   ├── 04_07_MethodB_Recalibrated_Performance_Dry.png   # [테마 4] Dry 종합 랭킹 차트
│   ├── 05_01 ~ 05_04_Cross_Spec_Comparison_*.png        # [테마 5] 교차 대조 (X라벨 90도 회전)
│   ├── 06_01_Braking_Spatial_Scatter_Analysis.png       # [테마 6] GPS 2D 제동 진입 좌표 분포
│   └── 06_02_Braking_Centroid_Deviation_Analysis.png   # [테마 6] 프로젝트별 중심점 편차 QC
└── EV3_IW01_Integrated_Braking_Analysis_Report.xlsx    # [MASTER EXCEL] 7개 시트 통합 마스터 리포트 (차트 내장)
```

---

## 🌡️ 1. 콘트롤 타이어 온도 의존성 (Baseline Sensitivity)
> [!abstract] **핵심 개념**
> 기상 보정의 전제 조건은 **"온도가 변하면 타이어 고무 접지력이 변하고, 콘트롤 타이어가 이를 물리적으로 감인한다"**는 점입니다.

### 📈 노면 전용 온도 (Road Temperature Matching)
* **대기 온도 한계:** 기존 기상 결합 시 단순 '대기 기온'만 매칭하는 것은 고무와 아스팔트 간의 물리 현상을 대변하기에 불완전합니다.
* **노면 온도 매칭:** 본 시스템은 노면의 습윤 상태에 따라 날씨 DB에서 정밀한 노면 온도를 동적으로 결합시킵니다.
  * **마른 노면 (DRY):** `BRK Dry Asp` (아스팔트 직사광 가열 온도) 매칭
  * **젖은 노면 (WET):** `BRK Wet Asp` (수막 및 수온 기화 작용 반영 온도) 매칭

### 📊 레인별 온도 감인성 (Control Thermal Sensitivity)
실제 수집된 콘트롤 타이어(`C1`, `C2` 등)의 온도 의존성 1차 추세선식 및 물리적 거동 특성은 다음과 같습니다.
> [!note] **WET vs DRY 물리 거동 역전**
> * **WET 노면 (lane1, lane4):** 온도가 상승함에 따라 제동거리가 **우상향으로 증가**합니다. (기울기 $m \approx +0.11 \sim +0.15 \text{ m/°C}$)
>   * *이유:* 고온 수막 거동 저하 및 수온 상승에 따른 전단력 변동. 고온에서 주행한 타이어들에 **가산점(보정 지수 상승)**을 부여해야 공평합니다.
> * **DRY 노면 (lane7, lane8):** 온도가 상승함에 따라 제동거리가 **우하향으로 단축**됩니다. (기울기 $m \approx -0.05 \text{ m/°C}$)
>   * *이유:* 고온 아스팔트 위에서 고무의 연화(softening) 작용으로 실질 접지 면적이 넓어지는 열적 접지력 이득 발생. 고온 주행 타이어들에 **감점(보정 지수 하락)**을 주어야 공평합니다.

---

## 🧬 2. 성능 지수(%) 연산 및 역전 현상 (Discordance)
> [!quote] **"실측은 더 긴데 지수는 왜 더 높은가?"** -> [[EV3_IW01_Integrated_Braking_Analysis_Report.xlsx]] 참고

### 🧮 성능지수(Performance Index) 정의
오리지널 성능지수는 해당 타이어 주행 찰나의 **선형 보간된 가상 콘트롤 성능(Moving Target)**을 기준으로 상대 평가합니다.

$$\text{성능지수 (\%)} = \frac{\text{주행 시점의 선형 보간된 '가상 콘트롤 제동거리 (100\% 과녁)'}}{\text{실험 타이어의 '실측 제동거리'}} \times 100$$

### 🚨 역전 판정 조건 (Discordance Inversion)
데이터베이스 전수 비교 루프를 돌며 아래 조건에 해당하는 1:1 대조 쌍을 자동으로 색출합니다.

$$\text{Discordant} \iff (brk\_mean_A > brk\_mean_B) \land (index\_brk\_mean_A > index\_brk\_mean_B)$$

> [!check] **공학적 정당성 검증**
> 이 역전 현상(Discordance)은 보정 엔진이 **노면 온도 열세 조건에서 악전고투한 타이어 A에게 공평한 가산점을 가미해 억울한 성적 순위를 정상적으로 구제해 주었음을 반증하는 결정적 증거**입니다.

---

## ⚓ 3. 공통 앵커 기반 교차 재보정 (Method B)
> [!warning] **로컬 기준 보정의 한계 및 서페이스 분리 원칙**
> 각 의뢰서(세션)마다 사용된 콘트롤 타이어 제품군이 달라졌다면, 로컬 100% 지수끼리 직접 대조하는 것은 심각한 왜곡을 유발합니다. 또한 물리 메커니즘이 다른 **Wet과 Dry를 하나로 섞어 종합 평균(Overall)을 내는 것은 금지되며, 반드시 Surface별 독립 랭킹을 산출**해야 합니다.

### ⛓️ 체인 캘리브레이션 (Chain Recalibration)
교차 시험된 스파이 타이어인 **`ex-MC-AP7` (미쉐린, TestTireSpec: `EXT-2026-00147`)**을 만능 앵커(기준기)로 지정하여, 이 앵커가 획득한 오리지널 지수를 역수로 삼아 전 프로젝트의 지수를 상대적으로 수평 정합(Re-scale)시킵니다.

$$\text{재보정 지수} = \text{기존 지수} \times \left( \frac{100.0}{\text{해당 세션에서의 ex-MC-AP7 지수}} \right)$$

* **슬로프 차트 동순위 슬롯 배정 (Zero Overlap):**
  * 공동 순위(예: 공동 11위, 공동 24위) 발생 시 텍스트가 겹치는 문제를 해결하기 위해, 정렬 순서대로 1:1 고유 물리 Y슬롯을 배정하고 실제 순위(`#11`, `#24`)를 표기하여 완벽한 시각적 가독성 확보.

---

## 🗺️ 4. 제동 시작점 GPS 공간 품질 검증 (Spatial QC)
> [!example] **운전자 거동의 과학적 감시**
> 운전자가 매 주행마다 동일한 진입 좌표에서 가감속 정렬 및 제동 시작 타이밍을 준수했는지 감시하는 엄밀한 품질 관리(QC) 프로세스입니다.

### 📐 종방향(X) 및 횡방향(Y) 오차 분할
* **종방향 편차 ($PosX - mean\_x$):** 진입 규정 속도를 맞추기 위한 브레이크 패달 작동 타이밍 오차(Longitudinal Error).
* **횡방향 편차 ($PosY - mean\_y$):** 주행 차선의 중심선(Centerline)에서 좌우로 어긋나 쏠려 진입한 횡적 얼라인먼트 오차(Lateral Error).

$$\text{종합 공간 이탈 편차 (Euclidean Distance)} = \sqrt{\Delta X^2 + \Delta Y^2}$$

---

## 🔬 5. 동일 스펙 교차 의뢰서 반복 시험 정밀 대조 (Cross-Spec Comparison)
* **X축 라벨 90도 회전:** 복잡한 메타데이터(스펙, 마킹, 일시)가 겹치지 않도록 수직 회전(`rotation=90`) 및 30% 하단 마진 확보.
* 봄 vs 혹서기 제동거리 변동(+4.44m 밀림)을 확인하고, Method B 재보정 시 지수가 오차 없이 수렴함을 입증.

---

## 🏛️ 6. EV3_IW01 모듈화 아키텍처 및 마스터 엑셀 리포트
* **`00_EV3_IW01_make_result.py`:** 원시 데이터 파싱 및 `0. db` 자동 캐싱.
* **`10_EV3_IW01_analysis.py`:** 총괄 오케스트레이터. `0. db` 로드, `2. fig` 넘버링 차트 저장, 엑셀 빌더 연동.
* **`20` ~ `25` 모듈:** 6대 분석 테마 독립 모듈 (Wet/Dry 분리, 슬로프 슬롯 분리, 라벨 90도 회전).
* **`30_EV3_IW01_export_integrated_excel.py`:** 7개 시트 통합 마스터 리포트 빌더.
  * 시트별 우측(H~K열)에 핵심 분석 차트 10종 자동 삽입.
  * 상단 제목행을 배제하고 A열 너비를 4~22의 슬림 폭으로 최적화하여 가독성 극대화.

---

## 📂 옵시디언 볼트 위키 매핑
* **작업 현황 보고서:** [[WORK_STATUS]]
* **통합 엑셀 마스터 리포트:** [[EV3_IW01_Integrated_Braking_Analysis_Report.xlsx]]
* **넘버링 차트 저장소:** `D:\uno\1. 2026\1. BRK\Autobuild IW01_EV3\2. fig\`
* **데이터베이스 저장소:** `D:\uno\1. 2026\1. BRK\Autobuild IW01_EV3\0. db\`
