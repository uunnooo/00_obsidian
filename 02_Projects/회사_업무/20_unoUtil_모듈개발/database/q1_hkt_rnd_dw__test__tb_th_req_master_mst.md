---
id: "q1_hkt_rnd_dw__test__tb_th_req_master_mst_20260920"
title: "q1_hkt_rnd_dw__test__tb_th_req_master_mst (시험의뢰 마스터 테이블 컬럼 정의) 상세 매뉴얼"
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

# 🗄️ q1_hkt_rnd_dw__test__tb_th_req_master_mst (시험의뢰 마스터 테이블 컬럼 정의) 상세 매뉴얼

> [!ABSTRACT] 📌 개요
> Databricks RND DW의 시험의뢰시스템 마스터 테이블 `tb_th_req_master_mst`에서 조회할 표준 컬럼 리스트(의뢰 코드, 시험장소, 접수일시 등)를 상수 문자열로 정의하는 데이터 맵핑 모듈입니다.
> 
> * **상위 대시보드**: [[00_unoUtil_모듈개발_대시보드]]

---

## 1. ⚙️ 데이터베이스 정의 컬럼 명세

| 물리 컬럼명 | 논리 한글 정의 | 비고 |
| :--- | :--- | :--- |
| `RQST_CD` | 의뢰 코드 | 마스터 기본 키 |
| `TST_HOST_CD` | 시험 주관 코드 | 주관 부서 코드 |
| `TPLNM` | 시험장소명 | 실차 시험장 위치 |
| `RQST_DTM` | 의뢰 일시 | 데이터 로드 기준 시점 |
| `RECV_DTM` | 접수 일시 | 데이터 접수 시점 |
| `CMPDTM` | 완료일시 | 시험 가용 완료 시점 |
| `TST_PPSNM` | 시험 목적명 | 목적성 태깅 |
| `TST_TITLE_CMMNT` | 시험 제목 코멘트 | 요약 비고 설명란 |

---

## 💻 2. 호출 예제 (Usage Example)

```python
from unoUtil.database.q1_hkt_rnd_dw__test__tb_th_req_master_mst import tb_th_req_master_mst

# q1 모듈에 정의된 컬럼 리스트를 활용한 고속 SQL SELECT 문 빌드
query = f"SELECT {tb_th_req_master_mst} FROM hkt_rnd_dw.test.tb_th_req_master_mst LIMIT 10"
print(query)
```

---

## 3. 📝 이중 동기화 프로토콜 준수사항
- 이 매뉴얼 파일은 동일 로컬 디렉터리(`unoUtil/database/`) 내에 1:1 대응하여 보관되며, 최종 작업 완료 선언 시 옵시디언 볼트로 일괄 배치 동기화 처리됩니다.
