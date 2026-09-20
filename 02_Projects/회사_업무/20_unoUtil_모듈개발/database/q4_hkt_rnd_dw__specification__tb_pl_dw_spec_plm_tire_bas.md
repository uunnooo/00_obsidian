---
id: "q4_hkt_rnd_dw__specification__tb_pl_dw_spec_plm_tire_bas_20260920"
title: "q4_hkt_rnd_dw__specification__tb_pl_dw_spec_plm_tire_bas (PLM 타이어 상세 구조 사양 정의) 상세 매뉴얼"
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

# 🗄️ q4_hkt_rnd_dw__specification__tb_pl_dw_spec_plm_tire_bas (PLM 타이어 상세 구조 사양 정의) 상세 매뉴얼

> [!ABSTRACT] 📌 개요
> Databricks RND DW의 PLM 규격 테이블 `tb_pl_dw_spec_plm_tire_bas`에서 타이어 그루브 깊이, 벨트 각도, 조인트리스 커버 타입 등 제품 설계 원천 물리 사양 표준 컬럼을 상수 문자열로 정의하는 데이터 맵핑 모듈입니다.
> 
> * **상위 대시보드**: [[00_unoUtil_모듈개발_대시보드]]

---

## 1. ⚙️ 데이터베이스 정의 컬럼 명세

| 물리 컬럼명 | 논리 한글 정의 | 비고 |
| :--- | :--- | :--- |
| `PLM_SPEC_OBJ_TBLK` | 피엘엠 규격 객체 테이블키 | PLM 테이블 마스터 기본 키 |
| `SPEC_CD` | 규격 코드 | 타이어 고유 KPKT 코드 |
| `CPTRD_CMPND_CD` | 캡트레드 컴파운드 코드 | 트레드 고무 컴파운드 사양 |
| `SBTRD_CMPND_CD` | 서브트레드 컴파운드 코드 | 언더트레드 고무 컴파운드 사양 |
| `TIRE_NCSW` | 타이어 공칭단면폭 | 타이어 단면폭 (예: 245 등) |
| `TIRE_APTRT` | 타이어 편평비 | 타이어 편평비 (예: 45 등) |
| `TIRE_RMICH` | 타이어 림인치 | 타이어 장착 인치 (예: 18 등) |
| `GRV_DTH` | 그루브 깊이 | 트레드 패턴 그루브 잔여 깊이 (mm) |
| `JNTRC_TYPE_CD` | 조인트리스커버 유형 코드 | JLB 보강 레이어 타입 코드 |
| `SNS` | 시즌 | 여름/겨울/사계절 사양 구분 |
| `FIRST_BT_ANG` | 제1 벨트 각도 | 스틸 벨트 보강층 코드 각도 |
| `BDFL_LTH` | 비드필러 길이 | 비드 보강 필러 고무 설계 단면 길이 |

---

## 💻 2. 호출 예제 (Usage Example)

```python
from unoUtil.database.q4_hkt_rnd_dw__specification__tb_pl_dw_spec_plm_tire_bas import tb_pl_dw_spec_plm_tire_bas

# q4 모듈에 정의된 PLM 타이어 물리 설계 컬럼 목록을 활용한 SQL SELECT 문 빌드
query = f"SELECT {tb_pl_dw_spec_plm_tire_bas} FROM hkt_rnd_dw.specification.tb_pl_dw_spec_plm_tire_bas LIMIT 10"
print(query)
```

---

## 3. 📝 이중 동기화 프로토콜 준수사항
- 이 매뉴얼 파일은 동일 로컬 디렉터리(`unoUtil/database/`) 내에 1:1 대응하여 보관되며, 최종 작업 완료 선언 시 옵시디언 볼트로 일괄 배치 동기화 처리됩니다.
