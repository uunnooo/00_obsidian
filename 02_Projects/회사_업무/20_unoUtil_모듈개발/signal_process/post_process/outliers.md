---
id: "outliers_20260918"
title: "outliers (다변량 이상치 정제 및 연속구간 판별) 상세 매뉴얼"
type: resource
category_main: 회사_업무
category_sub: 개발매뉴얼
date: 2026-09-18
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - 신호처리
  - 이상치
  - 이상치탐지
  - IsolationForest
  - 매뉴얼
project_link: "[[unoUtil]]"
---

# 🛡️ outliers (다변량 이상치 정제 및 연속구간 판별) 상세 매뉴얼

> [!ABSTRACT] 📌 개요
> 센서 통신 버스트, 터널 GPS 스파이크, 휠 락 등의 이상치를 통계적/머신러닝 기법으로 색출하고, 유효한 물리 시험 구간을 탐색하는 모듈입니다.  
> 
> * **영구 공학 지식 레퍼런스**: [[25_실차_신호처리_및_시계열_데이터_정제_공학]]
> * **상위 대시보드**: [[00_post_process_대시보드]] | [[00_unoUtil_모듈개발_대시보드]]

---

## 1. ⚙️ 주요 API 규격

### 1.1. `remove_outliers(data, method='percentile', threshold=..., ...)`
* **기능**: 선택된 알고리즘에 따라 이상치를 탐지하여 `NaN`으로 치환하거나 제거합니다.
* **지원 알고리즘 (`method`)**:
  - `'percentile'`: 상/하위 백분위수 초과치 제거.
  - `'zscore'`: 정규분포 가정 표준편차($3\sigma$) 초과치 제거.
  - `'isolation_forest'`: 비모수적 트리 분할 기반 다변량 이상치 탐지.
  - `'extended_if'`: 축 편향성을 제거한 하이퍼플레인 분할 이상치 탐지.
* **하위 호환 별칭**: `SP_RMOutlier`

### 1.2. `find_continuous_interval(data, condition, min_duration=..., ...)`
* **기능**: 특정 조건(예: 감속도 $\le -0.2G$)을 연속적으로 만족하는 구간의 시작/종료 인덱스를 고속 추출합니다.
* **하위 호환 별칭**: `SP_FindContinue`

---

## 2. 💻 호출 예제 (Usage Example)

```python
import pandas as pd
from unoUtil.signal_process.post_process import remove_outliers, find_continuous_interval

# 1. 이상치가 포함된 센서 데이터
df_speed = pd.DataFrame({"Speed": [100, 98, 250, 95, 93, 0, 90]})

# 2. 백분위수 기반 이상치 제거 (상/하위 5% 컷)
df_clean = remove_outliers(df_speed, method="percentile", threshold=(5, 95))

# 3. 제동 연속 구간 탐색 (속도 10 이하로 10샘플 이상 유지 구간)
intervals = find_continuous_interval(df_clean["Speed"], condition=lambda s: s <= 10, min_duration=10)
```
