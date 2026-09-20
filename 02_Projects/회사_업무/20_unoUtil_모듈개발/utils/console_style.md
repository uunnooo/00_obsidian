---
id: "console_style_20260920"
title: "console_style (터미널 ANSI 스타일 및 유니코드 표준화) 상세 매뉴얼"
type: resource
category_main: 회사_업무
category_sub: 개발매뉴얼
date: 2026-09-20
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - 유틸리티
  - 콘솔
  - 매뉴얼
project_link: "[[unoUtil]]"
---

# 🎨 console_style (터미널 ANSI 스타일 및 유니코드 표준화) 상세 매뉴얼

> [!ABSTRACT] 📌 개요
> 사용자 터미널 환경(CMD, PowerShell, VSCode, PyCharm, Linux 셸 등)의 가상 콘솔 활성화 모드와 이모지 인코딩 지원 가능 여부를 실시간 자동 분석하여, 색상 코드 및 진행률 이모지 기호를 일반 문자열과 완벽 교차 대체하는 스타일 표준화 모듈입니다.
> 
> * **상위 대시보드**: [[00_utils_대시보드]] | [[00_unoUtil_모듈개발_대시보드]]

---

## 1. ⚙️ 주요 API 규격

### 1.1. `check_supports_color() -> bool`
* **기능**: 터미널의 ANSI 가상 터미널 프로세싱 및 글자 색상 출력 지원 유무를 정밀 분석합니다. PyCharm 및 VSCode 터미널 등은 가용한 것으로 자동 판별하며, 구형 CMD의 경우 Windows API 커널(`kernel32.dll`)을 직접 호출해 가상 콘솔 모드(`ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004`)를 자동 활성화시킵니다.

### 1.2. `check_supports_unicode() -> bool`
* **기능**: 이모지(📅, ✅, 🚨 등)가 깨짐 없이 정상 출력될 수 있는 시스템 인코딩(`utf-8`) 상태인지 판별합니다. cp949/euc-kr 등 멀티바이트 유니코드 인코딩 불능 환경인 경우 `False`를 자동 반환합니다.

### 1.3. `CONSOLE` 네임스페이스 속성 제공
* **기능**: 스타일 상수들을 속성 형태로 접근 가능한 싱글톤 클래스 래퍼입니다.
  - **색상/스타일**: `STR_CLR_RED`, `STR_CLR_GREEN`, `STR_CLR_YELLOW`, `STR_CLR_BLUE`, `STR_CLR_END`, `STR_STY_BOLD`, `STR_STY_UNDERLINE` 등.
  - **기호 (유니코드 대응)**: `STR_CHR_DONE` (✅ / `[DONE]`), `STR_CHR_ERROR` (🚨 / `[ERROR]`), `STR_CHR_CALENDAR` (📅 / `[DATE]`) 등.

---

## 💻 2. 호출 예제 (Usage Example)

```python
from unoUtil.utils.console_style import CONSOLE, STR_CLR_GREEN, STR_STY_BOLD, STR_CLR_END, STR_CHR_DONE

# 1. ANSI 색상 및 유니코드 문자 조합 스타일 출력
message = f"{STR_STY_BOLD}{STR_CLR_GREEN}{STR_CHR_DONE} 작업이 완벽히 검증 완료되었습니다!{STR_CLR_END}"
print(message)

# 2. CONSOLE 네임스페이스 활용 (가변적 문자열 대응)
if CONSOLE.BOOL_SUPPORTS_COLOR:
    print(f"{CONSOLE.STR_CLR_RED}에러가 검출되었습니다!{CONSOLE.STR_CLR_END}")
else:
    print(f"{CONSOLE.STR_CHR_ERROR} 에러가 검출되었습니다!")
```
