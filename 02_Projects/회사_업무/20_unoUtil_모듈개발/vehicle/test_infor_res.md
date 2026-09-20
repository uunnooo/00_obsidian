# 🧭 test_infor_res 실차 시험 조건 및 분석 결과 표준 컨테이너 매뉴얼 (test_infor_res.md)

## 📌 1. 개요 및 목적 (Overview)
`test_infor_res` 모듈은 실차 시험의 조건 및 시험장에 따른 기하학적 메타 환경을 규정하는 **시험 정보 컨테이너 클래스(`TEST_INFORMATION`)**와, 분석이 완료된 1-Run 시계열 데이터 및 전체 통계 요약 성과를 다계층으로 저장 관리하는 **분석 결과 컨테이너 클래스(`TEST_RESULT`)**를 제공하는 사내 표준 데이터 캡슐화 패키지입니다.

주행 시험 전후로 수집되는 시험자, 타이어 세트명, 외기 온도, 기상 조건, 그리고 센서 보정 게인(Gain) 등의 부가 정보는 단순 변수로 분산되어 관리할 시 분석 연쇄 과정에서 빈번히 유실되거나 엉뚱한 수치와 매핑되는 문제를 안고 있었습니다. 
본 모듈은 이 모든 분산된 조건들을 하나의 데이터 구조로 캡슐화하고 객체 직렬화(`pickle`) 시에도 이력이 손상되지 않도록 정합 가이드를 완벽히 실현하고 있습니다.

---

## 🛠️ 2. 핵심 API 명세 (API Specifications)

### 2.1. `TEST_INFORMATION` 클래스 인터페이스

| 메서드명 / 속성 | 타입 | 설명 |
| :--- | :---: | :--- |
| `set` | `str` | 시험 타이어 세트명 명칭 (예: `'Set_A_Ref'`) |
| `gain_dict` | `Dict[str, float]`| 물리 센서 채널별 보정 스케일 팩터 게인 딕셔너리 (예: `{'Ax': 9.81}`) |
| `add_info_df(df_data)` | `Method` | 분석에 필요한 데이터프레임 내부 메타 구조를 자동으로 분석하여 채널 목록을 연동 추가 |
| `has_data()` | `Method` | 컨테이너 내부에 유효한 시험 정보가 적재되었는지 판별 (True/False) |
| `from_dict(di)` | `classmethod` | JSON 이나 nested dict 로부터 안전하게 시험 정보 인스턴스를 동적 생성 |

### 2.2. `TEST_RESULT` 클래스 인터페이스

| 메서드명 / 속성 | 타입 | 설명 |
| :--- | :---: | :--- |
| `df` | `pd.DataFrame` | 최종 분석 가공 처리가 끝난 1-Run 시계열 데이터프레임 |
| `summary` | `pd.DataFrame` | 해당 회차의 최대 감속도, 제동거리 등 핵심 물리 지표 요약 데이터프레임 |
| `has_data()` | `Method` | 가공 결과가 안전하게 메모리에 적재되어 살아있는지 판별 |

---

## 📋 3. 입력 파라미터 상세 정의 (Arguments)

1. **`set` (`str` - 필수)**:
   - 평가 대상 타이어 세트 고유의 명칭 문자열입니다.
2. **`gain_dict` (`Optional[dict]` - 선택, 기본값: 빈 사전)**:
   - 가속도 채널($g \leftrightarrow \text{m/s}^2$) 등의 단위 변환을 위한 물리 비례 게인 상수 맵입니다.

---

## 💻 4. 실무 활용 예제 (Multi-case Examples)

### 4.1. [시나리오 1] TEST_INFORMATION 생성 및 센서 변환 게인 셋업
```python
from unoUtil.vehicle.test_infor_res import TEST_INFORMATION

# 1. 신형 미쉐린 타이어 시험 세트 정보 및 가속도 센서 중력가속도(9.80665) 변환 게인 셋업
info = TEST_INFORMATION(
    set="Set_B_Michelin",
    gain_dict={"Acc_X": 9.80665}
)

# 2. 객체 정보 접근 검증
print(f"🛰️ 타이어 세트 식별자: {info.set}")
print(f"📏 Acc_X 센서 물리 게인: {info.gain_dict.get('Acc_X')}")
```

### 4.2. [시나리오 2] 중첩 딕셔너리(Nested Dict)로부터 안전한 동적 인스턴스 부활 (from_dict)
```python
# 외부 JSON 이나 PLM 데이터베이스 쿼리로부터 가져온 nested dictionary 정보
db_query_result = {
    "set": "Set_C_Control",
    "gain_dict": {"Brake_Pres": 100.0}
}

# 팩토리 메서드를 기동하여 동적 인스턴스 복원 수행
info_from_db = TEST_INFORMATION.from_dict(db_query_result)
print(f"🛡️ DB 정보 로드 성공! 세트명: {info_from_db.set} (Gain: {info_from_db.gain_dict})")
```

### 4.3. [시나리오 3] 분석 결과 컨테이너(TEST_RESULT)의 데이터 적재 유무 실증 판정
```python
import pandas as pd
from unoUtil.vehicle.test_infor_res import TEST_RESULT

# 가상 분석 완료 데이터프레임
df_analyzed = pd.DataFrame({"Velocity": [80, 40, 0]})
df_summary = pd.DataFrame({"BrakingDist": [36.5], "MF_Score": [0.98]})

# 결과 컨테이너에 적재
result_container = TEST_RESULT(df=df_analyzed, summary=df_summary)

if result_container.has_data():
    print(f"✅ 결과 적재 완료! 제동거리 요약: {result_container.summary['BrakingDist'].iloc[0]} m")
```
