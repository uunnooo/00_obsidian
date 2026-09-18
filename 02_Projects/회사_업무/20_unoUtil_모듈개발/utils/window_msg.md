# 🪟 utils.window_msg (Window Msg Helper)

## 1. 개요
`unoUtil.utils.window_msg` 모듈은 PyQt5 메시지 박스 또는 콘솔을 통해 경고 및 에러 메시지를 사용자에게 즉각 팝업/표시하는 편의 함수를 제공합니다.
과거 `unoUtil.convenienceFunction.WindowMsg`의 100% 하위 호환을 보장하며, 내부적으로 차세대 표준 로깅 시스템인 `unoUtil.logger.WindowHandler`와 연동됩니다.

---

## 2. 주요 기능 및 API

### `Window_Error_MSG(message: str, title: str = "Error") -> None`
- **설명**: 에러 메시지를 창(GUI) 또는 콘솔에 표시합니다.
- **Args**:
  - `message` (`str`): 표시할 에러 메시지 내용 (HTML 태그 `<br>` 지원).
  - `title` (`str`, optional): 메시지 박스 타이틀. 기본값은 `"Error"`.

```python
from unoUtil.utils.window_msg import Window_Error_MSG
# 또는 레거시 호환 경로
from unoUtil.convenienceFunction.WindowMsg import Window_Error_MSG

Window_Error_MSG("평가 데이터 파일이 손상되었습니다.", title="파일 로딩 에러")
```

---

## 3. 관련 문서
- [[unoUtil/logger/Logger|Logger 모듈 매뉴얼]]
- [[unoUtil/logger/WindowHandler|WindowHandler 매뉴얼]]
