---
id: "connect_vehicle_test_and_spec_20260923"
title: "connect_vehicle_test_and_spec (실차 평가 결과 및 PLM 세부 스펙 원스톱 통합 모듈) 매뉴얼"
type: resource
category_main: 회사_업무
category_sub: 개발매뉴얼
date: 2026-09-23
status: 완료
tags:
  - 회사_업무
  - GetDB
  - 데이터베이스
  - Databricks
  - 실차시험
  - PLM
  - 스펙연결
project_link: "[[00_unoUtil_모듈개발_대시보드]]"
---

# 🏎️ connect_vehicle_test_and_spec (실차 평가 결과 및 PLM 세부 스펙 원스톱 통합 모듈)

> [!ABSTRACT] 📌 개요
> 실차 시험 의뢰번호(`RQST_CD`)와 타이어 세트 식별자(`TIRE_SET_VAL`)를 기반으로 타이어 규격 코드(`SPEC_CD`) 및 PLM 세부 설계 스펙을 연동함과 동시에, 분석자가 특정 실차 평가 결과 테이블(`table_target`, 예: `tb_th_rslt_braking_wet_bas`, `dry`, `snow` 등)을 지정했을 때 해당 평가의 실제 측정 데이터(제동거리, 감속도 등)까지 실차 공통 키(`TRS_TITM_OBJ_TBLK`)로 안전하게 `LEFT JOIN`하여 원스톱으로 반환하는 통합 인터페이스 모듈입니다.
>
> * **소스 파일**: `_func_connect_vehicle_test_and_spec.py`
> * **상위 대시보드**: [[00_unoUtil_모듈개발_대시보드]]

---

## 1. ⚙️ 데이터 아키텍처 및 공통 키(Key) 매핑

모든 실차 평가 결과 테이블(`tb_th_rslt_*`)과 시험 조건 테이블(`tb_th_rslt_odr_cdn_bas`)은 **`TRS_TITM_OBJ_TBLK`(시험항목 객체 테이블키)**를 공유합니다. 본 모듈은 이 공통 키를 활용하여 수십 개의 결과 테이블을 직접 찾아다닐 필요 없이, 원하는 평가 결과 테이블만 즉시 결합합니다.

```mermaid
flowchart TD
    A["시험 조건 정보<br/>tb_th_rslt_odr_cdn_bas<br/>(RQST_CD, TIRE_SET_VAL, TST_ITMNM)"] -->|TRS_TITM_OBJ_TBLK| B["시험 항목 정보<br/>tb_th_req_item_bas"]
    B -->|TRS_SPEC_OBJ_TBLK| C["타이어 규격 정보<br/>tb_th_req_tire_spec_bas<br/>(SPEC_CD)"]
    C -->|SPEC_CD| D["PLM 설계 세부 스펙<br/>tb_pl_dw_spec_plm_tire_bas"]
    A -.->|TRS_TITM_OBJ_TBLK (LEFT JOIN)| E["실차 평가 결과 테이블<br/>(table_target: Wet/Dry/Snow 제동 등)"]
```

### 아키텍처 장점
1. **유연한 다형성**: `table_target`을 지정하지 않으면 가볍게 **시험조건+세부스펙**만 조회하고, 결과 테이블을 지정하면 **실측값+세부스펙**이 완벽 결합됩니다.
2. **데이터 유실 방지**: `LEFT JOIN` 구조를 채택하여, 해당 평가를 미수행했거나 결과 데이터가 비어있어도 스펙 데이터가 날아가지 않고 온전히 보존됩니다.
3. **스키마 자동 보정**: `tb_th_rslt_braking_wet_bas` 형식의 테이블명만 넘겨도 `hkt_rnd_dw.test.` 접두사를 자동 부여합니다.

---

## 2. 📋 함수 시그니처 및 파라미터

```python
def connect_vehicle_test_and_spec(
    req: Union[str, List[str]],
    tire_set: Optional[Union[str, List[str]]] = None,
    table_target: Optional[str] = None,
    target_spec: str = tb_pl_dw_spec_plm_tire_bas,
    target_rslt: str = "rslt.*",
    cur=None,
    **kwargs
) -> Optional[pd.DataFrame]:
```

| 파라미터 | 타입 | 기본값 | 설명 |
| :--- | :---: | :---: | :--- |
| `req` | `str \| list` | **필수** | 의뢰 코드 (예: `'26RE040025KF'`) |
| `tire_set` | `str \| list` | `None` | 타이어 세트 값 (예: `'T1'`, `['T1', 'T2']`). `set` 키워드도 호환 |
| `table_target` | `str` | `None` | 결합할 실차 결과 테이블명 (예: `'tb_th_rslt_braking_wet_bas'`) |
| `target_spec` | `str` | `tb_pl_dw_spec_plm_tire_bas` | 조회할 PLM 세부 스펙 프로젝션 컬럼 정의 |
| `target_rslt` | `str` | `'rslt.*'` | 결과 테이블에서 가져올 컬럼 정의 문자열 |
| `cur` | `Cursor` | `None` | Databricks 커서 객체 |
| `**kwargs` | `dict` | - | `limit`, `save` 옵션 지원 |

---

## 3. 💡 실무 사용 시나리오

### 시나리오 1: Wet 제동 실측값 + 타이어 PLM 세부 스펙 함께 결합
```python
from _authconn_ import make_conn, close_conn
from _func_connect_vehicle_test_and_spec import connect_vehicle_test_and_spec

conn = make_conn()
try:
    df = connect_vehicle_test_and_spec(
        req="26RE040025KF",
        tire_set="T1",
        table_target="tb_th_rslt_braking_wet_bas",  # Wet 제동 결과 연결
        cur=conn
    )
    # 제동거리(BRKGT_BRKGDST_AVRG 등)와 PLM 컴파운드/그루브깊이가 함께 조회됨
    print(df.head())
finally:
    close_conn(conn)
```

### 시나리오 2: 결과 테이블 없이 순수 시험 항목 메타 + 세부 스펙만 조회
```python
conn = make_conn()
try:
    df = connect_vehicle_test_and_spec(
        req="26RE040025KF",
        tire_set="T1",
        cur=conn
    )
    # T1 세트가 치른 시험 항목명(TST_ITMNM)과 PLM 세부 스펙이 깔끔하게 조회됨
    print(df.head())
finally:
    close_conn(conn)
```
