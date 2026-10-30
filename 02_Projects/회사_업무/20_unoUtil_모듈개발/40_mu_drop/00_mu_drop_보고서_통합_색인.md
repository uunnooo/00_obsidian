---
id: "mudrop_report_index"
title: "unoUtil Mu-Drop(마찰 저하 분석) 모듈 검증 보고서 통합 색인"
type: index
category_main: 회사_업무
category_sub: unoUtil
category_detail: mu_drop
date: 2026-10-30
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - mu_drop
  - abs
  - 제동
  - 색인
  - MOC
---

# 🛞 unoUtil Mu-Drop(마찰 저하 분석) 모듈 검증 보고서 통합 색인 (MOC)

> [!ABSTRACT] 📖 Mu-Drop 엔지니어링 보고서 허브
> 본 색인은 `unoUtil.vehicle.acc_brk` 패키지의 **Mu-Drop 분석(`AnMuDrop`, `func_acc_brk.py`) 및 ABS 제동 시 발생하는 마찰 저하·오실레이션 분석 파이프라인**에 대한 핵심 알고리즘 설계 원리와 실측 데이터(`25RD120004EF`) 실증 검증 보고서를 집대성한 전용 MOC입니다.

---

## 📑 모듈 검증 보고서 목록

| 번호 | 보고서 명칭 | 핵심 다룸 내용 및 실증 범위 | 작성일자 | 상태 |
| :---: | :--- | :--- | :---: | :---: |
| **10** | [[10_MuDrop_강건_분석_알고리즘_고도화_및_실측검증보고서\|10. Mu-Drop 강건(Robust) 분석 알고리즘 고도화 및 실측 검증 보고서: 피칭 보정 · 영위상 추세선 · 오실레이션 포락선]] | • 초기 제동 피칭 다이브 & 리바운드 비대칭 보정($\Delta V_{\text{trans}} = 14\%$ 앵커링)<br>• 속도 축 등간격 빈($\Delta V = 0.5\text{kph}$) 기반 영위상($\angle H = 0$) 추세선<br>• 차륜 가속도 RMS 및 감속도 Std 듀얼 오실레이션 포락선($Z_{\text{osc}}$) 추출<br>• 3D 스무딩 상태 공간 K-Means + DT 분기 속도 및 속도 균등 대표 감속도 산출 | 2026-10-30 | ✅ 완료 |

---

## 🔗 상위 및 연계 문서
- 💼 **프로젝트 마스터 MOC**: [[00_unoUtil_모듈개발_대시보드]]
- 📖 **도메인 지식 사전**: [[vt_acc_brk_사전]]
- 🛑 **연계 제동 공학 리소스**: [[20_ABS_로직_및_3단계_유압제어_분석]], [[30_실차_가감속_성능변화_분석_및_보정_시스템]]
