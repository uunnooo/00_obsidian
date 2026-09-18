---
id: "utils_dataframe_utils_20260918"
title: "dataframe_utils (데이터프레임 전처리 및 비율 연산) 상세 매뉴얼"
type: resource
category_main: 회사_업무
category_sub: 개발매뉴얼
date: 2026-09-18
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - 유틸리티
  - 데이터프레임
  - 매뉴얼
project_link: "[[unoUtil]]"
---

# 📊 dataframe_utils (데이터프레임 전처리 및 비율 연산) 상세 매뉴얼

> [!ABSTRACT] 📌 개요
> 수치형 컬럼 형변환(`astype_float`), 그룹별 평균 집계(`agg_mean`), 기준값 대비 비율/지수 연산(`calc_ratio`)을 전담하는 고속 데이터프레임 헬퍼 모듈입니다.  
> 
> * **상위 대시보드**: [[00_utils_대시보드]] | [[00_unoUtil_모듈개발_대시보드]]

---

## 1. ⚙️ 주요 API 규격

### 1.1. `astype_float(data, columns=None, fillna=0.0, ...)`
* **기능**: 데이터프레임의 지정 컬럼을 부동소수점(`float64`)으로 안전하게 강제 변환하며 결측치를 처리합니다.

### 1.2. `agg_mean(data, group_by, target_columns, ...)`
* **기능**: 특정 기준 열(예: 타이어 코드, 시험 회차)로 그룹화하여 평균 요약 테이블을 산출합니다.

### 1.3. `calc_ratio(data, ref_value, target_column, ...)`
* **기능**: 기준 시험값(Control Tire) 대비 평가 타이어(Test Tire)의 성능 지수(Index = 100 기준)를 계산합니다.
* **하위 호환 별칭**: `CalRatio`
