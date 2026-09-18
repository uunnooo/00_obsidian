---
id: "scaler_20260918"
title: "scaler (데이터 정규화 및 표준화) 상세 매뉴얼"
type: resource
category_main: 회사_업무
category_sub: 개발매뉴얼
date: 2026-09-18
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - 신호처리
  - 스케일러
  - 정규화
  - 매뉴얼
project_link: "[[unoUtil]]"
---

# 📐 scaler (데이터 정규화 및 표준화) 상세 매뉴얼

> [!ABSTRACT] 📌 개요
> 머신러닝 모델 입력 및 다축 센서 융합을 위해 데이터의 스케일을 정규화(`0~1`), 표준화(Z-score), 또는 로버스트 스케일링하는 모듈입니다.  
> 
> * **영구 공학 지식 레퍼런스**: [[25_실차_신호처리_및_시계열_데이터_정제_공학]]
> * **상위 대시보드**: [[00_post_process_대시보드]] | [[00_unoUtil_모듈개발_대시보드]]

---

## 1. ⚙️ 주요 API 규격

### 1.1. `scale_data(data, method='minmax', feature_range=(0, 1), ...)`
* **기능**: 데이터프레임의 수치형 열들에 대해 지정된 스케일링을 적용합니다.
* **지원 방식 (`method`)**:
  - `'minmax'`: 지정된 범위(기본값 0~1)로 선형 변환.
  - `'standard'`: 평균 0, 표준편차 1로 표준화.
  - `'robust'`: 중앙값과 IQR 기반으로 이상치에 강건한 스케일링.
* **하위 호환 별칭**: `SP_Normal`
