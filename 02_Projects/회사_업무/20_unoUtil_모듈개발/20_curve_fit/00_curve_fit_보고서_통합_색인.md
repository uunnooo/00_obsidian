---
id: "curve_fit_reports_index"
title: "unoUtil curve_fit 타이어 커브 피팅 및 휠 딜레이 보정 보고서 통합 색인"
type: dashboard
category_main: 회사_업무
category_sub: unoUtil
category_detail: curve_fit
date: 2026-10-21
status: 진행중
tags:
  - 회사_업무
  - unoUtil
  - curve_fit
  - MOC
  - 색인
---

# 📈 unoUtil curve_fit 모듈 개발 및 검증 보고서 통합 색인 (MOC)

> **상위 대시보드 링크**: [[00_unoUtil_모듈개발_대시보드]]  
> **관련 소스 코드 저장소**: `unoUtil/curve_fit` (`cf_tire.py`, `estimators/`, `func_acc_brk.py`)  
> **첨부 파일 위치**: `_attachments/10_회사_업무/curve_fit/`

---

## 📑 등록 보고서 목록 (Reports Index)

| 번호 | 보고서 명칭 | 핵심 내용 및 물리 모델 | 작성 일자 | 상태 |
| :---: | :--- | :--- | :---: | :---: |
| **10** | [[10_휠속도_시간지연_보정_및_타이어_커브피팅_종합보고서\|10. 휠 속도 시간 지연(Time-Delay) 물리 보정 및 범용 타이어 커브 피팅 종합 보고서]] | • 톤휠 엔코더 ZOH 스텝 홀드 지연($\Delta t_{\text{step}}/2$) 및 CAN 고정 통신 지연($L_{\text{CAN}}$) 결합 규명<br>• `calc_wheel_delay_compensation()` 신호 레벨 선행 물리 복원<br>• 비구동 후륜 Bias $0.00\text{ km/h}$ 완전 소거 및 발진 슬립-뮤 궤적 복원 검증 | 2026-10-21 | ✅ 완료 |
| **20** | [[20_타이어_커브피팅_전면_개발스토리_및_공학검증보고서\|20. 타이어 커브 피팅 전면 고도화 개발 스토리 및 물리/공학 검증 종합 보고서]] | • 제동 Onset 역추적 복원 및 과도 응답 4대 랜드마크(L0~L3) 위상 정렬<br>• 4대 피팅 알고리즘(Constrained MF, 2D Blend, LeastSquares, Combiner) 비교 검증<br>• 2단 미분 분할 필터링 및 샘플링 레이트(20~200Hz) 자가 적응 불변성 입증 | 2026-10-20 | ✅ 완료 |
| **30** | [[30_가속_시험_타이어_커브피팅_검증보고서\|30. 가속(ACC) 시험 타이어 커브 피팅 검증 및 피팅 결과 보고서]] | • 25RD120007EF run1 및 25RD110010EF run2 가속 데이터셋 실증<br>• 구동륜 극저속 미세 슬립 거동 및 차체 가속도($\text{AccForward}$) 매칭 분석 | 2026-10-20 | ✅ 완료 |
| **40** | [[40_NoABS_실측_VBB_타이어_커브피팅_검증보고서\|40. unoUtil No-ABS 실측 VBB 타이어 커브 피팅 3대 추정기 검증 보고서]] | • 핀란드 이발로 테크노트랙 스노우 노면 No-ABS VBB 제동 시험 분석<br>• LeastSquares vs Combiner vs Optimizer 정량 성능(RMSE, $C_\kappa, \mu_{\text{peak}}$) 비교 | 2026-10-17 | ✅ 완료 |

---

## 🛠️ 연계 파이썬 소스 코드 (Core Modules)

* **커브 피팅 Facade SSOT**: `unoUtil/curve_fit/tire_curve/cf_tire.py`
* **휠 딜레이 보정 및 슬립 계산 엔진**: `unoUtil/vehicle/acc_brk/func_acc_brk.py` (`calc_wheel_delay_compensation`, `calc_slip`)
* **3대 추정기 엔진**:
  - `unoUtil/curve_fit/estimators/least_squares_estimator.py`
  - `unoUtil/curve_fit/estimators/combiner_estimator/combiner_estimator.py`
  - `unoUtil/curve_fit/estimators/optimize_estimator.py`
* **통합 배치 가감속 분석기**: `unoUtil/vehicle/acc_brk/vt_acc_brk.py`
