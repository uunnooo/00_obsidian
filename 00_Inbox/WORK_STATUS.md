# 📋 unoUtil v2.6 전사 전수 명명 표준화 및 물리 레거시 완전 퇴출 보고서 (WORK_STATUS)

**일자**: 2026-09-23  
**작업자**: Gemini CLI  
**주요 목표**: 전사 모듈 대상 역방향 별칭(`Standard = LEGACY`) 전수 제거, 물리적 `legacy/` 디렉터리 100% 영구 퇴출(Zero Physical Legacy), 하위 호환성 100% 가상 리다이렉션 검증 및 Obsidian Vault 실시간 미러 동기화

---

## 🎯 1. 주요 작업 내역 및 완결 사항

### 1) 역방향 별칭 및 레거시 명명 전수 점검 및 교정 (Zero Inversion)
- **`unoUtil.logger.logger`**:
  - `class LOGGER:` $\rightarrow$ 공식 `class Logger:` 정의로 정상화.
  - 역방향 별칭 `Logger = LOGGER`를 공식 하위 호환 매핑 `LOGGER = Logger`로 교정.
  - 전역 로거 타입 힌트 `Dict[str, Logger]` 정합성 확보.
- **`unoUtil.uno_statistics.uncertainty`**:
  - `class UNCERTAINTY:` $\rightarrow$ 공식 `class Uncertainty:` 정의.
  - `class PLOT:` $\rightarrow$ 공식 `class UncertaintyPlot:` 정의.
  - 하위 호환 매핑 `UNCERTAINTY = Uncertainty`, `PLOT = UncertaintyPlot` 정상 정렬.
- **`unoUtil.graphics.controls.cursor_mode`**:
  - `def SetCursorMode` $\rightarrow$ 공식 `def set_cursor_mode`로 선언. 하위 호환 별칭 `SetCursorMode = set_cursor_mode` 수립.
- **`unoUtil.graphics.plotters.pair_plot`**:
  - `def PairPlotCorrWithScatter` $\rightarrow$ 공식 `def plot_pair_corr_with_scatter`로 선언. 하위 호환 별칭 수립.
- **`unoUtil.graphics.plotters.surface_3d`**:
  - `def Regression3D` $\rightarrow$ 공식 `def calc_regression_3d`로 선언. 하위 호환 별칭 `Regression3D = calc_regression_3d` 수립.
- **`unoUtil.signal_process.fft.tf_estimate`**:
  - `def TFEstimate` $\rightarrow$ 공식 `def calc_tf_estimate`로 선언. 하위 호환 별칭 `TFEstimate = calc_tf_estimate` 수립.
- **`unoUtil.utils.window_msg`**:
  - `def Window_Error_MSG` $\rightarrow$ 공식 `def set_window_error_msg`로 선언. 하위 호환 별칭 `Window_Error_MSG = set_window_error_msg` 수립.
- **`unoUtil.ai.dynamic_model`**:
  - `TireMagicFormula` $\rightarrow$ `def calc_tire_magic_formula`, `UnitYawRate` $\rightarrow$ `def calc_unit_yaw_rate`, `ObjectiveFunc_UnitYawRate` $\rightarrow$ `def calc_objective_unit_yaw_rate`로 선언. 하위 호환 별칭 및 `unoUtil.ai.__init__.py` 익스포트 완결.
- **`unoUtil.file_reader.standard_channel_pattern`**:
  - `class Infor_Vehicle` $\rightarrow$ `InforVehicle`, `class Infor_SensorPosition` $\rightarrow$ `InforSensorPosition`, `class GPS` $\rightarrow$ `Gps`로 선언.
- **`unoUtil.vehicle.hndl_test`**:
  - `SP_CurveFit_RF` $\rightarrow$ `calc_curvefit_rf`, `SP_CurveFit_MF` $\rightarrow$ `calc_curvefit_mf`로 선언 및 하위 호환 매핑.

---

### 2) Zero Physical Legacy (물리 레거시 폴더 100% 영구 퇴출)
- 디스크 상에 잔존하던 물리적 `legacy/` 디렉터리 9개 전량을 `_archive/`로 안전 격리 퇴출:
  - `unoUtil/ai/legacy` $\rightarrow$ `_archive/ai_legacy`
  - `unoUtil/database/legacy` $\rightarrow$ `_archive/database_legacy`
  - `unoUtil/file_reader/legacy` $\rightarrow$ `_archive/file_reader_legacy`
  - `unoUtil/logger/legacy` $\rightarrow$ `_archive/logger_legacy`
  - `unoUtil/signal_process/curve_fit/CurveCombiner/legacy` $\rightarrow$ `_archive/curve_fit_legacy`
  - `unoUtil/signal_process/fft/legacy` $\rightarrow$ `_archive/fft_legacy`
  - `unoUtil/signal_process/post_process/legacy` $\rightarrow$ `_archive/post_process_legacy`
  - `unoUtil/vehicle/legacy` $\rightarrow$ `_archive/vehicle_legacy`
  - `unoUtil/vehicle/acc_brk/legacy` $\rightarrow$ `_archive/acc_brk_legacy`
- `unoUtil/convenienceFunction` 디렉터리 완전 격리 (`_archive/convenienceFunction`).
- `unoUtil` 패키지는 이제 **순수 v2 공식 10대 도메인 디렉터리만 물리적으로 유지**.
- 모든 레거시 임포트는 메모리 상의 `_UnoUtilLegacyRedirectFinder` 및 사전 바인딩된 `sys.modules` 가상 레이어에서 100% 무중단 라우팅 처리됨.

---

### 3) 대시보드 및 문서 규격 표준화 (Phase 4 & 5)
- `unoUtil/vehicle/acc_brk/00_VT_ACCBRK_대시보드.md` 파일명을 표준 소문자 스네이크케이스인 `00_vt_acc_brk_대시보드.md`로 공식 변경.
- `GEMINI.md` 및 마스터 가이드의 경로 참조 일괄 동기화.
- `robocopy /MIR` 실행을 통해 Obsidian Vault 내 삭제된 레거시 문서 자동 퍼지(Purge) 및 신규 문서 100% 동기화 완료.

---

## 🧪 2. 전수 검증 결과 (100% PASS)

1. **`test_structure_integrity.py` (구조 및 하위 호환성 36개 항목 검증)**:
   - 10대 차세대 도메인 임포트: **100% PASS**
   - 핵심 클래스/함수 정합성: **100% PASS**
   - 레거시 패키지/모듈 가상 브릿지: **100% PASS**
2. **`test_pep8_all.py` (PEP 8 표준 및 함수/클래스 전수 검증)**:
   - vehicle & ACCBRK: **PASS**
   - ai 패키지: **PASS**
   - signal_process: **PASS**
   - logger 패키지: **PASS**
   - database 패키지: **PASS**
   - file_reader 패키지: **PASS**
   - uno_statistics & utils 패키지: **PASS**
   - **종합 결과**: `[SUCCESS] unoUtil 전 패키지 PEP 8 표준화 & 하위 호환성 100% PASS!`
