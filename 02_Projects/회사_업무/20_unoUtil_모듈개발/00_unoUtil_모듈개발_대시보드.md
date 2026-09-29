---
id: "unoutil_project_hub"
title: "unoUtil 사내 파이썬 통합 프레임워크 개발 프로젝트"
type: project
category_main: 회사_업무
category_sub: unoUtil
date: 2026-09-10
status: 진행중
tags:
  - 회사_업무
  - unoUtil
  - 파이썬
  - 개발도구
  - 대시보드
  - MOC
  - 아키텍처
  - 코딩표준
aliases:
  - unoUtil_모듈개발_대시보드
  - unoUtil개발허브
  - unoUtil_아키텍처_및_표준가이드
  - 00_unoUtil_PEP8_표준화_총괄_가이드
  - UNOUTIL_ARCHITECTURE
  - UNOUTIL_V2_REFACTORING_REPORT
  - 01_test_data_통합관리_계획서
  - "00_file_reader_대시보드"
  - "00_graphics_대시보드"
  - "00_models_대시보드"
  - "00_post_process_대시보드"
  - "00_utils_대시보드"
  - "00_vehicle_dynamic_대시보드"
  - "00_vt_acc_brk_대시보드"
  - "file_reader_대시보드"
  - "graphics_대시보드"
  - "models_대시보드"
  - "post_process_대시보드"
  - "utils_대시보드"
  - "vehicle_dynamic_대시보드"
  - "vt_acc_brk_대시보드"
---

# 💼 unoUtil 사내 파이썬 통합 프레임워크 개발 프로젝트 (Master MOC)

> ⚡ **Quick Jump**: [📅 1. 체인지로그](#-1-프로젝트-주요-버전-이력-changelog-타임테이블) · [🏛️ 2. 아키텍처](#️-2-clean-architecture-10대-도메인-아키텍처) · [🏎️ 3. vehicle/acc_brk](#️-3-vehicle-동역학--가감속제동-vt_acc_brk-도메인) · [🚀 4. file_reader](#-4-file_reader-이기종-계측-데이터-리더-도메인) · [🎨 5. graphics](#-5-graphics-실차-시각화-및-인터랙션-도메인) · [📐 6. models](#-6-models-공학-모델링-및-비선형-최적화-도메인) · [📶 7. signal_process](#-7-signal_process-신호-후처리-및-정제-도메인) · [🛠️ 8. utils/logger](#️-8-utils--logger-공통-유틸리티-도메인) · [🤖 9. ai/db/stats/gps](#-9-aidatabasestatisticsgps-기타-도메인) · [📖 10. 엔지니어링 표준](#-10-사용자-매뉴얼-및-엔지니어링-표준)

> [!ABSTRACT] 🚀 unoUtil 단일 마스터 MOC 허브
> 사내 파이썬 실차 데이터 분석 프레임워크 **`unoUtil v2.0+`**의 10대 도메인, 87개 핵심 모듈 기술 매뉴얼, Clean Architecture 명세 및 버전 관리 이력을 단일 페이지에서 1화면으로 조망·관리하는 **중앙 마스터 MOC 포털**입니다.

---

## 📅 1. 프로젝트 주요 버전 이력 (Changelog 타임테이블)

> [!NOTE]- 📜 v1.0 ~ v3.4 주요 개발 및 리팩토링 이력 [클릭하여 펼치기]
> | 버전 | 날짜 | 작업자 | 핵심 수정 및 개발 내역 (Changelog) | 상태 |
> | :---: | :---: | :---: | :--- | :---: |
> | **v3.4** | 2026-09-29 | uno &<br/>Gemini | 🎯 **curve_fit 최상위 도메인 승격, tire_curve 패키지 완전 일원화 및 단일 마스터 MOC 정비**<br/>• **curve_fit 최상위 도메인 신설**: `unoUtil.curve_fit` 도메인 및 `tire_curve/` 전용 패키지 구축<br/>• **타이어 피팅 단일 모듈화**: `CurveCombiner`, `fit_mf_ax`, `estimatorMF`, `MinimizeEstimator` 등 분산 피팅을 **`TireCurve` 단 하나의 타이어 피팅 모듈**로 완전 흡수 통합<br/>• **57KB 스플라인 결합 파이프라인 수납**: `curve_combiner/` 복합 파이프라인의 내부 캡슐화 및 OCP 미래 확장 구조 완비<br/>• **models(수식)와 curve_fit(피팅) 역할 분리**: `models`는 순수 지배 방정식 SSOT, `curve_fit`은 데이터 피팅 전담<br/>• **12대 도메인 및 36개 레거시 경로 100% 무결성 검증 통과 (Exit 0)** | ✅ 완료 |
> | **v3.3** | 2026-09-28 | uno &<br/>Gemini | 🎯 **TireCurve 전략 패턴 및 BicycleModel 전면 표준화 완결 (Exit 0)**<br/>• **TireCurve 구축**: 임의 수학 모델(`model`) 및 최적화 전략(`method`) 주입 가능한 전략 패턴(Strategy Pattern) 기반 단일 클래스 설계<br/>• **2-DoF 자전거 모델 정합**: `dynamic_formula` ➔ `bicycle_model.py`(`BicycleModel`) 자동차공학 국제 표준 정규화<br/>• **Pacejka MF SSOT 확립**: 도메인별 분산 수식을 `calc_magic_formula` 단일 코어로 일원화<br/>• **무결성 검증 100% 통과**: 11대 공식 도메인 패키지 & 36개 구버전 레거시 가상 리다이렉션 전원 통과 | ✅ 완료 |
> | **v2.9** | 2026-09-26 | uno &<br/>Gemini | 🏎️ **unoUtil.vehicle 도메인 v2 전면 표준화 및 Single Baseline Law 확립**<br/>• `vehicle_dynamic.py`를 `VehicleDynamic` 단일 표준 클래스로 캡슐화 완료 (8대 표준 동사 정합, v1 호환 별칭 바인딩, 비차단 시각화 및 자가 구동 테스트 스위트 구축)<br/>• `hndl_test.py`, `test_infor_res.py`, `analysis_test_data.py` 전면 리팩토링 및 1:1 위키 매뉴얼 100% 달성 | ✅ 완료 |
> | **v2.8** | 2026-09-24 | uno &<br/>Gemini | 🏁 **unoUtil v2.0 아키텍처 전면 완료 및 전수 무결성 검증 100% 통과 (Final)**<br/>🛡️ 사내 보안 정책(AppLocker) 및 Windows 11 Smart App Control 대응: `D:\uno\Python\envs\unoBase` 표준 환경 구축 및 C/Fortran 확장 DLL 로드 차단 완벽 해소<br/>🧪 전사 10대 도메인 & 36개 세부 레거시 경로 무결성 100% 통과 (`test_structure_integrity.py` Exit 0 달성) | ✅ 완료 |
> | **v2.7** | 2026-09-23 | uno &<br/>Gemini | 🧹 **전사 역방향 별칭(`Standard = LEGACY`) 전수 제거 및 정방향(`LEGACY = Standard`) 일괄 정합화**<br/>🛡️ 물리 `legacy/` 9개 디렉터리 및 `convenienceFunction/` 전량 `_archive/` 영구 퇴출 (Zero Physical Legacy 달성) | ✅ 완료 |
> | **v2.6** | 2026-09-23 | uno &<br/>Gemini | 🗄️ **GetDB 실차시험 스펙 및 결과 통합 엔진 신규 구축**<br/>• `_func_connect_spec_with_req_set.py` 및 `_func_connect_vehicle_test_and_spec.py` 구현, SSL 인증서 패치 적용 | ✅ 완료 |
> | **v2.0** | 2026-09-18 | uno &<br/>Gemini | 🏎️ **unoUtil v2.0 Clean Architecture 10대 도메인 설계 전면 전환**<br/>📦 패키지 다이어트: 1GB+ 거대 계측 데이터 전량 분리 $\rightarrow$ 루트 `test_data/` 중앙 통합 (15.62MB 순수 파이썬 초경량화, 98.5% 절감)<br/>🎯 8대 표준 동사 네이밍 수립 및 `MetaPathFinder` 무중단 가상 로더 수립 | ✅ 완료 |
> | **v1.0** | 2026-09-10 | uno | 🚀 unoUtil 사내 파이썬 통합 프레임워크 개발 프로젝트 킥오프 | ✅ 완료 |

---

## 🏛️ 2. Clean Architecture 10대 도메인 아키텍처

> [!NOTE]- 🏗️ 아키텍처 다이어그램 및 패키지 구조 [클릭하여 펼치기]
> ```mermaid
> flowchart TD
>     subgraph Storage_Isolation [프로젝트 최상위 3대 기둥 분리]
>         P_CODE["🚀 unoUtil/ (순수 파이썬 프레임워크 - 초경량화)"]
>         T_DATA["⭐ test_data/ (단일 중앙 테스트 데이터 - 90% 다이어트)"]
>         ARCH["🗄️ _archive/ (과거 코드 영구 보존소 - 탐색기 열람)"]
>     end
> 
>     subgraph Core_Domains [unoUtil 11대 핵심 도메인]
>         V["🏎️ vehicle/ (실차 시험 & 동역학)"]
>         G["🛰️ gps/ (GNSS 좌표계 투영 - gps_to_xy.py 단일화)"]
>         FR["🚀 file_reader/ (이종 계측데이터 통합 리더 + parsers/ 서브폴더)"]
>         CF["🎯 curve_fit/ (타이어 비선형 피팅 tire_curve/ SSOT)"]
>         M["📐 models/ (Pacejka MF, Bicycle Model 지배 수식 SSOT)"]
>         SP["📈 signal_process/ (fft, post_process 4대 전처리)"]
>         ST["📊 uno_statistics/ (순수 통계 & 측정불확도 uncertainty/)"]
>         GR["🎨 graphics/ (시각화 3대 서브폴더: plotters, controls, web)"]
>         UT["🛠️ utils/ (공통 유틸리티 통합 & logger/ 완성)"]
>         AI["🤖 ai/ (최적화 모델 & 피팅)"]
>         DB["🗄️ database/ (DW / PLM 연동)"]
>     end
> ```

---

## 🏎️ 3. vehicle 동역학 & 가감속/제동 (VT_ACCBRK) 도메인

> [!NOTE]- 🏎️ vehicle 및 acc_brk 모듈 1:1 매뉴얼 목록 [클릭하여 펼치기]
> | 모듈 / 서브패키지 | 핵심 기능 및 역할 | 1:1 기술 매뉴얼 링크 |
> | :--- | :--- | :---: |
> | **`VehicleDynamic`** | 실차 센서 장착점 ➔ 차량 무게중심(CG) 운동역학 변환 및 롤/피치 보정 | [[vehicle_dynamic\|매뉴얼 보기]] |
> | **`hndl_test`** | 실차 조종안정성(Handling) 계측 데이터 분석 및 요레이트/횡가속도 산출 | [[hndl_test\|매뉴얼 보기]] |
> | **`test_infor_res`** | 평가 정보(`TestInformation`) 및 결과(`TestResult`) 메타데이터 컨테이너 | [[test_infor_res\|매뉴얼 보기]] |
> | **`analysis_test_data`**| 제동 및 가속 성능 종합 통계 분석 및 평가 간 비교 엔진 | [[analysis_test_data\|매뉴얼 보기]] |
> | **`vt_acc_brk`** | 가감속/제동 자동화 파이프라인 마스터 오케스트레이터 | [[vt_acc_brk\|매뉴얼 보기]] |
> | **`vt_acc_brk_tire`** | 단일 타이어 동역학 분석, Wavelet 가속도 복원, 구간 자동 탐지 | [[vt_acc_brk_tire\|매뉴얼 보기]] |
> | **`vt_acc_brk_project`**| 다중 타이어 취합, 콘트롤 타이어 시계열 선형 보간 엔진 | [[vt_acc_brk_project\|매뉴얼 보기]] |
> | **`correct` / `correct_factors`** | 시험 환경(온도, 노면) 및 콘트롤 타이어 시계열 성능 지수 보정 | [[correct\|correct]] · [[correct_factors\|correct_factors]] |
> | **`base_memory`** | 대용량 실차 시계열 데이터 초고속 인메모리 관리 및 슬림 피클링 | [[base_memory\|매뉴얼 보기]] |
> | **`func_acc_brk`** | 제동 분석 전용 시계열 필터링, 데이터 슬라이싱 보조 함수군 | [[func_acc_brk\|매뉴얼 보기]] |
> | **`analyzers` (6대 서브)**| 가속대역, 감속응답, 슬립속도PDF, Mu-Drop, 왜도, 구간속도분할 전문 분석기 | [[an_acceleration\|가속]] · [[an_response\|응답]] · [[an_slip_pdf\|슬립PDF]] · [[an_mu_drop\|MuDrop]] · [[an_skewness\|왜도]] · [[an_split_speed\|속도분할]] |
> | **`plotter_tire` / `plotter_project`** | 단일 타이어 분석 차트 및 프로젝트 비교 시계열 플로터 | [[plotter_tire\|타이어플로터]] · [[plotter_project\|프로젝트플로터]] |

---

## 🚀 4. file_reader 이기종 계측 데이터 리더 도메인

> [!NOTE]- 🚀 file_reader 파서 및 리더 모듈 목록 [클릭하여 펼치기]
> | 모듈 / 서브패키지 | 핵심 기능 및 역할 | 1:1 기술 매뉴얼 링크 |
> | :--- | :--- | :---: |
> | **`file_data_reader`** | VBox(`.vbo`), Dewesoft(`.dwd`), RaceLogic(`.vbb`), 텍스트 이기종 자동 판별 통합 리더 | [[file_data_reader\|매뉴얼 보기]] |
> | **`parsers` (5대 서브)** | `base_parser`, `vbo_parser`, `vbb_parser`, `dwd_parser`, `text_parser` 전용 엔진 | [[base_parser\|기반]] · [[vbo_parser\|VBO]] · [[vbb_parser\|VBB]] · [[dwd_parser\|DWD]] · [[text_parser\|TEXT]] |
> | **`datetime_helper`** | GPS 시각 동기화, UTC-KST 변환 및 시계열 타임스탬프 정규화 | [[datetime_helper\|매뉴얼 보기]] |
> | **`standard_channel_pattern`** | 사내 계측 채널명 정규표현식 매핑 사전 및 표준 칼럼 변환 | [[standard_channel_pattern\|매뉴얼 보기]] |
> | **`DWDataReader` / `vbbTopython`** | Dewesoft C-DLL 바인딩 및 VBB 바이너리 파이썬 변환 엔진 | [[dwdReader\|dwdReader]] · [[VBBReader\|VBBReader]] |

---

## 🎨 5. graphics 실차 시각화 및 인터랙션 도메인

> [!NOTE]- 🎨 graphics 플로터, 컨트롤러, 웹 시각화 모듈 목록 [클릭하여 펼치기]
> | 모듈 / 서브패키지 | 핵심 기능 및 역할 | 1:1 기술 매뉴얼 링크 |
> | :--- | :--- | :---: |
> | **`plotter`** | Matplotlib 기반 실차 주행 시계열 표준 플로팅 엔진 (비차단 원칙) | [[plotter\|매뉴얼 보기]] |
> | **`pair_plot`** | 다변량 센서 신호 상관관계 매트릭스 시각화 | [[pair_plot\|매뉴얼 보기]] |
> | **`surface_3d`** | 노면 높이 및 3차원 공간 특성 서피스 렌더러 | [[surface_3d\|매뉴얼 보기]] |
> | **`text_offset`** | 차트 주석 텍스트 겹침 방지 자동 오프셋 계산기 | [[text_offset\|매뉴얼 보기]] |
> | **`cursor_mode` / `range_selector`** | GUI 인터랙티브 마우스 커서 측정 및 특정 구간 드래그 선택기 | [[cursor_mode\|커서]] · [[range_selector\|구간선택]] |
> | **`plotly_tools`** | 웹 기반 반응형 Plotly 대화형 차트 생성 툴킷 | [[plotly_tools\|매뉴얼 보기]] |

---

## 🎯 6. curve_fit 커브 피팅 및 타이어 곡선 도메인

> [!NOTE]- 🎯 curve_fit 타이어 특성 피팅 및 결합 모듈 목록 [클릭하여 펼치기]
> | 모듈 / 서브패키지 | 핵심 기능 및 역할 | 1:1 기술 매뉴얼 링크 |
> | :--- | :--- | :---: |
> | **`tire_curve` (`TireCurve`)** | **타이어 종/횡방향 비선형 특성 곡선 피팅 총괄 클래스 (단일 진실 공급원 - SSOT)** | [[tire_curve\|매뉴얼 보기]] |
> | **`fit_least_squares`** | Scipy 비선형 최소자승 가중치/Huber loss 추정기 (`EstimatorLeastSquares`) | [[fit_least_squares\|매뉴얼 보기]] |
> | **`curve_combiner`** | 다구간 스플라인 결합, 변곡점 검출 및 국소 트렌드 라인 복합 파이프라인 | [[curve_combiner\|매뉴얼 보기]] |

---

## 📐 7. models 공학 지배 수식 도메인

> [!NOTE]- 📐 models 순수 공학 수학 지배 방정식 및 신경망 모듈 목록 [클릭하여 펼치기]
> | 모듈 / 서브패키지 | 핵심 기능 및 역할 | 1:1 기술 매뉴얼 링크 |
> | :--- | :--- | :---: |
> | **`magic_formula`** | Pacejka Magic Formula 타이어 횡력/종력 비선형 모델 수식 (SSOT) | [[magic_formula\|매뉴얼 보기]] |
> | **`bicycle_model`** | 2자유도 차량 평면 횡방향 자전거 모델 수식 시뮬레이션 (`BicycleModel`) | [[bicycle_model\|매뉴얼 보기]] |
> | **`fit_nn`** | PyTorch / Scikit-Learn 기반 차량 동역학 신경망 모델러 | [[fit_nn\|매뉴얼 보기]] |

---

## 📶 7. signal_process 신호 후처리 및 정제 도메인

> [!NOTE]- 📶 post_process 4대 필터 및 FFT 모듈 목록 [클릭하여 펼치기]
> | 모듈 / 서브패키지 | 핵심 기능 및 역할 | 1:1 기술 매뉴얼 링크 |
> | :--- | :--- | :---: |
> | **`filters`** | Zero-Phase 이동평균 필터 및 Butterworth 저역통과 필터 | [[filters\|매뉴얼 보기]] |
> | **`resample`** | 비수치 메타데이터 손실 없는 시계열 고속 리샘플링 | [[resample\|매뉴얼 보기]] |
> | **`outliers`** | 이상치 자동 검출 및 연속 결측 구간 정제 | [[outliers\|매뉴얼 보기]] |
> | **`scaler`** | MinMax, Standard, Robust 시계열 신호 정규화 | [[scaler\|매뉴얼 보기]] |
> | **`extended_isolation_forest`** | 고차원 센서 이상치 탐지를 위한 EIF 알고리즘 | [[extended_isolation_forest\|매뉴얼 보기]] |
> | **`find_fft` / `single_track` / `tf_estimate`**| 주파수 스펙트럼 분석, 단일 트랙 FFT, 전달함수(TF) 추정 | [[find_fft\|FFT]] · [[single_track\|트랙]] · [[tf_estimate\|전달함수]] |

---

## 🛠️ 8. utils & logger 공통 유틸리티 도메인

> [!NOTE]- 🛠️ utils 및 로깅 모듈 목록 [클릭하여 펼치기]
> | 모듈 / 서브패키지 | 핵심 기능 및 역할 | 1:1 기술 매뉴얼 링크 |
> | :--- | :--- | :---: |
> | **`logger`** | 사내 프레임워크 표준 계층형 로깅 엔진 (Print 전면 퇴출) | [[logger\|매뉴얼 보기]] |
> | **`progress_bar`** | 콘솔 렌더링 칼정렬 및 깜빡임 없는 프로그레스 바 | [[progress_bar\|매뉴얼 보기]] |
> | **`console_style` / `styles`** | ANSI 컬러 터미널 출력 포맷터 | [[console_style\|console_style]] · [[styles\|styles]] |
> | **`dataframe_utils`** | 고속 판다스 조작, 데이터프레임 무결성 검증 유틸리티 | [[dataframe_utils\|매뉴얼 보기]] |
> | **`excel`** | OpenPyXL 기반 대용량 서식화 엑셀 시트 자동 생성기 | [[excel\|매뉴얼 보기]] |
> | **`files`** | 재귀적 파일 탐색, 디렉터리 안전 생성/삭제 유틸리티 | [[files\|매뉴얼 보기]] |
> | **`weather`** | 평가 일자/위치 기반 기상 데이터 수집 및 보간 | [[weather\|매뉴얼 보기]] |
> | **`window_handler` / `window_msg`** | 윈도우 OS 시스템 알림창 및 팝업 메시지 제어 | [[window_handler\|핸들러]] · [[window_msg\|메시지]] |

---

## 🤖 9. ai/database/statistics/gps 기타 도메인

> [!NOTE]- 🤖 AI, DB, 통계, GPS 모듈 목록 [클릭하여 펼치기]
> | 모듈 / 서브패키지 | 핵심 기능 및 역할 | 1:1 기술 매뉴얼 링크 |
> | :--- | :--- | :---: |
> | **`ai` (4대 모듈)** | 비선형 모델, 종방향 가속도 피팅, 최적화 모델, 딥러닝 피팅 | [[dynamic_model\|동적모델]] · [[fit_mf_ax\|MF가속]] · [[fit_minimize_optimization\|최적화]] · [[fit_nn\|신경망]] |
> | **`database` (5대 쿼리)** | PLM 및 사내 DW 시험 마스터, 조건, 결과 테이블 연동 SQL | [[auth_conn\|인증]] · [[load_plm\|PLM]] · [[q1_hkt_rnd_dw__test__tb_th_req_master_mst\|마스터]] · [[q2_hkt_rnd_dw__test__tb_th_rslt_odr_cdn_bas\|조건]] · [[q3_hkt_rnd_dw__test__tb_th_req_item_bas\|항목]] |
> | **`uno_statistics` / `uncertainty`**| 기술통계 요약(`summary`) 및 ISO GUM 표준 측정불확도 자동 평가 엔진 | [[summary\|통계요약]] · [[uncertainty\|측정불확도]] · [[uncertainty_theory\|불확도이론]] |
> | **`gps` (`gps_to_xy`)** | WGS84 위경도 좌표를 평면 직각 데카르트 좌표계(XY)로 투영 | [[gps_to_xy\|매뉴얼 보기]] |

---

## 📖 10. 사용자 매뉴얼 및 엔지니어링 표준

> [!NOTE]- 📘 사내 매뉴얼 및 코딩 표준 링크 [클릭하여 펼치기]
> * 📖 **[[90_ACCBRK_사용자매뉴얼|VT_ACCBRK 실무 사용자 매뉴얼]]**: 3단계 분석 공정 및 함수별 매개변수 가이드
> * 📘 **[[D:\00_obsidian\.agents\rules\PYTHON_CODE_AGENT.md|PYTHON_CODE_AGENT.md (글로벌 파이썬 마스터 규칙)]]**
> * 🛑 **[[00_제동_기술_통합_색인|차량 제동(Braking) 기술 위키 통합 색인]]**
> * 🏠 **[[04_Resources/00_지식_위키_통합_색인|04_Resources 지식 위키 중앙 대문]]**

---
**Last Updated**: 2026-09-29  
**Standard**: unoUtil Clean Architecture v2.0 & Single Baseline Law & Single Master MOC Law
