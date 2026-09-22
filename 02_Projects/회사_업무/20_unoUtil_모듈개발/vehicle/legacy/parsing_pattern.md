# 🧭 parsing_pattern 채널 패턴 이관 브릿지 매뉴얼 (parsing_pattern.md)

## 📌 1. 개요 및 목적 (Overview)
`parsing_pattern` 모듈은 계측 채널 한글/영문 정합을 처리하던 기존 레거시 함수형 코드를 투명하게 자동 보전하기 위한 **하위 호환성 전용 래퍼 프록시 브릿지 모듈**입니다.

과거 주행 시험 분석 스크립트들은 특정 텍스트 파일의 채널 패턴을 감지할 때 본 모듈의 원형인 `_ParsingPattern_` 라이브러리를 임포트하여 사용했습니다. 
본 모듈은 이 구버전 의존성에 의해 시스템이 다운되는 현상을 완벽히 차단하고, 모든 정식 감지 및 매핑 연산 로직은 차세대 공통 표준 패키지인 **`unoUtil.file_reader.standard_channel_pattern`** 모듈로 안전하게 우회 및 자동 위임 처리하여 무결점 0-Downtime 마이그레이션을 보장합니다.

---

## 🛠️ 2. 핵심 API 명세 (API Specifications)

### 2.1. 위임 브릿지 인터페이스 명세

| 함수명 / 클래스명 | 타입 | 위임 대상 (New Standard API) | 설명 |
| :--- | :---: | :--- | :--- |
| `detect_channel_pattern(...)` | 함수 | `standard_channel_pattern.detect_channel_pattern` | 입력된 채널 목록에서 표준 6대 계측 패턴 검출 위임 |
| `ParsingPattern` | 클래스 | `standard_channel_pattern.StandardChannelPattern` | 구버전 별칭 클래스 포워딩 바인딩 제공 |

---

## 📋 3. 입력 파라미터 상세 정의 (Arguments)

1. **`channels` (`List[str]` - 필수)**:
   - 계측 장비로부터 수집된 물리 원시 채널명 목록입니다.
2. **`**kwargs` (선택)**:
   - 레거시 헝가리안 인자 호환을 위한 매핑 슬롯입니다.

---

## 💻 4. 실무 활용 예제 (Multi-case Examples)

### 4.1. [시나리오 1] 레거시 구문 그대로 채널 패턴 매핑 검출 (무중단 가동)
```python
from unoUtil.vehicle.legacy.parsing_pattern import detect_channel_pattern

# 1. 기존 주피터 노트북에 박제되어 있던 옛날 호출 방식 그대로 기동!
raw_columns = ["Velocity_GPS", "LAT_ACC_VBOX", "Yaw_Rate_Sens"]

# 2. 내부 위임에 의해 신규 file_reader 표준 패턴 인식기로 자동 포워딩 연산됨
standard_cols = detect_channel_pattern(channels=raw_columns)

print(f"🛰️ 변환 완료! 정규화 채널 목록: {standard_cols}")
```

### 4.2. [시나리오 2] 구버전 ParsingPattern 클래스 별칭 인스턴스화 검증
```python
from unoUtil.vehicle.legacy.parsing_pattern import ParsingPattern

# 구버전 명칭의 클래스를 그대로 호출하여 최신 표준 클래스로 가상 로딩
pattern_detector = ParsingPattern()
print(f"🛡️ 하위 호환 가상 로딩 성공! 인스턴스: {pattern_detector}")
```

### 4.3. [시나리오 3] 대규모 컬럼 배치 치환 예외 격리 방어
```python
# 기기 오작동으로 깨져서 들어오는 특이 채널명 에러 격리 방어
weird_columns = ["???", "", "NULL_COL"]

# 비어있는 채널명이 들어와도 내부 예외 가드에 의해 빈 딕셔너리를 반환하며 크래시 예방
safe_result = detect_channel_pattern(channels=weird_columns)
print(f"✅ 예외 가드 작동 완료! 반환 결과: {safe_result}")
```
