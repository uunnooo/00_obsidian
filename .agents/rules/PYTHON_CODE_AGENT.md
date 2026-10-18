# 🧭 unoUtil 파이썬 코드 품질 및 개발 표준 마스터 규칙 (PYTHON_CODE_AGENT.md)

이 문서는 `unoUtil`을 비롯하여 사용자가 개발하는 모든 파이썬 프로젝트에서 코드 작성, 수정, 리팩토링 및 로컬 문서화 작업을 수행할 때 AI 에이전트(Gemini-CLI, agy 등)가 반드시 준수해야 하는 최상위 공통 엔지니어링 표준 법률입니다.

---

## 1. 🛡️ 핵심 엔지니어링 5대 원칙

1. **치명적 에러 무관용 (Zero Fatal Errors)**: 문법 에러, 런타임 예외, 미해제 파일 스트림(파일 락킹), 직렬화/역직렬화 실패는 발견 즉시 수정합니다.
2. **리포트 우선 승인 (Report-First Approval)**: 구조 변경 및 대규모 리팩토링 착수 전, 반드시 [점검 레포트]를 작성하여 사용자 승인을 득한 후 수정에 들어갑니다.
3. **극강의 닥스트링 및 타입 힌팅 표준**:
   * 모든 공개 함수/클래스에 Type Hinting(PEP 484)과 Google Style Docstring을 100% 기술합니다.
   * **`Args` 섹션에 `**kwargs`가 구버전의 어떤 레거시 헝가리안 인자(예: `df_input`, `str_col` 등)를 흡수하여 내부 변수로 포워딩하는지 반드시 상세 설명합니다.**
   * **`Examples` 섹션에 사용법을 직관적으로 복사해서 즉시 리마인드할 수 있는 예제 코드 블록(`>>>` doctest 스타일)을 필수로 기재합니다.**
4. **다변화 자가 구동 예제 (# region 구획)**:
   * 파일 하단에 외부 의존성(외부 파일, 데이터베이스) 없이 즉시 단독 구동 가능한 Mock 데이터 기반 검증 스위트를 구성합니다.
   * **단순 성공 케이스뿐만 아니라, 다양한 키워드 인자 조건, 입력 파라미터 변경 환경, 다형성 save 경로 분기 등 '최소 3개 이상의 다변화된 시나리오'를 예제 함수 형태로 구현하여 자가 구동하도록 만듭니다.**
5. **시각화 무중단(Non-blocking) 원칙**: Matplotlib 시각화 시 `plt.show()` 호출을 전면 금지하며, `plt.savefig()` 후 `plt.close(fig)` 처리합니다.
6. **진행률 바 터미널 렌더링 무결화 원칙**: 터미널 가로폭 초과로 인한 줄바꿈 잔상 오동작을 원천 방어하기 위해 프로그레스 바 출력 시 자동 개행 방지 시퀀스(\033[?7l, \033[?7h)를 적용하고, 전각 문자 비주얼 너비 계산 및 색상 누출 방지(STR_CLR_END 강제 추가) 표준을 의무 적용합니다.

---

## 2. 🛑 시각화 무중단 및 `save` 다형성 처리 표준

### 2.1. Non-blocking 시각화 아키텍처
배치 데이터 파이프라인과 백그라운드 태스크가 멈추는 현상(Hang)을 차단하기 위해, 모든 시각화 함수는 **"파일 저장 (`savefig`) → 메모리 해제 (`close`) → Figure 객체 반환"** 패턴을 의무화합니다.

### 2.2. 다형성(Polymorphism) `save` 파라미터 제어
모든 시각화 및 데이터 저장 인자인 `save`는 `Union[bool, str, Path]` 다형성을 수용하며, 아래 템플릿에 맞추어 완벽하게 분기 처리합니다:
1. `save = False` 또는 `None`: 파일 저장 프로세스 생략.
2. `save = True`: 미리 지정된 사내 디폴트 폴더에 디폴트 파일명으로 자동 저장.
3. `save = 디렉토리 경로 (str/Path)`: 해당 디렉토리 폴더 내부에 디폴트 파일명으로 저장.
4. `save = 파일 경로 (str/Path)`: 지정된 전체 경로 및 파일명 그대로 저장.

---

## 3. 🔤 초정밀 5대 네이밍 헌장 (Naming Conventions)

### 3.1. 표준 명명 체계
* **모듈 / 파일명**: `snake_case` (소문자+언더바) 조합 (예: `vt_acc_brk.py`)
* **클래스명**: `PascalCase` 조합 (예: `VTAccBrk`, `FileDataReader`)
* **함수명**: `snake_case` 조합이며, 반드시 아래 **8대 표준 동사 접두사** 중 하나로 시작합니다.
  1. `load_`: 파일 또는 외부 DB에서 단순히 로드할 때 (`load_plm()`)
  2. `read_`: 이기종 계측 장비 파일을 파싱하여 읽을 때 (`read_data_file()`)
  3. `save_`: 메모리 내 결과물을 물리 디스크에 영구 저장할 때 (`save_as_custom_excel()`)
  4. `calc_`: 물리적/수학적 알고리즘으로 수치/통계 지표를 계산할 때 (`calc_performance()`)
  5. `get_`: 객체 내부의 속성값, 요약 통계를 단순 조회할 때 (`get_statistics_df()`)
  6. `find_`: 시계열 데이터 내에서 특정 이벤트, 트리거 구간을 탐색할 때 (`find_reference_tire()`)
  7. `plot_`: 차트 및 리포트 시각화 객체를 생성할 때 (`plot_braking_profile()`, 반드시 `return fig, ax`)
  8. `set_`: 인스턴스의 설정값, 옵션을 지정할 때 (`set_cursor_mode()`)
* **🚨 클래스 역할 내포 시 메서드 접두사 중복 방지 원칙 (No Redundant Prefix Law)**:
  - `Plotter`, `PlotterTire`, `PlotterProject`, `Reader`, `Writer` 등 **클래스명 자체에 이미 특정 행위나 역할(동사적 의미)이 명확히 담겨 있는 경우, 내부 메서드에 동일한 동작 접두사(`plot_`, `read_`, `save_` 등)를 강제로 덧붙이지 않습니다.**
  - **사유**: `plotter.plot_accbrk()`, `plotter.plot_compare_braking()` 처럼 호출하면 클래스명과 메서드명이 불필요하게 중복되어(`plotter.plot_...`) 객체지향적 문맥(Context)에서 매우 부자연스럽고 가독성을 해칩니다.
  - **적용 기준**:
    - 시각화 전담 클래스(`PlotterTire`, `PlotterProject` 등) 내부 메서드는 `plotter.accbrk()`, `plotter.acceleration()`, `plotter.compare_braking()` 처럼 **대상(목적어) 또는 차별화된 세부 행위만 명료하게 기술**합니다.
    - 분석 전담 클래스(`AnAcceleration`, `AnResponse` 등) 내부 메서드는 `analysis()` 또는 `run()` 등 도메인 고유의 자연스러운 호출 규격을 유지합니다.
  - **8대 동사 접두사 의무 대상**: 일반 모듈 레벨 전역 함수(예: `calc_mfdd()`, `find_reference_tire()`) 및 다목적 서비스 클래스(예: `VehicleDynamic.align_coordinate()`, `VehicleDynamic.calc_side_slip_angle()`)에서는 8대 표준 동사를 엄격히 준수합니다.
* **입력 인자(Parameters)**: 헝가리안 표기법을 완전히 배제하고 직관적인 단어형 소문자 인자 사용. (예: `data`, `target_col`, `print_log=True`, `plot=False`, `save=True`, `close=True`)
* **내부 변수(Internal Variables)**: 사내 공통 도메인 변수 사전 단어로 통일. (예: `data`, `work_data`, `result`, `fig`, `ax`)

### 3.2. 레거시 파라미터 흡수 (`**kwargs` Absorption Pattern)
구버전 스크립트와의 호환성을 위해 함수 내부 상단에 `**kwargs` 자동 매핑 블록을 반드시 구현합니다:
```python
# 구버전 df_input, flag_print 인수 자동 흡수 예시
if data is None and "df_input" in kwargs:
    data = kwargs["df_input"]
if "flag_print" in kwargs:
    print_log = kwargs["flag_print"]
```

---

## 4. 🏗️ 파이썬 파일의 5단계 표준 아키텍처 및 자가 구동 템플릿

모든 모듈 파일은 예외 없이 다음 5단계 구조로 작성됩니다.

```python
# 1단계: 모듈 헤더 & 메타데이터 (Module-level Docstring)
"""
Module: vt_acc_brk_project
Description: 실차 가감속 시험 데이터를 취합하고 선형 보정을 수행합니다.
Date: YYYY-MM-DD
"""

# 2단계: 임포트 영역 (PEP 8 순서 정렬 및 unoUtil 최우선 재사용)
import os
from pathlib import Path
from typing import Optional, Union, Tuple, Any
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from unoUtil.logger import LOGGER                       # 사내 표준 로거 재사용
from unoUtil.graphics.plotters import format_fig        # 시각화 스타일 재사용

# 3단계: 전역 상수 및 설정
DEFAULT_SAVE_DIR = Path("D:/00_obsidian/_attachments/10_회사_업무")

# 4단계: 핵심 비즈니스 로직 (Core Classes & Functions)
def calc_something(data: pd.DataFrame, **kwargs) -> pd.DataFrame:
    # (핵심 비즈니스 로직 구현 및 kwargs 흡수...)
    pass

# 5단계: # region 자가 구동 및 다변화 검증 스위트 (Multi-case Test Suite)
# region Test Suite
if __name__ == "__main__":
    LOGGER.info("🚀 모듈 자가 구동 다변화 테스트를 시작합니다.")
    
    # 공통 Mock 데이터 세팅
    mock_df = pd.DataFrame({"Velocity": np.linspace(100, 0, 100)})
    
    # [시나리오 1] 기본 호출 및 콘솔 출력 검증
    LOGGER.info("--- [시나리오 1] 기본 성능 계산 및 로그 출력 검증 ---")
    res_1 = calc_something(data=mock_df)
    
    # [시나리오 2] 시각화 및 디폴트 자동 저장(save=True) 검증
    LOGGER.info("--- [시나리오 2] 시각화 및 디폴트 폴더 자동 저장 검증 ---")
    res_2 = calc_something(data=mock_df, plot=True, save=True, close=True)
    
    # [시나리오 3] 커스텀 파일 저장 및 구버전 레거시 인자(kwargs) 흡수 검증
    LOGGER.info("--- [시나리오 3] 커스텀 저장 경로 및 레거시 인자 호환 검증 ---")
    custom_path = Path("./test_output/custom_chart.png")
    res_3 = calc_something(df_input=mock_df, plot=True, save=custom_path, close=True)
    
    LOGGER.info("✅ 모든 다변화 시나리오 자가 구동 테스트 완료! (Code 0)")
# endregion
```

---

## 📚 5. 문서화 및 완료 후 배치 동기화(Batch Sync) 표준

### 5.1. 🏛️ 대시보드 볼트 단독 관리 및 매뉴얼 미러링 헌장 (Vault-Only Dashboard Law)
1. **대시보드 및 버전/작업 이력 관리 (`00_*_대시보드.md`, Changelog)의 볼트 단독 관리 (Vault-Only SSOT)**:
   * 각 도메인 대시보드(`00_*_대시보드.md`) 및 최상위 프로젝트 대시보드(`00_unoUtil_모듈개발_대시보드.md`)는 **오직 옵시디언 볼트(`D:\00_obsidian\02_Projects\회사_업무\20_unoUtil_모듈개발\...`)에서만 생성, 갱신, 관리**합니다.
   * **사유 (크로스 디바이스 동기화)**: 사용자가 여러 대의 컴퓨터(회사 데스크톱, 노트북, 외부 작업 PC 등)를 이동하며 작업을 수행할 때, **옵시디언 볼트가 실시간 클라우드 동기화망을 통해 항상 단일 최신 상태를 유지**합니다. 만약 소스 코드 폴더(`unoUtil/`) 내부에 대시보드와 버전 이력이 존재하면, 컴퓨터 간 Git 커밋/풀 시점 불일치로 인해 버전 이력이 역전되거나 충돌(conflict)이 발생하므로 이를 원천 차단합니다.
   * **파이썬 모듈 폴더(`unoUtil/`) 내 대시보드 생성 절대 금지**: 소스 코드 디렉토리 내부에는 어떠한 `00_*_대시보드.md`도 생성하거나 복사해 두지 않습니다.
2. **수정 이력, 작업 현황, 버전 관리의 볼트 단일 기준 불변 원칙 (Vault Master Baseline Law)**:
   * **수정 이력(Changelog), 작업 진행 현황(Status), 공식 버전(Version Tag)의 절대적인 단일 판정 기준(SSOT)은 오직 옵시디언 볼트**입니다.
   * "현재 모듈이 몇 버전이고 어디까지 개발되었는가?"는 소스 코드 주석이나 로컬 파일 타임스탬프가 아닌, **오직 볼트 내 대시보드 상단의 `Changelog 타임테이블`에 적힌 기록만을 진실로 인정**합니다.
   * 에이전트는 작업 착수 시 가장 먼저 볼트의 대시보드를 읽어 현재 버전과 히스토리를 파악해야 하며, 작업 완료 시 버전 승격(v2.x $\rightarrow$ v3.x)과 세부 내역 기록 역시 볼트 대시보드에 최우선적으로 단독 기록합니다.
3. **파이썬 모듈 폴더의 파일 구성**:
   * 파이썬 모듈 폴더에는 순수 파이썬 코드(`*.py`)와 함수/클래스 단위의 **1:1 기술 매뉴얼(`xxx.md`)만** 보관합니다.
4. **개별 코드 매뉴얼 격리 보존 원칙 (Code Manual Isolation Law)**:
   * 개별 모듈/클래스 단위의 1:1 기술 매뉴얼(`xxx.md`)은 **코드 저장소(`unoUtil/`) 내부에서 소스 코드와 함께 단일 관리(SSOT)**합니다.
   * **옵시디언 볼트로 개별 1:1 매뉴얼을 복사/미러링하는 행위를 원천 금지**합니다. (옵시디언 볼트 오염 방지 및 이중 유지보수 부채 제거)
   * 옵시디언 볼트에는 오직 전체 시스템 아키텍처, 버전 이력(Changelog)을 총괄하는 **단일 마스터 대시보드(`00_*_대시보드.md`)**, **모듈 도메인 사전(`[모듈명]_사전.md`)**, **핵심 도메인 공학 지식(`04_Resources/`)**, **종합 기술 분석 보고서**만 보관합니다.
5. **모듈 도메인 지식 사전 볼트 의무화 원칙 (Module Domain Dictionary Law)**:
   * 소스 코드 폴더 내부의 1:1 API 기술 매뉴얼(`xxx.md`)과 달리, 옵시디언 볼트의 전용 서브폴더(**`02_Projects/회사_업무/20_unoUtil_모듈개발/10_도메인_지식_사전/`**)에는 각 도메인 모듈의 설계 철학, 아키텍처, 데이터 파이프라인, 실무 종합 워크플로우를 집대성한 **`[모듈명]_사전.md`** 문서를 의무적으로 작성하고 최신화합니다.
   * **배경 지식의 원자화 및 링크 연동 (Knowledge Atomization)**: `[모듈명]_사전.md` 작성 시 등장하는 물리/수학 공식, 알고리즘, 공학 이론 등 독립적으로 재사용 가능한 지식은 볼트의 `04_Resources` 하위에 별도의 지식 노트로 분리 생성하고, 사전 문서에서는 위키링크(`[[...]]`)로 연결합니다. 이미 존재하는 리소스가 있다면 적극적으로 검색하여 연결합니다.
   * **향후 모듈 개발 시 필수 적용 (Mandatory for Future Modules)**: 앞으로 새롭게 개발되거나 대대적으로 개편되는 모든 unoUtil 도메인 모듈은 소스 코드 매뉴얼 작성과 병행하여 반드시 볼트 내 `10_도메인_지식_사전/[모듈명]_사전.md`를 템플릿(`_System/Templates/💻 unoUtil_모듈_사전_템플릿.md`)에 따라 작성/갱신해야 합니다.

### 5.2. 세부 문서화 지침
1. **로컬 1:1 매뉴얼 필수화 및 예외**:
   * 파이썬 파일(`.py`)을 신규 생성하거나 대폭 리팩토링할 때, **반드시 동일 로컬 디렉토리 내에 동명의 마크다운 파일(`.md`)을 생성**하여 상세 API 스펙과 사용 예를 기록합니다. (예: `logger.py` $\leftrightarrow$ `logger.md`)
   * **🚨 예외 규정**: **`__init__.py` 및 임시/테스트 스크립트(`test_*.py`)는 1:1 마크다운 매뉴얼 작성 대상에서 명시적으로 제외합니다.** 이 파일들은 매번 동일한 이름으로 생성되어 중복과 폴더 비대화를 유발할 뿐 가독성에 전혀 도움이 되지 않기 때문입니다. 대신, 패키지-레벨의 진입점 API 노출이나 동적 임포트 리다이렉트 아키텍처 설명은 볼트 내 해당 폴더의 **상위 모듈 대시보드(00_*_대시보드.md)**나 **모듈 사전([모듈명]_사전.md)**에 통합 수록합니다.
2. **옵시디언 볼트 유입 배제**: 개별 1:1 `.md` 매뉴얼은 코드 저장소 내에 머물며, 옵시디언 볼트로 복사하지 않습니다.
3. **모듈 사전 및 배경 지식 분리 생성 절차**:
   * 모듈 개발 또는 업데이트 완료 시, 에이전트는 `_System/Templates/💻 unoUtil_모듈_사전_템플릿.md` 규격을 준수하여 `02_Projects/회사_업무/20_unoUtil_모듈개발/10_도메인_지식_사전/[모듈명]_사전.md`를 생성/업데이트합니다.
   * 문서 작성 도중 도출되는 핵심 물리/수학 공식이나 공학 알고리즘은 `04_Resources/` 내 관련 도메인 하위에 원자적 지식 노트로 분리 생성하고 상호 링크를 구성합니다.
4. **최종 완료 후 대시보드 및 데일리 승격**: 전체 작업이 성공적으로 검증 완료되거나 사용자가 *"위키 정리해줘"* 라고 명시적으로 지시할 때, 볼트의 마스터 대시보드(`00_*_대시보드.md`) 상단 타임테이블(Changelog)을 업데이트하고 당일 데일리 노트에 Audit Trail을 기록합니다.
5. **대시보드 작성 및 업데이트 시 초반부 타임테이블 관리 의무화**:
   * 볼트 내 각 도메인 대시보드(`00_*대시보드.md`) 및 프로젝트 대시보드를 **새로 작성하거나 업데이트할 때, 문서 초반부(상단부)에 반드시 작업 내용에 대한 타임테이블(Changelog)이 포함**되어야 하며, 이 테이블을 통해 진행 상황과 모든 작업 내용의 히스토리를 정교하게 누적 관리해야 합니다.
   * 대시보드 진입 즉시(맨 앞부분에서) 타임테이블 형태로 작업 이력을 확인할 수 있게 함으로써, 개발 환경이 바뀌거나 세션이 달라져도 전체 프로젝트의 진행 경과와 수렴 방향, 정합성 역사를 즉시 추적할 수 있도록 보장합니다.
6. **임시 작업상태 파일(`WORK_STATUS.md` 등) 폴더별 생성 원천 금지 (No Standalone Status Files Law)**:
   * 사용자가 *"작업 정리해줘"*, *"위키 업데이트해줘"*, *"진행상황 요약해줘"* 라고 지시할 때, 프로젝트나 하위 소스 폴더에 `WORK_STATUS.md`, `*_work_status.md`, `작업정리.md` 등의 임시 마크다운 파일을 **절대로 별도로 새로 생성하지 않습니다.**
   * 모든 작업 진행 상황, 수정 내역, 트러블슈팅 결과는 볼트 내 해당 모듈/프로젝트의 마스터 대시보드(`00_*_대시보드.md`)의 **`## 📅 1. 프로젝트 주요 버전 이력 (Changelog 타임테이블)` 및 관련 본문 섹션에 직접 업데이트(Upsert)**하여 단일 진실 공급원(SSOT) 원칙을 유지합니다.

---

## 6. 🎯 unoUtil v2 개발 및 하위 호환성 단일 기준 불변 원칙 (Single Baseline Law)

1. **호환성의 기준은 오직 'v1 (구버전 오리지널 레거시)'이다**:
   * 하위 호환성(Backward Compatibility)은 오직 사내에서 실제로 배포/운영되던 v1 오리지널 레거시 코드(`unoUtil.vehicleTest.*`, `_AnalysisTestData_`, `_HndlTest_`, `_TEST_INFOR_RES_` 등)만을 대상으로 보장합니다.
2. **v2 과도기적 미완성 코드의 레거시 취급 원천 금지**:
   * 현재 진행 중인 작업은 "아직 완성되지 않은 v2를 정식 표준 규격으로 마무리(Finalize)하는 작업"입니다.
   * v2를 개발/리팩토링하는 과정에서 임시로 생성되었거나 표준에 맞지 않던 과도기적 중간 명칭, 파라미터, 임시 파일들을 '보존해야 할 레거시'로 착각하여 불필요한 별칭(Alias), 브릿지 파일, 중복 래퍼를 계속 덧붙이는 행위를 엄격히 금지합니다. (작업의 무한 증식 방지)
3. **직교적이고 깔끔한 v2 단일 표준 완성**:
   * v2 내부의 모든 모듈, 클래스, 메서드, 파라미터는 본 규격(PascalCase, 8대 표준 동사, 비차단 시각화, 도메인 표준 변수명)에 맞추어 단일 진실 공급원(SSOT) 형태로 깨끗하고 직교적으로 정비합니다.

