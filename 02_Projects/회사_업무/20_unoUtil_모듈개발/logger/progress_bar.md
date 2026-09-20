# 🧭 ProgressBar 캐리지 리턴 기반 콘솔 진행률 바 매뉴얼 (progress_bar.md)

## 📌 1. 개요 및 목적 (Overview)
`progress_bar` 모듈은 외부 무거운 라이브러리(tqdm 등)의 의존성 없이, 순수 파이썬 표준 라이브러리와 캐리지 리턴(Carriage Return, `\r`) 제어 및 ANSI 콘솔 이스케이프 코드를 활용하여 터미널 상에 **실시간 태스크 진행률 바(Percentage Gauge), 남은 시간(ETA) 및 초당 연산 속도(it/s)를 가볍고 매끄럽게 동적 렌더링**해 주는 경량 고성능 콘솔 가시화 유틸리티 패키지입니다.

대용량 15만 행 센서 데이터를 전처리하거나, 수백 번의 파라미터 최적화 루프를 돌릴 때, 진행률 표시 없이 콘솔이 멈춰 있으면 사용자가 연산이 다운되었는지 판별하기 어렵습니다. 
본 모듈은 CLI 백그라운드 구동 시 프로그레스 바가 깨져서 여러 줄 출력되는 지저분한 현상을 완벽하게 방어하는 **스마트 라인 버퍼링**을 지원하며, 총량(total)을 알 수 없을 때도 자율적으로 빙글빙글 돌아가는 **회전형 스피너(Spinner) 모드**로 자동 전환되어 인프라의 주행 가독성을 혁신해 줍니다.

---

## 🛠️ 2. 핵심 API 명세 (API Specifications)

### 2.1. `ProgressBar` 클래스 및 글로벌 헬퍼 함수 명세

| 메서드 / 함수명 | 타입 | 설명 |
| :--- | :---: | :--- |
| `get_active_progressbar()` | 글로벌 함수 | 현재 윈도우 콘솔 화면에 동적으로 렌더링 중인 활성 프로그레스 바 인스턴스 싱글톤 조회 |
| `ProgressBar` | 클래스 | 콘솔 터미널 진행률 바 출력 및 캐리지 리턴 갱신 엔진 객체 |
| `ProgressBar.update(n)` | 메서드 | 작업 완수량 `n` 단계를 프로그레스 바에 더하고 남은 시간(ETA)과 속도를 고속 재계산하여 콘솔에 한 줄 갱신 수행 |
| `ProgressBar.write(msg)` | 메서드 | 프로그레스 바가 그려지고 있는 도중 콘솔에 디버그 로그가 섞여 나와도 깨지지 않도록 라인을 임시 버퍼링해 안전하게 로그 출력 |
| `track(iterable, total, desc)` | 제너레이터 함수 | **[최우선 래퍼]** 반복 가능한 객체(Iterable)를 감싸서 for 루프를 돌기만 하면 자동으로 프로그레스 바를 그려내는 편리한 원라이너 함수 |

---

## 📋 3. 입력 파라미터 상세 정의 (Arguments)

1. **`total` (`int` - 선택, 기본값: `None`)**:
   - 전체 작업량 수치입니다. 이 값이 `None` 이면 백분율 대신 무한 순회 스피너(Spinner: `|`, `/`, `-`, `\`) 모드로 기동됩니다.
2. **`desc` (`str` - 선택, 기본값: `'Progress'`)**:
   - 프로그레스 바 왼쪽에 접두사로 표기할 설명 문구입니다 (예: `'Optimizing'`).
3. **`width` (`int` - 선택, 기본값: `40`)**:
   - 윈도우 콘솔에 그려질 게이지 바(`[██████░░░]`)의 정량적 글자 너비 크기입니다.

---

## 💻 4. 실무 활용 예제 (Multi-case Examples)

### 4.1. [시나리오 1] `track` 래퍼 함수를 이용한 데이터 전처리 for 루프 자동 프로그레스 바 렌더링
```python
import time
from unoUtil.logger.progress_bar import track

# 1. 100번 반복하는 가상 전처리 시퀀스
data_list = list(range(100))

# 2. 루프에 track() 래퍼를 씌우기만 하면 자동으로 콘솔에 진행률, ETA, 속도가 영롱하게 한 줄 갱신됩니다!
for i in track(data_list, desc="Processing VBOX Logs", unit="file"):
    # 가상의 계측 전처리 연산 수행
    time.sleep(0.02)
```

### 4.2. [시나리오 2] 총 작업량을 모르는 무한 스트림 데이터의 회전형 스피너(Spinner) 모드 기동
```python
from unoUtil.logger.progress_bar import ProgressBar

# total을 None으로 기입하여 스피너 모드로 수동 생성
pbar = ProgressBar(total=None, desc="Streaming Dewesoft Data", unit="pkt")

with pbar:
    for _ in range(50):
        time.sleep(0.05)
        pbar.update(1)  # 루프 돌 때마다 스피너 모양이 [ / ], [-], [ \ ] 으로 빙글빙글 회전 갱신됨
```

### 4.3. [시나리오 3] 진행률 바가 깨지지 않도록 버퍼링 로그 출력 (pbar.write)
```python
pbar_log = ProgressBar(total=10, desc="Fitting Magic Formula")

with pbar_log:
    for i in range(10):
        time.sleep(0.1)
        if i == 5:
            # 단순 print를 쓰면 게이지 바가 깨지지만, write()를 쓰면 안전하게 밀어내고 이쁘게 출력됨!
            pbar_log.write("⚠️ Warning: fitting convergence score is slightly low on iteration 5")
        pbar_log.update(1)
```
