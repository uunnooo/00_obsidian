---
id: "unoutil_dict_vt_acc_brk"
title: "vt_acc_brk 모듈 사전"
type: resource
category_main: 회사_업무
category_sub: unoUtil_사전
date: 2026-10-18
status: 상시운용
tags:
  - 회사_업무
  - unoUtil
  - unoUtil_사전
  - vt_acc_brk
  - 가감속제동
  - 차량동역학
aliases:
  - "vt_acc_brk_사전"
  - "vt_acc_brk 모듈 사전"
---

# 📖 vt_acc_brk 모듈 사전 (Domain Engineering Guide)

> ⚡ **Quick Jump**: [🎯 1. 설계 철학](#-1-설계-철학-및-모듈-개요) · [📚 2. 배경 지식](#-2-배경-지식-및-이론-지식-허브) · [🏗️ 3. 아키텍처](#️-3-아키텍처-및-데이터-파이프라인) · [🚀 4. 실전 워크플로우](#-4-실전-워크플로우-및-종합-스니펫) · [🛠️ 5. 트러블슈팅](#️-5-트러블슈팅-및-튜닝-노하우)

> [!ABSTRACT] 🏎️ 도메인 개요
> 실차 주행 시험에서 계측된 VBOX/Dewesoft 시계열 데이터로부터 가감속 및 제동 거동(MFDD, 슬립율, 제동거리, 응답시간)을 정밀 추출하고, **콘트롤 타이어 시계열 선형 보간 및 환경 보정을 통해 타이어 순수 성능 지수를 자동 산출하는 핵심 엔진**입니다.

---

## 🎯 1. 설계 철학 및 모듈 개요

### 1.1. 탄생 배경과 목적
* **기존 방식의 한계**: 수동 엑셀 분석 시 작업자마다 제동 시작점(트리거) 기준이 달라 수 미터의 오차 발생. 평가 중간 노면 온도 변화($\text{m}/^\circ\text{C}$)와 마찰계수 변화에 따른 왜곡 보정 체계 부재.
* **해결 과제**: 브레이크 시작점 자동 탐지(`find_brake_start_point`), 13대 물리 연산 표준화, 콘트롤 타이어 시계열 선형 보간 엔진 통합.
* **핵심 가치**: 단일 타이어 분석(`tire`) $\to$ 프로젝트 취합(`project`) $\to$ 원스톱 자동화 배치(`vt_acc_brk`) 3단계 계층 구조 및 Flat 단일 계층 저장소 정합.

### 1.2. 아키텍처 설계 사상
* **Single Stem Law (단일 식별자 불변 원칙)**: 타이어 객체 식별자(`[req]_[surface]_[item]_[cond]_[vel_tag]_{set}`)가 `.tir` 파일명, 차트 타이틀, 저장 이미지명과 100% 일치하도록 보장.
* **인메모리 프록시 캐싱 (`BaseMemory`)**: 대용량 실차 시계열 데이터를 딕셔너리 및 슬림 피클링으로 관리하여 반복 호출 시 디스크 I/O 병목 제거.
* **No Redundant Prefix**: 시각화 플로터(`PlotterTire`, `PlotterProject`) 메서드에서 중복 동사를 제거하여 `plotter.accbrk()`, `plotter.compare_braking()` 형태로 직관적 API 구축.

---

## 📚 2. 배경 지식 및 이론 (지식 허브)

> [!NOTE] 🧠 공학 이론 및 알고리즘 위키 링크 (Knowledge Atomization)
> *제동 동역학 및 보정 이론은 `04_Resources`에 완결된 단일 백서로 구축되어 있습니다.*

* 📄 **실차 가감속 종합 백서**: [[30_실차_가감속_성능변화_분석_및_보정_시스템|실차 가감속 성능변화 분석 및 보정 시스템 (마스터 백서)]]
* 📄 **제동 시작점 자동 탐지**: [[31_실차_제동_시작점_자동_탐지_및_과도응답_슬립_복원_공학|브레이크 시작점 노이즈 방어 및 슬립율 복원 공학]]
* 📄 **차량 제동 동역학**: [[10_차량_제동_동역학_시뮬레이션|타이어-노면 마찰 및 하중 이동 제동 동역학]]
* 📄 **노면온도 감인성 분석**: [[11_노면_온도와_타이어_제동_상관관계|노면 온도와 타이어 제동 거리 상관관계 (m/℃)]]
* 📄 **마찰계수 상관관계**: [[12_차량_시스템_제동성능과_마찰계수_상관관계|차량 시스템 제동성능과 마찰계수 상관관계]]
* 📄 **ABS 유압 제어 메커니즘**: [[20_ABS_로직_및_3단계_유압제어_분석|ABS 3단계 유압 제어 및 압력 맥동 분석]]
* 📄 **좌표계 변환 역학**: [[10_차량동역학_측정점_기준점_운동역학_변환|차량 계측점 기준점 동역학 변환]]
* 📄 **인메모리 캐싱 패턴**: [[30_대용량_시계열_인메모리_프록시_및_비파괴_캐싱_패턴|대용량 시계열 인메모리 프록시 아키텍처]]
* 📄 **표준 네이밍 기술 백서**: [[50_vt_acc_brk_표준_네이밍_규칙_및_저장_구조|가감속/제동 Flat 네이밍 규칙 및 저장 구조]]

---

## 🏗️ 3. 아키텍처 및 데이터 파이프라인

### 3.1. 엔드-투-엔드 데이터 흐름도

```mermaid
flowchart TD
    VBO["VBOX 원시 파일 (*.vbo, *.vbb)"] --> Reader["FileDataReader / Parsers"]
    Reader --> TireLevel["VTAccBrkTire\n(단일 타이어 런 분석, 슬립율/MFDD 산출)"]
    TireLevel --> BaseMem["BaseMemory (RAM 캐시 & .tir 직렬화)"]
    BaseMem --> PjtLevel["VTAccBrkProject\n(콘트롤 타이어 시계열 조각 선형 보간)"]
    PjtLevel --> Correct["Correct.py\n(온도 감인성 m/℃ 및 환경 보정)"]
    Correct --> Plotter["PlotterProject / PlotterTire\n(Non-blocking 비교 시각화)"]
    Plotter --> Final["Excel 리포트 & Flat 저장소 (.pjt, .fig)"]
```

### 3.2. 핵심 서브모듈 역할 분담표

| 서브모듈 파일명 | 담당 클래스 / 함수 | 핵심 책임 및 역할 |
| :--- | :--- | :--- |
| `vt_acc_brk.py` | `vt_acc_brk` | 전체 프로젝트 일괄 배치 및 최상위 오케스트레이션 (`col_curve_fit_wheelslip`, `cf_*` 3계층 분기 패스스루) |
| `vt_acc_brk_tire.py` | `VTAccBrkTire` | 단일 타이어 런 분할, 제동 시작점 검출, 7대 서브 분석기(`acceleration`, `response`, `slip_pdf`, `mu_drop`, `skewness`, `split_speed`, `curve_fit`) 및 런별·MF 피팅 지표(`cf_*`) 집계 |
| `vt_acc_brk_project.py`| `VTAccBrkProject` | 다중 타이어 취합, 콘트롤 타이어 시계열 선형 보간, `curve_fit` 보정 동기화 및 성능지수(`index_cf_*`) 산출 |
| `correct.py` | `Correct` | 노면온도 감인성(m/℃), 콘트롤 타이어 선형 보간 및 `analyzer.curve_fit` 게인($G_i$) 동기화 |
| `base_memory.py` | `BaseMemory` | 대용량 시계열 RAM 프록시 및 비파괴 슬림 피클링 관리 |
| `func_acc_brk.py` | `find_brake_start_point` 등 | 13대 핵심 물리 수식 (MFDD, 슬립율, 제동에너지, 감속도 등) |
| `plotter_tire.py` | `PlotterTire` | 단일 타이어 9대 시각화 (`accbrk`, `acceleration`, `response`, `slip_pdf`, `mu_drop`, `skewness`, `split_speed`, `curve_fit`, `curve_fit_detail`) |
| `plotter_project.py`| `PlotterProject` | 프로젝트 시험 간 9대 비교 플로터 (`compare_braking`, `compare_curve_fit` 등) |
| `analyzers/` (6대 서브) + `cf_tire.py`| `AnAcceleration`, `TireCurve` 등 | 가속대역, 감속응답, 슬립PDF, Mu-Drop, 왜도, 구간속도분할 및 Magic Formula 커브 피팅 전문 분석 |

### 3.3. 온디맨드(On-demand) 하이브리드 캐싱 아키텍처 및 센티널 라이프사이클 (v3.69)

#### 1) `None` vs `빈 데이터프레임(pd.DataFrame())`의 역할과 상태 전이 모델
`unoUtil v2` 분석기(`analyzers/`) 및 최상위 오케스트레이터(`VTAccBrkTire`)는 대용량 시계열 연산의 병목을 없애고 RAM 누수를 방지하기 위해 **온디맨드(On-demand) 자가 복원 프로퍼티 패턴**을 채택하고 있습니다. 여기서 `None`과 `pd.DataFrame()`(빈 DF)은 정반대의 명확한 라이프사이클 책임을 갖습니다:

| 상태 값 | 내부 의미 | `@property` 접근 시 동작 | 발생 시점 |
| :---: | :---: | :---: | :---: |
| **`None`** | **캐시 부재 / 메모리 소거**<br/>(연산 미수행 상태) | **`analysis()` 백그라운드 자동 복원 기동** | 최초 인스턴스 생성 시, `.tir` 저장 직렬화 시(`__getstate__`), `clear_cache()` 호출 시 |
| **`pd.DataFrame()`**<br/>(`empty == True`) | **연산 완료 (결과 부재 센티널)**<br/>(Sentinel Value) | **재연산 절대 금지! 빈 DF $O(1)$ 즉시 반환** | `analysis()`를 실행했으나 휠속도 채널 부재 또는 유효 구간 미검출로 조기 종료된 경우 |
| **`pd.DataFrame`**<br/>(`empty == False`) | **연산 완료 (정상 데이터 적재)** | **결과 데이터프레임 $O(1)$ 즉시 반환** | `analysis()`가 정상 완료된 경우 |

> [!IMPORTANT] 🛡️ 빈 데이터프레임의 센티널(Sentinel) 방어막 역할
> 만약 휠속도나 시험 구간이 없다고 해서 `self._df`를 `None`으로 남겨두면, 시스템은 이를 "아직 연산되지 않았거나 캐시가 비워진 상태"로 오판하여 프로퍼티(`.df`, `.summary`)를 조회할 때마다 `analysis()`를 무한히 재호출하는 **연쇄 호출 폭탄(Cascade Loop)**이 발생합니다.
> 따라서 `analysis()` 시작 시점에 빈 데이터프레임(`self._df = pd.DataFrame()`)을 채워두고 조기 종료함으로써, `self._df is not None` 상태를 만들어 **"이미 확인해 보았으니 재연산하지 말라"**는 센티널 방어막을 구축합니다.

#### 2) 선제적 빈 데이터프레임 초기화 (Pre-emptive Initialization) 패턴
`VTAccBrkTire.analysis()` 및 하위 분석기 모듈들은 메서드 진입 즉시(try 블록 최상단) 모든 결과 필드를 빈 데이터프레임으로 선제 초기화합니다:
```python
# VTAccBrkTire.analysis() 및 AnSlipPdf.analysis() 진입 즉시
self._result.df = pd.DataFrame()
self._result.summary = pd.DataFrame()
self._result.summary_all = pd.DataFrame()
self._result.detail = pd.DataFrame()
self._result.detail_all = pd.DataFrame()
```
* **효과**: 시험 속도 불일치, 속도/가속도 센서 노이즈, 유효 런 미검출 등으로 인해 중간에 어떤 지점에서 조기 반환(`return self`)하더라도, 모든 결과 속성이 안전한 빈 `pd.DataFrame()`으로 보장됩니다.
* **크래시 방어**: 외부 호출자나 시각화 플로터(`PlotterTire`, `PlotterProject`)에서 `tire.result.summary.empty`나 `tire.result.df.columns`에 접근할 때 **`AttributeError: 'NoneType' object has no attribute...`로 인한 시스템 다운을 100% 원천 차단**합니다.

#### 3) 단일 위임(Single Delegation) 및 책임 분리 헌장
* **단일 생성 책임**: 휠속도 채널 검증(`is_col_wheel_speed`) 및 휠 슬립률 시계열(`SR*`) 생성의 책임은 오직 **`AnSlipPdf`**에만 있습니다.
* **하위 분석기의 단일 위임**: `AnSlipModeSkewness`, `AnResponse`, `AnMuDrop` 등 슬립률을 소비하는 하위 분석기들은 상위 `test.df`의 컬럼을 직접 까보며 중복 가드를 치지 않고, 오직 `if self.test.slip_pdf.df.empty: return self` 단일 위임 조건만으로 우아하게 조기 종료합니다.
* **시각화 모듈 연계 안정성**: `PlotterTire`와 `PlotterProject`의 수많은 플롯 가드가 프로퍼티를 반복 조회하더라도, 이미 $O(1)$ 즉시 반환되므로 경고 로그 누출이나 재연산 병목 없이 안전하게 시각화를 건너뜁니다.

---

## 🚀 4. 실전 워크플로우 및 종합 스니펫

```python
"""
vt_acc_brk 가감속/제동 프로젝트 원스톱 실행 및 curve_fit 서브 분석·보정 비교 스크립트
"""
from pathlib import Path
from unoUtil.vehicle.acc_brk import (
    vt_acc_brk,
    VTAccBrkProject,
)

# 1. 가감속/제동 마스터 래퍼 실행 (curve_fit 옵션 3계층 자동 패스스루)
pjt_dir = Path("D:/test_data/acc_brk/pjt_bmw320_mock")
projects = vt_acc_brk(
    paths=pjt_dir,
    test_vel=[100, 5],
    cf_method="robust",
    cf_filter_transient=True,
    plot=True,
    excel=True,
)
project: VTAccBrkProject = projects[0]

# 2. 보정 성능 결과 및 MF 피팅 요약 데이터프레임 추출
summary_df = project.summary.df
print(summary_df[["TestSet", "mean_Distance", "corr_mean_Distance", "cf_peak_mu", "corr_cf_peak_mu", "index_cf_peak_mu"]])

# 3. 개별 타이어 상세 MF 진단 및 프로젝트 보정 MF 커브(0~1.0) 오버레이 비교 (Non-blocking)
first_tire = next(iter(project.tire_analyzers.values()))
first_tire.plot.curve_fit(detail=True, close=True)
project.plot.compare_curve_fit(corr="mean", xlim=(0.0, 1.0), show_peak=True, close=True)
```

---

## 🛠️ 5. 트러블슈팅 및 튜닝 노하우

### 5.1. 제동 시작점 50km/h 컷에 따른 외삽 결함 발생 시
* **증상**: 감속도 $0 \to 0.45\text{g}$ 구간이 조기 절단되어 음수 슬립율이 발생하거나 클램핑 수평선 결함 발생.
* **조치**: `func_acc_brk.py`의 `find_brake_start_point(window=11, baseline_sec=1.0, persistence=5)`를 적용하여 정속 기저선 대비 3중 노이즈 필터링으로 과도응답 램프업 구간을 자동 복원.

### 5.2. 콘트롤 타이어 평가 차수 불균형
* **증상**: C1과 C2 사이 시험 타이어가 과도하게 많거나 시간 간격이 4시간 이상 벌어져 선형 보간의 신뢰도 저하.
* **조치**: `correct.py`의 `set_interpolation_mode(mode='segmented_linear')`를 호출하거나, 온·습도 기상 DB가 존재하는 경우 `Correct.run(weather_adjust=True)`를 켜서 노면 온도 감인성 보정을 병합 적용.

### 5.3. `curve_fit` 서브 분석기 휠스피드 부재 방어 및 구동방식(`TestVehicleLayout`) 연동 (v3.48)
* **휠스피드 부재 시 자동 Skip**: CAN/아날로그 휠스피드 채널이 없는 GPS 단독 계측 데이터에서는 `tire.curve_fit`이 에러 없이 `is_fitted = False`로 자동 Skip되어 기존 6대 서브 분석기와 요약표가 정상 산출됨.
* **제동/가속 슬립 축 자동 선택**: 제동(`brk`)은 기본 전륜축(`FL`/`FR` 유효 채널 평균)을 사용하며, 가속(`acc`)은 `TestVehicleLayout` 메타데이터가 `RWD`이면 후륜축(`RL`/`RR`), `AWD`/`4WD`이면 4륜 전체, `FWD`/미지정 시 전륜축을 자동 선택함 (`col_curve_fit_wheelslip`으로 명시적 오버라이드 가능).
* **콘트롤 보정 게인($G_i$) 자동 동기화**: `Correct.run()` 실행 시 별도 재피팅 없이 [[30_실차_가감속_성능변화_분석_및_보정_시스템#7. 🎯 비선형 마찰 곡선(Magic Formula)의 콘트롤 게인 스케일링 동형성 법칙 (Control Gain Scaling Isomorphism)|콘트롤 게인 스케일링 동형성 법칙]]에 의해 `tire.curve_fit.df`(`corr_mean_Acc`, `corr_curve_Acc`) 및 `params`(`corr_D`, `corr_peak_mu`, `corr_stiffness`)가 자동 갱신됨.

### 5.4. 온디맨드 프로퍼티 무한 재호출 및 NoneType 크래시 트러블슈팅 (v3.69)
* **증상**: 휠속도 채널이 없는 시험 데이터를 로드한 후 `tire.plot()` 또는 `tire.slip_pdf.df`, `tire.result.summary`에 접근할 때마다 `[WARNING] 휠속도에 대한 채널이 없습니다` 경고가 수십 번 반복 출력되거나 `NoneType has no attribute 'empty'` 에러 발생.
* **원인**: 
  1. `an_slip_pdf.py`의 `df` 프로퍼티에 과거 휠 지연 보정 개발 시 작성된 과도기 코드 `not cached_df.attrs.get("wheel_delay_compensated", False)`가 잔존하여, 빈 데이터프레임이 캐싱되어 있음에도 매번 `analysis()`를 강제로 재호출함.
  2. `VTAccBrkTire.analysis()` 조기 반환 시 `_result.summary` 등이 `None`으로 방치되어 외부 호출부에서 크래시 발생.
* **조치**:
  1. `an_slip_pdf.py`의 과도기 조건문을 제거하고 표준 `if self._df is None:` 온디맨드 캐싱 패턴으로 복원.
  2. `VTAccBrkTire.analysis()` 최상단에 선제적 빈 DataFrame 초기화(`self._result.summary = pd.DataFrame()`)를 적용하여 안전성 완결.
