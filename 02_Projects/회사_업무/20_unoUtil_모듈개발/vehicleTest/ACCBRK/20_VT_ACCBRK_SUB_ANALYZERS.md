---
id: "work_20260910_VT_ACCBRK_SUB_ANALYZERS"
title: "20_VT_ACCBRK_SUB_ANALYZERS 7대 전문 서브 분석기 모듈"
type: resource
category_main: 회사_업무
category_sub: unoUtil
date: 2026-09-10
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - 매뉴얼
  - VT_ACCBRK
project_link: "[[unoUtil]]"
aliases:
  - "VT_ACCBRK_SUB_ANALYZERS"
  - "20_VT_ACCBRK_SUB_ANALYZERS"
---

> [!NOTE] 🧭 Obsidian 네비게이션 & 시스템 계층
> - **상위 컨테이너**: [[11_VT_ACCBRK_TIRE]] (단일 타이어 동역학 분석 엔진)
> - **최상위 제어기**: [[12_VT_ACCBRK_PROJECT]], [[10_VT_ACCBRK]]
> - **전역 색인 허브**: [[unoUtil]]

# 🔬 VT_ACCBRK 6대 동역학 전문 서브 분석 모듈 가이드

본 문서는 `VT_ACCBRK_TIRE` 내부에 바인딩되어 고정밀 물리량 계산 및 통계 모델링을 수행하는 **6대 전문 서브 분석 모듈**과 기반 클래스(`AN_MEMORY`)의 알고리즘, 파라미터, 활용법을 다룹니다.

---

## 🏛️ 서브 모듈 아키텍처 및 공통 메모리 모델 (`AN_MEMORY`)

모든 서브 분석 모듈은 `AN_MEMORY`를 상속받아 **하이브리드 캐시 라이프사이클**을 공유합니다:
- **`clear_cache()`**: 직렬화 저장(`.tir`, `.pjt`) 시 메모리 점유율을 최소화하기 위해 무거운 원시 시계열 데이터프레임(`_df`)을 캐시에서 비웁니다.
- **`@property df` 온디맨드 자동 복원**: 프로퍼티 호출 시 부모 타이어 인스턴스로부터 필터링된 유효 구간 데이터를 0.001초 내에 지연 복원합니다.

---

## 1. `AN_ACCELERATION` (속도 구간별 가속도 분석)
- **목적**: 전 속도 영역을 일정한 속도 인터벌(`interval`, 기본 10 km/h)로 분할하여 구간별 평균 가속도(G) 및 감쇠 추세를 산출합니다.
- **주요 파라미터**:
  - `interval`: 분할 속도 단위 (km/h, 예: 10.0, 5.0)
- **산출 지표**:
  - `vel_{min}_{max}_acc`: 구간별 가속도 ($g$)
  - `vel_{min}_{max}_acc_std`: 구간별 편차 ($g$)

---

## 2. `AN_SPLIT_SPEED` (고속/저속 속도 분할 분석)
- **목적**: 특정 분할 기준 차속(`vel_split`, 기본 50 km/h)을 기준으로 고속 영역과 저속 영역의 제동 거리 및 가속도를 분리 측정합니다.
- **주요 파라미터**:
  - `vel_split`: 고속/저속 경계 차속 (km/h)
- **산출 지표**:
  - `split_dist_high`, `split_dist_low`: 고속/저속 제동 거리 ($m$)
  - `split_acc_high`, `split_acc_low`: 고속/저속 평균 가속도 ($g$)

---

## 3. `AN_SLIP_PDF` (슬립율 확률 밀도 함수 분석)
- **목적**: 휠 슬립율의 가우시안 커널 밀도 추정(KDE PDF)을 통해 타이어가 어느 슬립 영역에서 최대 점유율을 갖는지 분석합니다.
- **주요 파라미터**:
  - `col_slip_pdf_wheelslip`: 분석 대상 휠 위치
  - `slip_range`: 슬립율 타겟 범위 (%)
  - `bw`: KDE 대역폭
- **산출 지표**:
  - `pdf_mode`: 최빈 슬립율 (%)
  - `pdf_eff_score`: 타겟 슬립 점유 면적비

---

## 4. `AN_MU_DROP` (수막현상 마찰 한계 손실 거리 분석)
- **목적**: 제동 중 노면 마찰력 급감 및 수막현상 천이 지점을 머신러닝(K-Means & Decision Tree)으로 감지하여 늘어난 손실 거리를 추정합니다.
- **주요 파라미터**:
  - `col_mudrop_wheelacc`: 휠 가속도 채널 (기본: WAFL)
  - `int_ncl`: 클러스터 수 (기본: 2)
- **산출 지표**:
  - `mudrop_dist`: 수막현상으로 인한 손실 거리 ($m$)
  - `mudrop_vel`: 마찰 한계 임계 차속 ($km/h$)

---

## 5. `AN_SLIP_MODE_SKEWNESS` (2D 슬립 지형도 및 제어 왜도)
- **목적**: 종가속도와 슬립율의 2D 밀도 지형도를 생성하고 최적 접지점(Mode) 대비 실제 주행 제어점(Mean) 간의 편차 벡터를 추적합니다.
- **주요 파라미터**:
  - `slip_mode_vel_range`: 분석 차속 범위
- **산출 지표**:
  - `skewness_shortest_dist`: 제어 변위 최단거리
  - `skewness_delta_slip`: 최적점 대비 슬립 오차

---

## 6. `AN_RESPONSE` (초기 제동 빌드업 응답성 분석)
- **목적**: 제동 입력 시점(휠 가속도 반응)부터 실제 차량 감속이 형성되는 과도 응답 지연 시간 및 가속도 상승 기울기를 회귀분석합니다.
- **주요 파라미터**:
  - `pre_sec`: 선행 관찰 시간 (초)
  - `response_target`: 감속 개시 임계값 ($g$)
- **산출 지표**:
  - `sys_response_time`: 시스템 응답 지연 시간 (초)
  - `sys_response_dist`: 지연 제동 거리 ($m$)
  - `sys_rising_slope`: 제동 가속도 초기 상승 기울기 ($g/s$)
