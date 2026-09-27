---
id: "auth_conn_20260920"
title: "auth_conn (Databricks RND DW 클라우드 클라이언트 연동) 상세 매뉴얼"
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
  - Databricks
  - 클라우드
project_link: "[[unoUtil]]"
---

# 🗄️ auth_conn (Databricks RND DW 클라우드 클라이언트 연동) 상세 매뉴얼

> [!ABSTRACT] 📌 개요
> 사내 고성능 주행/제동/타이어 시험 메타데이터가 보관된 Databricks RND DW 클라우드 인프라에 안전하게 접속하기 위해, Databricks OAuth 프로토콜 기반의 실시간 사용자 인증 세션을 관리하고 쿼리 실행용 커서(Cursor)를 바인딩 및 해제하는 코어 인증 모듈입니다.
> 
> * **상위 대시보드**: [[00_unoUtil_모듈개발_대시보드]]

---

## 1. ⚙️ 인증 메커니즘 및 SQL 규격 표준화

### 1.1. Databricks OAuth 인증 (make_conn)
사내 보안 정책에 따라 아이디/패스워드 하드코딩 방식의 접근은 차단되어 있습니다.  
`make_conn()` 가동 시, RND DW 호스트 서버에 `auth_type="databricks-oauth"` 프로토콜을 던져 로컬 웹 브라우저 사용자 인증 창을 호출하며, 발급된 OAuth 임시 토큰을 바탕으로 비차단 보안 터널링 및 커서(`Cursor`) 제어 권한을 획득합니다.

### 1.2. SQL IN 조건 인코딩 표준화 (normalize_sql_list)
사용자가 전달한 문자열 단일값 또는 리스트(예: KPKT 코드, 의뢰번호 리스트)를 SQL 쿼리 구문의 `IN (...)` 절에 삽입 가능한 형태로 변환합니다.
- **입력**: `["KPKT_1", "KPKT_2"]` ➔ **변환**: `'KPKT_1','KPKT_2'` (문자열)
- 만약 전체 데이터를 의미하는 `"ALL"` 키워드가 입력되거나 타입이 부합하지 않는 경우, 쿼리 무용을 방지하기 위해 `False`를 자동 반환합니다.

---

## 2. ⚙️ 주요 API 명세

### 2.1. `normalize_sql_list(value) -> Union[str, bool]`
* **기능**: 리스트 및 단일 문자열 데이터를 SQL IN 조건용 홑따옴표 쉼표 결합형 문장으로 인코딩합니다.

### 2.2. `make_conn(server_hostname=..., http_path=...) -> Optional[Cursor]`
* **기능**: Databricks OAuth 클라우드 연결 커넥션을 개설하고 쿼리 실행 커서 객체를 생성합니다.
* **하위 호환 별칭**: `auth_conn`, `create_conn`

### 2.3. `close_conn(obj_cursor) -> None`
* **기능**: 전달받은 커서 객체의 리소스 점유를 해제하고 커넥트 터널을 안전 종료합니다. None이 인입되거나 `close` 메서드가 부재한 경우에도 예외 없이 안전 무중단 소거를 수행합니다.

---

## 💻 3. 호출 예제 (Usage Example)

```python
from unoUtil.database.auth_conn import make_conn, close_conn, normalize_sql_list

# 1. KPKT 타이어 규격 리스트 SQL 규격화
tire_specs = ["KPKT1033338X00012", "KPKT1033338X00013"]
sql_in_clause = normalize_sql_list(tire_specs)
print(f"SQL 필터 조건절 삽입용 문자열: {sql_in_clause}")  # 'KPKT1033338X00012','KPKT1033338X00013'

# 2. Databricks OAuth 보안 세션 연결 시도
cursor = make_conn()

# 3. 데이터 쿼리 수행 (커서가 정상 바인딩되었을 때만 가동)
if cursor is not None:
    try:
        query = f"SELECT * FROM hkt_rnd_dw.specification.tb_pl_dw_spec_plm_tire_bas WHERE SPEC_CD IN ({sql_in_clause}) LIMIT 5"
        cursor.execute(query)
        
        # 패치 결과 수령
        results = cursor.fetchall()
        print(f"조회된 데이터 레코드 수: {len(results)}")
    except Exception as e:
        print(f"쿼리 실행 중 예외 오류 발생: {e}")
    finally:
        # 4. 사용이 완료된 커서 리소스 반환 (네트워크 터널 안전 소거)
        close_conn(cursor)
```

---

## 4. 📝 이중 동기화 프로토콜 준수사항
- 이 매뉴얼 파일(`auth_conn.md`)은 동일 로컬 디렉터리(`unoUtil/database/`) 내에 1:1 대응하여 보관되며, 최종 작업 완료 선언 시 옵시디언 볼트로 일괄 배치 동기화 처리됩니다.
