# 🧭 AnSlipModeSkewness 슬립-가속도 2D 왜도 분포 분석기 매뉴얼 (an_skewness.md)

## 📌 1. 개요 및 목적 (Overview)
`an_skewness` 모듈은 실차 제동 중 ABS 작동 상태에서 **휠 슬립률(Wheel Slip) 대 전후 감속도(Deceleration)** 2차원 공간 상의 확률 밀도 지형을 형성하고, 물리적 점착 정점인 최빈점(Mode)과 실제 제어 중심인 평균점(Mean) 간의 **기하학적 오차 변위 벡터(Shortest Distance, $\Delta\text{Slip}$, $\Delta\text{Decel}$)**를 연산하여 타이어-ABS 매칭 안정성을 평가하는 분석 엔진입니다.

`BaseMemory` 기반의 하이브리드 캐싱 모델을 적용하여 대용량 2D 히트맵(`_df_heatmap`) 및 시계열(`_df`)을 안전하게 관리합니다.

---

## 🛠️ 2. 핵심 클래스 및 API 명세 (API Specifications)

### 2.1. `AnSlipModeSkewness` 클래스
```python
class AnSlipModeSkewness(BaseMemory):
    def __init__(self, obj_tire: Any, **kwargs: Any) -> None: ...
```

* **상속**: `unoUtil.vehicle.acc_brk.base_memory.BaseMemory`
* **주요 속성(Properties)**:
  * `df` (`pd.DataFrame`): 슬립률-가속도 필터링 시계열 데이터프레임 (휘발성 캐시).
  * `df_heatmap` (`pd.DataFrame`): 2D 격자 확률 밀도 수치가 계산된 매트릭스 데이터프레임 (휘발성 캐시).
  * `summary` (`pd.DataFrame`): 2D 최단 오차 변위 및 편차량 최종 요약 테이블 (영구 보존).
  * `summary_detail` (`pd.DataFrame`): 각 휠별 왜도 성분 벡터 상세 데이터프레임 (영구 보존).
  * `has_data` (`bool`): 캐시 적재 여부.
* **주요 메서드**:
  * **`analysis(slip_mode_vel_range=None, col_slip_mode_wheelslip=None, **kwargs)`**:
    * 2차원 커널 확률 밀도를 구성하고 Mode 대비 Mean 편차 거리를 기하 연산.
  * **`clear_cache()`**:
    * 히트맵 및 시계열 캐시를 즉시 비워 대용량 메모리 점유 방지.

---

## 🎯 3. v1 레거시 하위 호환성 단일 기준 원칙 (Single Baseline Law)
* **v1 오리지널 레거시 100% 보장**:
  - `AN_SLIP_MODE_SKEWNESS = AnSlipModeSkewness` 별칭을 단일 기준으로 제공합니다.
* **과도기적 미완성 코드의 레거시 취급 배제**:
  - `AnSlipModeSkewness` 단일 표준 클래스를 중심으로 직교화되어 있습니다.

---

## 💻 4. 실무 활용 예제 (Usage Example)
```python
from unoUtil.vehicle.acc_brk.vt_acc_brk_tire import VTAccBrkTire

# 1. 타이어 인스턴스 준비
tire = VTAccBrkTire(tire_name="TestTire_B")

# 2. 80km/h ~ 20km/h 구간 슬립-가속도 왜도 분석 기동
tire.slip_mode_skewness.analysis(
    slip_mode_vel_range=[80, 20],
    col_slip_mode_wheelslip="front"
)

# 3. 최빈점 대비 평균점 오차 거리 및 요약 확인
print("📊 2D 왜도 오차 거리 요약:")
print(tire.slip_mode_skewness.summary)

# 4. 메모리 캐시 정리
tire.slip_mode_skewness.clear_cache()
```

---
**Last Updated**: 2026-09-26  
**Module**: `unoUtil.vehicle.acc_brk.analyzers.an_skewness`  
**Standard**: unoUtil Clean Architecture v2.0
