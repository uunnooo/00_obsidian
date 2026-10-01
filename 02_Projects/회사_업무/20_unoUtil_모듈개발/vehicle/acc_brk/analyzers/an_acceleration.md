---
id: "an_acceleration_20260920"
title: "an_acceleration (속도 대역별 가속도 분산 상태 및 물리적 거동 진단) 상세 매뉴얼"
type: resource
category_main: 회사_업무
category_sub: 개발매뉴얼
date: 2026-09-20
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - 매뉴얼
  - 분석기
  - 가속도
  - 제동
project_link: "[[unoUtil]]"
---

# 🚗 an_acceleration (속도 대역별 가속도 분산 상태 및 물리적 거동 진단) 상세 매뉴얼

> [!ABSTRACT] 📌 개요
> 실차 제동 및 가속 시험 시계열 데이터로부터 특정 타겟 속도 구역(예: 80km/h ➔ 10km/h) 내에 포진된 가속도(Ax, Ay) 값을 속도 구간 단위(예: 10kph, 5kph 단위)로 정교하게 격자 분할 수집하고, 각 속도 대역별 평균 가속도 및 분산 통계량을 산출하여 타이어 그립 접지 특성과 주행 안정성을 정량 추정하는 핵심 분석 모듈입니다.
> 
> * **상위 대시보드**: [[00_unoUtil_모듈개발_대시보드]]

---

## 1. ⚙️ 코어 알고리즘 및 캐싱 모델

### 1.1. 속도 대역별 격자 분할 통계 (Speed Segmenting)
시험 속도 상한값(예: 100kph)에서 하한값(예: 0kph) 사이를 사용자가 정의한 구간 크기(`interval` [kph])에 따라 분할합니다.  
각 속도 윈도우 슬롯에 걸친 제동 종방향 가속도($A_x$) 데이터포인트들을 수집하여 다음을 산출합니다:
- **평균 가속도 ($Acc_{mean}$)**: 해당 속도 영역에서의 실질적 제동 감속 효율성(g) 대조.
- **가속도 편차 ($Acc_{std}$)**: 노면 굴곡 또는 슬립 진동에 의한 거동 흔들림(진동량) 정량 진단.

### 1.2. 하이브리드 메모리 캐싱 모델 (RAM Lifecycle Management)
고해상도 실차 계측 데이터(수십만 포인트)의 시계열 복원 및 결합 연산 병목을 예방하면서도 메모리 누수를 원천 차단하기 위해 **하이브리드 캐싱 아키텍처**를 채택하고 있습니다.
- **휘발성 대용량 캐시 (`_df`)**: 프로퍼티 `df` 접근 시 단 한 번 계산되어 로딩되며, 반복적인 플롯/비교 연산 세션 동안 RAM 상에 유지됩니다.
- **영구 요약 통계 (`_summary`)**: 속도 대역별 콤팩트 통계 요약표는 메모리에 영구 유지되며, 최종 보고서 연동 및 직렬화 대상이 됩니다.
- **캐시 해제 (`clear_cache()`)**: 대화식 세션 또는 분석 연산이 완료되는 시점에 명시적으로 RAM 소거를 수행해 가상 메모리 크기를 원천 다이어트합니다.

---

## 2. ⚙️ 주요 API 및 프로퍼티 명세

### `AnAcceleration(obj_tire, level=None, **kwargs)`
* **기능**: 상위 타이어 분석기 인스턴스와 결속하여 분석기 메모리 공간 및 로깅 레벨을 초기화합니다. (상위 분석기와의 결합은 순환 참조 방지를 위해 약한 참조 `weakref` 처리됨).
* **인자**:
  - `obj_tire` (`VTAccBrkTire`): 상위 타이어 분석기 인스턴스.
  - `level` (`Union[int, str, None]`): 로깅 레벨 (기본값: `None`, 부모 `obj_tire.level` 자동 상속).
  - `**kwargs`: `print`, `flag_print` (하위 호환, `level`로 자동 매핑).

#### 핵심 프로퍼티:
* **`df` (pd.DataFrame)**: [온디맨드 자동 복원] 세션별 차속 대역 매핑 완료된 종가속도 시계열 원본 데이터프레임.
* **`summary` (pd.DataFrame)**: [온디맨드 자동 복원] 속도 구간별 평균 가속도 요약 통계 테이블.
* **`has_data` (bool)**: 현재 휘발성 대용량 원본 시계열(`_df`) 캐시가 RAM 상에 적재되어 있는지를 나타내는 정합성 플래그.
* **`level`**: 현재 적용 중인 로깅 레벨.
* **`logger`**: 피클 직렬화 안전성을 보장하는 동적 바인딩 로거.

#### 핵심 메서드:
* **`analysis(interval=10.0, level=None, **kwargs)`**: 실계측 원본 데이터프레임 필터링을 수행하고 지정 속도 인터벌 단위로 통계 계산을 전개합니다.
* **`clear_cache()`**: 대용량 `_df` 캐시를 소거하여 RAM을 즉시 해제합니다.

---

## 💻 3. 호출 예제 (Usage Example)

```python
# 상위 VT_ACCBRK_TIRE 인스턴스인 'tire'로부터 접근 호출
# 1. 10kph 단위 속도 대역별 제동 감속 효율 및 편차 분석 가동
tire.acceleration.analysis(interval=10.0)

# 2. 계산이 완료된 요약 통계 테이블 획득 및 조회
df_summary = tire.acceleration.summary
print(df_summary)

# 3. 휘발성 고용량 세그먼트 데이터프레임 접근 (메모리 로딩 확인)
print(f"현재 RAM 적재 상태: {tire.acceleration.has_data}")
df_time_series = tire.acceleration.df

# 4. 리포팅 연동 및 차트 작성이 완료되었으므로 대용량 원본 캐시 RAM 소거 단행 (RAM 누수 방어)
tire.acceleration.clear_cache()
print(f"클린업 후 RAM 적재 상태: {tire.acceleration.has_data}")  # False 반환
```

---

## 4. 📝 이중 동기화 프로토콜 준수사항
- 이 매뉴얼 파일(`an_acceleration.md`)은 동일 로컬 디렉터리(`unoUtil/vehicle/ACCBRK/analyzers/`) 내에 1:1 대응하여 보관되며, 최종 작업 완료 선언 시 옵시디언 볼트로 일괄 배치 동기화 처리됩니다.
