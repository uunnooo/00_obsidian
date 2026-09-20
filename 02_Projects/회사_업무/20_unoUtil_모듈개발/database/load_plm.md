---
id: "load_plm_20260920"
title: "load_plm (PLM 설계 메타데이터 조회 및 캐싱 엔진) 상세 매뉴얼"
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
  - PLM
  - 규격
project_link: "[[unoUtil]]"
---

# 📊 load_plm (PLM 설계 메타데이터 조회 및 캐싱 엔진) 상세 매뉴얼

> [!ABSTRACT] 📌 개요
> Databricks RND DW 서버의 글로벌 타이어 규격 테이블(`tb_pl_dw_spec_plm_tire_bas`)로부터 특정 타이어 스펙 코드(SPEC_CD, 예: KPKT 코드)에 매칭되는 설계 단면폭, 편평비, 그루브 깊이 등 주요 타이어 물리 구조 메타데이터를 일괄 고속 수집하고 물리 파일로 압축 캐싱(`pkl.gz`)하는 데이터베이스 통합 인터페이스 모듈입니다.
> 
> * **상위 대시보드**: [[00_unoUtil_모듈개발_대시보드]]

---

## 1. ⚙️ 데이터 스키마 및 캐싱 메커니즘

### 1.1. PLM 규격 테이블 정보 (tb_pl_dw_spec_plm_tire_bas)
타이어 가류 사양, 구조, 컴파운드 배합비 등 수백 개 항목의 마스터 DB 컬럼에 고속 맵핑됩니다.  
상세 컬럼 목록은 관련 쿼리 모듈(예: [[q4_hkt_rnd_dw__specification__tb_pl_dw_spec_plm_tire_bas]])을 참조하십시오.

### 1.2. 중복 I/O 배제 및 대칭 캐싱 (save)
- **외부 커서 주입 (`cur`)**: 루프 및 대량 쿼리를 기동하는 오케스트레이터 세션에서는 외부에서 오픈된 커서 인스턴스(`cur`)를 수동 매핑 전달함으로써, 쿼리 시마다 발생하는 클라우드 인증 네트워크 오버헤드를 극적으로 억제(속도 5~10배 개선)할 수 있습니다.
- **물리 Gzip 캐시 (`save`)**: DB 쿼리를 통해 패치 완료된 판다스 데이터프레임(`df_result`)은 이중 입출력을 줄이기 위해 Gzip 기술이 통합 적용된 피클 이진 아카이브(`pkl.gz`)로 즉각 물리 직렬화 저장할 수 있습니다.

---

## 2. ⚙️ 주요 API 명세

### 2.1. `load_plm(spec, target='*', cur=None, **kwargs) -> Optional[pd.DataFrame]`
* **기능**: SPEC 타겟 코드를 이용하여 PLM 테이블을 SELECT 조회하여 결측과 중복 컬럼이 없는 고품질 데이터프레임 형태로 복원합니다.
* **매개변수**:
  - `spec (str | List[str])`: 조회할 고유 타이어 규격 KPKT 코드 단일 문자열 또는 복수 리스트.
  - `target (str)`: SELECT 쿼리에 사용할 컬럼 타겟팅 구문 (예: `*` 또는 컬럼 상수 콤마 문자열). 기본값 `'*'`.
  - `cur (Cursor, optional)`: 사내 Databricks 커넥션 활성 커서 객체.
  - `**kwargs (Any)`: 추가적인 기능 제어 속성:
    - `'save'` (str | bool): `True` 전달 시 `"db.pkl.gzip"`에 자동 저장, 특정 파일 절대/상대 경로 지정 시 해당 주소로 압축 캐싱 저장. (주의: 확장자 `.gz` 필수 준수).
    - `'limit'` (int): 반환 레코드 총 행 개수 상한선(LIMIT) 한계치 제어.
* **반환값**: 수집 및 중복 컬럼 정제가 완료된 판다스 `pd.DataFrame`. 연결 장애 또는 쿼리 실패 시 `None`을 반환합니다.
* **하위 호환 별칭**: `func_load_plm`

---

## 💻 3. 호출 예제 (Usage Example)

```python
from unoUtil.database.auth_conn import make_conn, close_conn
from unoUtil.database.load_plm import load_plm
from unoUtil.database.q4_hkt_rnd_dw__specification__tb_pl_dw_spec_plm_tire_bas import tb_pl_dw_spec_plm_tire_bas

# 1. 조회 대상 KPKT 스펙 목록 정의
target_specs = ["KPKT1033338X00012", "KPKT1033338X00013"]

# 2. Databricks 연결 수립
conn = make_conn()

if conn is not None:
    try:
        # 3. load_plm 호출 - q4 모듈에 정의된 필수 설계 인자 목록(tb_pl_dw_spec_plm_tire_bas) 컬럼만 타겟 조회
        # 동시에 로컬에 gzip 바이너리 캐시 파일로 동시 저장(save)
        df_plm = load_plm(
            spec=target_specs,
            target=tb_pl_dw_spec_plm_tire_bas,
            cur=conn,
            save="tire_plm_structure_cache.pkl.gz"
        )
        
        # 4. 데이터프레임 활용
        if df_plm is not None:
            print(df_plm[["SPEC_CD", "TIRE_NCSW", "GRV_DTH"]])
            
    except Exception as e:
        print(f"PLM 쿼리 연동 중 장애 발생: {e}")
    finally:
        # 5. 커넥션 종료
        close_conn(conn)
```

---

## 4. 📝 이중 동기화 프로토콜 준수사항
- 이 매뉴얼 파일(`load_plm.md`)은 동일 로컬 디렉터리(`unoUtil/database/`) 내에 1:1 대응하여 보관되며, 최종 작업 완료 선언 시 옵시디언 볼트로 일괄 배치 동기화 처리됩니다.
