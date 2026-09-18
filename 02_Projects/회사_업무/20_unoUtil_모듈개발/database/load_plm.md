# 📊 unoUtil.database.load_plm 모듈 매뉴얼

## 1. 개요
PLM 시스템 및 시험 데이터베이스에서 타이어 시험 이력 및 메타데이터를 호출하는 표준 인터페이스입니다.

## 2. API 규격
```python
from unoUtil.database import load_plm, auth_conn

# PLM 데이터 조회
df_plm = load_plm(req_no="26RE020041KF")
```
