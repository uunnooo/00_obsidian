# 🧭 CorrectFactors 보정 계수 및 팩터 브릿지 매뉴얼 (correct_factors.md)

## 📌 1. 개요 및 목적 (Overview)
`correct_factors` 모듈은 실차 제동 및 가속 시험 데이터의 환경(온도, 노면 마찰계수) 보정 팩터 연산 엔진인 `correct` 모듈의 주요 클래스와 함수를 외부 및 v1 레거시 코드에 안정적으로 노출하기 위한 **호환 브릿지 모듈**입니다.

사내 레거시 분석 스크립트(`_Correct_factors_`)와의 무중단 연동성을 보장하며, 최신 v2 아키텍처의 `Correct` 클래스 및 표준 팩터 연산 함수를 직교적으로 제공합니다.

---

## 🛠️ 2. 노출 심볼 및 API 명세 (Exported Symbols)

| 심볼명 | 구분 | 매핑 소스 모듈 | 설명 |
| :--- | :---: | :--- | :--- |
| **`Correct`** | 클래스 | `unoUtil.vehicle.acc_brk.correct.Correct` | 온도 보정 계수($K_{temp}$) 및 환경 보정 수치 연산 총괄 클래스 |
| **`CORRECT`** | 클래스 별칭 | `unoUtil.vehicle.acc_brk.correct.Correct` | v1 오리지널 레거시 대문자 클래스 별칭 (100% 호환) |
| **`correct_factor_basic`** | 함수 | `unoUtil.vehicle.acc_brk.correct.correct_factor_basic` | 기본 선형/비선형 온도 보정 계수 산출 표준 함수 |

---

## 🎯 3. v1 레거시 하위 호환성 단일 기준 원칙 (Single Baseline Law)
* **v1 오리지널 레거시 100% 보장**:
  - `from unoUtil.vehicleTest._Correct_factors_ import CORRECT` 등 과거 작성된 시험 자동화 스크립트의 심볼 임포트를 단일 기준(Single Baseline)으로 지원합니다.
* **과도기적 중간 명칭 배제**:
  - v2 표준은 `unoUtil.vehicle.acc_brk.correct`를 단일 진실 공급원(SSOT)으로 하며, 본 모듈은 레거시 네임스페이스 라우팅만을 깔끔하게 수행합니다.

---

## 💻 4. 실무 활용 예제 (Usage Example)
```python
# 1. 최신 v2 표준 임포트
from unoUtil.vehicle.acc_brk.correct_factors import Correct

# 2. 보정 인스턴스 생성 및 계수 산출
corrector = Correct()
k_factor = corrector.calc_temp_factor(temp_surface=25.0, temp_refer=20.0)
print(f"✅ 노면 온도 보정 팩터: {k_factor:.4f}")

# 3. v1 레거시 스타일 임포트 호환
from unoUtil.vehicle.acc_brk.correct_factors import CORRECT
legacy_obj = CORRECT()
```

---
**Last Updated**: 2026-09-26  
**Module**: `unoUtil.vehicle.acc_brk.correct_factors`  
**Standard**: unoUtil Clean Architecture v2.0
