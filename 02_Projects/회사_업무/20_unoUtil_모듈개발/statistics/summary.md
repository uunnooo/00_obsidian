---
id: "statistics_summary_20260918"
title: "summary (10대 핵심 요약통계 추출기) 상세 매뉴얼"
type: resource
category_main: 회사_업무
category_sub: 개발매뉴얼
date: 2026-09-18
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - 통계
  - summary
  - 기술통계
  - 매뉴얼
project_link: "[[unoUtil]]"
---

# 📊 summary (10대 핵심 요약통계 추출기) 상세 매뉴얼

> [!ABSTRACT] 📌 개요
> 실차 시험 데이터프레임의 수치형 컬럼들로부터 **10대 핵심 기술통계량(Count, Mean, Std, Min, Max, Median, IQR, Skewness, Kurtosis, SEM)**을 일괄 계산하여 정형화된 리포트 테이블로 출력하는 통계 모듈입니다.  
> 
> * **상위 대시보드**: [[00_unoUtil_모듈개발_대시보드]]

---

## 1. ⚙️ 주요 API 규격

### 1.1. `get_statistics_df(data, columns=None, ...)`
* **기능**: 데이터프레임의 수치 컬럼별 10대 통계량을 데이터프레임 형태로 반환합니다.
* **매개변수**:
  - `data (pd.DataFrame)`: 입력 데이터프레임.
  - `columns (Optional[List[str]])`: 분석 대상 수치형 컬럼 목록.
* **산출 통계 지표**:
  - `count`, `mean`, `std`, `min`, `max`, `median`, `iqr`, `skew`, `kurtosis`, `sem`
* **하위 호환 별칭**: `get_statics_df` (구버전 철자 오타 무중단 지원)

---

## 2. 💻 호출 예제 (Usage Example)

```python
import pandas as pd
from unoUtil.statistics import get_statistics_df

df = pd.DataFrame({"Speed": [100, 95, 80, 50, 0], "Decel": [-0.1, -0.8, -0.9, -0.85, 0.0]})
df_summary = get_statistics_df(df)
print(df_summary)
```
