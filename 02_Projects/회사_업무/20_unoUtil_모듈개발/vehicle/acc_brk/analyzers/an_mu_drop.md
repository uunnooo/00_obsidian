---
id: "an_mu_drop_20260920"
title: "an_mu_drop (노면 마찰력 저하 및 제동거리 손실 정량 분석) 상세 매뉴얼"
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
  - 마찰저하
  - 제동
project_link: "[[unoUtil]]"
---

# 🚗 an_mu_drop (노면 마찰력 저하 및 제동거리 손실 정량 분석) 상세 매뉴얼

> [!ABSTRACT] 📌 개요
> 수막현상(Hydroplaning) 또는 노면 성상 급변으로 인해 고속 제동 구간에서 바퀴 접지 마찰력이 순간적으로 상실되는 분기 임계 속도(Mu-Drop Split Velocity)를 기계학습(K-Means & Decision Tree) 기법으로 탐색하고, 정상 대비 접지 한계 저하로 인해 증가(유실)된 손실 제동거리(Dist. Loss, m)를 수치 적분하여 정량 진단하는 핵심 거동 분석기 모듈입니다.
> 
> * **상위 대시보드**: [[00_unoUtil_모듈개발_대시보드]]

---

## 1. ⚙️ 공학적 원리 및 수치 연산식

### 1.1. 머신러닝 기반 마찰 급변 임계점 판정 (Mu-Drop Split)
차량이 수막 노면에 진입 시 타이어 배수 한계를 초과하면서 휠 슬립 가속도(Wheel Acceleration)가 급격한 하강 피크(격변 진동)를 형성합니다.
- **K-Means 군집화**: 고해상도 휠 가속 시계열 데이터를 마찰 접지 정상 상태(Normal)와 마찰 저하 특이 상태(Mu-Drop Active)로 이진 분류형 클러스터링을 실시합니다.
- **의사결정나무 (Decision Tree)**: 분류 경계선을 차속 시간축과 결속하여, 마찰 탈조가 발생한 정확한 **임계 분기 차속(Threshold Velocity, kph)**을 수학적으로 규명합니다.

### 1.2. 손실 제동거리 정량 수치 적분 (Braking Distance Loss)
임계 차속 이상 구간에서의 불완전한 감속 기울기와 임계점 이하 노면 접착 회복 후의 감속 가속도 기울기 차이점을 수학적으로 추적합니다.
- 이상적인 완전 접지 감속 시나리오와 수막 탈조 마찰 저하 실측 시나리오 간의 속도-거리 미적분 적분 면적 연산을 계산하여, **마찰 손실로 인해 추가 발생된 순수 오버런 제동 손실 거리(m)**를 누적 산출합니다.

---

## 2. ⚙️ 주요 API 및 프로퍼티 명세

### `AN_MU_DROP(obj_tire, **kwargs)`
* **기능**: 상위 타이어 분석기 인스턴스와 결속하여 분석기 메모리 상태를 초기화합니다 (순환 참조 방지 `weakref` 수립).

#### 핵심 프로퍼티:
* **`df` (pd.DataFrame)**: [온디맨드 자동 복원] 군집화 라벨과 판정 분기가 매핑 완료된 주행 물리 시계열 데이터프레임.
* **`summary` (pd.DataFrame)**: [온디맨드 자동 복원] 휠 전체 평균 마찰 저하 손실 제동거리 및 임계속도 등의 콤팩트 요약 테이블.
* **`summary_detail` (pd.DataFrame)**: [온디맨드 자동 복원] 바퀴 포지션별(FL, FR 등) 개별 분기 임계 속도 및 감속 세그먼트 상세 요약 통계 테이블.
* **`has_data` (bool)**: 현재 휘발성 대용량 원본 시계열(`_df`) 캐시가 RAM 상에 보존되어 있는지 판별하는 플래그.

#### 핵심 메서드:
* **`analysis(col_mudrop_wheelacc=None, **kwargs)`**: 휠 가속 채널을 입력받아 K-Means 군집화 및 수막 감속 분기 정량 수치 적분을 수행합니다.
* **`clear_cache()`**: 대용량 `_df` 캐시를 소거하여 RAM을 즉시 확보합니다 (메모리 누수 원천 방어).

---

## 💻 3. 호출 예제 (Usage Example)

```python
# 상위 VT_ACCBRK_TIRE 인스턴스인 'tire'로부터 접근 호출
# 1. 전륜 FL, FR 휠 가속 센서 데이터를 기준으로 수막현상 / 마찰저하 탐색 가동
tire.mudrop.analysis(col_mudrop_wheelacc=['WAFL', 'WAFR'])

# 2. 계산 완료된 통합 손실 제동거리 요약 결과 조회 (예: md_DistLoss)
df_summary = tire.mudrop.summary
print(df_summary)

# 3. 휠 포지션별(FL, FR) 개별 분기 수막 한계 속도 조회
df_detail = tire.mudrop.summary_detail
print(df_detail)

# 4. 분석 연산 작업이 완료되었으므로 대용량 시계열 군집화 데이터프레임 캐시 소거 (RAM 클린업)
tire.mudrop.clear_cache()
```

---

## 4. 📝 이중 동기화 프로토콜 준수사항
- 이 매뉴얼 파일(`an_mu_drop.md`)은 동일 로컬 디렉터리(`unoUtil/vehicle/ACCBRK/analyzers/`) 내에 1:1 대응하여 보관되며, 최종 작업 완료 선언 시 옵시디언 볼트로 일괄 배치 동기화 처리됩니다.
