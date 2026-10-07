---
id: "20261007_ev3_work_status"
title: "2026-10-07 EV3 IW01 노면온도 민감도 및 콘트롤 보간 왜곡 분석 작업 일지 (WORK_STATUS)"
type: work_status
date: 2026-10-07
status: 완료
tags:
  - 작업일지
  - EV3_IW01
  - 제동성능
  - 노면온도민감도
  - 콘트롤보간왜곡
  - 옵시디언동기화
---

# 📝 [2026-10-07] EV3 IW01 제동 노면온도 민감도 & 콘트롤 보간 왜곡 종합 작업 일지

## 1. 📌 작업 개요
* **프로젝트명**: `Braking_AutoBuild / EV3_IW01` (기아 EV3 실차 제동 계측 데이터 분석)
* **작업 일시**: 2026-10-06 ~ 2026-10-07
* **작업자**: uno & Gemini (Antigravity)
* **도메인 대시보드**: [[02_Projects/회사_업무/10_Braking_AutoBuild/00_Braking_AutoBuild_대시보드|00_Braking_AutoBuild_대시보드.md]] (v2.2 등록)
* **연계 마스터 리포트**: [[02_Projects/회사_업무/10_Braking_AutoBuild/20_EV3_IW01_노면온도_민감도_종합분석|20_EV3_IW01_노면온도_민감도_종합분석.md]]

---

## 2. 🚀 주요 작업 및 공학 성과 (Changelog)

### ① 노면온도 민감도 ($m = \text{m/}^\circ\text{C}$ 및 $\Delta D_{10^\circ\text{C}}$) 정량화 체계 수립
* 노면온도 $1^\circ\text{C}$ 상승 시 제동거리 변화율(기울기 $m$) 및 $10^\circ\text{C}$ 상승 시 제동거리 변화량($\Delta D_{10^\circ\text{C}}$)을 핵심 평가지표로 정의하고 전 스펙 회귀 분석 수행.
* 외측 범례(Outside Legend) 스카터 플랏 4종 및 노면별 민감도 바 차트 생성.

### ② 타이어 스펙별 열안정성 및 이상치 규명
* **미쉐린 AP7 (`ex/MC/AP7`)**: Wet 저마찰(Lane 4)에서 $m = \mathbf{+0.157\text{ m/}^\circ\text{C}}$ ($10^\circ\text{C}$ 상승 시 **$+1.57\text{ m}$ 증가**)로 전 타이어 중 **온도에 가장 취약**함.
* **현용 IW01-X19 (KP)**: Wet 저마찰에서 $m = \mathbf{+0.056\text{ m/}^\circ\text{C}}$로 미쉐린 AP7 대비 **온도 민감도가 1/3 수준**에 불과하며, Dry 마른 노면에서는 $52.3^\circ\text{C}$ 초고온까지 $m = \mathbf{-0.030\text{ m/}^\circ\text{C}}$로 제동거리 불변의 압도적 사계절 안정성을 입증.
* **콘티넨탈 TS (`ex/CT/TS`)**: 7월과 8월 사이의 시험장 마찰계수 환경 시프트(-3~5m)가 결합되어 외견상 음의 기울기를 보이나, 동차수(8월 30차) 기준 Lane 1에서 26.75m로 현용 IW01-X19(26.76m)와 동등한 최상위권 젖은 노면 제동력을 증명.
* **신규 개발품 (QW01-A, QW01-B)**: QW01-A는 고온 노면에서 페이드 없는 접지력을 유지했고, QW01-B는 Lane 1에서 **$26.54 \sim 26.83\text{ m}$라는 독보적 1위의 절대 제동거리**를 기록.

### ③ 콘트롤 타이어 시계열 보간(Interpolation) 순서 왜곡 메커니즘 규명
* 상대 제동 지수($\text{Index} = \frac{D_{\text{Control, interp}}}{D_{\text{Test, meas}}} \times 100\%$) 산출 시 분자(콘트롤 보간치) vs 분모(테스트 실측치)의 민감도 차이에 따른 순서 왜곡 모델링.
* **Control 대비 민감도 높음 ($m_T > m_C$)**: 오후로 갈수록 분모 급팽창 ➔ **선순위(오전/저온) 주행 시 유리**.
* **Control 대비 민감도 낮음 ($m_T < m_C$)**: 오후에 콘트롤 열화로 분자 팽창 ➔ **후순위(오후/고온) 주행 시 유리 (+3.0%p 가산점)**.
* **고온 점착/개선형 ($m_T < 0$)**: 오후에 실측거리는 줄고 분자는 커져 **후순위 주행 시 지수 대폭등 (+7.9%p 폭등, 최대 9.8%p 등급 역전)**.
* 교육용 3패널 인포그래픽 가이드 차트(`Control_Interpolation_Sensitivity_Bias_Guide.png`) 제작 및 옵시디언 영구 임베드.

### ④ CT-TS, IW01-X19, QW01 대상 실전 수치 시뮬레이터 엑셀 개발
* 기준온도($20^\circ\text{C}$)에서 30.0m로 동일한 성능의 세 타이어가 시험 순서에 따라 어떻게 평가가 뒤바뀌는지 시뮬레이션한 전용 엑셀(`Control_Interpolation_Simulation_CT_IW01_QW01.xlsx` / `.csv`) 개발 및 배포.

---

## 3. 📂 배포 및 연동 파일 현황

1. **옵시디언 마스터 보고서**:
   * `D:\00_obsidian\02_Projects\회사_업무\10_Braking_AutoBuild\20_EV3_IW01_노면온도_민감도_종합분석.md`
2. **도메인 대시보드 (v2.2 갱신 완료)**:
   * `D:\00_obsidian\02_Projects\회사_업무\10_Braking_AutoBuild\00_Braking_AutoBuild_대시보드.md`
3. **옵시디언 첨부 이미지 (전수 동기화)**:
   * `D:\00_obsidian\_attachments\10_회사_업무\Control_Interpolation_Sensitivity_Bias_Guide.png`
   * `D:\00_obsidian\_attachments\10_회사_업무\EV3_Sensitivity_Slope_Comparison.png`
   * `D:\00_obsidian\_attachments\10_회사_업무\EV3_Lane1_Wet_High_Scatter.png`
   * `D:\00_obsidian\_attachments\10_회사_업무\EV3_Lane4_Wet_Low_Scatter.png`
   * `D:\00_obsidian\_attachments\10_회사_업무\EV3_Lane7_Dry_Scatter.png`
   * `D:\00_obsidian\_attachments\10_회사_업무\EV3_temperature_sensitivity_comparison.png`
4. **정량 데이터 CSV 및 시뮬레이션 Excel 파일 배포 (이중 동기화)**:
   * `D:\00_obsidian\02_Projects\회사_업무\10_Braking_AutoBuild\Control_Interpolation_Simulation_CT_IW01_QW01.xlsx`
   * `D:\00_obsidian\02_Projects\회사_업무\10_Braking_AutoBuild\Control_Interpolation_Simulation_CT_IW01_QW01.csv`
   * `D:\uno\1. 2026\1. BRK\Autobuild IW01_EV3\Control_Interpolation_Simulation_CT_IW01_QW01.xlsx`
   * `D:\uno\1. 2026\1. BRK\Autobuild IW01_EV3\Control_Interpolation_Simulation_CT_IW01_QW01.csv`
   * `D:\00_obsidian\02_Projects\회사_업무\10_Braking_AutoBuild\EV3_Temperature_Sensitivity_Summary.csv`
   * `D:\00_obsidian\02_Projects\회사_업무\10_Braking_AutoBuild\EV3_Braking_Raw_Test_Data.csv`
   * `D:\uno\1. 2026\1. BRK\Autobuild IW01_EV3\EV3_Temperature_Sensitivity_Summary.csv`
   * `D:\uno\1. 2026\1. BRK\Autobuild IW01_EV3\EV3_Braking_Raw_Test_Data.csv`
