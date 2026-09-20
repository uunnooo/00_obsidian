---
id: "q3_hkt_rnd_dw__test__tb_th_req_item_bas_20260920"
title: "q3_hkt_rnd_dw__test__tb_th_req_item_bas (시험 항목 상태 및 조건 규격 정의) 상세 매뉴얼"
type: resource
category_main: 회사_업무
category_sub: 개발매뉴얼
date: 2026-09-20
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - 매뉴얼
  - 데이터베이스
  - SQL
  - 쿼리
project_link: "[[unoUtil]]"
---

# 🗄️ q3_hkt_rnd_dw__test__tb_th_req_item_bas (시험 항목 상태 및 조건 규격 정의) 상세 매뉴얼

> [!ABSTRACT] 📌 개요
> Databricks RND DW의 시험 항목 기본 테이블 `tb_th_req_item_bas`에서 시험일정 계획, 확인 상태, 시험 그룹/방법 및 타이어 물리 장착 상태(림 폭, 인치, 공기압) 컬럼 리스트를 상수 문자열로 정의하는 데이터 맵핑 모듈입니다.
> 
> * **상위 대시보드**: [[00_unoUtil_모듈개발_대시보드]]

---

## 1. ⚙️ 데이터베이스 정의 컬럼 명세

| 물리 컬럼명 | 논리 한글 정의 | 비고 |
| :--- | :--- | :--- |
| `RQST_CD` | 의뢰 코드 | 연동 조인 외래 키 |
| `PL_DTM` | 계획 일시 | 시험 가동 수립 스케줄 시점 |
| `CNFRMDTM` | 확인일시 | RND 시험 주관자 승인 확인 시점 |
| `RSDTM` | 결과일시 | 최종 데이터 계측 결과 기입 시점 |
| `TST_GR_CD` | 시험 그룹 코드 | 그룹 분류 코드 (예: 제동, 핸들링 등) |
| `TST_GRNM` | 시험 그룹명 | 그룹 분류 한글명 |
| `TST_ITEM_CD` | 시험 항목 코드 | 개별 항목 코드 (예: ABS 제동 등) |
| `TST_ITMNM` | 시험 항목명 | 개별 항목 한글명 |
| `TST_MTHD_CD` | 시험 방법 코드 | 실차/기계 시험 구분 코드 |
| `TST_MTNM` | 시험 방법명 | 실차 시험 상세 기법명 |
| `TST_CNDTNM_VAL` | 시험 조건번호 값 | 셋업 압력 및 조건 지정값 |
| `TST_CNDTNN` | 시험 조건명 | 노면 조건 및 상세 구분 기술 |
| `RLVHT_ITEM_ST_ID` | 실차시험 항목 상태 아이디 | 진행 단계 상태 플래그 (접수/종료 등) |
| `TRFTST_ST` | 시험용타이어 상태 | 타이어 장착 및 가류 상태 비고 |
| `TRS_TITM_OBJ_TBLK` | 시험항목 객체 테이블키 | 세부 조인 맵핑 외래 키 |
| `TRS_SPEC_OBJ_TBLK` | 규격 객체 테이블키 | PLM 타이어 규격 매핑 외래 키 |

---

## 💻 2. 호출 예제 (Usage Example)

```python
from unoUtil.database.q3_hkt_rnd_dw__test__tb_th_req_item_bas import tb_th_req_item_bas

# q3 모듈에 정의된 항목 상태 컬럼 리스트를 활용한 SQL SELECT 문 빌드
query = f"SELECT {tb_th_req_item_bas} FROM hkt_rnd_dw.test.tb_th_req_item_bas LIMIT 10"
print(query)
```

---

## 3. 📝 이중 동기화 프로토콜 준수사항
- 이 매뉴얼 파일은 동일 로컬 디렉터리(`unoUtil/database/`) 내에 1:1 대응하여 보관되며, 최종 작업 완료 선언 시 옵시디언 볼트로 일괄 배치 동기화 처리됩니다.
