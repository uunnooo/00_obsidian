---
id: "WORK_STATUS_20260923_GETDB"
title: "GetDB 실차시험 의뢰/세트 기반 스펙 및 평가결과 통합 연동 모듈 개발 일지"
type: daily_work_status
date: 2026-09-23
author: uno & Gemini
status: 완료
tags:
  - 작업일지
  - GetDB
  - Databricks
  - 데이터베이스
  - 실차시험
---

# 📋 2026-09-23 작업 상태 보고서 (WORK_STATUS)

## 🎯 1. 작업 개요 및 핵심 요구사항
* **배경**: 실차 시험 데이터베이스(Databricks RND DW)에서 시험 결과 및 의뢰 정보와 PLM 타이어 규격 메타데이터를 연결하는 작업 진행.
* **사용자 요구**: 
  1. 의뢰번호(`RQST_CD`)와 타이어세트(`TIRE_SET_VAL`, 예: T1)만 주어졌을 때 스펙코드(`SPEC_CD`)를 탐색하여 PLM 세부 스펙 테이블(`tb_pl_dw_spec_plm_tire_bas`)의 정의된 값만 가져오는 기능.
  2. 스펙키(`PLM_SPEC_OBJ_TBLK`)가 누락된 경우에도 정상 동작하는 안전한 조인 아키텍처 수립.
  3. 실차 시험 결과(제동거리 등)가 존재할 경우 공통 키(`TRS_TITM_OBJ_TBLK`)를 통해 유연하게 결합(LEFT JOIN)할 수 있는 통합 인터페이스 함수 및 모듈 신규 구현.

---

## 🛠️ 2. 신규 생성 모듈 및 주요 아키텍처

### 2.1. `_func_connect_spec_with_req_set.py`
* **함수명**: `connect_spec_with_req_set(req, tire_set=None, target=..., cur=None, **kwargs)`
* **핵심 기능**:
  - `tb_th_rslt_odr_cdn_bas` ➔ `tb_th_req_item_bas` ➔ `tb_th_req_tire_spec_bas` ➔ `tb_pl_dw_spec_plm_tire_bas` 경로 조인.
  - 내부 시스템 스펙키 부재 시에도 `SPEC_CD`를 직접 매개체로 연결하여 데이터 누락 원천 차단.
  - 불필요한 시험 조건 컬럼을 배제하고 `q4`에 정의된 타이어 핵심 설계 규격값만 슬림하게 추출.

### 2.2. `_func_connect_vehicle_test_and_spec.py`
* **함수명**: `connect_vehicle_test_and_spec(req, tire_set=None, table_target=None, ...)`
* **핵심 기능**:
  - `table_target` 미지정 시: 가볍게 시험 항목 메타(`TST_ITMNM`) 및 타이어 세부 스펙만 고속 조회.
  - `table_target` 지정 시: 지정된 평가 테이블(Wet/Dry/Snow 제동 등)의 측정값(제동거리, 감속도 등)을 공통 키(`TRS_TITM_OBJ_TBLK`)로 `LEFT JOIN`하여 결합.
  - 수십 개의 실차 평가 테이블을 개별적으로 탐색하지 않고 단일 함수로 원스톱 처리 가능.

---

## 📚 3. 문서화 및 옵시디언 위키 동기화 내역
1. **1:1 상세 매뉴얼 생성**:
   - `[[connect_spec_with_req_set]]`: 의뢰번호/타이어세트 기반 PLM 세부 스펙 추출 모듈 매뉴얼.
   - `[[connect_vehicle_test_and_spec]]`: 실차 평가 결과 및 PLM 세부 스펙 원스톱 통합 모듈 매뉴얼.
2. **볼트 배포 위치**: `D:\00_obsidian\02_Projects\회사_업무\20_unoUtil_모듈개발\database\`
3. **코드 무결성 검증**: `python -m py_compile` 문법 검증 전수 통과 (Syntax PASS).
