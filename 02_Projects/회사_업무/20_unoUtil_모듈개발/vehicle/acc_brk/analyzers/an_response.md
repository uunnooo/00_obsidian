# 🧭 AnResponse 제어 응답 지연 및 라이징 기울기 분석기 매뉴얼 (an_response.md)

## 📌 1. 개요 및 목적 (Overview)
`an_response` 모듈은 실차 제동(Braking) 및 가속(Acceleration) 시험 데이터에서 제어 입력(유압/페달) 인가 시점부터 실제 각 휠의 감속 개시 시점까지의 **지연 반응 시간(Response Time)**과 가속도가 급격히 솟구치는 **라이징 대역(Rising Slope)의 기울기**를 정량 분석하는 특화 분석기입니다.

`BaseMemory`를 상속하여 하이브리드 캐싱 모델을 적용하였으며, 고용량 시계열 데이터프레임(`_df`)을 지연 평가(Lazy Evaluation)하고 분석 완료 후 `clear_cache()`를 통해 메모리(RAM)를 안전하게 회수합니다.

---

## 🛠️ 2. 핵심 클래스 및 API 명세 (API Specifications)

### 2.1. `AnResponse` 클래스
```python
class AnResponse(BaseMemory):
    def __init__(self, obj_tire: Any, **kwargs: Any) -> None: ...
```

* **상속**: `unoUtil.vehicle.acc_brk.base_memory.BaseMemory`
* **주요 속성(Properties)**:
  * `df` (`pd.DataFrame`): 응답 지연 상태 플래그 및 리샘플링된 시계열 데이터프레임 (휘발성 캐시).
  * `summary` (`pd.DataFrame`): 휠별 지연 시간, 환산 반응 거리, 라이징 기울기 최종 요약 통계 테이블 (영구 보존).
  * `has_data` (`bool`): 메모리 캐시 적재 여부.
* **주요 메서드**:
  * **`analysis(pre_sec=2.0, resample='1ms', col_response_wheelslip=None, response_target=None, rising_target=None, **kwargs)`**:
    * 휠 속도 미분 프로파일과 차량 거동을 정밀 파싱하여 과도 응답 지연성과 라이징 타임/기울기를 연산.
  * **`clear_cache()`**:
    * 대용량 시계열 캐시(`_df`)를 즉시 소거하여 메모리 누수를 차단.

---

## 🎯 3. v1 레거시 하위 호환성 단일 기준 원칙 (Single Baseline Law)
* **v1 오리지널 레거시 100% 보장**:
  - `AN_RESPONSE = AnResponse` 클래스 별칭을 하단에 단일 기준으로 제공합니다.
* **과도기적 미완성 코드의 레거시 취급 배제**:
  - v2 최신 표준인 `AnResponse`를 본체로 하며, 불필요한 과도기적 브릿지 없이 직교적으로 동작합니다.

---

## 💻 4. 실무 활용 예제 (Usage Example)
```python
from unoUtil.vehicle.acc_brk.vt_acc_brk_tire import VTAccBrkTire

# 1. 타이어 분석기 생성 및 데이터 로드
tire = VTAccBrkTire(tire_name="TestTire_A")
# ... 데이터 로드 완료 후 ...

# 2. 제동 응답 지연 분석 기동
tire.response.analysis(
    pre_sec=2.0,
    resample="1ms",
    response_target=[0.05, 0.2], # 0.05g ~ 0.2g 감속 대역
    rising_target=[0.2, 0.8]     # 20% ~ 80% 라이징 기울기 구간
)

# 3. 요약 통계 확인 및 캐시 메모리 회수
print(tire.response.summary)
tire.response.clear_cache() # 시계열 캐시 해제
```

---
**Last Updated**: 2026-09-26  
**Module**: `unoUtil.vehicle.acc_brk.analyzers.an_response`  
**Standard**: unoUtil Clean Architecture v2.0
