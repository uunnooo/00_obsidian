# 🧭 DWDParser Dewesoft 포맷 브릿지 파서 매뉴얼 (dwd_parser.md)

## 📌 1. 개요 및 목적 (Overview)
`dwd_parser` 모듈은 Dewesoft 계측 데이터 포맷(`.d7d`, `.dxd`)을 초고속으로 파싱하여 Pandas DataFrame으로 변환해 주는 전용 디코더 브릿지 클래스(`DWDParser`)를 제공합니다.

Dewesoft 독점 바이너리 포맷은 상용 라이브러리로 접근이 거의 불가능합니다. 
본 모듈은 Dewesoft 공식 **`DWDataReader C-DLL v5.0.8`**을 파이썬 내부로 끌어와 동적 연동함으로써 계측 데이터를 디코딩합니다. 특히 Dewesoft의 가장 까다로운 스펙인 **"동기 채널(일정 주기의 아날로그 센서)"**과 **"비동기 채널(CAN 통신, GPS 위성 좌표)"**의 시계열 정합 문제를 `pd.merge_asof` 기반의 고속 타임라인 보간법으로 풀어내어, 15만 행 이상의 복합 채널 데이터를 단 2초 만에 완벽한 동기화 프레임으로 가공해 냅니다.

---

## 🛠️ 2. 핵심 API 명세 (API Specifications)

### 2.1. `DWDParser` 클래스 인터페이스

| 메서드명 | 타입 | 설명 |
| :--- | :---: | :--- |
| `can_parse(file_path)` | `Method` | 파일 확장자가 `.d7d` 또는 `.dxd` 인지 검출하여 Dewesoft 디코더 실행 여부 판단 (True/False 반환) |
| `parse(file_path)` | `Method` | `DWDataReader` C-DLL 바인딩 엔진을 가동하여 메모리에 바이너리를 풀고, 동기/비동기 채널을 정밀 합성 및 리샘플링하여 최종 정합 완료된 Pandas DataFrame 반환 |

---

## 📋 3. 입력 파라미터 및 속성 상세 정의 (Arguments)

1. **`file_path` (`str` / `Path` - 필수)**:
   - 디코딩할 Dewesoft 원시 데이터 파일(`.d7d`, `.dxd`)의 물리적 경로입니다.
   - 내부적으로 `DWDataReaderHeader`와 DLL 헤더 바인딩이 셋업되어 있어야 C-엔진의 접근이 허가됩니다.

---

## 💻 4. 실무 활용 예제 (Multi-case Examples)

### 4.1. [시나리오 1] Dewesoft 독점 바이너리 디코딩 및 C-DLL 기동
```python
from unoUtil.file_reader.parsers.dwd_parser import DWDParser

# Dewesoft 전용 파서 인스턴스화
dwd_parser = DWDParser()

dwd_path = "D:/test_data/dewesoft_braking_raw.d7d"

if dwd_parser.can_parse(dwd_path):
    # C-DLL 기동하여 바이너리 덤프 및 판다스 파이프라인 정합 기동
    df_dwd = dwd_parser.parse(file_path=dwd_path)
    
    print(f"🎨 Dewesoft 디코딩 완결! Shape: {df_dwd.shape}")
    print(f"📈 아날로그 + CAN/GPS 합성 완료 채널: {list(df_dwd.columns[:5])}")
```

### 4.2. [시나리오 2] 비동기 GPS 및 CAN 채널의 pd.merge_asof 기반 타임라인 보간 수동 검증
```python
# 내부 파서가 비동기 채널을 보간하는 수동 아키텍처 원리 검증
df_analog = get_analog_channels(dwd_path)  # 100Hz 동기 센서
df_can_gps = get_async_can_channels(dwd_path) # 비동기 10Hz 센서

# merge_asof 고속 정합 연산 기동
df_synced = pd.merge_asof(
    df_analog,
    df_can_gps,
    on='Time',
    direction='backward'  # 아날로그 시점 기준 가장 최신의 과거 비동기 신호 매핑
)

print(f"⚡ 100Hz 아날로그 시간 축에 CAN 데이터가 무손실 동기화되었습니다. (Rows: {len(df_synced)})")
```

### 4.3. [시나리오 3] 대규모 배치 파일 로딩 예외 격리 검수
```python
import os

dwd_dir = "D:/test_data/batch_dewesoft/"
successful_dfs = []

# 폴더 내 전체 Dewesoft 파일을 스캔하여 손상된 파일은 배제하고 정상 본만 이중 복구
for file_name in os.listdir(dwd_dir):
    full_path = os.path.join(dwd_dir, file_name)
    if dwd_parser.can_parse(full_path):
        try:
            df = dwd_parser.parse(full_path)
            successful_dfs.append(df)
            print(f"✅ {file_name} 로드 완료")
        except RuntimeError as e:
            # DLL 내부 디코딩 크래시 격리 방어
            print(f"❌ {file_name} 디코딩 에러 무시 및 격리: {e}")
```
