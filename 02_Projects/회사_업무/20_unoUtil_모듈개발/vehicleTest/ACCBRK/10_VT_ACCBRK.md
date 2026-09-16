---
id: "work_20260910_VT_ACCBRK_manual"
title: "10_VT_ACCBRK 최상위 통합 자동화 파이프라인 매뉴얼"
type: resource
category_main: 회사_업무
category_sub: unoUtil
date: 2026-09-10
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - 매뉴얼
  - VT_ACCBRK
project_link: "[[unoUtil]]"
aliases:
  - "VT_ACCBRK"
  - "10_VT_ACCBRK"
---

> [!NOTE] 🧭 Obsidian 네비게이션 & 시스템 계층
> - **상위 허브**: [[unoUtil]] (사내 자동화 도구 통합 허브)
> - **하위 핵심 모듈**:
>   - [[12_VT_ACCBRK_PROJECT]]: 프로젝트 단위 다중 타이어 취합, 선형 보간 성능 보정(Control Tire), 비교 시각화 엔진
>   - [[11_VT_ACCBRK_TIRE]]: 단일 타이어 동역학 분석, Wavelet 노이즈 제거, 6대 전문 서브 분석 모듈
>   - [[21_CORRECT]]: 콘트롤 타이어 및 환경 인자 기반 보정 알고리즘
>   - [[31_PLOTTER_PROJECT]] / [[30_PLOTTER_TIRE]]: 전용 시각화 대시보드 플로터

# 🏛️ 차량 제동/가속(ACCBRK) 자동화 분석 시스템 마스터 기술 백서 (Confidential)

본 문서는 고주파 시계열 계측 데이터의 전처리 및 신호 복원부터 시작하여 각 단계별 클래스의 속성, 메서드 스펙, 작동 원리 및 개별 활용법을 포괄적으로 수록한 **사내 엔지니어링 표준 기술 매뉴얼**입니다.

---

## 📂 목차
1. [시스템 다차원 설계 및 데이터 흐름](#1-시스템-다차원-설계-및-데이터-흐름)
2. [단일 타이어 분석 엔진: `VT_ACCBRK_TIRE` & 서브 분석 모듈](#2-단일-타이어-분석-엔진-vt_accbrk_tire--서브-분석-모듈)
3. [단일 타이어 시각화 엔진: `PLOTTER_TIRE` 상세 스펙](#3-단일-타이어-시각화-엔진-plotter_tire-상세-스펙)
4. [통합 프로젝트 보정 엔진: `VT_ACCBRK_PROJECT` & 보정 알고리즘](#4-통합-프로젝트-보정-엔진-vt_accbrk_project--보정-알고리즘)
5. [통합 프로젝트 비교 시각화 엔진: `PLOTTER_PROJECT` 비교 가이드](#5-통합-프로젝트-비교-시각화-엔진-plotter_project-비교-가이드)
6. [통합 자동화 최상위 인터페이스: `VT_ACCBRK` & YAML 연동](#6-통합-자동화-최상위-인터페이스-vt_accbrk--yaml-연동)
7. [실무 문제 해결 및 아키텍처 제약 규칙 (Troubleshooting)](#7-실무-문제-해결-및-아키텍처-제약-규칙-troubleshooting)

---

## 1. 시스템 다차원 설계 및 데이터 흐름

본 패키지는 차량 평가 데이터의 노면 변이 및 기상 편차를 수학적으로 제거하고 타이어 고유의 물리 거동 성능을 정량 대조하기 위해 설계된 **객체 지향(OOP) 성능 평가 분석 프레임워크**입니다.

### 📐 데이터 상속 체계 메커니즘
```text
[LAYER 1: 전역 전용 설정 (Global Only)]
  └── info (차량 모델명, 중량 데이터, 센서 기상 정보 등 전역 메타데이터 스키마)
  └── excel (통합 보고서 엑셀 저장 경로 및 그래프 인쇄 레이아웃 제어)
         │
         ▼ [make_path_dict]를 통한 1차 하향식 경로 확장 (1:N 브로드캐스팅)
[LAYER 2: 프로젝트/노면별 (Project/Surface)]
  └── path에 등록된 노면 키(dry, wet 등)의 개수만큼 독립 딕셔너리로 세션 병렬 가동
  └── 노면별 평가 타겟 속도(test_vel) 개별 분기 제어
         │
         ▼ [get_tire_value]를 통한 2차 타이어별 매핑 (1:N 또는 N:N 덮어쓰기)
[LAYER 3: 타이어 세트별 (Tire Set)]
  └── 계측 데이터 파일명 끝에서 세트 키(C1, T1 등) 자동 추출
  └── 특정 타이어 세트별 고유 스펙(spec), 마킹(marking) 오버라이드
  └── [2중 중첩 매트릭스] 설정 시, 노면과 타이어 조건이 엇갈리는 고난도 복합 평가 완벽 대응
```

### 🏃‍♂️ 데이터 처리 파이프라인 (System Workflow)
```text
[계측 로우 데이터 (.vbo, .d7d)]
       │
       ▼ [VT_ACCBRK_TIRE] 인스턴스화 (Wavelet 노이즈 제거, 미소거리 적산)
┌─────────────────────────────────────────────────────────────┐
│ 1단계: 단일 타이어 성능 분석 및 피팅 (Tire Layer)                │
│  - 런(Run) 탐색 및 정합성 검증                                 │
│  - 6대 전문 동역학 분석 서브 모듈 (AN_*) 개별 가동                │
└─────────────────────────────────────────────────────────────┘
       │
       ▼ [.tir] 압축 바이너리 직렬화 저장 및 [VT_ACCBRK_PROJECT] 수집
┌─────────────────────────────────────────────────────────────┐
│ 2단계: 프로젝트 세션 통합 및 시계열 보정 (Project Layer)          │
│  - 콘트롤 타이어 시계열 기준선 선형 보간 (Linear Interpolation)   │
│  - 정지수/역지수 기반 외기/온도 편차 상쇄 지수 산출                 │
└─────────────────────────────────────────────────────────────┘
       │
       ▼ [.pjt] 파일 백업 및 시각화 출력 가동
┌─────────────────────────────────────────────────────────────┐
│ 3단계: 보고서 빌드 및 대조 분석 시각화 (Action Layer)             │
│  - PLOTTER_TIRE / PLOTTER_PROJECT 대시보드 플로팅              │
│  - 엑셀 인쇄 영역 좌표 적산 자동 리포팅                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 단일 타이어 분석 엔진: `VT_ACCBRK_TIRE` & 서브 분석 모듈

`VT_ACCBRK_TIRE` 클래스는 단일 시계열 데이터프레임(예: 단일 `.vbo` 파일)을 전처리하고, 유효 제동/가속 런(Run) 구간을 선별하여 물리 특성 공간을 매핑하는 단일 객체 분석 코어 엔진입니다.

### ① 클래스 주요 멤버 변수 (Attributes)

| 변수명 | 타입 | 설명 |
|:---|:---|:---|
| `self.df` | `pd.DataFrame` | 가속도 필터링(Wavelet), 미소 거리 적산 및 단위 변환이 완료된 전처리 시계열 데이터프레임 |
| `self.information` | `TEST_INFORMATION` | 의뢰번호(`req`), 타이어세트(`set`), 사양(`spec`), 마킹(`marking`), 노면(`surface`), 샘플레이트(`sr`) 등 전역 변수가 저장된 정보 구조체 |
| `self.result` | `TEST_RESULT` | 분석이 완료된 시계열 데이터(`self.result.df`)와 단일 행으로 축약된 동역학 물리 요약 레코드(`self.result.summary`)의 저장소 |
| `self.plot` | `PLOTTER_TIRE` | 이 타이어 인스턴스를 주체로 삼아 6종의 개별 전문 플롯을 렌더링하는 전용 시각화 플로터 |
| `self.mode` | `str` | 가동 모드 지정 변수 (`'brk'`: 제동 평가, `'acc'`: 가속 평가) |
| `self.test_vel` | `list[int]` | 분석 범위로 설정된 타겟 [시작 속도, 종료 속도] 리스트 |
| `self.valid_count` | `int` | 요약 통계를 산출할 때 가공 대상이 되는 최소 유효 데이터 수 |
| `self.acceleration` | `AN_ACCELERATION` | 속도 구간별 가속도(g) 분석 서브 인스턴스 |
| `self.split_speed` | `AN_SPLIT_SPEED` | 임계 속도 기준 고속/저속 제동력 분할 분석 서브 인스턴스 |
| `self.slip_pdf` | `AN_SLIP_PDF` | 가우시안 커널 밀도 추정 기반 슬립율 분포 분석 서브 인스턴스 |
| `self.mu_drop` | `AN_MU_DROP` | 기계학습 기반 수막현상(Mu-Drop) 손실 거리 분석 서브 인스턴스 |
| `self.slip_mode` | `AN_SLIP_MODE_SKEWNESS` | 2D 밀도 지형도 기반 제어 변위 분석 서브 인스턴스 |
| `self.sys_response` | `AN_RESPONSE` | 초기 제동 빌드업 및 시스템 지연 시간 분석 서브 인스턴스 |
| `self.local_pos` | `Optional[Union[str, dict]]` | 로컬 직교 좌표계(`PosX`, `PosY`) 변환 기준 위치 및 회전각 ('technoring', 'technotrack' 또는 커스텀 dict) |

---

### ② 핵심 멤버 함수 (Methods)

#### 1. `__init__(df_raw, **kwargs)` : 객체 생성 및 물리 신호 복원
*   **기능**: 입력받은 원시 계측 데이터를 복제하고, 가속도 신호 유실 또는 노이즈 관찰 시 **Wavelet Denoising(VisuShrink Soft, db4, Level 4)** 필터링을 수행하여 가공용 데이터셋을 구축합니다.
*   **매개변수**:
    *   `df_raw` (`pd.DataFrame`): 계측기로부터 출력된 원시 시계열 데이터프레임.
    *   `kwargs`: 샘플레이트(`sr`), 속도 컬럼(`col_vel`), 가속도 컬럼(`col_ax`), 기상 데이터(`weather`) 등.

#### 2. `analysis(test_vel, valid_count, outlier, sel_mode)` : 기본 성능 지표 계산
*   **기능**: 차속과 감속 G의 변화량을 실시간 감지하여 가속/제동 행위 구간(`TestNum`)을 검출하고, 이상치(`outlier`)를 제거한 후 가장 일관성 있는 상위 N개의 유효 런(`EffNum`)을 선별하여 요약 성능지표를 도출합니다.
*   **매개변수**:
    *   `test_vel` (`list[int]`): 분석 대상 시작/종료 속도 대역.
    *   `valid_count` (`int`): 최종 통계 요약에 포함할 세션 수.
    *   `outlier` (`list[int]`): 분석에서 제외할 불량 세션 번호 리스트.
    *   `sel_mode` (`str` / `list[int]`): 수동 인덱스 리스트 지정 또는 `'max_min'` / `'minimum_std'` 선택 알고리즘 모드 지정.
    *   `local_pos` (`str` / `dict`, optional): 로컬 직교 좌표계(`PosX`, `PosY`) 변환 기준 위치 및 각도 ('technoring', 'technotrack' 또는 커스텀 dict).

#### 3. `save(path, print=True)` : 바이너리 직렬화 파일 압축 저장
*   **기능**: 분석 연산이 완료된 타이어 인스턴스 전체 상태를 `.tir` 확장자를 가진 이진 파일로 최고 압축률 9단계(`gzip`)로 직렬화하여 기록합니다.
*   **매개변수**:
    *   `path` (`str`): 저장할 폴더 경로 또는 특정 파일 경로.

#### 4. `load(file, inform, print=True)` [Class Method] : 타이어 파일 복원
*   **기능**: 디스크에 저장된 `.tir` 바이너리 파일을 역직렬화하여 메모리 상에 완전한 파이썬 객체로 재생성하고, 필요한 경우 전역 메타데이터를 즉시 갱신합니다.
*   **매개변수**:
    *   `file` (`str`): 불러올 `.tir` 파일의 경로.

#### 5. `plt(save, excel, html, close)` : 전체 물리 특성 그래프 일괄 출력
*   **기능**: 6대 동역학 해석 플롯(Sequence, G-force, Speed, Slip PDF, Mu-drop, Skewness, Response)을 순차적으로 렌더링하고 이미지로 저장하거나 지정된 엑셀 시트에 자동 기록합니다.

---

### ③ 6대 동역학 서브 분석 모듈 상세 기능

| 분석 모듈 클래스 | 주요 입력 인자 (Arguments) | 연산 및 수학적 알고리즘 | 최종 산출 물리 성능 지표 |
|:---|:---|:---|:---|
| **`AN_SLIP_PDF`** | `col_slip_pdf_wheelslip` (휠 위치),<br>`slip_range` (타겟 구간),<br>`bw` (대역폭) | - 휠 센서 신호 보정 지수(`gain`) 자동 계산<br>- 가우시안 커널 밀도 추정(KDE) 및 수치적분(trapz) 적용 | • `pdf_mode`: 최빈 슬립율 (%)<br>• `pdf_eff_score`: 타겟 접지 슬립 영역 점유비율 |
| **`AN_MU_DROP`** | `col_mudrop_wheelacc` (휠 가속도 채널),<br>`int_ncl` (클러스터 수),<br>`leaf_rate` (DT 분기 노드비) | - [차속, 차가속, 휠가속] 데이터의 K-Means 클러스터링<br>- Decision Tree를 통한 수막현상 천이 임계 차속 및 제동거리 손실 계산 | • `mudrop_dist`: 수막현상에 의한 제동 거리 손실 ($m$)<br>• `mudrop_vel`: 마찰 한계 임계 차속 ($km/h$) |
| **`AN_SLIP_MODE_SKEWNESS`** | `slip_mode_vel_range` (차속 범위),<br>`limit_out` (노이즈 컷오프) | - 가우시안 평활 필터링 기반 2D 고해상도 밀도 지형도 빌드<br>- 최빈 제어점(Mode)과 실제 주행 제어 중심점(Mean) 간 편차 추적 | • `skewness_shortest_dist`: 제어 변위 최단거리<br>• `skewness_delta_slip`: 최적점 대비 슬립 오차 |
| **`AN_RESPONSE`** | `pre_sec` (선행 관찰 시간),<br>`response_target` (감속 개시 임계),<br>`rising_target` (초기 상승 구간) | - 유압 형성 시점(휠 가속도 낙하)부터 차체 감속 응답 개시 시점까지의 타임랙 추적<br>- 초기 빌드업 감속 구간 최소자승법(OLS) 선형 회귀 | • `sys_response_time`: 시스템 응답 지연 타임 (초)<br>• `sys_response_dist`: 지연 제동 거리 ($m$)<br>• `sys_rising_slope`: 제동 가속도 초기 상승 기울기 ($g/s$) |
| **`AN_ACCELERATION`** | `interval` (속도 구간 단위) | - 속도 구간 단위 대역별로 데이터를 슬라이싱하여 밴드 패스 평균 가속도 계산 | • `vel_{min}_{max}_acc`: 속도 대역별 가속 성능 지표 ($g$) |
| **`AN_SPLIT_SPEED`** | `vel_split` (분할 임계 속도) | - 고속 및 저속 영역으로 데이터셋을 이분할하여 개별 적산 | • `split_dist_high/low`: 영역별 순수 제동 거리 ($m$)<br>• `split_acc_high/low`: 영역별 평균 제동 감속도 ($g$) |

---

## 3. 단일 타이어 시각화 엔진: `PLOTTER_TIRE` 상세 스펙

`PLOTTER_TIRE` 클래스는 `self.outer`로 정의된 상위 타이어 분석기 객체와 연결되며, 분석 완료된 동역학 물리 데이터를 고해상도 차트 레이아웃으로 플로팅합니다.

### ① 주요 시각화 메서드 및 기능

*   **`accbrk(ax, show, x_off)`**: 속도 및 가속도 시계열 원시 데이터 위에 탐색된 시험 구간과 선별된 유효 구간을 대조 드로잉하고, 각 런별 제동 거리 수치를 텍스트 노출합니다.
*   **`acceleration(ax)`**: 속도 대역별 가속도의 통계적 분산(Box Plot) 및 밀도(Swarm Plot)를 중첩 표시하고, 구간별 평균 가속도 지표의 중심값들을 붉은색 점선(`Mean Trend`)으로 자동 연결하여 가속 성능 감쇠 트렌드를 보여줍니다.
*   **`split_speed(ax)`**: 임계 분기 차속을 기준으로 고속 영역(High Region)과 저속 영역(Low Region)을 Red/Blue 색상으로 명확히 구분하여 차속-시간 추이 및 차속-가속도 산점도를 2단 분할 플로팅합니다.
*   **`slip_check(ax)`**: 실차 수평 기준 속도 프로파일 위에 4륜 개별 바퀴 속도의 시계열 미세 슬립 편차를 대조 플로팅하고, 하단에 휠 가속도 물리 거동을 함께 표현하여 휠 잠김(Lock) 유발 시점을 추적합니다.
*   **`slip_pdf(ax, xlim)`**: 슬립율 확률 밀도 곡선(KDE) 위에 최빈 그립 점(Mode), 평균 제어점(Mean), 표준편차 영역(1-Sigma)을 정밀 계산하여 면적으로 표시하며, 우측 상단에 왜도(Skewness), 첨도(Kurtosis) 등을 요약한 텍스트 박스를 자동 배치합니다.
*   **`mu_drop(ax, cmap, show)`**: 노면 상태가 급격히 바뀌는 슬라이딩 마찰 한계 지점을 추적하여, 수막현상으로 인해 늘어난 실제 거리와 가상의 물리적 한계 거리 사이의 편차를 **제동 거리 손실분(Dist. Loss)** 면적 음영 그래프로 도식화합니다. 3D 공간 산점도 플롯도 동시 제공합니다.
*   **`slip_mode_skewness(suptitle, xlim, ylim)`**: 종가속도와 슬립율의 관계를 2D 고해상도 등고 지형도(`imshow` bilinear 방식)로 구현하고, 최적 그립 타겟점(Mode)과 실제 주행 제어점(Mean) 간의 편차 추적 벡터 화살표를 드로잉합니다.
*   **`sys_response(suptitle)`**: 제동 유압 빌드업 시점의 휠 가속도 반응 시점부터 실제 종G가 형성되는 과도 응답 지연 구간을 포커싱하고, 라이징 슬로프 곡선을 최소자승법(OLS) 선형 접선으로 피팅하여 표시합니다.

---

## 4. 통합 프로젝트 보정 엔진: `VT_ACCBRK_PROJECT` & 보정 알고리즘

`VT_ACCBRK_PROJECT` 클래스는 여러 타이어 인스턴스를 프로젝트 저장소에 바인딩하고, 시험 중 발생하는 기온 및 노면 변화 변이를 콘트롤 타이어 기반의 선형 보간을 통해 상쇄하는 고품격 보정 모듈입니다.

### ① 클래스 주요 멤버 변수 (Attributes)

|:---|:---|:---|
| `self.prj_name` | `str` | 프로젝트의 고유 식별 명칭 (결과 파일 및 리포트 그래프의 Prefix로 작동) |
| `self.tire_analyzers` | `dict[str, VT_ACCBRK_TIRE]` | 타이어 세트명(Key)과 `deepcopy` 처리된 안전한 개별 분석 객체 사본(Value)의 컨테이너 |
| `self.result.summary_all` | `pd.DataFrame` | 모든 콘트롤 타이어(C1, C2...)를 포함하여 보정 연산이 최종 완료된 전체 결과 데이터프레임 |
| `self.result.summary` | `pd.DataFrame` | 보고서 작성용으로 첫 번째 콘트롤과 대조 타이어만 선별한 콤팩트 결과 데이터프레임 |
| `self.plot` | `PLOTTER_PROJECT` | 프로젝트에 속한 타이어 세트들의 성능 차이를 오버레이 방식으로 일괄 비교 시각화하는 다차원 플로터 |
| `self.ref_kwd` | `str` | 보정 연산 시 기준 타이어로 자동 필터링할 문자열 접두어 규칙 (기본값: `'c'`) |
| `self.mask_ref_tire` | `pd.Series (bool)` | 전체 데이터 중 콘트롤 타이어에 해당하는 지점을 지목하는 논리 불리언 마스크 |
| `self.mask_summary` | `pd.Series (bool)` | 요약 리포트용 첫 번째 콘트롤 및 테스트 타이어 세션을 지목하는 마스크 |

---

### ② 핵심 멤버 함수 (Methods)

#### 1. `add_tire(obj, tire=None)` : 개별 분석기 복사 및 등록
*   **기능**: 단일 타이어 객체를 복제하여 관리 목록에 안전하게 추가하고 메타데이터 동기화를 거쳐 프로젝트 하위 노드로 종속시킵니다.
*   **설명**: 사본 추가 방식을 사용하여 외부 원본 객체 데이터를 임의로 수정하더라도 프로젝트에 누적된 데이터셋의 신뢰성이 보존됩니다.

#### 2. `add_tire_file(file, tire=None)` : 물리 저장 파일로부터 가동
*   **기능**: 외기 디스크에 이미 기록되어 있는 `.tir` 파일을 언피클링(Unpickle)하여 프로젝트 딕셔너리로 다이렉트 로드합니다.

#### 3. `cal_corrected(inverse=False)` : 콘트롤 기반 선형 보간 보정 연산 (핵심 🧠)
*   **기능**: 시험 시퀀스(`Datetime`)에 배치된 콘트롤 타이어 성능들의 연속적 추이를 선형 보간하여 동적 보정 기준선을 구성하고, 각 테스트 타이어의 순수 성능 변화량 지수 및 보정 거리(m), 가속도(g)를 자동 계산합니다.

#### 4. `update_summary()` : 실시간 요약 데이터 최신 동기화
*   **기능**: 프로젝트 내 특정 타이어 인스턴스의 정보나 세부 수치를 외부에서 수정한 후, 전체 프로젝트 보정 테이블에 최신 상태를 강제 동기화 갱신합니다.

#### 5. `makefile_summary()`, `makefile_summary_all()`, `makefile_summary_index()` : 정제 테이블 출력
*   **기능**: 엑셀 시트나 실무 검증용 보고서에 바로 바인딩할 수 있도록, 지수와 결과값만 깔끔하게 정렬된 형태로 전치(Transpose)된 데이터프레임을 생성해 줍니다.

#### 6. `save_pjt(path)` : 프로젝트 전체 상태 영구 직렬화 백업
*   **기능**: 수집된 타이어 사본들과 프로젝트 보정 데이터 전체를 압축률 최고 단계(`Gzip Level 9`)로 패키징하여 `.pjt` 단일 파일로 기록 보관합니다.

---

### ③ 선형 보간 성능 보정 수식 (Correction Engine Formulas)

#### 1) 보정 기준선 (`adj_refer`) 생성
시험 시퀀스(`col_seq`) 상의 콘트롤 타이어 성능 변화를 시간순으로 연결하여 보정 기준선(`adj_refer`)을 동적으로 구성합니다.
$$\text{adj\_refer}_{t} = \text{Interpolate}(\text{Control}_{\text{prev}}, \text{Control}_{\text{next}})$$
*(Note: 콘트롤 타이어 이전 구간 및 이후 구간은 가장 가까운 콘트롤 값으로 각각 `ffill()` 및 `bfill()` 처리하여 빈틈없는 기준선을 형성합니다.)*

#### 2) 성능 지수 (`Index`) 산출
*   **Positive 지표 (가속도 등 - 클수록 우수)**:
    $$\text{Index} = \frac{\text{Target}}{\text{adj\_refer}} \times 100$$
*   **Negative 지표 (제동거리 등 - 작을수록 우수, 정지수 방식)**:
    $$\text{Index} = \frac{2 \times \text{adj\_refer} - \text{Target}}{\text{adj\_refer}} \times 100$$
*   **Negative 지표 (역지수 방식 - 기존 성적서 양식 통일용)**:
    $$\text{Index} = \frac{\text{adj\_refer}}{\text{Target}} \times 100$$

#### 3) 최종 보정 성능값 (`Corrected`) 도출
일반 테스트 타이어가 외기 편차가 없는 고정된 평균 노면 상태에서 주행했을 때 얻을 수 있는 가상 성능값입니다.
$$\text{Corrected} = \text{Mean}(\text{Baseline}_{\text{Control}}) \times \left(1 + \left(1 - \frac{\text{Index}}{100}\right)\right)$$
*(Note: 콘트롤 타이어가 2개 미만일 경우 단일 콘트롤 값의 평균을 사용하며, 2개 이상일 경우 전체 선형보간 기준선 평균을 적용합니다.)*

---

## 5. 프로젝트 비교 시각화 엔진: `PLOTTER_PROJECT` 비교 가이드

`PLOTTER_PROJECT` 클래스는 동일 시험 노면 조건에서 여러 타이어의 성능 편차와 물리 변위를 비교하기 위해, 다중 레이어 오버레이 방식으로 그래프를 렌더링합니다.

### ① 주요 비교 시각화 메서드 및 기능

*   **`compare_braking(col_dist, save)`**: 기준 타이어와 대조 타이어의 실측 거리 대비 최종 보정 제동거리를 나란히 표시하고, 우측 차트에 100% 한계 기준선(Red Line)을 활용해 상대 성능 지수(%)를 정량 대조합니다.
*   **`compare_index_braking(col_tire, col_dist, ax)`**: 보정 제동 지수 바 차트를 구성하고, 각 바 끝에 실제 제동 거리(m) 수치를 문자열로 오버레이 출력합니다.
*   **`compare_acceleration(colors, save)`**: 속도 구간별 평균 가속도 변화를 오버레이 선 차트로 도식화하며, **`Rectangle Bar`** 패치 기법을 결합하여 특정 구간의 접지 거동 성능을 직관적인 영역으로 표현합니다.
*   **`compare_split_distance(width, save)`**: 전체 제동 거리를 고속 영역과 저속 영역의 물리적 거리(m)로 분할하여 단일 누적 바 차트(Stacked Bar) 형태로 도식화해 줍니다.
*   **`compare_index_split_distance(width, save)`**: 고속 및 저속 영역의 제동 성능 지수(Index %)를 스택형 누적 비율로 대조 출력합니다.
*   **`compare_split_acceleration(width, colors, ax)`**: 고속 구간과 저속 구간의 가속도를 좌우 병렬 바 플롯으로 분할 시각화하여 영역별 가속 응답을 분석합니다.
*   **`compare_index_split_acceleration(width, colors, ax)`**: 고속 및 저속 분할 구간 가속도에 대해 각각의 가속 성능 지수(%) 바 차트를 병렬 드로잉합니다.
*   **`compare_slip_pdf(h, xlim, save)`**: 겹쳐 그리면 가독성이 무너지는 여러 타이어의 슬립율 밀도 분포(PDF)를 산맥 형태의 **`Ridgeline Plot`**으로 입체감 있게 적층하여 비교합니다.
*   **`compare_mudrop_dist(save)`**: 각 타이어 세트별 수막현상으로 유실된 손실 거리(m)와 타이어의 순수 제동 거리(m)를 직관적인 이분할 누적 차트로 표현하여 환경 강건성을 대조 평가합니다.
*   **`compare_slip_mode_skewness(save)`**: 각 타이어 세트별 최빈 제어 슬립점(Mode)과 실제 평균 제어점(Mean)의 거동 편차를 산점도로 뿌리고, 편차 크기를 벡터 라인으로 연결해 제어 강건성을 시각적 면적으로 비교합니다.
*   **`compare_response(save)`**: 제동 시스템 지연 개시 거리(m) 대비 감속 상승 속도($g/s$)의 성능 편차를 타이어 세트별 산점도와 범례로 표현합니다.

---

## 6. 통합 자동화 최상위 인터페이스: `VT_ACCBRK` & YAML 연동

최상위 래퍼 함수인 `VT_ACCBRK`는 복잡한 하위 개별 가동 과정을 파이프라인으로 연결하여, 단 한 번의 호출로 원클릭 분석 및 엑셀 보고서 인쇄까지 자동으로 수행합니다.

### ① 파이프라인 라이프사이클 및 데이터 흐름

```mermaid
graph TD
    A[입력 경로 / YAML 설정] --> B[1. 디렉토리 검증 및 캐시 경로 설정]
    B --> C{load_file 캐시 존재?}
    C -- No --> D1[FileDataReader: 원천 VBO/VBB 파일 일괄 로드]
    D1 --> D2[0. db 디렉토리에 .gz 압축 캐시 저장]
    C -- Yes --> D3[0. db/*.gz 캐시에서 초고속 로드]
    
    D2 --> E[2. 타이어 단위 분석 루프]
    D3 --> E
    
    E --> F{load_tire 캐시 존재?}
    F -- No --> G1[VT_ACCBRK_TIRE.run 실행]
    G1 --> G2[0. db/*.tir 경량 캐시 저장]
    F -- Yes --> G3[0. db/*.tir 캐시 로드]
    
    G2 --> H[3. 노면별 프로젝트 통합]
    G3 --> H
    
    H --> I[VT_ACCBRK_PROJECT 객체 생성]
    I --> J[CORRECT 보정 엔진 구동 (Control / Factor)]
    J --> K[0. db/*.pjt 프로젝트 파일 저장]
    
    K --> L[4. 종합 리포트 및 시각화]
    L --> M1[통합 엑셀 워크북 (.xlsx) 생성]
    L --> M2[비교 차트 (.png, .html) 2. fig에 저장]
```

---

### ② 표준 디렉토리 구조 및 캐싱 아키텍처

`VT_ACCBRK` 파이프라인은 반복 재연산 오버헤드를 극소화하기 위해 표준화된 3단계 폴더 규격을 사용합니다:

```text
[평가 프로젝트 루트 폴더]/
│
├── 0. db/                   <-- 초경량 중간 연산 캐시 파일 저장소
│   ├── rawdata_cache.gz     <-- 로우 계측 데이터 압축 캐시
│   ├── C1.tir, T1.tir ...   <-- 개별 타이어 분석 객체 (.tir)
│   └── project_dry.pjt      <-- 프로젝트 보정 완료 인스턴스 (.pjt)
│
├── 1. rawdata/              <-- 현장에서 취득된 원천 계측 파일 (VBO, VBB, D7D 등)
│   ├── C1_run01.vbo
│   └── T1_run01.vbo
│
└── 2. fig/                  <-- 결과 차트 이미지 및 대시보드 출력소
    ├── 0. Braking Test Result.png
    └── 1. Acceleration Distribution.png
```

---

### ③ 마스터 YAML 설정 파일 템플릿 (`master_config.yaml`)

윈도우 파일 경로를 복사하여 그대로 감싸 붙여넣을 수 있도록 최적화된 마스터 YAML 템플릿입니다.

```yaml
# =============================================================================
# ACCBRK 차량 평가 데이터 분석 마스터 설정 파일 (3단계 상속 구조 완벽 지원)
# =============================================================================

# =============================================================================
# [LAYER 1] 전역 및 필수 설정 (Global & Essential - 단 1번만 정의하는 영역)
# =============================================================================

# 1-1. [최우선 필수] 세션 노면 경로 지정
# 윈도우 탐색기에서 복사한 경로를 그대로 붙여넣고 양 끝에 작은따옴표(' ')만 감싸주세요.
path:
  dry: 'D:\uno\Python\Projects\unoUtil\unoUtil\vehicleTest\ACCBRK\example\26RE020041KF_BMW320_Dry,Wet,Con_ADAC,Winter_Sibana\260311_BMW320d_ADAC_Dry'
  wet: 'D:\uno\Python\Projects\unoUtil\unoUtil\vehicleTest\ACCBRK\example\26RE020041KF_BMW320_Dry,Wet,Con_ADAC,Winter_Sibana\260310_BMW320d_ADAC_Wet'

# 1-2. 전역 공통 시험 정보 (info)
# 분석 전역에 공유될 차량 기본 정보입니다. (자동 추출되는 set, cond는 깔끔하게 제외)
info:
  TestVehicle: "BMW 320d"
  TestVehicleType: "ICV"
  TestVehicleLayout: "RWD"
  TestLocation: "TR"

  # [신규 추가 시험 메타데이터 스키마 영역] (기본값 null)
  vehicle_model: null
  vehicle_year: null
  vehicle_type: null
  vehicle_layout: null
  location: null
  surface: null
  surface_number: null
  surface_position: null
  air: null
  water: null
  test_cond1: null
  test_cond2: null
  test_cond3: null
  weight: null
  weight_fl: null
  weight_rl: null
  weight_fr: null
  weight_rr: null
  temp_air: null
  temp_surface: null
  temp_tire: null
  weather_cond1: null
  weather_cond2: null
  weather_cond3: null
  etc1: null
  etc2: null
  etc3: null

# 1-3. 엑셀 출력 및 보고서 서식 설정 (excel)
excel:
  excel_path: 'D:\uno\Python\Projects\unoUtil\unoUtil\vehicleTest\ACCBRK\example\26RE020041KF_BMW320_Dry,Wet,Con_ADAC,Winter_Sibana\graph.xlsx'
  sheet_name: "Graph"
  fig_object: null
  start_cell: "B2"
  width: 150
  height: null
  # [요약 그래프 단일 시트 프로젝트별 열(Column) 배치 제어 옵션]
  sheet_summary: "Graph_Summary"     # 종합 요약 비교 그래프가 취합될 단일 워크시트명 (기본값: Graph_Summary)
  excel_opt: "down"                  # 동일 프로젝트 내 요약 차트 배치 방향 (기본값: 'down', 8개 비교 그래프가 세로로 배치)
  split_summary_sheets: false        # false: 단일 시트 내 프로젝트별 열(세로 스택) 우측 확장 배치(기본값), true: 노면별 개별 시트 분리


# =============================================================================
# [LAYER 2 & 3] 계층형 가변 설정 (Hierarchical Configs)
# 1중 구조(단일, 노면별, 타이어별)뿐만 아니라 복잡한 2중 중첩(노면 x 타이어) 매트릭스도 완벽히 지원합니다.
# 사용하고자 하는 방식의 주석(#)을 풀어서 자유롭게 정의하십시오.
# =============================================================================

# -----------------------------------------------------------------------------
# [A] 시험 정보 / 메타데이터 설정군
# -----------------------------------------------------------------------------

# 2-1. 의뢰 번호 (req)
# [Style A] 전역 일괄 단일값 적용
req: "26RE020041KF"

# 2-2. 시험 항목 (item)
item: "제동성능 평가"

# 2-3. 시험 방법 (method)
method: "ADAC Winter"

# 2-4. 시험 환경 조건 (cond)
cond: null

# 2-5. 시험 노면 명칭 (surface)
surface: "dry"

# 2-6. 타이어 세트명 지정 (set)
set: null

# 2-7. 타이어 세트별 상세 사양 코드 (spec)
spec:
  C1: "EXT-2022-00621"
  T1: "KPKT1037718X00012"
  T2: "KPKT1037718X00013"
  T3: "KPKT1037718X00014"
  C2: "EXT-2022-00621"

# 2-8. 상세 마킹 정보 설정 (marking)
marking:
  C1: "MARKING-C1"
  T1: "MARKING-T1"
  T2: "MARKING-T2"
  T3: "MARKING-T3"
  C2: "MARKING-C2"


# -----------------------------------------------------------------------------
# [B] 데이터 필터 및 분석 제어 파라미터군
# -----------------------------------------------------------------------------

# 2-9. 평가 목표 속도 조건 [목표속도, 분석시작속도차이] (test_vel)
test_vel:
  dry: [100, 1]
  wet: [80, 1]

# 2-10. 아웃라이어 데이터 인덱스 제거 설정 (outlier)
outlier:
  C1: [1]
  T1: null
  T2: null
  T3: null
  T4: null
  C2: [0]

# 2-11. 유효 데이터 분석 대상 인덱스 선택 설정 (sel_mode)
sel_mode:
  C1: [0, 2, 3]
  T1: [0, 1, 2, 3]
  T2: [0, 1, 3, 4]
  T3: [0, 1, 2, 4]
  T4: [0, 1, 2, 5]
  C2: [1, 3]

# 2-12. 세션당 최소 유효 데이터 수 (valid_count)
valid_count: 3

# 2-13. 가속 구간 속도 세분화 분석 시간 단위 인터벌 (interval)
interval: 0.5

# 2-14. 하이/로우 분석용 분할 기준 속도값 (vel_split)
vel_split: 50.0

# 2-15. 로컬 직교 좌표계 변환 설정 (local_pos) - 단일값 또는 노면/타이어별 dict
local_pos: 'technoring'
```

---

### ④ 실무 핵심 활용 시나리오 및 예제 레시피 (Case-by-Case Recipes)

최상위 래퍼 함수인 `VT_ACCBRK`는 설계 초기부터 단일 시험의 초간단 자동화부터 다중 프로젝트 배치, YAML 기반 마스터 자동화, 그리고 후처리 데이터 통합까지 현업의 모든 케이스를 커버할 수 있도록 파라미터가 유연하게 구조화되어 있습니다. 아래의 5가지 실제 실무 케이스 예제를 참조하여 자동화 파이프라인을 구축하십시오.

---

#### 💡 Case A: 단일 프로젝트 & 단일 노면 정밀 분석 (Single Surface Runner)
- **대상 시나리오**: `EV3_IW01_make_result.py`와 같이 특정 차량(예: EV3)의 단일 노면 조건(예: Dry 제동만 또는 Wet 제동만)을 대상으로, 구체적인 시험 속도 구간 및 아웃라이어 인덱스, 타이어 사양 정보를 코드 레벨에서 직접 튜닝하여 고속으로 결과를 추출하고 싶을 때 사용합니다.
- **주요 파라미터 셋**:
  - `path`에 단일 문자열 경로 전달.
  - `test_vel`에 특정 [시작속도, 종료속도] 단일 리스트 전달.
  - `outlier` 및 `sel_mode`를 이용해 특정 타이어의 불량 런 제외 및 유효 런 수동 지정.

```python
import pandas as pd
from unoUtil.vehicleTest.ACCBRK.VT_ACCBRK import VT_ACCBRK

if __name__ == "__main__":
    # 1. 단일 노면 원시 데이터 경로 지정 (Dry 노면 제동 데이터)
    raw_path = r"D:\Braking_AutoBuild\EV3_IW01\rawdata_dry"
    
    # 2. 시험 및 차량 기본 메타데이터 정보 설정
    test_infor = {
        'TestVehicle': "Kia EV3",
        'TestVehicleType': "EV",
        'TestVehicleLayout': "FWD",
        'TestLocation': "TR_Track"
    }
    
    # 3. 타이어 세트별 상세 사양코드 명시 (Control C1, Test T1/T2 등)
    tire_spec = {
        'C1': "SPEC-EV3-C1",
        'T1': "SPEC-EV3-T1",
        'T2': "SPEC-EV3-T2",
        'C2': "SPEC-EV3-C2"
    }
    
    # 4. 분석 세부 튜닝 및 아웃라이어 정밀 제거
    outlier_runs = {
        'C1': [1],     # C1 타이어의 1번째 런(Run)은 가감속 불안정으로 제외
        'T1': None,
        'T2': [0]      # T2 타이어의 0번째 런은 노이즈로 제외
    }
    
    # 5. 엑셀 리포트 자동 출력 레이아웃 정의
    excel_report = {
        'excel_path': r"D:\Braking_AutoBuild\EV3_IW01\EV3_IW01_Braking_Result.xlsx",
        'sheet_name': "Dry_Braking_Performance",
        'start_cell': "B2",
        'width': 150
    }
    
    # 6. VT_ACCBRK 래퍼 함수 원클릭 가동
    #  - test_vel=[100, 1]: 100km/h에서 1km/h까지의 제동거리를 적산 분석
    #  - load_file=True: 이미 캐싱된 .gz 파일이 존재할 경우 하드디스크 I/O 없이 0.1초 만에 실행
    dict_pjt = VT_ACCBRK(
        path=raw_path,
        test_vel=[100, 1],
        infor=test_infor,
        spec=tire_spec,
        outlier=outlier_runs,
        valid_count=3,           # 요약 계산 시 타이어당 최소 3개 이상의 유효 런 필요
        surface="dry",
        pjt_name="EV3_Dry_Project",
        close_tire=True,         # 개별 타이어 차트 메모리 해제
        close_pjt=False,         # 프로젝트 종합 비교 대시보드 출력 유지
        save_pjt=True,           # 0. db 폴더에 .pjt 압축 백업본 영구 저장
        excel=excel_report
    )
    
    print("🎉 EV3 Dry 단일 노면 평가 자동 분석 및 보고서 생성이 완료되었습니다!")
```

---

#### 💡 Case B: 다중 프로젝트 & 다중 노면 일괄 대량 자동화 (Multi-Surface Runner)
- **대상 시나리오**: Dry, Wet, Snow 등 여러 시험 환경 데이터를 순차적으로 한 번에 배치 가공하여, **단 하나의 통합 엑셀 파일 내의 개별 시트들**로 보고서를 통합하고 싶을 때 사용합니다. 각 노면별로 타겟 차속이나 보정(CORRECT) 팩터가 달라야 하는 실무 환경에 완벽 대응합니다.
- **주요 파라미터 셋**:
  - `path`에 딕셔너리(`{'dry': 경로, 'wet': 경로}`) 전달.
  - `test_vel`을 딕셔너리로 설정하여 노면별 분석 타겟 속도를 개별 분기 제어.
  - `correct_factor`에 `'dry'`, `'wet'` 등 노면별 외란 보정 물리 지형 프로파일 자동 매핑.

```python
import pandas as pd
from unoUtil.vehicleTest.ACCBRK.VT_ACCBRK import VT_ACCBRK
from unoUtil.convenienceFunction.MakeDFWeatherTring import load_master_database

if __name__ == "__main__":
    # 1. 기상 마스터 데이터베이스 로드 (외기온도 편차 보정용)
    df_weather = load_master_database().reset_index()

    # 2. 다중 노면 데이터 소스 폴더 일괄 바인딩
    multi_paths = {
        'dry': r"D:\Braking_AutoBuild\EV3_IW01\rawdata_dry",
        'wet': r"D:\Braking_AutoBuild\EV3_IW01\rawdata_wet"
    }
    
    # 3. 노면별 맞춤 차속 프로파일 분기 설정 (Dry 100km/h 대 Wet 80km/h)
    vel_config = {
        'dry': [100, 1],
        'wet': [80, 20]
    }
    
    # 4. 노면별 맞춤형 환경 요인 보정 프로파일 설정
    #  - dry: 외기온도 편차에 강인한 dry 보정 팩터 적용
    #  - wet: 수막 및 노면 변이에 특화된 wet 보정 팩터 적용
    correct_config = {
        'dry': 'dry',
        'wet': 'wet'
    }
    
    # 5. 하나의 엑셀 워크북에 노면별 개별 시트로 저장되도록 엑셀 세션 통합 설정
    excel_config = {
        'excel_path': r"D:\Braking_AutoBuild\EV3_IW01\EV3_IW01_Integrated_Result.xlsx",
        'sheet_name': "Dry_Result",         # 첫 번째 가동되는 노면의 시트명
        'split_summary_sheets': True        # 노면별로 서로 다른 개별 시트로 자동 분할 출력 활성화 🎯
    }
    
    # 6. 복합 파이프라인 가동
    dict_projects = VT_ACCBRK(
        path=multi_paths,
        test_vel=vel_config,
        correct_factor=correct_config,
        weather=df_weather,
        pjt_name={'dry': 'EV3_Dry_PJT', 'wet': 'EV3_Wet_PJT'},
        excel=excel_config,
        load_file=True,
        save_tire=True,
        save_pjt=True,
        close_tire=True,
        close_pjt=True
    )
    
    print(f"🎉 일괄 처리 완료된 프로젝트 노면 목록: {list(dict_projects.keys())}")
```

---

#### 💡 Case C: YAML 설정을 이용한 노코드 제어 자동화 (Declarative Runner)
- **대상 시나리오**: 파이썬 코드를 전혀 수정하지 않고, 외부 `master_config.yaml` 파일만을 변경하여 프로그램 제어권을 완전히 동적으로 위임하고 싶을 때 사용합니다. 정형화된 성적서 발행이나 대량 생산 파이프라인 운영에 가장 적합한 실무 표준 구조입니다.
- **주요 파라미터 셋**:
  - `config_file` 인자에 YAML 파일 절대 경로만 전달. 나머지 파이썬 호출 매개변수는 무시되거나 YAML 파일 값에 상속/오버라이드됩니다.

```python
import warnings
from unoUtil.vehicleTest.ACCBRK.VT_ACCBRK import VT_ACCBRK

# 불필요한 라이브러리 경고창을 차단하여 터미널 가독성 확보
warnings.simplefilter(action='ignore', category=FutureWarning)

if __name__ == "__main__":
    # YAML 설정 파일의 마스터 경로 지정
    yaml_config = r"D:\Braking_AutoBuild\EV3_IW01\master_config.yaml"
    
    # YAML 내에 기재된 모든 아웃라이어, 속도, 경로, 시각화 스타일을 가져와 완전 자동 배치 처리
    dict_project = VT_ACCBRK(
        config_file=yaml_config,
        load_file=True,      # CSV 파싱 생략, 압축 바이너리 .gz 캐시로 초고속 처리
        save_tire=True,      # 연산 결과 .tir 캐시 업데이트
        save_pjt=True,       # 보정 완료된 최종 상태 .pjt로 저장
        close_tire=True,
        close_pjt=False
    )
    
    print("\n🎉 YAML 기반 대규모 일괄 평가 보고서 인쇄가 성황리에 완료되었습니다!")
```

---

#### 💡 Case D: 초고속 프로젝트 재로드 및 사후 수평 병합 (Lazy Load & Post-Merge)
- **대상 시나리오**: 이미 연산이 완료되어 로컬 `0. db` 폴더에 저장되어 있는 `.pjt` 압축 캐시 파일들을 불러와, **Dry와 Wet 노면의 성능 지표를 하나의 수평 비교 테이블 및 통합 Ridgeline 차트**로 결합하여 2차 대조 보고서를 즉석에서 생성하고 싶을 때 사용합니다. 원천 VBO/CSV 파일의 재파싱이나 물리 연산 과정이 없으므로 **단 0.5초 만에 완료**됩니다.
- **주요 API**:
  - `VT_ACCBRK_load`로 프로젝트 객체 로드 (`restore=False` 지연 로딩을 통한 메모리 절약)
  - `VT_ACCBRK_merge`로 두 프로젝트의 타이어 성능 데이터를 수평 결합 (접미사 자동 매핑)

```python
from unoUtil.vehicleTest.ACCBRK.VT_ACCBRK import VT_ACCBRK_load, VT_ACCBRK_merge

if __name__ == "__main__":
    # 1. 0.05초 만에 기존 Dry 및 Wet 프로젝트 캐시 파일(.pjt) 동시 로드 (restore=False)
    pjt_files = [
        r"D:\Braking_AutoBuild\EV3_IW01\rawdata_dry\0. db\EV3_Dry_PJT.pjt",
        r"D:\Braking_AutoBuild\EV3_IW01\rawdata_wet\0. db\EV3_Wet_PJT.pjt"
    ]
    
    dict_loaded = VT_ACCBRK_load(path=pjt_files, restore=False)
    
    # 2. 로드된 개 개별 프로젝트를 단일 '통합 비교 프로젝트'로 수평 병합 (Merge)
    #  - suffix=['Dry', 'Wet']: 타이어 세트명이 'Dry_C1', 'Wet_C1' 형태로 개편되어 범례 충돌 방지 🎯
    #  - order_col='TestTireSet': 병합 완료 후 타이어 이름을 기준으로 출력 테이블을 깔끔하게 재정렬
    tire_sequence = {'Dry_C1': 0, 'Dry_T1': 1, 'Dry_T2': 2, 'Dry_C2': 3,
                     'Wet_C1': 4, 'Wet_T1': 5, 'Wet_T2': 6, 'Wet_C2': 7}
    
    merged_project = VT_ACCBRK_merge(
        dict_pjt=dict_loaded,
        suffix=['Dry', 'Wet'],
        sel_tire=['C1', 'T1', 'T2', 'C2'],
        order_col='TestTireSet',
        order=tire_sequence
    )
    
    # 3. 병합된 통합 프로젝트에서 종합 비교 엑셀 리포트 및 시각화 즉석 출력
    merged_excel = {
        'excel_path': r"D:\Braking_AutoBuild\EV3_IW01\EV3_IW01_Comparative_Analysis.xlsx",
        'sheet_name': "Dry_Wet_Comparison",
        'start_cell': "B2",
        'width': 150
    }
    
    merged_project.plt(
        save=True,          # 2. fig 폴더에 통합 8대 비교 차트 이미지 저장 (.png)
        excel=merged_excel, # 지정된 엑셀 시트에 통합 비교 결과 및 차트 이미지 배치
        close=False         # 결과 관찰을 위해 차트 출력 유지
    )
    
    print("\n🎉 로드 및 병합(Merge)을 활용한 2차 종합 비교 분석이 성공적으로 마무리되었습니다!")
```

---

#### 💡 Case E: 실무 대량 다중 의뢰서 일괄 루핑 및 수평 교차 성능 시각화 (EV3 실전 배치 가동 시나리오)
- **대상 시나리오**: `EV3_IW01_make_result.py`와 같이 대규모 프로젝트 내의 **여러 개별 의뢰서(26RE040025KF, 26RE060023KF 등)들을 일괄적으로 루핑 순회**하며, 각 의뢰서 하위 디렉토리를 동적으로 파싱(surface 및 lane 자동 추출)하여 `VT_ACCBRK` 분석을 차례대로 완수한 뒤, **1세대(1st Mold)와 2세대(2nd Mold) 타이어 간의 종방향 가속도 성능과 제동 분포 산점도를 커스텀 라인 및 마커로 수평 대조 플로팅**하는 가장 고도화된 실무 아키텍처입니다.
- **주요 기법**:
  - `Path.glob`과 폴더명 문자열 슬라이싱을 통해 `surface`와 `lane` 키를 런타임에 자동 추출하고 `dict_path`, `dict_testSpeed`, `dict_selmode` 등의 맵을 동적으로 동시 구축하여 래퍼 함수를 가동합니다.
  - 사후 비교 시 `VT_ACCBRK_load`로 여러 프로젝트의 캐시(.pjt)를 불러와 `VT_ACCBRK_merge`로 병합하되, `suffix`를 주어 각 타이어가 어떤 의뢰서 및 레인 소스 출신인지를 명확히 꼬리표화합니다.
  - 병합된 프로젝트의 시각화 플로터(`compare_acceleration`, `compare_scatter_detail`) 상에서 세대별 구분(예: 1세대 점선, 2세대 실선)을 위해 **커스텀 선 스타일(`linestyle`) 및 마커 딕셔너리(`marker`)를 직접 맵으로 엮어 주입**하여 시각적 변별력을 극대화합니다.

```python
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from unoUtil.graphicTools._Plotter_ import gen_list_colors
from unoUtil.vehicleTest.ACCBRK.VT_ACCBRK import VT_ACCBRK, VT_ACCBRK_load, VT_ACCBRK_merge

# 1. EV3 IW01 마스터 디렉토리 설정 및 대상 의뢰서 일괄 정의
BASE_DIR = Path(r"D:\uno\1. 2026\1. BRK\Autobuild IW01_EV3")
TARGET_REQS = [
    '26RE040025KF',  # 1st Mold 0_0
    '26RE070033KF',  # 2nd Mold 1_2
]

dict_all_pjt = {}
infor_common = {'TestVehicle': 'EV3', 'TestVehicleType': 'EV', 'TestVehicleLayout': 'FF', 'TestLocation': 'TR'}

# 2. 다중 의뢰서 순회 일괄 루핑 파이프라인 가동
for req_code in TARGET_REQS:
    # 각 의뢰서 명칭이 포함된 하위 루트 디렉토리 탐색
    dir_path = next(BASE_DIR.glob(f"{req_code}*"), None)
    if not dir_path:
        continue
        
    print(f"\n🚀 [실행] {req_code} 배치 자동화 가동: {dir_path.name}")
    
    # 래퍼 주입용 매핑 딕셔너리 동적 초기화
    dict_path, dict_req, dict_surface, dict_cond, dict_testSpeed, dict_selmode, dict_correct_type = {}, {}, {}, {}, {}, {}, {}
    
    # 하위 폴더들을 탐색하며 노면(surface) 및 레인(lane) 채널 동적 파싱 구축 🎯
    for folder in sorted(dir_path.glob('*')):
        if folder.is_dir() and not folder.name.startswith(('0.', '1.', '2.')):
            lane = folder.name.split('_')[-1]       # 예: 'lane1' 또는 'lane4'
            surface = folder.name.split('_')[-2].lower()  # 'dry' 또는 'wet'
            path_name = f"{surface}_{lane}"
            
            dict_path[path_name] = folder
            dict_req[path_name] = req_code
            dict_surface[path_name] = surface
            dict_cond[path_name] = lane
            dict_testSpeed[path_name] = [80, 1] if 'wet' in surface else [100, 1]
            dict_selmode[path_name] = 'max_min'
            dict_correct_type[path_name] = 'control'
            
    # 해당 의뢰서별 고유 스펙 및 마킹 하드웨어 정보 오버라이드 매핑
    spec_map = {
        '26RE040025KF': {'C1': 'EXT-2026-00147', 'T1': 'EXT-2026-00148', 'T2': 'KPKT1033338X00013', 'C2': 'EXT-2026-00147'},
        '26RE070033KF': {'C1': 'EXT-2026-00147', 'T1': 'EXT-2024-00280', 'T2': 'KPKT1033338X00013', 'C2': 'EXT-2026-00147'}
    }[req_code]
    
    excel_cfg = {
        'excel_path': str(dir_path / "graph.xlsx"),
        'sheet_name': 'Graph',
        'sheet_summary': 'Graph_Summary',
        'fig_object': None, 'start_cell': 'B2', 'width': 150, 'height': None
    }
    
    # 래퍼 단일 실행 호출 (동적 딕셔너리 오버라이딩 적용)
    dict_all_pjt[req_code] = VT_ACCBRK(
        path=dict_path, ref_time={'time': 9}, infor=infor_common,
        req=dict_req, cond=dict_cond, surface=dict_surface,
        spec=spec_map, item='brk', test_vel=dict_testSpeed,
        sel_mode=dict_selmode, correct_type=dict_correct_type,
        close_tire=True, close_pjt=True, save_pjt=True, excel=excel_cfg
    )

# 3. [POST-ANALYSIS] 사후 세대 간 교차 비교 분석 (1st vs 2nd Mold)
print("\n🔥 [대조 분석] 1세대(0_0) vs 2세대(1_2) 타이어 교차 대조 시작")
dir_1st_wet = BASE_DIR / "26RE040025KF_IW01_EV3_1st Mold_0_0_Dry, Wet_0429" / "260428_Wet_lane4" / "0. db" / "260428_Wet_lane4.pjt"
dir_2nd_wet = BASE_DIR / "26RE070033KF_IW01_EV3_2nd Mold_1_2_Wet, Dry_0722" / "260722_EV3_Wet_lane4" / "0. db" / "260722_EV3_Wet_lane4.pjt"

# 대소문자 0. db / 0. DB 폴더 호환성 체크 
if not dir_1st_wet.exists():
    dir_1st_wet = dir_1st_wet.parent.parent / "0. DB" / "260428_Wet_lane4.pjt"
if not dir_2nd_wet.exists():
    dir_2nd_wet = dir_2nd_wet.parent.parent / "0. DB" / "260722_EV3_Wet_lane4.pjt"

if dir_1st_wet.exists() and dir_2nd_wet.exists():
    # .pjt 프로젝트 복수 역직렬화 로드
    combined_pjts = VT_ACCBRK_load([str(dir_1st_wet), str(dir_2nd_wet)], restore=False)
    
    # 1세대 lane4 데이터와 2세대 lane4 데이터를 수평 결합 (Merge)
    compare_molds_wet = VT_ACCBRK_merge(
        dict_pjt=combined_pjts,
        suffix=['1st_lane4', '2nd_lane4'],
        sel_tire=['C1', 'T2', 'C2'], # 비교 타겟인 C1, T2, C2 타이어만 필터링
        order_col='TestTireSet'
    )
    
    # 시각화 변별력을 위한 커스텀 스타일 및 마커 딕셔너리 구성 🎨
    list_tab10 = gen_list_colors(10)
    dict_colors = {'C1': list_tab10[0] + (1.0,), 'C2': list_tab10[1] + (1.0,), 'T2': list_tab10[2] + (1.0,)}
    
    # 1세대는 점선(-.), 2세대는 실선(-)으로 선형 구분 적용
    dict_lines = {'1st_lane4': '-.', '2nd_lane4': '-'}
    
    # 속도 대역별 가속 응답 오버레이 선플롯 출력
    compare_molds_wet.plot.compare_acceleration(
        color=dict_colors, linestyle=dict_lines,
        color_legend=dict_colors, linestyle_legend=dict_lines
    )
    
    # 1세대는 X마커, 2세대는 다이아몬드(D)마커로 가시성 극대화 산점도 분석
    dict_markers = {'1st_lane4': 'X', '2nd_lane4': 'D'}
    compare_molds_wet.plot.compare_scatter_detail(
        col_x='온도', col_y='brk_dist',
        color=dict_colors, marker=dict_markers,
        color_legend=dict_colors, marker_legend=dict_markers,
        label_x="Air Temperature [℃]", label_y="Braking Distance [m]",
        title="EV3 1st vs 2nd Mold Braking Scatter (Wet)"
    )
    plt.show()
```

---

## 7. 실무 문제 해결 및 아키텍처 제약 규칙 (Troubleshooting)

| 발생 가능한 버그 및 오류 현상 | 아키텍처 원인 분석 | 실무 즉각 조치 가이드 및 해결책 |
|:---|:---|:---|
| **타이어별 스펙/마킹 정보가 고정되어 서로 섞여 나오는 현상** | 전역 `info` 딕셔너리 하단에 실수로 특정 타이어 세트명(예: `set: 'C1'`)을 하드코딩한 경우, 자동 세트 인식기가 무력화되어 발생합니다. | 전역 `info:` 설정 맵 내부의 `set` 및 `cond` 항목은 반드시 빈 값(**`null` 또는 `None`**)으로 공백 유지해 주십시오. |
| **`PermissionError: [Errno 13] Permission denied`** | 보고서용 통합 엑셀 파일(`graph.xlsx`)을 윈도우 엑셀 환경에 열어둔 채 분석 코드를 재가동할 때 쓰기 권한이 락업되어 발생합니다. | 가공 전, **현재 열려 있는 해당 결과 엑셀 시트 창을 수동으로 완전히 닫은 후** 분석 코드를 재실행해 주십시오. |
| **줄바꿈 후 경로가 손실되는 현상 (`FileNotFoundError`)** | YAML 마스터 파일의 긴 경로를 작은따옴표(`'`) 내에서 수동 줄바꿈할 경우, YAML 파서가 개행 자리에 공백을 삽입하여 경로가 깨집니다. | 홑따옴표 멀티라인을 쓰지 말고, 가급적 **한 줄로 길게 경로를 타이핑한 뒤 PyCharm의 자동 줄바꿈(`Soft-Wrap`) 환경**을 가동해 주십시오. |
| **`KeyError` 또는 `AttributeError`로 인한 비정상 종료** | 계측 데이터의 파일명 포맷 규칙(`_구분자` 형태)이 맞지 않아 내부 정제 파서가 세트 식별자(`infor_set`)를 긁어오지 못하는 현상입니다. | 원시 계측 파일명 끝자리가 반드시 **`*_C1.vbo`**, **`*_T1.d7d`** 와 같이 언더바(`_`) 및 영수 숫자 규칙을 준수하고 있는지 포맷을 정렬하십시오. |

---