# 🧭 VBOParser VBOX ASCII 포맷 파서 매뉴얼 (vbo_parser.md)

## 📌 1. 개요 및 목적 (Overview)
`vbo_parser` 모듈은 Racelogic VBOX ASCII 로그 포맷(`.vbo`, `.VBO`)을 고속으로 해석하기 위한 사내 전용 특화 파서 엔진(`VBOParser`)을 제공합니다. 

실차 평가에서 널리 활용되는 VBOX 데이터는 대용량 채널과 다양한 시험 환경 메타데이터가 텍스트 블록에 혼재되어 있습니다. 
본 모듈은 VBOX 파일의 4대 핵심 섹션인 헤더(`[header]`), 채널 단위(`[channel units]`), 컬럼명(`[column names]`), 데이터 블록(`[data]`)을 **10ms 이내에 초고속 스캔**하여 데이터 인덱스를 감지하고, 수만~수십만 행에 달하는 대용량 수치 데이터 블록을 Pandas DataFrame으로 무결하게 자동 정렬 및 파싱하여 데이터 파이프라인의 입구 역할을 완벽하게 수행합니다.

---

## 🛠️ 2. 핵심 API 명세 (API Specifications)

### 2.1. `VBOParser` 클래스 인터페이스

| 메서드명 | 타입 | 설명 |
| :--- | :---: | :--- |
| `can_parse(file_path)` | `Method` | 파일의 확장자가 `.vbo` 또는 `.VBO` 인지 판단하여 구동 여부 결정 (True/False 반환) |
| `parse(file_path, head_end_line, encoding)` | `Method` | VBOX 파일을 읽어 4대 섹션을 디코딩하고 정렬된 Pandas DataFrame 및 메타정보 사전 반환 |
| `_extract_save_date(lines, path, reftime)` | 비공개 Method | 파일 내부의 생성 시간 문자열을 파싱하여 기준 일자(`save_date`) 산출 |
| `_extract_sample_rate(lines)` | 비공개 Method | 헤더 블록에서 GPS 계측 주파수(예: `10Hz`, `100Hz`) 정보 추출 |
| `_extract_units(lines)` | 비공개 Method | `[channel units]` 섹션의 채널 단위 목록 파싱 및 매핑 |
| `_extract_columns_and_data_index(lines)` | 비공개 Method | `[column names]` 채널명 리스트를 추출하고 데이터 수치 블록이 시작되는 정확한 물리 라인 인덱스 산출 |

---

## 📋 3. 입력 파라미터 및 속성 상세 정의 (Arguments)

1. **`file_path` (`str` / `Path` - 필수)**: 
   - 파싱할 대상 `.vbo` 파일의 전체 절대 경로입니다.
2. **`head_end_line` (`int` - 선택, 기본값: 자동 감지)**:
   - 헤더 스캔 속도를 최적화하기 위해 데이터 블록 시작 전까지만 파일을 읽도록 강제하는 줄 번호 한계점입니다.
3. **`encoding` (`str` - 선택, 기본값: `'utf-8'`)**:
   - 한글 코멘트 등이 섞여 있을 때 깨짐을 방지하기 위한 문자열 인코딩 규격입니다.

---

## 💻 4. 실무 활용 예제 (Multi-case Examples)

### 4.1. [시나리오 1] 기본 VBOX ASCII 파일 파싱 및 데이터프레임 추출
```python
from unoUtil.file_reader.parsers.vbo_parser import VBOParser

# 파서 인스턴스화
parser = VBOParser()

vbo_path = "D:/test_data/lane1_dry_braking.vbo"

if parser.can_parse(vbo_path):
    # parse 실행하여 데이터프레임과 메타 데이터 수집
    df_result, meta_dict = parser.parse(vbo_path)
    
    print(f"📊 파싱 완료! Shape: {df_result.shape}")
    print(f"🛰️ 계측 채널 목록: {list(df_result.columns)}")
    print(f"📅 계측 생성 시간: {meta_dict.get('save_date')}")
```

### 4.2. [시나리오 2] GPS 계측 주파수 및 단위 매핑 검증
```python
# 비공개 헬퍼 함수를 통한 메타데이터 선제 스캔 검증
with open(vbo_path, 'r', encoding='utf-8') as f:
    lines = [f.readline() for _ in range(100)]  # 앞 100줄만 고속 스캔

hz = parser._extract_sample_rate(lines)
units_map = parser._extract_units(lines)

print(f"⚡ VBOX 위성 계측 주파수: {hz} Hz")
print(f"📏 속도 채널 단위: {units_map.get('velocity', 'km/h')}")
```

### 4.3. [시나리오 3] 커스텀 인코딩 및 강제 헤더 라인 지정을 통한 대용량 파일 복구
```python
# 헤더에 노이즈 라인이 많아 인덱스가 밀린 깨진 VBO 파일 대응
broken_vbo_path = "D:/test_data/corrupted_device_log.vbo"

# 150줄 이내에 헤더 섹션이 무조건 끝남을 보장하고 cp949 인코딩으로 수동 강제 디코딩
df_recovered, meta = parser.parse(
    file_path=broken_vbo_path,
    head_end_line=150,
    encoding='cp949'
)

print(f"✅ 깨진 파일 복구 완료! 복구된 계측 행수: {len(df_recovered)}")
```
