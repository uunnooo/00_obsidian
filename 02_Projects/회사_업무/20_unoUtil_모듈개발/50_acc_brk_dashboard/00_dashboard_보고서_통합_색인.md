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
| **20** | [[2026-11-12_v4.00_대시보드_v2.0_실시간콘솔_경로정규화_안정화_종합개발보고서|20. 가감속/제동(acc_brk) 대시보드 v2.0 실시간 콘솔 스트리머·경로 정규화 및 런처 안정화 종합개발보고서]] | • 실시간 콘솔 스트리머(`StreamlitLiveConsole`) 심각도 4단계 정밀 판정(`_classify_line`, `has_warning`) & 4색 뱃지/보더(ERROR/WARNING/STREAMING/COMPLETED)<br>• 오류/경고 발생 시 콘솔 유지 방어선<br>• 웹 드래그앤드롭 업로드 배치 추출(`_extract_latest_upload_batch`, `_normalize_uno_upload_relpath`) & 수동 텍스트 경로 동기화(`_pending_lc_meta_override`)<br>• 스피너(`spinner_slot`) 및 콘솔(`term_placeholder`) 컨테이너 슬롯 분리<br>• 계측 차속 대역 미검출(`all_empty`) 시 친절한 원인/조치 가이드 경고문 탑재<br>• PyCharm 디버거(pydevd) 몽키패치 해제 및 Streamlit 런처 안정화 | 2026-11-12 | ✅ 완료 |
| **30** | [[2026-11-15_v4.15_가감속_대시보드_사이버틱_UIUX_및_배경그래픽_네온바이올렛_정합_개발보고서|30. 가감속/제동(acc_brk) 대시보드 v2.0(v4.15) 사이버틱 다크 테크 UI/UX 완성, 배경 홀로그램 바퀴 국소 네온 바이올렛 정합 및 공식 매뉴얼 체계 수립 종합개발보고서]] | • 사이버틱 HUD 다크 테크 UI/UX 및 186px 사이드바 연결된 게이트웨이(Door Open!) 인터랙션<br>• 배경 홀로그램 시험 차량(cc_brk_hologram_bg.jpg) 타이어/바퀴 국소 네온 바이올렛(Hue 282°, #C084FC) 정밀 발광 튜닝<br>• 최상단 활성 프로젝트 및 팝오버 네온 바이올렛 테크 뱃지 테마 통일<br>• 차트 더블클릭(dblclick) 고해상도 새창 뷰어 및 공식 피규어 타이틀 파일명 자동 연동 다운로드<br>• 신규 Tab 5 Weather 기상 마스터 DB 연동 파이프라인 완결<br>• 16:9 Full HD 13-Slide 공식 PPTX 사용자 매뉴얼(ACC_BRK_DASHBOARD_USER_MANUAL.pptx) 및 1:1 기술 매뉴얼(dashboard_app.md) 전면 동기화 | 2026-11-15 | ✅ 완료 |
| **50** | [[2026-11-17_v4.23_acc_brk_모듈고도화_및_Circuit_Hydro_최종검증_종합개발보고서\|50. 가감속/제동(acc_brk) 모듈 및 웹 대시보드 v4.23 종합 고도화, WetHD 데이터 처리 통합 및 v2 표준 최종 검증 보고서]] | • 대시보드 인터랙션 버그(전체 삭제, 빈 프로젝트 전환) 완전 해결<br>• 첫 타이어 메타데이터 기반 병합 프로젝트명 자동 명명(표준 규격 준수) 및 중복 접미사 방지 로직<br>• 인터랙티브 테이블 조작 시 Rerun 멈춤 현상 제거 (st.form 구조 재설계)<br>• 대용량 프로젝트 파일 로드 시 0.01초 즉각 스피너 피드백 및 원본 경로 직결 로딩 최적화<br>• WetHD 데이터(`sample_handling_raw.pkl`, `total.pkl`) 처리 통합 및 지표 검증 | 2026-11-17 | ✅ 완료 |
| **40** | [[2026-11-16_v4.21_가감속_대시보드_SSOT_단일화_및_스마트드래그앤드롭_네이티브디렉토리_안정화_종합보고서|40. 가감속/제동(acc_brk) 대시보드 v2.0(v4.21) 백엔드 SSOT 전면 연동, 3단계 스마트 드래그앤드롭 네온 피드백 및 브라우저 네이티브 디렉토리 안정화 종합보고서]] | • 백엔드 도메인 상수/시그니처(vt_acc_brk, TestInformation, Unit) 100% SSOT 동적 연동 및 하드코딩 완전 제거<br>• 전 영역 stFileUploader 3단계 스마트 드래그앤드롭 네온 라임 호버(.uno-drag-over) & 에메랄드 시안 성공 플래시(.uno-drop-success) 피드백 구축<br>• 로컬 PC 실제 절대경로 역추적 알고리즘 전면 개편 (개발용 test_data 최하위 강등 및 실제 업무 폴더 D:/uno/1.2026 1순위 매칭 보장)<br>• TireCurve 순환 참조(Circular Import) 해결을 위한 __getattr__ 지연 로딩 패턴 적용 및 Clear all 크래시 원천 차단<br>• 브라우저 보안 정책에 의한 자바스크립트 가짜 이벤트 차단 및 MutationObserver 무한 루프(프리징) 완벽 해결 (HTML5 webkitdirectory 네이티브 표준 전환)<br>• Weather 탭 3초 토스트, 세션 격리, 4대 KPI ➔ 테이블 ➔ 100% 풀 와이드 Base64 고해상도 차트 레이아웃 최적화 | 2026-11-16 | ✅ 완료 |

---

## 🔗 상위 및 연계 문서
- 💼 **프로젝트 마스터 MOC**: [[00_unoUtil_모듈개발_대시보드]]
- 📖 **도메인 지식 사전**: [[vt_acc_brk_사전]]
- ⏱️ **응답성 보고서 MOC**: [[00_response_보고서_통합_색인]]
- 🛞 **마찰저하 보고서 MOC**: [[00_mu_drop_보고서_통합_색인]]
