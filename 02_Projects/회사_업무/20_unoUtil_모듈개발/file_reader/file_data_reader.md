# 🚀 FileDataReader 기술 매뉴얼 및 사용자 가이드

> **소속 모듈**: `unoUtil.file_reader.file_data_reader`  
> **상태**: 릴리즈 완료 (Active)  
> **관련 영구 지식 문서**: [[20_VBOX_계측_데이터_규격_및_GPS좌표계]], [[21_바이너리_파일_IO_및_VBB_데이터_포맷_구조]], [[22_GPS_좌표_기반_타임존_자동_판별_및_시계열_합성_이론]], [[23_이종_계측_데이터_통합_파이프라인_및_대규모_마이그레이션_엔지니어링]], [[ReadDataFile]]

---

## 1. 📌 개요 및 도입 배경

차량 실차 시험(제동, 조향, 핸들링, 스노우 평가 등) 과정에서는 Racelogic VBOX ASCII(`.vbo`), VBOX Binary(`.vbb`), Dewesoft(`.d7d`), Oxford RT 및 조향 로봇(`.txt`, `.csv`, `.sdf`) 등 극도로 이질적인 데이터 포맷들이 수집됩니다.

기존 레거시 `ReadDataFile` 모듈은 단일 모놀리식 구조로 인해 다음과 같은 한계가 있었습니다:
1. **과도한 I/O 지연**: 수십만 행의 VBO 파일을 순수 파이썬 루프로 한 줄씩 파싱하여 파일 1개 로드에 수 초 이상 소요 (벤치마크 기준 3~6초).
2. **모놀리식 블랙박스 파이프라인**: 10여 개가 넘는 전처리 인자(표준 채널, 결측치 보간, 시계열 생성 등)가 하나의 함수 내부에 뒤엉켜 있어 단계별 제어 및 디버깅 곤란.
3. **타임존 수동 하드코딩의 불편함**: GPS 타임은 본질적으로 UTC 기준이나, 한국(테크노링, 남양)은 UTC+9, 핀란드(이발로)는 UTC+2(하계 DST UTC+3) 등 시험 장소에 따라 사용자가 매번 오프셋을 수동 입력해야 하는 번거로움 존재.
4. **파일 경로 메타정보 부재**: 반환값이 튜플 `(name, df, date, rate)` 형태로만 한정되어 원본 파일의 디렉토리, 확장자, 원시 단위 등을 체계적으로 추적하기 어려움.

**`FileDataReader`**는 이러한 한계를 완벽히 극복하기 위해 설계된 **차세대 객체 지향 계측 데이터 리더 프레임워크**입니다.

---

## 2. 🏛️ 시스템 아키텍처

```mermaid
flowchart TD
    Target[계측 파일 경로 / 디렉토리] --> FDR["FileDataReader(path, **kwargs)"]
    
    subgraph Path_Properties [1. 명시적 경로 속성]
        FDR --> P1[".file_path (절대 경로)"]
        FDR --> P2[".dir_path (부모 폴더)"]
        FDR --> P3[".file_name (파일명)"]
        FDR --> P4[".file_ext (확장자)"]
    end

    subgraph Format_Dispatch [2. 전용 고속 파서 라우팅]
        FDR --> BP{확장자 판정}
        BP -->|".vbo"| VBO[VBOParser: C-엔진 고속 파싱]
        BP -->|".vbb"| VBB[VBBParser: VBBReader 브릿지]
        BP -->|".d7d"| DWD[DWDParser: DWDataReader C-DLL]
        BP -->|".txt/.csv"| TXT[TextParser: 헤더/구분자 자동 감지]
    end

    VBO --> MD[MeasurementData 표준 컨테이너]
    VBB --> MD
    DWD --> MD
    TXT --> MD

    subgraph Transformations [3. 독립 변환 메서드 체이닝 (Fluent API)]
        MD --> T1[".apply_standard_channels()"]
        T1 --> T2[".add_datetime(timezone='auto')"]
        T2 --> T3[".interpolate_nans(method='pchip')"]
        T3 --> T4[".align_sensor_rows()"]
        T4 --> T5[".set_units(enable=True)"]
        T5 --> T6[".correct_steering_sign()"]
        T6 --> T7[".drop_empty_columns()"]
    end

    subgraph Output_Interfaces [4. 다형성 출력 인터페이스]
        T7 --> OUT1[".data 또는 .df (DataFrame)"]
        T7 --> OUT2[".to_legacy_tuple() (구버전 4-튜플)"]
        T7 --> OUT3[".to_measurement_data() (불변 스냅샷)"]
        T7 --> OUT4["FileDataReader.scan_dir() (일괄 배치)"]
    end
```

### 2.1. 완전 독립 패키지 구성 (Zero-Dependency Package Architecture)
`file_reader`는 향후 레거시 `readDataFile` 패키지가 완전히 제거되어도 독자적으로 100% 동작할 수 있도록, 필요한 모든 하위 디코더와 DLL 라이브러리를 내부에 완벽히 내재화(Self-Contained)하였습니다:

```text
📂 unoUtil/file_reader/
├── file_data_reader.py          # 통합 Facade 엔트리포인트
├── standard_channel_pattern.py  # [표준화 ⭐] 정규식 기반 표준 채널/단위 매핑
├── datetime_helper.py           # GPS 좌표 바운딩 박스 타임존 & 2-Stage 시계열
├── 00_file_reader_대시보드.md    # [신규 ⭐] file_reader 마스터 대시보드
├── 📂 parsers/                  # 전용 고속 파서 서브패키지
│   ├── base_parser.py           # 파서 추상 규격 및 MeasurementData 컨테이너
│   ├── vbo_parser.py            # Racelogic VBO 전용 C-엔진 파서
│   ├── vbb_parser.py            # Racelogic VBB 바이너리 파서
│   ├── dwd_parser.py            # Dewesoft D7D 바이너리 파서
│   └── text_parser.py           # Oxford RT, 조향로봇, TXT/CSV/SDF 파서
├── 📂 vbbTopython/              # [내재화 ⭐] VBB 바이너리 고속 디코더 엔진
│   ├── VBBReader.py             # 마스터 타임라인 무손실 조립 & 전원 급차단 3중 방어
│   ├── FileReader.py            # NumPy 바이트 스트리밍 I/O
│   ├── VBBFile.py               # VBB 바이너리 구조체 컨테이너
│   └── VBBReader.md             # VBB 디코더 상세 매뉴얼
└── 📂 DWDataReader_v5_0_8/      # [내재화 ⭐] Dewesoft C-DLL 및 Python 래퍼
    ├── DWDataReaderHeader.py    # ctypes C-헤더 정의 및 라이브러리 로더
    ├── dwdReader.py             # Dewesoft 고속 채널 추출기 (Sync/Async)
    ├── DWDataReaderLib64.dll    # Windows 64-bit 전용 공식 네이티브 라이브러리
    ├── DWDataReaderLib64.so     # Linux 64-bit 라이브러리
    └── DWDataReaderLib64.dylib  # macOS 64-bit 라이브러리
```

---

## 3. 🌟 핵심 기능 및 기술 혁신

### 3.1. 명시적 파일 경로 속성 (Path Properties)
데이터 로드 후 언제 어디서나 원본 파일의 위치 및 메타정보를 즉시 조회할 수 있습니다:
- `reader.file_path`: 대상 파일의 절대 경로 (`pathlib.Path`)
- `reader.dir_path`: 파일이 포함된 디렉토리 경로 (`pathlib.Path`)
- `reader.file_name`: 확장자를 제외한 파일명 (`str`)
- `reader.file_ext`: 소문자 확장자 (예: `'.vbo'`, `'.vbb'`)

### 3.2. 포맷별 전용 파서 라우팅 및 5배속 I/O 혁신
각 계측 포맷의 물리적 특성에 최적화된 독립 파서를 호출합니다:
- **`VBOParser`**: Pandas C-엔진의 `sep=r'\s+', skiprows=...`를 직접 결합하여 대용량 VBO 로딩 속도를 **3.03초 $\rightarrow$ 0.458초 (5.5배 단축)**로 혁신.
- **`VBBParser`**: 바이너리 VBB 데이터로부터 멀티 채널 비동기 정합 및 표준화 지원.
- **`DWDParser`**: Dewesoft C-DLL(v5.0.8)을 직접 연동하여 14만 행 이상의 고속 수집 데이터 및 CAN/GPS 비동기 정합 지원.
- **`TextParser`**: RT3000, 조향 로봇, 일반 CSV 파일의 헤더 및 구분자(탭, 쉼표, 공백)를 휴리스틱하게 자동 판별.

### 3.3. GPS 좌표 기반 로컬 타임존 및 서머타임(DST) 자동 보정
- 위도/경도 바운딩 박스를 통해 한국(테크노링, 남양) $\rightarrow$ UTC+9, 핀란드(이발로 테크노트랙) $\rightarrow$ UTC+2(하계 UTC+3) 등 시험장 로컬 시간대를 100% 자동 판별.
- Python 3.9 표준 `zoneinfo.ZoneInfo`를 결합하여 일광 절약 시간제(DST)가 적용되는 유럽 시험장의 오프셋 변동을 완벽히 해결.
- `reftime={'Time': 9}` 또는 사용자 수동 오프셋/날짜 입력 시 수동 설정 우선 적용.

### 3.4. 일자/시각 2단계 분리 판정 (2-Stage Resolution)
- **1단계 (Date)**: 사용자 reftime $\rightarrow$ 헤더 날짜 $\rightarrow$ 파일명 날짜 패턴(정규식) $\rightarrow$ 수정일시(mtime) 순으로 기준 일자 결정.
- **2단계 (Time)**: VBOX 포맷(HHMMSS.ss) 또는 경과 시간(sec) 여부를 자동 식별하고 타임존 오프셋을 정밀 합산.
- **3단계 (Series)**: Pandas C-엔진 `pd.date_range` 기반 고속 시계열 생성 (10만 행 기준 **3.03ms** 소요).

### 3.5. 듀얼 인터페이스: 유연한 메서드 체이닝 vs 1줄 원스톱 생성자
- **메서드 체이닝 (Fluent API)**: 단계별 데이터 변환 과정을 명시적으로 확인하고 디버깅 가능.
- **생성자 원스톱 파이프라인 (One-shot)**: 기존 `ReadDataFile` 사용 스타일 그대로 키워드 인자 1줄로 모든 전처리 완료.

---

## 4. 💻 상세 사용법 및 코드 예제

### 4.1. [Case 1] 1줄 황금 기본값 로드 (Recommended ⭐)
실무에서 가장 많이 쓰는 **표준 채널 매핑(`chname=True`)**, **GPS 자동 로컬 타임존 일시 열(`date='auto'`)**, **진행 로그(`verbose=True`)**가 기본값으로 내장되어 있어 별도 인자 없이 파일 경로만 넘겨도 완벽히 정제된 데이터를 즉시 얻을 수 있습니다:
```python
from unoUtil.fileDataReader import FileDataReader

# 인자 없이 호출해도 표준 채널 매핑 + 한국 로컬 Datetime(+9h) 자동 생성 완료!
reader = FileDataReader("example/example_BRK.VBO")

print("파일명:", reader.file_name)
print("크기:", reader.shape)
print("시작 일시:", reader.data["Datetime"].iloc[0])
```

### 4.2. [Case 2] 원시 데이터(Raw) 로드 및 경로 속성 접근
어떠한 전처리도 거치지 않은 순수 원본 데이터를 열람하려면 `auto_process=False`로 로드합니다:
```python
from unoUtil.fileDataReader import FileDataReader

# 원시 데이터 로드 (추가 전처리 미적용)
reader = FileDataReader("example/example_BRK.VBO", auto_process=False)

print("절대 경로:", reader.file_path)
print("부모 폴더:", reader.dir_path)
print("순수 파일명:", reader.file_name)
print("확장자:", reader.file_ext)
print("데이터 크기:", reader.shape)
print("채널 목록:", reader.channels[:5])
```

### 4.2. [Case 2] 독립 메서드 체이닝 (Fluent API)
```python
from unoUtil.fileDataReader import FileDataReader

reader = FileDataReader("example/example_BRK.VBO", auto_process=False)

# 단계별 전처리 체이닝
(
    reader
    .apply_standard_channels(del_non_std=False)  # 표준 신호명 치환
    .add_datetime(timezone="auto")              # GPS 자동 타임존 로컬 일시 생성
    .interpolate_nans(method="pchip")           # 결측치 보간
    .set_units(enable=True)                     # ('Name', 'Unit') MultiIndex 변환
)

print(reader.df.head(3))
```

### 4.3. [Case 3] 1줄 원스톱(One-shot) 생성자 호출 (상세 로깅 및 소요 시간 모니터링)
```python
from unoUtil.fileDataReader import FileDataReader

# verbose=True 또는 print=True를 전달하면 단계별 소요 시간과 상세 진행 로그가 출력됩니다.
reader = FileDataReader(
    "example/example_BRK.VBO",
    chname=True,      # 표준 채널명 변환
    date="auto",      # GPS 로컬 타임존 자동 일시 열 생성
    inter=True,       # 결측치 보간
    unit=True,        # 단위 레벨 포함
    print=True        # [NEW ⭐] 상세 진행 로그 및 단계별 소요 시간 출력 (verbose=True와 동일)
)

# 콘솔 출력 예시:
# 15:35:00 [ℹ️ INFO   ] [unoUtil.FileDataReader] ✔ [example_BRK.VBO] 파일 로드 및 원시 데이터 파싱 완료 (0.045s)
# 15:35:00 [ℹ️ INFO   ] [unoUtil.FileDataReader] 파서 매칭 완료: VBOParser -> 'example_BRK.VBO'
# 15:35:00 [ℹ️ INFO   ] [unoUtil.FileDataReader] 데이터 로드 완료: Shape=(78526행, 20채널), 샘플링=100.0Hz, 시작일시=2023-08-25 10:15:30
# 15:35:00 [ℹ️ INFO   ] [unoUtil.FileDataReader] ✔ 표준 채널명 매핑 완료 (0.003s)
# 15:35:00 [ℹ️ INFO   ] [unoUtil.FileDataReader] ✔ Datetime 시계열 생성 완료 (0.008s)
# 15:35:00 [ℹ️ INFO   ] [unoUtil.FileDataReader] ✔ 결측치 보간 (pchip) 완료 (0.012s)
# 15:35:00 [ℹ️ INFO   ] [unoUtil.FileDataReader] ✔ 단위 MultiIndex 변환 완료 (0.001s)

# 기존 레거시 함수와 동일한 4-튜플로 즉시 언패킹 가능
name, df, save_date, sample_rate = reader.to_legacy_tuple()
```

### 4.4. [Case 4] 디렉토리 일괄 스캔 및 실시간 프로그레스 바 (Batch Scan)
```python
from unoUtil.file_reader import FileDataReader

# 특정 폴더 내의 로그 파일들을 일괄 수집 (프로그레스 바 기본 활성화)
# 콘솔 출력: 계측 파일 일괄 로딩: 100.0% |█████████████████████████| 12/12 [00:03<00:00, 3.8file/s]
readers = FileDataReader.scan_dir(
    dir_path="D:/LogFolder",
    extensions=[".vbo", ".vbb", ".d7d"],
    recursive=False,
    chname=True,
    date="auto",
    progress_bar=True  # [NEW ⭐] 실시간 진행률 게이지 바 활성화 (pbar=True 별칭 지원, 침묵 모드는 False)
)

for r in readers:
    print(f"[{r.file_ext}] {r.file_name:20s} -> Shape: {r.shape}, Hz: {r.sample_rate}")
```

> [!TIP] **전용 프로그레스 바 독립 검증 예제 스크립트**  
> `scan_dir()`의 프로그레스 바 렌더링, 로그 발생 시 게이지 보존 메커니즘(Anti-Break), 침묵 모드(Silent)를 직접 눈으로 확인하려면 프로젝트 루트에서 아래 예제를 실행하세요:  
> ```bash
> python unoUtil/example/example_scan_dir_progressbar.py
> ```

---

## 5. 📊 벤치마크 및 자가 검증 결과

| 검증 항목 | 대상 파일 | 행/열 크기 | FileDataReader 처리 시간 | 레거시 ReadDataFile 대비 |
| :--- | :--- | :--- | :--- | :--- |
| **VBO 고속 파싱** | `example_BRK.VBO` | 78,526 x 20 | **0.458 초** | **5.5배 이상 단축** (3.03s $\rightarrow$ 0.458s) |
| **VBB 바이너리** | `example_VBB_DryBRK.VBB`| 95,860 x 51 | **4.249 초** | 정합 및 단위 매핑 완전 자동화 |
| **Dewesoft D7D** | `exampled7d_2.d7d` | 148,676 x 28 | **1.684 초** | 비동기 CAN/GPS 채널 고속 동기화 |
| **Oxford RT 텍스트**| `example_readData.txt` | 8,605 x 25 | **0.180 초** | 구분자/헤더 자동 식별 |
| **Datetime 시계열** | 100,000행 시뮬레이션 | 100,000행 | **0.003 초 (3.03ms)**| C-엔진 date_range 최적화 |

---

## 6. 🔄 레거시 마이그레이션 가이드

기존 `ReadDataFile`을 사용 중인 코드는 단 한 줄의 임포트 및 객체 생성 변경으로 즉시 전환할 수 있습니다.

```python
# ---------------------------------------------------------
# [기존 레거시 방식]
# ---------------------------------------------------------
from unoUtil.readDataFile import ReadDataFile

results, paths = ReadDataFile("test.vbo", chname=True, date='auto')
name, df, save_date, sample_rate = results[0]

# ---------------------------------------------------------
# [신규 권장 방식: FileDataReader]
# ---------------------------------------------------------
from unoUtil.fileDataReader import FileDataReader

# 황금 기본값(chname=True, date='auto', verbose=True)이 내장되어 별도 옵션 없이 1줄로 호출!
reader = FileDataReader("test.vbo")

# 명시적 속성으로 직관적 접근
print(reader.file_name, reader.df, reader.save_date, reader.sample_rate)
print(reader.file_path, reader.dir_path, reader.channels)

# 또는 기존 코드 유지를 위해 4-튜플로 언패킹
name, df, save_date, sample_rate = reader.to_legacy_tuple()
```

---

## 7. 🔗 관련 문서 및 영구 도메인 지식
- [[VBBReader]] : VBOX 바이너리(.vbb) 고속 디코더 엔진 매뉴얼 (`vbbTopython`)
- [[dwdReader]] : Dewesoft D7D C-DLL 연동 및 비동기 채널 정합 엔진 (`DWDataReader_v5_0_8`)
- [[23_이종_계측_데이터_통합_파이프라인_및_대규모_마이그레이션_엔지니어링]] : 영구 도메인 지식 (전체 엔지니어링 마스터)
- [[20_VBOX_계측_데이터_규격_및_GPS좌표계]] : VBOX 하드웨어 및 계측 데이터 규격
- [[21_바이너리_파일_IO_및_VBB_데이터_포맷_구조]] : 바이너리 I/O 아키텍처
- [[22_GPS_좌표_기반_타임존_자동_판별_및_시계열_합성_이론]] : GPS 바운딩 박스 타임존 판별 이론
- [[00_unoUtil_모듈개발_대시보드]] : 모듈 개발 현황 대시보드
- [[ReadDataFile]] : 레거시 모놀리식 모듈 (폐기 예정)

