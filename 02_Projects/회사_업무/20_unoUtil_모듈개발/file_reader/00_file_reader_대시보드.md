# 🚀 unoUtil 이기종 계측 데이터 리더 도메인 대시보드 (file_reader)

이 문서는 실차 주행 시험에서 발생하는 다양한 이기종 계측 장비(Racelogic VBOX ASCII/Binary, Dewesoft D7D, Oxford RT, 조향 로봇, CAN 로거 등)의 원시 로그를 초고속으로 파싱하고 표준 규격으로 정규화하는 `unoUtil.file_reader` 도메인의 마스터 MOC(Map of Content) 대시보드입니다.

---

## 📜 버전 이력 및 주요 개발 현황 (Changelog)

| 날짜 (Date) | 커밋 / 버전 | 변경 유형 | 작업 내역 및 아키텍처 개선 사항 | 상태 |
| :---: | :---: | :---: | :--- | :---: |
| **2026-09-27** | `v2.0.0` (Final) | `Refactor & Docs` | **`file_reader` 도메인 8대 동사 전면 표준화 및 자가 구동/문서 완성**<br>• `standard_channel_pattern.py`: 8대 표준 동사 `to_standard_channels`, `get_default_signals` 신규 구현, 레거시 `funcChangeSignalName` 100% 호환 보존, 3개 시나리오 자가 구동 스위트 및 1:1 매뉴얼 신설<br>• `dwdReader.py`: 8대 동사 `read_dwd_file`, `diagnose_dwd` 신규 구현 및 구버전 카멜케이스 별칭 바인딩<br>• `parsers/` 서브패키지: 외부 실차 로그 부재 시 Mock 자립 구동 3-시나리오 테스트 스위트 전면 보강<br>• `00_file_reader_대시보드.md` 신규 구축 및 상위 마스터 대시보드 연동 | **완료 (PASS)** |
| **2026-03-24** | `v2.0-rc1` | `Architecture` | **`FileDataReader` Facade 타워 및 4대 독립 파서 분리 아키텍처 구축**<br>• VBO C-엔진 고속 파싱, VBB 바이너리 디코더 내재화, Dewesoft C-DLL 인터페이스 분리<br>• GPS 좌표 기반 전세계 주요 시험장 로컬 타임존 및 DST 자동 판별 엔진 탑재<br>• Fluent API 메서드 체이닝 및 배치 `scan_dir()` 지원 | **완료** |

---

## 🧭 1. 도메인 아키텍처 및 파이프라인 (Architecture)

```mermaid
flowchart TD
    RawFile["📁 이기종 계측 원시 파일<br/>(.VBO, .VBB, .d7d, .txt, .csv, .sdf)"] --> FDR["FileDataReader(path, **kwargs)<br/>[통합 파사드 타워]"]

    subgraph Auto_Dispatcher [1. 전용 파서 자동 라우팅]
        FDR --> VBO["VBOParser<br/>(C-엔진 고속 파싱)"]
        FDR --> VBB["VBBParser & VBBReader<br/>(전원 급차단 3중 방어)"]
        FDR --> DWD["DWDParser & dwdReader<br/>(C-DLL & 비동기 시간축 정합)"]
        FDR --> TXT["TextParser<br/>(인코딩/구분자 자동 감지)"]
    end

    VBO & VBB & DWD & TXT --> MD["MeasurementData<br/>(표준 불변 데이터 캡슐)"]

    subgraph Standard_Pipeline [2. 표준화 및 후처리 파이프라인 (Fluent API)]
        MD --> SCP["StandardChannelPattern (Signal)<br/>to_standard_channels()<br/>(국제/사내 표준 채널 & 단위 교정)"]
        SCP --> DH["DateTimeHelper<br/>add_datetime(timezone='auto')<br/>(GPS 좌표 기반 타임존 & DST 시계열)"]
        DH --> PostProc["결측치 보간 (.interpolate_nans)<br/>센서 축 정렬 (.align_sensor_rows)<br/>조향각 부호 교정 (.correct_steering_sign)"]
    end

    subgraph Output_Interfaces [3. 다형성 출력 인터페이스]
        PostProc --> DF["reader.data / reader.df (DataFrame)"]
        PostProc --> TUPLE["reader.to_legacy_tuple()<br/>(파일명, DF, 저장일시, 주율 4-튜플)"]
        PostProc --> SNAPSHOT["reader.to_measurement_data()"]
    end
```

---

## 📚 2. 서브모듈 상세 명세 및 1:1 매뉴얼 링크

| 모듈 / 서브패키지 | 핵심 클래스 / 함수 | 주요 기능 및 역할 | 1:1 기술 매뉴얼 |
| :--- | :--- | :--- | :---: |
| **`file_data_reader`** | `FileDataReader`, `scan_dir` | 계측 파일 통합 로더, 자동 파서 라우팅, Fluent API 체이닝, 일괄 배치 스캔 | [[file_data_reader|기술 문서]] |
| **`standard_channel_pattern`** | `Signal`, `StandardChannelPattern` | 정규식 기반 수백 종 비표준 채널명 표준화, 깨진 단위 기호 자동 교정 | [[standard_channel_pattern|기술 문서]] |
| **`datetime_helper`** | `DateTimeHelper`, `calc_gps_datetime` | 전세계 시험장 GPS 바운딩 박스 타임존 매핑, DST 서머타임 보정, 시계열 합성 | [[datetime_helper|기술 문서]] |
| **`parsers.base_parser`** | `BaseParser`, `MeasurementData` | 파서 추상 규격, 계측 데이터 표준 캡슐 컨테이너, 레거시 튜플 변환 | [[base_parser|기술 문서]] |
| **`parsers.vbo_parser`** | `VBOParser` | Racelogic VBOX ASCII(`.vbo`) C-엔진 고속 파서 (초당 수십만 행) | [[vbo_parser|기술 문서]] |
| **`parsers.vbb_parser`** | `VBBParser` | Racelogic VBOX Binary(`.vbb`) 파서 (저수준 VBBReader 연동) | [[vbb_parser|기술 문서]] |
| **`parsers.dwd_parser`** | `DWDParser` | Dewesoft 고속 계측(`.d7d`, `.dxd`) C-DLL 파서 | [[dwd_parser|기술 문서]] |
| **`parsers.text_parser`** | `TextParser` | Oxford RT, 조향 로봇, TXT/CSV/SDF 텍스트 계측 데이터 파서 | [[text_parser|기술 문서]] |
| **`vbbTopython`** | `VBBReader`, `FileReader`, `VBBFile` | VBB 바이너리 저수준 디코더, 전원 급차단 3중 방어, 무손실 벡터 합성 | [[VBBReader|기술 문서]] |
| **`DWDataReader_v5_0_8`** | `read_dwd_file`, `diagnose_dwd` | Dewesoft C-DLL 래퍼, Sync/Async 채널 시간축 지능형 격자 정합 | [[dwdReader|기술 문서]] |

---

## 📊 3. 지원 계측 포맷 매트릭스

| 포맷 | 대표 확장자 | 담당 파서 | 지원 샘플링 레이트 | 주요 계측 장비 | 비고 |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **VBOX ASCII** | `.vbo` | `VBOParser` | 10 ~ 100 Hz | Racelogic VBOX II / III / 3i | C-엔진 기반 고속 로딩 |
| **VBOX Binary** | `.vbb` | `VBBParser` | 10 ~ 100 Hz | Racelogic VBOX 3i, CAN 로거 | 전원 급차단 무손실 복구 지원 |
| **Dewesoft** | `.d7d`, `.dxd` | `DWDParser` | 100 ~ 20,000 Hz | Dewesoft SIRIUS, DEWE-43 | C-DLL 래퍼 & 비동기 CAN 정합 |
| **Oxford RT** | `.txt`, `.csv` | `TextParser` | 100 ~ 250 Hz | Oxford RT2000 / RT3000 | 텍스트 헤더 및 단위 자동 분리 |
| **Steering Robot** | `.txt`, `.sdf` | `TextParser` | 100 ~ 1000 Hz | ABD, Anthony Best Dynamics | 구분자 및 가변 헤더 자동 감지 |

---

## 🚀 4. 핵심 사용법 및 워크플로우 (Quick Start)

### 4.1. 단일 파일 로딩 및 체이닝 (Fluent API)

```python
from unoUtil.file_reader import FileDataReader

# 1. 인스턴스 생성 및 로드
reader = FileDataReader("test_data/sample.vbo")
reader.load()

# 2. 메서드 체이닝을 통한 정규화 파이프라인 적용
(
    reader
    .apply_standard_channels(del_non_std=False)  # 표준 신호명 변환
    .add_datetime(timezone="auto")              # GPS 타임존 자동 보정
    .interpolate_nans(method="pchip")           # 결측치 보간
)

# 3. 데이터프레임 및 물리량 접근
df = reader.data
print(f"데이터 형상: {df.shape}")
print(f"계측 시작 일시: {reader.save_date}")
print(f"계측 주율: {reader.sample_rate} Hz")
print(f"단위 딕셔너리: {reader.units}")
```

### 4.2. 폴더 내 계측 파일 일괄 배치 스캔 (`scan_dir`)

```python
from unoUtil.file_reader import FileDataReader

# 특정 폴더 내의 모든 계측 파일 자동 감지 및 일괄 로딩
results = FileDataReader.scan_dir(
    folder_path="test_data/raw_readers",
    apply_standard=True,
    add_datetime=True,
    timezone="auto"
)

for item in results:
    print(f"[{item.file_name}] {item.shape} | {item.save_date}")
```

### 4.3. 레거시 4-튜플 변환 호환성

```python
# 기존 v1 레거시 함수형 코드와의 무중단 연동
name, df, save_date, sample_rate = reader.to_legacy_tuple()
```

---

## 🛡️ 5. 하위 호환성 및 개발 원칙 (Single Baseline Law)

1. **단일 기준 불변 원칙 (Single Baseline Law)**:
   - 사내 실제 운영되던 v1 오리지널 레거시 인터페이스(`unoUtil.vehicleTest.*`, `ReadDataFile`, `funcChangeSignalName`)만을 대상으로 호환성을 보장합니다.
2. **클래스 역할 내포 시 메서드 접두사 중복 방지 (No Redundant Prefix Law)**:
   - `FileDataReader` 및 각 `Parser` 클래스는 이미 역할이 클래스명에 포함되어 있으므로, `reader.read_vbo()` 대신 `reader.load()`, `parser.parse()`의 간결하고 직관적인 명칭을 유지합니다.
3. **8대 표준 동사 규칙 준수**:
   - 모듈 레벨 전역 함수는 `read_dwd_file`, `diagnose_dwd`, `to_standard_channels` 등 8대 표준 동사를 엄격히 준수하며, 기존 함수명은 100% 별칭으로 바인딩되어 있습니다.
