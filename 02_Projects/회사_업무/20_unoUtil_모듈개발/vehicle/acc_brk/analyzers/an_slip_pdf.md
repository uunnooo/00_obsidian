# 🧭 AnSlipPdf 휠 슬립률 확률 밀도 함수(PDF) 분석기 매뉴얼 (an_slip_pdf.md)

## 📌 1. 개요 및 목적 (Overview)
`an_slip_pdf` 모듈은 실차 제동 및 가속 시험 데이터에서 **직진 등속 구간의 휠 반경 속도 오차 보정 계수(Gain)**를 자동 도출하고, ABS 제동 중 발생하는 **각 바퀴 슬립률(Slip Ratio)의 시계열 거동을 커널 밀도 함수(Gaussian KDE)**로 모델링하여 최빈 슬립률(Mode), 가중 평균(Mean), 제동 점착 유효 효율 점수(Efficiency Score)를 분석하는 핵심 분석기입니다.

`BaseMemory` 기반의 하이브리드 캐싱을 통해 대용량 슬립 프로파일 시계열(`_df`) 및 PDF 좌표 매트릭스(`_pdf`)를 안전하게 지연 계산하고 `clear_cache()`로 메모리를 즉시 해제합니다.

---

## 🛠️ 2. 핵심 클래스 및 API 명세 (API Specifications)

### 2.1. `AnSlipPdf` 클래스
```python
class AnSlipPdf(BaseMemory):
    def __init__(self, obj_tire: Any, **kwargs: Any) -> None: ...
```

* **상속**: `unoUtil.vehicle.acc_brk.base_memory.BaseMemory`
* **주요 속성(Properties)**:
  * `df` (`pd.DataFrame`): 휠 속도 보정 및 동적 슬립률 시계열 데이터프레임 (휘발성 캐시).
  * `pdf` (`pd.DataFrame`): 슬립률(X축) 대 확률 밀도(Y축) 격자 데이터프레임 (휘발성 캐시).
  * `summary` (`pd.DataFrame`): 최빈 슬립률, 평균, 표준편차, 제동 효율 최종 요약 통계 테이블 (영구 보존).
  * `has_data` (`bool`): 메모리 캐시 적재 여부.
* **주요 메서드**:
  * **`analysis(slip_range=None, col_slip_pdf_wheelslip=None, **kwargs)`**:
    * 휠 속도 센서 오차 자동 보정 및 커널 밀도 분포 추정, 목표 대역(예: 0~20%) 내 점유 효율 산출.
  * **`clear_cache()`**:
    * 시계열 및 PDF 캐시를 즉각 소거하여 RAM 사용량 최소화.

---

## 🎯 3. v1 레거시 하위 호환성 단일 기준 원칙 (Single Baseline Law)
* **v1 오리지널 레거시 100% 보장**:
  - `AN_SLIP_PDF = AnSlipPdf` 별칭을 단일 기준으로 제공합니다.
* **과도기적 미완성 코드의 레거시 취급 배제**:
  - `AnSlipPdf` 단일 표준 클래스를 중심으로 직교화되어 있습니다.

---

## 💻 4. 실무 활용 예제 (Usage Example)
```python
from unoUtil.vehicle.acc_brk.vt_acc_brk_tire import VTAccBrkTire

# 1. 타이어 인스턴스 준비
tire = VTAccBrkTire(tire_name="TestTire_C")

# 2. 전륜 축 중심, 최적 점착 슬립 구간 [8%, 18%] 대역의 점유 효율 분석
tire.slip_pdf.analysis(
    slip_range=[[8.0, 18.0]],
    col_slip_pdf_wheelslip="front"
)

# 3. 최빈 슬립률 및 효율 요약표 확인
print("📊 슬립률 확률 밀도 분석 요약:")
print(tire.slip_pdf.summary)

# 4. 메모리 해제
tire.slip_pdf.clear_cache()
```

---
**Last Updated**: 2026-09-26  
**Module**: `unoUtil.vehicle.acc_brk.analyzers.an_slip_pdf`  
**Standard**: unoUtil Clean Architecture v2.0
