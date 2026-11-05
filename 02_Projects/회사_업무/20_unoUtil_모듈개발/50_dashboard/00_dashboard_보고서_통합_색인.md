---
id: "dashboard_report_index"
title: "unoUtil Dashboard(가감속/제동 인터랙티브 웹 대시보드) 모듈 개발 보고서 통합 색인"
type: index
category_main: 회사_업무
category_sub: unoUtil
category_detail: dashboard
date: 2026-11-05
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - dashboard
  - streamlit
  - telemetry
  - 색인
  - MOC
---

# 🖥️ unoUtil Dashboard(가감속/제동 인터랙티브 웹 대시보드) 모듈 개발 보고서 통합 색인 (MOC)

> [!ABSTRACT] 📖 Dashboard 엔지니어링 개발 및 실증 보고서 허브
> 본 색인은 `unoUtil.vehicle.acc_brk` 도메인의 **독립 인터랙티브 웹 대시보드(`dashboard_app.py`, 5,400+ 라인)** 구축 및 아키텍처, 다크 홀로그램 글래스모피즘 UI/UX, 온디맨드 시각화, 그리고 **사내 실차 시험 공식 표준 속도 규격(스노우 가속 5-40 km/h) 코어 모듈(SSOT) 일원화**에 대한 종합 기술 개발 보고서를 집대성한 전용 MOC입니다.

---

## 📑 모듈 개발 보고서 목록

| 번호 | 보고서 명칭 | 핵심 다룸 내용 및 실증 범위 | 작성일자 | 상태 |
| :---: | :--- | :--- | :---: | :---: |
| **10** | [[2026-11-05_v3.82_가감속제동_인터랙티브_웹대시보드_구축_및_스노우가속_표준속도정합_종합개발보고서\|10. 가감속/제동(acc_brk) 통합 인터랙티브 웹 대시보드 구축 및 스노우 가속 표준 속도(5-40) 정합 종합개발보고서]] | • 대시보드 독립 패키지화 (`unoUtil/vehicle/acc_brk/dashboard/`)<br>• 5대 네온 메달리온 메뉴 및 다크 홀로그램 글래스모피즘(68~80%) 테마<br>• 0ms 런 선별 인터랙티브 테이블(`_TIRE_RUN_TABLE_HTML`) & 드래그앤드롭 정렬(`_DND_TIRE_HTML`)<br>• 온디맨드 렌더링 및 팝업 차단 100% 우회 전문 인터랙티브 새 창 뷰어(`Blob URL`: 휠 줌 0.1~15x, 마우스 드래그 이동, Shift/버튼 박스 영역 부분 확대, 화면 맞춤)<br>• 플로터 12×6 표준화 & `#런번호 (수치)` 3단 지그재그 뱃지 오버레이<br>• 스노우 가속 `5 → 40 km/h` 코어 모듈(`get_default_test_vel`) SSOT 일원화<br>• Tire 탭 파라미터 승계(`min_sec`, `max_sec`, `ws`, `filter`) 핫픽스 | 2026-11-05 | ✅ 완료 |

---

## 🔗 상위 및 연계 문서
- 💼 **프로젝트 마스터 MOC**: [[00_unoUtil_모듈개발_대시보드]]
- 📖 **도메인 지식 사전**: [[vt_acc_brk_사전]]
- ⏱️ **응답성 보고서 MOC**: [[00_response_보고서_통합_색인]]
- 🛞 **마찰저하 보고서 MOC**: [[00_mu_drop_보고서_통합_색인]]
