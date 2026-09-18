---
id: "filters_20260918"
title: "filters (Zero-Phase 이동평균 필터) 상세 매뉴얼"
type: resource
category_main: 회사_업무
category_sub: 개발매뉴얼
date: 2026-09-18
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - 신호처리
  - 필터
  - filtfilt
  - 매뉴얼
project_link: "[[unoUtil]]"
---

# 🌊 filters (Zero-Phase 이동평균 필터) 상세 매뉴얼

> [!ABSTRACT] 📌 개요
> 실차 센서(CAN 휠 속도, 가속도, 제동 압력 등) 신호의 고주파 진동 및 노이즈를 **위상 지연(Phase Lag) 없이** 완벽하게 정제하는 영위상(Zero-Phase) 필터 모듈입니다.  
> Scipy의 `signal.filtfilt` 양방향 필터링과 경계값 대칭 반사 패딩(`padlen`)을 기본 탑재하고 있습니다.  
> 
> * **영구 공학 지식 레퍼런스**: [[25_실차_신호처리_및_시계열_데이터_정제_공학]]
> * **상위 대시보드**: [[00_post_process_대시보드]] | [[00_unoUtil_모듈개발_대시보드]]

---

## 1. ⚙️ 주요 API 규격

### 1.1. `moving_average(data, window_size=5, columns=None, ...)`
* **기능**: 데이터프레임 또는 시리즈에 대해 순방향 및 역방향 필터링을 수행하여 위상 지연이 0인 이동평균을 산출합니다.
* **매개변수**:
  - `data (pd.DataFrame | pd.Series)`: 입력 신호 데이터.
  - `window_size (int)`: 이동평균 윈도우 크기 (홀수 권장, 기본값 5).
  - `columns (Optional[List[str]])`: 특정 수치형 컬럼만 선택 적용할 경우 지정.
  - `plot (bool)`: 전/후 비교 플롯 출력 여부 (기본값 False).
  - `save (Optional[str])`: 플롯 저장 경로.
  - `close (bool)`: 플롯 자동 종료 여부 (기본값 True $\rightarrow$ Non-blocking 원칙 준수).
  - `method (str)`: filtfilt 경계 패딩 방식 (`'pad'` 기본값, `'gust'`). 50만 행 이상 대용량 시계열에서 `'pad'` 방식을 적용하여 최소제곱 행렬 분해(`lstsq`) 병목을 제거하고 **연산 속도를 117배 가속(5.2초 → 0.04초)**합니다.
* **반환값**: 필터링된 `pd.DataFrame` 또는 `pd.Series`.
* **하위 호환 별칭**: `SP_MovingAverage`

### 1.2. `moving_average_fast(data, window_size=5, ...)`
* **기능**: 대용량 고속 데이터(10만 행 이상)를 위해 2차 섹션(SOS) 필터 엔진(`sosfiltfilt`)을 적용한 초고속 영위상 필터.
* **하위 호환 별칭**: `SP_HighSpeed_MovingAverage`

---

## 2. 💻 호출 예제 (Usage Example)

```python
import numpy as np
import pandas as pd
from unoUtil.signal_process.post_process import moving_average, moving_average_fast

# 1. 100Hz 계측 노이즈 합성 데이터 생성
t = np.linspace(0, 10, 1000)
clean_signal = np.sin(2 * np.pi * 0.5 * t)
noise = np.random.normal(0, 0.2, len(t))
df_sample = pd.DataFrame({"Time": t, "Accel": clean_signal + noise})

# 2. Zero-Phase 이동평균 필터 적용 (위상 지연 없음)
df_filtered = moving_average(df_sample, window_size=21, columns=["Accel"])

# 3. 고속 SOS 필터 적용
df_fast = moving_average_fast(df_sample, window_size=21)
```

---

## 3. 🧪 무중단 시각화 검증

`plot=True` 옵션 지정 시 원본 신호와 필터링 신호의 오버레이 비교 그래프가 자동 생성되며, `close=True` 기본값에 의해 GUI 블로킹 없이 디스크 저장(`save="path.png"`) 또는 메모리 해제됩니다.
