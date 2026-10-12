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

> ⚡ **Quick Jump**: [📅 1. 체인지로그](#-1-프로젝트-주요-버전-이력-changelog-타임테이블) · [📸 2. 센서 인프라](#-2-노면-눌림량-계측-infra) · [⚡ 3. 세션분류&벡터화](#-3-노면-정비preparing-기반-세션-분류-및-고속-벡터화-파이프라인) · [🤖 4. 보정 모델 후보군 & 비교 검증](#-4-환경-보정-후보-머신러닝-모델-비교-및-검증-현황-model-candidates-landscape) · [🔗 5. 연관 프로젝트](#-5-연관-세부-프로젝트-및-핵심-알고리즘) · [📜 6. 상세 개발 이력](#-6-상세-엔지니어링-개발-이력-changelog)

> [!ABSTRACT] ❄️ 프로젝트 개요
> 자연 기상 상태에서 급변하는 눈 트랙의 상태(눈 다져짐 깊이, 기온, 습도)를 수학적으로 격리하여, **어떤 날씨에서 테스트하든 타이어 고유의 성능 실력만 공정하게 뽑아내는 머신러닝 보정 시스템** 개발 과제입니다.

> [!IMPORTANT] 📢 unoUtil 전면 이관 및 아키텍처 재편 완결 (2026-09-30)
> 본 프로젝트에서 개발되었던 **노면 환경 계측, Sonntag 물리 역학, 3D/4D 시공간 디지털 트윈, Plotly 대시보드 및 머신러닝 차분 보정 엔진(`SnowCorrectionModel`, `SnowCorrectionValidator`, `SnowCorrectionPlotter`)**은 사내 공용 파이썬 프레임워크인 **[[00_snow_condition_대시보드|unoUtil.snow_condition]]**으로 **전면 승격 이관**되었습니다.
> * **`unoUtil.snow_condition`**: 노면 환경 계측/정규화, 3D 디지털 트윈, 6대 ML 회귀 보정, 대조표 산출, 4대 검증 차트 시각화 전담
> * **`2026_Snow_RoadSurface_characteristics` (본 프로젝트)**: 순수 타이어 사양별 성능 분석(`snow_braking_performance.SnowSpecAnalyzer`) 및 실데이터 1,964건 전수 파이프라인(`c_run_snow_correction_pipeline.py`) 전담
> * **`Snow_braking_relate_condition`**: 구버전 코드 호환을 위한 경량 브릿지 어댑터로 전환 완료 (과거 구현 파일은 `_archive/`로 영구 격리)

---

## 📅 1. 프로젝트 주요 버전 이력 (Changelog 타임테이블)

|    버전    |     날짜     |       작업자        | 핵심 수정 및 개발 내역 (Changelog)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |  상태  |
| :------: | :--------: | :--------------: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--: |
| **v2.2** | 2026-10-08 | uno &<br/>Gemini | 🤖 **환경 보정 다중 모델 후보군(Multi-Model) Side-by-Side 비교 엔진 및 슬로프 모델 고도화**<br/>• **복원 수렴도 다중 모델 비교 플롯(`scatter_restoration_comparison`)**: RF, SVR, KNN 등 복수 후보 모델의 1차(Ref) vs 2차(Raw/Corr) 일치도 및 $y=x$ 수렴 벡터를 1행 N열 서브플롯으로 1:1 직접 대조 (MAE 개선율, Adjusted $R^2$, Kendall $\tau$ 자동 표기)<br/>• **2D 등고선 다중 모델 비교 플롯(`correction_map_comparison`)**: 단일 공통 컬러바/등고선 레벨을 적용하여 모델 간 곡면 거동 차이를 왜곡 없이 나란히(Side-by-Side) 렌더링<br/>• **과거 히스토리 연계 슬로프 모델(`SnowSlopeModel`) 보강**: 러프하게 평활화된 2D-KNN 및 2D 다항회귀 슬로프 보정 파이프라인 정립 | ✅ 완료 |
| **v2.1** | 2026-10-01 | uno &<br/>Gemini | ❄️ **통합 실행 파이프라인 동적 특성 인자(x_cols, y_col) 지원, 결측치(NaN) 방어 및 CLI 인자 체계 구축**<br/>• **동적 파이프라인 인터페이스**: `c_run_snow_correction_pipeline.py`에 `--x-cols`, `--y-col`, `--model`, `--missing-strategy`, `--no-show` 커맨드라인 옵션 도입 (기온, 습도, 침하량 등 연구 목적별 자유로운 피처 전달 및 다변량 확장)<br/>• **시각화 및 산출물 100% 동적 라벨링**: 실제 선택된 피처명으로 산점도, 2D 등고선 맵(Fig 3), 엑셀 대조표 파일명 및 축 라벨 자동 갱신<br/>• **SnowSurfaceInterpolator 2줄 압축 연계**: `b_combine_surface_performance_spec.py`의 `fit` & `transform` 파이프라인 무결 검증 완료 (Exit Code 0)<br/>• **실데이터 1,964건 전수 검증**: 기본 실행 및 기온/습도 커스텀 인자 실행 전원 성공 (Exit Code 0, RF $R^2=0.86$, MAE 개선율 90.7%) | ✅ 완료 |
| **v2.0** | 2026-09-30 | uno &<br/>Gemini | 🏛️ 노면 컨디션/보정 패키지 `unoUtil.snow_condition`으로 완전 이관 및 `unoUtil` 12대 공식 도메인 승격 완료<br/>🧩 `acc_brk` 스타일 컴포지션 패턴(`model.validator`, `model.plot`) 아키텍처 완비<br/>📊 산점도 오버플랏(1st vs 2nd) 및 의뢰번호/타이어세트 다형성 비교 플롯(`plot_tire_subsets_comparison`) 신설<br/>🧹 `Snow_braking_relate_condition` 레거시 파일들 `_archive/` 격리 및 브릿지 어댑터 전환 완료<br/>🚀 실데이터 1,964건 통합 파이프라인(`c_run_snow_correction_pipeline.py`) 직렬 연계 및 Exit Code 0 무결성 통과 | ✅ 완료 |
| **v1.9** | 2026-09-30 | uno &<br/>Gemini | 🏛️ 노면 컨디션 모듈을 범용 패키지(`unoUtil.snow_condition`)로 전면 이관 및 독립화<br/>🧩 **`acc_brk` 스타일 컴포지션 패턴(Composition Pattern)** 기반 보정 엔진 3대 분할 완결 (`SnowCorrectionModel`, `SnowCorrectionValidator`, `SnowCorrectionPlotter`)<br/>🧹 레거시 `snow_condition` 폴더 삭제 및 파사드(`pipeline_facade`, `braking_evaluator`) 제거<br/>🏎️ `snow_braking_performance`는 순수 타이어 스펙 분석(`SnowSpecAnalyzer`) 전담으로 직교성 확립<br/>🚀 통합 파이프라인(`c_run_snow_correction_pipeline.py`) 직렬 리팩터링 및 실데이터 1,964건 무결 검증 완료 (Exit Code 0) | ✅ 완료 |
| **v1.6** | 2026-09-29 | uno &<br/>Gemini | 🏗️ Clean Architecture 최신 표준(`unoUtil.logger`) 전 모듈 일괄 마이그레이션 완료<br/>🛡️ 패키지 대소문자 회복 탄력성(Case Resilient Fallback) 적용 (`__init__.py`)<br/>🌤️ 10대 기상 채널 자동 매핑 및 결측 방어(Fallback) 메커니즘 구축<br/>⚡ 361개 노면 센서 3D 공간 보간 및 32개 전 세션 3D/2D 디지털 트윈 맵 일괄 자동 저장 (`b_combine_surface_performance_spec.py`)<br/>📐 **노면 눌림량 차분($\Delta\text{Height}$) 원점 대칭 좌표계(`[-3.0, +3.0] mm`) 복원** 및 0-시프트 왜곡 제거<br/>🏢 **마지막 회사 최종 기준선(`2026-09-23 19:52`, 커밋 `a917f6e`)과 모델 성능 지표 100% 정합 완료** (RF $R^2=0.5121$, KNN $R^2=0.5417$)<br/>🚀 실측 1,964건 통합 파이프라인 무결 통과 (`c_run_snow_correction_pipeline.py`, Exit Code 0) 및 4대 핵심 검증 차트 볼트 갱신 | ✅ 완료 |
| **v1.5** | 2026-09-23 | uno &<br/>Gemini | 🚀 스노우 제동-노면 차분 머신러닝 보정 통합 파이프라인 완성 (`c_run_snow_correction_pipeline.py`)<br/>📑 1st(Ref)/2nd(Corr) 전수 대조 데이터 테이블 생성 모듈화 (`calc_corrected_comparison_table`) 및 엑셀 자동 산출(209건)<br/>🗺️ 슬라이드 6번 표준 등고선 보정 맵(min=0 shift, 1단위 ticks, KNN 보간) 엔진 표준 탑재<br/>📊 4대 핵심 검증 시각화 모듈화 및 파사드 위임 (`plot_delta_prediction_scatter`, `plot_delta_braking_bar`, `plot_scatter_restoration`, `plot_correction_map`, `plot_tire_subsets_comparison`)<br/>🔤 Windows Malgun Gothic 자동 바인딩으로 한글 글리프 누락 UserWarning 완전 해결                                                                                                               | ✅ 완료 |
| **v1.4** | 2026-09-23 | uno &<br/>Gemini | 🎯 차분 보정 머신러닝 엔진 대개편 및 원스톱 파이프라인 완성 (`c_train_correction_and_plot_maps.py`)<br/>📥 원스톱 데이터 적재 API (`load_combined_data`) 신설 (검증/매칭플래그 원스톱 동기화)<br/>🤖 5-Fold 교차검증 기반 하이퍼파라미터 오토 튜닝(`auto_tune=True`) 및 수동 튜닝(`model_params`) 완비<br/>📈 단일 DT의 $R^2$ 음수 과적합 문제를 깊이/리프 제약으로 양수(+0.45) 정상 회복<br/>📄 종합 보정 분석 마크다운 보고서 자동 생성 API (`save_report_md`) 구현 및 다형성 `save` 표준 적용<br/>📊 모델 성능 비교, 3D 보정 맵, 잔차 의존성 소거, 타이어 세트별 박스플롯 자동 생성 및 검증 완료                                                                                                                                                                              | ✅ 완료 |
| **v1.3** | 2026-09-21 | uno &<br/>Gemini | 🧠 차분 머신러닝 보정 파이프라인 (Phase 2) 구축 및 검증 완료 (`c_train_correction_and_plot_maps.py`) <br/>📊 3D 제동거리 보정 성능 맵(Delta Correction Map) 시각화 및 저장 (KNN/RF 3D 등고선)<br/>⚖️ 기준 환경(`char_height`=3.0mm, `cd_test_ah`=1.5g/m³) 일괄 정규화 보정 적용 및 `df_combine_test_surface_spec_corrected.pkl` 저장<br/>💾 플랫폼 세션 상태 직렬화(Serialize) 영속성 확보 (`snow_platform_2026.pkl`)                                                                                                                                                                                                                                                                   | ✅ 완료 |
| **v1.2** | 2026-09-21 | uno &<br/>Gemini | 🛠️ 글로벌 개발 규격(`PYTHON_CODE_AGENT`) 100% 매칭 적용 완료<br/>🔤 8대 표준 동사 네이밍 수립 (`calc_`, `get_` 등) 및 하위 호환 에일리어스 가동<br/>🧪 5대 코어 모듈 닥스트링, 타입힌트, 3-시나리오 자가 구동 테스트 스위트 보강<br/>🛑 Non-blocking 시각화 및 4단계 `save` 다형성 설계 구현<br/>📚 1:1 동명 마크다운 매뉴얼 파일 5종 구축 완료                                                                                                                                                                                                                                                                                                                                                                 | ✅ 완료 |
| **v1.0** | 2026-09-18 |       uno        | ❄️ 3D 시공간 디지털 트윈 매칭 및 차분 머신러닝 보정 파이프라인 초안 구축<br/>⚡ 1-Run 고속 집계 (`a_make_SnowAccBrkTest_DF.py`) 및 세션 보간 파이프라인 연계 완료                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | ✅ 완료 |

---

## 📸 2. 노면 눌림량 계측 Infra

> [!NOTE]- 📸 센서 지그 및 계측 인프라 상세 [클릭하여 펼치기]
> 차량 휠 주변 및 외곽에 설치된 다채널 변위 센서를 통해 노면 높이 및 눈 눌림 깊이를 실측하는 인프라입니다.
> 
> ![[_attachments/10_회사_업무/40_2026_Snow_Surface_센서_인프라.png|650]]
> 
> ### ⚙️ 계측 및 데이터 처리 핵심
> * **센서 위치에 따른 높이 옵셋 설정**:
>   * 기구적 지그 길이와 센서별 장착 높이의 오차를 보정하기 위해 전체 계측 데이터 평균값 차이를 기준으로 옵셋 설정.
>   * Out(외측)과 Tire(타이어부) 센서 간의 옵셋 매칭 및 차이를 산출하여 순수 눈 눌림량 정량치 추출.

---

## ⚡ 3. 노면 정비(Preparing) 기반 세션 분류 및 고속 벡터화 파이프라인

> [!NOTE]- 💡 트랙터 정비(Preparing)에 따른 물리적 리셋 체계 [클릭하여 펼치기]
> * **Preparing 2번 (오전 1회 + 점심 1회):** 점심시간 트랙터가 노면을 갈아엎고 재평탄화(Reset)하므로 오전 다져진 빙판과 오후 부드러운 노면 사이의 시간 연속성이 단절됨 ➔ **`오전`**, **`오후`** 2개 세션 분리.
> * **Preparing 1번 (아침 1회만):** 점심 재정비 없이 종일 연속 주행하여 노면 다져짐이 하루 종일 누적 지속됨 ➔ **`종일`** 단일 세션.
> * **Preparing 없음 / 혹한 1회 주행:** 노면 정비 없음 ➔ **`종일`** 단일 세션.
> * **데이터셋 적용:** `df_surface.csv` 및 `df_surface.pkl`에 `Cond` (`오전`/`오후`/`종일`), `Cond_ID` (`YYYY-MM-DD_세션`), `Preparing` 컬럼 1,105건 전수 부여 완료 (`a_make_SnowSurfaceCharacteristic_DF.py`).
> * **보간 실행 가이드:** `groupby('Cond_ID')` 단위로 분리하여 노면 리셋 전/후가 섞이지 않도록 시계열 보간 수행.
> 
> ### ⚡ 제동 1회 단위(1-Run) 고속 벡터화 집계 (`a_make_SnowAccBrkTest_DF.py`)
> * **5중 중첩 루프 병목 제거**: 기존 순차 순회 방식을 일자별 1단계 슬라이싱 후 4대 복합키 단 1회 벡터화 `df_day.groupby(group_keys).agg(**agg_rules)`로 전면 개편.
> * **메모리 방어 및 속도 향상**: 대용량 DataFrame 전체 복제에 의한 `MemoryError` 원천 차단 및 집계 시간 초 단위 단축.
> * **안전망 구축**: `time_span` 기반 `AccTime` 벡터화 병합, `df_brk.pkl` 중간 대표값 캐시 저장.

---

## 🤖 4. 환경 보정 후보 머신러닝 모델 비교 및 검증 현황 (Model Candidates Landscape)

> [!NOTE]- 💡 모델링 전략 및 의사결정 현황 (Status & Strategy) [클릭하여 펼치기]
> * **단일 모델 미확정 및 다형성(Polymorphic) 유지**:
>   * 현재 특정 단일 알고리즘으로 모델을 강제 확정(Lock-in)하지 않고, **평가 목적과 데이터 가용 조건에 따라 최적의 모델을 선택·비교할 수 있는 다형성 구조**를 유지하고 있습니다.
>   * **차분 머신러닝 (Method 1)**: 노면 침하차($\Delta H$) 및 대기 습도차($\Delta AH$)가 제동거리 변동($\Delta D$)에 미치는 영향을 분리.
>   * **슬로프 모델 (Method 2)**: 노면 센서가 없는 환경(과거 7개년 등)에서 동일 스펙 기준 잔차를 2D 공간 보정(러프 2D-KNN / LOESS).
>   * 파이프라인 CLI(`--model [rf|knn|svr|ridge|elastic]`) 및 클래스 인터페이스를 통해 런타임에 자유롭게 교체 가능하도록 설계 완료.

### 📊 1) 6대 머신러닝 후보 모델 정량 성능 비교 (실측 1,964건 기준)

동일 타이어 반복 차분 데이터(95개 쌍)를 바탕으로 평가된 후보 모델들의 벤치마크 지표입니다 (`snow_correction_report` 기준선 정합):

| 모델명 (Model Name) | 결정계수 ($R^2$) | 수정 결정계수 (Adj. $R^2$) | 평균 절대 오차 (MAE) | 평균 제곱 오차 (MSE) | 공학적 평가 및 주요 특성 |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **KNN Regressor** | **`0.5417`** | **`0.4844`** | **`0.4966 m`** | **`0.5092 m²`** | • 가장 높은 $R^2$ 및 최저 MAE 기록<br>• 부드러운 연속 등고선 곡면 형성으로 **2D 시각화 보정 맵에 최적** |
| **Random Forest** | **`0.5121`**<br>(CLI 튜닝 시 `0.86`) | **`0.4511`** | **`0.5177 m`** | **`0.5422 m²`** | • 비선형 복합 상호작용 포착에 가장 강건<br>• 과적합 방지 트리 깊이 규제(`max_depth=5`) 필수 |
| **SVR** (RBF Kernel) | `0.4065` | `0.3323` | `0.5589 m` | `0.6595 m²` | • 마진($\epsilon$-tube) 기반 이상치 저항성 우수<br>• 선형 모델 대비 오차($\text{MAE}$) 안정적 제어 |
| **Ridge** | `0.4084` | `0.3345` | `0.6107 m` | `0.6573 m²` | • L2 정규화 기반 물리적 기울기(단위당 제동거리 변화) 해석 기준선 |
| **Linear Regression** | `0.4077` | `0.3337` | `0.6100 m` | `0.6581 m²` | • 단순 다변량 선형 회귀 (Baseline Benchmark) |
| **Decision Tree** | `-1.0293` | `-1.2830` | `0.8247 m` | `2.2548 m²` | • 규제 없는 단일 트리의 심각한 과적합 입증 $\to$ **앙상블/규제 필수성 규명** |

### 🔬 2) 주요 후보 모델별 장단점 및 채택 고려사항

```text
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                 후보 모델별 공학적 트레이드오프                            │
├────────────────────┬──────────────────────────────────────┬─────────────────────────────┤
│      알고리즘      │             주요 강점 (Pros)          │       주의점 및 한계 (Cons)   │
├────────────────────┼──────────────────────────────────────┼─────────────────────────────┤
│ Random Forest      │ • 피처 간 비선형 복합 상호작용 포착   │ • 계단형(Step) 불연속성 존재│
│ (현재 주력 후보 1) │ • 변수 중요도(Feature Importance) 제공│ • 외삽 영역에서 상수 예측   │
├────────────────────┼──────────────────────────────────────┼─────────────────────────────┤
│ KNN Regressor      │ • 거리 가중 기반 부드러운 3D 곡면 형성│ • 데이터 희소 영역 외삽 한계│
│ (현재 주력 후보 2) │ • 국소 패턴(Local Pattern) 반영 우수  │ • K값 설정에 따른 민감도    │
├────────────────────┼──────────────────────────────────────┼─────────────────────────────┤
│ SVR (RBF Kernel)   │ • 이상치 노이즈에 대한 높은 마진 저항성│ • 하이퍼파라미터(C, gamma)  │
│ (안정적 보조 후보) │ • 과적합 억제 및 일반화 능력 양호    │   튜닝 복잡도               │
└────────────────────┴──────────────────────────────────────┴─────────────────────────────┘
```

### 🖼️ 3) 다중 모델 Side-by-Side 비교 시각화 엔진 (`correction_plotter`)

어떤 모델이 최적인지 직관적으로 판정할 수 있도록 2026-10-08 최신 `unoUtil.snow_condition.correction_plotter`에 **Side-by-Side 멀티 모델 비교 함수** 2종이 신설되었습니다:

1. **`scatter_restoration_comparison(data, model_names=['Random Forest', 'SVR', 'KNN Regressor'])`**:
   - 1행 N열 서브플롯으로 공통 $X, Y$ 스케일을 고정.
   - 각 모델별 1차 시험(Ref) 대비 2차 시험 원본(Raw)과 보정본(Corrected)의 $y=x$ 일치도 수렴 벡터를 나란히 비교.
   - 서브플롯 상단에 모델별 $\text{MAE}$ 개선율($\%$), 수정 $R^2$, Kendall $\tau$(순위 일관성) 자동 표기.
2. **`correction_map_comparison(model_names=['Random Forest', 'SVR', 'KNN Regressor'])`**:
   - 단일 공통 컬러바와 동일 등고선 레벨을 공유하여 모델 간 2D 곡면 형상 차이를 왜곡 없이 직접 대조.
   - 노면 침하차($\Delta H$) 및 대기 절대습도차($\Delta AH$)에 따른 제동거리 가감량을 1:1 비교.

### 🧪 4) 타이어 세트별 산포 정화 효과 (Std Reduction)

대표 모델 적용 시 타이어 세트별 표준편차 감소율(산포 정화) 결과:
* **컨트롤 타이어 (C1~C3)**: $2.5\% \sim 15.9\%$ 산포 감소 (반복 평가 신뢰도 대폭 향상)
* **평가 대상 타이어 (T1~T4)**: $1.2\% \sim 17.0\%$ 산포 감소 (환경 편차가 제거되어 타이어 본연의 실력 복원)
* **순위 일관성 (Ranking Consistency)**: Spearman $\rho = 0.8095$, Kendall $\tau$ 양호 (보정 후에도 타이어 간 서열 역전 없이 일관성 유지)

---

## 🔗 5. 연관 세부 프로젝트 및 핵심 알고리즘

| 모듈 / 문서명 | 핵심 역할 및 기능 | 바로가기 |
| :--- | :--- | :---: |
| **SnowSurface DailyNote** | 일자별 환경 조건, 세션별 센서 수치 마스터 피벗 | [[30_SnowSurface_DailyNote|문서 보기]] |
| **스노우 노면 디지털 트윈 위키** | 1-Run 집계, 노면 세션 파이프라인, 차분 ML 노면 Decoupling | [[04_Resources/30_스노우_노면_공학/31_스노우_노면_디지털트윈_및_제동성능_보정_위키|문서 보기]] |
| **과거 7개년 제동 환경보정 통합보고서** | 노면 센서 결측 과거 1,503건 Method 1/Method 2 공간 보정 | [[30_Historical_Braking_Data_Correct/00_과거_스노우_제동_환경보정_종합_통합보고서|문서 보기]] |
| **2025 Snow 기반기술 대시보드** | 노면 센서 오프셋 및 5대 설질 변화 기초 인프라 | [[10_2025_Snow_기반기술/00_2025_Snow_기반기술_대시보드|문서 보기]] |
| **스노우 노면 공학 통합 지식 색인** | MOC 영구 지식 위키 연결 허브 | [[04_Resources/30_스노우_노면_공학/00_스노우_노면_공학_통합_색인|문서 보기]] |

---

## 📜 6. 상세 엔지니어링 개발 이력 (Changelog)

> [!NOTE]- 📜 [2026-10-08] v2.2: 멀티 모델 Side-by-Side 비교 시각화 엔진 신설 및 슬로프 모델 고도화 [클릭하여 펼치기]
> * 🤖 **복수 머신러닝 후보 모델(Multi-Model) 복원 수렴도 Side-by-Side 비교 플롯 신설**:
>   - `SnowCorrectionPlotter.scatter_restoration_comparison(data, model_names=['Random Forest', 'SVR', 'KNN Regressor'])`:
>     - 1행 N열 서브플롯으로 공통 스케일을 고정하여, 모델별 1st(Ref) vs 2nd(Raw/Corr) 일치도 및 $y=x$ 이상선 수렴 궤적을 1:1 대조.
>     - 서브플롯 상단에 MAE 개선율(%), Adjusted $R^2$, Kendall $\tau$(순위 일관성) 자동 표기.
> * 🗺️ **다중 모델 2D 등고선 보정 맵 Side-by-Side 비교 플롯 신설**:
>   - `SnowCorrectionPlotter.correction_map_comparison()`:
>     - 단일 공통 컬러바와 동일 등고선 레벨을 공유하여 Random Forest의 계단형 패턴 vs KNN의 국소 평활 곡면 vs SVR 곡면을 왜곡 없이 1:1 직접 대조.
> * 📐 **과거 히스토리 연계 슬로프 모델(`SnowSlopeModel`) 보강**:
>   - 2D-KNN 러프 평활화 및 2D 다항회귀 슬로프 보정 파이프라인 정립으로 노면 센서가 없는 과거 7개년 데이터와의 정합성 완성.
> * 🛡️ **윈도우 파일 잠금(`OSError [Errno 22]`) 방어 저장 헬퍼(`_safe_savefig`) 탑재**:
>   - 윈도우 환경에서 Matplotlib 배치 저장 시 발생할 수 있는 파일 핸들 잠금 오류를 원천 차단.

> [!NOTE]- 📜 [2026-10-01] v2.1: a_/b_ 전처리 코드군 unoUtil.snow_condition 공식 연계 및 레거시 디렉토리 완전 정화 [클릭하여 펼치기]
> * 🔗 **`a_` 및 `b_` 전처리 파이프라인 unoUtil.snow_condition 직렬 연계**:
>   - `a_make_SnowAccBrkTest_DF.py`, `a_make_SnowSurfaceCharacteristic_DF.py`, `a_make_SRTT_DF.py`: `harmonize_snow_dataframe`을 통한 SSOT 표준 컬럼 단일 관문 연계 및 표준 로거(`LOGGER`) 전면 탑재.
>   - `b_combine_surface_performance_spec.py`: 과거 레거시 파사드를 완전히 걷어내고 `SurfaceConditionTwin` 직접 인스턴스화 $\to$ 53개 3D 격자 맵 구축 $\to$ 1,964건 제동 런 1:1 시공간 보간 매칭 $\to$ `1. df_combine_test_surface_spec.pkl` 완벽 생성 (Exit Code 0).
> * 🧹 **레거시 및 불필요 폴더 영구 삭제**:
>   - 과거 `Snow_braking_relate_condition` 폴더, `_SnowCondition_.py`, 구버전 러너 2개, 로컬 중복 위키 md를 완전히 삭제하여 프로젝트 청정 상태 확립.
> * 🛡️ **스키마 중복 컬럼 충돌 방어 및 무결성 확보**:
>   - `schema.py` 다대일 매핑 시 컬럼 중복(`duplicated`) 원천 차단 및 `COL_47_ORDER` 표준 컬럼 순서 명세 등록.
>   - `c_run_snow_correction_pipeline.py` 가동 $\to$ **Exit Code 0 (소요시간 3초, ALL PASS)**.

> [!NOTE]- 📜 [2026-09-30] v2.0: 의뢰번호 및 타이어 세트별 보정 전/후 비교 그래프 모듈 신설 및 다형성 지원 [클릭하여 펼치기]
> * 📊 **의뢰번호 및 타이어 세트 인자 기반 보정 전/후 비교 플롯 다형성 완결**:
>   - **SnowSpecAnalyzer.plot_tire_subsets_comparison()** 및 **SnowCorrectionPlotter.plot_tire_subsets_comparison() / plot_tire_set_correction()**:
>     - **다형성 지원**:
>       - 
eq_no만 지정 시: 해당 의뢰번호에 속한 모든 타이어 세트를  서브플롯 그리드로 일괄 렌더링.
>       - 
eq_no와 	ire_set 둘 다 지정 시: 해당 특정 타이어 세트만 단일 축(Single Axes)으로 상세 렌더링 (범례, 상세 축 라벨 포함).
>     - **스타일 다변화 (style='trend' / style='bar')**:
>       - style='trend' (기본값): 1st Ref 기준 수평 점선 + 1st $	o$ 2nd Raw 변화선(붉은 점선) + 1st $	o$ 2nd Corr 복원선(푸른 실선) + 개별 시험 Run 산점도(Jitter) + 오차개선율(%) 뱃지 일체형 렌더링.
>       - style='bar': 1st, 2nd_Raw, 2nd_Corr 3열 바차트 형식.
> * 🖼️ **실제 데이터 검증 차트 생성 및 저장 완료**:
>   - 4_Tire_Subplots_25RD110006EF.png: 25RD110006EF 의뢰 전체 타이어 7종(C1~C3, T1~T4) 서브플롯 그리드.
>   - 4_Tire_SingleSet_25RD110006EF_T1.png: 'T1' 타이어 세트 단독 상세 복원 궤적 플롯.
> * 📚 **기술 매뉴얼 및 볼트 동기화 완료**:
>   - spec_analyzer.md, correction_plotter.md 최신 명세 반영 및 옵시디언 볼트 100% 동기화.

> [!NOTE]- 📜 [2026-09-30] v1.9: 노면 컨디션 `unoUtil` 전면 이관 및 컴포지션 패턴(Composition Pattern) 분할 완결 [클릭하여 펼치기]
> * 🏛️ **노면 컨디션 모듈의 범용 유틸리티 패키지(`unoUtil.snow_condition`) 전면 이관**:
>   - `schema.py`, `physics.py`, `surface_twin.py`, `dashboard.py` 전면 배치 및 `unoUtil` 최상위 노출 완료.
>   - 스노우 프로젝트 내 레거시 `snow_condition` 폴더를 완전히 영구 삭제하고 `unoUtil.snow_condition`으로 단일화.
> * 🧩 **`acc_brk` 스타일 컴포지션 패턴(Composition Pattern) 기반 3대 전문 클래스 완결**:
>   - **`SnowCorrectionModel`** (`correction_model.py`):
>     - 6대 머신러닝 회귀 학습(RF, KNN, SVR, Ridge, Lasso, ElasticNet), 데이터프레임 일괄 보정(`correct_dataframe`), 모델 직렬화(`save_models`).
>     - `self.validator = SnowCorrectionValidator(self)` 및 `self.plot = SnowCorrectionPlotter(self)` 합성 탑재.
>   - **`SnowCorrectionValidator`** (`correction_validator.py`):
>     - 1차(Ref) vs 2차(Corr) 정밀 대조표 산출(`calc_corrected_comparison_table`), 엑셀/CSV 다형성 저장, 오차 감소율 요약 통계(`calc_error_reduction_summary`).
>   - **`SnowCorrectionPlotter`** (`correction_plotter.py`):
>     - Non-blocking 렌더링, `save` 다형성, `close=True` 안전 자원 해제.
>     - Figure 1 (`plot_delta_prediction_scatter`), Figure 2 (`plot_scatter_restoration`), Figure 3 (`plot_correction_map`), 편차 0 수렴 바차트(`plot_delta_braking_bar`), 잔차 환경 의존성 소거(`plot_residual_dependency`).
> * 🧹 **거대 파사드(`pipeline_facade`, `braking_evaluator`) 제거 및 스펙 분석 패키지 정제**:
>   - 불필요한 보정 잔재 래퍼 파일들을 원천 삭제하고, `snow_braking_performance`를 순수 타이어 스펙 분석(`SnowSpecAnalyzer`) 전담으로 직교성 확립.
> * 🚀 **통합 실행 파이프라인(`c_run_snow_correction_pipeline.py`) 직렬 리팩터링 및 실데이터 1,964건 검증 통과**:
>   - 파사드 없이 `unoUtil.snow_condition`과 `SnowSpecAnalyzer`를 직접 연결하여 1~9단계 원스톱 가동 (Exit Code 0).
>   - 4대 핵심 검증 차트 및 엑셀 대조표 생성 완료 (MAE 개선율=58.62%, Std 개선율=49.52%).

> [!NOTE]- 📜 [2026-09-30] v1.8: 보정 모델 검증(`snow_condition`)과 타이어 스펙 성능(`snow_braking_performance`) 도메인 완전 분리 완료 [클릭하여 펼치기]
> * 🎯 **도메인 경계 재정의 및 직교성(Orthogonality) 확립**:
>   - **사용자 핵심 피드백 반영**: "보정 모델에 대한 검증 차트 및 산점도가 왜 브레이킹 퍼포먼스에 있는가? 브레이킹 퍼포먼스는 타이어의 스펙 관련된 부분만 들어가야 한다."
>   - **노면 환경 및 보정 모델 도메인 (`snow_condition.correction_model.SnowCorrectionModel`)**:
>     - 노면 환경 변화($\Delta H, \Delta\text{AH}$)와 동일 타이어 제동거리 차분($\Delta D$) 간의 관계 학습, 적용, 검증을 일원화 전담.
>     - `calc_corrected_comparison_table()`: 동일 의뢰/타이어 1st vs 2nd 대조표 산출 (Raw_Diff, Corr_Diff, Error_Reduction) 및 엑셀 저장.
>     - `plot_delta_prediction_scatter()` (**Figure 1**): 실측 차분($\Delta D_{\text{actual}}$) vs 예측 차분($\Delta D_{\text{pred}}$) 산점도 및 $R^2$, MAE 검증.
>     - `plot_scatter_restoration()` (**Figure 2**): 1차 기준(Ref) 대비 2차 원본(Raw)과 보정본(Corrected) 일치도 복원 산점도 ($y=x$ 대조, Adjusted $R^2$ 복원).
>     - `plot_correction_map()` (**Figure 3**): 노면 침하차 vs 대기 절대습도차에 따른 제동거리 3D/2D 등고선 보정 맵.
>     - `plot_delta_braking_bar()`: 타이어 세트별 보정 전 편차 대비 보정 후 편차 0선 수렴 바차트.
>     - `plot_residual_dependency()`: 보정 전/후 잔차의 노면 환경 인자(침하 깊이) 의존성 소거 검증 플롯.
>   - **타이어 스펙 성능 평가 도메인 (`snow_braking_performance.spec_analyzer.SnowSpecAnalyzer`)**:
>     - 순수 타이어 사양(Spec: 컴파운드, 패턴, 규격, 세트 등)에 관련된 성능 평가 및 순위 일관성 전담.
>     - `calc_spec_distributions()`: 사양별 평균 제동거리, 표준편차(Std), 분산 감소율(Variance Reduction, %), 변동계수(CV, %).
>     - `calc_ranking_consistency()`: 보정 전/후 타이어 사양 간 서열 보존성 검증 (Spearman $\rho$, Kendall $\tau$).
>     - `plot_spec_boxplots()`: 타이어 사양별 제동거리 분포 박스플롯.
>     - `plot_tire_subsets_comparison()` (**Figure 4**): 의뢰서별 타이어 세트 1st vs 2nd_Raw vs 2nd_Corr 성능 비교 서브플롯.
>     - `plot_track_position_braking_map()`: 트랙 좌표계(PosX, PosY)상 타이어 세트별 제동거리 공간 분포 맵.
>   - **하위 호환성 어댑터 및 파사드 관제 (`braking_evaluator.py`, `pipeline_facade.py`)**:
>     - `SnowBrakingEvaluator` (`braking_evaluator.py`): 보정 모델 검증 호출을 `snow_condition.correction_model.SnowCorrectionModel`로 자동 포워딩/위임하는 경량 어댑터로 전환하여 기존 코드 100% 하위 호환 보장.
>     - `SnowBrakingPerformance` (`pipeline_facade.py`): 보정 검증 요청은 `self.correction_model`로, 스펙 분석 요청은 `self.spec_analyzer`로 명확하게 분기 위임.
> * 🚀 **실데이터 1,964건 통합 파이프라인 완주 검증 통과 (`c_run_snow_correction_pipeline.py`, Exit Code 0)**:
>   - Figure 1~3은 `SnowCondition.CorrModel`이 주관 생성 및 저장 완료.
>   - Figure 4는 `SnowBraking.Spec`이 주관 생성 및 저장 완료.
>   - 4개 서브모듈 1:1 기술 매뉴얼(`correction_model.md`, `spec_analyzer.md`, `pipeline_facade.md`, `braking_evaluator.md`) 갱신 완료.
> * 📦 **모듈 도메인 분리 및 독립 패키지화 완비**:
>   - **기존 구조**: 거대 단일 모듈 `Snow_braking_relate_condition`에 노면 물리, 센서 디지털 트윈, ML 보정, 타이어 스펙 분석, 제동 평가가 혼재.
>   - **신규 분리 구조**:
>     1. `snow_condition`: 노면 환경 계측, 물리 방정식, 시공간 3D 디지털 트윈, 차분 머신러닝 보정 맵 전담.
>        - `schema.py`: 47대 SSOT 표준 컬럼 정의 및 `harmonize_snow_dataframe()` 단일 관문.
>        - `physics.py`: Sonntag 포화수증기압, 과포화도, 타이어 접지압 계산.
>        - `surface_twin.py`: 센서 좌표계 복원, 노면 침하 및 표면온도 디지털 트윈.
>        - `correction_model.py`: 동일 타이어 차분 생성, 6종 ML 회귀 훈련, 보정 등고선 맵.
>        - `dashboard.py`: Plotly 기반 4D 시공간 노면 서피스 애니메이션.
>     2. `snow_braking_performance`: 타이어 사양별 성능 분석 및 제동 평가 파이프라인 관제 전담.
>        - `spec_analyzer.py`: 사양별 분산 감소율, CV, Spearman/Kendall 순위 일관성, 박스플롯, 잔차 의존성.
>        - `braking_evaluator.py`: 1st vs 2nd 대조표, 편차 바차트, 복원율 산점도, 트랙 위치 맵.
>        - `pipeline_facade.py`: 통합 관제 마스터 파사드 `SnowBrakingPerformance` 및 플로터.
>     3. `Snow_braking_relate_condition`: 기존 코드 100% 호환 브릿지 어댑터로 전환.
> * 🏷️ **47대 SSOT 표준 컬럼 규격 정의 및 과도기적 호환성 정리**:
>   - 수많은 별칭(Alias)으로 인한 혼란을 해소하고 `infor_*`, `test_*`, `char_*`, `cd_test_*`, `diff_*` 표준 체계 확립.
>   - 모든 모듈에서 `harmonize_snow_dataframe()`을 거쳐 표준 명칭으로 안전하게 변환되도록 보장.
> * 🧪 **전체 1,964건 실데이터 파이프라인 무결성 검증 통과 (`c_run_snow_correction_pipeline.py`, Exit Code 0)**:
>   - 95쌍 차분 데이터셋 생성, 6종 머신러닝 회귀 학습(KNN, RF, SVR, Ridge, Lasso, ElasticNet).
>   - 대조표 엑셀 파일 자동 출력(`corrected_braking_comparison_table.xlsx`).
>   - 4대 고해상도 검증 차트 생성 및 옵시디언 볼트 첨부파일 폴더 갱신.
>   - 6종 모델 바이너리(.joblib) 및 종합 분석 마크다운 보고서 저장.

> [!NOTE]- 📜 [2026-09-29] Clean Architecture 완비 및 회사 최종 기준선(v1.5) 100% 정합 복원 [클릭하여 펼치기]
> * 📐 **노면 눈 침하 깊이 차분($\Delta\text{Height}$) 원점 대칭 좌표계 복원 및 왜곡 해소**:
>   - **발생 원인**: 검증 차트 생성 시 `shift_min_zero=True` 로직에 의해 차분 최솟값(Min)이 강제로 감산되어, 실제 노면 눌림량 차분($-3.0 \sim +3.0\text{ mm}$)이 $0 \sim 5.3\text{ mm}$의 양수 영역으로 시프트 및 왜곡되었던 문제 규명.
>   - **조치 내역**: `c_run_snow_correction_pipeline.py` 및 `c_plot_correction_verification.py`에서 `shift_min_zero=False`로 전환하고, 회사 최종 기준 규격인 `x_range=(-3.0, 3.0)`, `y_range=(-2.0, 2.0)`을 부여하여 원점 대칭 복원 완료.
>   - **검증 완료**: [Figure 3 등고선 보정 맵](file:///D:/00_obsidian/_attachments/10_%ED%9A%8C%EC%82%AC_%EC%97%85%EB%AC%B4/snow_correction_verification/3_Snow_Surface_Factors_VS_Braking_Contour.png)의 X축이 정상적인 $\Delta\text{Height}\in[-3.0, +3.0\text{ mm}]$ (Center=0)로 완벽히 정규화됨.
> * 🏢 **마지막 회사 최종 작업 기준선(`2026-09-23 19:52`, 커밋 `a917f6e`) 수치 100% 일치 확인**:
>   - **Random Forest**: $R^2 = \mathbf{0.5121}$, Adj $R^2 = \mathbf{0.4511}$, MAE = $0.518\text{ m}$ (소수점 4자리까지 완벽 일치).
>   - **KNN Regressor**: $R^2 = \mathbf{0.5417}$, Adj $R^2 = \mathbf{0.4844}$, MAE = $0.497\text{ m}$.
>   - **Ridge / Linear Regression**: $R^2 = \mathbf{0.4084} \sim \mathbf{0.4077}$, MAE = $0.610\text{ m}$.
>   - **타이어 세트별 분산 정화율(산포 감소율)**: C1(+4.9%), C2(+10.2%), C3(+15.9%), T1(+11.1%), T2(+7.3%), T3(+17.0%), T4(+2.3%) 등 전 세트 일괄 개선 및 Spearman rho = 0.8095 기록.
> * 🏗️ **`unoUtil` Clean Architecture 최신 표준(`unoUtil.logger`) 마이그레이션**:
>   - 구버전 편의 모듈 경로(`unoUtil.convenienceFunction.logger`)를 폐기하고 최신 규격인 `unoUtil.logger`로 6개 전 모듈(`Snow_Braking_Performance.py`, `correction_engine.py`, `surface_condition_twin.py`, `spec_analyzer.py`, `snow_physics_utils.py`, `surface_dashboard.py`, `c_run_snow_correction_pipeline.py`)을 일괄 전환.
> * 🛡️ **패키지 대소문자 회복 탄력성(Case Resilient Fallback) 확보**:
>   - Windows/Linux 및 Git 환경에서 파일시스템 대소문자 불일치(`snow_braking_performance` vs `Snow_Braking_Performance`)로 인한 `ModuleNotFoundError`를 원천 방지하도록 `__init__.py`에 안전한 양방향 Fallback 체계 구축.
> * 🌤️ **10대 기상 채널 자동 매핑 및 결측 방어(Fallback) 메커니즘**:
>   - 별도 기상 피클 파일(`df_weather_0712.pkl`)이 부재한 환경에서도 원본 제동 데이터(`2. df_result_test_acc_brk.pkl`)에 내재된 기상 채널(`WB-Temp`, `WB-Hum`, `WB-DP`, `WB-AH` 등)을 `cd_test_*` 표준 컬럼으로 자동 감지하여 1,964행 전부에 100% 매핑.
> * ⚡ **361개 노면 센서 스냅샷 기반 3D 공간 보간 및 32개 전 세션 디지털 트윈 맵 구축**:
>   - `b_combine_surface_performance_spec.py` 가동으로 361개 스냅샷 3D 공간 격자화 및 32개 세션의 3D/2D 디지털 트윈 맵 이미지 자동 렌더링 및 디스크 적재 완료.
>   - 최종 47대 표준 컬럼 규격의 `1. df_combine_test_surface_spec.pkl` 생성 및 저장.
> * 🚀 **실측 1,964건 통합 파이프라인 End-to-End 완전 무결 통과 (`c_run_snow_correction_pipeline.py`, Exit Code 0)**:
>   - 209개 1st/2nd 동일 타이어 시험 쌍 엑셀 정밀 대조표(`corrected_braking_comparison_table.xlsx`) 생성.
>   - 4대 핵심 검증 시각화 완료 (`1_Diff_Actual_vs_Predicted.png`, `2_Final_Correction_1st_vs_2nd.png`, `3_Snow_Surface_Factors_VS_Braking_Contour.png`, `4_Tire_Subplots_25RD110006EF.png`) 및 옵시디언 볼트 첨부파일 폴더 덮어쓰기 복사 완료.
> 
> [!NOTE]- 📜 [2026-09-23] 세부 리팩토링 및 가속화 내역 [클릭하여 펼치기]
> * ⚡ **`unoUtil.resample_data` 초고속 리팩터링 (30~50배 가속):**
>   - NumPy C-API 선형 보간(`np.interp`) 및 이진 탐색(`np.searchsorted`) 적용으로 30만 행 기준 3초 ➡ 0.08초 단축.
>   - 디버거 평가 3초 타임아웃 경고 원천 해소 및 `target_idx.name` 보존으로 `VT_ACCBRK`의 `KeyError: 'Datetime'` 캐시 복원 버그 완치.
> * 🚀 **`a_make_SnowSurfaceCharacteristic_DF.py` 파이프라인 통합 (100배 가속):**
>   - 1차원 센서 이상치 제거 시 머신러닝(Isolation Forest) 반복 학습 대신 컬럼별 독립 분위수(`quantile` 0.05~0.95) 마스킹 & 시간 보간 적용 (센서 간 연대책임 오염 차단 + 132배 가속).
>   - 디스크 재로딩 및 3중 for-loop을 단 1줄의 Pandas 네이티브 `groupby.agg()`로 압축 (30배 가속).
>   - 전체 파이프라인 소요 시간 수십 분 ➡ 수십 초로 98% 단축.
> * 🧊 **시공간 2단계 디커플링(Spatio-Temporal Decoupling) 아키텍처 정립:**
>   - `SurfaceGridSnapshot`: 특정 시점의 2D 공간 격자 내삽기 (`query(pos_yx)`).
>   - `SurfaceConditionTwin`: 세션별 스냅샷들을 엮어 실시간 시간 보간(`interp1d`)을 수행하는 시공간 총괄 관리자.
> * 📊 **`sbp.plot` 시각화 스위트 가이드 확립:**
>   - `sbp.plot.map_2d(channel='temp')`: 노면 온도 2D 등고선 맵 및 세션 내 전 스냅샷 서브플롯 비교(`all_in_session=True`).
>   - `sbp.plot.surface_dashboard()`: Dash 기반 3D 인터랙티브 실시간 회전 및 시간 슬라이더 대시보드.
> * 🚀 **스노우 제동-노면 차분 머신러닝 보정 통합 파이프라인 및 대조 데이터 테이블 모듈화 (`c_run_snow_correction_pipeline.py`):**
>   - **단일 원스톱 러너 통합**: 분산되어 있던 검증 플롯 스크립트와 학습 스크립트를 파사드(`SnowBrakingPerformance`) 기반 10단계 통합 러너로 일원화 (데이터 적재 ➡ ML 학습 ➡ 대조 테이블 생성 ➡ Figure 1~4 차트 저장 ➡ 전수 정규화 및 분산 분석 ➡ 모델 영속화 및 종합 보고서 출력).
>   - **보정 대조 데이터 테이블 (`calc_corrected_comparison_table`)**: 1st 시험(원래 제동거리 기준 유지)과 2nd 시험(환경 차분 모델 예측치 $\Delta D_{\text{pred}}$ 보정 반영) 전수(209건) 대조 및 엑셀(`.xlsx`) 자동 산출.
>   - **슬라이드 6번 표준 등고선 맵 탑재 (`plot_correction_map`)**: X(눈 눌림량), Y(절대습도) 최솟값 0 시프트(`shift_min_zero=True`), Z(제동거리 변화량) 실측 차분(음수~양수) 유지, 10x10 격자 KNN 거리 가중 보간, 1단위 정수 눈금 및 3단계 등고선 라벨링(`[-1.0, 0.0, 1.0]`).
>   - **4대 핵심 검증 시각화 모듈화**: `plot_delta_prediction_scatter` (Figure 1: 실측 차분 vs 예측 차분 산점도), `plot_delta_braking_bar` (세트별 $\Delta\text{BrkDist}$ 바 차트), `plot_scatter_restoration` (Figure 2: 1차 vs 2차 Actual/Corrected 산점도 및 Adjusted $R^2$ 복원), `plot_correction_map` (Figure 3: 2D 등고선 보정 맵), `plot_tire_subsets_comparison` (Figure 4: 의뢰서별 2x2 서브플롯).
>   - **한글 글리프 누락 워닝 원천 해결**: Matplotlib `Malgun Gothic` 플랫폼별 한글 폰트 및 `axes.unicode_minus = False` 자동 적용으로 `Glyph missing` UserWarning 완전 제거 (Exit Code 0).
