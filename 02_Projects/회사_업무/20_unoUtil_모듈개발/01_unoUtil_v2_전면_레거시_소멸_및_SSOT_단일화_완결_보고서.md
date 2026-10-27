---
id: "unoutil_v2_legacy_cleanup_and_ssot_finalization_report"
title: "unoUtil v2.0 전면 레거시 소멸, 절대 참조 단일화 및 SSOT 표준화 완결 종합 보고서"
type: report
category_main: 회사_업무
category_sub: unoUtil
date: 2026-10-27
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - 리팩토링
  - 보고서
  - 아키텍처
  - CleanArchitecture
  - SSOT
project_link: "[[00_unoUtil_모듈개발_대시보드]]"
---

# 🏛️ unoUtil v2.0 전면 레거시 소멸, 절대 참조 단일화 및 SSOT 표준화 완결 종합 보고서

> **작성 일자**: 2026-10-27  
> **작성자**: Uno & Antigravity 에이전트  
> **상위 대시보드 링크**: [[00_unoUtil_모듈개발_대시보드]]  
> **관련 소스 코드 저장소**: `D:\uno\Python\Projects\unoUtil` (`branch: refactor-v2`)  
> **적용 버전**: `unoUtil v3.68.0` (Clean Architecture SSOT Finalized)

---

## 📌 1. 개요 및 추진 배경 (Overview & Background)

`unoUtil`은 사내 실차 주행 시험(가감속, 제동, 조종안정성 등)과 다양한 센서 계측 데이터(VBOX, Dewesoft, GPS 등)를 통합 처리하는 핵심 파이썬 프레임워크입니다.  
v2 Clean Architecture로 구조 재편을 거치며 12대 전문 도메인이 확립되었으나, 실제 실무 환경에서 다음과 같은 **구조적 부채와 잠재적 오류 요인**이 존재했습니다:

1. **내부 `__main__` 단독 실행 시 상대 참조 에러 발생**:
   - 패키지 내 33개 파일에서 `from .` 또는 `from ..` 형태의 상대 참조(Relative Import)를 혼용하여, VS Code나 터미널에서 특정 스크립트를 단독 실행할 때 `ImportError: attempted relative import with no known parent package` 에러가 빈번히 발생함.
2. **v2 과도기 중간 코드와 빈 껍데기 폴더 잔존**:
   - 상위 도메인(`models/`, `curve_fit/`)으로 기능이 승격된 이후에도 임시 래퍼 역할을 하던 브릿지 파일(`ai/*.py`, `curve_fit/tire_curve/fit_least_squares.py`)과 내용물 없는 빈 `legacy/` 폴더 7곳이 방치되어 구조적 혼선을 유발함.
3. **모듈 내부 하단에 중복 기재된 과거 호환용 레거시 별칭(Aliases)**:
   - 각 파이썬 모듈 파일 하단에 `Infor_Vehicle = InforVehicle`, `VD_AlignCoordinate = align_coordinate` 등 v1 구버전 호출을 지원하기 위한 수십 개의 별칭이 잔존하여 단일 진실 공급원(SSOT) 원칙을 저해함.
4. **루트 및 서브 `__init__.py`의 비대화**:
   - 최상위 `unoUtil/__init__.py`에 250줄이 넘는 과거 가상 리다이렉터 엔진과 가상 모듈 바인딩 코드가 적재되어 패키지 로딩 오버헤드와 복잡도를 가중시킴.
5. **코드 저장소 내 비매뉴얼 보고서/임시 산출물 방치**:
   - 1:1 기술 매뉴얼 격리 보존 헌장에도 불구하고, 백서나 과거 분석 보고서, 하드코딩된 일회성 연구 스크립트와 수십 MB의 차트 이미지(`fig/`)가 코드 디렉토리에 혼재함.

이에 사용자의 명확한 **4대 핵심 대원칙**을 수립하고, 패키지 전역에 걸친 대대적인 클린업 및 단일화를 집행하였습니다.

---

## ⚖️ 2. 확립된 4대 핵심 대원칙 (Core Mandates)

본 리팩토링은 타협 없는 단일 진실 공급원(SSOT) 구축을 위해 아래 4대 원칙을 철저히 집행했습니다:

1. **모든 과거용 레거시는 삭제한다 (No Standalone Legacy Law)**:
   - 소스 코드 디렉토리 내에 물리적으로 존재하는 모든 과거용 레거시 브릿지 파일, 과도기 래퍼, 빈 `legacy/` 폴더를 전수 삭제.
2. **과거를 위해 남겨둔 폴더, 파일, 모듈 임포트등도 모두 정리한다**:
   - 과거 호환성만을 위해 각 패키지/모듈에 중복으로 유지되던 별칭, 이종 모듈 재노출(Re-export), 불필요한 브릿지 구문을 걷어내고 오직 최신 v2 표준 심볼만 보존.
3. **각 서브 모듈들에 대한 `__init__.py` 에도 과거 레거시와 호환성을 위해 남겨둔 부분들은 정리한다**:
   - 서브패키지 `__init__.py`에서 과거 구버전 모듈 바인딩, v1 대문자 별칭, 철자 오타 별칭을 전수 제거.
4. **유노유틸 전체(최상위 루트) 모듈에 대한 `__init__.py` 에서도 과거 호환성을 위한 부분들은 다 정리한다**:
   - 최상위 루트 `unoUtil/__init__.py`의 메타패스 리다이렉터 및 가상 모듈 바인딩(250줄+)을 전면 삭제하고, 순수 12대 공식 도메인 Facade(180줄)로 전면 슬림화.

---

## 🛠️ 3. 세부 리팩토링 및 클린업 수행 내역

### Phase 1. 상대 참조 100% 절대 참조(`unoUtil.*`) 전환 (총 33개 파일)
- **전수 스캔 및 변환**: `from .` 및 `import .` 구문을 전수 발굴하여 모두 `from unoUtil.<도메인>.<모듈>` 형태의 완전한 절대 참조로 치환 완료.
- **파일명 중복 모호성 원천 차단**: 서로 다른 패키지에 동일 이름이 존재하던 모듈(`magic_formula`, `fit_nn`, `detect_initial_rectangle`, `make_trend_line` 등)을 고유한 절대 경로로 명확히 매핑하여 임포트 충돌 방지.
- **효과**: 개별 파이썬 파일을 어디서 실행하더라도 `attempted relative import` 에러 없이 독립 실행(`__main__`) 및 단위 테스트가 100% 보장됨.

### Phase 2. 과거용 레거시 폴더 및 브릿지 파일 전수 삭제
- **비어있는 `legacy/` 디렉토리 7개소 영구 삭제**:
  - `ai/legacy`, `database/legacy`, `file_reader/legacy`, `logger/legacy`, `signal_process/fft/legacy`, `signal_process/post_process/legacy`, `vehicle/legacy`
- **과도기 레거시 브릿지 모듈 및 매뉴얼 영구 삭제**:
  - `ai/fit_minimize_optimization.py`, `.md` (존재하지 않는 모듈 임포트로 에러 유발 중이던 죽은 코드)
  - `ai/dynamic_model.py`, `.md` (`models/mathematical`로 승격 완료)
  - `ai/fit_nn.py`, `.md` (`models/neural_net`으로 승격 완료)
  - `curve_fit/tire_curve/fit_least_squares.py` (`curve_fit/estimators`로 승격 완료)
  - `signal_process/curve_fit/` (잔여 껍데기 디렉토리 및 `CurveCombiner` 브릿지 전수 삭제 $	o$ 커브 피팅은 최상위 도메인 `curve_fit`으로 단일화)
- **루트 임시 잔재 파일 삭제**:
  - `1` (외부 Chrome DevTools MCP 실행 시 쉘 리다이렉션 실수로 생성되었던 임시 파일 삭제 및 `.gitignore` 등록)
  - `.pytest_cache/`, `unoUtil.egg-info/`, `signal_process/post_process/resample.py.bak`

### Phase 3. `example/` 디렉토리 임시 연구 스크립트 및 대용량 결과물 정리
- **삭제 항목**:
  - 특정 PC 로컬 경로(`C:\Users\uunnoo\...`)가 하드코딩되어 외부 실행이 불가능했던 일회성 연구 스크립트 5종 (`example_acc_speed_cutoffs.py`, `example_combiner_diagnostics.py`, `example_combiner_speed_matrix.py`, `example_acc_brk_start_points.py`, `comprehensive_example.py`)
  - `example/fig/` 대용량 차트 이미지 폴더 전체 삭제 (저장소 다이어트 달성)
- **표준 검증 도구 보존**:
  - `example/test_structure_integrity.py` (v2 순수 표준 도메인 무결성 전수 검증)
  - `example/test_pep8_all.py` (PEP 8 표준 규격 및 클래스/함수 검증)
  - `example/example_scan_dir_progressbar.py` (독립 실행형 ProgressBar 데모)

### Phase 4. 각 서브 모듈 내 과거 호환용 레거시 별칭(Alias) 32개 파일 전수 소멸
모듈 파일 내부 하단에 선언되어 있던 `Alias = RealName` 형태의 레거시 별칭 코드를 전수 삭제하고, 정식 표준 명칭(SSOT)으로 단일화:

| 도메인 | 대상 파일 | 주요 조치 및 제거된 별칭 |
| :--- | :--- | :--- |
| **`file_reader`** | `standard_channel_pattern.py` | • `Infor_Vehicle`, `Infor_SensorPosition`, `GPS` 전면 삭제 |
| **`vehicle`** | `vehicle_dynamic.py` | • `VD_AlignCoordinate`, `VD_RotKinematics`, `VD_RotOrigin`, `VD_CalP2PInterCoordinate`, `VD_CalSideSlipAngle`, `VD_CalSlipAngleFR`, `VD_CalLoadTransferLongi`, `makeStandardDF` (v1 대문자 별칭 8개 전면 삭제) |
| | `hndl_test.py` | • `SP_CurveFit_RF`, `sp_curvefit_rf`, `SP_CurveFit_MF`, `sp_curvefit_mf` 삭제<br>• 내부 `TireMagicFormula` 호출을 정식 `calc_tire_magic_formula`로 직결 |
| | `test_infor_res.py` | • `TEST_INFORMATION`, `TEST_RESULT` 대문자 별칭 삭제 |
| | `analysis_test_data.py` | • `make_performance_df`, `make_compare_df` 별칭 삭제 |
| **`signal_process`** | `resample.py` | • `SP_Resample`, `SP_Interpolation`, `SP_Merge` 삭제 |
| | `filters.py` | • `fast_denoise_wavelet_1d`, `SP_MovingAverage` 삭제 |
| | `outliers.py` / `scaler.py` | • `SP_RMOutlier`, `SP_Normal` 삭제 |
| | `sections.py` | • 내부 `fast_denoise_wavelet_1d` 호출을 정식 `denoise_wavelet`으로 단일화 |
| | `single_track.py` / `tf_estimate.py` | • `single_track`, `tf_estimate` 소문자 중복 별칭 삭제 |
| **`curve_fit`** | `combiner_estimator.py` | • `CurveCombiner = CombinerEstimator` 삭제 |
| | `optimize_estimator.py` | • `MinimizeEstimator`, `FitMinimizeOptimization` 삭제 |
| | `least_squares_estimator.py`| • `EstimatorMF = LeastSquaresEstimator` 삭제 |
| **`models`** | `bicycle_model.py` | • `calc_unit_yaw_rate`, `UnitYawRate`, `ObjectiveFunc_UnitYawRate` 등 6개 삭제 |
| | `magic_formula.py` | • `TireMagicFormula`, `tire_magic_formula`, `MagicFormula`, `calculate_Fx` 4개 삭제 |
| | `neural_net/fit_nn.py` | • `fit_nn = fitNN` 별칭 삭제 |
| **기타 도메인** | `gps`, `graphics`, `database`, `logger`, `uno_statistics`, `utils` | • `GPSProcessor`, `_Plotter_`, `SetCursorMode`, `func_load_plm`, `PROGRESS_BAR`, `WINDOW_HANDLER`, `get_statics_df`, `UNCERTAINTY`, `PLOT`, `CalRatio`, `Window_Error_MSG` 등 전수 삭제 |

### Phase 5. 최상위 루트 `unoUtil/__init__.py` 전면 슬림화
- **과거 호환 가상 리다이렉터 완전 제거**:
  - `_UnoUtilLegacyRedirectFinder`, `_EXACT_MAPPINGS`, `_PREFIX_MAPPINGS` (150줄+) 및 가상 모듈 바인딩(`sys.modules['unoUtil.vehicleTest']`, `sys.modules['unoUtil.convenienceFunction']` 등 120줄)을 **전면 삭제**.
- **순수 v2 Facade 구축 (단 180줄)**:
  - 12대 공식 도메인(`file_reader`, `vehicle`, `gps`, `signal_process`, `curve_fit`, `graphics`, `uno_statistics`, `utils`, `logger`, `models`, `ai`, `database`, `snow_condition`)과 각 도메인의 핵심 클래스/함수 표준 노출만 명료하게 수납.

### Phase 6. 비매뉴얼 보고서/백서 옵시디언 볼트 안전 이관
코드 저장소에는 1:1 파이썬 기술 매뉴얼만 격리 보존한다는 헌장(`GEMINI.md`)을 준수하여 보고서 형식을 볼트로 체계적 이관:
- **신규 이관**:
  - `curve_fit/tire_curve/tire_curve_pipeline_and_real_data_issues.md` (19KB 백서) $	o$ 볼트 `20_curve_fit/` 폴더에 **`25_실차_계측데이터_태생적_문제점과_8단계_통합파이프라인_백서.md`**로 정식 등록 및 통합 색인 연계 완료.
- **중복 문서 삭제**:
  - `TIRE_CURVE_FITTING_RESULT.md` (볼트 `40_NoABS_실측_VBB_타이어_커브피팅_검증보고서.md`에 기보존) $	o$ 코드 폴더에서 삭제.
  - `uno_statistics/uncertainty/docs/uncertainty_theory.md` (볼트 `04_Resources/23_측정_불확도_공학/10_측정불확도_완벽_이론_및_수학적_유도_가이드.md`에 기보존) $	o$ 코드 폴더에서 삭제.
  - `curve_fit/tire_curve/explain/README.md` $	o$ 코드 폴더에서 삭제.
- **결과**:
  - `unoUtil` 패키지 내부의 모든 81개 `.md` 파일은 **단 1개의 예외 없이 파이썬 모듈(`xxx.py`)과 1:1 대응되는 순수 기술 매뉴얼(`xxx.md`)만 완벽하게 격리 보존**됨.

---

## 📊 4. 최종 정합성 및 무결성 검증 결과

| 검증 항목 | 검증 스크립트 | 결과 | 비고 |
| :--- | :--- | :---: | :--- |
| **상대 참조 잔존 여부** | 전수 AST 및 정규식 스캔 | **0건 (완전 소멸)** | 전 패키지 `unoUtil.*` 절대 참조 유지 |
| **레거시 별칭 잔존 여부** | 32개 모듈 심볼 스캔 | **0건 (완전 소멸)** | 하위 호환 별칭 일체 배제, SSOT 달성 |
| **비매뉴얼 마크다운 잔존 여부** | 저장소 `.md` 파일 전수 조사 | **0건 (완전 소멸)** | 루트 2건(README, GEMINI) 외 81건 전수 1:1 매뉴얼 |
| **패키지 도메인 구조 무결성** | `example/test_structure_integrity.py` | **100% PASS** | 12대 공식 도메인 및 핵심 피팅 검증 통과 |
| **PEP 8 표준 및 함수 규격** | `example/test_pep8_all.py` | **100% PASS** | 7대 패키지 표준 인터페이스 전수 통과 |
| **독립 실행형 프로그레스바 데모** | `example/example_scan_dir_progressbar.py`| **100% PASS** | VBO 가상 스캔 및 프로그레스바 정상 렌더링 |

---

## 💡 5. 향후 운영 및 개발 가이드라인

1. **신규 모듈 개발 시 절대 참조 의무화**:
   - 패키지 내부의 모든 임포트는 반드시 `from unoUtil.<도메인>.<모듈> import ...` 형태의 명시적 절대 참조를 준수합니다.
2. **과도기 임시 별칭 작성 원천 금지 (Single Baseline Law)**:
   - 함수명이나 클래스명을 리팩토링할 때, 과거 이름을 보존하기 위한 별칭(`OldName = NewName`)을 덧붙이지 않고 호출부를 직접 일괄 수정하여 코드베이스의 단일 표준을 항상 유지합니다.
3. **기술 문서 격리 보존 원칙 철저 집행**:
   - 파이썬 소스 코드 폴더(`unoUtil/`) 내부에는 `*.py`와 1:1로 매핑되는 순수 기술 매뉴얼(`*.md`)만 작성합니다.
   - 프로젝트 진행 상황, 회의록, 수학 이론 백서 및 종합 분석 보고서는 반드시 옵시디언 볼트(`D:\00_obsidian`) 내의 지정된 위키 폴더에 단독 작성·관리합니다.

---

## 📜 6. 관련 문서 링크

- **마스터 대시보드**: [[00_unoUtil_모듈개발_대시보드]]
- **커브 피팅 보고서 통합 색인**: [[00_curve_fit_보고서_통합_색인]]
- **신규 이관 백서**: [[25_실차_계측데이터_태생적_문제점과_8단계_통합파이프라인_백서]]
- **측정불확도 이론 가이드**: [[10_측정불확도_완벽_이론_및_수학적_유도_가이드]]
