---
id: "weather_20260920"
title: "weather (실차 계측용 정밀 기상정보 통합 및 매핑 엔진) 상세 매뉴얼"
type: resource
category_main: 회사_업무
category_sub: 개발매뉴얼
date: 2026-09-20
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - 유틸리티
  - 기상정보
  - 매뉴얼
project_link: "[[unoUtil]]"
---

# 🌦️ weather (실차 계측용 정밀 기상정보 통합 및 매핑 엔진) 상세 매뉴얼

> [!ABSTRACT] 📌 개요
> 실차 시험장(테크노링 등)의 5분 단위 노면 온도 센서 데이터와 15분 주기의 기상 종합 스테이션 계측 데이터를 시간 연속적인 5분 타임라인으로 정밀 통합(Reindexing & Time Interpolation)하고, 시험 계측 파일(VBOX 등)과 가장 인접한 시간대로 결합하는 기상 환경 매핑 모듈입니다.
> 
> * **상위 대시보드**: [[00_utils_대시보드]] | [[00_unoUtil_모듈개발_대시보드]]

---

## 1. ⚙️ 주요 API 규격

### 1.1. `load_master_database(dir=None, range=None) -> pd.DataFrame`
* **기능**: Gzip으로 압축된 기상 마스터 데이터베이스(.pkl.gz)를 고속 디스크 복원 로드하고, 6자리(`yymmdd`) 또는 8자리(`YYYYmmdd`) 날짜 가용 구간에 맞춰 시간축 데이터를 정밀 슬라이싱합니다.

### 1.2. `update_master_database(df_new_weather_data, str_master_file_path) -> pd.DataFrame`
* **기능**: 신규 처리된 기상 통합 데이터를 기존 마스터 DB에 추가적으로 Concat 병합하며, 중복 날짜/시간대는 최신(last) 데이터로 중복 제거하여 압축 저장합니다.

### 1.3. `save_as_custom_excel(df_report_input, save, col_sel=None) -> None`
* **기능**: 데이터프레임을 전치(Transpose)하고, 시간열을 Excel 가로형 2칸씩 병합 셀 서식으로 가공하여 사내 주행시험 결과 최종 보고서 양식에 즉시 붙여 넣을 수 있는 특화 파일로 자동 기록합니다.

### 1.4. `connect_weather(df_input, df_weather, refer_col='Datetime', ...)`
* **기능**: 실차 주행 시험 시계열 데이터프레임(`df_input`)에 `pd.merge_asof(..., direction='nearest')` 기법을 적용하여, 실차 센서가 기록된 순간에 가장 가까운 최적 기상 환경 데이터(온도, 노면온도, 풍속 등)를 연동 결합합니다.

---

## 💻 2. 호출 예제 (Usage Example)

```python
import pandas as pd
from unoUtil.utils.weather import load_master_database, connect_weather

# 1. 1분 간격의 실차 주행 데이터 예시
drive_df = pd.DataFrame({
    "Datetime": pd.to_datetime(["2026-03-18 10:00:15", "2026-03-18 10:01:20"]),
    "GPS_Speed": [80.5, 100.2]
})

# 2. 사내 보관 기상 마스터 DB 로드 (특정 기간 슬라이싱 적용)
weather_df = load_master_database(
    dir="D:/uno/0. DB/1. weather/0. DB/master_weather_database.pkl.gz",
    range=["20260301", "20260331"]
)

# 3. nearest 시간대 병합을 통해 주행 시험 데이터에 기상 정보 연동
merged_df = connect_weather(
    df_input=drive_df,
    df_weather=weather_df,
    refer_col="Datetime",
    target_col=["온도", "풍속", "BRK Wet Asp"]
)
print(merged_df)
```

---

## 3. 📝 이중 동기화 프로토콜 준수사항
- 이 매뉴얼 파일(`weather.md`)은 동일 로컬 디렉터리(`unoUtil/utils/`) 내에 1:1 대응하여 보관되며, 최종 작업 완료 선언 시 옵시디언 볼트로 일괄 배치 동기화 처리됩니다.
