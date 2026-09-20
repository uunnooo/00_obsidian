# 🧭 TextParser 텍스트 기반 계측 파일 파서 매뉴얼 (text_parser.md)

## 📌 1. 개요 및 목적 (Overview)
`text_parser` 모듈은 Oxford RT, 조향 로봇(Steering Robot), 일반 CSV, SDF, DAT 등 전 세계 주행 시험장에서 출하되는 다양한 **텍스트(ASCII) 기반 쉼표/공백/탭 구분 형태의 계측 데이터 파일(`.txt`, `.csv`, `.sdf`, `.dat`) 전용 파서 클래스(`TextParser`)**를 정의합니다.

텍스트 기반 계측 파일은 기기 브랜드마다 문자 인코딩(CP949, UTF-8, Latin-1 등)이 다르고, 주율이 적힌 헤더 위치와 단위 행(Unit Row)의 존재 유무가 제각각이어서 일관된 코드로 파싱하기가 매우 까다롭습니다. 
본 모듈은 유연한 구분자 빈도 분석 및 C-엔진 기반 데이터 스캔을 통해 **수치 데이터 시작점과 헤더 행 구조를 100% 자동으로 역추적 판별**하여, 다량의 텍스트 원시 계측 파일을 표준 데이터 구조(`MeasurementData`)로 매끄럽고 신속하게 변형 및 수집해 줍니다.

---

## 🛠️ 2. 핵심 API 명세 (API Specifications)

### 2.1. `TextParser` 클래스 인터페이스

| 메서드명 | 타입 | 설명 |
| :--- | :---: | :--- |
| `can_parse(file_path)` | `Method` | 파일 확장자가 `.txt`, `.csv`, `.sdf`, `.dat` 범위 내에 있는지 판단하여 구동 여부 결정 (True/False 반환) |
| `parse(file_path, header_max_lines, delimiter, encoding, **kwargs)` | `Method` | 텍스트 파일 헤더를 정밀 분석하여 인코딩, 일자, 채널명, 단위를 추출하고 C-엔진 기반 Pandas 로더로 고속 디코딩 실행 |
| `_detect_encoding(path)` | 비공개 Method | CP949, UTF-8, Latin-1 등을 순차 시도하여 예외 크래시 없는 최적의 파일 디코딩 인코딩 감지 |
| `_extract_save_date(lines, path, reftime)` | 비공개 Method | 헤더 상단 텍스트 블록에서 계측 개시 년-월-일 및 시:분:초 타임스탬프 스캔 |
| `_analyze_structure(lines, delimiter)` | 비공개 Method | 구분자 빈도를 판별하고 수치 비율 70%가 넘는 최초 라인을 데이터 시작행으로 검출하고 컬럼명/단위 행 자동 식별 |
| `_extract_columns_and_units(lines, idx_col, idx_unit, sep)` | 비공개 Method | 컬럼명 텍스트와 단위 텍스트를 파싱 및 정형화하여 단위 사 사전 구축 |
| `_calculate_sample_rate(df, lines)` | 비공개 Method | 헤더 내부 주파수 검색 구문이나 Time 컬럼 간격(`diff().idxmax()`)을 토대로 정밀 주율 계산 |

---

## 📋 3. 입력 파라미터 및 속성 상세 정의 (Arguments)

1. **`file_path` (`str` / `Path` - 필수)**:
   - 파싱 대상이 되는 텍스트 파일의 경로입니다.
2. **`delimiter` (`str` - 선택, 기본값: `None`)**:
   - 수동으로 기입할 구분자 정보입니다. 지정하지 않을 시 탭(`\t`), 쉼표(`,`), 공백(`\s+`) 중 빈도가 높은 문자를 기계적으로 자동 선택합니다.
3. **`encoding` (`str` - 선택, 기본값: `None`)**:
   - 파일 디코딩 문자셋입니다. 지정하지 않으면 최적 인코딩을 자동 역추적합니다.

---

## 💻 4. 실무 활용 예제 (Multi-case Examples)

### 4.1. [시나리오 1] 일반 Oxford RT 텍스트 계측 데이터 자동 판별 및 파싱
```python
from unoUtil.file_reader.parsers.text_parser import TextParser

# 텍스트 파서 객체화
text_parser = TextParser()

txt_path = "D:/test_data/oxford_rt_log.txt"

if text_parser.can_parse(txt_path):
    # 인코딩, 구분자, 헤더 위치를 모두 자동 역추적 파싱 수행
    data_container = text_parser.parse(file_path=txt_path)
    
    print(f"✅ 파싱 성공! 데이터 크기: {data_container.shape}")
    print(f"📏 검출된 계측 주파수: {data_container.sample_rate} Hz")
    print(f"📐 채널별 단위 매핑: {data_container.units}")
```

### 4.2. [시나리오 2] 탭 구분자 및 CP949 수동 지정을 통한 손상된 로봇 로그 복구
```python
# 한글 코멘트와 탭 구분이 혼재된 깨진 로봇 텍스트 파일 복구
corrupted_txt = "D:/test_data/steering_robot_raw.dat"

# 강제 옵션을 주어 150줄 이내에서 데이터 구획을 파괴하지 않고 CP949로 무중단 디코딩
recovered_container = text_parser.parse(
    file_path=corrupted_txt,
    header_max_lines=200,
    delimiter="\t",
    encoding="cp949"
)

print(f"💾 복구 완결! 복구된 채널 수: {len(recovered_container.channels)}")
```

### 4.3. [시나리오 3] `reftime` 우선순위 날짜 주입을 통한 시계열 기준 보정
```python
# VBOX 등과 동시 정합을 위해, 텍스트 파일 헤더 날짜 대신 사용자가 보정한 reftime 날짜 강제 주입
adjusted_container = text_parser.parse(
    file_path=txt_path,
    reftime={"date": "2026-09-19"}  # 헤더 탐색 날짜 대신 이 날짜가 save_date에 강제 주입됨
)

print(f"📅 시공간 정렬 완료! 보정된 일시: {adjusted_container.save_date}")
```
