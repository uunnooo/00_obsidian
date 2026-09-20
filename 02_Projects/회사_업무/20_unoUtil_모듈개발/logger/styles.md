# 🧭 ColoredFormatter ANSI 감쇄 콘솔 컬러 로깅 모듈 매뉴얼 (styles.md)

## 📌 1. 개요 및 목적 (Overview)
`styles` 모듈은 주행 시험 및 분석 자동화 스크립트의 실행 추적을 돕기 위해, **터미널 환경(Windows CMD, PowerShell, PyCharm, Linux 등)을 자동 감지하여 최적의 ANSI 16컬러 스타일, 유니코드 이모지, 그리고 실시간 경과 시간 및 직전 로그 대비 시간 차이(Delta, $\Delta t$)를 조합하여 렌더링하는 고성능 컬러 로그 포매터 클래스(`ColoredFormatter`)**와 ANSI 코드를 제거해 주는 유틸리티 함수들을 제공합니다.

가혹한 데이터 연산 로그를 단순 백색 텍스트로만 출력하면 중요 경고나 예외 발생 시 가독성이 저하됩니다. 
본 모듈은 터미널의 유니코드 및 ANSI 색상 지원도를 지능적으로 자동 판별하여, 색상이 지원되지 않는 구버전 콘솔이나 **텍스트 파일 출력 시에는 ANSI 제어 문자들을 자동으로 깨끗이 날려주는 감쇄 포맷터(Ansi Stripper)** 능력을 완벽히 실현하고 있습니다.

---

## 🛠️ 2. 핵심 API 명세 (API Specifications)

### 2.1. `ColoredFormatter` 클래스 및 글로벌 헬퍼 함수 명세

| 메서드 / 함수명 | 타입 | 설명 |
| :--- | :---: | :--- |
| `check_supports_color()` | 글로벌 함수 | 터미널 환경변수와 플랫폼 정보(Windows 버드 등)를 역추적하여 ANSI 컬러 스타일링 출력 가능 유무 감지 |
| `check_supports_unicode()` | 글로벌 함수 | 유니코드 특수문자 및 유니코드 이모지 기호가 깨짐 없이 정상 출력될 수 있는지 감지 |
| `strip_ansi(text)` | 글로벌 함수 | 로그 파일 저장 시 텍스트가 깨져 보이지 않도록 문자열 내부의 모든 ANSI 제어 이스케이프 문자열을 정규식으로 완벽히 소거 |
| `ColoredFormatter` | 클래스 | 파이썬 로깅 모듈에 장착할 수 있는 고성능 ANSI 컬러/이모지/시간차 델타 로그 포매터 |
| `ColoredFormatter.format(record)` | 메서드 | 로그를 가로채어 레벨에 맞춰 컬러화하고, 프로그램 기동 후 누적된 경과 시간 및 직전 로그 호출 시점과의 미세 시차 델타 시간을 자동으로 계산해 덧붙여 반환 |

---

## 📋 3. 입력 파라미터 상세 정의 (Arguments)

1. **`use_color` (`bool` - 선택, 기본값: 자동 판별)**:
   - ANSI 컬러 코드 적용 여부입니다. `False` 일 경우 컬러 코드가 완전히 스키핑되어 순수 플레인 텍스트만 출력됩니다.
2. **`show_delta` (`bool` - 선택, 기본값: `True`)**:
   - 직전 로그가 출력된 시점으로부터 현재 로그가 찍히기까지 소요된 미세 시차 시간(예: `+0.045s`)을 로그 접두사에 자동으로 덧붙여 보여줄지 여부입니다.

---

## 💻 4. 실무 활용 예제 (Multi-case Examples)

### 4.1. [시나리오 1] 파이썬 표준 로깅에 ColoredFormatter를 장착하여 가독성 높은 실시간 컬러 로그 출력
```python
import logging
import sys
from unoUtil.logger.styles import ColoredFormatter

# 1. 전역 로거 및 스트림 핸들러 정의
logger = logging.getLogger("Acc_Braking")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)

# 2. 명품 컬러 포매터 장착 (컬러 지원, 경과 시간 표시, 델타 시차 표시 ON)
formatter = ColoredFormatter(
    use_color=True,
    show_time=True,
    show_elapsed=True,
    show_delta=True
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# 3. 로그 출력 기동
logger.info("VBOX ASCII 계측 로그 파일 스캔을 시작합니다.")
logger.warning("Warning: GPS signal quality is slightly fluctuating")
```

### 4.2. [시나리오 2] 파일로 로그를 저장할 때 strip_ansi를 기동하여 깨끗한 텍스트 파일 저장
```python
from unoUtil.logger.styles import strip_ansi

# ANSI 제어 문자(색상 정보)가 섞인 로깅 텍스트 가상 데이터
colored_raw_log = "\x1b[32m[SUCCESS]\x1b[0m 7대 킬러 모듈 전수 마이그레이션이 완료되었습니다."

# 이 텍스트를 그대로 메모장이나 파일에 쓰면 '^[32m' 등의 깨진 제어 코드가 나타납니다.
# strip_ansi로 정규식 소거 처리를 가합니다.
plain_cleaned_log = strip_ansi(colored_raw_log)

print(f"📄 원본 로그: {colored_raw_log}")
print(f"🧹 파일 저장용 텍스트: {plain_cleaned_log}")
# Output: [SUCCESS] 7대 킬러 모듈 전수 마이그레이션이 완료되었습니다.
```

### 4.3. [시나리오 3] 터미널 유니코드 및 이모지 출력 지원도 오토 체크
```python
from unoUtil.logger.styles import check_supports_color, check_supports_unicode

supports_ansi = check_supports_color()
supports_emoji = check_supports_unicode()

print(f"⚙️ 현재 터미널 분석 스냅샷:")
print(f"  - ANSI 컬러 가동 유무: {supports_ansi}")
print(f"  - 이모지 이모티콘 기호 가동 유무: {supports_emoji}")
```
