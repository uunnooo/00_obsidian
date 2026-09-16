# 🚀 Data File Reader (uno-Series): 초정밀 전처리 엔진 통합 마스터 레퍼런스

본 문서는 데이터 분석 실무자가 VBO, TXT, SDF 등 다양한 계측 로그를 다룰 때 발생할 수 있는 모든 시나리오를 해결하기 위해 작성되었습니다. 각 함수의 내부 로직, 입력 인자의 분기 처리, 그리고 실무 적용 예시를 단 하나도 빠짐없이 기술합니다.

> **소속 모듈**: `unoUtil.readDataFile.ReadDataFile` (레거시 보존)  
> **차세대 대체 모듈**: [[FileDataReader]] (`unoUtil.fileDataReader.FileDataReader`)  
> **상태**: 레거시 유지 관리 (Legacy Active)

---

### 🏛️ 모듈 시스템 아키텍처 (Architecture)

모듈은 데이터의 흐름에 따라 **[식별 → 분석 → 행렬화 → 시계열화]**의 4단계 논리 계층으로 작동합니다.
* **Layer 1. Ready (입력)**: `ReadDataFile` (GUI/경로 스캔 및 파일 큐 생성)
* **Layer 2. Meta (분석)**: `funcFindHeader`, `funcFindSaveDate`, `funcFindSampleRate` (위치/시간/Hz 확정)
* **Layer 3. Matrix (조립)**: `funcMakeDataFrame` (수치 행렬 구축 및 멀티 인덱스 부여)
* **Layer 4. Action (정제)**: `funcReadDataFile` (전체 프로세스 통합 관리 및 최종 출력)

---

### 📖 모든 함수별 초정밀 상세 가이드 (Full API Deep Dive)

### 1. `ReadDataFile(FileName=None, **kwargs)` ⭐ (최상위 사용자 인터페이스)
💡 **기능**: 사용자로부터 입력받은 경로의 성격에 따라 처리 모드를 지능적으로 전환합니다.

* **⚙️ 입력 케이스별 상세 동작 및 사용 예시**:
    * **CASE 1: `FileName=None` (GUI 탐색기 모드)**
        * **동작**: `PyQt5.QtWidgets.QFileDialog`를 실행하여 윈도우 탐색기를 띄웁니다.
        * **예시**: `data_list, _ = ReadDataFile(filter='*.vbo')`
        * **설명**: 사용자가 탐색기에서 파일을 직접 선택하며, `filter` 인자에 따라 특정 확장자만 노출됩니다.
    * **CASE 2: `FileName="C:/Logs"` (디렉토리 스캔 모드)**
        * **동작**: 지정된 폴더 내 파일을 검색하며, `auto` 인자에 따라 검색 깊이가 결정됩니다.
        * **분기 1 (`auto=False`)**: 해당 폴더 내 **직속 파일**만 검색합니다. (하위 폴더 제외)
            - 예: `ReadDataFile("D:/Test", auto=False, filter='*.txt')`
        * **분기 2 (`auto='all'`)**: `os.walk`를 사용하여 **모든 하위 폴더**를 재귀적으로 뒤져 파일을 수집합니다.
            - 예: `ReadDataFile("D:/Test", auto='all', filter='*.vbo')`
        * **필수 조건**: 폴더 스캔 시에는 반드시 `filter`를 통해 유효한 확장자를 지정해야 오류 없이 파일을 큐에 담을 수 있습니다.
    * **CASE 3: `FileName="C:/Logs/data.vbo"` (단일 파일 경로)**
        * **동작**: 입력된 경로가 파일인 경우 즉시 단일 파일 로드 프로세스를 시작합니다.
    * **CASE 4: `FileName=["a.vbo", "b.vbo"]` (리스트 입력)**
        * **동작**: 리스트에 담긴 여러 파일 경로를 순차적으로 `funcReadDataFile`에 전달하여 일괄 처리합니다.

---

### 2. `funcReadDataFile(FileName, **kwargs)` (통합 실행 엔진)
💡 **기능**: 개별 파일 하나를 열어 분석 가능한 데이터프레임으로 변환하는 **실질적인 컨트롤 타워**입니다.

* **⚙️ 핵심 키워드(kwargs) 상세 사용법**:
    * `headendline` (int): 데이터 시작점을 찾기 위해 훑을 최대 라인수. (예: `headendline=300`)
    * `chname` (bool): `True` 설정 시 `par.Signal()`에 정의된 표준 명칭(예: Speed -> VehSpd)으로 변환.
    * `swa` (str): 조향 부호 반전 기준 채널명. (예: `swa="VW_Sign"` 입력 시 해당 채널이 1인 구간의 SWA에 -1 곱함)
    * `reftime` (다중 형식 지원):
        * **딕셔너리**: `reftime={'Time': 9}` (Time 열 기준 9시간 더하기)
        * **불리언**: `reftime=True` (저장된 GPS 시간을 기준으로 0초 오프셋 적용)
        * **문자열**: `reftime='20260101'` (특정 날짜를 기준으로 시간축 생성)
    * `fixfile` (bool): `True`인 경우 정제된 데이터를 `.vbo-fix` 형태의 원본 포맷 텍스트로 재저장.
    * `inter` (bool): `True`일 때 `pchip` 알고리즘을 사용하여 결측치를 보간합니다.
    * `align_rows` (bool): 센서 간 데이터 기록 시작 시점이 다를 때 발생하는 NaN 행을 정렬 및 제거합니다.

---

### 3. `funcFindHeader(RawData, endLine=False)`
💡 **기능**: 비정형 텍스트에서 **채널명 행**과 **데이터 시작 행**의 위치를 지능적으로 찾아냅니다.

* **⚙️ 내부 로직 및 사용 예시**:
    * **동작**: 문자와 숫자의 분포 비율 및 연속성을 계산하여 데이터 경계면을 감지합니다.
    * **예시**: `col_idx, start_idx, line_range = funcFindHeader(raw_df, endLine=200)`
    * **해석**: 파일 상단 200줄 이내에서 채널명 위치(`col_idx`)와 실제 수치 데이터 시작점(`start_idx`)을 반환합니다.

---

### 4. `funcMakeDataFrame(RawData, lineNum, changeval=False)`
💡 **기능**: 원문 텍스트를 수치 행렬로 변환하고 채널명/단위를 구조화합니다.

* **⚙️ 입력 형태에 따른 분기**:
    * **`lineNum`이 정수(int)**: 해당 행을 채널명으로, 그 다음 행을 단위(Unit)로 인식하여 **2단 Multi-Index** 구축.
        * **예시**: `df_cols = funcMakeDataFrame(raw, 15)` (15번 행을 헤더로 사용)
    * **`lineNum`이 리스트/범위**: 해당 구역의 수치를 파싱하여 데이터프레임 생성.
    * **`changeval`**: 숫자 변환 에러(`ValueError`) 발생 시 대체할 값. (예: `changeval=np.nan`)

---

### 5. `funcMakeDateTime(RawData, RefDateTime, **kwargs)`
💡 **기능**: 상대 시간 데이터에 **절대 시각(Timestamp)**을 부여하여 `Datetime` 열을 생성합니다.

* **⚙️ 제어 파라미터**:
    * `RefDateTime`: 시작 기준 시각 (예: `datetime(2026, 3, 30, 9, 0, 0)`)
    * `sign`: `+`(시간 가산), `-`(시간 역산).
* **💻 예시**:
```python
# 기준 시각으로부터 샘플링 주기에 맞춰 시간축 자동 생성
df_final = funcMakeDateTime(df_source, RefDateTime=dt_start, sign='+')
```

---

### 6. `funcFindSaveDate(RawData, **kwargs)`
💡 **기능**: 파일 헤더 텍스트에서 **기록된 날짜와 시각** 메타데이터를 추출합니다.

* **⚙️ 사용 시나리오**:
    * 파일 내부의 `file create`나 `start` 키워드 주변의 날짜 형식을 인식합니다.
    * `pm` 키워드 발견 시 자동으로 12시간을 가산 보정합니다.
    * **예시**: `dt_save = funcFindSaveDate(df_raw.iloc[0:50])` (상단 50줄에서 날짜 추출)

---

### 7. `funcFindSampleRate(RawData, ChName, RawDF)`
💡 **기능**: 장비의 **계측 속도(Sampling Hz)**를 도출합니다.

* **⚙️ 탐색 시나리오**:
    1. 헤더에서 `sample rate` 수치 검색.
    2. 부재 시, `Time` 채널의 데이터 간격(`diff`)을 역산하여 Hz 도출.
    3. **예시**: `hz = funcFindSampleRate(header, df.columns, df)`

---

### 💻 실무 통합 응용 예제 (The Master Example)

```python
# [종합] VBOX 데이터를 로드하여 한국 시간 보정, 보간, 조향 부호 반전 처리
from uno_module import ReadDataFile

# 1. 통합 함수를 통한 대규모 폴더 스캔 및 자동 전처리
results, _ = ReadDataFile(
    FileName="D:/Project/Logs", 
    auto='all',          # 재귀적 폴더 스캔
    filter='*.vbo',      # VBO 파일만 필터링
    date=True,           # Datetime 컬럼 생성 활성화
    reftime={'Time': 9}, # UTC+9 한국 시간 보정
    chname=True,         # 표준 시그널명 매핑
    inter=True,          # 결측치 보간(PCHIP)
    align_rows=True,     # 센서 딜레이로 인한 NaN 행 정렬 제거
    swa="VW_Sign"        # VW_Sign 채널에 따른 조향각 부호 반전
)

# 2. 결과 출력 및 데이터 활용
for name, df, s_date, hz in results:
    # 정제된 데이터프레임으로 즉시 시각화 및 통계 분석 가능
    print(f"[{name}] 샘플링: {hz}Hz | 기록 시점: {s_date}")
    df_visual = df[['Datetime', 'VehSpd', 'VehSWA']].dropna()
```

---

### 🛡️ 목적별 퀵 가이드 (Safety Net)

| 나의 분석 상황 | 추천 함수 및 옵션 조합 | 기대 효과 |
| :--- | :--- | :--- |
| **"파일을 직접 마우스로 선택하고 싶을 때"** | `ReadDataFile(None, filter='*.vbo')` | GUI 창 활성화 및 확장자 필터링 |
| **"하위 폴더 상관없이 특정 폴더만 스캔할 때"** | `ReadDataFile("경로", auto=False)` | 지정 폴더 직속 파일만 빠르게 로드 |
| **"계측 장비와 PC 시간이 다를 때"** | `reftime={'Time': 시간차}` | 기준 시간 오프셋 보정으로 데이터 동기화 |
| **"데이터 이름이 제각각일 때"** | `chname=True` | 표준화된 명칭(VehSpd 등)으로 자동 통일 |

**Documented by your Coding Partner & Technical Writer, uno.**
