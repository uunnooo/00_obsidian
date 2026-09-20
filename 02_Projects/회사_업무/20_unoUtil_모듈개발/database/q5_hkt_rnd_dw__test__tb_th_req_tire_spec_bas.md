---
id: "q5_hkt_rnd_dw__test__tb_th_req_tire_spec_bas_20260920"
title: "q5_hkt_rnd_dw__test__tb_th_req_tire_spec_bas (평가용 타이어 매핑 규격 정의) 상세 매뉴얼"
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

# 🗄️ q5_hkt_rnd_dw__test__tb_th_req_tire_spec_bas (평가용 타이어 매핑 규격 정의) 상세 매뉴얼

> [!ABSTRACT] 📌 개요
> Databricks RND DW의 타이어 사양 매핑 테이블 `tb_th_req_tire_spec_bas`에서 타이어 패턴명, 규격 사이즈 크기 정보 등 시험의뢰와 실제 장착 제품 스펙 간의 대조 연결 표준 컬럼을 상수 문자열로 정의하는 데이터 맵핑 모듈입니다.
> 
> * **상위 대시보드**: [[00_unoUtil_모듈개발_대시보드]]

---

## 1. ⚙️ 데이터베이스 정의 컬럼 명세

| 물리 컬럼명 | 논리 한글 정의 | 비고 |
| :--- | :--- | :--- |
| `SPEC_CD` | 규격 코드 | 타이어 KPKT 규격 코드 |
| `TRS_SPEC_OBJ_TBLK` | 시험의뢰시스템 규격 객체 테이블키 | 내부 시스템 고유 규격 매핑 키 |
| `PLM_SPEC_OBJ_TBLK` | 피엘엠 규격 객체 테이블키 | PLM 연동용 조인 외래 키 |
| `PTTRNM` | 패턴명 | 타이어 트레드 패턴 상품 한글명 (예: Ventus S1) |
| `SPEC_SIZE` | 규격 크기 | 타이어 표준 형식 사이즈 문자열 (예: 245/45R18) |

---

## 💻 2. 호출 예제 (Usage Example)

```python
from unoUtil.database.q5_hkt_rnd_dw__test__tb_th_req_tire_spec_bas import tb_th_req_tire_spec_bas

# q5 모듈에 정의된 평가용 타이어 사양 컬럼 목록을 활용한 SQL SELECT 문 빌드
query = f"SELECT {tb_th_req_tire_spec_bas} FROM hkt_rnd_dw.test.tb_th_req_tire_spec_bas LIMIT 10"
print(query)
```

---

## 3. 📝 이중 동기화 프로토콜 준수사항
- 이 매뉴얼 파일은 동일 로컬 디렉터리(`unoUtil/database/`) 내에 1:1 대응하여 보관되며, 최종 작업 완료 선언 시 옵시디언 볼트로 일괄 배치 동기화 처리됩니다.
