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
  - "00_curve_fit_대시보드"
  - "curve_fit_대시보드"
  - "00_file_reader_대시보드"
  - "00_graphics_대시보드"
  - "00_models_대시보드"
  - "00_post_process_대시보드"
  - "00_utils_대시보드"
  - "00_vehicle_dynamic_대시보드"
  - "00_vt_acc_brk_대시보드"
  - "00_snow_condition_대시보드"
  - "snow_condition_대시보드"
  - "file_reader_대시보드"
  - "graphics_대시보드"
  - "models_대시보드"
  - "post_process_대시보드"
  - "utils_대시보드"
  - "vehicle_dynamic_대시보드"
  - "vt_acc_brk_대시보드"
---

# 💼 unoUtil 사내 파이썬 통합 프레임워크 개발 프로젝트 (Master MOC)

> ⚡ **Quick Jump**: [📅 1. 체인지로그](#-1-프로젝트-주요-버전-이력-changelog-타임테이블) · [🏛️ 2. 아키텍처](#️-2-clean-architecture-11대-도메인-아키텍처) · [🏎️ 3. vehicle/acc_brk](#️-3-vehicle-동역학--가감속제동-vt_acc_brk-도메인) · [🚀 4. file_reader](#-4-file_reader-이기종-계측-데이터-리더-도메인) · [🎨 5. graphics](#-5-graphics-실차-시각화-및-인터랙션-도메인) · [🎯 6. curve_fit](#-6-curve_fit-커브-피팅-및-타이어-곡선-도메인) · [📐 7. models](#-7-models-공학-지배-수식-도메인) · [📶 8. signal_process](#-8-signal_process-신호-후처리-및-정제-도메인) · [🛠️ 9. utils/logger](#️-9-utils--logger-공통-유틸리티-도메인) · [🤖 10. ai/db/stats/gps](#-10-aidatabasestatisticsgps-기타-도메인) · [❄️ 11. snow_condition](#-11-snow_condition-노면-환경--머신러닝-보정-도메인) · [📖 12. 엔지니어링 표준](#-12-사용자-매뉴얼-및-엔지니어링-표준)

> [!ABSTRACT] 🚀 unoUtil 단일 마스터 MOC 허브
> 사내 파이썬 실차 데이터 분석 프레임워크 **`unoUtil v2.0+`**의 10대 도메인, 87개 핵심 모듈 기술 매뉴얼, Clean Architecture 명세 및 버전 관리 이력을 단일 페이지에서 1화면으로 조망·관리하는 **중앙 마스터 MOC 포털**입니다.

---

## 📅 1. 프로젝트 주요 버전 이력 (Changelog 타임테이블)

> [!NOTE]- 📜 v1.0 ~ v3.14 주요 개발 및 리팩토링 이력 [클릭하여 펼치기]
> | 버전 | 날짜 | 작업자 | 핵심 수정 및 개발 내역 (Changelog) | 상태 |
> | :---: | :---: | :---: | :--- | :---: |
> | **v3.14** | 2026-10-06 | uno &<br/>Gemini | ❄️ **스노우 제동 환경보정 방법 2 1차/2차 양방향 절대 보정(CORR_D1, CORR_D2, CORR_AVG) 파이프라인 완성 및 Figure 2 수렴 산점도 연동**<br/>• **방법 2 양방향 절대 보정 엔진 완성**: 1차와 2차 시험을 각각 사내 공통 기준 환경($-8.0^\circ\text{C}, 1.5\text{ g/m}^3$)으로 독립 절대 보정하여 `BRK_DIST_METHOD2_CORR_D1`, `BRK_DIST_METHOD2_CORR_D2`, `BRK_DIST_METHOD2_CORR_AVG` 산출 완비<br/>• **Figure 2-M2 산점도 수렴 벡터 연동**: `SnowSlopePlotter.scatter_restoration`에 양방향 절대 보정 모드 구현 (1차 및 2차의 보정 전 $\to$ 보정 후 $y=x$ 완전 일치선으로의 수렴 벡터 렌더링, 온습도 표준 환경 라벨링 정합)<br/>• **실증 검증 및 16개 시트 다중 엑셀/피클 배포**: 1,043쌍 검증 결과 2D-KNN 광역 평활화로 양측 절대 보정 시 오차 누적 없이 MAE $0.822\text{m} \to \mathbf{0.804\text{m}}$(+7.6% 개선), $R^2: 0.837 \to \mathbf{0.844}$, $r: 0.921 \to \mathbf{0.923}$ 달성 및 16개 시트 다중 엑셀(`df_corrected_method2_by_category_env.xlsx`) 일괄 재배포 완결 | ✅ 완료 |
> | **v3.13** | 2026-10-02 | uno &<br/>Gemini | ❄️ **스노우 제동 환경보정 2D-KNN 러프 평활화 모델 확정, 10~35m 이상치 필터링 복원, 복원 전·후 R² 및 산포개선율 단일 마스터 통합보고서 완성**<br/>• **방법 2 2D-KNN 러프 평활화 확정**: `SnowCorrectionModel(target_model='KNN Regressor')` 단일 엔진 적용, 국소 아일랜드 배제를 위해 $k=40\sim 150$(20%) 및 uniform 가중치 적용 완만 노면 반응면 도출<br/>• **정상 평가 구간(10m~35m) 이상치 필터링 복원**: 50m 수준 이상치 사전 차단으로 회귀면 왜곡 원천 제거<br/>• **단일 마스터 통합 보고서 완성 (개별 파편 파일 100% 정화)**: 분산된 개별 보고서 3종을 영구 삭제하고 `00_과거_스노우_제동_환경보정_종합_통합보고서.md` 단일 마스터로 통합, 그래프와 100% 일치하는 복원 전·후 $R^2$($0.70\sim 0.91$) 및 $r$($0.86\sim 0.96$) 단독 표와 방법 2 표준편차($\sigma$) 산포개선율 단독 표 정립<br/>• **심층 공학 분석 수록 (Section 2.2)**: 방법 1(RF) 절대 보정 적용 시 비선형 가산성 결핍 및 오차 누적(MAE 0.608m vs 1.110m) 실증 규명 및 역할 분담 체계 정립<br/>• **51종 시각화 및 16개 시트 다중 엑셀/피클 배포 완결** | ✅ 완료 |
> | **v3.12** | 2026-10-02 | uno &<br/>Gemini | ❄️ **unoUtil.snow_condition 노면 환경 선처리 분리, 방법 2 동일스펙 독립 물리 기울기 엔진(SnowSlopeModel) 정식 편입 및 No Redundant Prefix Law 적용 완결**<br/>• **데이터 선처리 전담 모듈 분리 (`preprocessor.py`)**: `filter_snow_conditions()`로 기온 영역(정상 vs 이상), 강설 여부(눈 제외 vs 포함), 타이어 카테고리별 선처리 로직 격리 및 모델 범용성 확보<br/>• **방법 2 전용 엔진 (`slope_model.py`) 신규 구축**: 동일 스펙(`SPEC_NO`) 중심화 1변수 독립 OLS 물리 기울기($k_{\text{air}}, k_{\text{ah}}$) 산출, 표준 환경(-8℃, 1.5g/m³) 일괄 보정 및 전용 플로터(`SnowSlopePlotter`) 탑재<br/>• **No Redundant Prefix Law 전면 준수**: 플로터 내 메서드명에서 `plot_` 접두사 전면 삭제 (`delta_prediction_scatter`, `scatter_restoration`, `correction_map`, `slope_scatter`, `variance_reduction`)<br/>• **과거 7개년 스노우 제동 데이터 전면 재구축 및 8대 데이터셋/시각화 완료**: 4대 시나리오별 매트릭스 파이프라인 가동 및 8종 pkl/xlsx 분리 저장, 90여 종 시각화 실시간 배포 완료 | ✅ 완료 |
> | **v3.11** | 2026-10-02 | uno &<br/>Gemini | 🏎️ **unoUtil.vehicle.acc_brk 가감속/제동 전 도메인 v2 정식 표준화 및 로거 레벨 격리 완결**<br/>• **인스턴스 격리 동적 로거 아키텍처 수립**: `print` 키워드 인자 전면 퇴출 및 `level: Union[int, str] = logging.DEBUG/INFO` 도입, 피클 직렬화 안전성을 위한 `self._level` 저장 + `@property def logger(self):` 동적 바인딩 완성<br/>• **과도기 코드 레거시 취급 배제 (Single Baseline Law)**: `cal_control.py` 및 `.md` 완전 삭제 및 `correct.py` 단일 SSOT 흡수, v2 내부 상호 호출에서 구버전 대문자 심볼 전면 배제<br/>• **전용 클래스 메서드 접두사 중복 배제 (No Redundant Prefix)**: `PlotterTire`, `PlotterProject`의 `plot_` 접두사를 제거하여 `plotter.accbrk()`, `plotter.all()`, `compare_braking()` 등 직관적 객체지향 API 정립<br/>• **표준 파라미터 네이밍 전면 정합**: `df_raw`, `df_input` ➔ `data: pd.DataFrame`, `sr` ➔ `sample_rate`, `flag_print` ➔ `level`<br/>• **18개 소스 파일 및 15종 기술 매뉴얼 100% 무결성 검증**: AST 기반 파라미터 정밀 감사(구버전 변수 0건) 및 모듈별 자율 시뮬레이션(Exit Code 0) 전원 통과, 옵시디언 볼트 1:1 미러링 완료 | ✅ 완료 |
> | **v3.10** | 2026-10-01 | uno &<br/>Gemini | ❄️ **SnowSurfaceInterpolator 순수 공간 보간기 정립 (센서 연산 완전 분리, char_* 단일 표준화 및 3중 결측/이상치 방어)**<br/>• **센서 하드웨어 연산 100% 완전 분리 (SoC)**: 보간기 내부의 특정 센서 뺄셈(`Height1~6`, `Temp1~2`, `h_left`, `h_right`, `h_out`, `h_tire` 등)을 전면 삭제하고 데이터 전처리 영역으로 격리, 순수 3D 공간 보간기에만 집중하도록 정립<br/>• **`char_*` 단일 명명 체계 (SSOT) 전면 일원화**: 파편화된 별칭(`calc_h_diff`, `calc_t_diff`, `HeightDiffAver`, `TempDiffAver`) 영구 정리, `char_height`, `char_temp`, `Cond_ID` 표준 컬럼으로 인터페이스 및 내부 학습 단일화<br/>• **3중 결측치·이상치 안전 정제 파이프라인 (`_sanitize_feature`, `np.clip`)**: 비수치 변환 ➔ 센서 결측치(NaN) 중앙값 대치 ➔ 물리적 범위 이탈값 `np.clip` 상/하한 안전 제한 완비<br/>• **실데이터 엔드투엔드 파이프라인 전수 통과**: `b_combine_surface_performance_spec.py` 1,964건 전수 결합 및 `c_run_snow_correction_pipeline.py` 머신러닝 차분 보정 완벽 완주 (Exit Code 0) | ✅ 완료 |
> | **v3.9** | 2026-10-01 | uno &<br/>Gemini | ❄️ **노면 차분 머신러닝 보정 엔진 동적 특성 인자(x_cols, y_col) 지원, 결측치(NaN) 방어 가드 및 시각화 동적화**<br/>• **동적 특성 인자 리스트 표준화**: 고정 키워드 인자(`x_1`, `x_2`)를 완전히 탈피하고, 파이썬 표준 리스트 인터페이스 `x_cols: Optional[List[str]]` 및 `y_col: str`로 전면 개편 (기온, 습도, 침하량 등 임의 조합 및 3개 이상 다변량 피처 확장 100% 지원)<br/>• **결측치(NaN) 자동 정제 및 방어 가드 (`missing_strategy='drop'`)**: 센서 결측치 자동 드롭, All NaN 컬럼 및 빈 입력 시 명시적 `ValueError` 사전 차단<br/>• **다형성 예측 인터페이스 (`predict_delta`)**: 스칼라, 딕셔너리, NumPy 배열, Pandas DataFrame 단일 함수 다형성 지원<br/>• **시각화 플로터 및 검증기 100% 동적 라벨링 연동**: 모델에 전달된 특성 컬럼명이 산점도(Fig 1), 2D 등고선 맵(Fig 3), 대조표에 자동 실시간 반영<br/>• **전수 무결성 검증 통과**: 단위 테스트 및 1,964건 실데이터 파이프라인 완벽 완주 (Exit Code 0) | ✅ 완료 |
> | **v3.8** | 2026-10-01 | uno &<br/>Gemini | ❄️ **SnowSurfaceInterpolator 직관적 단일 표준 확립 및 12:30 세션 쪼개짐 원천 해결**<br/>• **네이밍 & 아키텍처 혁신**: 추상적이고 모호했던 `SurfaceConditionTwin` 및 `surface_twin.py`를 완전히 폐기하고, 수치해석/데이터과학 표준에 부합하는 **`SnowSurfaceInterpolator`** (`surface_interpolator.py`)로 승격 리팩토링<br/>• **사이킷런 표준 인터페이스**: `interp.fit(df_surface)` (3D 격자 보간 모델 구축) $\to$ `interp.transform(df_brk)` (제동 데이터에 노면 특성치 일괄 결합) 표준 확립<br/>• **시험 묶음 최초 시작 시각(`min(Datetime)`) 기반 단일 세션 결합**: `Date + ReqNo + TestOrder` 그룹별 최초 시작 시각을 감지하여 12:30 경계 전후에 걸쳐 진행된 제동 시험 세트가 am/pm으로 분열되는 치명적 데이터 왜곡 결함을 100% 원천 해결<br/>• **파이프라인 초경량화**: `b_combine_surface_performance_spec.py`의 수동 for 루프 30줄을 단 2줄로 압축, 1,964건 제동 데이터 전수 매칭 및 2026-01-13 단일 세션 유지 완벽 검증 | ✅ 완료 |
> | **v3.7** | 2026-10-01 | uno &<br/>Gemini | ❄️ **노면 정비 세션(Cond_ID) 기반 시공간 디지털 트윈 격리 보간 및 SSOT 스키마 정합**<br/>• **세션(Session) 개념 정합**: '동일 시기 및 동일 노면 컨디션(정비 이력)'을 보장하는 단일 세션(`Cond_ID`, 예: `2026-01-15_am`, `2026-01-19_all`) 체계 완비<br/>• **세션 자동 분류기 편입**: `classify_surface_condition(dt)` 공식 함수 구현 (노면일지 3단계 정비 캘린더 규칙: 2회 정비일 12:30 분기, 혹한 0/1회 정비일 all 단일 세션 자동 판별)<br/>• **세션 격리 시공간 보간**: `SurfaceConditionTwin.get_surface_condition`에서 해당 `Cond_ID` 스냅샷 그룹 내부에서만 시간 축 선형 보간을 수행하여 정비 전후 노면 왜곡 및 이종 날짜 혼합 원천 차단<br/>• **스키마 및 애니메이터 연동**: `schema.py`(`COL_COND_ID`, `COL_PREPARING`), `surface_animator.py`(`cond_id` 인자 지원) 전면 정합 및 전수 자가 테스트 통과 (Code 0) | ✅ 완료 |
> | **v3.6** | 2026-10-01 | uno &<br/>Gemini | ❄️ **Single Master MOC 헌장 정합 및 snow_condition 서브모듈 리팩토링**<br/>• **Single Master MOC & Vault-Only SSOT 완결**: 소스 코드 디렉토리 내 오생성 대시보드 및 하위 대시보드 영구 삭제, 최상위 단일 대시보드로 MOC 완전 흡수 일원화<br/>• **모듈 명명 정합화**: 프로젝트 대시보드와의 명칭 혼동을 원천 해소하기 위해 `dashboard.py` ➔ **`surface_animator.py`**(`SurfaceAnimator` 클래스 및 `create_surface_animation_figure` 함수)로 승격 리팩토링<br/>• **1:1 기술 매뉴얼 정합**: `surface_animator.md` 로컬 및 옵시디언 이중 동기화 완료 및 전수 자가 구동 테스트 통과 (Exit 0) | ✅ 완료 |
> | **v3.5** | 2026-09-30 | uno &<br/>Gemini | ❄️ **snow_condition 공식 도메인 승격 및 acc_brk 스타일 컴포지션 패턴 구축**<br/>• **snow_condition 전면 이관**: 47대 SSOT 노면 계측, 물리 역학, 3D 디지털 트윈, 4D 대시보드, ML 보정 엔진 공식 편입<br/>• **컴포지션 패턴 분할**: SnowCorrectionModel(코어 모델) + SnowCorrectionValidator(정량 검증) + SnowCorrectionPlotter(시각화 플로터)<br/>• **보정 전/후 다형성 비교 플롯**: plot_tire_subsets_comparison 구현 (의뢰번호 전체 서브플롯 및 개별 세트 상세 플롯, 1st Ref선 vs 2nd Raw 점선 vs 2nd Corr 실선 + Run 산점도)<br/>• **1:1 기술 매뉴얼 7종 및 하위 대시보드 MOC 완비, 전수 무결성 검증 통과 (Exit 0)** | ✅ 완료 |
> | **v3.4** | 2026-09-29 | uno &<br/>Gemini | 🎯 **curve_fit 최상위 도메인 승격, tire_curve 패키지 완전 일원화 및 단일 마스터 MOC 정비**<br/>• **curve_fit 최상위 도메인 신설**: `unoUtil.curve_fit` 도메인 및 `tire_curve/` 전용 패키지 구축<br/>• **타이어 피팅 단일 모듈화**: `CurveCombiner`, `fit_mf_ax`, `estimatorMF`, `MinimizeEstimator` 등 분산 피팅을 **`TireCurve` 단 하나의 타이어 피팅 모듈**로 완전 흡수 통합<br/>• **57KB 스플라인 결합 파이프라인 수납**: `curve_combiner/` 복합 파이프라인의 내부 캡슐화 및 OCP 미래 확장 구조 완비<br/>• **models(수식)와 curve_fit(피팅) 역할 분리**: `models`는 순수 지배 방정식 SSOT, `curve_fit`은 데이터 피팅 전담<br/>• **12대 도메인 및 36개 레거시 경로 100% 무결성 검증 통과 (Exit 0)** | ✅ 완료 |
> | **v3.3** | 2026-09-28 | uno &<br/>Gemini | 🎯 **TireCurve 전략 패턴 및 BicycleModel 전면 표준화 완결 (Exit 0)**<br/>• **TireCurve 구축**: 임의 수학 모델(`model`) 및 최적화 전략(`method`) 주입 가능한 전략 패턴(Strategy Pattern) 기반 단일 클래스 설계<br/>• **2-DoF 자전거 모델 정합**: `dynamic_formula` ➔ `bicycle_model.py`(`BicycleModel`) 자동차공학 국제 표준 정규화<br/>• **Pacejka MF SSOT 확립**: 도메인별 분산 수식을 `calc_magic_formula` 단일 코어로 일원화<br/>• **무결성 검증 100% 통과**: 11대 공식 도메인 패키지 & 36개 구버전 레거시 가상 리다이렉션 전원 통과 | ✅ 완료 |
> | **v2.9** | 2026-09-26 | uno &<br/>Gemini | 🏎️ **unoUtil.vehicle 도메인 v2 전면 표준화 및 Single Baseline Law 확립**<br/>• `vehicle_dynamic.py`를 `VehicleDynamic` 단일 표준 클래스로 캡슐화 완료 (8대 표준 동사 정합, v1 호환 별칭 바인딩, 비차단 시각화 및 자가 구동 테스트 스위트 구축)<br/>• `hndl_test.py`, `test_infor_res.py`, `analysis_test_data.py` 전면 리팩토링 및 1:1 위키 매뉴얼 100% 달성 | ✅ 완료 |
> | **v2.8** | 2026-09-24 | uno &<br/>Gemini | 🏁 **unoUtil v2.0 아키텍처 전면 완료 및 전수 무결성 검증 100% 통과 (Final)**<br/>🛡️ 사내 보안 정책(AppLocker) 및 Windows 11 Smart App Control 대응: `D:\uno\Python\envs\unoBase` 표준 환경 구축 및 C/Fortran 확장 DLL 로드 차단 완벽 해소<br/>🧪 전사 10대 도메인 & 36개 세부 레거시 경로 무결성 100% 통과 (`test_structure_integrity.py` Exit 0 달성) | ✅ 완료 |
> | **v2.7** | 2026-09-23 | uno &<br/>Gemini | 🧹 **전사 역방향 별칭(`Standard = LEGACY`) 전수 제거 및 정방향(`LEGACY = Standard`) 일괄 정합화**<br/>🛡️ 물리 `legacy/` 9개 디렉터리 및 `convenienceFunction/` 전량 `_archive/` 영구 퇴출 (Zero Physical Legacy 달성) | ✅ 완료 |
> | **v2.6** | 2026-09-23 | uno &<br/>Gemini | 🗄️ **GetDB 실차시험 스펙 및 결과 통합 엔진 신규 구축**<br/>• `_func_connect_spec_with_req_set.py` 및 `_func_connect_vehicle_test_and_spec.py` 구현, SSL 인증서 패치 적용 | ✅ 완료 |
> | **v2.0** | 2026-09-18 | uno &<br/>Gemini | 🏎️ **unoUtil v2.0 Clean Architecture 10대 도메인 설계 전면 전환**<br/>📦 패키지 다이어트: 1GB+ 거대 계측 데이터 전량 분리 $\rightarrow$ 루트 `test_data/` 중앙 통합 (15.62MB 순수 파이썬 초경량화, 98.5% 절감)<br/>🎯 8대 표준 동사 네이밍 수립 및 `MetaPathFinder` 무중단 가상 로더 수립 | ✅ 완료 |
> | **v1.0** | 2026-09-10 | uno | 🚀 unoUtil 사내 파이썬 통합 프레임워크 개발 프로젝트 킥오프 | ✅ 완료 |

---

## 🏛️ 2. Clean Architecture 12대 도메인 아키텍처

> [!NOTE]- 🏗️ 아키텍처 다이어그램 및 패키지 구조 [클릭하여 펼치기]
> ```mermaid
> flowchart TD
>     subgraph Storage_Isolation [프로젝트 최상위 3대 기둥 분리]
>         P_CODE["🚀 unoUtil/ (순수 파이썬 프레임워크 - 초경량화)"]
>         T_DATA["⭐ test_data/ (단일 중앙 테스트 데이터 - 90% 다이어트)"]
>         ARCH["🗄️ _archive/ (과거 코드 영구 보존소 - 탐색기 열람)"]
>     end
> 
>     subgraph Core_Domains [unoUtil 12대 핵심 도메인]
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
>         SC["❄️ snow_condition/ (노면 환경 & ML 보정)"]
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

## 📶 8. signal_process 신호 후처리 및 정제 도메인

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

## 🛠️ 9. utils & logger 공통 유틸리티 도메인

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

## 🤖 10. ai/database/statistics/gps 기타 도메인

> [!NOTE]- 🤖 AI, DB, 통계, GPS 모듈 목록 [클릭하여 펼치기]
> | 모듈 / 서브패키지 | 핵심 기능 및 역할 | 1:1 기술 매뉴얼 링크 |
> | :--- | :--- | :---: |
> | **`ai` (4대 모듈)** | 비선형 모델, 종방향 가속도 피팅, 최적화 모델, 딥러닝 피팅 | [[dynamic_model\|동적모델]] · [[fit_mf_ax\|MF가속]] · [[fit_minimize_optimization\|최적화]] · [[fit_nn\|신경망]] |
> | **`database` (5대 쿼리)** | PLM 및 사내 DW 시험 마스터, 조건, 결과 테이블 연동 SQL | [[auth_conn\|인증]] · [[load_plm\|PLM]] · [[q1_hkt_rnd_dw__test__tb_th_req_master_mst\|마스터]] · [[q2_hkt_rnd_dw__test__tb_th_rslt_odr_cdn_bas\|조건]] · [[q3_hkt_rnd_dw__test__tb_th_req_item_bas\|항목]] |
> | **`uno_statistics` / `uncertainty`**| 기술통계 요약(`summary`) 및 ISO GUM 표준 측정불확도 자동 평가 엔진 | [[summary\|통계요약]] · [[uncertainty\|측정불확도]] · [[uncertainty_theory\|불확도이론]] |
> | **`gps` (`gps_to_xy`)** | WGS84 위경도 좌표를 평면 직각 데카르트 좌표계(XY)로 투영 | [[gps_to_xy\|매뉴얼 보기]] |

---


---

## ❄️ 11. snow_condition 노면 환경 & 머신러닝 보정 도메인

> [!NOTE]- ❄️ snow_condition 7대 핵심 모듈 목록 [클릭하여 펼치기]
> | 모듈명 | 핵심 클래스 / 역할 | 1:1 기술 매뉴얼 링크 |
> | :--- | :--- | :---: |
> | **`schema`** | SSOT 47대 표준 컬럼 및 DataFrame 정규화 단일 관문 (`harmonize_snow_dataframe`) | [[schema|매뉴얼 보기]] |
> | **`physics`** | Sonntag 빙점하 수증기압, 과포화도, 타이어 접지압 물리 역학 수식 | [[physics|매뉴얼 보기]] |
> | **`surface_interpolator`** | 센서 좌표계 복원, 3D 시공간 격자 보간 및 시험 묶음 시작 시각 기반 결합 (`SnowSurfaceInterpolator`) | [[surface_interpolator|매뉴얼 보기]] |
> | **`surface_animator`** | Plotly 4D 시공간 인터랙티브 노면 환경 애니메이션 (`SurfaceAnimator`) | [[surface_animator|매뉴얼 보기]] |
> | **`correction_model`** | 6대 머신러닝 회귀 학습 및 데이터 보정 코어 엔진 (`SnowCorrectionModel`) | [[correction_model|매뉴얼 보기]] |
> | **`correction_validator`** | 1st vs 2nd 대조표 산출, 엑셀 내보내기, 오차 감소율 통계 (`SnowCorrectionValidator`) | [[correction_validator|매뉴얼 보기]] |
> | **`correction_plotter`** | 다형성 비교 플롯, 오버플랏 산점도, 2D 등고선 보정 맵 (`SnowCorrectionPlotter`) | [[correction_plotter|매뉴얼 보기]] |
> 
> ```mermaid
> classDiagram
>     direction TB
>     class SnowCorrectionModel {
>         +model_type: str
>         +train(df_train)
>         +predict_diff(df_cur, df_ref)
>         +correct_dataframe(df)
>         +validator: SnowCorrectionValidator
>         +plot: SnowCorrectionPlotter
>     }
>     class SnowCorrectionValidator {
>         +calc_corrected_comparison_table(df_test)
>         +evaluate_restoration_metrics(df_comp)
>     }
>     class SnowCorrectionPlotter {
>         +plot_delta_prediction_scatter()
>         +plot_scatter_restoration()
>         +plot_correction_map()
>         +plot_tire_subsets_comparison(req_no, tire_set)
>     }
>     SnowCorrectionModel *-- SnowCorrectionValidator : Composition (self.validator)
>     SnowCorrectionModel *-- SnowCorrectionPlotter : Composition (self.plot)
> ```

---

## 📖 12. 사용자 매뉴얼 및 엔지니어링 표준

> [!NOTE]- 📘 사내 매뉴얼 및 코딩 표준 링크 [클릭하여 펼치기]
> * 📖 **[[90_ACCBRK_사용자매뉴얼|VT_ACCBRK 실무 사용자 매뉴얼]]**: 3단계 분석 공정 및 함수별 매개변수 가이드
> * 📘 **[[D:\00_obsidian\.agents\rules\PYTHON_CODE_AGENT.md|PYTHON_CODE_AGENT.md (글로벌 파이썬 마스터 규칙)]]**
> * 🛑 **[[00_제동_기술_통합_색인|차량 제동(Braking) 기술 위키 통합 색인]]**
> * 🏠 **[[04_Resources/00_지식_위키_통합_색인|04_Resources 지식 위키 중앙 대문]]**

---

## 📜 13. 버전 이력 및 주요 개발 현황 (Changelog)

### [2026-10-01] v3.9 - 노면 차분 머신러닝 보정 엔진 동적 특성 인자(x_cols, y_col) 지원, 결측치(NaN) 방어 가드 및 시각화 동적화
- **동적 특성 인자 리스트 인터페이스 (`x_cols: List[str]`, `y_col: str`) 혁신**:
  - 기존의 고정 키워드 인자(`x_1`, `x_2`) 방식을 과감히 폐기하고 머신러닝 표준 규격인 `x_cols: Optional[List[str]]` 및 `y_col: str`로 전면 개편.
  - 침하 깊이, 표면 온도, 기온, 절대습도 등 임의의 실험 인자 조합은 물론 3개 이상의 다변량 피처 확장까지 완전 지원.
- **결측치(NaN) 자동 정제 및 방어 가드 (`missing_strategy='drop'`)**:
  - 센서 결측치 자동 드롭, All NaN 컬럼 및 빈 입력 시 명시적 `ValueError` 사전 차단.
- **다형성 예측 인터페이스 (`predict_delta`)**:
  - 스칼라 가변인자(`*args`), 딕셔너리(`dict`), 1D/2D NumPy 배열, Pandas DataFrame 입력을 단일 함수에서 자동 판별 처리.
- **시각화 플로터 및 검증기 100% 동적 라벨링 연동**:
  - `SnowCorrectionPlotter`의 Figure 1(산점도), Figure 3(등고선 맵), 오버플랏 플롯의 축 라벨 및 타이틀이 모델의 `x_cols`, `y_col` 명칭으로 자동 치환.
  - 다변량(3개 이상) 피처 등고선 맵 렌더링 시 미선택 축은 0.0(기준 baseline)으로 고정하여 2D 격자 정밀 평가.
- **전수 무결성 검증 통과 (Exit Code 0)**:
  - 단위 테스트 및 실데이터 1,964건 통합 파이프라인 전수 완주 (Exit Code 0).

### [2026-10-01] v3.8 - SnowSurfaceInterpolator 직관적 단일 표준 확립 및 12:30 세션 쪼개짐 원천 해결
- **`SnowSurfaceInterpolator` 리팩토링 및 완전 승격**:
  - 모호했던 과도기적 명칭 `SurfaceConditionTwin` 및 `surface_twin.py`를 완전히 폐기하고, 사이킷런 표준 인터페이스 기반의 직관적인 **`SnowSurfaceInterpolator`** (`surface_interpolator.py`)로 전면 개편.
  - `fit(df_surface)` $\to$ `transform(df_brk)` 구조로 표준화하여 `b_combine_surface_performance_spec.py`의 수동 for 루프를 단 2줄로 경량화.
- **시험 묶음 최초 시작 시각(`min(Datetime)`) 기반 단일 세션 결합 (`transform`)**:
  - `Date + ReqNo + TestOrder` 그룹별로 평가 시작 시각을 감지하여 세션(`test_cond_id`)을 판별.
  - 12:30 전후로 걸쳐 진행된 제동 시험 세트(예: 2026-01-13 10:07~12:34)가 런별 단순 시각 비교로 인해 am/pm으로 분열되던 중대 결함을 100% 원천 해결.
- **파이프라인 무결성 검증 완결**:
  - `surface_interpolator.py`, `surface_animator.py` 자가 구동 테스트 전수 통과 (Exit Code 0).
  - 실차 제동 1,964건 전수 보간 매칭 완결 및 2026-01-13 단일 세션 유지 완벽 검증.

### [2026-10-01] v3.6 - snow_condition 도메인 a_/b_ 전처리 직렬 연계 및 중복 컬럼 완전 정화
- **a_/b_ 전처리 직렬 연계**: `a_make_SnowAccBrkTest_DF.py`, `a_make_SnowSurfaceCharacteristic_DF.py`, `a_make_SRTT_DF.py` 최종 저장에 `harmonize_snow_dataframe` 적용.
- **`b_combine_surface_performance_spec.py` 전면 현대화**: 과거 레거시 파사드를 완전 걷어내고 `SurfaceConditionTwin` 직접 인스턴스화하여 53개 3D 스냅샷 복원 $\to$ 1,964건 제동 런 1:1 시공간 보간 매칭 파이프라인 완성.
- **스키마 무결성 강화**: `schema.py` 내 레거시 다대일 매핑 시 중복 컬럼 생성 버그 원천 해결 및 `COL_47_ORDER` 표준 정렬 상수 공식 탑재.
- **Exit Code 0 무결성 통과**: `c_run_snow_correction_pipeline.py` 가동 전수 통과 (3초 완결).

---
**Last Updated**: 2026-10-01  
**Standard**: unoUtil Clean Architecture v3.9 & Single Baseline Law & Single Master MOC Law
