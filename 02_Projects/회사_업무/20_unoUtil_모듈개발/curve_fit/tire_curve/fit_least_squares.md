---
id: "fit_least_squares"
aliases:
  - fit_least_squares
  - EstimatorLeastSquares
  - EstimatorMF
tags:
  - unoUtil
  - curve_fit
  - tire_curve
  - least_squares
  - MagicFormula
created: 2026-09-29
updated: 2026-09-29
version: v3.3
---

# 🎯 unoUtil.curve_fit.tire_curve.fit_least_squares 기술 매뉴얼

> **패키지 경로**: `unoUtil.curve_fit.tire_curve.fit_least_squares`  
> **역할**: 가중치 마스크 및 Huber loss를 지원하는 Scipy `least_squares` 비선형 추정기  
> **주요 클래스**: `EstimatorLeastSquares`, `EstimatorMF` (호환 별칭)

---

## 📌 1. 개요

`fit_least_squares.py`는 Scipy의 `scipy.optimize.least_squares` 엔진을 기반으로,
1. 초기 구간 가중치 마스크(`wm`, `wg`)
2. 이상치(Outlier)에 강건한 Huber / Soft L1 손실 함수
3. 물리적 경계 조건(`bounds`)
을 통합 지원하는 타이어 비선형 최소자승 최적화 엔진입니다.
