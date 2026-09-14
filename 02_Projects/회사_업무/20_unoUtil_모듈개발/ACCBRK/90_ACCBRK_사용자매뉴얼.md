---
title: "90_ACCBRK 사용자 매뉴얼 및 종합 가이드라인"
aliases:
  - "ACCBRK"
  - "ACCBRK_사용자매뉴얼"
  - "90_ACCBRK_사용자매뉴얼"
---

# 🏎️ VT_ACCBRK 통합 실차 성능 분석 시스템: 실무 사용자 매뉴얼

본 시스템은 실차 제동 및 가속 시험 데이터를 정밀 가공하여 기술적 인사이트를 도출하는 4개의 핵심 모듈로 구성됩니다. **개별 분석(Tire) → 검증(Plotter_T) → 통합 및 보정(Project) → 비교 리포팅(Plotter_P)**으로 이어지는 완벽한 아키텍처를 경험해 보세요.

---

## 🏛️ 제0계층: 시스템 아키텍처 및 전체 분석 흐름

이 시스템은 거친 원시 데이터(Raw Data)로부터 최종 의사결정 리포트까지의 과정을 **3단계 공정**으로 정의합니다.



### 1. 전처리 및 개별 분석 단계 (Ready to Core)
* **Raw Data Ingestion**: 계측기(VBOX 등)에서 추출된 시계열 데이터($V$, $a$)를 시스템에 입력합니다.
* **Signal Processing**: Wavelet Denoising으로 가속도 노이즈를 제거하고, `detect_test_segments` 알고리즘이 수만 행의 데이터 중 실제 브레이크/가속 페달을 밟은 구간만 자동으로 찾아냅니다.
* **Reliability Check**: `select_valid_runs` 함수가 중앙값 기반 편차 분석을 통해 운전자가 실수한 데이터를 걸러내고 가장 신뢰도 높은 데이터셋을 구성합니다.

### 2. 프로젝트 통합 및 보정 단계 (Integration & Normalization)
* **Data Aggregation**: 서로 다른 날짜, 다른 장소에서 시험된 개별 타이어 분석 객체들을 `VT_ACCBRK_PROJECT`라는 하나의 컨테이너에 수집합니다.
* **Environmental Correction**: 시험 중간중간 배치된 **콘트롤 타이어(Reference)**의 성능 변화를 시계열로 추적하여, 노면 온도 및 외기 환경 변화에 따른 오차를 선형 보간(Linear Interpolation) 알고리즘으로 상쇄합니다.

### 3. 기술 인사이트 및 리포팅 단계 (Action & Insight)
* **Performance Indexing**: 절대 수치($m$, $g$)를 기준 타이어 대비 % 점수(Index)로 변환하여 성능 서열을 명확히 합니다.
* **Behavioral Decoding**: 슬립 분포(PDF)와 노면 대응력(Mu-drop) 시각화를 통해 "왜 이 타이어의 제동력이 우수한가?"에 대한 물리적 근거를 도출합니다.

---

## 🪄 제1계층: 분석 및 관리 모듈 상세 가이드

### 🛠️ 모듈 1. VT_ACCBRK_TIRE (단일 타이어 물리 분석 엔진)
타이어 하나에 대한 5대 성능 항목(제동, 가속, 대역 가속, 구간 비중, 노면 대응)을 정밀 분석합니다.

| 함수명 | 기능 (Pain Point Killer) | 입력 인자 (Required) | 핵심 키워드 인자 (Options & Detailed) | 출력 (Output) |
| :--- | :--- | :--- | :--- | :--- |
| `__init__` | 데이터 로드 및 가속도/거리 채널 자동 생성 | `df_raw` (데이터) | **sr**: 샘플링레이트(기본 100)<br>**unit_ax**: 가속도 단위('g', 'ms2')<br>**col_vel**: 속도 컬럼명 지정<br>**slip**: 슬립계산 여부(True/False)<br>**weather**: 기상 데이터프레임 병합 | 분석 인스턴스 |
| `detect_test_segments` | 수만 행 중 실제 시험 구간만 칼같이 추출 | `target`: [시작, 끝] 속도 | **ws**: 가속도 평활화 윈도우 크기(기본 10)<br>**min_sec**: 유효 구간 최소 지속 시간(기본 1.0)<br>**max_sec**: 유효 구간 최대 허용 시간(기본 20.0)<br>**filter**: Wavelet 필터 적용 여부(True/False) | 태깅된 데이터셋 |
| `select_valid_runs` | 운전자 실수 등 이상치 제거 및 상위 N개 선별 | `valid_count` (개수) | **mode**: 'brk' 또는 'acc' 자동 판별 기준<br>**metric**: 선별 기준 지표(거리 혹은 시간) | 유효 데이터 (EffNum) |
| `analysis_accbrk` | 가장 기본이 되는 제동 거리 및 가속 시간 산출 | - | **custom_report_items**: 추가 집계 항목 리스트<br>(예: [('Peak_G', 'AccForward', 'max')]) | 요약 통계량 |
| `analysis_acceleration`| 속도 대역별(100-90 등) 가속 성능 정밀 분석 | `interval` (간격) | **interval**: 속도 대역 나눌 간격(기본 10.0)<br>**unit**: 결과값 가속도 단위 지정 | 대역별 평균 가속도 |
| `analysis_split_speed` | 고속/저속 구간별 제동 기여도 및 응답성 분석 | `vel_split` (기준속도) | **vel_split**: 고/저속 분할 속도 임계값(기본 50.0) | 구간별 거리/가속도 |
| `analysis_slip_speed_pdf`| ABS 제어 정밀도 및 슬립 밀도 확률 분석 | - | **pos**: 분석 위치('front', 'rear', 'all', 'each')<br>**bw**: KDE 대역폭(기본 0.2)<br>**bin**: PDF 포인트 개수(기본 500)<br>**xlim**: 분석할 슬립 범위(기본 [0, 30]) | 슬립 PDF 데이터 |
| `analysis_mu_drop` | 노면 변화(Mu-drop) 시점 포착 및 손실 분석 | `ch_wa` (휠가속도 채널) | **ch_wa**: 감시할 휠 가속도 채널(기본 'WAFL')<br>**ncl**: KMeans 클러스터 수(기본 2)<br>**init**: KMeans 초기화 방식('k-means++')<br>**out**: 이상치 제거 여부(True/False) | Mu-drop 거리 손실 |

### 🏛️ 모듈 3. VT_ACCBRK_PROJECT (통합 관리 및 보정 엔진)
여러 타이어를 조합하고 환경 변화를 상쇄하여 공정한 성능 순위를 산출합니다.

| 함수명 | 기능 (Pain Point Killer) | 입력 인자 (Required) | 핵심 키워드 옵션 (Detailed) | 출력 (Output) |
| :--- | :--- | :--- | :--- | :--- |
| `add_tire` | 분석 완료된 객체를 프로젝트에 등록 | `obj` (Tire 인스턴스) | **tire**: 프로젝트용 별칭(중복 시 덮어쓰기 주의)<br>**copy**: deepcopy 수행 여부(기본 True) | 통합 프로젝트 객체 |
| `add_tire_file` | 저장된 `.tir` 파일을 불러와 프로젝트에 합침 | `path` (파일/폴더 경로) | **file**: 특정 파일 혹은 폴더 경로 선택<br>**tire**: 로드 시 부여할 고유 이름 | 로드된 객체들 |
| `cal_corrected` | **[핵심]** 환경 변화 보정 및 상대 지수 산출 | - | **ref_kwd**: 콘트롤 타이어 식별 키워드(기본 'c')<br>**inverse**: 점수 역전 여부(제동 거리 분석 시 필수 True)<br>**col_target_positive**: 클수록 좋은 지표 리스트<br>**col_target_negative**: 작을수록 좋은 지표 리스트<br>**col_seq**: 시계열 정렬 기준 컬럼(기본 'Datetime') | 보정 완료 데이터셋 |
| `save_pjt` | 분석 중인 프로젝트 전체 상태를 압축 저장 | `path` (저장 경로) | **path**: 파일명 혹은 폴더 경로(자동 이름 생성 지원)<br>**compresslevel**: gzip 압축률(기본 9) | `.pjt` 통파일 |
| `load` (classmethod) | 기존 저장된 프로젝트 복원 | `path` (파일 경로) | **path**: 불러올 `.pjt` 파일의 물리적 경로 | 복원된 프로젝트 객체 |

---

## 🎨 제2계층: 시각화 계층 (Visualization Layer) - 상세 그래픽 가이드

시각화 모듈은 분석 결과를 인간이 이해할 수 있는 **기술적 통찰(Insight)**로 변환합니다. 모든 시각화 함수는 공통적으로 `save`(저장경로), `html`(인터랙티브 여부), `close`(메모리해제) 인자를 지원합니다.

### 🖼️ 모듈 2. PLOTTER_TIRE (단일 타이어 검증 플로터)
분석된 개별 타이어의 데이터 품질과 물리적 거동을 시각적으로 검증합니다.

| 함수명 | 기능 (What it solves) | 핵심 키워드 옵션 (Detailed) | 상황별 옵션 활용 팁 |
| :--- | :--- | :--- | :--- |
| `accbrk` | 추출된 시험 구간의 타당성 검토 | **show**: 제동거리/가속시간 텍스트 표시 여부<br>**x_off**: 텍스트 표기 X축 오프셋 비율<br>**title**: 그래프 메인 제목 지정 | `show=True`로 구간별 거리($m$)를 즉시 확인 |
| `acceleration` | 속도 대역별 가속 분포 및 트렌드 확인 | **palette**: 색상 테마 지정('tab10' 등)<br>**jitter**: 데이터 포인트 좌우 흩뿌림 정도<br>**meanprops**: 평균 마커 스타일 지정 | 박스플롯과 평균 연결선으로 가속의 선형성을 확인 |
| `split_speed` | 고속/저속 영역의 물리량 상관관계 분석 | **alpha**: 포인트 투명도 조절<br>**sharex**: X축 공유 여부(기본 False) | 시간-속도, 속도-가속도 2중 차트로 제어 특성 파악 |
| `slip_check` | 휠 속도 동기화 및 센서 이상 유무 확인 | **legend**: 범례 표시 여부 및 위치<br>**figsize**: 그래프 캔버스 크기 조정 | 차량 속도 대비 4륜의 휠 속도를 겹쳐서 센서 튐 확인 |
| `slip_speed` | 슬립율 확률 밀도(PDF) 정밀 시각화 | **color**: PDF 곡선 색상 지정<br>**xlim**: X축(Slip Ratio) 범위 제한<br>**box_props**: 통계 텍스트 박스 스타일 | 최빈값(Mode)과 1-Sigma 영역을 통해 ABS 안정성 검증 |
| `mu_drop` | 노면 변화 구간을 2D/3D로 입체 분석 | **cmap**: 클러스터 컬러맵 테마('viridis', 'coolwarm')<br>**show**: 분석 수치(텍스트) 오버레이 여부<br>**close**: 저장 후 피규어 닫기 활성화 | 노면 변화로 인한 '황금색 거리 손실 영역' 확인 |

### 📊 모듈 4. PLOTTER_PROJECT (다중 타이어 비교 리포터)
여러 타이어 간의 상대적 성능 우위를 비교하고 리포트용 차트를 생성합니다.

| 함수명 | 기능 (What it solves) | 핵심 키워드 옵션 (Detailed) | 데이터 해석의 포인트 |
| :--- | :--- | :--- | :--- |
| `compare_braking` | 보정 전(실측) vs 보정 후 성능 대조 | **col_dist**: 비교 기준 컬럼(기본 'brk_mean')<br>**sharey**: Y축 타이어 리스트 공유 여부 | 보정 후 순위가 바뀌었는지(환경 영향) 확인 |
| `compare_index_braking` | 성능 지수(%) 기반의 최종 서열화 | **col_tire**: 타이어 세트 식별 컬럼명<br>**style**: 그래프 스타일 테마('minimal_x') | 기준 타이어(100%) 대비 우열을 한눈에 파악 |
| `compare_acceleration` | 속도 대역별 가속 트렌드 역전 구간 탐색 | **cmap**: 컬러맵 테마 지정<br>**zorder**: 레이어 적층 순서 제어<br>**alpha**: 트렌드 라인 투명도 | 사각형 마커 위치로 특정 속도의 접지 효율 확인 |
| `compare_split_distance`| 고속/저속 구간별 제동 거리 기여도 비교 | **width**: 바 너비(기본 0.6)<br>**label**: 각 구간(High/Low) 범례 이름 | 초기 제동 응답성이 좋은 타이어(High-speed 비중) 선별 |
| `compare_slip_pdf` | 타이어별 슬립 안정성 Ridgeline 비교 | **h**: 곡선 간 겹침 정도(기본 -0.7)<br>**xlim**: X축 표시 범위 제한(0~30)<br>**cmap**: 타이어별 색상 구분 컬러맵 | 산맥 모양이 왼쪽으로 좁게 솟을수록 우수한 제어 |
| `compare_mudrop_dist` | 노면 변화 강건성(Robustness) 비교 | **col_dist_mudrop**: 손실 거리 컬럼명 지정<br>**alpha**: 누적 바의 투명도 | 붉은색 '손실 거리'가 짧을수록 안전한 타이어임 |

---

## 🛡️ 실무자를 위한 퀵 가이드 및 안전망

> **[심리적 안전망: 시각화 팁]**
> * **"그래프가 깨져 보여요"**: `plt()` 함수 호출 시 `close=True`를 주면 대량의 그래프 생성 시 메모리 오류를 방지할 수 있습니다.
> * **"특정 구간만 저장하고 싶어요"**: `save` 인자에 경로를 주면 파일명이 규칙(`get_path`)에 따라 자동 생성되어 저장됩니다.
> * **"인터랙티브하게 보고 싶어요"**: `html=True` 옵션을 사용하면 웹브라우저에서 마우스 오버로 상세 수치를 확인할 수 있습니다.

### 🎯 나의 분석 목적별 함수 매칭
| 분석 목적 | 추천 함수 | 비고 |
| :--- | :--- | :--- |
| **분석된 제동 구간이 맞는지 확인** | `plot.accbrk()` | TIRE 모듈에서 실행 |
| **타이어별 상대 점수(Index) 산출** | `plot.compare_index_braking()` | PROJECT 모듈에서 실행 |
| **제동 시 휠 잠김 및 슬립 안정성 비교** | `plot.compare_slip_pdf()` | Ridgeline Plot 활용 |
| **노면이 변할 때 누가 덜 밀리나 확인** | `plot.compare_mudrop_dist()` | Mu-Drop Loss 분석 |

---

## 💻 실무 밀착형 종합 예제 코드

```python
# [변수 네이밍 규칙: 변수타입_목적(이름)]

# 1. 단일 타이어 분석 및 개별 검증
obj_tire_t1 = VT_ACCBRK_TIRE(df_raw, req="26RE_01", set="T1")
(
    obj_tire_t1.detect_test_segments(target=[100, 1], ws=15, filter=True)
)
obj_tire_t1.plot.accbrk(show=True, save="./verify", html=True)  # 개별 검증용 저장

# 2. 통합 프로젝트 구축 (과거 데이터 조합)
prj_braking = VT_ACCBRK_PROJECT(name="2026_Winter_Comp")
prj_braking.add_tire(obj_tire_t1)
prj_braking.add_tire_file("./last_year_CTR.tir")  # 과거 CTR 데이터 로드

# 3. 보정 연산 및 비교 리포트 생성
# ref_kwd='c' 로 설정된 콘트롤 타이어를 기준으로 환경 보정 수행
prj_braking.cal_corrected(ref_kwd='c', inverse=True, col_seq='Datetime')
prj_braking.plot.compare_braking(save="./report", html=True)  # 비교표 저장
prj_braking.plot.compare_slip_pdf(xlim=(0, 20), h=-0.6, save="./report", cmap='tab20')  # 슬립 비교

# 4. 분석 결과 통파일 저장 (Gzip 레벨 9 압축)
prj_braking.save_pjt("./final_result.pjt")
```

**Documented by your Coding Partner & Technical Writer, uno.**