# 🧭 AnSplitSpeed 고속/저속 구간 분할 통계 분석기 매뉴얼 (an_split_speed.md)

## 📌 1. 개요 및 목적 (Overview)
`an_split_speed` 모듈은 실차 제동 및 가속 시험 과정에서 설정된 **기준 임계 차속(Split Speed, 기본 50 km/h)**을 기점으로 주행 구간을 **고속 영역(High Region)**과 **저속 영역(Low Region)**으로 분할하고, 각 속도 대역별 **구간 제동 거리(Braking Distance), 지속 시간(Duration Time), 평균 종방향 가속도(Mean Accel)**를 정량 비교 분석하는 특화 분석기입니다.

`BaseMemory`를 상속하여 하이브리드 캐싱 모델을 적용하였으며, 시계열 태깅 데이터프레임(`_df`)을 온디맨드로 지연 연산하고 `clear_cache()`를 통해 메모리 점유를 최소화합니다.

---

## 🛠️ 2. 핵심 클래스 및 API 명세 (API Specifications)

### 2.1. `AnSplitSpeed` 클래스
```python
class AnSplitSpeed(BaseMemory):
    def __init__(self, obj_tire: Any, **kwargs: Any) -> None: ...
```

* **상속**: `unoUtil.vehicle.acc_brk.base_memory.BaseMemory`
* **주요 속성(Properties)**:
  * `df` (`pd.DataFrame`): 원본 시계열에 고속/저속 라벨이 태깅된 데이터프레임 (휘발성 캐시).
  * `summary` (`pd.DataFrame`): 영역별 누적 제동거리 및 평균 가속도 요약 통계 테이블 (영구 보존).
  * `has_data` (`bool`): 메모리 캐시 적재 여부.
* **주요 메서드**:
  * **`analysis(vel_split=50.0, **kwargs)`**:
    * 분할 기준 속도(km/h)를 기준으로 고속/저속 구간 물리량 분할 연산.
  * **`clear_cache()`**:
    * 대용량 시계열 캐시(`_df`)를 즉각 소거.

---

## 🎯 3. v1 레거시 하위 호환성 단일 기준 원칙 (Single Baseline Law)
* **v1 오리지널 레거시 100% 보장**:
  - `AN_SPLIT_SPEED = AnSplitSpeed` 별칭을 단일 기준으로 제공합니다.
* **과도기적 미완성 코드의 레거시 취급 배제**:
  - `AnSplitSpeed` 단일 표준 클래스를 중심으로 직교화되어 있습니다.

---

## 💻 4. 실무 활용 예제 (Usage Example)
```python
from unoUtil.vehicle.acc_brk.vt_acc_brk_tire import VTAccBrkTire

# 1. 타이어 인스턴스 준비
tire = VTAccBrkTire(tire_name="TestTire_D")

# 2. 50km/h 기준 고/저속 영역 분할 분석 기동
tire.split_speed.analysis(vel_split=50.0)

# 3. 영역별 제동거리 및 평균 가속도 요약표 확인
print("📊 고/저속 분할 요약 리포트:")
print(tire.split_speed.summary)

# 4. 메모리 정리
tire.split_speed.clear_cache()
```

---
**Last Updated**: 2026-09-26  
**Module**: `unoUtil.vehicle.acc_brk.analyzers.an_split_speed`  
**Standard**: unoUtil Clean Architecture v2.0
