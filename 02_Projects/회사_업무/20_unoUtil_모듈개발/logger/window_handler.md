# 🧭 window_handler PyQt5 기반 자동 팝업 경고 및 예외 알림 매뉴얼 (window_handler.md)

## 📌 1. 개요 및 목적 (Overview)
`window_handler` 모듈은 사내 실차 제동 분석 자동화 스크립트 실행 중 치명적인 에러나 의사결정이 필요할 때, **PyQt5 GUI 인터페이스를 활용하여 사용자 화면 중앙에 자동으로 팝업 메시지 박스를 띄우는 알림 핸들러 모듈(`show_window_msg`, `WindowMsgHandler`)**을 제공합니다.

자동화 파이프라인이나 배치 가감속 분석 툴을 기동할 때, 치명적인 파일 유실이나 위성 계측 음영 에러가 발생해도 콘솔 창에 텍스트만 흐르고 넘어가 버리면 사용자가 모른 채 퇴근하는 사고가 발생합니다. 
본 모듈은 Windows OS GUI 윈도우 매니저와 직접 결합하여 화면에 강력한 메시지 박스 경고를 뿜어주며, 디스플레이 서버가 없는 서버 백그라운드 환경(헤드리스 CLI)에서는 자동으로 감지하여 **안전하게 콘솔 표준 에러(stderr) 스트림 출력으로 다운그레이드 우회**하여 프로그램이 크래시되지 않도록 철저한 가드를 이중으로 제공합니다.

---

## 🛠️ 2. 핵심 API 명세 (API Specifications)

### 2.1. `WindowMsgHandler` 클래스 및 글로벌 함수 명세

| 메서드 / 함수명 | 타입 | 설명 |
| :--- | :---: | :--- |
| `show_window_msg(message, title, level)` | 글로벌 함수 | HTML 태그를 지원하는 정교한 메시지를 PyQt5 경고 창 또는 콘솔 표준 에러 스트림에 동적으로 표시 |
| `WindowMsgHandler` | 클래스 | Python logging 표준 모듈에 플러깅할 수 있는 자동 경고 팝업 로깅 핸들러 |
| `WindowMsgHandler.emit(record)` | 메서드 | 로그를 가로채어 로그 레벨이 설정값(기본: `ERROR` 이상)과 대조될 때, 자동으로 윈도우 중앙에 경고 팝업 메시지 창을 가동시킴 |

---

## 📋 3. 입력 파라미터 상세 정의 (Arguments)

1. **`message` (`str` - 필수)**:
   - 팝업 창 본문에 노출할 상세 에러 경고 메시지입니다. HTML 줄바꿈 태그(`<br>`) 및 볼드 처리를 완벽하게 지원합니다.
2. **`level` (`str` / `int` - 선택, 기본값: `'error'`)**:
   - 메시지의 심각성 수준을 나타냅니다. (`'info'`, `'warning'`, `'error'` 아이콘 테마가 팝업 창 왼쪽에 자동 바인딩됩니다.)

---

## 💻 4. 실무 활용 예제 (Multi-case Examples)

### 4.1. [시나리오 1] 제동거리 임계치 유실 에러 발생 시 사용자 화면에 즉각 QMessageBox PyQt5 팝업창 가동
```python
from unoUtil.logger.window_handler import show_window_msg

# 실차 평가 중 심각한 VBOX 파일 손상 감지 시나리오
try:
    raise FileNotFoundError("lane8_wet_braking_corrupted.vbo 파일의 내부 데이터 스트림이 유실되었습니다.")
except Exception as e:
    # 윈도우 화면 중앙에 경보 QMessageBox가 즉시 팝업 기동됨!
    show_window_msg(
        message=f"🚨 <b>실차 제동 분석 크래시 경보</b><br><br>상세 원인: {e}",
        title="Braking Pipeline Error",
        level="error"
    )
```

### 4.2. [시나리오 2] 파이썬 표준 로거와 결합하여 ERROR 로그 발생 시 자동 GUI 팝업 연동
```python
import logging
from unoUtil.logger.window_handler import WindowMsgHandler

# 1. 테스트 표준 로거 설정
custom_logger = logging.getLogger("Braking_System")
custom_logger.setLevel(logging.INFO)

# 2. QMessageBox 자동 연동 팝업 로깅 핸들러 플러깅!
popup_handler = WindowMsgHandler(level=logging.ERROR)
custom_logger.addHandler(popup_handler)

# 3. 비즈니스 로직 수행 중 에러를 로깅하기만 하면, 자동으로 QMessageBox가 사용자 화면을 깨우며 팝업됩니다.
custom_logger.error("VBOX 위성 수신 감도가 0.0 으로 유실되었습니다. 즉각 안테나 상태를 점검하십시오.")
```

### 4.3. [시나리오 3] 헤드리스(CLI Server / 가상환경) 환경에서의 무인 감쇄 콘솔 에러 대체 자동 검증
```python
# DISPLAY 서버가 없거나 PyQt5가 설치되지 않은 특수 헤드리스 가상 서버 환경이라고 가정
# show_window_msg 함수는 내부 예외 가드가 탑재되어 있어, GUI 로드가 안 되면 자동으로 안전하게 콘솔 sys.stderr로 대체 출력함!
show_window_msg(
    message="가상 서버 자동화 빌드 완료 보고",
    title="CI/CD Status",
    level="info"
)
print("🛡️ GUI 로드 불능 상태에서도 프로세스 정지나 크래시 없이 안전하게 에러 우회가 완결되었습니다.")
```
