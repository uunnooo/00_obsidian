---
id: "resample_20260918"
title: "resample (비수치 보존 리샘플링 및 보간) 상세 매뉴얼"
type: resource
category_main: 회사_업무
category_sub: 개발매뉴얼
date: 2026-09-18
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - 신호처리
  - 리샘플링
  - 보간
  - 매뉴얼
project_link: "[[unoUtil]]"
---

# ⏱️ resample (비수치 보존 리샘플링 및 보간) 상세 매뉴얼

> [!ABSTRACT] 📌 개요
> 이종 센서(VBOX 100Hz, CAN 20Hz, 기상 1Hz 등)의 샘플링 레이트 불일치를 해소하기 위해, **수치형 신호의 수학적 보간**과 **문자열/범주형 메타데이터의 무손실 전파(ffill/bfill)**를 결합한 전용 리샘플링 모듈입니다.  
> 
> * **영구 공학 지식 레퍼런스**: [[25_실차_신호처리_및_시계열_데이터_정제_공학]]
> * **상위 대시보드**: [[00_post_process_대시보드]] | [[00_unoUtil_모듈개발_대시보드]]

---

## 1. ⚙️ 주요 API 규격

### 1.1. `resample_data(data, target_freq=100, method='linear', ...)`
* **기능**: 시계열 데이터프레임을 지정된 주파수(`Hz`) 또는 시간 간격(`ms`)으로 리샘플링합니다.
* **매개변수**:
  - `data (pd.DataFrame)`: DatetimeIndex 또는 수치형 시간축 컬럼을 보유한 데이터프레임.
  - `target_freq (int | float)`: 목표 주파수(Hz, 기본값 100Hz).
  - `method (str)`: 보간 방식 (`'linear'`, `'cubic'`, `'nearest'`).
* **하위 호환 별칭**: `SP_Resample`

### 1.2. `interpolate_data(data, method='linear', ...)`
* **기능**: 결측치(NaN)가 발생한 데이터프레임에서 수치형 데이터는 보간하고, 비수치형 데이터는 `ffill/bfill`로 보존합니다.
* **하위 호환 별칭**: `SP_Interpolation`

### 1.3. `merge_data(data1, data2, on='Time', tolerance=0.05, ...)`
* **기능**: 서로 다른 주기와 시작 시점을 가진 두 계측 데이터를 최근접 시간축(`merge_asof`) 기반으로 무손실 병합합니다.
* **하위 호환 별칭**: `SP_Merge`

---

## 2. 💻 호출 예제 (Usage Example)

```python
import pandas as pd
from unoUtil.signal_process.post_process import resample_data, merge_data

# 1. 10Hz CAN 데이터와 100Hz VBOX 데이터 준비
df_can = pd.DataFrame({"Time": [0.0, 0.1, 0.2], "Steer": [10.5, 12.0, 15.2], "Gear": ["D", "D", "D"]})
df_vbox = pd.DataFrame({"Time": [0.0, 0.05, 0.1, 0.15, 0.2], "Speed": [100.0, 95.0, 89.0, 82.0, 75.0]})

# 2. 비수치 보존 리샘플링 (Gear는 유지, Steer는 선형 보간)
df_can_100hz = resample_data(df_can, target_freq=100)

# 3. 비동기 최근접 정합 병합
df_merged = merge_data(df_vbox, df_can_100hz, on="Time")
```
