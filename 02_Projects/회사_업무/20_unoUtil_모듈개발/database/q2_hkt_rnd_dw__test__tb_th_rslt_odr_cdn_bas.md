---
id: "q2_hkt_rnd_dw__test__tb_th_rslt_odr_cdn_bas_20260920"
title: "q2_hkt_rnd_dw__test__tb_th_rslt_odr_cdn_bas (시험 항목 및 차량 환경 조건 컬럼 정의) 상세 매뉴얼"
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

# 🗄️ q2_hkt_rnd_dw__test__tb_th_rslt_odr_cdn_bas (시험 항목 및 차량 환경 조건 컬럼 정의) 상세 매뉴얼

> [!ABSTRACT] 📌 개요
> Databricks RND DW의 시험 조건 기본 테이블 `tb_th_rslt_odr_cdn_bas`에서 차량 속성, 시험장소, 공차 중량 및 탑승 배분 하중 정보 컬럼 리스트를 상수 문자열로 정의하는 데이터 맵핑 모듈입니다.
> 
> * **상위 대시보드**: [[00_unoUtil_모듈개발_대시보드]]

---

## 1. ⚙️ 데이터베이스 정의 컬럼 명세

| 물리 컬럼명 | 논리 한글 정의 | 비고 |
| :--- | :--- | :--- |
| `RQST_CD` | 의뢰 코드 | 연동 조인 외래 키 |
| `RLVTPNM` | 실차시험장소명 | 타겟 시험장 규격 매핑 |
| `TRS_TITM_OBJ_TBLK` | 시험항목 객체 테이블키 | 내부 시스템 고유 키 |
| `TRS_TITM_ST_TBLK` | 시험항목 상태 테이블키 | 내부 시스템 상태 키 |
| `TST_NUM` | 시험 번호 | 시험 차수 식별키 |
| `TST_CNDTNM` | 시험 조건번호 | 조건 일련번호 |
| `TCNDTNM` | 시험조건명 | 제동 노면/평가 조건명 |
| `FIRST_DRVR1` | 제1 운전자1 | 주 운전자 명칭 |
| `SECOND_DRVR2` | 제2 운전자2 | 부 운전자 명칭 |
| `VHCL_BRDNM` | 차량 브랜드명 | 평가 차량 제조사 |
| `VHCL_MDLNM` | 차량 모델명 | 평가 차량 모델 |
| `VHCL_NGNDVSNM` | 차량 엔진구분명 | 가솔린/디젤/EV 분기 |
| `VHCL_GDVSNM` | 차량 기어구분명 | 수동/자동 단수 기입 |
| `VHCL_MOVE_TYPE_CD` | 차량 구동 유형 코드 | 4WD/2WD 구동 배분 |
| `LOAD_CFG_NM` | 하중 구성 명 | 공차/만차 배분 기준명 |
| `LSFWH_LOAD` | 좌측전륜 하중 | FL 현가 축중계 무게 (kg) |
| `RSFWH_LOAD` | 우측전륜 하중 | FR 현가 축중계 무게 (kg) |
| `LSBWH_LOAD` | 좌측후륜 하중 | RL 현가 축중계 무게 (kg) |
| `RSBWH_LOAD` | 우측후륜 하중 | RR 현가 축중계 무게 (kg) |
| `ADDBRD_LOAD` | 추가탑승 하중 | 가중 추 탑승 중량 |
| `VHCTWG_LOAD` | 차량총중량 하중 | 실차 총 중량 합산 수치 |

---

## 💻 2. 호출 예제 (Usage Example)

```python
from unoUtil.database.q2_hkt_rnd_dw__test__tb_th_rslt_odr_cdn_bas import tb_th_rslt_odr_cdn_bas

# q2 모듈에 정의된 차량 하중 및 사양 컬럼 리스트를 활용한 SQL SELECT 문 빌드
query = f"SELECT {tb_th_rslt_odr_cdn_bas} FROM hkt_rnd_dw.test.tb_th_rslt_odr_cdn_bas LIMIT 10"
print(query)
```

---

## 3. 📝 이중 동기화 프로토콜 준수사항
- 이 매뉴얼 파일은 동일 로컬 디렉터리(`unoUtil/database/`) 내에 1:1 대응하여 보관되며, 최종 작업 완료 선언 시 옵시디언 볼트로 일괄 배치 동기화 처리됩니다.
