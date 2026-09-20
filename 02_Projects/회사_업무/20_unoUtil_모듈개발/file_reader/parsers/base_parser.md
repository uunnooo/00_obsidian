# 🧭 BaseParser / MeasurementData 표준 데이터 구조 매뉴얼 (base_parser.md)

## 📌 1. 개요 및 목적 (Overview)
`base_parser` 모듈은 사내의 다양한 실차 계측 파일 포맷(VBO, VBB, D7D, DXD, CSV, TXT 등)을 파싱하는 모든 하위 전문 파서 클래스들이 상속해야 하는 **최상위 공통 추상 인터페이스(`BaseParser`)**와, 파싱된 센서 시계열 수치 데이터 및 시험 장비 메타데이터를 정형화하여 보관 및 유통하는 **표준 계측 데이터 모델 컨테이너(`MeasurementData`)**를 정의합니다.

데이터 전처리 파이프라인에서 기존에 사용되던 단순 `(파일명, 데이터프레임, 시작일시, 계측주율)`의 4-튜플 구조는 확장성이 떨어지고 채널 단위(Units)나 장비 헤더 원문 등의 부가 정보를 담지 못해 시스템 연계 시 한계가 명확했습니다. 
본 모듈은 이 4-튜플을 완벽하게 대체 및 캡슐화하면서도, 기존 레거시 함수형 인터페이스들과의 무중단 호환성을 위해 `to_legacy_tuple()` 변환 메서드를 탑재한 데이터 캡슐 아키텍처를 구현하고 있습니다.

---

## 🛠️ 2. 핵심 API 명세 (API Specifications)

### 2.1. `@dataclass` `MeasurementData` 클래스 인터페이스

| 메서드 / 속성 | 타입 | 설명 |
| :--- | :---: | :--- |
| `file_path` | `Path` | 원시 계측 로그 파일의 전체 절대 경로 |
| `file_name` | `str` | 확장자를 배제한 순수 파일 식별명 (예: `'lane1_wet_brk'`) |
| `data` (또는 `df`) | `pd.DataFrame` | 정제 및 로컬 타임존 보정이 완벽히 완료된 메인 센서 시계열 데이터프레임 |
| `save_date` | `datetime` | 계측이 시작된 실제 현지 절대 시간 로컬 타임스탬프 |
| `sample_rate` | `float` | 계측 주파수 (Hz 단위, 예: 100.0) |
| `channels` | `List[str]` | 데이터프레임 내에 정렬 탑재된 센서 물리 채널명 목록 |
| `units` | `Dict[str, str]`| 각 채널별 물리 단위 딕셔너리 매핑 (예: `{'Velocity': 'km/h'}`) |
| `shape` | `property` | 데이터프레임의 크기 반환 (Rows, Cols) |
| `to_legacy_tuple()` | 메서드 | 기존 레거시 함수형 함수들과의 호환을 위한 `(파일명, 데이터, 날짜, 주율)` 4-튜플 변환 |
| `to_csv(output_path)` | 메서드 | 정제 완료된 데이터프레임을 수동 디렉토리 또는 자동 명칭으로 CSV 물리 파일 내보내기 수행 |

### 2.2. `BaseParser` 추상 클래스 인터페이스

| 메서드명 | 타입 | 설명 |
| :--- | :---: | :--- |
| `can_parse(file_path)` | `abstractmethod` | 파일 확장자와 바이트 시그니처를 검사하여 이 파서가 해석할 수 있는지 판별 (True/False 반환) |
| `parse(file_path, **kwargs)` | `abstractmethod` | 파일을 파싱 및 전처리하여 최종 `MeasurementData` 표준 데이터 객체 반환 |

---

## 📋 3. 입력 파라미터 및 속성 상세 정의 (Arguments)

1. **`data` (또는 `df`) (`pd.DataFrame` - 필수)**:
   - 전처리 정제가 끝난 메인 계측 데이터프레임입니다. 객체 직접 접근 및 수정(`df.setter`) 시 자동으로 채널 목록이 연동 업데이트됩니다.
2. **`reftime` (`dict` / `str` - `**kwargs` 선택)**:
   - 파서 구동 시 전달되는 수동 날짜 설정값입니다. 파일 헤더의 불완전한 기록을 방지하기 위한 우선순위 속성입니다.

---

## 💻 4. 실무 활용 예제 (Multi-case Examples)

### 4.1. [시나리오 1] MeasurementData 컨테이너 생성 및 속성 직접 접근
```python
import pandas as pd
import datetime
from pathlib import Path
from unoUtil.file_reader.parsers.base_parser import MeasurementData

# 1. 수치 데이터 생성 및 컨테이너 캡슐화
mock_df = pd.DataFrame({"Velocity": [100, 50, 0]})
container = MeasurementData(
    file_path=Path("D:/Logs/brk_test.vbo"),
    file_name="brk_test",
    file_ext=".vbo",
    dir_path=Path("D:/Logs"),
    data=mock_df,
    save_date=datetime.datetime.now(),
    sample_rate=100.0,
    units={"Velocity": "km/h"}
)

# 2. 직관적인 속성 접근 및 인덱싱 활용
print(f"📊 Rows: {len(container)} | Columns: {container.channels}")
print(f"🛰️ 속도 데이터 직접 슬라이싱: {list(container['Velocity'])}")
```

### 4.2. [시나리오 2] 레거시 함수형 모듈 연동을 위한 4-튜플 호환 변환
```python
# 기존 레거시 함수들은 여전히 (file_name, df, save_date, sample_rate) 구조를 인자로 요구함
legacy_params = container.to_legacy_tuple()

# 무중단 파라미터 언팩킹(Unpacking) 포워딩
file_name, df_data, save_dt, hz = legacy_params
print(f"📅 하위 호환 변환 완료! 타겟 명칭: {file_name} (Hz: {hz}Hz)")
```

### 4.3. [시나리오 3] 정제된 데이터의 CSV 고속 자동 저장 기동 (to_csv)
```python
# 아카이브 폴더에 정제 완료된 데이터 내보내기 자동 수행
target_save_dir = "D:/test_data/archive"

# to_csv API의 다형성 save 경로 처리 기법 적용
saved_csv_path = container.to_csv(
    output_path=Path(target_save_dir) / f"{container.file_name}_cleaned.csv"
)

print(f"💾 CSV 파일 저장 완료: {saved_csv_path}")
```
