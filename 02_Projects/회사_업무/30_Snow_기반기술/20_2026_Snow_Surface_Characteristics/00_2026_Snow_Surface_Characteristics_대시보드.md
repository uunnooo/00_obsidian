---
id: "work_2026_snow_surface"
title: "00_2026 Snow Surface Characteristics 프로젝트 대시보드"
type: project
category_main: 회사_업무
category_sub: SnowSurface
date: 2026-09-10
status: 진행중
tags:
  - 회사_업무
  - SnowSurface
  - 노면특성
  - 데이터분석
  - 머신러닝
aliases:
  - "2026_Snow_Surface_Characteristics"
  - "00_2026_Snow_Surface_Characteristics_대시보드"
  - "2026-09-18_스노우노면_일지개편_및_세션보간파이프라인_작업보고"
---

# 💼 2026 Snow Surface Characteristics (스노우 노면 특성 분석)

> [!ABSTRACT] ❄️ 프로젝트 개요
> 자연 기상 상태에서 급변하는 눈 트랙의 상태(눈 다져짐 깊이, 기온, 습도)를 수학적으로 격리하여, **어떤 날씨에서 테스트하든 타이어 고유의 성능 실력만 공정하게 뽑아내는 머신러닝 보정 시스템** 개발 과제입니다.

---

## 📅 1. 프로젝트 주요 버전 이력 (Changelog 타임테이블)

| 버전 | 날짜 | 작업자 | 핵심 수정 및 개발 내역 (Changelog) | 상태 |
| :---: | :---: | :---: | :--- | :---: |
| **v1.2** | 2026-09-21 | uno &<br/>Gemini | 🛠️ 글로벌 개발 규격(`PYTHON_CODE_AGENT`) 100% 매칭 적용 완료<br/>🔤 8대 표준 동사 네이밍 수립 (`calc_`, `get_` 등) 및 하위 호환 에일리어스 가동<br/>🧪 5대 코어 모듈 닥스트링, 타입힌트, 3-시나리오 자가 구동 테스트 스위트 보강<br/>🛑 Non-blocking 시각화 및 4단계 `save` 다형성 설계 구현<br/>📚 1:1 동명 마크다운 매뉴얼 파일 5종 구축 완료 | ✅ 완료 |
| **v1.0** | 2026-09-18 | uno | ❄️ 3D 시공간 디지털 트윈 매칭 및 차분 머신러닝 보정 파이프라인 초안 구축<br/>⚡ 1-Run 고속 집계 (`a_make_SnowAccBrkTest_DF.py`) 및 세션 보간 파이프라인 연계 완료 | ✅ 완료 |

---

# 1. 노면 눌림량 계측 Infra

> [!NOTE] 📸 센서 지그 및 계측 인프라 구성
> 차량 휠 주변 및 외곽에 설치된 다채널 변위 센서를 통해 노면 높이 및 눈 눌림 깊이를 실측하는 인프라입니다.

![[_attachments/10_회사_업무/40_2026_Snow_Surface_센서_인프라.png|650]]

### ⚙️ 계측 및 데이터 처리 핵심
* **센서 위치에 따른 높이 옵셋 설정**:
  * 기구적 지그 길이와 센서별 장착 높이의 오차를 보정하기 위해 전체 계측 데이터 평균값 차이를 기준으로 옵셋 설정.
  * Out(외측)과 Tire(타이어부) 센서 간의 옵셋 매칭 및 차이를 산출하여 순수 눈 눌림량 정량치 추출.

---

## 2. 노면 정비(Preparing) 기반 세션 분류 및 고속 벡터화 파이프라인 (2026-09-18 구축)

> [!TIP] 💡 트랙터 정비(Preparing)에 따른 물리적 리셋 체계
> * **Preparing 2번 (오전 1회 + 점심 1회):** 점심시간 트랙터가 노면을 갈아엎고 재평탄화(Reset)하므로 오전 다져진 빙판과 오후 부드러운 노면 사이의 시간 연속성이 단절됨 ➔ **`오전`**, **`오후`** 2개 세션 분리.
> * **Preparing 1번 (아침 1회만):** 점심 재정비 없이 종일 연속 주행하여 노면 다져짐이 하루 종일 누적 지속됨 ➔ **`종일`** 단일 세션.
> * **Preparing 없음 / 혹한 1회 주행:** 노면 정비 없음 ➔ **`종일`** 단일 세션.
> * **데이터셋 적용:** `df_surface.csv` 및 `df_surface.pkl`에 `Cond` (`오전`/`오후`/`종일`), `Cond_ID` (`YYYY-MM-DD_세션`), `Preparing` 컬럼 1,105건 전수 부여 완료 (`a_make_SnowSurfaceCharacteristic_DF.py`).
> * **보간 실행 가이드:** `groupby('Cond_ID')` 단위로 분리하여 노면 리셋 전/후가 섞이지 않도록 시계열 보간 수행.

> [!NOTE] ⚡ 제동 1회 단위(1-Run) 고속 벡터화 집계 파이프라인 (`a_make_SnowAccBrkTest_DF.py`)
> * **5중 중첩 루프 병목 제거**: 기존 `Date` ➔ `ReqNo` ➔ `TestOrder` ➔ `TestTireSet` ➔ `TestNum` 순차 순회 방식을 일자별 1단계 슬라이싱(`unique_dates`) 후 4대 복합키 단 1회 벡터화 `df_day.groupby(group_keys).agg(**agg_rules)`로 전면 개편.
> * **메모리 방어 및 속도 향상**: 대용량 DataFrame 전체 복제에 의한 `MemoryError`를 원천 차단하고 집계 소요 시간을 초 단위로 단축.
> * **안전망 구축**: `time_span` 기반 `AccTime` 벡터화 병합, `df_brk.pkl` 중간 대표값 캐시 저장 및 `len(list_tmp_df) > 0` 가드 로직 탑재.

---

## 🔗 연관 세부 프로젝트 및 핵심 알고리즘

* 📋 **[[30_SnowSurface_DailyNote|SnowSurface DailyNote (통합 노면일지)]]**
  * **[테이블 1]** 일자별 환경 조건 및 노면 총괄 마스터 (20행: Preparing 횟수, 강설 타임라인, 노면 총평)
  * **[테이블 2]** 세션별 제동 성능 및 노면 센서 수치 마스터 (57행: Line 1~3, SRTT, 전체평균, 편차, 눌림량, 기온 콤팩트 피벗)
  * **[테이블 3]** 세션별 주행 관측 및 엔지니어링 메모 마스터 (28행: 시간대별 가속감, 미끄러움, 잔설, 센서 세팅 메모)
* 🚀 **[[20_SnowBrakingPerformance_통합모듈_매뉴얼|SnowBrakingPerformance 통합 모듈 매뉴얼]]**
  * 노면 데이터/제동 평가(ACCBRK) 누적 등록, 3D 디지털 트윈, 차분 ML 보정 및 스펙 영향도 분석 마스터 클래스
* ❄️ **[[31_스노우_노면_디지털트윈_및_제동성능_보정_위키|스노우 노면 디지털 트윈 및 제동 성능 환경 보정 종합 위키]]**
  * 1-Run 집계(`a_make_SnowAccBrkTest_DF.py`), 노면 세션(`Cond_ID`) 파이프라인(`a_make_SnowSurfaceCharacteristic_DF.py`), 차분 머신러닝 노면 Decoupling 및 웹 대시보드
* 📊 **[[10_노면특성_계측데이터_분석|노면특성 계측데이터 분석]]**
  * 다채널 센서 계측 로우데이터 기반 노면 특성 데이터베이스 구축
* 🧠 **[[30_Snow_제동성능보정_알고리즘|Snow제동성능보정 알고리즘 (Resources)]]**
  * **1단계 (시공간 디지털 트윈)**: 공간 예측 (Random Forest) ➡️ 시간 보간 (scipy interp1d) ➡️ VBOX GPS 격자 매칭
  * **2단계 (차분 머신러닝 보정)**: 타이어 고유 실력 소거(차분법) ➡️ KNN(3D 등고선 맵 시각화) + Random Forest(최종 정밀 보정 엔진)
* ❄️ **[[04_Resources/30_스노우_노면_공학/00_스노우_노면_공학_통합_색인|스노우 노면 공학 통합 지식 색인 (MOC)]]**