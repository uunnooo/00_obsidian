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

1. **로컬 1:1 매뉴얼 필수화 및 예외**:
   * 파이썬 파일(`.py`)을 신규 생성하거나 대폭 리팩토링할 때, **반드시 동일 로컬 디렉토리 내에 동명의 마크다운 파일(`.md`)을 생성**하여 상세 API 스펙과 사용 예를 기록합니다. (예: `logger.py` $\leftrightarrow$ `logger.md`)
   * **🚨 예외 규정**: **`__init__.py` 및 임시/테스트 스크립트(`test_*.py`)는 1:1 마크다운 매뉴얼 작성 대상에서 명시적으로 제외합니다.** 이 파일들은 매번 동일한 이름으로 생성되어 중복과 폴더 비대화를 유발할 뿐 가독성에 전혀 도움이 되지 않기 때문입니다. 대신, 패키지-레벨의 진입점 API 노출이나 동적 임포트 리다이렉트 아키텍처 설명은 해당 폴더의 **상위 모듈 대시보드(00_*_대시보드.md)**에 통합 수록합니다.
2. **실시간 이중 동기화 폐지**: 개발하는 과정에서 매번 옵시디언 볼트에 실시간으로 쓰기 작업을 수행하지 않습니다.
3. **최종 완료 후 일괄 위키 승격 (Batch Sync)**: 전체 작업이 성공적으로 검증 완료되거나 사용자가 *"위키 정리해줘"* 라고 명시적으로 지시할 때 비로소 로컬 `.md` 문서들을 옵시디언 볼트(`02_Projects/회사_업무/20_unoUtil_모듈개발/...`)로 일괄 업서트(Upsert) 및 병합하고 당일 데일리 노트에 Audit Trail을 기록합니다.
4. **각 도메인 대시보드(MOC) 버전 이력 영구 기록 의무화**:
   * 단순 코드 수정뿐만 아니라, 해당 모듈이 속해 있는 각 서브패키지 폴더의 `00_*대시보드.md` 및 최상위 프로젝트 `00_unoUtil_모듈개발_대시보드.md` 하단에 반드시 **`## 📜 버전 이력 및 주요 개발 현황 (Changelog)`** 섹션을 신설 혹은 최신화하여 세션별 변경 내역을 영구히 남겨야 합니다.
   * 이로 인해 개발 장비가 바뀌거나 다른 컴퓨터에서 가상 보관소를 이어서 작업할 때도, 대시보드 히스토리 하나만으로 전체 패키지의 수렴 방향과 정합성 역사를 즉시 완벽하게 연계 파악할 수 있도록 보장합니다.
