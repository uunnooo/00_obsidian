---
id: "work_20260910_Tableau"
title: "20_회사 Tableau 대시보드 사용 매뉴얼"
type: resource
category_main: 회사_업무
category_sub: 사내매뉴얼
date: 2026-09-10
status: 완료
tags:
  - 회사_업무
  - Tableau
  - Databricks
  - 사내매뉴얼
aliases:
  - "회사_Tableau_사용_매뉴얼"
  - "20_회사_Tableau_사용_매뉴얼"
---

# 💼 Tableau 사내 DB 연동 매뉴얼

> [!NOTE] 📘 목적
> 사내 Insight Portal 및 Databricks 클러스터/Warehouse와 Tableau Desktop을 연동하여 시험 계측 데이터에 접속하기 위한 표준 가이드입니다.

---

## 1. Insight Portal에서 Tableau 계정 활성화 상태 확인

🔗 [사내 Insight Portal 바로가기](https://insight.hankooktech.com/HOME/home.html)

* 기본적으로 계정이 있으면 사이트에 재접속하는 것만으로 활성화됩니다.
* ![[_attachments/10_회사_업무/10_Tableau_사용_매뉴얼_01.png|650]]

> [!WARNING] 계정 권한 문의
> 계정에 문제가 있거나 권한이 비활성화된 경우 Insight 담당자에게 문의하세요.  
> *(담당: IT서비스PM팀 이재상)*

---

## 2. Teams 접속 확인

* Teams에 정상 로그인 및 접속되어 있어야 SSO 라이선스 계정이 활성화 상태로 유지됩니다.

---

## 3. Tableau Desktop 실행

* 계정이 활성화된 상태라면 정상적으로 Tableau Desktop이 구동됩니다.
* 실행 오류 발생 시 1번(Portal) 및 2번(Teams) 인증 상태를 우선 재확인합니다.

---

## 4. Databricks 연동 및 설정

### 1) Databricks 웹사이트 로그인 및 접속
🔗 [한국타이어 Databricks 포털](https://hknc-hankooktire-rnd.cloud.databricks.com/)
* 사내 회사 이메일 인증 코드를 통해 로그인하여 세션을 활성화합니다.

### 2) 접속 가능한 SQL Warehouse 상태 확인
* 내 계정에서 접근 가능한 SQL Warehouse 인스턴스가 `Running` 상태인지 확인합니다. (Warehouse에 실제 DB 존재)
* ![[_attachments/10_회사_업무/11_Tableau_사용_매뉴얼_02.png|650]]

### 3) Connection Details 정보 일치 확인
* Warehouse의 **Connection Details** (서버 호스트 이름, HTTP 경로, 포트 등) 정보와 Tableau 내 Databricks 연결 구성 창의 정보가 일치해야 합니다.
* ![[_attachments/10_회사_업무/12_Tableau_사용_매뉴얼_03.png|650]]
* ![[_attachments/10_회사_업무/13_Tableau_사용_매뉴얼_04.png|650]]

### 4) 웹 브라우저 인증 및 연동 완료
* 설정 후 웹 브라우저 SSO 인증을 완료하면 Tableau에서 Databricks 데이터베이스 테이블을 쿼리하거나 시각화 대시보드로 활용할 수 있습니다.

> [!WARNING] Databricks 연결 문의
> 모든 설정 값이 동일함에도 연결에 실패할 경우 인프라 담당자에게 문의하세요.  
> *(담당: 디지털테크팀 안준혁)*