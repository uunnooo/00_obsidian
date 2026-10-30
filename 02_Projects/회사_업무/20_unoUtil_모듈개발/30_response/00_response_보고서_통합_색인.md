---
id: "response_report_index"
title: "unoUtil Response(과도 응답성) 모듈 검증 보고서 통합 색인"
type: index
category_main: 회사_업무
category_sub: unoUtil
category_detail: response
date: 2026-10-30
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - response
  - 과도응답
  - 색인
  - MOC
---

# ⏱️ unoUtil Response(과도 응답성) 모듈 검증 보고서 통합 색인 (MOC)

> [!ABSTRACT] 📖 Response 엔지니어링 보고서 허브
> 본 색인은 `unoUtil.vehicle.acc_brk` 패키지의 **과도 응답성 평가(`AnResponse`, `func_acc_brk.py`) 및 휠 속도 센서(WSS) 통신 지연/극저속 슬립 복원 파이프라인**에 대한 핵심 알고리즘 설계 원리와 실측 데이터(`25RD120007EF`) 실증 검증 보고서를 집대성한 전용 MOC입니다.

---

## 📑 모듈 검증 보고서 목록

| 번호 | 보고서 명칭 | 핵심 다룸 내용 및 실증 범위 | 작성일자 | 상태 |
| :---: | :--- | :--- | :---: | :---: |
| **10** | [[10_가속_제동_과도응답_Response_알고리즘_고도화_및_실측검증보고서\|10. 가속·제동 휠 딜레이 보정 및 과도 응답(Response/Rising) 알고리즘 고도화 및 실측 검증 보고서]] | • CAN 통신 지연($L_{\text{can}} \approx 20\text{ms}$) 및 극저속 WSS 0-Lock 데드존 탄성 슬립 복원<br>• 저마찰 노면 발진 역추적 창($\le 3.5\text{s}$) 및 적응형 기저점($A_{\text{base}}$) 역추적<br>• $d^2V/dt^2=0$ 1차 과도 피크 및 25~75% 적응형 타겟 대역 응답 지연($\Delta t_{\text{resp}}$)<br>• 순수 진폭 10~90% 라이징 기울기 회귀 및 3열/2×2 진단 대시보드 실측 검증 | 2026-10-30 | ✅ 완료 |

---

## 🔗 상위 및 연계 문서
- 💼 **프로젝트 마스터 MOC**: [[00_unoUtil_모듈개발_대시보드]]
- 📖 **도메인 지식 사전**: [[vt_acc_brk_사전]]
- 🏛️ **연계 공학 리소스**: [[31_실차_제동_시작점_자동_탐지_및_과도응답_슬립_복원_공학]]
