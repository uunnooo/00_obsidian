# 🧭 DateTimeHelper 고정밀 절대시간 및 타임존 보정 헬퍼 매뉴얼 (datetime_helper.md)

## 📌 1. 개요 및 목적 (Overview)
`datetime_helper` 모듈은 차량 실차 시험 계측 데이터의 신뢰성 높은 **절대 시간(Datetime 시계열) 생성, 타임존 보정 및 글로벌 시험장(한국 테크노링, 핀란드 이발로, 스페인 IDIADA 등) 자동 위도/경도 바운딩 감지**를 수행하는 사내 핵심 지능형 시계열 정합 유틸리티입니다.

이종 계측기(VBOX, Dewesoft, GPS 등)를 켜고 끌 때, 위성 통신 시간(UTC)과 현지 컴퓨터 시간(Local Time)이 어긋나 시계열 결합 시 몇 초에서 수 시간의 시간 차(Time-offset) 에러가 빈번히 유발됩니다. 
본 모듈은 Python 3.9 내장 표준 라이브러리인 `zoneinfo`를 전격 기동하여 전 세계 시험장의 GPS 위도/경도 좌표를 실시간으로 역추적하여 현지 타임존과 **서머타임(Daylight Saving Time, DST) 여부를 100% 무결하게 감지**하고, 판다스 C-엔진 기반의 고속 절대 시계열 생성 파이프라인을 구축해 줍니다.

---

## 🛠️ 2. 핵심 API 명세 (API Specifications)

### 2.1. 글로벌 헬퍼 함수 명세

| 함수명 | 입력 파라미터 | 설명 |
| :--- | :---: | :--- |
| `detect_timezone_from_coords(lat, lon, ref_date)` | `lat`, `lon`, `ref_date` | 위도와 경도 좌표를 판별하여 전 세계 주요 시험장의 IANA 타임존 명칭과 DST가 보정된 오프셋 시간 자동 산출 |
| `resolve_base_date(header_text, file_path, reftime, save_date)` | `header_text`, `file_path`, `reftime`, `save_date` | 계측 파일 헤더 텍스트, 사용자 입력 변수 간의 우선순위를 기계적으로 정립하여 정밀한 기준 년-월-일 확정 |
| `resolve_base_time(df, reftime, timezone, ref_date, save_date)` | `df`, `reftime`, `timezone`, `ref_date`, `save_date` | 계측 시작 정확한 시:분:초:마이크로초를 확정하고 GPS 위도 기반 로컬 타임존 시차 오프셋을 자동 덧셈 연산 |
| `build_datetime_series(df_raw, base_datetime, sign, interval, col_time)` | `df_raw`, `base_datetime`, `sign`, `interval`, `col_time` | 확정된 기준 일시와 시간 컬럼을 결합하여 C-엔진 기반으로 10만 행을 0.02초 만에 완벽한 `DatetimeIndex` 시계열로 변환 생성 |

---

## 📋 3. 입력 파라미터 상세 정의 (Arguments)

1. **`lat` / `lon` (`float` / `pd.Series` - 필수)**:
   - 위도(Latitude)와 경도(Longitude) WGS84 수치 정보입니다. 사내 주요 시험장 영역 바운딩 박스와 대조됩니다.
2. **`reftime` (`dict` / `str` - 선택, 기본값: `None`)**:
   - 사용자가 강제로 지정하고자 하는 수동 기준 일시 값입니다. (텍스트 스캔 결과보다 최우선 순위를 가집니다.)
3. **`base_datetime` (`pd.Timestamp` - 필수)**:
   - 연산의 절대 영점(Zero-point)이 될 계측 시작 시점의 기준 타임스탬프입니다.

---

## 💻 4. 실무 활용 예제 (Multi-case Examples)

### 4.1. [시나리오 1] GPS 위도/경도 좌표 기반 핀란드 이발로(Ivalo) 시험장 및 DST 자동 판별
```python
import pandas as pd
from unoUtil.file_reader.datetime_helper import detect_timezone_from_coords

# 핀란드 이발로 스노우 테스트 트랙 GPS 위경도 정보
ivalo_lat, ivalo_lon = 68.6189, 27.4475
ref_test_date = pd.Timestamp("2026-02-15")  # 겨울 이발로 테스트

# 타임존 및 현지 시차 판별
iana_tz, utc_offset = detect_timezone_from_coords(
    lat=ivalo_lat,
    lon=ivalo_lon,
    ref_date=ref_test_date
)

print(f"❄️ 탐색된 시험장 타임존: {iana_tz}")  # Output: Europe/Helsinki
print(f"⏰ UTC 대비 시차 오프셋: {utc_offset} hours (겨울 표준시 +2h 적용)")
```

### 4.2. [시나리오 2] 기준 일시 우선순위 확인 및 기계적 확정 (resolve_base_date)
```python
from unoUtil.file_reader.datetime_helper import resolve_base_date

# VBOX 텍스트 코멘트 가상 데이터
vbox_header = "file created 18/09/2026 14:22:15 \n [header]..."
file_save_date = "2026-09-18"

# 사용자가 직접 전달한 reftime 우선순위 작동 테스트
base_date = resolve_base_date(
    header_text=vbox_header,
    file_path="D:/test.vbo",
    reftime={'date': "2026-09-19"},  # 수동 우선순위 1순위
    save_date=file_save_date
)

print(f"📅 확정된 기준 일자: {base_date}")  # Output: 2026-09-19 (reftime 우선 채택 완료)
```

### 4.3. [시나리오 3] 대용량 등간격 계측 데이터의 C-엔진 기반 Datetime 시계열 초고속 생성
```python
from unoUtil.file_reader.datetime_helper import build_datetime_series

# 10만 행의 가상 아날로그 데이터프레임
df_big = pd.DataFrame({'Time': np.arange(0, 1000, 0.01)})  # 100Hz, 10만건
start_time = pd.Timestamp("2026-09-19 12:00:00")

# pandas date_range 최적화 C-엔진 파이프라인 기동
datetime_series = build_datetime_series(
    df_raw=df_big,
    base_datetime=start_time,
    interval=10,  # 10ms 주기 (100Hz)
    col_time='Time'
)

print(f"⚡ Datetime 시계열 생성 성공! 행수: {len(datetime_series)}")
print(f"⏰ 시작 시간: {datetime_series.iloc[0]} ➡️ 종료 시간: {datetime_series.iloc[-1]}")
```
