---
id: "circuit_report_index"
title: "unoUtil 서킷 및 조종안정성(Circuit) 모듈 검증 보고서 통합 색인"
type: index
category_main: 회사_업무
category_sub: unoUtil
category_detail: circuit
date: 2026-11-16
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - circuit
  - handling
  - 조종안정성
  - 색인
  - MOC
---

# 🏎️ unoUtil 서킷 및 조종안정성(Circuit) 모듈 검증 보고서 통합 색인 (MOC)

> [!ABSTRACT] 📖 Circuit 엔지니어링 보고서 허브
> 본 색인은 `unoUtil.vehicle_test.circuit` 패키지의 **서킷 조종안정성 평가(WetHD 레거시 100% 호환 복원), 8대 서브 분석기 체계, 프로세스 기반 7대 통합 대시보드 및 온디맨드 GPS 가속도 히트맵 트랙맵, 순환 랩(Closed Loop Lap) 분할 정상화**에 대한 종합 기술 개발 및 실측 데이터(`sample_handling.vbo`, `Technoring 6개 타이어`) 실증 검증 보고서를 집대성한 전용 MOC입니다.

---

## 📑 모듈 검증 보고서 목록

| 번호 | 보고서 명칭 | 핵심 다룸 내용 및 실증 범위 | 작성일자 | 상태 |
| :---: | :--- | :--- | :---: | :---: |
| **10** | [[2026-11-16_v4.20_서킷_조종안정성_모듈_전면고도화_60대결과인자복원_통합대시보드_순환랩분할_종합검증보고서\|10. 서킷 및 조종안정성 모듈 전면 고도화, WetHD 60대 핵심 결과 인자 100% 복원, 7대 프로세스 통합 대시보드 및 순환 랩 분할 종합 검증 보고서]] | • WetHD 60대 핵심 결과 인자(단일 타이어 54종 + 프로젝트 6종) 전수 100% 복원 및 실측 수치 대조 검증<br>• 34개 난립 창 ➔ 분석기별 1-대시보드 피규어(7종) + 온디맨드 가속도 트랙맵(1종) 압축 및 화면 60~65% 최적 황금비율 정립<br>• `cKDTree` 결측치(NaN/Inf) 방어 및 궤적 선형 보간(`bfill/ffill`) 3중 방어막 완비<br>• 5.5km 가상 마진 결함 철거 및 `find_continuous_interval` 기반 순환 랩(75~78초) 분할 정상화<br>• 한국테크노링 6개 타이어 실차 시험 데이터 배치 분석 검증 완료 (Exit Code 0) | 2026-11-16 | ✅ 완료 |

---

## 🔗 상위 및 연계 문서
- 💼 **프로젝트 마스터 MOC**: [[00_unoUtil_모듈개발_대시보드]]
- 📖 **도메인 지식 사전**: [[circuit_사전]]
- 🏛️ **연계 도메인 MOC**: [[00_curve_fit_보고서_통합_색인]], [[00_response_보고서_통합_색인]], [[00_mu_drop_보고서_통합_색인]]
