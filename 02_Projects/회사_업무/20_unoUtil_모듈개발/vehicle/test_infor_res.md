# 🧭 TestInfoRes 시험 정보 및 결과 데이터 컨테이너 매뉴얼 (test_infor_res.md)

## 📌 1. 개요 및 목적 (Overview)
`test_infor_res` 모듈은 실차 시험의 **조건/환경 메타데이터(시험의뢰, 차종, 타이어 규격, 노면, 기온 등)**를 체계적으로 관리하고, 시험 분석 후 산출되는 **회차별 상세 데이터, 요약 통계, 전체 통합 지표**를 구조화하여 보관하는 표준 데이터 컨테이너 모듈입니다.

v2 아키텍처에서는 기존 대문자 스네이크 표기(`TEST_INFORMATION`, `TEST_RESULT`)를 Python 공식 표준인 **`TestInformation`**, **`TestResult` (PascalCase)**로 전면 정비하고, 딕셔너리 기반 팩토리 메서드(`from_dict`) 및 메타데이터 일괄 갱신(`update_metadata`) 인터페이스를 표준화하였습니다.

---

## 🛠️ 2. 핵심 클래스 및 구조 명세 (Data Structures)

### 2.1. `TestInformation` (시험 조건 및 메타데이터 컨테이너)
* **목적**: 30여 개 이상의 시험 조건 필드를 통합 관리하고, 분석에 필요한 물리 단위 게인(`gain_ax`, `gain_vel`) 및 단일 행 메타데이터 DataFrame을 자동 구성.
* **주요 메서드**:
  * `from_dict(data: dict) -> TestInformation`: 딕셔너리로부터 유효 필드만 추출하여 인스턴스 안전 생성.
  * `update_metadata(target, info_dict, obj_names=None)`: 상위 분석 인스턴스 및 하위 서브 객체(acc, brk 등)의 메타데이터와 DF 컬럼을 일괄 동기화.

### 2.2. `TestResult` (분석 결과 컨테이너)
* **목적**: 원시 시계열(`df`), 유효 회차 요약(`summary`), 전체 회차 요약(`summary_all`), 상세 회차 지표(`detail`, `detail_all`)를 캡슐화.
* **주요 속성**:
  * `has_data`: 유효 결과 데이터의 존재 여부를 boolean으로 즉시 반환.

---

## 🎯 3. v1 레거시 하위 호환성 단일 기준 원칙 (Single Baseline Law)
* **v1 오리지널 레거시 호환 100% 보장**:
  - `unoUtil.vehicleTest._TEST_INFOR_RES_` 등에서 사용되던 대문자 클래스명 `TEST_INFORMATION`, `TEST_RESULT` 및 레거시 메서드 `_update_metadata`를 하위 호환 별칭으로 100% 제공합니다.
* **과도기적 미완성 코드의 레거시 취급 배제**:
  - v2 개발 과정 중의 임시 파라미터나 불필요한 별칭은 남기지 않고 단일 표준 형태로 정합되었습니다.

---

## 💻 4. 실무 활용 3대 다변화 시나리오 (Multi-case Examples)

### 4.1. [시나리오 1] `TestInformation` 생성 및 단위 게인 자동 산출
```python
from unoUtil.vehicle.test_infor_res import TestInformation

# 1. 시험 조건 인스턴스 생성
info = TestInformation(
    req="REQ-2026-001",
    item="Braking_Dry",
    vehicle_model="Passat B9 Variant",
    unit_ax="g",      # 가속도 단위
    unit_vel="kmh"    # 속도 단위
)

# 2. 자동 계산된 단위 변환 게인 확인
print(f"가속도 게인: {info.gain_ax} m/s^2, 속도 게인: {info.gain_vel:.4f} m/s")
# 3. 1행 메타데이터 데이터프레임 확인
print("메타 DF 컬럼:", info.df.columns.tolist()[:5])
```

### 4.2. [시나리오 2] `from_dict` 팩토리 및 `update_metadata` 일괄 갱신
```python
from unoUtil.vehicle.test_infor_res import TestInformation

# 1. 외부 JSON / Dict 데이터로부터 인스턴스 생성
raw_info = {
    "req": "REQ-2026-002",
    "item": "Acceleration",
    "surface": "Dry Asphalt",
    "unit_ax": "ms2"
}
info_obj = TestInformation.from_dict(raw_info)

# 2. 시험 도중 노면 온도 변경 시 일괄 갱신
TestInformation.update_metadata(target_instance, {"temp_surface": "32.5"})
```

### 4.3. [시나리오 3] `TestResult` 결과 컨테이너 보관 및 v1 레거시 호환
```python
import pandas as pd
from unoUtil.vehicle.test_infor_res import TestResult, TEST_RESULT

# 1. 신규 표준 TestResult 인스턴스 구성
summary_df = pd.DataFrame({"Metric": ["StopDistance", "MFDD"], "Value": [36.2, 8.9]})
result_container = TestResult(summary=summary_df)
print(result_container)

# 2. v1 오리지널 레거시 대문자 클래스 호출 호환
legacy_result = TEST_RESULT(summary=summary_df)
print("v1 레거시 호환 정상:", legacy_result.has_data)
```

---
**Last Updated**: 2026-09-26  
**Module**: `unoUtil.vehicle.test_infor_res`  
**Standard**: unoUtil Clean Architecture v2.0
