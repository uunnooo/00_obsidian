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


---

## 4. 🚨 사내망 SSL Inspection 및 OAuth 트러블슈팅 가이드

### 4.1. 증상: 웹은 정상 접속되나 파이썬 실행 시 SSL 검증 에러 발생
```text
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1133)
databricks.sql.exc.RequestError: HTTP request failed: HTTPSConnectionPool(host='hknc-hankooktire-rnd.cloud.databricks.com', port=443): Max retries exceeded with url: /oidc/.well-known/oauth-authorization-server
```

### 4.2. 원인 분석: 왜 브라우저 팝업 창조차 뜨지 않고 사전에 차단되는가?
1. **사내 보안 장비의 SSL Inspection(가로채기)**: 사내망(한국타이어 인트라넷, 기업 방화벽/Zscaler)에서는 외부 클라우드 통신을 감시하기 위해 사내 자체 서명 인증서(Self-Signed Root CA)로 SSL 패킷을 교체하여 전달합니다.
2. **웹 브라우저 vs 파이썬의 인증서 참조 차이**:
   - **웹 브라우저(크롬, 엣지)**: 윈도우 OS 시스템 인증서 저장소에 사내 루트 인증서가 기본 등록되어 있으므로 "안전한 사이트"로 인식되어 정상 접속됩니다.
   - **파이썬(urllib3, databricks-sql)**: 윈도우 인증서 저장소가 아닌 파이썬 내부 `certifi` CA 번들만 확인하므로, 사내 보안 프록시의 인증서를 미신뢰 자체 서명 인증서로 간주하여 연결을 즉시 차단합니다.
3. **OAuth 1단계 백그라운드 탐색 실패**:
   - `auth_type="databricks-oauth"` 가동 시 브라우저 창을 띄우기 전, 먼저 백그라운드로 `/.well-known/oauth-authorization-server`에 접속하여 OAuth 메타데이터를 수집합니다.
   - 이 1단계 백그라운드 호출에서 SSL 검증 에러가 발생하므로, 브라우저 창을 띄우는 2단계 코드까지 도달하지 못하고 즉시 런타임 예외가 발생합니다.

### 4.3. 해결책: make_conn의 _tls_no_verify=True 기본 탑재
`_authconn_.py`의 `sql.connect` 호출 시 사내망 검증 우회 플래그를 기본 전달하고, 불필요한 콘솔 경고를 억제합니다:

```python
from databricks import sql
import urllib3

# 사내망 SSL 검증 우회 시 발생하는 터미널 경고 억제
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def make_conn(server_hostname=server_hostname, http_path=http_path, tls_no_verify=True, **kwargs):
    try:
        conn = sql.connect(
            server_hostname=server_hostname,
            http_path=http_path,
            auth_type="databricks-oauth",
            _tls_no_verify=tls_no_verify,  # 👈 사내망 SSL 검증 우회 적용
            **kwargs
        ).cursor()
        print("✅ DB 연결 성공! 쿼리를 시작합니다.")
    except Exception as e:
        conn = None
        print(f"⚠️ 서버 연결 중 예상치 못한 오류 발생: {e}")
    return conn
```
이 조치로 1단계 백그라운드 메타데이터 조회가 정상 통과되며, 인증 만료 시 정상적으로 브라우저 로그인 창이 팝업됩니다.

## 5. 📝 이중 동기화 프로토콜 준수사항
- 이 매뉴얼 파일(`auth_conn.md`)은 동일 로컬 디렉터리(`unoUtil/database/`) 내에 1:1 대응하여 보관되며, 최종 작업 완료 선언 시 옵시디언 볼트로 일괄 배치 동기화 처리됩니다.
