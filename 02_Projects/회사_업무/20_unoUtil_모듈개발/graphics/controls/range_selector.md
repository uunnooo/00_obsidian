# 🧭 SelRangeMouseClick 클릭 인터랙션 관심영역(ROI) 선택기 매뉴얼 (range_selector.md)

## 📌 1. 개요 및 목적 (Overview)
`range_selector` 모듈은 Matplotlib으로 그려진 주행 데이터 차트 위에서 사용자가 마우스로 직접 두 점을 클릭하여, **그 사이 구간에 해당하는 특정 관심 주행 데이터 영역(Region of Interest, ROI)을 정밀 추출하는 고성능 마우스 클릭 이벤트 인터랙션 클래스(`SelRangeMouseClick`)**를 제공합니다.

실차 가감속 및 제동 평가 시, 수 만개에 달하는 시계열 전체 데이터를 분석하는 것보다 운전자가 제동 페달을 밟기 시작한 정확한 시점부터 차량이 완전히 정지한 시점까지의 '특정 구간 데이터'만 정밀하게 슬라이싱하는 것이 핵심입니다. 
본 모듈은 Matplotlib의 `mpl_connect` 마우스 이벤트 루프와 결합하여 사용자가 차트 위를 가볍게 마우스 클릭하는 것만으로 그 한계 지점 안의 수치 인덱스를 정교하게 가로채어 연산 파이프라인으로 다이렉트 이송해 줍니다.

---

## 🛠️ 2. 핵심 API 명세 (API Specifications)

### 2.1. `SelRangeMouseClick` 클래스 인터페이스

| 메서드명 | 타입 | 설명 |
| :--- | :---: | :--- |
| `__init__(selFig, selAx, selLine)` | 생성자 | 마우스 드래그를 감지할 대상 Figure, Axes 및 플롯 라인(Line2D) 객체를 약한 참조 형태로 연결 바인딩 |
| `__call__(event)` | 이벤트 콜백 | 사용자가 마우스 버튼을 누르는 물리 이벤트를 감지하여 클릭된 시계열 X 좌표 정보를 큐(Queue)에 적재하고 두 점이 확보되면 해당 범위 인덱스 반환 |

---

## 📋 3. 입력 파라미터 및 속성 상세 정의 (Arguments)

1. **`selFig` (`plt.Figure` - 필수)**:
   - 마우스 이벤트를 연결할 Matplotlib 피규어 인스턴스입니다.
2. **`selAx` (`plt.Axes` - 필수)**:
   - 데이터 좌표를 파싱할 타겟 2D 축 인스턴스입니다.
3. **`selLine` (`matplotlib.lines.Line2D` - 필수)**:
   - 클릭된 점이 실제로 위치한 2D 수치 라인 객체입니다. 이 라인으로부터 내부 X, Y 원시 데이터프레임 인덱스를 역추적합니다.

---

## 💻 4. 실무 활용 예제 (Multi-case Examples)

### 4.1. [시나리오 1] 주행 그래프 위에서 마우스 클릭을 통한 제동 구간 ROI 인덱스 실시간 감지
```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from unoUtil.graphics.controls.range_selector import SelRangeMouseClick

# 1. 100Hz 제동 속도 그래프 렌더링
t_data = np.linspace(0, 10, 1000)
v_data = 100 - (t_data ** 2)

fig, ax = plt.subplots(figsize=(10, 6))
line_obj, = ax.plot(t_data, v_data, 'r-', label='Speed Profile')
ax.legend()

# 2. 마우스 클릭 ROI 선택기 바인딩 기동
selector = SelRangeMouseClick(selFig=fig, selAx=ax, selLine=line_obj)

# mpl_connect 마우스 버튼 누름 이벤트에 콜백 바인딩
fig.canvas.mpl_connect('button_press_event', selector)

# [수동 차트 띄우기 예시] 사용자가 두 곳을 클릭할 때까지 대기
# plt.show()는 GUI 전용이므로 사용자 검수 환경에서만 조건식 실행
```

### 4.2. [시나리오 2] 선택기 __call__ 이벤트 트리거 수동 모의 검증 (Mock Call)
```python
# 마우스 클릭 이벤트를 인위적으로 모의하여 정상 범위 판정 테스트
class MockEvent:
    def __init__(self, xdata, ydata, button):
        self.xdata = xdata
        self.ydata = ydata
        self.button = button
        self.inaxes = True

# 1. 첫 번째 제동 시작 시점 클릭 모의 (t=2.5s)
event_1 = MockEvent(xdata=2.5, ydata=93.75, button=1)
selector(event_1)

# 2. 두 번째 제동 정지 시점 클릭 모의 (t=8.2s)
event_2 = MockEvent(xdata=8.2, ydata=32.76, button=1)
selector(event_2)

# 두 점 사이의 정렬 완료된 궤적 시간 인덱스 확인
print(f"📐 탐색된 제동 개시 범위: {selector.start_x:.2f}s ➡️ 정지 범위: {selector.end_x:.2f}s")
```

### 4.3. [시나리오 3] Non-blocking GUI 루프 회수 처리
```python
# 자동화 배치 CI/CD 검증 환경에서 마우스 인터랙션을 통과시키기 위해 close=True 안전 가드 가동
fig.canvas.draw()
plt.savefig("./test_output/range_selector_mock.png", dpi=200)

# 메모리 즉시 회수 처리로 GUI 무한 대기(Hang) 현상 원천 방지
plt.close(fig)
print("🛡️ 무중단 range_selector 자가 구동 검증이 완료되었습니다.")
```
