---
id: "circuit_report_index"
title: "unoUtil 서킷 및 조종안정성(Circuit) 모듈 검증 보고서 통합 색인"
type: index
category_main: 회사_업무
category_sub: unoUtil
category_detail: circuit
date: 2026-11-25
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
> 본 색인은 `unoUtil.vehicle_test.circuit` 패키지의 **서킷 조종안정성 평가(WetHD 레거시 100% 호환 복원), 8대 서브 분석기 체계, 프로세스 기반 12대 통합 대시보드 및 온디맨드 GPS 가속도 히트맵 트랙맵, 순환 랩(Closed Loop Lap) 분할 정상화**에 대한 종합 기술 개발 및 실측 데이터(`sample_handling.vbo`, `Technoring 6개 타이어`) 실증 검증 보고서를 집대성한 전용 MOC입니다.

---

## 📑 모듈 검증 보고서 목록

| 번호 | 보고서 명칭 | 핵심 다룸 내용 및 실증 범위 | 작성일자 | 상태 |
| :---: | :--- | :--- | :---: | :---: |
| **50** | [[2026-11-24_v4.36_서킷_조종안정성_WetHD_KDE_동적구배_물리엔진_1대1_호환_및_시각화_고도화_종합보고서|50. 서킷 조종안정성 WetHD KDE 동적구배 물리 엔진 1:1 완벽 호환 및 시각화 고도화 종합보고서]] | • WetHD analysis_gradient_v2 물리 엔진 1:1 완벽 호환(`calc_dynamic_gradients`) 및 턴인 단조 증가 구간 정밀 추출<br>• 조타 및 전/후륜 슬립 구배(`VehSWA_grad`, `ReferSlipFront_grad`, `ReferSlipRear_grad`) KDE 최빈 피크 및 신뢰 대역 산출<br>• 언더스티어 구배($K_{us}$) 및 15% 포화 조향각 탐색 엔진 정합<br>• `PlotterTire` 4대 핵심 시각화 피규어(`gradient_kde`, `understeer_curve` 축 전환, `vehicle_balance` 통계 집계 음영/평균선, `friction_circle` 4대 극치점 마커 배지) 정밀 튜닝 | 2026-11-24 | ✅ 완료 |
| **40** | [[2026-11-23_circuit_진행보고서_파이프라인안정성검증\|40. circuit 모듈 파이프라인 안정성 검증 세부 진행보고서]] | • `vt_circuit` 최상위 오케스트레이터 및 하위 8대 분석기 파이프라인 무결성 검증<br>• `cKDTree` 기반 궤적 분석 시 결측치(NaN/Inf) 방어 로직 완비<br>• `normalize_circuit_time()` 내 자정 롤오버 0.001초 단위 정밀 보정으로 서킷 랩타임 오차 완전 해소 | 2026-11-23 | ✅ 완료 |
| **30** | [[2026-11-20_v2.0_circuit_고도화_세부작업보고서\|30. circuit 모듈 고도화 상세 구현 작업 보고서]] | • `circuit_enhancement_plan.md` 4대 영역 1:1 대응 구현 완결<br>• `VTCircuitProject`/`VTCircuitTire` 편의 인터페이스 10종 완비 및 순환참조 방지<br>• 5대 동역학 채널 이상치 정제(`StatsParallelDF`), 전/후륜 슬립각 구배(FSG/RSG), 랩 열화 분석 복원<br>• 시각화 엔진 신규 대시보드 6종 탑재 및 Technoring 6개 타이어 실데이터 배치 검증 통과 | 2026-11-20 | ✅ 완료 |
| **매뉴얼** | [[friction_circle_fitting\|복합 마찰원(GG Diagram) 95% 한계 경계선 피팅 및 면적 적분 알고리즘]] | • 2D KDE 노이즈 필터링/분위수 추출/주기적 B-스플라인 피팅 기술 상세 | 2026-11-19 | ✅ 완료 |
| **20** | [[2026-11-17_v4.23_서킷_조종안정성_모듈_전면고도화_시간축정규화_대표이벤트추출_종합검증보고서\|20. 서킷 및 조종안정성 모듈 전면 고도화, 시간축(VBO 분 점프) 정규화 및 대표 조종 응답 이벤트(In/Out/Apex) 자동 추출 종합검증보고서]] | • VBO 데이터 분 점프(40.01초) 가상 시간 점프 감지 및 연속 초(Seconds) 시계열 정규화<br>• 대표 조종 응답 구간 탐색 알고리즘(조향 반전 에너지 기반 In/Out/Apex 구간 자동 추출 및 5초 구간 정밀 분석)<br>• 300ms 스무딩 미분 및 채터링 방어(`min_segment_len`) 알고리즘 탑재 및 지표 정합성 고도화 | 2026-11-17 | ✅ 완료 |
| **10** | [[2026-11-16_v4.20_서킷_조종안정성_모듈_전면고도화_60대결과인자복원_통합대시보드_순환랩분할_종합검증보고서\|10. 서킷 및 조종안정성 모듈 전면 고도화, WetHD 60대 핵심 결과 인자 100% 복원, 7대 프로세스 통합 대시보드 및 순환 랩 분할 종합 검증 보고서]] | • WetHD 60대 핵심 결과 인자(단일 타이어 54종 + 프로젝트 6종) 전수 100% 복원 및 실측 수치 대조 검증<br>• 34개 난립 창 ➔ 분석기별 1-대시보드 피규어(7종) + 온디맨드 가속도 트랙맵(1종) 압축 및 화면 60~65% 최적 황금비율 정립<br>• `cKDTree` 결측치(NaN/Inf) 방어 및 궤적 선형 보간(`bfill/ffill`) 3중 방어막 완비<br>• 5.5km 가상 마진 결함 철거 및 `find_continuous_interval` 기반 순환 랩(75~78초) 분할 정상화<br>• 한국테크노링 6개 타이어 실차 시험 데이터 배치 분석 검증 완료 (Exit Code 0) | 2026-11-16 | ✅ 완료 |

---

## 🔗 상위 및 연계 문서
- 💼 **프로젝트 마스터 MOC**: [[00_unoUtil_모듈개발_대시보드]]
- 📖 **도메인 지식 사전**: [[circuit_사전]]
- 🏛️ **연계 도메인 MOC**: [[00_curve_fit_보고서_통합_색인]], [[00_response_보고서_통합_색인]], [[00_mu_drop_보고서_통합_색인]]
