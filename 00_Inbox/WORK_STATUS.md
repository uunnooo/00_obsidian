---
id: "WORK_STATUS_2026-09-28"
title: "unoUtil v3.3 TireCurve 전략 패턴 및 Bicycle Model 전면 표준화 완결 감사 보고서"
type: audit
date: 2026-09-28
author: uno & Gemini
status: 완료
tags:
  - unoUtil
  - 감사보고서
  - models
  - TireCurve
  - BicycleModel
  - MagicFormula
  - SSOT
  - 리팩토링
  - 대시보드
  - v3.3
---

# 🏁 unoUtil v3.3 TireCurve 전략 패턴 및 Bicycle Model 전면 표준화 완결 감사 보고서

> **일자**: 2026-09-28  
> **프로젝트**: 사내 실차 시험 통합 프레임워크 unoUtil (`refactor-v2`)  
> **수행자**: uno & Gemini  
> **최종 상태**: ✅ **100% 무결성 검증 통과 (Exit Code 0), TireCurve 전략 패턴 및 2-DoF Bicycle Model 정규화 완료**

---

## 🎯 1. 주요 작업 목적 및 달성 내역

오늘 세션에서는 사용자님의 탁월한 아키텍처 제안에 따라:
1. **타이어 특성 곡선 총괄 클래스 `TireCurve` 구축**:
   - 특정 수식에 얽매이지 않고 임의의 수학 모델(`model`)과 최적화 알고리즘(`method`)을 주입(Dependency Injection)받아 처리하는 **전략 패턴(Strategy Pattern)** 기반 단일 클래스 설계.
   - 종방향(제동/구동력, $F_x$)과 횡방향(코너링포스, $F_y$) 해석을 일원화하고 강성(`stiffness`), 피크치(`peak_value`), 피크슬립(`peak_slip`)을 단 1개의 일관된 인터페이스로 제공.
2. **2자유도 횡운동 지배 수식의 국제 표준 정규화 (`bicycle_model.py`)**:
   - 모호했던 `dynamic_formula` 명칭을 전 세계 자동차공학(Vehicle Dynamics) 공식 학술/산업 표준인 **자전거 모델(`bicycle_model.py`, `BicycleModel`)**로 정합 완료.
   - 물리 브릿지 파일 무잔존 원칙(Zero Physical Legacy Law)을 준수하여 디스크 찌꺼기 파일 0개 달성.
3. **Pacejka Magic Formula 단일 진실 공급원(SSOT) 확립**:
   - 도메인별로 흩어져 있던 MF 수식을 `calc_magic_formula` 단일 코어로 일원화.
4. **100% 무중단 하위 호환성 및 무결성 검증 전원 통과**:
   - `test_structure_integrity.py` 11대 도메인 및 36개 세부 레거시 경로 **100% PASS (Exit Code 0)**.

---

## 🛠️ 2. 세부 집행 내역 (Changelog)

### 1) models/tire_curve.py 신설 (`TireCurve`)
* 모델 주입: `'magic_formula'`(기본값) 또는 사용자 정의 함수 `f(x, *params)` 지원.
* 전략 주입: `'least_squares'`, `'combiner'`(직선 결합), `'optimizer'`(베이지안), `'ax'` 지원.
* 물리 프로퍼티: `stiffness` ($B \cdot C \cdot D$), `peak_value` ($D$), `peak_slip` (최대력 발생점) 자동 연산.
* 편의 팩토리: `fit_magic_formula(x, y, method=...)` 단 1줄 피팅 함수 제공.

### 2) models/mathematical/bicycle_model.py 승격 (`BicycleModel`)
* 2-DoF 차량 횡운동 정상 상태 요레이트 연산(`calc_bicycle_yaw_rate`) 및 목적함수 RSS(`calc_objective_bicycle_yaw_rate`).
* `BicycleModel` 클래스 캡슐화 완료.
* 구버전 호환 별칭: `calc_unit_yaw_rate`, `UnitYawRate`, `calc_objective_unit_yaw_rate`, `ObjectiveFunc_UnitYawRate` 100% 보존.

### 3) models/fitting/fit_least_squares.py 정합 (`EstimatorLeastSquares`)
* Scipy `least_squares` 기반 가중치 마스크(`wm`, `wg`), 경계 조건(`bounds`), Huber/Soft L1 loss 지원.
* 구버전 호환: `EstimatorMF`, `estimatorMF`, `fit_mf_ax` 100% 보존.

### 4) 1:1 마크다운 기술 매뉴얼 3종 신규 배포
* `models/tire_curve.md` (타이어 특성 곡선 통합 클래스 매뉴얼)
* `models/mathematical/bicycle_model.md` (2-DoF 자전거 모델 매뉴얼)
* `models/fitting/fit_least_squares.md` (비선형 최소자승 추정기 매뉴얼)

### 5) 옵시디언 볼트 MOC 대시보드 갱신
* `models/00_models_대시보드.md` 전면 갱신 (전략 패턴 Mermaid 다이어그램, 1:1 링크 정합).
* `00_unoUtil_모듈개발_대시보드.md` 상단 타임테이블 `v3.3` 확정 반영.

---

## 🧪 3. 최종 무결성 검증 결과 (`test_structure_integrity.py`)

* ✅ **11대 공식 도메인 패키지 임포트**: **100% PASS**
* ✅ **핵심 클래스 정합성 (`TireCurve`, `BicycleModel`, `TireMagicFormula`, `EstimatorMF`, `CurveCombiner`, `MinimizeEstimator`)**: **100% PASS**
* ✅ **TireCurve 실측 자가 피팅 및 프로퍼티 연산**: **100% PASS (Stiffness: 14.30, Peak: 1.10)**
* ✅ **SSOT 동일성 단언 검증**: **100% PASS**
* ✅ **36개 구버전 레거시 경로 가상 리다이렉션**: **100% PASS (Exit Code 0)**

---
**보고서 작성 완료**: 2026-09-28  
**기록 보관소**: `D:\00_obsidian\00_Inbox\WORK_STATUS.md`
