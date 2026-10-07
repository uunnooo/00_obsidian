---
id: "20261006_ev3_work_status"
title: "2026-10-06 EV3 IW01 노면온도 민감도 및 제동 분석 작업 일지 (WORK_STATUS)"
type: work_status
date: 2026-10-06
status: 완료
tags:
  - 작업일지
  - EV3_IW01
  - 제동성능
  - 노면온도민감도
  - 옵시디언동기화
---

# 📝 [2026-10-06] EV3 IW01 제동 노면온도 민감도(Sensitivity) 분석 작업 일지

## 1. 📌 작업 개요
* **프로젝트명**: `Braking_AutoBuild / EV3_IW01` (기아 EV3 실차 제동 계측 데이터 분석)
* **작업 일시**: 2026-10-06
* **작업자**: uno & Gemini (Antigravity)
* **연계 마스터 리포트**: [[02_Projects/회사_업무/10_Braking_AutoBuild/20_EV3_IW01_노면온도_민감도_종합분석|20_EV3_IW01_노면온도_민감도_종합분석.md]]

---

## 2. 🚀 주요 작업 및 공학 성과 (Changelog)

### ① 노면온도 민감도 ($m = \text{m/}^\circ\text{C}$ 및 $\Delta D_{10^\circ\text{C}}$) 분석 프레임워크 수립
* 기존 단순 제동거리 절대치 비교에서 벗어나, **노면온도 $1^\circ\text{C}$ 상승 시 제동거리 변화율(기울기 $m$) 및 $10^\circ\text{C}$ 상승 시 제동거리 변화량($\Delta D_{10^\circ\text{C}}$)**을 핵심 평가지표로 정의하고 전 스펙 회귀 분석 수행.

### ② 외측 범례(Outside Legend) 스카터 플랏 및 민감도 바 차트 구축
* 그래프 내부 플롯 포인트를 가리던 범례 박스를 완전히 제거하고, 우측 바깥쪽(`bbox_to_anchor=(1.02, 1)`)으로 분리 배치.
* 산출된 차트 5종:
  1. `EV3_Sensitivity_Slope_Comparison.png` (노면별 온도 민감도 기울기 가로 바 차트)
  2. `EV3_Lane4_Wet_Low_Scatter.png` (Lane 4 Wet 저마찰 스카터 플랏 & 회귀선)
  3. `EV3_Lane1_Wet_High_Scatter.png` (Lane 1 Wet 고마찰 스카터 플랏 & 회귀선)
  4. `EV3_Lane7_Dry_Scatter.png` (Lane 7 Dry 고마찰 스카터 플랏 & 회귀선)
  5. `EV3_temperature_sensitivity_comparison.png` (3개 노면 통합 3패널 차트)

### ③ 핵심 공학 발견 및 타이어별 열안정성 평가
* **미쉐린 AP7 (`ex/MC/AP7`)**: Wet 저마찰(Lane 4)에서 $m = \mathbf{+0.157\text{ m/}^\circ\text{C}}$ ($10^\circ\text{C}$ 상승 시 **$+1.57\text{ m}$ 증가**)로 전 타이어 중 **온도에 가장 취약**함.
* **현용 IW01-X19 (KP)**: Wet 저마찰에서 $m = \mathbf{+0.056\text{ m/}^\circ\text{C}}$로 미쉐린 AP7 대비 **온도 민감도가 1/3 수준**에 불과하며, Dry 마른 노면에서는 $52.3^\circ\text{C}$ 초고온까지 $m = \mathbf{-0.030\text{ m/}^\circ\text{C}}$로 제동거리 불변의 압도적 사계절 안정성을 입증.
* **콘티넨탈 TS (`ex/CT/TS`)**: 7월과 8월 사이의 시험장 마찰계수 환경 시프트(-3~5m)가 결합되어 외견상 음의 기울기를 보이나, 동차수(8월 30차) 기준 Lane 1에서 26.75m로 현용 IW01-X19(26.76m)와 동등한 최상위권 젖은 노면 제동력을 증명.
* **신규 개발품 (QW01-A, QW01-B)**: QW01-A는 고온 노면에서 페이드 없는 접지력을 유지했고, QW01-B는 Lane 1에서 **$26.54 \sim 26.83\text{ m}$라는 독보적 1위의 절대 제동거리**를 기록.

### ④ 콘트롤 타이어 시계열 보간(Interpolation)에 따른 순서별 유불리 왜곡 메커니즘 규명
* 상대 제동 지수($\text{Index} = \frac{D_{\text{Control, interp}}}{D_{\text{Test, meas}}} \times 100\%$) 산출 시 분자(콘트롤 보간치) vs 분모(테스트 실측치)의 민감도 차이에 따른 순서 왜곡 모델링.
* **Control 대비 민감도 높음 ($m_T > m_C$)**: 선순위(오전/저온) 주행 시 유리 (분모 팽창 방지).
* **Control 대비 민감도 낮음 ($m_T < m_C$)**: 후순위(오후/고온) 주행 시 유리 (콘트롤 열화로 인한 분자 팽창 혜택 수혜).
* 인포그래픽 가이드 차트(`Control_Interpolation_Sensitivity_Bias_Guide.png`) 생성 및 옵시디언 동기화 완료.

---

## 3. 📂 배포 및 연동 파일 현황
1. **옵시디언 마스터 보고서**:
   * `D:\00_obsidian\02_Projects\회사_업무\10_Braking_AutoBuild\20_EV3_IW01_노면온도_민감도_종합분석.md`
2. **옵시디언 첨부 이미지 (전수 동기화)**:
   * `D:\00_obsidian\_attachments\10_회사_업무\EV3_Sensitivity_Slope_Comparison.png`
   * `D:\00_obsidian\_attachments\10_회사_업무\EV3_Lane1_Wet_High_Scatter.png`
   * `D:\00_obsidian\_attachments\10_회사_업무\EV3_Lane4_Wet_Low_Scatter.png`
   * `D:\00_obsidian\_attachments\10_회사_업무\EV3_Lane7_Dry_Scatter.png`
   * `D:\00_obsidian\_attachments\10_회사_업무\EV3_temperature_sensitivity_comparison.png`
   * `D:\00_obsidian\_attachments\10_회사_업무\Control_Interpolation_Sensitivity_Bias_Guide.png`
3. **정량 데이터 CSV 파일 배포 (Excel 호환 UTF-8-BOM)**:
   * `D:\00_obsidian\02_Projects\회사_업무\10_Braking_AutoBuild\EV3_Temperature_Sensitivity_Summary.csv`
   * `D:\00_obsidian\02_Projects\회사_업무\10_Braking_AutoBuild\EV3_Braking_Raw_Test_Data.csv`
   * `D:\uno\1. 2026\1. BRK\Autobuild IW01_EV3\EV3_Temperature_Sensitivity_Summary.csv`
   * `D:\uno\1. 2026\1. BRK\Autobuild IW01_EV3\EV3_Braking_Raw_Test_Data.csv`
4. **도메인 대시보드 최신화**:
   * `D:\00_obsidian\02_Projects\회사_업무\10_Braking_AutoBuild\00_Braking_AutoBuild_대시보드.md` (v2.1 Changelog 및 링크 등록 완료)
