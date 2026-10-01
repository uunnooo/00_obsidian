# 📋 WORK STATUS: unoUtil.vehicle.acc_brk v2 정식 표준화 및 로거 레벨 격리 완결

- **일시**: 2026-10-02
- **작업자**: uno & Gemini (Antigravity)
- **작업 도메인**: `c:\Users\uunnoo\PycharmProjects\unoUtil\unoUtil\vehicle\acc_brk` 및 `analyzers/` (18개 소스 파일 + 15종 기술 매뉴얼)

---

## 🎯 1. 작업 개요 및 핵심 목적

1. **사용자 요청 사항 100% 충족**:
   - `"우선 유노유틸에 acc_brk 폴더만 할거야.. 거기안에 있는 analyzers 까지... 무슨 말인지 알지?"` ➔ 작업 영역을 `unoUtil/vehicle/acc_brk` 및 `analyzers/`로 한정 집중.
   - `"print 키워드 인자를 다 없애줘 대신에 로거 레벨을 입력받아서.. 이걸 기준으로 보여주면 될것 같은데 어떻해 생각해?"` ➔ 모든 `print` 인자를 퇴출하고 `level: Union[int, str] = logging.DEBUG/INFO`로 전면 교체.
   - `"각 클래스 객체에 원래 로거 객체가 합쳐지나? 지금 보여준것처럼?"` ➔ 피클 직렬화 안전성을 위해 인스턴스에 로거 객체를 직접 보관하지 않고 `self._level` 정수만 유지하며 `@property def logger(self):` 동적 바인딩 채택.
2. **단일 기준 불변 원칙 (Single Baseline Law)**:
   - 과도기 파일 `cal_control.py` 및 `.md` 완전 영구 삭제, `correct.py`로 단일 SSOT 흡수.
   - v2 내부 상호 호출에서 구버전 대문자 심볼 전면 배제.
3. **메서드 접두사 중복 배제 (No Redundant Prefix Law)**:
   - `PlotterTire`, `PlotterProject`의 메서드에서 중복 `plot_` 접두사 제거 (`plotter.accbrk()`, `plotter.all()`, `compare_braking()` 등).
4. **표준 파라미터 네이밍 전면 정합**:
   - `df_raw`, `df_input` ➔ `data: pd.DataFrame`, `sr` ➔ `sample_rate`, `flag_print` ➔ `level`.
5. **대시보드 볼트 단독 관리 및 매뉴얼 1:1 미러링 헌장 (Vault-Only Dashboard Law)**:
   - 파이썬 소스 코드 폴더 내에 대시보드 파일 생성 원천 차단.
   - 15종 기술 매뉴얼을 옵시디언 볼트(`D:\00_obsidian\...`)로 1:1 복사 미러링.
   - 볼트 마스터 대시보드 상단 Changelog에 **v3.11** 단독 기록.

---

## 🛠️ 2. 상세 수정 내역

### 1) 로거 인스턴스 격리 (`unoUtil/logger/logger.py`)
- `Logger` 클래스 내부에서 `self._level`을 인스턴스 단위로 격리 보관.
- `log`, `info`, `debug`, `warning`, `error`, `critical`, `success`에 `self.level` 기준 인스턴스 격리 필터링 구현.

### 2) 기반 클래스 및 6대 서브 분석기 (`unoUtil/vehicle/acc_brk/`)
- **`base_memory.py`**: 부모 `self.test`의 `level` 자동 상속, `@property def logger(self):` 동적 바인딩.
- **`analyzers/an_acceleration.py`**: `AnAcceleration(..., level=None)`, `analysis(..., level=None)` 지원.
- **`analyzers/an_mu_drop.py`**: `AnMuDrop(..., level=None)`, `analysis(..., level=None)` 지원.
- **`analyzers/an_response.py`**: `AnResponse(..., level=None)`, `analysis(..., level=None)` 지원.
- **`analyzers/an_skewness.py`**: `AnSlipModeSkewness(..., level=None)`, `analysis(..., level=None)` 지원.
- **`analyzers/an_slip_pdf.py`**: `AnSlipPdf(..., level=None)`, `analysis(..., level=None)` 지원, MockTire 파라미터 `data` 표준화.
- **`analyzers/an_split_speed.py`**: `AnSplitSpeed(..., level=None)`, `analysis(..., level=None)` 지원.

### 3) 코어 분석 및 파사드 모듈
- **`vt_acc_brk_tire.py`**: `VTAccBrkTire.__init__(data=None, sample_rate=100, level=logging.DEBUG)`, 동적 `logger` 프로퍼티.
- **`vt_acc_brk_project.py`**: `VTAccBrkProject.__init__(name='', ref_kwd='c', level=logging.INFO)`, `save_pjt(..., level=None)`.
- **`plotter_tire.py` / `plotter_project.py`**: 불필요한 `if self.flag_print:` 분기를 `self.logger.info/debug`로 치환, `level` 인자 지원.
- **`func_acc_brk.py`**: `calc_acc_brk`, `calc_slip`, `calc_reference_corrected`에 `level` 인자 도입 및 내부 8곳의 `if flag_print:` 분기를 `func_logger.debug(...)`로 치환.
- **`correct.py`**: `cal_control.py` 함수(`find_reference_tire`, `reorder_columns`) 흡수 완료, `p_logger = getattr(project, "logger", logger)` 기반 일원화.
- **`vt_acc_brk.py`**: 파사드 함수에 `level: Union[int, str] = logging.INFO` 도입, `kwargs` 하위 호환 매핑.

---

## 🧪 3. 무결성 검증 결과 (Verification)

| 대상 스크립트 | 실행 모드 | 실행 결과 | 비고 |
| :--- | :--- | :---: | :--- |
| `scratch/run_acc_brk_focused_audit.py` | AST 기반 18개 파일 파라미터 전수 감사 | **통과 (0건 검출)** | `flag_print`, `df_input` 등 구버전 잔재 0건 (100% 클린) |
| `analyzers/an_acceleration.py` | 단독 실행 시뮬레이션 | **Code 0 통과** | 부트스트랩 및 로거 격리 확인 |
| `analyzers/an_mu_drop.py` | 단독 실행 시뮬레이션 | **Code 0 통과** | K-Means & Decision Tree 정상 동작 |
| `analyzers/an_response.py` | 단독 실행 시뮬레이션 | **Code 0 통과** | 0.05g~0.2g 감속 대역 반응 지연 연산 통과 |
| `analyzers/an_skewness.py` | 단독 실행 시뮬레이션 | **Code 0 통과** | 2D 왜도 오차 거리 및 요약 통과 |
| `analyzers/an_slip_pdf.py` | 단독 실행 시뮬레이션 | **Code 0 통과** | 4륜 KDE 확률밀도함수(PDF) 적산 통과 |
| `analyzers/an_split_speed.py` | 단독 실행 시뮬레이션 | **Code 0 통과** | 50km/h 기준 고/저속 분할 통과 |
| `vt_acc_brk_tire.py` | 단독 실행 시뮬레이션 | **Code 0 통과** | 3중 캐시 최적화 및 직렬화 안전성 통과 |
| `vt_acc_brk_project.py` | 단독 실행 시뮬레이션 | **Code 0 통과** | 4개 시나리오(Control, Factor, Range, Serialization) 전수 통과 |
| `func_acc_brk.py` | 단독 실행 시뮬레이션 | **Code 0 통과** | Scenario A, B, C, D 전원 통과 |
| `vt_acc_brk.py` | 단독 실행 시뮬레이션 | **Code 0 통과** | Case 1(단일 타이어), Case 2(다중 프로젝트), Case 3(보정) 전수 통과 |

---

## 📚 4. 1:1 기술 매뉴얼 및 볼트 동기화 현황

- **갱신된 1:1 기술 매뉴얼 15종**:
  - `base_memory.md`, `correct_factors.md`, `correct.md`, `func_acc_brk.md`
  - `plotter_project.md`, `plotter_tire.md`, `vt_acc_brk_project.md`, `vt_acc_brk_tire.md`, `vt_acc_brk.md`
  - `analyzers/an_acceleration.md`, `analyzers/an_mu_drop.md`, `analyzers/an_response.md`
  - `analyzers/an_skewness.md`, `analyzers/an_slip_pdf.md`, `analyzers/an_split_speed.md`
- **옵시디언 볼트 동기화**: `D:\00_obsidian\02_Projects\회사_업무\20_unoUtil_모듈개발\vehicle\acc_brk`로 15종 1:1 복사 완료.
- **볼트 마스터 대시보드 Changelog**: `00_unoUtil_모듈개발_대시보드.md` 상단에 **v3.11** 등록 완료.
