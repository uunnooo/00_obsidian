---
id: "unoutil_project_hub"
title: "unoUtil 사내 파이썬 통합 프레임워크 개발 프로젝트"
type: project
category_main: 회사_업무
category_sub: unoUtil
date: 2026-09-10
status: 진행중
tags:
  - 회사_업무
  - unoUtil
  - 파이썬
  - 개발도구
  - 대시보드
  - MOC
  - 아키텍처
  - 코딩표준
aliases:
  - unoUtil_모듈개발_대시보드
  - unoUtil개발허브
  - unoUtil_아키텍처_및_표준가이드
  - 00_unoUtil_PEP8_표준화_총괄_가이드
  - UNOUTIL_ARCHITECTURE
  - UNOUTIL_V2_REFACTORING_REPORT
  - 01_test_data_통합관리_계획서
  - "00_curve_fit_대시보드"
  - "curve_fit_대시보드"
  - "00_file_reader_대시보드"
  - "00_graphics_대시보드"
  - "00_models_대시보드"
  - "00_post_process_대시보드"
  - "00_utils_대시보드"
  - "00_vehicle_dynamic_대시보드"
  - "00_vt_acc_brk_대시보드"
  - "00_snow_condition_대시보드"
  - "snow_condition_대시보드"
  - "file_reader_대시보드"
  - "graphics_대시보드"
  - "models_대시보드"
  - "post_process_대시보드"
  - "utils_대시보드"
  - "vehicle_dynamic_대시보드"
  - "vt_acc_brk_대시보드"
---

# 💼 unoUtil 사내 파이썬 통합 프레임워크 개발 프로젝트 (Master MOC)

> ⚡ **Quick Jump**: [📅 1. 체인지로그](#-1-프로젝트-주요-버전-이력-changelog-타임테이블) · [🏛️ 2. 아키텍처](#️-2-clean-architecture-12대-도메인-아키텍처) · [📖 도메인 지식 사전](#-unoutil-12대-도메인-지식-사전-engineering-dictionaries-hub) · [🏎️ 3. vehicle/acc_brk](#️-3-vehicle-동역학--가감속제동-vt_acc_brk-도메인) · [🚀 4. file_reader](#-4-file_reader-이기종-계측-데이터-리더-도메인) · [🎨 5. graphics](#-5-graphics-실차-시각화-및-인터랙션-도메인) · [🎯 6. curve_fit](#-6-curve_fit-커브-피팅-및-타이어-곡선-도메인) · [📐 7. models](#-7-models-공학-지배-수식-도메인) · [📶 8. signal_process](#-8-signal_process-신호-후처리-및-정제-도메인) · [🛠️ 9. utils/logger](#️-9-utils--logger-공통-유틸리티-도메인) · [🤖 10. ai/db/stats/gps](#-10-aidatabasestatisticsgps-기타-도메인) · [❄️ 11. snow_condition](#-11-snow_condition-노면-환경--머신러닝-보정-도메인) · [📖 12. 엔지니어링 표준](#-12-사용자-매뉴얼-및-엔지니어링-표준)

> [!ABSTRACT] 🚀 unoUtil 단일 마스터 MOC 허브
> 사내 파이썬 실차 데이터 분석 프레임워크 **`unoUtil v2.0+`**의 10대 도메인, 87개 핵심 모듈 기술 매뉴얼, Clean Architecture 명세 및 버전 관리 이력을 단일 페이지에서 1화면으로 조망·관리하는 **중앙 마스터 MOC 포털**입니다.

---

## 📅 1. 프로젝트 주요 버전 이력 (Changelog 타임테이블)

> [!NOTE]- 📜 v1.0 ~ v3.60 주요 개발 및 리팩토링 이력 [클릭하여 펼치기]
> | 버전 | 날짜 | 작업자 | 핵심 수정 및 개발 내역 (Changelog) | 상태 |
> | :--- | :---: | :---: | :--- | :---: |
| **v3.68** | 2026-10-27 | uno &<br/>Gemini | 🏛️ **unoUtil v2.0 전면 레거시 소멸, 전 패키지 상대 참조 100% 절대 참조(`unoUtil.*`) 전환, 4대 대원칙 기반 과거 레거시 폴더/파일/별칭(32개 모듈) 전수 소멸, 최상위 루트 `__init__.py` 슬림화 및 SSOT 표준화 완결 종합 보고서([[01_unoUtil_v2_전면_레거시_소멸_및_SSOT_단일화_완결_보고서]]) 등재**<br/>• **전 패키지 상대 참조 100% 절대 참조 전환**: 33개 파일 내 `from .` 상대 참조를 `unoUtil.*` 절대 참조로 전수 치환하여 모듈 단위 독자 실행(`__main__`) 시 `attempted relative import` 에러를 원천 박멸<br/>• **4대 대원칙 기반 과거 레거시 전면 소멸**: 빈 `legacy/` 7개소, 과도기 브릿지 4종(`ai/*`, `curve_fit/tire_curve/fit_least_squares.py`), 잔여 `signal_process/curve_fit` 폴더, 백업(`.bak`) 및 임시 산출물(`1`, `.pytest_cache`, `egg-info`) 전수 삭제<br/>• **32개 모듈 내부 레거시 별칭(Aliases) 전수 제거**: 모듈 하단에 잔존하던 구버전 별칭(`Infor_Vehicle`, `VD_*` 8종, `SP_CurveFit_*` 4종, `CurveCombiner`, `MinimizeEstimator`, `SP_Resample`, `TireMagicFormula` 등) 전면 삭제 및 표준 명칭(SSOT) 단일화<br/>• **최상위 루트 `__init__.py` 250줄 슬림화**: 과거 메타패스 가상 리다이렉터 및 가상 모듈 바인딩 완전 제거, 12대 공식 도메인 순수 Facade(180줄)로 재탄생<br/>• **비매뉴얼 보고서 볼트 안전 이관**: `tire_curve_pipeline_and_real_data_issues.md`를 볼트 `25_실차_계측데이터_태생적_문제점과_8단계_통합파이프라인_백서.md`로 신규 이관, 코드 폴더에는 81개 순수 1:1 기술 매뉴얼만 격리 보존 | ✅ 완료 |
| **v3.67** | 2026-10-27 | uno &<br/>Gemini | 🚀 **`unoUtil.file_reader` 이기종 계측 리더 전 파서 컬럼명 순수화 & units 단일 표준화, 비정형 TXT 지능형 헤더 탐색 엔진(`HeaderFinder`) 신설, 패키지 전수 절대 참조 전환, 순수 1:1 기술 매뉴얼 헌장(`code-manual-writer` 스킬) 및 도메인 지식 사전 상시 동기화(Living Sync) 완결**<br/>• **전 파서 컬럼명 순수화 & 단위 100% 분리**: VBB, VBO, DWD, TXT 전 파서에서 컬럼명의 대괄호/단위 기호(`[unit]`)를 완전 배제하고 순수 채널명 단일 레벨로 통일, 물리 단위는 `reader.units` (`Dict[str, str]`) 단일 표준 규격으로 일괄 분리 정합<br/>• **비정형 TXT 지능형 헤더 탐색 엔진 신설 (`header_finder.py`)**: unoUtil v1 레거시 거리 가중치 스코어링 공식($Score = L \times (1 - 0.1 \times D)$) 및 연속 수치 안정성 변곡점 분석을 모듈화하여 상단 주석이 긴 비정형 TXT 파일에서도 채널명/단위/데이터 시작점을 100% 자율 식별하고 공백 내 `Name [Unit]` 결합 파싱 및 중복 컬럼명 자동 고유화 방어 구현<br/>• **패키지 전수 절대 참조(`unoUtil.file_reader.*`) 전환**: 모든 서브파서 및 하위 유틸 내 상대 참조(`from .`)를 절대 참조로 100% 치환하여 모듈 단위 독자 실행(`__main__`) 및 단위 테스트 완벽 보장<br/>• **순수 1:1 기술 매뉴얼 작성 헌장 및 신규 전문 스킬 신설**: 옵시디언 위키링크를 배제한 순수 GFM 규격, 키워드 인자(`**kwargs`) 전수 명세표, 2-Track 실전 예제를 강제하는 `code-manual-writer` 스킬 및 마스터 룰북 조항 공식 등재<br/>• **레거시 코드, 별칭, 패칭 및 폴더 전면 삭제 (Clean v2 순수화)**: 빈 `legacy/` 폴더 물리적 완전 삭제, `__init__.py` 내 `sys.modules` 패칭 4개 행 및 `ReadDataFile` 별칭 제거, `file_data_reader.py` 내 `to_legacy_tuple`, `_CallableModule`, `print` 레거시 키워드 제거 및 `verbose` 단일 표준화, `base_parser.py` 내 `to_legacy_tuple` 제거, `standard_channel_pattern.py` 내 `funcChangeSignalName` 제거, `dwdReader.py` 내 `dwdRead`/`diagnoseDWD` 제거로 100% 직교적 단일 표준(SSOT) 완결<br/>• **도메인 지식 사전(`file_reader_사전.md`) Living Sync**: 신규 아키텍처 다이어그램 및 HeaderFinder 역할을 볼트 도메인 지식 사전에 직접 동기화 반영 | ✅ 완료 |
| **v3.66** | 2026-10-22 | uno &<br/>Gemini | 🛞 **`unoUtil.curve_fit.tire_curve` 실차 계측 신호처리부터 구속조건 Magic Formula(MF) 피팅까지 8단계 통합 파이프라인 완결, 절제된 딥 네이비 단색 Chevron 화살표 PPTX 프레젠테이션 제작, 가속/제동 전 관점 통합 기술 백서(`tire_curve_pipeline_and_real_data_issues.md`) 수립 및 실측 로우 데이터 4대 태생적 한계 4분할(2×2) 종합 진단 차트(`plot_raw_data_limitations.py`) 실증 완결**<br/>• **8단계 통합 엔지니어링 파이프라인 수립**: ① 원시 신호 입력 & 휠속도 결측 가드(`ptp > 1e-3, std > 1e-4`) ➔ ② CAN 지연 보상(`wheel_delay_compensated`) 및 구동계(RWD/AWD/FWD) 슬립 채널 선별 ➔ ③ Jerk 도함수 융합 Onset($t_0$) 복원 및 이상 회차 배제 ➔ ④ 4대 과도응답 랜드마크($L0\to L1\to L2\to L3$) 위상 동기화 및 초기 탄성 강성($K_{\text{pk}}=\mu_{L2}/s_{L2}$) 확정 ➔ ⑤ 3단 데이터 분리(관성 데드존/과도 휠스파이크/차속 컷오프) 및 본체 0.15s 영위상 스무딩 ➔ ⑥ 슬립 구간 밀도 역가중치($w_i \propto 1/\text{count}^{0.65}$) & IQR 국소 이상치 감쇠 ➔ ⑦ 원점 강성 등식 제약($B = K_{\text{pk}} / (C \cdot D)$) 기반 3변수 $(C, D, E)$ `soft_l1` TRF 비선형 피팅 ➔ ⑧ 표준 6-파라미터 복원 및 대표 곡선 테이블 생성<br/>• **보고/발표용 맞물림 Chevron 화살표 슬라이드 제작 (`tire_curve_pipeline_flowchart.pptx`)**: 과도한 원색 및 자잘한 불릿 텍스트를 전면 배제하고, 차분한 모던 딥 네이비 단색 기반의 8단계 맞물림 갈매기형 화살표(`MSO_SHAPE.CHEVRON`) 프로세스 1페이지 압축 슬라이드 완성<br/>• **가속 및 제동 전 관점 통합 기술 백서 구축 (`tire_curve_pipeline_and_real_data_issues.md`)**: 실차 계측 데이터의 태생적 5대 한계 규명(운전자 조작 지터, 센서 딜레이, 관성 데드존/스파이크, 제어기 슬립 편중, 미분/유압 노이즈) 및 제동 vs 가속 12대 비교 매트릭스 집대성<br/>• **실측 로우 데이터 현상 실증 4분할(2×2) 종합 진단 차트 구축 (`plot_raw_data_limitations.py` ➔ `real_vehicle_raw_data_limitations.png`)**: 실측 제동(19,522개) 및 가속(32,753개) 데이터를 인위적 색상 구분 없이 '단일 회색(Gray) 산점도'로 표출하여 실차 데이터의 현실적 난점을 그대로 살리고, 레전드를 없애고 핵심 물리 현상 주석만 집중 배치: (a) 제동 슬립 산점도 4대 왜곡 & Naive 피팅 파탄, (b) 가속 노이즈 구름 & 트랙션 이탈, (c) 다중 런 조작 타이밍 지터($\sigma \approx 24.5\text{ms}$)와 단순 시간평균 시 피크 15~25% 상쇄 붕괴(Phase Blur), (d) 시간 경과에 따른 노면 마찰 드리프트($C1 \ne C2$)와 콘트롤 타이어(Control) 보정 필요성 실증 | ✅ 완료 |
> | **v3.65** | 2026-10-22 | uno &<br/>Gemini | 🛞 **curve_fit 타이어 커브 과도기 위상 동기화(Phase Alignment)·인덱스 정합 메커니즘 정립, 점 군집(Cluster) 이동 검증, 볼트 20_curve_fit 보고서 전 도판 18종 일괄 코드화(
un_all.py 100% PASS), 콘트롤 타이어 보정(스케일링 동형성) 아키텍처 완결 및 	ire_curve_사전.md 신설**<br/>• **과도기 위상 동기화 판정 기준 및 물리 랜드마크 교차 정합 정립 (ig10_transient_sync_criteria.py)**: 단일 신호 고정이 아니라, 차체 관성 지연 구간(\to L1$)은 슬립(Slip) 극대($\max s$)를 기준, 타이어 바이트 구간(\to L2$)은 감속도(Decel Mu) 극대($\max \mu$)를 교차 기준으로 동기화하는 물리적 랜드마크 정합 메커니즘 수립 및 실측 검증 도판 구축<br/>• **타이밍 지터(Jitter) 극복 38개 고정 인덱스(=0\sim 37$) 정합 구조 규명 (ig12_index_alignment_explained.py, ig14_acc_jitter_alignment.py)**: 회차마다 27~33개(제동) 및 20~86개(가속)로 불균일한 원시 샘플을 38개 고정 인덱스로 리샘플링하여 피크를 28번 인덱스에 일제히 결집시킴으로써, 단순 시간 평균 시 발생하는 피크 평탄화(Phase Blur) 및 초기 강성($) 왜곡을 완벽 소거. 특히 발진 시차 0.61초에 달하는 가속 시험에서 트랙션 무릎점($) 및 구동 탄성 강성(=2.66$) 복원 실증<br/>• **선(Line)의 흩어짐 착시 극복 및 인덱스별 점(Point) 군집 진화 검증 (ig13_point_cluster_evolution.py, ig13b_acc_point_cluster_evolution.py)**: 선으로 보면 루프 폭이 달라 흩어져 보이지만, 38개 인덱스 $ 순서대로 점을 찍으면 매 스텝마다 4~6개 런의 점들이 좁은 클러스터($\sigma_\mu \le 0.025\text{g}$)로 똘똘 뭉쳐서 이동함을 실측 데이터로 증명<br/>• **제동/가속 시작점 복원 및 4대 랜드마크 시계열 동시 표기 (ig1a_brk_onset_recovery.py, ig1b_acc_onset_recovery.py)**: 실제 물리적 $ Onset 시간축(=0\text{s}$) 정합 리셋으로 수직 가이드라인과 곡선 피크의 100% 일치를 실현하고, 표준 속도 컷오프(\to 8\text{kph}$, \to 40\text{kph}$)로 소실되던 초기 탄성 과도 구간을 완벽 회수<br/>• **볼트 20_curve_fit 4대 보고서 전 도판 파이썬 코드화 및 자립 구축 (18종 완비)**: 10호 보고서 휠속도 지연 보정 도판 5종(
eport10_delay_compensation_figures.py), 20/30호 보고서 타이어별/프로젝트별 도판 15종(
eport20_30_batch_curve_fit_reports.py), 40호 보고서 No-ABS 3대 추정기 도판 4종(
eport40_noabs_strategy_comparison.py)을 완비하고 통합 러너 
un_all.py 18건 전수 100% PASS 검증 완료<br/>• **콘트롤 타이어 성능 보정(Control Correction) 스케일링 동형성 아키텍처 완비 (cf_tire.md, 	ire_curve_사전.md)**: Pacejka 비선형 Magic Formula에 보정 게인( = G_i$)을 곱하는 것이 피크 계수( \to gD$) 및 초기 강성( \to gK$) 스케일링과 완벽히 동형(Isomorphic)임을 수학적으로 증명하고, _save_raw_snapshot() 멱등성 보장 및 프로젝트 단위 일괄 보정 연동 완결<br/>• **볼트 지식 사전 허브 확장 (10_도메인_지식_사전/tire_curve_사전.md)**: 객체 아키텍처, 멤버 변수 체계(로우 데이터 vs 피팅 결과), 과도기 싱크 기준, 콘트롤 보정 전용 챕터를 집대성한 전용 사전 신설 및 curve_fit_사전.md 상호 링크 완료 | ✅ 완료 |
| **v3.60** | 2026-10-21 | uno &<br/>Gemini | 📈 **`unoUtil.curve_fit` 옵시디언 볼트 4대 보고서 지식 허브(`20_curve_fit`) 구축, `PlotterProject` 커브 피팅 & 슬립률 PDF 더블 Y축 복합 비교 플로터(`compare_curve_fit_pdf`) 신설 및 최상위 `vt_acc_brk` 17대 차트 자동 연동, `tire_curve/explain` 1파일 1그래프 공학 시각화 파이프라인(9종) 완결**<br/>• **옵시디언 볼트 `20_curve_fit` 지식 허브 및 4대 심층 보고서 구축**: `20_curve_fit` 폴더 신설 및 마스터 MOC([[00_curve_fit_보고서_통합_색인]]), 4대 보고서([[10_휠속도_시간지연_보정_및_타이어_커브피팅_종합보고서]], [[20_타이어_커브피팅_전면_개발스토리_및_공학검증보고서]], [[30_가속_시험_타이어_커브피팅_검증보고서]], [[40_NoABS_실측_VBB_타이어_커브피팅_검증보고서]]) 이관 및 36종 고해상도 차트(`_attachments/10_회사_업무/curve_fit/`) 100% 위키링크 연동 완료<br/>• **`PlotterProject.compare_curve_fit_pdf` 더블 Y축 복합 시각화 신설 및 다중 콘트롤 정규화 합성 (`plotter_project.py`, `plotter_project.md`)**: 좌측 Y축(Magic Formula 커브 피팅 곡선 + 피크 마커)과 우측 Y축(`twinx`, 실시간 주행 휠 슬립률 가우시안 확률 밀도 PDF 반투명 면적 채우기 `alpha=0.22` + 보조 점선)을 단일 X축(슬립률)에 동시 중첩 렌더링. 다중 콘트롤 타이어(C1, C2...)에 대한 곡선 평균화 및 슬립률 PDF 적분 면적 1.0 보존 정규화(NumPy 2.0+ `trapezoid` 호환) 완비로 단일 대표 객체 표현 확립<br/>• **최상위 배치 함수 `vt_acc_brk()` 및 `PlotterProject.all()` 17번째 공식 차트(`17_Curve_Fit_PDF`) 자동 연동**: `pjt.plot.all()` 및 `vt_acc_brk()` 배치 실행 시 가속 6대, 제동 10대 비교 차트로 자동 포함되어 이미지 및 엑셀 일괄 출력 파이프라인 완결 (`BMW320d_ADAC_Dry` 실측 VBB 데이터로 142KB 고해상도 차트 정상 생성 검증)<br/>• **`tire_curve/explain` 1파일 1그래프 공학 시각화 모듈 허브(9종) 구축**: `fig1_brk_onset_recovery.py` ~ `fig8_sr_dynamic_scaling_invariance.py` 및 사용자 질의 심층 분석기 `fig9_transient_landmark_deep_dive.py`($L0\to L1\to L2\to L3$ 타이밍 지터 정량화 및 4단계 과도 분리·본체 피팅 통합 가시화)를 1파일 1그래프 원칙으로 개별 모듈화하고 공통 데이터 로더(`common_data.py`), 일괄 배치 러너(`run_all.py`, 100% PASS), `README.md` 구축 완료 (볼트 보고서 4.3절 신규 수록) | ✅ 완료 |
| **v3.50** | 2026-10-20 | uno &<br/>Antigravity | 📊 **가감속/제동(`vt_acc_brk`) 및 타이어 커브(`curve_fit`) 시각화 로깅 1줄 요약(`그래프 생성 중 .... 생성 완료.`) 전면 통일, `format_fig` 일원화(`Errno 22` 해결), 커스텀 범례 덮어쓰기 버그 및 경로 조작 취약점 완결**<br/>• **플로터 1줄 요약 로깅(`One-Line Summary Law`) 전면 통일 (`plotter_tire.py`, `plotter_project.py`)**: `PlotterTire` 9대 메서드 및 `PlotterProject` 13대 `compare_*` 메서드의 시작 로그를 `DEBUG`(`그래프 생성 시작...`)로 격하하고, 완료 로그를 `self.logger.info(f"[{name}] 그래프 생성 중 .... 생성 완료.")` 1줄 요약 포맷으로 전면 통일하여 콘솔 가독성 극대화 (`PlotterTire.all()` 내 전역 `logger` 오용도 `self.logger`로 정합)<br/>• **선택적 휠 채널/서브 분석 미실행 시 로그 레벨 `WARNING` 일원화 (`plotter_project.py`, `cf_tire.py`)**: `PlotterProject`의 4대 서브 분석 비교(`compare_slip_pdf`, `compare_mudrop_dist`, `compare_slip_mode_skewness`, `compare_response`) 데이터 부재 시 `ERROR` 대신 `WARNING`을 출력하도록 교정하고, `TireCurve.fit()`에서 휠 슬립 채널 부재로 스킵 시 `[Curve_Fit] 분석에 필요한 휠 슬립 채널 데이터가 존재하지 않아 분석을 건너뜁니다.` `WARNING` 안내 신설<br/>• **`TireCurve.plot()`의 `format_fig` 위임 일원화 및 `Errno 22` 저장 충돌 원천 차단 (`cf_tire.py`)**: `format_fig` 호출 후 중복 실행되던 수동 `plt.tight_layout()` 및 `fig.savefig()` 블록을 제거하고 `format_fig`로 저장·레이아웃·메모리 해제를 100% 일원화하여 파일 뷰어 열람 중 발생하던 `[Errno 22] Invalid argument` 충돌 및 이중 저장 오버헤드 완전 해결<br/>• **커스텀 범례(`legend`) 덮어쓰기 버그 및 경로 슬라이싱 취약점 해결 (`plotter_tire.py`, `plotter_project.py`)**: `format_fig` 기본값(`legend=True`)이 다크 테마/상단 커스텀 핸들 범례를 덮어쓰던 버그를 `kwargs.setdefault('legend', False)`(`slip_mode_skewness`, `sys_response`, `compare_slip_mode_skewness`, `compare_response`)로 해결하고, `save[:-4]` 문자열 슬라이싱을 `Path` 기반 `_format_save_path` 헬퍼로 교체 및 `"Aeceleration [g]"` 오타 수정 (`plotter_tire.md`, `plotter_project.md` 1:1 매뉴얼 동기화 및 자가 검증 통과) | ✅ 완료 |
| **v3.49** | 2026-10-20 | uno &<br/>Antigravity | ⏱️ **가감속/제동(`vt_acc_brk`) 과도 응답성 분석기(`calc_response` in `func_acc_brk.py`) 유효 응답 및 Rising 구간 추출 4대 구조적 결함 해결 완결**<br/>• **저마찰(Snow/Ice 등) 임계값 비례 스케일링 및 역전 방지**: 목표 가감속도(`response_target`) 미달로 종료 임계값(`threshold_end`)이 완화될 때, 시작 임계값(`threshold_start`)도 완화 비율(`scale_ratio = threshold_end / target_limit`)에 맞추어 자동 비례 축소되도록 개선하여 시작점-종료점 임계값 역전 및 탈락 원천 해결<br/>• **`pre_sec` 구간 기저선(Baseline) 클리핑 정상화**: `pre_sec` 맨 앞의 첫 노이즈(`index[0]`)를 잘라내던 기존 오류를 수정하여, 유효 세션 시작점(`df_group.index[0]`) 직전의 마지막 영점/기저선(`index[-1]`) 이후부터 탐색하도록 정합하고 기저선 미교차 시 극값 폴백(`idxmax`/`idxmin`) 방어선 탑재<br/>• **단일 불량 차수로 인한 전체 조기 종료(`return dict_result`) 버그 수정**: 다중 차수(`EffNum`)·휠 채널 반복 루프 중 특정 1개 차수가 임계치 미달이더라도 전체 결과를 초기화하며 종료하지 않고 해당 차수만 `continue`로 스킵하여 정상 차수들의 분석 결과를 온전히 보존<br/>• **초기 Rising 구간 탐색 시 전역 노이즈 피크 오탐 방지**: 2차 미분(`d2_vel`) 극값 탐색 범위를 전체 주행 구간이 아닌 초기 과도 응답 구간(`idx_diff_vel_start` ~ `idx_diff_vel_end + 1.5s`)으로 한정하여 ABS 중후반부나 정지 직전 피칭 노이즈에 의한 Rising 구간 오탐 원천 차단 (`func_acc_brk.md` 1:1 매뉴얼 동기화 및 검증 완료) | ✅ 완료 |
| **v3.48** | 2026-10-19 | uno &<br/>Antigravity | 🎯 **가감속/제동(`vt_acc_brk`) 7번째 공식 서브 분석기로서의 `curve_fit`(`TireCurve` v4.5) 전면 통합, `fit`/`predict` 분리, 구동방식(`TestVehicleLayout`) 기반 슬립 축 자동 선택, 프로젝트 콘트롤 보정 게인($G_i$) 동기화, 다중 타이어 비교 플로터(`compare_curve_fit`) 및 대표 래퍼(`vt_acc_brk`)·7대 1:1 매뉴얼 완결**<br/>• **`VTAccBrkTire.curve_fit` 서브 분석기 공식 통합 및 `fit()` vs `predict()` 책임 분리 (`cf_tire.py` v4.5, `vt_acc_brk_tire.py`)**: `VTAccBrkTire.run()` 실행 시 7번째 서브 분석기로 `self.curve_fit = TireCurve(self, ...)`을 자동 기동하여 요약(`summary.df`)에 `cf_B`~`cf_Sv`, `cf_peak_mu`, `cf_peak_slip`, `cf_stiffness`, `cf_r_squared`, `cf_rmse`, `cf_method`를 자동 산출. `fit()`은 6대 최적화 메서드(`'robust'`, `'binning'`, `'two_stage'`, `'ransac'`, `'lsq'`, `'custom'`)로 인자를 추정하고, `predict(x=None, interval=0.005)`는 기본 $[0.0, 1.0]$ 구간 또는 사용자 지정 구간(`[start, end]`)·배열(`np.ndarray`)에 대한 예측 곡선(`df[['Slip', 'Acc']]`)을 생성하도록 정립 (`BaseMemory` 호환 `clear_cache`/`restore_cache` 내장)<br/>• **휠스피드 부재 시 자동 Skip 및 시험 모드(`brk`/`acc`)·차량 구동방식(`TestVehicleLayout`) 연동 슬립 축 자동 결정**: 원시 데이터에 휠스피드/슬립 채널이 없으면 에러 없이 자동 Skip(`is_fitted = False`)하고, 제동(`brk`)은 전륜축(`FL`/`FR` 중 유효 채널 평균)을 기본 적용하되 가속(`acc`)은 `tire.infor.result` 내 `TestVehicleLayout`이 `RWD`/`FR`/`MR`/`RR`이면 후륜축(`RL`/`RR`), `AWD`/`4WD`이면 4륜 전체(`all`), `FWD`/미지정 시 전륜축(`front`)을 자동 선택 (`col_curve_fit_wheelslip` 명시 지정 시 최우선 오버라이드)<br/>• **프로젝트 콘트롤 타이어 보정(`Correct.run`) 동기화 및 요약 지표(`corr_cf_*`, `index_cf_*`) 산출 (`correct.py`, `vt_acc_brk_project.py`)**: 별도 재피팅 없이 콘트롤 타이어 선형 보간 게인($G_i = \text{corr\_Acc} / \text{mean\_Acc}$)을 각 타이어의 `curve_fit.df`(`corr_mean_Acc`, `corr_curve_Acc`), `df_raw`, `params`(`corr_D`, `corr_peak_mu`, `corr_stiffness`)에 동기화하고, 프로젝트 요약표에 `corr_cf_peak_mu`, `index_cf_peak_mu`, `corr_cf_stiffness`, `index_cf_stiffness`, `corr_cf_D`를 자동 산출<br/>• **단일 타이어(`PlotterTire`)·프로젝트(`PlotterProject`) 시각화 및 최상위 래퍼(`vt_acc_brk`) 연동**: `tire.plot.curve_fit(detail=False)`, `tire.plot.curve_fit_detail()` (6-패널 진단), `project.plot.compare_curve_fit(corr='mean', xlim=(0.0, 1.0), show_peak=True)` 신설 및 `vt_acc_brk()` 대표 함수에 `col_curve_fit_wheelslip`, `cf_method`, `cf_vel_range`, `cf_slip_range`, `cf_refine_start`, `cf_filter_transient` 3계층 분기 패스스루 완성<br/>• **7대 모듈 Docstring 및 1:1 기술 매뉴얼(`cf_tire.md` v4.5, `vt_acc_brk*.md`, `correct.md`, `plotter_*.md`), 도메인 사전([[vt_acc_brk_사전]], [[curve_fit_사전]]) 및 영구 지식 위키([[30_실차_가감속_성능변화_분석_및_보정_시스템]]) 전수 동기화 완료** | ✅ 완료 |
| **v3.47** | 2026-10-19 | uno &<br/>Antigravity | ❄️ **스노우 노면·기상 환경 보정(`snow_condition`) 다중 스케일(`StandardScaler`) 자동 정규화 파이프라인(`correction_model.py`), 기상/노면 인자별 동적 축 범위·눈금·레이아웃 플로터(`correction_plotter.py`) 고도화 및 최신 DB 동기화 실증 완결**<br/>• **다중 스케일 피처 자동 정규화 파이프라인 구축 (`SnowCorrectionModel.train_models`)**: 기온($\Delta T \in [-10, +13]^\circ\text{C}$, $\sigma \approx 4.9$) 및 상대습도($\Delta RH \in [-15, +9]\%$, $\sigma \approx 4.9$) 등 입력 인자 간 물리적 단위 스케일이 큰 조합($\max(\sigma_X) > 2.5$)이 감지되면, 거리/커널 기반 모델인 `KNN Regressor`와 `SVR`에 `make_pipeline(StandardScaler(), ...)`을 자동 결합하고 `SVR` 무차원 유효 대역폭($\gamma_{\text{eff}} = 0.07 \times 1.28^2 \approx 0.1147$)을 주입하여 등고선 말림과 축 왜곡을 원천 차단 (기존 `[char_height, cd_test_ah]` 조합은 $\max(\sigma_X) \approx 1.54 \le 2.5$로 원시 스케일 100% 보존)<br/>• **기상/노면 인자별 동적 등고선 축 스케일링 및 타이틀 간섭 해소 (`SnowCorrectionPlotter`)**: `correction_map` 및 `correction_map_comparison(x_range=None, y_range=None)`에서 선택된 인자(`char_height`, `cd_test_ah`, `cd_test_temp`, `cd_test_hum`)의 실제 차분 분포와 인자별 전용 여백(Margin)·눈금 간격(Step)·한글 물리 단위 라벨을 자동 적용하고, 우측 공통 컬러바와 서브플롯 타이틀 간 겹침을 원천 차단<br/>• **VBO 날짜 교정 최신 DB(`3-1. df_combine_brk_surface_spec.pkl`) 기반 3종 보정 모델 전수 실증**: `Case 1 [눌림량+절대습도]` (`VIF = 1.07`, `RF` 제동거리 `0.516 m` / 지수 `2.887 %p`), `Case 2 [기온+절대습도]` (Sonntag 방정식 열역학 다중공선성 `VIF = 16.89` 규명), `Case 3 [기온+상대습도]` (`VIF = 2.53`, `RF` 제동거리 `0.495 m` [+43.6%] / 지수 `2.732 %p` [+20.6%]) 통합 비교 완결<br/>• **1:1 코드 매뉴얼(`correction_model.md`, `correction_plotter.md`), 도메인 지식 사전([[snow_condition_사전]]) 및 스노우 공학 영구 지식 위키([[31_스노우_노면_디지털트윈_및_제동성능_보정_위키]]) 동기화 완료** | ✅ 완료 |
| **v3.46** | 2026-10-19 | uno &<br/>Antigravity | 🎯 **제동(`BRK`) 초기 과도 응답 4-랜드마크(`L0→L1→L2→L3`) 위상 정합(`calc_brk_transient_landmarks`), 2대 물리 지표($K_{\text{pk}}$ & $d\mu/dt$) 산출, 초기 과도 루프(`L0~L3`) 전체 분리 후 정상 상태(`L3~`) 본체 피팅(`filter_transient=True`), 고슬립 표본 밀도 역가중치·스노우 웻지(`enable_wedge=True`) 결합, 제외 로우 데이터(`✕`/`△`)·포함/제외 비교 시각화(`compare_unfiltered=True`) 및 VBO 날짜 파싱 3중 안전망(`datetime_helper.py`) 완결**<br/>• **제동 초기 과도 응답 4-랜드마크 위상 정합 및 2대 물리 지표 산출 (`calc_brk_transient_landmarks`)**: `unoUtil.signal_process.post_process.filters.moving_average_fast` 및 `get_col_slip`을 활용하여 회차별 `L0`(제동 시작점), `L1`(관성 불감대 종료 변곡점, $\mu \ge 0.035\text{g}$, 평균 $\Delta t_{L1} \approx 50\sim 80\,\text{ms}$), `L2`(1차 최대 마찰 피크), `L3`(1차 ABS 감압 골짜기)를 자동 검출하고 무차원 위상($s \in [0, 3]$)으로 동기화하여 대표 초기 루프를 복원. 슬립 축 유효 초기 강성인 **피크-코드 강성($K_{\text{pk}} = \mu_{L2}/\kappa_{L2}$)** 과 휠속도 노이즈에 무관한 **시간축 마찰 빌드업 속도($d\mu/dt = \Delta\mu_{10\to 90\%}/\Delta t$)** 를 동시 산출하여 타이어 초기 응답성 정량화<br/>• **초기 과도 루프(`L0~L3`) 전체 분리 후 정상 상태(`L3~`) 본체 피팅 (`filter_deadzone=True`, `filter_transient=True`)**: 초반 기울기($K_{x0}$) 추출에 사용된 `L0~L1` 관성 데드존(`self.deadzone_data`)과 `L1~L3` 1차 과도 스파이크(`self.transient_data`)가 저슬립 상단에 이질적 군집을 형성하여 본체 피팅을 왜곡하는 현상을 원천 해결하기 위해, `L0~L3` 전체를 본체 피팅에서 제외하고 `L3` 이후 정상 상태 제동 데이터만으로 피팅하도록 이원화 $\to$ `Snow_ACC_BRK` 4대 세트 전원에서 **피팅 오차(RMSE) $18.5\% \sim 23.7\%$ 대폭 감소** (C1: $0.0651\to 0.0522$, T1: $0.0715\to 0.0555$, T2: $0.0739\to 0.0564$, C2: $0.0729\to 0.0594$) 및 T2 고슬립 포화 마찰 추종성($0.404\text{g} \to 0.420\text{g}$) 완벽 복원<br/>• **고슬립($\kappa > 0.25$) 이격 해소: 구간 밀도 역가중치(`calc_bin_density_weights`) 및 스노우 웻지(`enable_wedge=True`) 결합**: ABS 제어 대역 편중($85\%$ 이상이 $\kappa < 0.25$)을 슬립 구간별 역제곱근 가중치($w_i \propto N_b^{-0.65}$)로 균등화하고, 고슬립 눈 쐐기(Snow Wedge) 선형 재상승 항($+W_{\text{snow}}\cdot\max(0, \kappa-\kappa_{\text{valley}})$)을 결합하여 고슬립 하향 이격(Gap) 완전 해소<br/>• **제외 로우 데이터 마커 분리 표시 및 초기 과도 포함 vs 제외 동시 비교 시각화 (`compare_unfiltered=True`)**: `TireCurve.plot()` 및 `plot_tire_set_curve_comparison()`에서 정상 피팅 데이터(차속 컬러맵 `●`)와 별도로 제외 데이터 ① 관성 데드존(`L0~L1`, 빨간색 `✕`) 및 제외 데이터 ② 초반 과도 스파이크(`L1~L3`, 주황색 `△`)를 분리 표시하고, 초기 과도 포함 Fit(보라색 파선 `--`)과 초기 과도 제외 최종 Fit(빨간색 실선 `—`)을 동시 오버레이 비교 (`04_BRK_TRANSIENT_INCLUDED_VS_EXCLUDED_COMPARISON.png` 등 생성 완료)<br/>• **VBO 날짜 파싱 3중 안전망(`datetime_helper.py`) 및 `CombinerEstimator` v4.1 정합**: ① 2-1단계 동계 시험 도메인 게이트(`snow`/`winter`/`핀란드`/`utac` 경로 감지 시 겨울철 11~4월 우선, 여름철 5~10월 배제), ② 2-2단계 장비 시그니처(`VBox Touch` $\to$ 미국식 `MM/DD`, `[SessionData]`/`Exported` $\to$ 유럽식 `DD/MM`), ③ 6단계 `mtime` 근접도 30일 이내 제한으로 17개 스노우 세션 날짜 불일치 100% 해결. `CombinerEstimator` 저슬립(`0~0.20`) 가중치(`wg=20`)·`TrendLine` 양수 기울기 클램핑(`[0.5, 25.0]`)·원점 `(0, 0)` 직선 보정 완성<br/>• **1:1 코드 매뉴얼(`cf_tire.md` v4.4, `combiner_estimator.md` v4.1, `magic_formula.md`, `datetime_helper.md` v3.46), 도메인 지식 사전(`curve_fit_사전.md`, `file_reader_사전.md`, `models_사전.md`) 및 제동 영구 지식 위키([[31_실차_제동_시작점_자동_탐지_및_과도응답_슬립_복원_공학]]) 동기화 완료** | ✅ 완료 |
| **v3.45** | 2026-10-19 | uno &<br/>Antigravity | 🎯 **`TireCurve` 해법 C(2단계 강성 구속 단일 MF: `constrained_mf`) 공식 엔진 편입, 사용자 제안 2D 분포 분할 시그모이드 블렌딩(해법 A-v2: `split_blend`) 정식 구현 및 가속(`Snow_ACC_BRK`)·제동(`Snow_BRK_ABS`) 11종 전 케이스 원클릭 통합 리포팅 파이프라인 완결**<br/>• **해법 C (`method="constrained_mf"`) 공식 엔진 탑재 (`cf_tire.py`, `magic_formula.py`)**: 1단계로 저슬립 탄성 영역($0 \le x \le 0.035$)에서 원점 구속 RANSAC(`calc_initial_stiffness`)으로 초기 탄성 강성 $K = \frac{dy}{dx}\big|_{x=0}$를 확정하고, 2단계로 등식 제약 $B = \frac{K}{C \cdot D}$가 주입된 3파라미터 매직포뮬러(`constrained_magic_formula`)를 최적화하여 원점 정합 및 데이터 정중앙 관통을 보장하는 단일 해석 수식 엔진 완성<br/>• **사용자 제안 해법 A-v2 (`method="split_blend"`) 구현 및 전이부 Hump 원천 차단**: 1D 히스토그램 KDE 밀도 능선에서 제어 클러스터 진입 변곡점($x_{\text{kde\_onset}}$)을 포착하여 고슬립 클러스터($x \ge x_{\text{kde\_onset}}$) 데이터만으로 순수 4파라미터 MF($y_{\text{MF\_high}}$)를 독립 피팅한 뒤, 저슬립 직선($y = K \cdot x$)과의 실제 교차점($x_{\text{trans}}$)에서 시그모이드 가중치로 블렌딩함으로써 구형 해법 A의 전이부 상단 불룩함(Hump) 현상을 100% 제거 (`00_TIRE_CURVE_APPROACHES_C_VS_AV2.png` 4분할 정밀 대조 실증)<br/>• **극저속 휠스핀 노이즈 스마트 컷오프 및 단일 런 폴백 방어선 구축**: `TireCurve._extract_data_from_tire()`에 가속 시험 $V \ge 8.0\text{km/h}$, 제동 시험 $V \ge 3.0\text{km/h}$ 및 $0 < x \le 1.0$ 기본 필터링을 적용하여 출발 직후 분모 $V \to 0$에 의한 슬립 폭주 노이즈를 원천 차단하고, 단일 런 아웃라이어 판정 시 전체 검출 런으로 안전 폴백하는 방어 로직 탑재<br/>• **가속(`Snow_ACC_BRK` 8종) 및 제동(`Snow_BRK_ABS` 3종) 전 케이스 원클릭 리포팅 완결 (`example_acc_brk_start_points.py`)**: 전 11개 케이스에 대해 4대 모델(`constrained_mf`, `split_blend`, `combiner`, `least_squares`) 동시 피팅 검증, 세트별 통합 비교 차트(`curve_fit_comparison_Snow_ACC_5-40_AllSets.png`, `curve_fit_comparison_Snow_BRK_40-5_AllSets.png`) 및 정량 요약 CSV(`tire_curve_11cases_summary.csv`) 생성 완료 (Exit Code 0)<br/>• **1:1 코드 매뉴얼(`cf_tire.md` v4.2) 및 도메인 지식 사전(`curve_fit_사전.md`) 동기화 완료** | ✅ 완료 |
| **v3.44** | 2026-10-19 | uno &<br/>Gemini | 🎯 **`curve_fit` 실차 데이터(제어 몰림 및 초기 급경사) MF 한계 극복 3대 대안(가중 블렌딩, 격자 빈 대표값, 2단계 강성구속 MF) 실증 비교, v1 원본(2025-12-01 커밋) 성공 커브 발굴 대조, 해법 C(2단계 강성구속 MF) 다각도 전수 검증 및 사용자 제안 2D 분포 분할(A 고도화) 아키텍처 정립 (안티그래비티 앱 연계 완결)**<br/>• **3대 대안 수치 비교 실증**: Baseline($K=0.62$, 강성 붕괴) vs 해법 A($K=4.84$, $\mu=0.181$, RMSE 0.0248) vs 해법 B($K=0.59$, 중앙값 상향 왜곡) vs 해법 C($K=4.70$, $\mu=0.176$, RMSE 0.0252)<br/>• **사용자 핵심 피드백 및 물리적 원인 규명**: 해법 A가 전이부($x \approx 0.04\sim 0.08$)에서 데이터 구름 상단을 스치며 위로 불룩해지는(Hump) 현상 규명(초반 0.13g 붕 뜬 Baseline MF 블렌딩 오염), 비닝 미디언(해법 B)이 저슬립 희소성으로 인해 중앙값이 0.14g로 과대평가되는 왜곡 규명, 해법 C가 원점 $(0, 0)$에서 시작하여 데이터 구름 정중앙을 가장 이상적으로 관통함을 확인<br/>• **v1 오리지널 성공 커브(2025-12-01 커밋 8cd7d5b) 발굴 대조**: 과거 성공 커브(`None-7. Curvefit.png`, `None-5. HermiteConnector.png`)의 실체가 횡력 슬립각 데이터(`ID-X55-P33-JF0_raw_raw.pkl`, $K \approx 20.9$, $\mu=0.82g$)였음을 전수 확인하고 거동 비교 기준선 확립<br/>• **해법 C 다각도 전수 검증 완결**: ① 과거 레거시 2종(SDF 횡력 $K=20.88$, VBO 가속 $K=2.03$), ② 실측 스노우 가속 4대 세트(C1: $K=4.57, \mu=0.178g$ / T1: $K=5.32, \mu=0.175g$ / T2: $K=5.64, \mu=0.167g$ / C2: $K=5.72, \mu=0.184g$ 성능 분별력 완벽 확보), ③ 차속 컷오프(4~12km/h) 전 대역 피팅 곡선 단일화 완벽 수렴 실증<br/>• **사용자 제안 2D 분포 분할(해법 A 고도화) 설계**: 2D 데이터 밀도 능선에서 직선-곡선 전이점($x_{\text{trans}}$)을 포착하여 저슬립 직선부와 순수 곡선부 MF를 분리 피팅 후 결합하는 무결점 아키텍처 정립<br/>• 🚩 **안티그래비티 앱 바통 터치 과제 (TODO)**: ① 해법 C의 $B \cdot C \cdot D = K$ 등식 제약 단일 MF 엔진을 `TireCurve` 공식 옵션으로 정식 탑재, ② 사용자 제안 2D 밀도 분기 기반 직선/곡선 분할 블렌딩(해법 A-v2) 프로토타입 구현 및 해법 C와의 1:1 최종 대조 | ✅ 완료 |
> | **v3.43** | 2026-10-18<br/>(야간) | uno &<br/>Gemini | 🎯 **`curve_fit` & `CombinerEstimator` 정밀 결함 추적, v1 오리지널 정통 2D 국소 에르미트 탐색 메커니즘 규명, 직선 쉬프트 버그 해소 및 차속 컷오프(4~12km/h) 5x5 매트릭스 진단 파이프라인 완성 (내일 작업 연계 쟁점 정립)**<br/>• **가속 시험 초반 휠스핀 노이즈($V < 6\text{km/h}$)와 차속 컷오프($V \ge 8\text{km/h}$) 효과 실증**: 슬립율 $0 \sim 278\%$ 폭주 및 분모 $V$ 극소 왜곡을 걷어내는 속도별($2 \sim 20\text{km/h}$) 10단계 피팅 비교 완료. $V \ge 8 \sim 10\text{km/h}$에서 타이어 형상이 가장 이상적으로 정돈됨을 입증<br/>• **v1 오리지널 레거시(`master` 브랜치: `unoUtil/curveFit/CurveCombiner/`) 전수 정밀 대조 분석**: 단위 체계(슬립율 $0 \sim 1.0$, 가속도 $[g]$ $\approx \mu$)가 최초 설계부터 SSOT였음을 주석과 코드로 100% 확인. 종방향 가속도 $Ax$에서 `d2y_nor`의 최저점이 원점에 위치하여 `ind_end_line == 0`으로 조기 탈출하던 v1의 숨은 결함을 규명하고 물리적 하한선($x \ge 0.015$)으로 방어. `clothoid_val = 0.03`의 본래 역할이 에르미트 품질 불량 시의 비상 대피소였으며, 직선 끝점 좌우 국소 구간($\Delta x \approx 0.015 \sim 0.035$)에서 2D 탐색 시 `score < 0.03`으로 에르미트가 본래 100% 정상 채택되었음을 수학적으로 증명<br/>• **직선 쉬프트(Left Shift) 버그 완벽 규명 및 RANSAC `model_line.predict(...)` 직접 적용**: 원점 $(0, 0)$을 강제하려 절편 $c$를 누락하여 발생했던 직선의 좌측 쉬프트를 RANSAC 모델 직접 적용으로 100% 해소하여 3열과 4/5열 직선을 완전 일치시킴<br/>• **에르미트 솟구침($y = 1.958\text{g}$) 원인 규명 및 Fritsch-Carlson 단조성 가드 탑재**: 브릿지가 피크점까지 길어져($\Delta x = 0.36$) $\Delta x \cdot m_0 \approx 5.4$로 폭발하던 Runge 현상을 천이 대역($x \le 0.075$) 캡핑 및 Fritsch-Carlson PCHIP 단조성 제약(기울기 $\le 2.5 \times \Delta y / \Delta x$)으로 원천 차단하여 실제 데이터($0.22\text{g}$) 스케일 안착<br/>• **v2 최신 표준 모듈 체계(SSOT) 준수**: 구형 레거시 명칭을 전면 배제하고 `LeastSquaresEstimator`, `scale_data`, `format_fig`, `LOGGER`로 일원화<br/>• **5x5 매트릭스 진단 차트(`00_COMBINER_STEPS_BY_SPEED_MATRIX_V2_OFFICIAL.png`) 및 11개 전 케이스 종합 비교 차트 갱신 완결**<br/>• 🚩 **내일(출근 후) 집중 검토 및 이어갈 잔여 쟁점 (TODO)**: ① "아직도 이상해": 현재 최종 곡선과 로우 데이터의 결합 부위가 사용자의 시각적/동역학적 기대치와 여전히 미세하게 불일치하는 지점 정밀 청취 (직선 구간의 시작점을 원점 0에서 시작하게 할지, RANSAC의 실제 영점 교차점 $x \approx 0.008$에서 시작하게 할지 등), ② 저슬립 영역의 가속도 데이터가 0 근처에 머무는 구동계 토크 지연 구간과 순수 타이어 탄성 강성 직선 간의 물리적 정합 기준선 확립, ③ 제동(`Snow_BRK_ABS`)과 가속(`Snow_ACC_BRK`)의 상호 간섭 없는 단일 파이프라인 최종 점검 | ✅ 완료 |
| **v3.42** | 2026-10-18 | uno &<br/>Gemini | 🎯 **`curve_fit` & `acc_brk` 가감속 시작점(Onset) 도함수(Jerk) 융합 정밀화, 0 근처 평형 기저선 노면 떨림 밴드(`ax_smooth <= base_mean + 2*std`) 및 앞뒤 양방향(Bidirectional) Onset 탐색 구축, 시작점 가속도($Ax_{onset}$) 기반 이상치 판정 전면 전환, 콤바이너(Combiner) 초기 선형 강성 직선 복원 및 차속 컬러바 탑재 타이어 세트별 듀얼 모델(Combiner vs LeastSquares) 통합 비교 시각화 완결**<br/>• **타행 감속(Coasting/엔진 브레이크: $-0.02 \sim -0.04\text{g}$) 및 제동 전 가속 기저선 오염 원천 해결**: 제동 전 엑셀 가속 구간($A_x > +0.03\text{g}$)을 기저선 탐색에서 원천 배제하여, 반드시 $A_x \le 0.01\text{g}$ (0 근처 평형 대역)에서 평균(`base_mean`)과 노면 떨림 폭(`safe_std`)을 산출하도록 물리 가드 구축. 가속도가 줄어드는 1차 하강(엑셀 오프)은 무시하고, 유압 브레이크 인가로 급강하하는 Min Jerk 피크($-4.5 \sim -5.0\,\text{g/s}$)에서 역추적하여 평형 떨림 밴드($A_x \le \text{base\_mean} + 2\sigma$)로 진입하는 변곡점 Onset을 정밀 포착<br/>• **앞뒤 양방향(Bidirectional Window) 제동 Onset 탐색 구축**: 운전자가 목표 속도(예: 20kph)에 도달하기 전뿐만 아니라 도달한 직후(미래 0.8초)에 브레이크를 밟은 케이스(`NoABS_20_30_반복.VBB` 등)까지 완벽 포괄하도록 앞뒤 양방향 윈도우 탐색을 적용하여, 평형 구간 한가운데가 엉뚱하게 시작점으로 잡히던 결함을 100% 박멸<br/>• **시작점 순간 가속도($Ax_{onset}$) 기준 아웃라이어 판정 전면 전환**: 운전자의 진입 타이밍에 종속되던 $\Delta t$(시간차) 기준을 완전 폐기하고, 시작점 당시의 가속도가 0 근처 평형 상태($-0.09\text{g} \le Ax_{onset} \le +0.025\text{g}$) 및 그룹 IQR 범위 내에 있는지를 기준으로 불량 런을 칼같이 자동 선별하도록 개편<br/>• **콤바이너(Combiner) 초기 선형 구간(직선) 복원 및 원점 보정**: `ind_end_line == 0` 조기 탈출 버그를 제거하고, 저슬립 대역(0~2%)에서 `LineMaker`가 강건 회귀(RANSAC/ODR) 직선을 항상 추출한 뒤 `Hermite`/`Clothoid`로 접합하고 원점($x=0, y=0$) 연결 직선 보정을 거치도록 파이프라인을 완전 복원<br/>• **타이어 객체(`VTAccBrkTire`) ➔ 추정기(`TireCurve`) 직결 및 전용 `StartPointResult` 객체 구축**: `tire.curve_fit = TireCurve(tire=tire, method="combiner")`로 서브 분석기 패턴 직결. `fit()` 단 1회 호출로 [시작점 복원 ➔ $Ax_{onset}$ 이상치 필터링 ➔ 커브 피팅(기본 Combiner)] 원스톱 자동 완결. `tire.curve_fit.start_point`에 상세표(`.df`), 통계(`.summary`), 아웃라이어(`.outliers`), 줌인 차트(`.plot()`) 캡슐화<br/>• **차속 그라데이션 컬러 매핑(`hue="speed"`) 및 세트별 듀얼 모델(Combiner vs LeastSquares) 통합 비교 시각화 신설**: 로우 데이터에 주행 차속별 그라데이션 컬러 및 컬러바(`시험 차속 (제동: 40→5, 가속: 5→40) [km/h]`) 제공. 신설된 `plot_tire_set_curve_comparison`을 통해 한 피규어에 4개 타이어 세트(C1, T1, T2, C2)의 개별 듀얼 피팅과 전체 세트 오버레이 비교를 6분할로 조망하는 마스터 비교 차트 생성 완료<br/>• **11종 실제 VBB 데이터셋 일괄 재검증 및 차트 갱신 완료**: `Snow_ACC_BRK` 4종(8케이스) 및 `Snow_BRK_ABS` 3종 전체에 대한 파이프라인 무결성 검증 완료 | ✅ 완료 |
| **v3.41** | 2026-10-18 | uno &<br/>Gemini | 🛰️ **`file_reader` VBO 계측 파일 날짜 파싱 모호성(DD/MM vs MM/DD) 7단계 지능형 판정 파이프라인(`_resolve_ambiguous_header_date`) 구축, 미래 날짜 배제(Future Date Gate) 절대 물리 법칙 탑재 및 12시간제(AM/PM) 파싱 완결**<br/>• **VBO 헤더 유럽식(DD/MM) vs 미국식(MM/DD) 파싱 왜곡 원천 해결**: VBOX 계측기 펌웨어 및 로케일에 따라 `01/06/2026`(1월 6일)이 6월 1일로 오판되던 결함을 숫자 범위 판정(`> 12`), 절대 물리 법칙(파일 시스템 `mtime` 및 오늘 날짜 대비 미래 날짜 배제), 파일명 크로스체크, 형제 파일(Sibling `.vbo`) 포맷 학습, 디렉터리 연/월 토큰 매칭, `mtime` 시간차 최소화, 영국 Racelogic 기본 폴백의 **7단계 스마트 판정 파이프라인**으로 100% 무결하게 해결<br/>• **미래 날짜 배제 절대 물리 법칙 (Future Date Gate) 탑재**: 계측 일시는 파일 시스템 생성/수정 일시(`mtime`) 또는 오늘보다 미래일 수 없다는 대원칙에 따라, 한 후보가 미래 날짜인 경우 유효한 과거 날짜로 즉시 일/월 자동 스왑 확정<br/>• **VBOParser 헤더 스캔 확장 및 12시간제 AM/PM 파싱 지원**: `_extract_save_date`에서 `lines[:120]`까지 스캔 범위를 넓혀 `[SessionData]` 보조 날짜(`Date:`, `Append:`) 크로스체크를 지원하고, `at 01:28:28 PM` 형식의 12시간제 표기를 24시간제(`13:28:28`)로 완벽 변환<br/>• **1:1 기술 매뉴얼(`datetime_helper.md`) 및 8대 엣지 케이스 자가 검증 스위트 완비**: 7단계 판정 파이프라인 아키텍처 다이어그램 및 시나리오 5 예제 코드 반영, `datetime_helper.py` 내 8대 엣지 케이스 단위 테스트 및 실제 `ExampleBrakeStop.vbo` 실측 계측 파이프라인(Shape 8582, 44채널) 연동 100% 무결성 통과 (Exit Code 0) | ✅ 완료 |
> | **v3.40** | 2026-10-18 | uno &<br/>Gemini | 📖 **unoUtil 12대 전 도메인 지식 사전(`[모듈명]_사전.md`) 신설, 템플릿 표준(`_System/Templates/`) 확립, 글로벌 룰북(`PYTHON_CODE_AGENT.md`) 및 감사 스킬 개정 완결**<br/>• **12대 핵심 도메인 지식 사전 구축 완결**: `snow_condition`, `vt_acc_brk`, `curve_fit`, `file_reader`, `signal_process`, `graphics`, `models`, `uncertainty`, `logger`, `gps`, `database`, `ai` 총 12개 전 도메인에 대해 5대 표준 섹션(설계 철학, 배경 이론, 아키텍처 다이어그램, 실전 워크플로우, 트러블슈팅)을 갖춘 `[모듈명]_사전.md` 신설 완료<br/>• **지식의 원자화(Knowledge Atomization) 및 영구 위키(04_Resources) 100% 연계**: 각 모듈 사전에 파편화된 이론을 방치하지 않고, `04_Resources` 내 25개 이상의 공학/물리/수학/아키텍처 영구 지식 노트로 상호 연결망 확립<br/>• **공식 템플릿(`💻 unoUtil_모듈_사전_템플릿.md`) 및 글로벌 거버넌스 헌장 집행**: 코드 매뉴얼 격리 보존 원칙(1:1 소스 매뉴얼)을 유지하면서도 볼트 내 도메인 지식 사전을 의무화하는 법률 제정 및 `code-audit-obsidian-docs` 스킬 동기화 완료 | ✅ 완료 |
> | **v3.39** | 2026-10-17 | uno &<br/>Gemini | 🎯 **`curve_fit` 차세대 3계층 메타 아키텍처(데이터/모델 주입 분리) 전면 재구조화, 3대 추정기(`LeastSquares`, `Optimize`, `Combiner`) 공통 프로토콜 정립, 단일 기준 불변 원칙(Single Baseline) 철저 집행 및 실차 제동 `find_brake_start_point` 완성**<br/>• **"데이터(x, y)와 모델 주입" 기반 3계층 아키텍처 확립**: 타이어 도메인(`tire_curve`)에 종속되어 있던 피팅 엔진들을 순수 수학적 범용 추정기 계층(`unoUtil.curve_fit.estimators`)으로 전면 승격 분리하고, 타이어 공학 지식(원점 구속, 초기 강성 $B \cdot C \cdot D$)을 담은 도메인 래퍼(`cf_tire.py`)와 완벽 분리<br/>• **Base Estimator Protocol (모든 추정기 규격 통일)**: `LeastSquaresEstimator`, `OptimizeEstimator`, `CombinerEstimator` 전원에 대해 `__init__(model_func)`, `.fit(x, y)`, `.predict(x)`, `self.rmse`(평균 제곱근 오차 필수 내장), `.plot(save, close=False)`, `is_fitted` 및 실측 데이터 연동 `__main__` 자가 검증 스위트 100% 장착<br/>• **`CombinerEstimator` 의존성 주입 혁신 및 연산 속도 극대화**: 내부의 `EstimatorMF` 하드코딩을 전면 제거하고, 주입받은 모델로 초기 선형(가중치)과 후반 곡선(가중치)을 분할 최적화하여 새로운 합성 회귀 모델(`Predictor`)을 도출하도록 재설계. 에르미트 접합 2D 탐색 다운샘플링으로 연산 속도를 5분$\to$**0.05초**로 비약적 단축 및 `__iter__` 튜플 언패킹 100% 무중단 호환 보존<br/>• **과도기적 레거시 및 별칭 전수 숙청 (Single Baseline Law 철저 준수)**: `fit_magic_formula`, `EstimatorMF`, `estimatorMF`, `EstimatorLeastSquares`, `MinimizeEstimator`, `FitMinimizeOptimization`, `CurveCombiner` 등 군더더기 별칭/래퍼를 전면 삭제하고 4대 공식 표준 클래스(`TireCurve`, `LeastSquaresEstimator`, `OptimizeEstimator`, `CombinerEstimator`)로 export 단일화 (`hndl_test.py` 등 호출부 전수 갱신)<br/>• **실차 제동 브레이크 시작점 자동 탐지 함수 신규 구축 (`find_brake_start_point`)**: `unoUtil.vehicle.acc_brk.func_acc_brk`에 3중 노이즈 방어(1차 11샘플 평활화 + 정속 1초 기저선 통계 추정 + 5샘플 연속 지속성 검증) 기반 브레이크 시작점 탐색 함수 구현 $\to$ 50km/h 고정 컷으로 잘려나가던 감속도 $0 \to 0.45\text{g}$ 및 슬립율 램프업 구간을 자동 역추적 복원하여 음수 슬립 외삽 클램핑 수평선 결함 원천 해결<br/>• **1:1 기술 매뉴얼 완비 및 실측 데이터 검증 보고서 배포**: `cf_tire.md`, `least_squares_estimator.md`, `optimize_estimator.md`(신규), `combiner_estimator.md`, `func_acc_brk.md` 1:1 매뉴얼 완비 (Code Manual Isolation Law 준수) 및 실측 VBB 데이터 기반 `TIRE_CURVE_FITTING_RESULT.md` 및 `fig/` 고해상도 차트 4종 생성 완료 | ✅ 완료 |
| **v3.38** | 2026-10-16 | uno &<br/>Gemini | 🏛️ **가감속/제동(`vt_acc_brk`) 설정 가이드(`vt_acc_brk_config_guide.md`)의 `vt_acc_brk.md` 제3대단원 완전 통합 및 파이썬 모듈 1:1 SSOT 매뉴얼 체계 확립 완결**<br/>• **입력 설정 가이드 대단원 신설 및 완전 흡수 (`vt_acc_brk.md`)**: 기존에 별도 분리되어 관리되던 `vt_acc_brk_config_guide.md`의 핵심 내용(3계층 분기 깔때기 아키텍처 다이어그램, 4대 파라미터 입력 형태 규격, 전체 파라미터 상세 명세 및 스마트 디폴트 매트릭스, 물리 부호 자동 정규화 메커니즘, 다중 속도 및 아웃라이어 실전 레시피)을 `vt_acc_brk.md`의 `## 🎛️ 3. 계층형 파라미터 입력 체계 및 스마트 설정 종합 가이드 (Config Guide)`로 온전히 통합<br/>• **중복 파일 삭제 및 코드 매뉴얼 격리 보존 원칙(Code Manual Isolation Law) 정합**: 파이썬 패키지 내부의 파편화된 `vt_acc_brk_config_guide.md`를 영구 삭제하여, `unoUtil` 내 모든 파이썬 모듈이 `*.py` $\leftrightarrow$ `*.md` 1:1 단일 매뉴얼 원칙(SSOT)에 완벽히 부합하도록 정비 완료<br/>• **문서 목차 구조 일원화**: `1. 개요 및 3계층 아키텍처` $\to$ `2. 최상위 함수 인터페이스` $\to$ `3. 계층형 파라미터 입력 종합 가이드 (신설)` $\to$ `4. 유틸리티 함수 인터페이스` $\to$ `5. 실무 활용 시나리오` $\to$ `6. 표준 네이밍 및 Flat 저장 구조`로 일목요연하게 재정렬 | ✅ 완료 |
> | **v3.37** | 2026-10-16 | uno &<br/>Gemini | 🛠️ **가감속/제동(`vt_acc_brk`) 역직렬화·온디맨드 복원·캐시 소거 로깅 아키텍처 개편 및 INFO(상태 요약)/DEBUG(상세 데이터) 역할 완전 분리 완결**<br/>• **터미널 수백 줄 도배 원천 해소 및 INFO/DEBUG 계층화**: 프로젝트 및 타이어 역직렬화(`__setstate__`) 시 `tire_analyzers`와 `result.df` 전체를 덤프하여 콘솔을 수백 줄 도배하던 레거시 디버그 출력을 정리하고, 평상시에는 1줄 요약 브리핑(`INFO`), 상세 데이터 스펙 및 명판은 디버깅 모드(`DEBUG`)에서만 표출되도록 계층화 분리<br/>• **`VTAccBrkProject` 로깅 개편 (`vt_acc_brk_project.py`)**: `__setstate__` 시 `INFO`로 `[{prj_name}] 프로젝트 역직렬화 로드 완료 (타이어 {n}개: {t_keys})` 한 줄 요약만 출력하고, 수백 줄의 `tire_analyzers` 상세 명판은 `DEBUG` 모드로 완전 격리. `restore_cache` 호출 시 `INFO`로 `[{prj_name}] 전체 프로젝트 캐시 복원 완료` 출력<br/>• **`VTAccBrkTire` 로깅 개편 (`vt_acc_brk_tire.py`)**: `__setstate__` 시 `[result.df] 캐쉬 상태 : None` 2회 중복 출력을 제거하고 `DEBUG` 모드 1줄로 단정하게 정리. `result` 프로퍼티 온디맨드 복원 및 `restore_cache` 시 `INFO`로 `[Memory] {set}[ACC/BRK Test] : 대용량 캐시 복원 완료`, `DEBUG` 모드 시 실제 복원된 `result.df`의 `Shape` 및 `Columns` 상세 출력. `clear_cache` 시 `INFO`로 삭제 완료, `DEBUG`로 소거 상태(`df=None`) 확인 출력<br/>• **`calc_response` 가속/제동 Rising 슬라이싱 IndexError 핫픽스 및 `excel=False` 안전 방어**: `func_acc_brk.py`에서 가속/제동 초기 라이징 구간(`rising_target`) 탐색 시 목표 도달 데이터가 없어 발생하던 `IndexError: index -1 is out of bounds for axis 0 with size 0` 결함을 빈 매칭(`matched.empty`) 가드 및 차수별 `continue` 방어선으로 완벽 해결. `vt_acc_brk.py`의 `excel=False` 실행 시 `excel_raw` NoneType AttributeError 가드 탑재<br/>• **기본 로거 레벨 최적화 (`INFO`) 및 실무 파이프라인 실증**: `vt_acc_brk_project.py`와 `vt_acc_brk_tire.py`의 모듈 로거 기본 레벨을 `logging.INFO`로 정합하여 스노우 노면 특성 분석 파이프라인(`a_make_SnowSurfaceCharacteristic_DF.py`) 실행 시 터미널 가독성 극대화 (실제 `251230_snow_surface_20-5.pjt` 로드 및 온디맨드 복원 실증 완료) | ✅ 완료 |
> | **v3.36** | 2026-10-16 | uno &<br/>Gemini | ⚙️ **가감속/제동(`vt_acc_brk`) 폴더 $\to$ 속도/모드 $\to$ 타이어 3계층 파라미터 분기 단일 표준화 (`resolve_hierarchy_param`), 서브 분석기 스마트 디폴트·부호 자동 동기화(Auto-Sign Alignment) 및 종합 설정 매뉴얼(`vt_acc_brk_config_guide.md`) 완결**<br/>• **단일 표준 3계층 분기 엔진 구축 (`resolve_hierarchy_param`)**: 기존의 비대칭이던 `make_path_dict`와 `get_tire_value`를 단 하나의 일관된 SSOT 함수로 단일화 $\to$ `[1. 폴더/노면]` $\to$ `[2. 속도 조건(vel_tag) / 시험 모드(mode)]` $\to$ `[3. 타이어 시편(tire_set)]` 우선순위로 파라미터를 정밀 매핑하고 기존 함수는 호환 래퍼로 100% 하위 호환 보존<br/>• **서브 분석기 9대 파라미터 계층 분기 정식 편입**: `response_target`, `rising_target`, `vel_split`, `pre_sec`, `col_mudrop_wheelacc`, `col_slip_pdf_wheelslip`, `slip_range`, `slip_mode_vel_range`, `col_slip_mode_wheelslip` 등 서브 분석기 설정 전원을 `config_all_dict` 및 `tire_dict_maps`에 정식 등록하여 폴더별·속도별·타이어별 독립 분기 완비<br/>• **스마트 디폴트 및 물리 부호 자동 동기화 (Auto-Sign Alignment)**: `response_target` 미입력 시 현재 속도 방향에 맞춰 제동 `[-0.5, -0.2]`, 가속 `[0.2, 0.5]` 자동 분기 및 양수 `[0.2, 0.6]` 입력 시 제동 모드 음수 자동 반전 탑재 (`func_acc_brk.py`, `an_response.py` 공통 방어선 구축). `vel_split` 미입력 시 `test_vel`의 중간값으로 자동 스마트 계산 ([100,0] $\to$ 50.0, [20,35] $\to$ 27.5)<br/>• **입력 설정 종합 가이드 매뉴얼 완결 (`vt_acc_brk_config_guide.md`)**: 소스 코드 저장소 직하위에 4대 입력 형태(단일값, 모드별 dict, 폴더별 dict, 타이어별 복합 dict), 전체 파라미터 매트릭스, 스마트 디폴트 로직, 4대 실무 실전 코드 레시피를 집대성한 가이드라인 구축 완료 (Code Manual Isolation Law 준수)<br/>• **자가 진단 스위트 전수 통과**: Case 7(신규 계층 분기 실증), Case 1(Mock 제동 파이프라인), Case 2(다중 프로젝트 병합), Case 6(실무 VBB 가속 풀링 배치) Exit Code 0 무결성 통과 | ✅ 완료 |
> | **v3.35** | 2026-10-16 | uno &<br/>Gemini | 🏷️ **가감속/제동(`vt_acc_brk`) 통합 표준 네이밍 시스템 및 Flat(단일 계층) 저장 구조 구축, 메타데이터 `vel_range` 정규화 및 기술 백서(`vt_acc_brk_모듈_네이밍룰.md`) 확립 완결**<br/>• **식별자-파일명-차트 타이틀 1:1 완전 일치 원칙 (Single Stem Law) 집행**: 타이어 객체 표준 식별자 `[req]_[surface]_[item]_[cond]_[vel_tag]_{set}` 조립 및 `self.tire_name` 프로퍼티 신설, `.tir` 파일명 및 차트 이미지명/타이틀 완전 일치. 프로젝트 객체 3단계 우선순위(1순위: `pjt_name` $\to$ 2순위: 메타데이터 조합 $\to$ 3순위: `{최하위폴더명}_{item}_{vel_tag}`) 조립 및 `self.project_name` 프로퍼티 신설, `.pjt` 파일명 및 프로젝트 비교 차트 이미지명/타이틀 완전 일치<br/>• **단일 계층(Flat) 저장 아키텍처 전면 개편**: 과거 파일명 중복 방지용 임의 하위 폴더(`0. db/brk_100-5/` 등) 완전 폐지 $\to$ `0. db/`, `2. fig/`, `3. result/` 직하위 단일 계층에 정갈하게 보관<br/>• **속도 구간 메타데이터 `vel_range` / `vel_tag` 체계 공식 편입 (`test_infor_res.py`)**: `TestInformation`에 `vel_range` 필드 공식 추가, 리스트(`[100, 5]`) 및 문자열(`'100-5'`, `'20-35'`) 유연한 정규화 파서 탑재, `vel_tag` 프로퍼티 및 `METADATA_MAP['vel_range'] = 'TestVelRange'` 연동으로 요약 테이블 자동 표기<br/>• **오케스트레이터 및 시각화 전 도메인 정합**: `vt_acc_brk.py`에서 `curr_test_vel` 속도 조건을 `tire_infor['vel_range']`에 직통 주입, 캐시 로드(`load_tire`, `load_pjt`) 시 플랫 디렉토리 내 `vel_tag` 스마트 매칭 지원. `plotter_tire.py`, `plotter_project.py`의 `get_path()`, `get_title()` 표준 식별자 Stem 기반 1:1 매칭 연동<br/>• **전용 기술 헌장 및 매뉴얼 완결**: 볼트 프로젝트 폴더 내 **[[50_vt_acc_brk_표준_네이밍_규칙_및_저장_구조|표준 네이밍 룰]]** 영구 기술 백서 신설 (종합 매트릭스, Flat 구조도, 실무 로드 레시피 수록) 및 코드 1:1 매뉴얼(`vt_acc_brk.md`, `vt_acc_brk_tire.md`, `vt_acc_brk_project.md`), 독스트링 Google Style 100% 동기화 완료 | ✅ 완료 |
> | **v3.34** | 2026-10-15 | uno &<br/>Gemini | 🏎️ **가감속 속도 구간 분할 모듈(`segments.py`) 신설, acc_brk 속도 구간 모듈화 선행 리팩토링 및 `04_Resources` 영구 지식위키 거버넌스 전면 개편 완결**<br/>• **`unoUtil.signal_process.post_process.segments` 신규 구축**: 단조성 검사 기반 가감속 속도 구간 분할 알고리즘, 분할 경계 미세시간 선형 보간($\le 1\text{ms}$) 엔진 공식 탑재 (409줄 구축, `segments.py`) 및 마스터 MOC 8번 도메인 공식 편입<br/>• **`acc_brk` 및 `post_process` 속도 구간 모듈화 선행 리팩토링 (`e62e284`)**: `filters.py`, `outliers.py`, `resample.py`, `scaler.py` 및 6대 서브 분석기(`an_acceleration`, `an_mu_drop`, `an_response`, `an_skewness`, `an_slip_pdf`, `an_split_speed`), 코어 오케스트레이터(`func_acc_brk`, `vt_acc_brk*`, `plotter_*`) 총 47개 파일 9,101 라인 대대적 정합 및 속도 대역 모듈화 선행 완료<br/>• **`12_파이썬_소프트웨어_아키텍처_및_엔지니어링` 전용 지식 허브 신설**: 대규모 패키지 모듈화 및 무중단 아키텍처([[10_대규모_파이썬_패키지_모듈화_및_무중단_아키텍처]]), 엔터프라이즈 계층형 로깅 및 Non-blocking 시각화([[20_엔터프라이즈_계층형_로깅_및_무중단_시각화_패턴]]), 대용량 시계열 인메모리 프록시 및 비파괴 슬림 피클링([[30_대용량_시계열_인메모리_프록시_및_비파괴_캐싱_패턴]]) 3대 핵심 아키텍처 수립<br/>• **`13_시계열_신호처리_공학` 전용 지식 허브 신설**: Zero-Phase 필터링 및 위상지연 극복([[10_Zero_Phase_필터링_및_위상지연_극복_공학]]), 1D 웨이블렛 변환 디노이징 및 피크 G 보존([[20_1D_웨이블렛_변환_디노이징_및_피크_보존_수학]]), 적응형 KDE 고속화([[30_적응형_커널_밀도_추정_KDE_및_초고속_알고리즘]]), 다변량 이상치 탐지 및 속도 구간 분할([[40_다변량_센서_이상치_탐지_및_시계열_리샘플링_공학]]) 4대 마스터 위키 완결<br/>• **`21_제동` 30번 단일 마스터 백서 확립 및 구버전 파편 4종 영구 삭제**: 기존 40~43번 파편 문서 4종을 완전히 삭제하고, 오직 **[[30_실차_가감속_성능변화_분석_및_보정_시스템]]** 단 1개의 완결된 백서로 일원화 (콘트롤 타이어 시계열 조각 선형 보간, Polarity 상대 성능지수, 노면온도 감인성 m/℃, GPS 2포인트 공간QC, Mu-Drop 손실거리 분석 등 핵심 공학 이론 100% 보존)<br/>• **`11_회사_실차평가_데이터프레임` 계측 스키마 슬림화**: 승격 완료된 모듈화·로깅·신호처리·보정 중복 문서 4종을 안전 정리하고, VBOX/VBB/Dewesoft 계측 규격 및 표준 DataFrame 스키마([[00_실차평가_데이터프레임_통합_색인]])로 정체성 확립 | ✅ 완료 |
> | **v3.33** | 2026-10-14 | uno &<br/>Gemini | 🧹 **가감속/제동(`unoUtil.vehicle.acc_brk`) 전 도메인 레거시 연결·구버전 함수·과도기 별칭 전면 삭제 및 v2 순수 단일 표준(Single Baseline) 완결**<br/>• **불필요 브릿지/임시 파일 및 레거시 캐시 폴더 영구 삭제**: `correct_factors.py`, `correct_factors.md`, `yaml_test.py`, `legacy/` 디렉토리 및 구버전 `.pyc` 캐시 전수 삭제<br/>• **v2에서 대체 완료된 구버전(v1) 중복 함수·메서드 8종 전면 삭제**: `func_acc_brk.py` 및 `correct.py`의 `calc_braking`, `calc_acceleration`, `calc_kmeans`, `calc_partial_hydro`, `calc_reference_corrected`, `find_reference_tire`, `reorder_columns`와 `VTAccBrkProject.correct_control_tire` 삭제 (`calc_acc_brk`, `Correct.run` 단일 엔진으로 완전 일원화)<br/>• **패키지 전역 레거시 리다이렉트 및 대문자/구버전 별칭 전면 철폐**: `unoUtil/__init__.py`, `vehicle/__init__.py`, `acc_brk/__init__.py`, `analyzers/__init__.py` 및 14개 모듈 하단의 `_BRKTest_`, `ACCBRK`, `VT_ACCBRK*`, `AN_MEMORY`, `CORRECT`, `Cal_Control`, `PLOTTER_TIRE`, `PLOTTER_PROJECT`, `AN_*`, `PP_*`, `save_pjt`, `add_list_tire`, `plot_all`, `plt`, `flag_print`/`bool_print` 프로퍼티 등 모든 레거시 연결고리 100% 제거<br/>• **레거시 `**kwargs` 흡수 로직 제거 및 시그니처 순수화**: 전 모듈에서 `df_raw`, `df_input`, `print`, `flag_print`, `only_braking`, `sr`, `effNum` 등 과도기 인자 흡수 블록을 제거하고 `data: pd.DataFrame`, `bins: int = 100`, `level` 등 순수 v2 표준 시그니처로 정합 (`vt_acc_brk_tire.py` Case 4 `FileDataReader` 정합 포함)<br/>• **12종 1:1 기술 매뉴얼(`.md`) 전수 최신화 및 레거시 섹션 삭제**: `base_memory.md`, `correct.md`, `func_acc_brk.md`, `vt_acc_brk*.md`, `plotter_*.md`, `analyzers/an_*.md`의 시그니처·파라미터·반환 스키마를 실제 코드와 1:1 동기화하고 하위 호환성 섹션 전면 삭제 (전 모듈 단위 테스트 Exit Code 0 통과) | ✅ 완료 |
> | **v3.32** | 2026-10-13 | uno &<br/>Gemini | 🏎️ **가감속/제동(`vt_acc_brk`) 프로젝트 다중 타이어 비교 시각화 엔진(`plotter_project.py`) 가속 시험(Acceleration) 양수(+) 물리 부호 정합 및 속도 대역 정렬 완결**<br/>• **가속도 분포 차트(`compare_acceleration`) 가속 모드 양수 보존 및 정렬 완합**: 제동 전용 시절 하드코딩된 `-1 *` 부호 반전으로 인해 가속 시험 데이터($+0.16g$)가 음수($-0.16g$)로 거꾸로 그려지던 결함을 모드 판별(`mode == 'acc'`)을 통해 원시 양수 물리 부호 그대로 보존하도록 교정하고, 속도 구간 정렬을 가속 모드 시 저속$\to$고속 순방향(`reverse=False`, 예: 20_30 $\to$ 30_35)으로 자연스럽게 표시<br/>• **구간별 가속도 및 성능 지수 차트(`compare_split_acceleration`, `compare_index_split_acceleration`) 양수 정합**: 고속/저속 구간 가속도(`col_acc_high`, `col_acc_low`) 바 차트 및 지수 텍스트 라벨에서 `-1 *` 강제 반전을 제거하여 가속 시험 시 0 기준 위쪽(양수 막대)으로 정확히 렌더링되도록 개선 및 수직 텍스트 정렬(`va = 'bottom' if val >= 0 else 'top'`) 방어 구축<br/>• **가속 응답성 상승 기울기(`compare_rising_slope`) 물리 부호 정상화**: 시스템 응답성 비교 시 `mode == 'acc'`일 때 양의 상승 기울기($+g/\text{s}$)를 유지하도록 분기하여 음수 축소 결함 해결<br/>• **가속(Case 6) 및 제동(BMW 320d Dry) 듀얼 실측 시각화 검증 통과**: 스노우 가속 시험의 Acceleration Distribution($+0.16\sim +0.18g$), Split Acceleration($+0.17\sim +0.18g$) 양수 출력 및 제동 시험의 감속도 크기 양수 비교 정상 표출 100% 동시 검증 완료 | ✅ 완료 |
| **v3.31** | 2026-10-13 | uno &<br/>Gemini | 🗺️ **GPS 로컬 직교 좌표계(`GPStoXYCord`) 시험장 자동 감지, 1000Hz$\to$100Hz 고속 보간 매핑(15ms)을 통한 좌표 슬라이싱 데이터 유실 버그 해결 및 테크노링 직선 시험로 회전각(`rotate = -0.4°`) 기하학적 정합 완결**<br/>• **1000Hz 리샘플 결과(`_result.df`) $\to$ 100Hz 원본 계측(`self.df`) 좌표 슬라이싱 버그 원천 해결 (`vt_acc_brk_tire.py`)**: `self.df[col] = self._result.df[col]` 단순 인덱스 슬라이싱으로 인해 10배 차이나는 행 개수(52,702 vs 527,011)로 앞쪽 10%(52초)만 복사되고 90% 데이터가 증발하던 치명적 결함을 시간 축(`Datetime`/`Time`) 기준 1D 고속 선형 보간(`np.interp`, 단 15ms)으로 완벽 해결 $\to$ T1~T4 모든 타이어의 가속 및 제동 궤적/유효 런(0~8) 100% 온전 복원<br/>• **GPS 시험장 프리셋 인접 자동 판별 기능 신규 탑재 (`GPStoXYCord.detect_preset`, `from_infer`)**: `local_pos=None` 지정 시 데이터 첫 지점 위경도를 기반으로 사내 시험장(테크노링, 테크노트랙 등)을 $\pm 0.05^\circ$ 반경 내에서 자동 감지하여 프리셋 좌표(`reflong`, `reflat`, `rotate`)를 자동 주입하는 편의성 제공<br/>• **Racelogic VBOX 포맷 음수 경도(-7580 분) 부호 보정 로직 보존 및 무결성 검증**: `01_C1.VBO` 실측 검증을 통해 `to_decimal_degrees`의 음수 경도 반전 처리와 정상적인 $+126.3353^\circ$ 변환 동작 재확인<br/>• **테크노링 직선 시험로 회전각 `rotate = -0.4°` 수학적/물리적 증명 및 시각화 검증 완료**: 트랙이 진북 대비 서쪽으로 기울어진 방위각 $\phi = -0.4^\circ$에 대해, 2D 회전 변환 행렬 적용 후 각도 $\phi_{new} = \phi - \theta$ 수식을 기하학적으로 증명 $\to$ 원래 트랙 각도를 빼줌($- (-0.4^\circ)$)으로써 $+0.4^\circ$ 적용 시 2배로 누워버리는 현상($-0.819^\circ$)을 배제하고, `-0.4°` 적용 시 잔여 각도 $-0.019^\circ$로 수직 기준선($X=0$)에 오차 $\pm 3\text{cm}$ 이내 칼같이 수직 정렬됨을 실측 데이터 1:1 비교 검증 완료 (`rotation_comparison_final.png`)<br/>• **가속/제동 전체 파이프라인 무결성 회복**: 예제 6번 등 프로젝트 단위 가속 시험 및 제동 시험에서 모든 타이어의 유효 런과 루프 형상 궤적이 정상 가동됨을 최종 검증 | ✅ 완료 |
> | **v3.30** | 2026-10-13 | uno &<br/>Gemini | 🏎️ **가감속/제동(`vt_acc_brk`) 물리 부호 체계 일원화 리팩토링 (Signed Acceleration Law 집행) 및 가속/제동 전 모듈 정합 완결**<br/>• **물리 가속도 부호 보존 및 임의 반전 강제 철폐 (`func_acc_brk.py`)**: `calc_slip_mode_skewness` 등에서 관습적으로 수행하던 `ax = -1 * ax` 임의 반전을 전면 제거하여 센서 원시 부호 보존 $\to$ 감속(제동)은 음수($-$, 예: $-0.8g$), 가속은 양수($+$, 예: $+0.5g$)로 완전 일원화<br/>• **2D 왜도 밀도 평면 및 시각화 Y축 동적 분기 (`func_acc_brk.py`, `plotter_tire.py`, `an_skewness.py`)**: `mode='brk'` 시 Y축 `[-1.4, 0.0]`(음수 감속 평면) 및 `Deceleration (g)`, `mode='acc'` 시 Y축 `[0.0, 1.4]`(양수 가속 평면) 및 `Acceleration (g)` 동적 라벨링 탑재, `an_skewness.py`의 `mode == 'acc'` 분석 가드 해제<br/>• **가속/제동 슬립률(Wheel Spin vs Wheel Lock) 정의 분기 (`func_acc_brk.py`, `an_slip_pdf.py`)**: `calc_slip`에 `mode` 파라미터 탑재 $\to$ 제동 시 휠락 슬립률 $(V - V_w)/V \times 100$, 가속 시 휠스핀 슬립률 $(V_w - V)/V \times 100$을 양수로 일관되게 산출하도록 분기<br/>• **가속도 기반 성능 보정 및 지수(Index) 크기 비율 연산 정합 (`correct.py`)**: `col_target_negative`에서 `decel` 키워드 제외 $\to$ 제동 시 더 강한 감속력($-0.90g$ vs 기준 $-0.80g$)과 가속 시 더 빠른 가속력($+0.50g$ vs 기준 $+0.40g$) 모두 크기 비율(`abs()`)로 계산하여 각각 112.5%, 125.0% 정상 산출 및 보정값 물리 부호 완벽 보존<br/>• **가속/제동 시스템 응답성 지연 시간 탐색 분기 (`calc_response`, `an_response.py`)**: 제동 시 감속도 하강(음수 $dVelHorizontal \le -0.2$), 가속 시 가속도 상승(양수 $dVelHorizontal \ge +0.2$)으로 분기하여 가속 응답성 분석 완결<br/>• **속도 구간별 가속도 시각화 X축 반전 조건화 (`plotter_tire.py`)**: `split_speed`에서 속도 축 반전(`invert_xaxis()`)을 제동 시험(`is_brk`)일 때만 수행하도록 제한하여 가속 시험 시 저속$\to$고속 순방향 보존<br/>• **단위 및 통합 검증 스위트 100% 통과**: `test_signed_acc_brk.py`를 통해 슬립률, 2D 왜도, 응답성, 보정 지수 전 영역 물리 부호 정합성 검증 완결 (Exit Code 0) | ✅ 완료 |
> | **v3.29** | 2026-10-13 | uno &<br/>Gemini | 🏎️ **가감속/제동(`vt_acc_brk`) 6대 서브 분석기 구버전 호출 전면 정합 및 전체 1:1 기술 매뉴얼(15종) 대대적 개정 완료 (입력인자·kwargs·반환값 스키마·실무 레시피 완비)**<br/>• **6대 서브 분석기 내부 구버전/레거시 함수 호출 전면 정합**: `an_acceleration.py` (`AN_Acceleration` $\to$ `calc_speed_acceleration`), `an_mu_drop.py` (`AN_MuDrop` $\to$ `calc_mu_drop`), `an_response.py` (`AN_Response` $\to$ `calc_response`), `an_slip_pdf.py` (`PP_Slip` $\to$ `calc_slip`, `AN_Histogram`/`AN_PDF` $\to$ `calc_histogram`/`calc_pdf`), `an_split_speed.py` (`AN_Split_Speed` $\to$ `calc_split_speed`) 전면 교체 및 6대 분석기 독립 실행 단위 검증 전수 통과 (Exit Code 0)<br/>• **14대 핵심 계산/동역학 함수 상세 매뉴얼 구축 (`func_acc_brk.md`)**: `calc_mfdd`, `calc_braking`, `calc_acceleration`, `calc_acc_brk`, `calc_slip`, `calc_speed_acceleration`, `calc_split_speed`, `calc_histogram`, `calc_pdf`, `calc_mu_drop`, `calc_slip_mode_skewness`, `calc_response`, `calc_reference_corrected`, `calc_partial_hydro` 전수에 대해 시그니처, 입력 인자, kwargs, 반환값 딕셔너리/데이터프레임 스키마, 실무 레시피 코드 신규 수록<br/>• **6대 서브 분석기 1:1 매뉴얼 대대적 보강 (`analyzers/*.md`)**: `an_acceleration.md`, `an_split_speed.md`, `an_slip_pdf.md`, `an_mu_drop.md`, `an_skewness.md`, `an_response.md` 전 파일의 클래스 생성자, `analysis()` 인자/kwargs, summary/df 프로퍼티 스키마, 온디맨드 캐시 라이프사이클(`clear_cache`), 4륜 위치별 분석 및 실무 레시피 완결<br/>• **상위 코어 분석기 및 보정/시각화 매뉴얼 완결 (`vt_acc_brk_tire.md`, `vt_acc_brk_project.md`, `vt_acc_brk.md`, `correct.md`, `correct_factors.md`, `plotter_tire.md`, `plotter_project.md`, `base_memory.md`)**: 클래스 생성자, 핵심 메서드 파라미터 및 `**kwargs` 상세 명세, 반환값(Returns) 구조, 요약 테이블 스키마, 듀얼 레이아웃 시각화 옵션, 그리고 v1 오리지널 레거시 호환 별칭 명세를 완벽 정합<br/>• **코드 매뉴얼 격리 보존 원칙(Code Manual Isolation Law) 준수**: 1:1 모듈 매뉴얼을 소스 코드 저장소(`unoUtil/vehicle/acc_brk/`) 내부에만 단독 보관하고 볼트로 복사/미러링하지 않음으로써 볼트 오염 방지 및 단일 진실 공급원(SSOT) 준수 | ✅ 완료 |
> | **v3.28** | 2026-10-13 | uno &<br/>Gemini | 🏎️ **가감속/제동(`vt_acc_brk`) 최상위 오케스트레이터 프로젝트 단위 가속 시험(`vt_acc_brk`) 일괄 배치 파이프라인 완성, 2D 왜도 모듈 임포트 누락 핫픽스(`an_skewness.py`) 및 실무 예제(`Case 6`)·1:1 기술 매뉴얼 정합 완결**<br/>• **최상위 오케스트레이터 프로젝트 단위 가속 시험(`vt_acc_brk`) 파이프라인 완비**: 단일 함수 `vt_acc_brk(path={'snow': acc_dir}, item='acc', surface='snow', test_vel=[20, 35], ref_kwd='t1')` 호출 한 번으로 폴더 내 복수 바이너리 파일(`T1.VBB` ~ `T4.VBB`) 자동 스캔 $\to$ 타이어 객체(`VTAccBrkTire`) 생성 $\to$ 프로젝트 취합(`VTAccBrkProject`) $\to$ 컨트롤 타이어(T1) 기준 가속시간/가속도 시계열 보정 및 성능 지수(Index) 산출까지 원스톱으로 처리되는 프로젝트 단위 가속 배치 분석 워크플로우 확립<br/>• **2D 왜도 모듈 임포트 누락 핫픽스 (`an_skewness.py`)**: `an_skewness.py` 내 `calc_slip_mode_skewness` 미임포트로 인해 제동 시험 시 발생하던 `NameError`를 자가 진단 중 적발하여 즉시 정상 임포트 완료<br/>• **실측 가속 계측 데이터 프로젝트 단위 실증 파이프라인 탑재 (`vt_acc_brk.py` Case 6)**: `test_data/acc_brk/acc` 실측 VBB 데이터 기반으로 Case 6 프로젝트 단위 배치 파이프라인을 탑재하여 `Snow_Passing_ACC` 실증 성공 (T1 100%, T2 110.14%, T3 81.21%, T4 103.45%, Exit Code 0 통과)<br/>• **1:1 기술 매뉴얼(`vt_acc_brk.md`) 및 독스트링 최신화**: `vt_acc_brk()` 함수 docstring에 가속 시험 예제 등록 및 `vt_acc_brk.md`에 Case F(스노우 추월 가속 시험 프로젝트 일괄 배치 분석) 실무 레시피 영구 반영 (Code Manual Isolation Law 준수) | ✅ 완료 |
> | **v3.27** | 2026-10-13 | uno &<br/>Gemini | 🏎️ **가감속/제동(`vt_acc_brk`) 가속 시험(Acceleration Test) 모듈 전면 정상화, 5대 핵심 결함 핫픽스 및 실측 가속 계측 데이터(`test_data/acc_brk/acc/*.VBB`) 실증 파이프라인(Case 4) 완결**<br/>• **평균 가속도(`acc_mean`) vs 가속 시간(`acc_time_mean`) 키 충돌(Key Collision) 원천 해소 (`func_acc_brk.py`)**: `get_result()`에서 `mode == 'acc'` 시 가속 소요 시간 통계를 `acc_time_mean`, `acc_time_Range` 등으로 분리 생성하여, 기존 평균 가속도(g) `acc_mean`이 가속 시간(sec)으로 덮어써지던 치명적 결함을 완벽히 해소하고 가속도(g)와 가속시간(s) 동시 보존<br/>• **가속 시험 기본값 및 필터링 정상화 (`calc_acceleration`)**: 제동 하드코딩 기본값(`target_speed=[80, 5]`)으로 인해 0$\to$100km/h 가속 구간이 공집합으로 탈락하던 버그를 해결 $\to$ `target_speed=[0, 100]`, min/max 동적 순서 보정 및 `max_sec=15` 적용<br/>• **가속 모드 감지 시 런 유효 시간 동적 승격 (`calc_acc_brk`, `VTAccBrkTire.analysis`)**: 가속 시험(`test_vel[1] > test_vel[0]`) 감지 시 `default_max_sec=25`초로 자동 승격하여 긴 가속 런이 잘려나가는 문제를 방지하고, 플롯 어노테이션 텍스트(`acc_time`, 단위 `s`, `m`) 정상 표기<br/>• **프로젝트 보정 시 가속시간 성능 지수(Index) 정상화 (`vt_acc_brk_project.py`, `correct.py`)**: `col_result_pjt`에 가속시간 보정 컬럼을 정식 등록하고 `col_target_negative`에 `acc_time`, `acc_time_mean`을 기본 편입 $\to$ 가속 시간이 빠른(우수한) 타이어가 100%를 초과하는 정상 성능 지수를 얻도록 교정 및 `correct.py` 빈 데이터 `.astype(str)` 방어선 구축<br/>• **가속 슬립률(Wheel Spin) 부호 정합 및 PDF 커널 적분 지원 (`an_slip_pdf.py`)**: 가속 모드(`mode == 'acc'`) 감지 시 `slip_mult = -1.0`을 자동 적용하여 휠스핀에 따른 음수 슬립률을 양의 가속 슬립률(SAE 규격)로 자동 정합, KDE 적분 및 `slip_range=[[0, 20]]` 연동 정상화<br/>• **실제 계측 가속 시험 데이터(`test_data/acc_brk/acc/*.VBB`) 실증 파이프라인 탑재 (`vt_acc_brk_tire.py` Case 4)**: VBOX 실측 바이너리 파일(`T1.VBB` ~ `T4.VBB`) 자동 탐색 및 중속 가속(20$\to$35 km/h, 6회차 유효 선별) 정밀 분석, 6대 서브 분석기 연동 및 `VTAccBrkProject`를 통한 컨트롤 타이어(T1) 기준 성능 지수 보정(T2 110.14% 우수, T3 81.21% 열세) 전 파이프라인 실증 통과 (Exit Code 0) | ✅ 완료 |
> | **v3.26** | 2026-10-13 | uno &<br/>Gemini | 🏷️ **가감속/제동(`vt_acc_brk`) 원천 계측 데이터(`tire.df`) 시험 구간 자동 라벨링 및 실시간 구간 물리량(`TestTime`, `TestDist`) 연산 탑재**<br/>• **원천 로우 데이터(`tire.df`) 시험 차수 자동 라벨링 (`VTAccBrkTire.analysis`)**: `analysis()` 실행 시 1ms 리샘플 결과(`result.df`)뿐만 아니라 원본 계측 데이터(`tire.df`)에도 시간축 구간 매핑을 통해 전체 차수 `TestNum` 및 유효 선별 차수 `EffNum`을 1:1로 자동 부여 (시험 외 구간은 `NaN` 자동 격리)<br/>• **구간별 경과 시간(`TestTime`) 및 누적 이동 거리(`TestDist`) 자동 계산**: 각 차수 시작점(0.0s, 0.0m) 기준의 초 단위 경과 시간과 미소 거리 적산 이동 거리를 자동 생성하여, 별도 다운샘플링이나 복잡한 merge_asof 연산 없이도 조향각·브레이크압력·휠속도 등 원본 센서 채널을 차수별로 즉시 필터링·그룹핑·시각화 가능<br/>• **메모리 및 저장 용량 최적화 검증**: 추가 컬럼 4개 부여에 따른 RAM 증가는 약 1~2MB(0.01% 미만)이며, 반복 이산 라벨 및 결측치 특성상 gzip 압축 효율이 극대화되어 `.tir` 저장 파일 증가폭은 수십 KB(0.03MB) 수준으로 성능·용량 부하 0에 수렴<br/>• **판다스 미래 호환성 확보 및 단위 검증 완료**: `groupby(..., observed=False)` 명시로 `FutureWarning`을 원천 차단하고 단위 검증 스위트 100% 통과 | ✅ 완료 |
> | **v3.25** | 2026-10-13 | uno &<br/>Gemini | 🛡️ **가감속/제동(`vt_acc_brk`) 센서 미연결 채널 3중 방어선 구축, Qhull 차원 축퇴(`QhullError`) 원천 해결 및 파이참 IDE 소스 루트 정상화**<br/>• **센서 미연결(Dead Sensor) 자동 감지 및 NaN 격리 (`calc_slip`)**: 휠속도 신호 결측(전행 0, 분산 0, 또는 게인 $\le 0$) 사전 감지 $\to$ 가짜 100% 슬립률 생성을 차단하고 `WS`, `WA`, `SR` 채널을 `NaN`으로 안전 격리<br/>• **전 분석기 유효 채널 자동 선별 (Auto-Pruning)**: `AnSlipPdf`, `AnMuDrop`, `AnSlipModeSkewness`, `AnResponse`에서 실제 유효 데이터($\ge 10$) 및 분산(`ptp > 1e-3`)이 있는 채널만 자동 선별하여, 좌측 센서 단선(`FL`, `RL`) 시에도 우측 휠(`FR`, `RR`)만으로 전 파이프라인 무중단 완주<br/>• **2D 왜도 및 수막 분석 Qhull/KDE 수치적 축퇴 방어**: `calc_slip_mode_skewness` 및 `calc_mu_drop`에서 분산 부재 시 전체 종료 대신 개별 채널 `continue` 스킵 처리, SciPy `griddata`의 2D Qhull 들로네 삼각분할 `try...except` 예외 격리로 `QhullError` 크래시 원천 차단<br/>• **파이참 IDE 소스 루트(`.idea/unoUtil.iml`) 복구 및 인덱싱 복원**: 모듈 설정 파일 내 `<content url="file://$MODULE_DIR$"><sourceFolder .../></content>` 누락 결함을 복구하고 가상환경 `pip install -e .` 링크를 갱신하여 에디터 내 컨트롤+클릭(코드 정의 이동) 100% 복원<br/>• **시각화 무중단 및 대용량 배치 메모리 보호(`close=True`) 아키텍처 안내**: 8종 전문 차트 동시 생성 시 메모리 누수 방지 패턴 및 화면 표출(`close=False` / `tire.plot.slip_pdf()`) 가이드 확립 | ✅ 완료 |
> | **v3.24** | 2026-10-12 | uno &<br/>Gemini | ⏱️ **가감속/제동(`vt_acc_brk`) 및 파일리더(`file_reader`) 시간 결함 감사 및 슬립률·타임존 무결성 정상화**<br/>• **VBOX GPS 시간 파싱 및 타임존 오프셋 핵심 버그 해결**: VBOX `time` 컬럼 수치화 시 선행 0 탈락(예: `053648.72` $\to$ `53648.72`)에 따른 `zfill(6)` 누락 결함 수정 $\to$ 53시로 오판되어 Seconds 단위로 빠져 엉뚱한 심야 시각(23:54)이 되던 오류를 원천 차단하고 UTC 05:36 $\to$ KST 14:36(오후 2시 36분) 정상 계산 완료<br/>• **타임존 오프셋 가산 및 자정 통과 시 일자(`Day`) 자동 롤오버 보존**: UTC 저녁 시간대 시험에 타임존(+9h) 가산 시 익일 날짜 자동 승격(`return_datetime=True`) 및 단일 주행 중 자정 통과 시 `pd.date_range` 타임스탬프 자동 증가 검증 완료<br/>• **슬립률 분포 분석 구간 기본값 개선 (`an_slip_pdf.py`, `an_skewness.py`)**: 하드코딩된 임의 속도(80~5kph)를 제거하고 시험 속도(`test_vel`, 예: 100~1kph)를 기본 분석 구간으로 동적 연동, 정지 부근(0kph) 분모 0 발산 방지를 위한 최소 속도(min_vel=1kph) 가드 및 상세 주석 명시<br/>• **자동 `am`/`pm` 접미사 제거 및 `cond` 수동 처리 규격화**: 13시 분기 기반 임의 접미사 부여 로직 전면 삭제, 수동 입력 없을 시 파일명 및 그래프 타이틀에 `_None`, `_am`, `_pm`이 일절 표기되지 않는 클린 파일명 체계 확립 | ✅ 완료 |
> | **v3.23** | 2026-10-12 | uno &<br/>Gemini | 🗄️ **unoUtil.database 스펙 결합 모듈(`connect_spec_with_req_set`) 정합 및 스노우 파이프라인 직결 연계 완결**<br/>• **오리지널 함수 자산 존중 및 SSOT 일원화**: 사용자가 이전에 완성해 둔 모듈 인터페이스(`connect_spec_with_req_set`)를 그대로 존중하여 `unoUtil.database` 정식 모듈로 수납하고, 스노우 프로젝트(`b_combine_surface_performance_spec.py`)에서 직접 임포트하여 노면-제동-스펙 3대 축을 단일 파이프라인으로 연결<br/>• **정의된 핵심 스펙 인자 슬림 결합 규격 확립**: 불필요한 시험 컬럼을 배제하고 `tb_pl_dw_spec_plm_tire_bas`의 핵심 스펙 인자(`SPEC_CD`, `PTTRNM`, `TIRE_NCSW`, `TIRE_APTRT`, `TIRE_RMICH`)만 정규화하여 55열 통합 데이터셋으로 초경량화 완성<br/>• **오프라인 캐싱 및 예외 방어 강화**: `save` 파라미터 기반 gzip 압축 피클 캐싱 지원으로 오프라인 및 로컬 재실행 안정성 확보 | ✅ 완료 |
> | **v3.22** | 2026-10-12 | uno &<br/>Gemini | 🧹 **옵시디언 볼트 슬림화(볼트 다이어트) 및 소스 코드 매뉴얼 격리 보존 원칙 (Code Manual Isolation Law) 확립**<br/>• **개별 1:1 모듈 매뉴얼(87종) 볼트 전면 퇴출**: 옵시디언 내 불필요하게 복사되어 볼트 비대화 및 이중 동기화 부채를 유발하던 87개 저수준 `.md` 매뉴얼을 전면 삭제하고, Git 형상 관리가 적용되는 소스 코드 저장소(`D:\uno\Python\Projects\unoUtil\`)로 단일 진실 공급원(SSOT) 일원화<br/>• **마스터 MOC 허브 3열 규격표 로컬 코드 직결 리팩토링**: 볼트 내부 위키링크(`[[모듈명]]`)로 인한 고아 링크 및 인덱싱 오염을 원천 차단하고, 11대 도메인 87개 모듈을 실제 소스 코드 경로(`file:///D:/uno/Python/Projects/unoUtil/...`)로 1초 만에 바로 열 수 있는 고속 하이퍼링크 체계로 개편<br/>• **전역 거버넌스 헌장 4대 규칙집(SSOT) 일괄 정합**: `AGENTS.md`, `PYTHON_CODE_AGENT.md`, `code-audit-obsidian-docs/SKILL.md`, `obsidian-wiki-sync/SKILL.md`에서 개별 매뉴얼 볼트 미러링 조항을 전면 폐기하고, "코드 매뉴얼은 코드 저장소에서만 단독 관리하고 볼트에는 단일 마스터 대시보드와 공학 지식(`04_Resources`)만 관리한다"는 헌장 제5조 명문화 | ✅ 완료 |
> | **v3.21** | 2026-10-08 | uno &<br/>Gemini | 🏆 **SnowCorrectionModel 과적합(Overfitting) 배제 및 물리적 설명 가능성을 위한 광역 러프(완만화) 규격 확정**<br/>• **공학적 통찰 기반 과적합 탈피 결단**: 수치적 MAE만 쥐어짜다 발생하는 국소 구역 쪼개짐, 계단식 타일링 및 동심원 분화구(아일랜드)를 전면 배제하고, 물리적으로 타당하고 매끄러운 광역 반응면을 확보하기 위해 광역 러프(완만화) 규격 채택<br/>• **Random Forest 러프 규격 정립**: `max_depth=3, min_samples_leaf=6, min_samples_split=12, n_estimators=100` 반영 $\to$ 모자이크 타일링을 없애고 직관적인 3~4개 거시 구역으로 정돈, 외삽(+3.5mm) $+0.92\text{m}$ 안정 유지, 실차 복원 MAE $0.872\text{m} \to \mathbf{0.460\text{m}}$ (**+47.3% 개선**), $R^2: 0.580 \to \mathbf{0.813}$<br/>• **KNN Regressor 광역 평활화 규격 정립**: `n_neighbors=25` (전체의 약 26%), `weights='uniform'` 탑재 $\to$ 거리 가중치에 의해 생기던 국소 동심원 아일랜드 및 도넛 분화구를 100% 완전 소멸시키고 완만한 광역 평균 경사면 구축, 실차 복원 MAE $0.872\text{m} \to \mathbf{0.613\text{m}}$ (**+29.7% 개선**), $R^2: 0.580 \to \mathbf{0.758}$<br/>• **SVR 주력 모델 확정 및 3대 모델 2D 등고선 맵 최신화**: `3_Snow_Correction_3Models_Contour_Comparison.png` 및 `2_Final_Correction_1st_vs_2nd_Comparison.png` 일괄 갱신 완료 | ✅ 완료 |
| **v3.20** | 2026-10-08 | uno &<br/>Gemini | 🏆 **SnowCorrectionModel 기본 주력 모델 SVR 공식 승격 및 RF / KNN 3대 모델 전수 하이퍼파라미터 그리드 서치(Grid Search) 최적화 기본값 반영**<br/>• **기본 모델 SVR 공식 승격**: `SnowCorrectionModel` 초기화 시 `target_model='SVR'` 및 `c_run_snow_correction_pipeline.py` 기본값을 `'SVR'`로 일원화 확정 (RBF 커널 $C=2.0, \gamma=0.07, \epsilon=0.10$으로 외삽 말림 0% 및 연속 매끄러운 물리 곡면 보장)<br/>• **Random Forest 그리드 서치 최적 규격 기본화**: `max_depth=4, min_samples_leaf=3, min_samples_split=6, n_estimators=100` 탑재 $\to$ 과적합/단차를 제거하고 외삽($h \ge +3.5\text{mm}$)에서도 $+0.56\text{m}$ 정상 양수 유지, 실차 복원 MAE $0.872\text{m} \to \mathbf{0.426\text{m}}$ (**+51.2% 개선**), $R^2: 0.580 \to \mathbf{0.831}$<br/>• **KNN Regressor 그리드 서치 최적 규격 기본화**: `n_neighbors=10, weights='distance', p=1` (Manhattan Distance) 탑재 $\to$ 기존 러프 평활화($k=30$, MAE $0.636\text{m}$) 대비 비약적 향상, 실차 복원 MAE $0.872\text{m} \to \mathbf{0.419\text{m}}$ (**+51.9% 개선**), 순위 보존도 Kendall $\tau=\mathbf{0.472}$ (3대 모델 중 최고 순위 보존력)<br/>• **타이어 스펙별 복원 거동 무결성 검증**: 의뢰 25RD110006EF의 C1~T4 전수 1:1 대조로 2차 온습도 상승($\Delta AH \approx +1.02\text{ g/m}^3$)에 따른 전 타이어 일관된 차감 보정($-0.6\sim -0.7\text{m}$) 무결성 확인 및 T1, T2의 실측 역주행 원인(타이어 고유 패턴 특성/1차 런 노이즈) 규명 완결 | ✅ 완료 |
> | **v3.19** | 2026-10-08 | uno &<br/>Gemini | 🏆 **SnowCorrectionModel SVR 3대 핵심 하이퍼파라미터($C, \gamma, \epsilon$) 그리드 서치(Grid Search) 최적 튜닝 및 주력 보정 모델(`primary_model='SVR'`) 정식 승격**<br/>• **75개 파라미터 조합 그리드 탐색**: 외삽 말림 방지($h \ge +3.5\text{mm} \to +0.67\text{m}$ 안정 유지)와 실차 1차 vs 2차 복원 성능(MAE 개선율)의 최적 균형점인 **`C=2.0, gamma=0.07, epsilon=0.10`** 도출 확정<br/>• **실차 복원율 대폭 향상**: 95개 세트 실차 복원 MAE $0.872\text{m} \to \mathbf{0.528\text{m}}$ (**+39.2% 개선**, 초기 완만화 +35.0% 대비 대폭 향상), $R^2: 0.5804 \to \mathbf{0.7672}$, 추세선 기울기 $\text{Slope}: 0.61 \to \mathbf{0.70}$<br/>• **주력 파이프라인 공식 승격**: `c_run_snow_correction_pipeline.py`의 `primary_model` 기본값을 `'SVR'`로 변경하고 전 단계 재가동 (엑셀 테이블 `corrected_char_brk_dist_comparison_table.xlsx` 및 Figure 1, 2, 3, 4 SVR 기준 산출 완결)<br/>• **스펙별 타이어 분산 검증**: 의뢰 25RD110006EF 대상 Tire C2 오차 개선율 **88.7%**, Tire T4 **80.4%**, Tire T3 **47.6%** 복원 입증 | ✅ 완료 |
> | **v3.18** | 2026-10-08 | uno &<br/>Gemini | 🌐 **SnowCorrectionModel SVR RBF 외삽 말림(Curling) 규명 및 완만화(`gamma=0.05`) 규제 정식 반영**<br/>• **SVR RBF 외삽 감쇠 메커니즘 공학적 규명**: 데이터가 없는 최외곽($\Delta \text{char\_height} \ge +2.5\text{mm}$) 영역에서 가우시안 커널 $K(x, x') \to 0$으로 급격히 소멸하며 모델 예측값이 바이어스($b \approx 0\text{m}$)로 강제 추락하고 등고선이 안쪽으로 둥글게 말려 들어가는(Curling/Looping) 현상 수치 검증 완료 ($h=+1.5\text{mm} \to +1.05\text{m} \to h=+3.5\text{mm} \to +0.12\text{m} \to h=+4.0\text{mm} \to -0.16\text{m}$ 역전)<br/>• **SVR 완만화 규제 정식 탑재 (`gamma=0.05`, `svr_params` 지원)**: 가우시안 유효 반경을 대폭 확장하여 최외곽에서도 $+0.80\sim 0.89\text{m}$의 안정적 양수 보정값을 유지하고 등고선이 바깥으로 자연스럽게 뻗어나가는 열린 곡면 구조 확립<br/>• **3대 모델 2D 등고선 보정 맵 및 1차 vs 2차 복원 산점도 일괄 최신화**: `3_Snow_Correction_3Models_Contour_Comparison.png` 및 `2_Final_Correction_1st_vs_2nd_Comparison.png` 재생성 완료 (95개 세트 실차 복원 MAE 개선율 +35.0%, $R^2=0.7608$)<br/>• **기술 매뉴얼 동기화**: `correction_model.md`의 `train_models`에 `svr_params` 파라미터 및 외삽 방어 설계 명세 반영 | ✅ 완료 |
> | **v3.17** | 2026-10-08 | uno &<br/>Gemini | 📊 **SnowCorrectionPlotter 3대 모델(RF vs SVR vs KNN) 1차(Ref) vs 2차(Raw/Corr) 실차 제동거리 복원 수렴도 산점도 비교 체계 및 파일 잠금 방어 체계 구축**<br/>• **[Figure 2-Multi] 복원 산점도 비교 메서드 정식 탑재 (`scatter_restoration_comparison`)**: 1차 기준(Ref) vs 2차 실측(Raw)/보정(Corr) 산점도를 1행 3열 서브플롯으로 구성하고, $X, Y$ 공통 축 범위 고정, $y=x$ 대각선, 2nd Raw(붉은 원) $\to$ 2nd Corr(푸른 사각) 수렴 화살표 벡터, 선형 회귀 추세선(Trendline) 및 타이어 순위 보존도(Kendall $\tau$, Spearman $\rho$)를 자동 라벨링<br/>• **3대 모델 실증 정량 검증 ($N=95$ 세트)**:<br/>  - **SVR (RBF)**: MAE $0.872\text{m} \to \mathbf{0.452\text{m}}$ (**+48.20% 개선, 1등 🥇**), 타이어 순위 보존도 Kendall $\tau=\mathbf{0.4076}$ (**1등 🥇**), Spearman $\rho=\mathbf{0.4848}$ (**1등 🥇**)<br/>  - **Random Forest**: MAE $0.872\text{m} \to 0.453\text{m}$ (+48.05% 개선), $R^2: 0.5804 \to \mathbf{0.8160}$, Kendall $\tau=0.3537$<br/>  - **KNN Regressor**: MAE $0.872\text{m} \to 0.636\text{m}$ (+27.07% 개선), $R^2: 0.5804 \to 0.7484$, Kendall $\tau=0.3416$<br/>• **Windows 파일 잠금(`OSError [Errno 22]`) 방어 저장 체계 완비 (`_safe_savefig`)**: 사진 뷰어 열림 상태에서도 파이프라인 중단 없이 안전 로깅 및 우회 처리 지원<br/>• **파이프라인 및 문서 동기화**: `c_run_snow_correction_pipeline.py` 5-1단계 공식 연동 (`2_Final_Correction_1st_vs_2nd_Comparison.png`) 및 `correction_plotter.md` 갱신 | ✅ 완료 |
> | **v3.16** | 2026-10-08 | uno &<br/>Gemini | 🌲 **SnowCorrectionModel Random Forest 파라미터 완만화(Regularization) 및 3대 핵심 모델(RF vs SVR vs KNN) 2D 등고선 보정 맵 비교 체계 구축**<br/>• **외삽(Extrapolation) 왜곡 메커니즘 규명**: 침하량 차분 실측 최대값(+3.12mm)을 초과하는 3~4mm 영역이 100% 외삽 영역임을 확인하고, 3.0mm 외곽의 소수 특이 음수 샘플($-0.98\text{m}, -0.40\text{m}$)에 의해 깊은 트리(`max_depth=5, leaf=1`)가 과적합되어 제동거리 증가가 역전/감소하던 비물리적 현상 완전 규명<br/>• **RF 파라미터 완만화 규제 적용 (`max_depth=3, min_samples_leaf=4, min_samples_split=8`)**: 의사결정나무의 자잘한 계단식 타일링 및 세로 줄무늬를 제거하고 외곽 영역에서도 안정적인 정상 양수 보정값(+1.0~1.4m) 유지. 실차 편차 개선율 48.05%, $R^2=0.6140$ 확보<br/>• **3대 모델(RF vs SVR vs KNN) 등고선 비교 메서드 탑재**: `SnowCorrectionPlotter.correction_map_comparison()` 구현으로 단일 화면(1행 3열)에서 동일한 컬러바(Colorbar) 스케일로 각 모델의 반응면을 왜곡 없이 1:1 대조 지원 (`3_Snow_Correction_3Models_Contour_Comparison.png`)<br/>• **5-Fold 교차 검증(Out-of-Sample CV) 및 SVR(RBF) 우수성 실증**: RF의 $R^2=0.86$은 훈련 데이터 암기(과적합) 효과였으며, 미관측 데이터에 대한 교차 검증 일반화 성능은 매끄러운 유선형 물리 곡면을 형성하는 SVR(RBF 커널)이 CV $R^2=0.4848$, CV MAE=$0.4873\text{m}$로 전체 1위임을 입증<br/>• **파이프라인 및 문서 완비**: `c_run_snow_correction_pipeline.py` 가동 및 `correction_model.md`, `correction_plotter.md`, `00_unoUtil_모듈개발_대시보드.md` 최신화 완료 | ✅ 완료 |
> | **v3.15** | 2026-10-08 | uno &<br/>Gemini | ❄️ **SnowSurfaceInterpolator 데이터 무손실 원칙 복원(range=None) 및 노면 등고선 세션 간 1:1 비교 전역 고정 스케일 시각화 체계 확립**<br/>• **데이터 무손실 원칙 복원 (`range_height=None, range_temp=None`)**: 3.0mm 하드코딩 클리핑을 전면 해제하여 실제 스노우 침하 깊이(1.6~18.8mm) 및 노면 온도차를 100% 무손실 보존. `_sanitize_feature` 및 `get()`에서 `valid_range is None`일 때 클리핑 바이패스 처리<br/>• **통합 데이터셋 복원 재가동**: `b_combine_surface_performance_spec.py` 재실행으로 `1. df_combine_test_surface_spec.pkl` 무손실 복원 완료 (`char_height` 최대값 3.0mm $\to$ 8.40mm, 차분 표준편차 $\Delta \text{char\_height}$ 0.13mm $\to$ 1.54mm로 10배 이상 물리적 변동성 복원)<br/>• **세션 간 1:1 비교 전역 고정 스케일 시각화 표준화**: `SnowSurfaceInterpolator.plot()`에 X축(0~400m), Y축(45~90m), Z침하량(0~12mm, 25 levels), Z온도차(-0.5~3.5℃, 25 levels) 고정 스케일 및 `cond_id` 기반 다중 세션 스냅샷 자동 탐색 지원<br/>• **보정 파이프라인 및 등고선 보정맵 갱신**: `c_run_snow_correction_pipeline.py` 가동으로 Random Forest $R^2=0.8645$, MAE 55.9% 개선 확인 및 복원된 노면 침하량(-4.0~4.0mm) 반영 2D 등고선 보정맵(`3_Snow_Surface_char_height_VS_cd_test_ah_Contour.png`) 최신화<br/>• **1:1 기술 매뉴얼 동기화**: `surface_interpolator.md` 명세 및 실무 예제 갱신 | ✅ 완료 |
> | **v3.15** | 2026-10-17 | uno &<br/>Gemini | 🎯 **CurveCombiner v2 전면 표준화, 컴포지션 패턴 혁신 및 Slip_Ax_Test 실차 VBB 제동 슬립 피팅 파이프라인 완성**<br/>• **치명적 결함(SP_Normal NameError) 원천 해결**: `_archive` 레거시 함수를 `unoUtil.signal_process.post_process.scaler.scale_data`로 완벽 치환 ([0, 1] Min-Max 안전 정규화)<br/>• **안티패턴(`self.__dict__.copy()`) 및 다중 상속 전면 폐기**: `BaseSpline` ➔ `GradientSmoother` ➔ `TransitionFinder` ➔ `LineMaker` ➔ `HermiteConnector` ➔ `PchipSmoother` ➔ `ClothoidConnector` 각 컴포넌트를 독립 객체화하고, `CurveCombiner`가 총괄 지휘하는 **순수 컴포지션 패턴(Composition Pattern)**으로 전면 리팩토링<br/>• **제동 초반/후반 슬립률 보존 동적 속도 탐색기(`find_optimal_fitting_vel_range`) 신규 탑재**: 통상 [40, 5] km/h 고정 구간의 슬립률 양 끝단 결손 한계를 극복, 제동 시작 시점($a_x < -0.05\text{g}$) 직전 차속과 정차 최저 속도($1.0\text{ km/h}$)를 자동 감지하여 전체 슬립 구간($0 \sim 100\%$) 데이터 보존 자동화<br/>• **실제 실차 계측 데이터(Slip_Ax_Test VBB) 및 방식 B (`VTAccBrkTire` + `AnSlipPdf`) 연동 완성**: `FileDataReader` + `VTAccBrkTire.analysis` + `AnSlipPdf`를 통해 휠속도 게인 보정 및 슬립률/감속도 자동 추출 후 `CurveCombiner.fit`으로 직결되는 3대 자가 구동 스위트 전원 통과 (Exit 0)<br/>• **비차단(Non-blocking) 시각화 및 다형성 save 표준화**: 모든 플롯에 `plt.close(fig)` 의무화로 GUI 블로킹/메모리 누수 차단, 1:1 기술 매뉴얼(`curve_combiner.md`) 최신 실무 예제로 100% 동기화 | ✅ 완료 |
> | **v3.14** | 2026-10-06 | uno &<br/>Gemini | ❄️ **스노우 제동 환경보정 방법 2 1차/2차 양방향 절대 보정(CORR_D1, CORR_D2, CORR_AVG) 파이프라인 완성 및 Figure 2 수렴 산점도 연동**<br/>• **방법 2 양방향 절대 보정 엔진 완성**: 1차와 2차 시험을 각각 사내 공통 기준 환경($-8.0^\circ\text{C}, 1.5\text{ g/m}^3$)으로 독립 절대 보정하여 `BRK_DIST_METHOD2_CORR_D1`, `BRK_DIST_METHOD2_CORR_D2`, `BRK_DIST_METHOD2_CORR_AVG` 산출 완비<br/>• **Figure 2-M2 산점도 수렴 벡터 연동**: `SnowSlopePlotter.scatter_restoration`에 양방향 절대 보정 모드 구현 (1차 및 2차의 보정 전 $\to$ 보정 후 $y=x$ 완전 일치선으로의 수렴 벡터 렌더링, 온습도 표준 환경 라벨링 정합)<br/>• **실증 검증 및 16개 시트 다중 엑셀/피클 배포**: 1,043쌍 검증 결과 2D-KNN 광역 평활화로 양측 절대 보정 시 오차 누적 없이 MAE $0.822\text{m} \to \mathbf{0.804\text{m}}$(+7.6% 개선), $R^2: 0.837 \to \mathbf{0.844}$, $r: 0.921 \to \mathbf{0.923}$ 달성 및 16개 시트 다중 엑셀(`df_corrected_method2_by_category_env.xlsx`) 일괄 재배포 완결 | ✅ 완료 |
> | **v3.13** | 2026-10-02 | uno &<br/>Gemini | ❄️ **스노우 제동 환경보정 2D-KNN 러프 평활화 모델 확정, 10~35m 이상치 필터링 복원, 복원 전·후 R² 및 산포개선율 단일 마스터 통합보고서 완성**<br/>• **방법 2 2D-KNN 러프 평활화 확정**: `SnowCorrectionModel(target_model='KNN Regressor')` 단일 엔진 적용, 국소 아일랜드 배제를 위해 $k=40\sim 150$(20%) 및 uniform 가중치 적용 완만 노면 반응면 도출<br/>• **정상 평가 구간(10m~35m) 이상치 필터링 복원**: 50m 수준 이상치 사전 차단으로 회귀면 왜곡 원천 제거<br/>• **단일 마스터 통합 보고서 완성 (개별 파편 파일 100% 정화)**: 분산된 개별 보고서 3종을 영구 삭제하고 `00_과거_스노우_제동_환경보정_종합_통합보고서.md` 단일 마스터로 통합, 그래프와 100% 일치하는 복원 전·후 $R^2$($0.70\sim 0.91$) 및 $r$($0.86\sim 0.96$) 단독 표와 방법 2 표준편차($\sigma$) 산포개선율 단독 표 정립<br/>• **심층 공학 분석 수록 (Section 2.2)**: 방법 1(RF) 절대 보정 적용 시 비선형 가산성 결핍 및 오차 누적(MAE 0.608m vs 1.110m) 실증 규명 및 역할 분담 체계 정립<br/>• **51종 시각화 및 16개 시트 다중 엑셀/피클 배포 완결** | ✅ 완료 |
> | **v3.12** | 2026-10-02 | uno &<br/>Gemini | ❄️ **unoUtil.snow_condition 노면 환경 선처리 분리, 방법 2 동일스펙 독립 물리 기울기 엔진(SnowSlopeModel) 정식 편입 및 No Redundant Prefix Law 적용 완결**<br/>• **데이터 선처리 전담 모듈 분리 (`preprocessor.py`)**: `filter_snow_conditions()`로 기온 영역(정상 vs 이상), 강설 여부(눈 제외 vs 포함), 타이어 카테고리별 선처리 로직 격리 및 모델 범용성 확보<br/>• **방법 2 전용 엔진 (`slope_model.py`) 신규 구축**: 동일 스펙(`SPEC_NO`) 중심화 1변수 독립 OLS 물리 기울기($k_{\text{air}}, k_{\text{ah}}$) 산출, 표준 환경(-8℃, 1.5g/m³) 일괄 보정 및 전용 플로터(`SnowSlopePlotter`) 탑재<br/>• **No Redundant Prefix Law 전면 준수**: 플로터 내 메서드명에서 `plot_` 접두사 전면 삭제 (`delta_prediction_scatter`, `scatter_restoration`, `correction_map`, `slope_scatter`, `variance_reduction`)<br/>• **과거 7개년 스노우 제동 데이터 전면 재구축 및 8대 데이터셋/시각화 완료**: 4대 시나리오별 매트릭스 파이프라인 가동 및 8종 pkl/xlsx 분리 저장, 90여 종 시각화 실시간 배포 완료 | ✅ 완료 |
> | **v3.11** | 2026-10-02 | uno &<br/>Gemini | 🏎️ **unoUtil.vehicle.acc_brk 가감속/제동 전 도메인 v2 정식 표준화 및 로거 레벨 격리 완결**<br/>• **인스턴스 격리 동적 로거 아키텍처 수립**: `print` 키워드 인자 전면 퇴출 및 `level: Union[int, str] = logging.DEBUG/INFO` 도입, 피클 직렬화 안전성을 위한 `self._level` 저장 + `@property def logger(self):` 동적 바인딩 완성<br/>• **과도기 코드 레거시 취급 배제 (Single Baseline Law)**: `cal_control.py` 및 `.md` 완전 삭제 및 `correct.py` 단일 SSOT 흡수, v2 내부 상호 호출에서 구버전 대문자 심볼 전면 배제<br/>• **전용 클래스 메서드 접두사 중복 배제 (No Redundant Prefix)**: `PlotterTire`, `PlotterProject`의 `plot_` 접두사를 제거하여 `plotter.accbrk()`, `plotter.all()`, `compare_braking()` 등 직관적 객체지향 API 정립<br/>• **표준 파라미터 네이밍 전면 정합**: `df_raw`, `df_input` ➔ `data: pd.DataFrame`, `sr` ➔ `sample_rate`, `flag_print` ➔ `level`<br/>• **18개 소스 파일 및 15종 기술 매뉴얼 100% 무결성 검증**: AST 기반 파라미터 정밀 감사(구버전 변수 0건) 및 모듈별 자율 시뮬레이션(Exit Code 0) 전원 통과, 옵시디언 볼트 1:1 미러링 완료 | ✅ 완료 |
> | **v3.10** | 2026-10-01 | uno &<br/>Gemini | ❄️ **SnowSurfaceInterpolator 순수 공간 보간기 정립 (센서 연산 완전 분리, char_* 단일 표준화 및 3중 결측/이상치 방어)**<br/>• **센서 하드웨어 연산 100% 완전 분리 (SoC)**: 보간기 내부의 특정 센서 뺄셈(`Height1~6`, `Temp1~2`, `h_left`, `h_right`, `h_out`, `h_tire` 등)을 전면 삭제하고 데이터 전처리 영역으로 격리, 순수 3D 공간 보간기에만 집중하도록 정립<br/>• **`char_*` 단일 명명 체계 (SSOT) 전면 일원화**: 파편화된 별칭(`calc_h_diff`, `calc_t_diff`, `HeightDiffAver`, `TempDiffAver`) 영구 정리, `char_height`, `char_temp`, `Cond_ID` 표준 컬럼으로 인터페이스 및 내부 학습 단일화<br/>• **3중 결측치·이상치 안전 정제 파이프라인 (`_sanitize_feature`, `np.clip`)**: 비수치 변환 ➔ 센서 결측치(NaN) 중앙값 대치 ➔ 물리적 범위 이탈값 `np.clip` 상/하한 안전 제한 완비<br/>• **실데이터 엔드투엔드 파이프라인 전수 통과**: `b_combine_surface_performance_spec.py` 1,964건 전수 결합 및 `c_run_snow_correction_pipeline.py` 머신러닝 차분 보정 완벽 완주 (Exit Code 0) | ✅ 완료 |
> | **v3.9** | 2026-10-01 | uno &<br/>Gemini | ❄️ **노면 차분 머신러닝 보정 엔진 동적 특성 인자(x_cols, y_col) 지원, 결측치(NaN) 방어 가드 및 시각화 동적화**<br/>• **동적 특성 인자 리스트 표준화**: 고정 키워드 인자(`x_1`, `x_2`)를 완전히 탈피하고, 파이썬 표준 리스트 인터페이스 `x_cols: Optional[List[str]]` 및 `y_col: str`로 전면 개편 (기온, 습도, 침하량 등 임의 조합 및 3개 이상 다변량 피처 확장 100% 지원)<br/>• **결측치(NaN) 자동 정제 및 방어 가드 (`missing_strategy='drop'`)**: 센서 결측치 자동 드롭, All NaN 컬럼 및 빈 입력 시 명시적 `ValueError` 사전 차단<br/>• **다형성 예측 인터페이스 (`predict_delta`)**: 스칼라, 딕셔너리, NumPy 배열, Pandas DataFrame 단일 함수 다형성 지원<br/>• **시각화 플로터 및 검증기 100% 동적 라벨링 연동**: 모델에 전달된 특성 컬럼명이 산점도(Fig 1), 2D 등고선 맵(Fig 3), 대조표에 자동 실시간 반영<br/>• **전수 무결성 검증 통과**: 단위 테스트 및 1,964건 실데이터 파이프라인 완벽 완주 (Exit Code 0) | ✅ 완료 |
> | **v3.8** | 2026-10-01 | uno &<br/>Gemini | ❄️ **SnowSurfaceInterpolator 직관적 단일 표준 확립 및 12:30 세션 쪼개짐 원천 해결**<br/>• **네이밍 & 아키텍처 혁신**: 추상적이고 모호했던 `SurfaceConditionTwin` 및 `surface_twin.py`를 완전히 폐기하고, 수치해석/데이터과학 표준에 부합하는 **`SnowSurfaceInterpolator`** (`surface_interpolator.py`)로 승격 리팩토링<br/>• **사이킷런 표준 인터페이스**: `interp.fit(df_surface)` (3D 격자 보간 모델 구축) $\to$ `interp.transform(df_brk)` (제동 데이터에 노면 특성치 일괄 결합) 표준 확립<br/>• **시험 묶음 최초 시작 시각(`min(Datetime)`) 기반 단일 세션 결합**: `Date + ReqNo + TestOrder` 그룹별 최초 시작 시각을 감지하여 12:30 경계 전후에 걸쳐 진행된 제동 시험 세트가 am/pm으로 분열되는 치명적 데이터 왜곡 결함을 100% 원천 해결<br/>• **파이프라인 초경량화**: `b_combine_surface_performance_spec.py`의 수동 for 루프 30줄을 단 2줄로 압축, 1,964건 제동 데이터 전수 매칭 및 2026-01-13 단일 세션 유지 완벽 검증 | ✅ 완료 |
> | **v3.7** | 2026-10-01 | uno &<br/>Gemini | ❄️ **노면 정비 세션(Cond_ID) 기반 시공간 디지털 트윈 격리 보간 및 SSOT 스키마 정합**<br/>• **세션(Session) 개념 정합**: '동일 시기 및 동일 노면 컨디션(정비 이력)'을 보장하는 단일 세션(`Cond_ID`, 예: `2026-01-15_am`, `2026-01-19_all`) 체계 완비<br/>• **세션 자동 분류기 편입**: `classify_surface_condition(dt)` 공식 함수 구현 (노면일지 3단계 정비 캘린더 규칙: 2회 정비일 12:30 분기, 혹한 0/1회 정비일 all 단일 세션 자동 판별)<br/>• **세션 격리 시공간 보간**: `SurfaceConditionTwin.get_surface_condition`에서 해당 `Cond_ID` 스냅샷 그룹 내부에서만 시간 축 선형 보간을 수행하여 정비 전후 노면 왜곡 및 이종 날짜 혼합 원천 차단<br/>• **스키마 및 애니메이터 연동**: `schema.py`(`COL_COND_ID`, `COL_PREPARING`), `surface_animator.py`(`cond_id` 인자 지원) 전면 정합 및 전수 자가 테스트 통과 (Code 0) | ✅ 완료 |
> | **v3.6** | 2026-10-01 | uno &<br/>Gemini | ❄️ **Single Master MOC 헌장 정합 및 snow_condition 서브모듈 리팩토링**<br/>• **Single Master MOC & Vault-Only SSOT 완결**: 소스 코드 디렉토리 내 오생성 대시보드 및 하위 대시보드 영구 삭제, 최상위 단일 대시보드로 MOC 완전 흡수 일원화<br/>• **모듈 명명 정합화**: 프로젝트 대시보드와의 명칭 혼동을 원천 해소하기 위해 `dashboard.py` ➔ **`surface_animator.py`**(`SurfaceAnimator` 클래스 및 `create_surface_animation_figure` 함수)로 승격 리팩토링<br/>• **1:1 기술 매뉴얼 정합**: `surface_animator.md` 로컬 및 옵시디언 이중 동기화 완료 및 전수 자가 구동 테스트 통과 (Exit 0) | ✅ 완료 |
> | **v3.5** | 2026-09-30 | uno &<br/>Gemini | ❄️ **snow_condition 공식 도메인 승격 및 acc_brk 스타일 컴포지션 패턴 구축**<br/>• **snow_condition 전면 이관**: 47대 SSOT 노면 계측, 물리 역학, 3D 디지털 트윈, 4D 대시보드, ML 보정 엔진 공식 편입<br/>• **컴포지션 패턴 분할**: SnowCorrectionModel(코어 모델) + SnowCorrectionValidator(정량 검증) + SnowCorrectionPlotter(시각화 플로터)<br/>• **보정 전/후 다형성 비교 플롯**: plot_tire_subsets_comparison 구현 (의뢰번호 전체 서브플롯 및 개별 세트 상세 플롯, 1st Ref선 vs 2nd Raw 점선 vs 2nd Corr 실선 + Run 산점도)<br/>• **1:1 기술 매뉴얼 7종 및 하위 대시보드 MOC 완비, 전수 무결성 검증 통과 (Exit 0)** | ✅ 완료 |
> | **v3.4** | 2026-09-29 | uno &<br/>Gemini | 🎯 **curve_fit 최상위 도메인 승격, tire_curve 패키지 완전 일원화 및 단일 마스터 MOC 정비**<br/>• **curve_fit 최상위 도메인 신설**: `unoUtil.curve_fit` 도메인 및 `tire_curve/` 전용 패키지 구축<br/>• **타이어 피팅 단일 모듈화**: `CurveCombiner`, `fit_mf_ax`, `estimatorMF`, `MinimizeEstimator` 등 분산 피팅을 **`TireCurve` 단 하나의 타이어 피팅 모듈**로 완전 흡수 통합<br/>• **57KB 스플라인 결합 파이프라인 수납**: `curve_combiner/` 복합 파이프라인의 내부 캡슐화 및 OCP 미래 확장 구조 완비<br/>• **models(수식)와 curve_fit(피팅) 역할 분리**: `models`는 순수 지배 방정식 SSOT, `curve_fit`은 데이터 피팅 전담<br/>• **12대 도메인 및 36개 레거시 경로 100% 무결성 검증 통과 (Exit 0)** | ✅ 완료 |
> | **v3.3** | 2026-09-28 | uno &<br/>Gemini | 🎯 **TireCurve 전략 패턴 및 BicycleModel 전면 표준화 완결 (Exit 0)**<br/>• **TireCurve 구축**: 임의 수학 모델(`model`) 및 최적화 전략(`method`) 주입 가능한 전략 패턴(Strategy Pattern) 기반 단일 클래스 설계<br/>• **2-DoF 자전거 모델 정합**: `dynamic_formula` ➔ `bicycle_model.py`(`BicycleModel`) 자동차공학 국제 표준 정규화<br/>• **Pacejka MF SSOT 확립**: 도메인별 분산 수식을 `calc_magic_formula` 단일 코어로 일원화<br/>• **무결성 검증 100% 통과**: 11대 공식 도메인 패키지 & 36개 구버전 레거시 가상 리다이렉션 전원 통과 | ✅ 완료 |
> | **v2.9** | 2026-09-26 | uno &<br/>Gemini | 🏎️ **unoUtil.vehicle 도메인 v2 전면 표준화 및 Single Baseline Law 확립**<br/>• `vehicle_dynamic.py`를 `VehicleDynamic` 단일 표준 클래스로 캡슐화 완료 (8대 표준 동사 정합, v1 호환 별칭 바인딩, 비차단 시각화 및 자가 구동 테스트 스위트 구축)<br/>• `hndl_test.py`, `test_infor_res.py`, `analysis_test_data.py` 전면 리팩토링 및 1:1 위키 매뉴얼 100% 달성 | ✅ 완료 |
> | **v2.8** | 2026-09-24 | uno &<br/>Gemini | 🏁 **unoUtil v2.0 아키텍처 전면 완료 및 전수 무결성 검증 100% 통과 (Final)**<br/>🛡️ 사내 보안 정책(AppLocker) 및 Windows 11 Smart App Control 대응: `D:\uno\Python\envs\unoBase` 표준 환경 구축 및 C/Fortran 확장 DLL 로드 차단 완벽 해소<br/>🧪 전사 10대 도메인 & 36개 세부 레거시 경로 무결성 100% 통과 (`test_structure_integrity.py` Exit 0 달성) | ✅ 완료 |
> | **v2.7** | 2026-09-23 | uno &<br/>Gemini | 🧹 **전사 역방향 별칭(`Standard = LEGACY`) 전수 제거 및 정방향(`LEGACY = Standard`) 일괄 정합화**<br/>🛡️ 물리 `legacy/` 9개 디렉터리 및 `convenienceFunction/` 전량 `_archive/` 영구 퇴출 (Zero Physical Legacy 달성) | ✅ 완료 |
> | **v2.6** | 2026-09-23 | uno &<br/>Gemini | 🗄️ **GetDB 실차시험 스펙 및 결과 통합 엔진 신규 구축**<br/>• `_func_connect_spec_with_req_set.py` 및 `_func_connect_vehicle_test_and_spec.py` 구현, SSL 인증서 패치 적용 | ✅ 완료 |
> | **v2.0** | 2026-09-18 | uno &<br/>Gemini | 🏎️ **unoUtil v2.0 Clean Architecture 10대 도메인 설계 전면 전환**<br/>📦 패키지 다이어트: 1GB+ 거대 계측 데이터 전량 분리 $\rightarrow$ 루트 `test_data/` 중앙 통합 (15.62MB 순수 파이썬 초경량화, 98.5% 절감)<br/>🎯 8대 표준 동사 네이밍 수립 및 `MetaPathFinder` 무중단 가상 로더 수립 | ✅ 완료 |
> | **v1.0** | 2026-09-10 | uno | 🚀 unoUtil 사내 파이썬 통합 프레임워크 개발 프로젝트 킥오프 | ✅ 완료 |

---

## 🏛️ 2. Clean Architecture 12대 도메인 아키텍처

> [!NOTE]- 🏗️ 아키텍처 다이어그램 및 패키지 구조 [클릭하여 펼치기]
> ```mermaid
> flowchart TD
>     subgraph Storage_Isolation [프로젝트 최상위 3대 기둥 분리]
>         P_CODE["🚀 unoUtil/ (순수 파이썬 프레임워크 - 초경량화)"]
>         T_DATA["⭐ test_data/ (단일 중앙 테스트 데이터 - 90% 다이어트)"]
>         ARCH["🗄️ _archive/ (과거 코드 영구 보존소 - 탐색기 열람)"]
>     end
> 
>     subgraph Core_Domains [unoUtil 12대 핵심 도메인]
>         V["🏎️ vehicle/ (실차 시험 & 동역학)"]
>         G["🛰️ gps/ (GNSS 좌표계 투영 - gps_to_xy.py 단일화)"]
>         FR["🚀 file_reader/ (이종 계측데이터 통합 리더 + parsers/ 서브폴더)"]
>         CF["🎯 curve_fit/ (타이어 비선형 피팅 tire_curve/ SSOT)"]
>         M["📐 models/ (Pacejka MF, Bicycle Model 지배 수식 SSOT)"]
>         SP["📈 signal_process/ (fft, post_process 4대 전처리)"]
>         ST["📊 uno_statistics/ (순수 통계 & 측정불확도 uncertainty/)"]
>         GR["🎨 graphics/ (시각화 3대 서브폴더: plotters, controls, web)"]
>         UT["🛠️ utils/ (공통 유틸리티 통합 & logger/ 완성)"]
>         AI["🤖 ai/ (최적화 모델 & 피팅)"]
>         DB["🗄️ database/ (DW / PLM 연동)"]
>         SC["❄️ snow_condition/ (노면 환경 & ML 보정)"]
>     end
> ```

### 📖 unoUtil 12대 도메인 지식 사전 (Engineering Dictionaries Hub)

> [!NOTE] 💡 도메인 지식 사전 (Domain Engineering Guide)
> 각 사전 문서는 **설계 철학, 아키텍처, 데이터 파이프라인, 실전 워크플로우 템플릿, 트러블슈팅 노하우**를 완비하고 있으며, 세부 수식 및 이론은 `04_Resources` 영구 지식 노트로 연결됩니다.

| 도메인 | 지식 사전 (Obsidian SSOT) | 핵심 아키텍처 및 역할 | 연계 공학 리소스 (04_Resources) |
| :---: | :--- | :--- | :--- |
| **🏎️ vehicle/acc_brk** | [[vt_acc_brk_사전\|가감속/제동 사전]] | 가감속/제동 동역학, 콘트롤 타이어 선형 보간, 시작점 자동 검출 | [[30_실차_가감속_성능변화_분석_및_보정_시스템\|실차 가감속 백서]] |
| **❄️ snow_condition** | [[snow_condition_사전\|스노우 환경 사전]] | 3D 노면 공간 보간, 1-Run 시공간 결합, 머신러닝 차분 환경 보정 | [[31_스노우_노면_디지털트윈_및_제동성능_보정_위키\|스노우 디지털트윈]] |
| **🎯 curve_fit** | [[curve_fit_사전\|커브 피팅 사전]] | 3계층 메타 추정기, 에르미트 블렌딩 합성, 타이어 비선형 피팅 | [[40_비선형_회귀_메타_추정기_및_에르미트_블렌딩_아키텍처\|메타 추정기]] |
| **🚀 file_reader** | [[file_reader_사전\|계측 데이터 리더 사전]] | VBOX, VBB, Dewesoft, CSV 이기종 통합 리더 및 표준 채널 정규화 | [[24_유노유틸_파일리더_표준채널명\|표준 채널 명세서]] |
| **📶 signal_process** | [[signal_process_사전\|신호처리 사전]] | Zero-Phase 필터, 1D 웨이블렛 디노이징, 가감속 속도 구간 분할 | [[10_Zero_Phase_필터링_및_위상지연_극복_공학\|Zero-Phase 필터]] |
| **🎨 graphics** | [[graphics_사전\|그래픽스 시각화 사전]] | 비차단(Non-blocking) 고속 렌더링, 표준 테마, GUI 커서 컨트롤 | [[50_Matplotlib_시각화_무중단_개발_표준\|시각화 무중단 표준]] |
| **📐 models** | [[models_사전\|공학 수식 모델 사전]] | Pacejka MF, 2-DoF 평면 자전거 모델 순수 지배 수식 SSOT | [[12_차량_시스템_제동성능과_마찰계수_상관관계\|Pacejka 수식]] |
| **📊 statistics** | [[uncertainty_사전\|측정불확도 사전]] | ISO GUM 측정불확도 자동 평가 엔진, 자유도 및 파레토 분석 | [[10_측정불확도_완벽_이론_및_수학적_유도_가이드\|측정불확도 이론]] |
| **🛠️ utils / logger** | [[logger_사전\|로거 및 유틸 사전]] | 싱글톤 멀티 스트림 로거(`LOGGER`), 깜빡임 없는 프로그레스 바 | [[20_엔터프라이즈_계층형_로깅_및_무중단_시각화_패턴\|계층형 로깅]] |
| **🛰️ gps** | [[gps_사전\|GPS 측지 좌표 사전]] | WGS84 지구 타원체 평면 직각 데카르트(XY, m) 정밀 투영 엔진 | [[20_VBOX_계측_데이터_규격_및_GPS좌표계\|VBOX GPS 규격]] |
| **🗄️ database** | [[database_사전\|사내 DB 연동 사전]] | 사내 PLM/DW 연동, 의뢰번호 기반 타이어 스펙 자동 병합 | [[10_회사_DB_사용_매뉴얼\|회사 DB 매뉴얼]] |
| **🤖 ai** | [[ai_사전\|인공지능 최적화 사전]] | 베이지안/그리드 목적함수 최소화(`fit_minimize`), 신경망 피팅 | [[32_서포트_벡터_머신_및_회귀(SVM_SVR)_원리와_하이퍼파라미터_가이드\|SVR 가이드]] |

---

## 🏎️ 3. vehicle 동역학 & 가감속/제동 (acc_brk) 도메인

> [!NOTE]- 🏎️ vehicle 및 acc_brk 모듈 소스 코드 목록 [클릭하여 펼치기]
> | 모듈 / 서브패키지 | 핵심 기능 및 역할 | 소스 코드 (Repo) |
> | :--- | :--- | :---: |
> | **`VehicleDynamic`** | 실차 센서 장착점 ➔ 차량 무게중심(CG) 운동역학 변환 및 롤/피치 보정 | [`vehicle_dynamic.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle/vehicle_dynamic.py) |
> | **`hndl_test`** | 실차 조종안정성(Handling) 계측 데이터 분석 및 요레이트/횡가속도 산출 | [`hndl_test.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle/hndl_test.py) |
> | **`test_infor_res`** | 평가 정보(`TestInformation`) 및 결과(`TestResult`) 메타데이터 컨테이너 | [`test_infor_res.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle/test_infor_res.py) |
> | **`analysis_test_data`**| 제동 및 가속 성능 종합 통계 분석 및 평가 간 비교 엔진 | [`analysis_test_data.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle/analysis_test_data.py) |
> | **`vt_acc_brk`** | 가감속/제동 자동화 파이프라인 마스터 오케스트레이터 (`cf_*` 3계층 패스스루, 표준 네이밍: [[50_vt_acc_brk_표준_네이밍_규칙_및_저장_구조|표준 네이밍 룰]], 1:1 매뉴얼: [`vt_acc_brk.md`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle/acc_brk/vt_acc_brk.md)) | [`vt_acc_brk.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle/acc_brk/vt_acc_brk.py) |
> | **`vt_acc_brk_tire`** | 단일 타이어 동역학 분석, Wavelet 가속도 복원, 7대 서브 분석기(`curve_fit` 내장) 및 원천 데이터(`tire.df`) 시험 라벨링 | [`vt_acc_brk_tire.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle/acc_brk/vt_acc_brk_tire.py) |
> | **`vt_acc_brk_project`**| 다중 타이어 취합, 콘트롤 타이어 시계열 선형 보간 및 `curve_fit` 보정 지수(`index_cf_*`) 산출 엔진 | [`vt_acc_brk_project.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle/acc_brk/vt_acc_brk_project.py) |
> | **`correct`** | 시험 환경(온도, 노면) 프로파일(`correct_factor_basic`), 콘트롤 타이어 시계열 성능 지수 보정 및 `curve_fit` 게인($G_i$) 동기화 (`Correct`) | [`correct.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle/acc_brk/correct.py) |
> | **`base_memory`** | 대용량 실차 시계열 데이터 초고속 인메모리 관리 및 슬림 피클링 (`BaseMemory`) | [`base_memory.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle/acc_brk/base_memory.py) |
> | **`func_acc_brk`** | 가감속/제동 13대 핵심 동역학·신호처리·슬립·수막·응답성 계산 함수군 | [`func_acc_brk.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle/acc_brk/func_acc_brk.py) |
> | **`analyzers` (6대 서브) + `curve_fit`**| 가속대역, 감속응답, 슬립속도PDF, Mu-Drop, 왜도, 구간속도분할 및 Magic Formula 커브 피팅(`TireCurve`) 7대 전문 서브 분석기 | [`analyzers/`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle/acc_brk/analyzers/) |
> | **`plotter_tire` / `plotter_project`** | 단일 타이어 9대 분석 차트(`PlotterTire`: `curve_fit`, `curve_fit_detail` 포함) 및 프로젝트 9대 비교 플로터(`PlotterProject`: `compare_curve_fit` 포함) | [`plotter_tire.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle/acc_brk/plotter_tire.py) · [`plotter_project.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle/acc_brk/plotter_project.py) |

---

## 🚀 4. file_reader 이기종 계측 데이터 리더 도메인

> [!NOTE]- 🚀 file_reader 파서 및 리더 모듈 목록 [클릭하여 펼치기]
> | 모듈 / 서브패키지 | 핵심 기능 및 역할 | 소스 코드 (Repo) |
> | :--- | :--- | :---: |
> | **`file_data_reader`** | VBox(`.vbo`), Dewesoft(`.dwd`), RaceLogic(`.vbb`), 텍스트 이기종 자동 판별 통합 리더 | [`file_data_reader.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/file_reader/file_data_reader.py) |
> | **`parsers` (6대 서브)** | `base_parser`, `vbo_parser`, `vbb_parser`, `dwd_parser`, `text_parser`, `header_finder` 지능형 엔진 | [`parsers/`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/file_reader/parsers/) |
> | **`datetime_helper`** | GPS 시각 동기화, 7단계+3중 안전망(동계 도메인 게이트·장비 시그니처·30일 mtime 가드) 날짜 판정 및 시계열 정규화 | [`datetime_helper.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/file_reader/datetime_helper.py) |
> | **`standard_channel_pattern`** | 사내 계측 채널명 정규표현식 매핑 사전 및 표준 칼럼 변환 | [`standard_channel_pattern.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/file_reader/standard_channel_pattern.py) |
> | **`DWDataReader` / `vbbTopython`** | Dewesoft C-DLL 바인딩 및 VBB 바이너리 파이썬 변환 엔진 | [`DWDataReader/`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/file_reader/DWDataReader_v5_0_8/) · [`vbbTopython/`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/file_reader/vbbTopython/) |

---

## 🎨 5. graphics 실차 시각화 및 인터랙션 도메인

> [!NOTE]- 🎨 graphics 플로터, 컨트롤러, 웹 시각화 모듈 목록 [클릭하여 펼치기]
> | 모듈 / 서브패키지 | 핵심 기능 및 역할 | 소스 코드 (Repo) |
> | :--- | :--- | :---: |
> | **`plotter`** | Matplotlib 기반 실차 주행 시계열 표준 플로팅 엔진 (비차단 원칙) | [`plotter.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/graphics/plotters/plotter.py) |
> | **`pair_plot`** | 다변량 센서 신호 상관관계 매트릭스 시각화 | [`pair_plot.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/graphics/plotters/pair_plot.py) |
> | **`surface_3d`** | 노면 높이 및 3차원 공간 특성 서피스 렌더러 | [`surface_3d.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/graphics/plotters/surface_3d.py) |
> | **`text_offset`** | 차트 주석 텍스트 겹침 방지 자동 오프셋 계산기 | [`text_offset.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/graphics/plotters/text_offset.py) |
> | **`cursor_mode` / `range_selector`** | GUI 인터랙티브 마우스 커서 측정 및 특정 구간 드래그 선택기 | [`controls/`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/graphics/controls/) |
> | **`plotly_tools`** | 웹 기반 반응형 Plotly 대화형 차트 생성 툴킷 | [`plotly_tools.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/graphics/web/plotly_tools.py) |

---

## 🎯 6. curve_fit 커브 피팅 및 타이어 곡선 도메인

> 📑 **curve_fit 심층 검증 보고서 허브 (MOC)**: [[00_curve_fit_보고서_통합_색인|🎯 20_curve_fit 보고서 통합 색인 바로가기]]
> • [[10_휠속도_시간지연_보정_및_타이어_커브피팅_종합보고서|10. 휠 속도 시간 지연(Time-Delay) 물리 보정 및 커브 피팅 종합 보고서]]
> • [[20_타이어_커브피팅_전면_개발스토리_및_공학검증보고서|20. 타이어 커브 피팅 전면 고도화 개발 스토리 및 물리/공학 검증 종합 보고서]]
> • [[30_가속_시험_타이어_커브피팅_검증보고서|30. 가속(ACC) 시험 타이어 커브 피팅 검증 및 피팅 결과 보고서]]
> • [[40_NoABS_실측_VBB_타이어_커브피팅_검증보고서|40. unoUtil No-ABS 실측 VBB 타이어 커브 피팅 3대 추정기 검증 보고서]]

> [!NOTE]- 🎯 curve_fit 타이어 특성 피팅 및 범용 추정기 모듈 목록 [클릭하여 펼치기]
> | 모듈 / 서브패키지 | 핵심 기능 및 역할 | 소스 코드 (Repo) |
> | :--- | :--- | :---: |
> | **`tire_curve` (`TireCurve` v4.5)** | **타이어 종/횡방향 비선형 특성 곡선 피팅 총괄 클래스 (`VTAccBrkTire.curve_fit` 공식 서브 분석기, 6대 최적화 엔진, 구동방식 기반 슬립 축 자동 선택, 콘트롤 보정 동기화 SSOT Facade)** | [`cf_tire.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/curve_fit/tire_curve/cf_tire.py) |
> | **`least_squares_estimator`** | Scipy 비선형 최소자승 가중치/Huber loss 범용 추정기 (`LeastSquaresEstimator`) | [`least_squares_estimator.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/curve_fit/estimators/least_squares_estimator.py) |
> | **`optimize_estimator`** | Scipy minimize 및 Bayesian 최적화 범용 추정기 (`OptimizeEstimator`) | [`optimize_estimator.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/curve_fit/estimators/optimize_estimator.py) |
> | **`combiner_estimator`** | 모델 주입 기반 다구간 스플라인 결합, 저슬립 가중치·양수 기울기 클램핑 및 원점 `(0, 0)` 직선 보정 파이프라인 (`CombinerEstimator` v4.1) | [`combiner_estimator.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/curve_fit/estimators/combiner_estimator/combiner_estimator.py) |

---

## 📐 7. models 공학 지배 수식 도메인

> [!NOTE]- 📐 models 순수 공학 수학 지배 방정식 및 신경망 모듈 목록 [클릭하여 펼치기]
> | 모듈 / 서브패키지 | 핵심 기능 및 역할 | 소스 코드 (Repo) |
> | :--- | :--- | :---: |
> | **`magic_formula`** | Pacejka Magic Formula 4파라미터 및 2단계 강성 구속(`calc_constrained_magic_formula`, $B=K/(C\cdot D)$) 비선형 모델 수식 (SSOT) | [`magic_formula.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/models/mathematical/magic_formula.py) |
> | **`bicycle_model`** | 2자유도 차량 평면 횡방향 자전거 모델 수식 시뮬레이션 (`BicycleModel`) | [`bicycle_model.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/models/mathematical/bicycle_model.py) |
> | **`fit_nn`** | PyTorch / Scikit-Learn 기반 차량 동역학 신경망 모델러 | [`fit_nn.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/models/neural_net/fit_nn.py) |

---

## 📶 8. signal_process 신호 후처리 및 정제 도메인

> [!NOTE]- 📶 post_process 4대 필터 및 FFT 모듈 목록 [클릭하여 펼치기]
> | 모듈 / 서브패키지 | 핵심 기능 및 역할 | 소스 코드 (Repo) |
> | :--- | :--- | :---: |
> | **`filters`** | Zero-Phase 이동평균 필터 및 Butterworth 저역통과 필터 | [`filters.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/signal_process/post_process/filters.py) |
> | **`resample`** | 비수치 메타데이터 손실 없는 시계열 고속 리샘플링 | [`resample.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/signal_process/post_process/resample.py) |
| **`outliers`** | 이상치 자동 검출 및 연속 결측 구간 정제 | [`outliers.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/signal_process/post_process/outliers.py) |
| **`segments`** | 가감속 속도 구간 분할(Speed Segments), 단조성 검사 및 정밀 시간 보간 엔진 | [`segments.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/signal_process/post_process/segments.py) |
| **`scaler`** | MinMax, Standard, Robust 시계열 신호 정규화 | [`scaler.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/signal_process/post_process/scaler.py) |
> | **`extended_isolation_forest`** | 고차원 센서 이상치 탐지를 위한 EIF 알고리즘 | [`extended_isolation_forest.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/signal_process/post_process/extended_isolation_forest.py) |
> | **`find_fft` / `single_track` / `tf_estimate`**| 주파수 스펙트럼 분석, 단일 트랙 FFT, 전달함수(TF) 추정 | [`fft/`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/signal_process/fft/) |

---

## 🛠️ 9. utils & logger 공통 유틸리티 도메인

> [!NOTE]- 🛠️ utils 및 로깅 모듈 목록 [클릭하여 펼치기]
> | 모듈 / 서브패키지 | 핵심 기능 및 역할 | 소스 코드 (Repo) |
> | :--- | :--- | :---: |
> | **`logger`** | 사내 프레임워크 표준 계층형 로깅 엔진 (Print 전면 퇴출) | [`logger.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/logger/logger.py) |
> | **`progress_bar`** | 콘솔 렌더링 칼정렬 및 깜빡임 없는 프로그레스 바 | [`progress_bar.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/logger/progress_bar.py) |
> | **`console_style` / `styles`** | ANSI 컬러 터미널 출력 포맷터 | [`console_style.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/utils/console_style.py) · [`styles.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/logger/styles.py) |
> | **`dataframe_utils`** | 고속 판다스 조작, 데이터프레임 무결성 검증 유틸리티 | [`dataframe_utils.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/utils/dataframe_utils.py) |
> | **`excel`** | OpenPyXL 기반 대용량 서식화 엑셀 시트 자동 생성기 | [`excel.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/utils/excel.py) |
> | **`files`** | 재귀적 파일 탐색, 디렉터리 안전 생성/삭제 유틸리티 | [`files.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/utils/files.py) |
> | **`weather`** | 평가 일자/위치 기반 기상 데이터 수집 및 보간 | [`weather.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/utils/weather.py) |
> | **`window_handler` / `window_msg`** | 윈도우 OS 시스템 알림창 및 팝업 메시지 제어 | [`window_handler.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/logger/window_handler.py) · [`window_msg.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/utils/window_msg.py) |

---

## 🤖 10. ai/database/statistics/gps 기타 도메인

> [!NOTE]- 🤖 AI, DB, 통계, GPS 모듈 목록 [클릭하여 펼치기]
> | 모듈 / 서브패키지 | 핵심 기능 및 역할 | 소스 코드 (Repo) |
> | :--- | :--- | :---: |
> | **`ai` (4대 모듈)** | 비선형 모델, 종방향 가속도 피팅, 최적화 모델, 딥러닝 피팅 | [`ai/`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/ai/) |
> | **`database` (5대 쿼리 & spec)** | PLM/DW 연동, 의뢰번호 기반 규격 스펙 결합 (`connect_spec_with_req_set`) | [`database/`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/database/) |
> | **`uno_statistics` / `uncertainty`**| 기술통계 요약(`summary`) 및 ISO GUM 표준 측정불확도 자동 평가 엔진 | [`uno_statistics/`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/uno_statistics/) |
> | **`gps` (`gps_to_xy`)** | WGS84 위경도 좌표를 평면 직각 데카르트 좌표계(XY)로 투영 | [`gps_to_xy.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/gps/gps_to_xy.py) |

---


---

## ❄️ 11. snow_condition 노면 환경 & 머신러닝 보정 도메인

> [!NOTE]- ❄️ snow_condition 9대 핵심 모듈 목록 [클릭하여 펼치기]
> | 모듈명 | 핵심 클래스 / 역할 | 소스 코드 (Repo) |
> | :--- | :--- | :---: |
> | **`schema`** | SSOT 47대 표준 컬럼 및 DataFrame 정규화 단일 관문 (`harmonize_snow_dataframe`) | [`schema.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/snow_condition/schema.py) |
> | **`preprocessor`** | 로컬 노면 계측 데이터 자동 수집 및 시간-공간 1차 정제 엔진 | [`preprocessor.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/snow_condition/preprocessor.py) |
> | **`physics`** | Sonntag 빙점하 수증기압, 과포화도, 타이어 접지압 물리 역학 수식 | [`physics.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/snow_condition/physics.py) |
> | **`surface_interpolator`** | 센서 좌표계 복원, 3D 시공간 격자 보간 및 시험 묶음 결합 (`SnowSurfaceInterpolator`) | [`surface_interpolator.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/snow_condition/surface_interpolator.py) |
> | **`surface_animator`** | Plotly 4D 시공간 인터랙티브 노면 환경 애니메이션 (`SurfaceAnimator`) | [`surface_animator.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/snow_condition/surface_animator.py) |
> | **`correction_model`** | 6대 머신러닝 회귀 학습 및 데이터 보정 코어 엔진 (`SnowCorrectionModel`) | [`correction_model.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/snow_condition/correction_model.py) |
> | **`slope_model`** | 노면 경사도 수치 지형 모델링 및 중력 분력 제동 보정 엔진 (`SnowSlopeModel`) | [`slope_model.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/snow_condition/slope_model.py) |
> | **`correction_validator`** | 1st vs 2nd 대조표 산출, 엑셀 내보내기, 오차 감소율 통계 (`SnowCorrectionValidator`) | [`correction_validator.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/snow_condition/correction_validator.py) |
> | **`correction_plotter`** | 다형성 비교 플롯, 오버플랏 산점도, 2D 등고선 보정 맵 (`SnowCorrectionPlotter`) | [`correction_plotter.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/snow_condition/correction_plotter.py) |
> 
> ```mermaid
> classDiagram
>     direction TB
>     class SnowCorrectionModel {
>         +model_type: str
>         +train(df_train)
>         +predict_diff(df_cur, df_ref)
>         +correct_dataframe(df)
>         +validator: SnowCorrectionValidator
>         +plot: SnowCorrectionPlotter
>     }
>     class SnowCorrectionValidator {
>         +calc_corrected_comparison_table(df_test)
>         +evaluate_restoration_metrics(df_comp)
>     }
>     class SnowCorrectionPlotter {
>         +plot_delta_prediction_scatter()
>         +plot_scatter_restoration()
>         +plot_correction_map()
>         +plot_tire_subsets_comparison(req_no, tire_set)
>     }
>     SnowCorrectionModel *-- SnowCorrectionValidator : Composition (self.validator)
>     SnowCorrectionModel *-- SnowCorrectionPlotter : Composition (self.plot)
> ```

---

## 📖 12. 사용자 매뉴얼 및 엔지니어링 표준

> [!NOTE]- 📘 사내 매뉴얼 및 코딩 표준 링크 [클릭하여 펼치기]
> * 📖 **[[90_ACCBRK_사용자매뉴얼|VT_ACCBRK 실무 사용자 매뉴얼]]**: 3단계 분석 공정 및 함수별 매개변수 가이드
> * 📘 **[[D:\00_obsidian\.agents\rules\PYTHON_CODE_AGENT.md|PYTHON_CODE_AGENT.md (글로벌 파이썬 마스터 규칙)]]**
> * 🛑 **[[00_제동_기술_통합_색인|차량 제동(Braking) 기술 위키 통합 색인]]**
> * 🏠 **[[04_Resources/00_지식_위키_통합_색인|04_Resources 지식 위키 중앙 대문]]**

---

## 📜 13. 버전 이력 및 주요 개발 현황 (Changelog)

### [2026-10-27] v3.68 - unoUtil v2.0 전면 레거시 소멸, 절대 참조 100% 전환, 모듈 내부 별칭 전수 소멸 및 SSOT 단일화 완결
* **공식 종합 보고서**: [[01_unoUtil_v2_전면_레거시_소멸_및_SSOT_단일화_완결_보고서]]
* **전 패키지 상대 참조 100% 절대 참조(`unoUtil.*`) 전환**:
  - 패키지 내 33개 파일의 상대 참조(`from .`, `import .`)를 전수 발굴하여 `from unoUtil.<도메인>.<모듈>` 완전한 절대 참조로 치환 완료. 모듈 단위 독자 실행(`__main__`) 및 단위 테스트 완벽 보장.
* **4대 대원칙 기반 과거 레거시 폴더/파일 전수 영구 소멸**:
  - 내용물 없는 빈 `legacy/` 폴더 7곳(`ai`, `database`, `file_reader`, `logger`, `signal_process/fft`, `signal_process/post_process`, `vehicle`) 완전 삭제.
  - 과도기 브릿지 파일 4종(`ai/dynamic_model`, `ai/fit_nn`, `ai/fit_minimize_optimization`, `curve_fit/tire_curve/fit_least_squares`) 및 매뉴얼 영구 삭제.
  - 잔여 껍데기 폴더 `signal_process/curve_fit` 및 `CurveCombiner` 완전 삭제 $	o$ 커브 피팅은 최상위 공식 도메인 `unoUtil.curve_fit`으로 단일화.
  - 외부 CLI 리다이렉션 실수로 생성되었던 루트 임시 파일 `1`, `.pytest_cache/`, `unoUtil.egg-info/`, `resample.py.bak` 완전 삭제 및 `.gitignore` 등록.
* **example/ 디렉토리 다이어트 및 표준 검증 도구 확립**:
  - 특정 PC 로컬 경로 하드코딩 일회성 연구 스크립트 5종 및 `fig/` 대용량 차트 이미지 디렉토리 전수 삭제 (저장소 다이어트 달성).
  - v2 순수 표준 무결성 전수 검증 스크립트(`test_structure_integrity.py`), PEP 8 규격 검증(`test_pep8_all.py`), 독립형 데모(`example_scan_dir_progressbar.py`) 3종 보존 및 표준화.
* **32개 모듈 내부 과거 호환용 레거시 별칭(Alias = RealName) 전수 소멸**:
  - 모듈 하단에 잔존하던 구버전 별칭(`Infor_Vehicle`, `VD_*` 8종, `SP_CurveFit_*` 4종, `CurveCombiner`, `MinimizeEstimator`, `SP_Resample`, `TireMagicFormula`, `MagicFormula`, `UnitYawRate` 등) 전면 삭제 및 단일 진실 공급원(SSOT) 확립.
  - `VehicleDynamic` 및 `FileDataReader`의 중복 전역 함수 바인딩(`align_coordinate = VehicleDynamic.align_coordinate`, `scan_dir = FileDataReader.scan_dir` 등)을 전면 삭제하고 클래스 메서드로 단일화.
* **최상위 루트 `unoUtil/__init__.py` 250줄 슬림화**:
  - 과거 메타패스 가상 리다이렉터 엔진 및 가상 모듈 바인딩 코드를 전면 삭제하고, 12대 공식 도메인과 핵심 클래스만 담긴 순수하고 가벼운 표준 Facade(180줄)로 재구축.
* **비매뉴얼 보고서 볼트 안전 이관 (1:1 코드 매뉴얼 격리 헌장 준수)**:
  - 19KB 백서(`tire_curve_pipeline_and_real_data_issues.md`)를 볼트 `20_curve_fit/`에 `25_실차_계측데이터_태생적_문제점과_8단계_통합파이프라인_백서.md`로 신규 이관 및 색인 연계.
  - 볼트 기보존 중복 보고서 2종 코드 폴더 삭제. 패키지 내 모든 81개 마크다운 문서는 100% 모듈 1:1 기술 매뉴얼만 격리 보존 달성.


### [2026-10-21] v3.60 - curve_fit 4대 보고서 볼트 이관, PlotterProject compare_curve_fit_pdf 더블 Y축 신설 및 tire_curve/explain 모듈 허브 완결
- **옵시디언 볼트 `20_curve_fit` 지식 허브 구축 및 4대 기술 보고서 이관**:
  - `D:\00_obsidian\02_Projects\회사_업무\20_unoUtil_모듈개발\20_curve_fit\` 폴더를 신설하고 마스터 색인 MOC([[00_curve_fit_보고서_통합_색인]]) 구축.
  - 4대 심층 보고서 이관 완결:
    1. [[10_휠속도_시간지연_보정_및_타이어_커브피팅_종합보고서]] (WSS ZOH 스텝 홀드 $\Delta t_{\text{step}}/2$ 및 CAN 지연 결합 규명, 비구동 후륜 Bias $0.00\text{ km/h}$ 완전 소거 검증)
    2. [[20_타이어_커브피팅_전면_개발스토리_및_공학검증보고서]] (4대 랜드마크 위상 정합, 구속형 MF, 2단계 분리 신호처리, $20\sim 200\text{Hz}$ 샘플링 불변성)
    3. [[30_가속_시험_타이어_커브피팅_검증보고서]] (스노우 가속 run1/run2 실측 데이터셋 검증)
    4. [[40_NoABS_실측_VBB_타이어_커브피팅_검증보고서]] (이발로 No-ABS 3대 추정기 성능 비교)
  - 36종의 고해상도 분석 그래프를 `_attachments/10_회사_업무/curve_fit/`로 전량 이관하고 옵시디언 전용 위키링크(`![[_attachments/...|900]]`)로 100% 변환.
- **`PlotterProject.compare_curve_fit_pdf` 더블 Y축 복합 비교 시각화 신설 (`plotter_project.py`, `plotter_project.md`)**:
  - **더블 Y축 연출**: 좌측 메인 축에 Magic Formula 타이어 마찰 특성 곡선 + 최대 마찰 피크점 마커($\mu_{\text{peak}}, s_{\text{peak}}$), 우측 보조 축(`twinx`)에 실시간 주행 휠 슬립률 가우시안 확률 밀도(PDF, 반투명 면적 채우기 `alpha=0.22` + 보조 점선)를 오버레이.
  - **다중 콘트롤 타이어(C1, C2...) 정규화 합성**: 커브 피팅 곡선 평균화와 함께 슬립률 PDF 역시 사다리꼴 적분(NumPy 2.0+ `trapezoid` 호환)을 통해 **적분 면적이 정확히 1.0이 되도록 정규화 합성(Normalized Averaging)**하여 단 하나의 대표 콘트롤 객체로 표현.
  - **최상위 배치 파이프라인 자동 연동**: `pjt.plot.all()` 및 `vt_acc_brk()` 일괄 출력 차트 목록에 17번째 공식 차트(`17_Curve_Fit_PDF`)로 등록 완료 (`BMW320d_ADAC_Dry` 실측 VBB 데이터로 142KB 고해상도 차트 정상 생성 검증).
- **`tire_curve/explain` 1파일 1그래프 공학 시각화 모듈 허브(9종) 구축**:
  - `unoUtil/curve_fit/tire_curve/explain/` 폴더를 신설하고 보고서 수록 전체 핵심 공학 차트를 1파일 1그래프 원칙으로 개별 모듈화:
    1. `fig1_brk_onset_recovery.py`: 속도 컷오프 저슬립 소실 vs $L_0$ 역추적 복원
    2. `fig2_phase_warping_timing_jitter.py`: 런별 타이밍 지터 vs 위상 정렬 $K_{\text{pk}}$ 추출
    3. `fig3_method_comparison_brk.py`: 4대 커브피팅 방법론 정량 비교
    4. `fig4_detail_diagnostic_brk.py`: 제동 3색 분리 정밀 진단 플롯 (`detail=True`)
    5. `fig5_acc_noise_and_split_filtering.py`: 가속 VBOX 미분 노이즈 vs 2단계 분리 신호처리
    6. `fig6_detail_diagnostic_acc.py`: 가속 정밀 진단 플롯 (`detail=True`)
    7. `fig7_surface_drift_correction.py`: 노면 드리프트 보정 (비보정 vs 단일 Control)
    8. `fig8_sr_dynamic_scaling_invariance.py`: $20\sim 200\text{Hz}$ 샘플링 주파수 동적 스케일링 불변성
    9. `fig9_transient_landmark_deep_dive.py`: [사용자 통찰 심층 가시화] $L0\to L1\to L2\to L3$ 타이밍 지터 정량화 및 4단계 과도 분리·본체 피팅 통합 가시화 (볼트 보고서 4.3절 수록 완료)
    10. `run_all.py` 및 `common_data.py`: 공통 데이터 로더 및 원클릭 일괄 러너 (9개 스크립트 100% PASS 검증)

### [2026-10-20] v3.49 - 가감속/제동(`vt_acc_brk`) 과도 응답성 분석기(`calc_response`) 유효 응답 및 Rising 구간 추출 4대 구조적 결함 해결
- **저마찰 노면(Snow/Ice 등) 임계값 비례 스케일링 및 역전 원천 방지 (`func_acc_brk.py`)**:
  - 제동(`[-0.5, -0.2]`) 및 가속(`[0.2, 0.5]`) 기본 목표 가감속도에 미달하는 저마찰 노면에서 종료 임계값(`threshold_end`)이 완화될 때, 시작 임계값(`threshold_start`)도 완화 비율(`scale_ratio = threshold_end / target_limit`)에 맞추어 자동 비례 축소되도록 개선하여 시작점-종료점 임계값 역전 및 구간 탈락을 원천 해결.
- **`pre_sec` 구간 기저선(Baseline) 클리핑 정상화 및 폴백 방어선**:
  - `pre_sec`(기본 2.0초) 구간 맨 앞의 첫 번째 노이즈(`index[0]`)를 잘라내던 기존 오류를 수정하여, 유효 세션 시작점(`df_group.index[0]`) 직전의 마지막 영점/기저선(`index[-1]`) 이후부터 탐색하도록 정합하고 기저선 미교차 시 극값 폴백(`idxmax`/`idxmin`) 방어선 탑재.
- **단일 불량 차수로 인한 전체 분석 조기 종료(`return dict_result`) 버그 수정**:
  - 다중 차수(`EffNum`) 및 휠 채널 반복 루프 중 특정 1개 차수가 임계치 미달이더라도 전체 결과를 빈 값으로 덮어쓰며 즉시 반환하지 않고 해당 차수만 `continue`로 스킵하여 정상 차수들의 분석 결과를 온전히 보존.
- **초기 Rising 구간 탐색 시 전역 노이즈 피크 오탐 방지**:
  - 2차 미분(`d2_vel`) 극값 탐색 범위를 전체 주행 구간이 아닌 초기 과도 응답 구간(`idx_diff_vel_start` ~ `idx_diff_vel_end + 1.5s`)으로 한정하여 ABS 중후반부나 정지 직전 피칭 노이즈에 의한 Rising 구간 오탐을 원천 차단하고, `func_acc_brk.md` 1:1 매뉴얼 동기화 완료.

### [2026-10-19] v3.48 - 가감속/제동(`vt_acc_brk`) 7번째 공식 서브 분석기로서의 `curve_fit`(`TireCurve` v4.5) 전면 통합, 구동방식(`TestVehicleLayout`) 기반 슬립 축 자동 선택, 콘트롤 보정 게인($G_i$) 동기화 및 다중 타이어 비교 플로터(`compare_curve_fit`) 완결
- **`VTAccBrkTire.curve_fit` 공식 서브 분석기 편입 및 `fit()` vs `predict()` 책임 분리 (`cf_tire.py` v4.5, `vt_acc_brk_tire.py`)**:
  - `VTAccBrkTire.run()` 실행 시 7번째 서브 분석기로 `self.curve_fit = TireCurve(self, ...)`이 자동 기동되며, 요약(`summary.df`)에 `cf_B`~`cf_Sv`, `cf_peak_mu`, `cf_peak_slip`, `cf_stiffness`, `cf_r_squared`, `cf_rmse`, `cf_method`를 자동 산출.
  - `fit(...)`은 6대 최적화 메서드(`'robust'`, `'binning'`, `'two_stage'`, `'ransac'`, `'lsq'`, `'custom'`)로 MF 파라미터를 추정하고, `predict(x=None, interval=0.005)`는 기본 $[0.0, 1.0]$ 구간 또는 사용자 지정 구간(`[start, end]`)·배열(`np.ndarray`)에 대한 예측 곡선(`df[['Slip', 'Acc']]`)을 산출.
- **휠스피드 부재 시 자동 Skip 및 시험 모드(`brk`/`acc`)·차량 구동방식(`TestVehicleLayout`) 연동 슬립 축 자동 결정**:
  - 휠스피드/슬립 채널이 없는 계측 데이터는 에러 없이 `is_fitted = False`로 자동 Skip.
  - 제동(`brk`)은 전륜축(`FL`/`FR` 중 유효 채널 평균)을 기본 적용하고, 가속(`acc`)은 `tire.infor.result` 내 `TestVehicleLayout`이 `RWD`/`FR`/`MR`/`RR`이면 후륜축(`RL`/`RR`), `AWD`/`4WD`이면 4륜 전체(`all`), `FWD`/미지정 시 전륜축(`front`)을 자동 선택 (`col_curve_fit_wheelslip` 명시 지정 시 최우선 오버라이드).
- **프로젝트 콘트롤 타이어 보정(`Correct.run`) 동기화 및 요약 지표(`corr_cf_*`, `index_cf_*`) 산출 (`correct.py`, `vt_acc_brk_project.py`)**:
  - 별도 재피팅 없이 콘트롤 타이어 선형 보간 게인($G_i = \text{corr\_Acc} / \text{mean\_Acc}$)을 각 타이어의 `curve_fit.df`(`corr_mean_Acc`, `corr_curve_Acc`), `df_raw`, `params`(`corr_D`, `corr_peak_mu`, `corr_stiffness`)에 동기화하고, 프로젝트 요약표에 `corr_cf_peak_mu`, `index_cf_peak_mu`, `corr_cf_stiffness`, `index_cf_stiffness`, `corr_cf_D`를 자동 산출.
- **단일 타이어(`PlotterTire`)·프로젝트(`PlotterProject`) 시각화 및 대표 래퍼(`vt_acc_brk`) 연동**:
  - `tire.plot.curve_fit(detail=False)`, `tire.plot.curve_fit_detail()` (6-패널 진단), `project.plot.compare_curve_fit(corr='mean', xlim=(0.0, 1.0), show_peak=True)` 신설 및 `vt_acc_brk()` 대표 함수에 `col_curve_fit_wheelslip`, `cf_method`, `cf_vel_range`, `cf_slip_range`, `cf_refine_start`, `cf_filter_transient` 3계층 분기 패스스루 완성.
  - 7대 모듈 Docstring 및 1:1 기술 매뉴얼(`cf_tire.md` v4.5, `vt_acc_brk*.md`, `correct.md`, `plotter_*.md`), 도메인 사전([[vt_acc_brk_사전]], [[curve_fit_사전]]) 및 영구 지식 위키([[30_실차_가감속_성능변화_분석_및_보정_시스템]]) 전수 동기화 완료.

### [2026-10-19] v3.47 - 스노우 노면·기상 환경 보정(`snow_condition`) 다중 스케일(`StandardScaler`) 자동 정규화 파이프라인(`correction_model.py`) 및 기상/노면 동적 등고선 플로터(`correction_plotter.py`) 고도화
- **다중 스케일 피처 자동 정규화 파이프라인 (`SnowCorrectionModel.train_models`)**:
  - 기온($\Delta T \in [-10, +13]^\circ\text{C}$, $\sigma \approx 4.9$) 및 상대습도($\Delta RH \in [-15, +9]\%$, $\sigma \approx 4.9$) 등 입력 인자 간 물리적 단위 스케일이 큰 조합($\max(\sigma_X) > 2.5$)이 입력될 경우, 거리 기반 `KNN Regressor`와 커널 기반 `SVR`에 `make_pipeline(StandardScaler(), ...)`을 자동 결합하고 `SVR` 무차원 유효 대역폭($\gamma_{\text{eff}} = 0.07 \times 1.28^2 \approx 0.1147$)을 주입.
  - 기존 노면 기본 조합(`[char_height, cd_test_ah]`, $\max(\sigma_X) \approx 1.54 \le 2.5$)에서는 원시 스케일을 그대로 유지하여 기존 기준선 수치를 100% 보존.
- **기상/노면 인자별 동적 등고선 축 스케일링 및 레이아웃 최적화 (`SnowCorrectionPlotter`)**:
  - `correction_map` 및 `correction_map_comparison(x_range=None, y_range=None)`에서 `char_height`, `cd_test_ah`, `cd_test_temp`, `cd_test_hum` 인자별 실제 차분 분포와 전용 여백(Margin)·눈금 간격(Step)·한글 물리 단위 라벨을 자동 적용하고, 우측 공통 컬러바와 서브플롯 타이틀 간 겹침을 원천 차단.
- **최신 DB(`3-1. df_combine_brk_surface_spec.pkl`) 기반 3종 보정 모델 전수 실증**:
  - `Case 1 [눌림량+절대습도]` (`VIF = 1.07`), `Case 2 [기온+절대습도]` (Sonntag 열역학 다중공선성 `VIF = 16.89` 규명), `Case 3 [기온+상대습도]` (`VIF = 2.53`, `Random Forest` 물리 제동거리 `0.495 m` [+43.6%] / 지수 `2.732 %p` [+20.6%]) 통합 비교 완결.

### [2026-10-19] v3.46 - 제동 초기 과도 응답 4-랜드마크(`L0~L3`) 분리·Snow Wedge 피팅(`TireCurve` v4.4), `CombinerEstimator` v4.1 및 VBO 날짜 파싱 3중 안전망(`datetime_helper`) 완결
- **제동 초기 과도 응답 4-랜드마크(`L0→L1→L2→L3`) 위상 정합 및 정상 상태(`L3~`) 본체 피팅 분리 (`cf_tire.py`)**:
  - `calc_brk_transient_landmarks`로 회차별 유압 시작(`L0`), 관성 데드존 종료(`L1`), 1차 마찰 피크(`L2`), 1차 ABS 감압 골짜기(`L3`)를 검출하고 피크-코드 강성($K_{\text{pk}} = \mu_{L2}/\kappa_{L2}$) 및 시간축 마찰 빌드업 속도($d\mu/dt$)를 산출.
  - 초반 기울기 추출에만 사용된 `L0~L3` 과도 루프 전체를 본체 피팅에서 배제(`filter_deadzone=True`, `filter_transient=True`)하고, 슬립 구간별 밀도 역가중치(`calc_bin_density_weights`) 및 고슬립 스노우 웻지(`enable_wedge=True`)를 결합하여 피팅 RMSE를 $18.5\% \sim 23.7\%$ 저감.
  - `compare_unfiltered=True` 옵션을 통해 제외 로우 데이터(`✕`/`△`) 마커 분리 표시 및 초기 과도 포함(파선) vs 제외(실선) 오버레이 비교 시각화 완성.
- **`CombinerEstimator` v4.1 및 2단계 강성 구속 Magic Formula (`combiner_estimator.py`, `magic_formula.py`)**:
  - `calc_constrained_magic_formula(x, C, D, E, K, Sh, Sv)` ($B = K / (C \cdot D)$) 등식 제약 수식 편입 및 `CombinerEstimator` 저슬립(`0.0~0.20`) 가중치(`wg=20`), `TrendLine` 양수 물리 기울기 클램핑(`[0.5, 25.0]`), 원점 `(0, 0)` 직선 확장 보정 완결.
- **VBO 계측 날짜 파싱 3중 안전망 구축 (`datetime_helper.py`)**:
  - 2-1단계 동계 시험 도메인 게이트(겨울철 11~4월 우선, 여름철 5~10월 배제), 2-2단계 장비 시그니처 판정(`VBox Touch` 미국식 `MM/DD` vs `[SessionData]`/`Exported` 유럽식 `DD/MM`), 6단계 `mtime` 30일 이내 제한을 탑재하여 17개 스노우 세션 날짜 왜곡 100% 종결.

### [2026-10-12] v3.22 - 옵시디언 볼트 슬림화(볼트 다이어트) 및 소스 코드 매뉴얼 격리 보존 원칙 (Code Manual Isolation Law) 확립
- **개별 1:1 모듈 매뉴얼(87종) 볼트 전면 퇴출 및 코드 저장소 SSOT 일원화**:
  - 파이썬 함수/클래스 단위의 저수준 기술 매뉴얼(`.md`) 87종을 옵시디언 볼트에서 완전 삭제하고, 소스 코드 저장소(`D:\uno\Python\Projects\unoUtil\`) 내부에 코드(`.py`)와 함께 영구 보존.
  - 옵시디언 볼트의 비대화 및 이중 동기화 부채를 원천 해소하고, 옵시디언 본연의 역할(마스터 MOC, 공학 이론, 종합 분석 보고서, 타임라인 관리)로 회귀.
- **마스터 MOC 허브 3열 인덱싱 로컬 코드 직결 리팩토링**:
  - 기존 옵시디언 내부 위키링크(`[[모듈명]]`)로 인한 깨진 링크 및 고아 노드 발생을 방지하고, 11대 도메인 87개 모듈의 실제 소스 파일(`file:///D:/uno/Python/Projects/unoUtil/...`)로 직접 연결되는 고속 하이퍼링크 체계 완비.
  - ❄️ snow_condition 도메인의 `preprocessor.py` 및 `slope_model.py` 누락 항목을 전면 보강하여 9대 핵심 모듈 체계 정립.
- **전역 거버넌스 헌장 4대 규칙집(SSOT) 개정 완료**:
  - `AGENTS.md` (제4장 ⑤항 신설 - 소스 코드 단위 저수준 매뉴얼 옵시디언 유입 금지)
  - `PYTHON_CODE_AGENT.md` (제5.1장 4항 개정 - 개별 코드 매뉴얼 격리 보존 원칙)
  - `code-audit-obsidian-docs/SKILL.md` (제2장 2항 개정 - 개별 코드 매뉴얼 격리 보존)
  - `obsidian-wiki-sync/SKILL.md` (제3장 3항 개정 - 저수준 매뉴얼 유입 원천 차단)

### [2026-10-12] v3.24 - 가감속/제동(vt_acc_brk) 및 파일리더(file_reader) 결함 감사 및 시간·슬립률 무결성 정상화
- **VBOX GPS 시간 파싱 및 타임존 오프셋 핵심 버그 해결 (`datetime_helper.py`, `file_data_reader.py`)**:
  - `07_C2.VBO` 파일의 GPS 원시 시각 `053648.720` (UTC 05:36:48) 파싱 시, Pandas float 변환으로 인한 앞자리 0 탈락(`53648.72`) 상태에서 `zfill(6)` 없이 앞 2자리를 잘라 53시 $\ge$ 24로 인식하여 VBOX 포맷 판정에서 탈락하던 치명적 결함 수정.
  - VBOX 판정 탈락 후 초(Seconds since midnight) 단위로 오판되어 +9시간 가산 후 23시 54분이라는 엉뚱한 심야 시각이 산출되던 문제를 `str_val.zfill(6)` 의무화 및 VBOX 고유 컬럼 감지로 원천 해결 (UTC 05:36 $\to$ 한국 시각 14:36 완벽 계산).
- **타임존 가산 및 자정 통과 시 일자(Day) 자동 롤오버 보존**:
  - `resolve_base_time`에 `return_datetime=True` 옵션을 지원하여, 야간 시험에 +9시간을 더해 자정을 넘어가더라도 익일 날짜가 `FileDataReader.save_date` 및 `Datetime` 컬럼에 온전히 보존되도록 개선.
  - 단일 주행 중 자정 통과 시에도 `build_datetime_series`의 `pd.date_range` C-엔진을 통해 연속 타임스탬프에서 일자가 자연스럽게 증가함을 검증 완료.
- **슬립률 분포 분석 구간 기본값 개선 (`an_slip_pdf.py`, `an_skewness.py`)**:
  - 하드코딩된 임의 속도(80~5kph) 대신 사용자가 설정한 시험 속도(`test_vel`, 예: 100~1kph)를 기본 분석 구간으로 동적 연동.
  - 0kph 정지 부근에서 발생하는 휠 슬립률 분모 0 발산 및 휠 락 노이즈를 방어하기 위해 최소 속도(min_vel=1kph) 가드를 필수 보장하고 상세 공학적 사유를 주석/닥스트링에 명시.
- **자동 `am`/`pm` 접미사 제거 및 `cond` 수동 처리 규격화 (`vt_acc_brk.py`, `vt_acc_brk_tire.py`, `plotter_*.py`)**:
  - 13시 분기 기반 임의 `am`/`pm` 자동 생성 로직을 완전히 삭제하고 수동 지정만 지원.
  - 미지정 시 파일명이나 플롯 타이틀에 `_am`, `_pm`, `_None`이 일절 포함되지 않도록 클린 명명 체계 정합.
- **BMW 320d ADAC Dry 실차 통합 분석 파이프라인 (Case 4) 무결성 통과 (Exit Code 0)**.

### [2026-10-08] v3.15 - SnowSurfaceInterpolator 데이터 무손실 원칙 복원 및 노면 등고선 세션 간 1:1 비교 전역 고정 스케일 체계 확립
- **데이터 무손실 원칙 복원 (`range_height=None, range_temp=None`)**:
  - `SnowSurfaceInterpolator.__init__`에서 3.0mm 하드코딩 클리핑 범위를 전면 제거하고 기본값을 `None`으로 개편.
  - `_sanitize_feature` 및 `get()`에서 `valid_range is None`일 때 클리핑을 건너뛰도록 처리하여 1.6~18.8mm의 실제 스노우 침하 깊이 및 노면 온도차를 100% 무손실 보존.
  - 필요 시 사용자가 `(min, max)` 튜플을 전달할 때만 안전하게 클리핑하도록 Scikit-learn 표준 인터페이스 정립.
- **통합 제동-노면 데이터셋(`1. df_combine_test_surface_spec.pkl`) 무손실 복원**:
  - `b_combine_surface_performance_spec.py` 재실행으로 `char_height` 최대값이 기존 3.0mm(83% 강제 포화)에서 실제 8.40mm로 정상 복원.
  - 1차 vs 2차 제동 시험 간의 차분 표준편차($\Delta \text{char\_height}$)가 0.13mm에서 1.54mm로 10배 이상 물리적 변동성을 회복하여 노면 침하에 따른 제동거리 반응성 확보.
- **노면 등고선 세션 간 1:1 비교 전역 고정 스케일 시각화 (`SnowSurfaceInterpolator.plot`)**:
  - 세션마다 X, Y, Z(컬러바) 스케일이 달라 상호 비교가 불가능했던 문제를 해결하기 위해 전역 고정 스케일 기본 탑재:
    - 트랙 위치: X축 `[0.0, 400.0]m`, Y축 `[45.0, 90.0]m`
    - 컬러바: 침하 깊이 `[0.0, 12.0]mm` (25단계), 노면 온도차 `[-0.5, 3.5]℃` (25단계)
    - `extend='both'` 및 Non-blocking(`close=True`, `save: Union[bool, str, Path]`) 완벽 준수.
  - `cond_id` 인자를 통해 원하는 시험 세트 스냅샷을 1초 만에 자동 탐색 및 시각화 지원.
- **보정 파이프라인 및 등고선 보정 맵 최신화**:
  - `c_run_snow_correction_pipeline.py` 가동으로 Random Forest $R^2=0.8645$, MAE 55.9% 감소 확인.
  - 2D 등고선 보정 맵(`3_Snow_Surface_char_height_VS_cd_test_ah_Contour.png`)의 X축 범위를 복원된 실제 분포에 맞추어 `[-4.0, 4.0]mm`로 확장 갱신.
- **1:1 기술 매뉴얼 동기화**:
  - `surface_interpolator.md` 명세 및 실무 예제 100% 갱신 완료.

### [2026-10-01] v3.9 - 노면 차분 머신러닝 보정 엔진 동적 특성 인자(x_cols, y_col) 지원, 결측치(NaN) 방어 가드 및 시각화 동적화
- **동적 특성 인자 리스트 인터페이스 (`x_cols: List[str]`, `y_col: str`) 혁신**:
  - 기존의 고정 키워드 인자(`x_1`, `x_2`) 방식을 과감히 폐기하고 머신러닝 표준 규격인 `x_cols: Optional[List[str]]` 및 `y_col: str`로 전면 개편.
  - 침하 깊이, 표면 온도, 기온, 절대습도 등 임의의 실험 인자 조합은 물론 3개 이상의 다변량 피처 확장까지 완전 지원.
- **결측치(NaN) 자동 정제 및 방어 가드 (`missing_strategy='drop'`)**:
  - 센서 결측치 자동 드롭, All NaN 컬럼 및 빈 입력 시 명시적 `ValueError` 사전 차단.
- **다형성 예측 인터페이스 (`predict_delta`)**:
  - 스칼라 가변인자(`*args`), 딕셔너리(`dict`), 1D/2D NumPy 배열, Pandas DataFrame 입력을 단일 함수에서 자동 판별 처리.
- **시각화 플로터 및 검증기 100% 동적 라벨링 연동**:
  - `SnowCorrectionPlotter`의 Figure 1(산점도), Figure 3(등고선 맵), 오버플랏 플롯의 축 라벨 및 타이틀이 모델의 `x_cols`, `y_col` 명칭으로 자동 치환.
  - 다변량(3개 이상) 피처 등고선 맵 렌더링 시 미선택 축은 0.0(기준 baseline)으로 고정하여 2D 격자 정밀 평가.
- **전수 무결성 검증 통과 (Exit Code 0)**:
  - 단위 테스트 및 실데이터 1,964건 통합 파이프라인 전수 완주 (Exit Code 0).

### [2026-10-01] v3.8 - SnowSurfaceInterpolator 직관적 단일 표준 확립 및 12:30 세션 쪼개짐 원천 해결
- **`SnowSurfaceInterpolator` 리팩토링 및 완전 승격**:
  - 모호했던 과도기적 명칭 `SurfaceConditionTwin` 및 `surface_twin.py`를 완전히 폐기하고, 사이킷런 표준 인터페이스 기반의 직관적인 **`SnowSurfaceInterpolator`** (`surface_interpolator.py`)로 전면 개편.
  - `fit(df_surface)` $\to$ `transform(df_brk)` 구조로 표준화하여 `b_combine_surface_performance_spec.py`의 수동 for 루프를 단 2줄로 경량화.
- **시험 묶음 최초 시작 시각(`min(Datetime)`) 기반 단일 세션 결합 (`transform`)**:
  - `Date + ReqNo + TestOrder` 그룹별로 평가 시작 시각을 감지하여 세션(`test_cond_id`)을 판별.
  - 12:30 전후로 걸쳐 진행된 제동 시험 세트(예: 2026-01-13 10:07~12:34)가 런별 단순 시각 비교로 인해 am/pm으로 분열되던 중대 결함을 100% 원천 해결.
- **파이프라인 무결성 검증 완결**:
  - `surface_interpolator.py`, `surface_animator.py` 자가 구동 테스트 전수 통과 (Exit Code 0).
  - 실차 제동 1,964건 전수 보간 매칭 완결 및 2026-01-13 단일 세션 유지 완벽 검증.

### [2026-10-01] v3.6 - snow_condition 도메인 a_/b_ 전처리 직렬 연계 및 중복 컬럼 완전 정화
- **a_/b_ 전처리 직렬 연계**: `a_make_SnowAccBrkTest_DF.py`, `a_make_SnowSurfaceCharacteristic_DF.py`, `a_make_SRTT_DF.py` 최종 저장에 `harmonize_snow_dataframe` 적용.
- **`b_combine_surface_performance_spec.py` 전면 현대화**: 과거 레거시 파사드를 완전 걷어내고 `SurfaceConditionTwin` 직접 인스턴스화하여 53개 3D 스냅샷 복원 $\to$ 1,964건 제동 런 1:1 시공간 보간 매칭 파이프라인 완성.
- **스키마 무결성 강화**: `schema.py` 내 레거시 다대일 매핑 시 중복 컬럼 생성 버그 원천 해결 및 `COL_47_ORDER` 표준 정렬 상수 공식 탑재.
- **Exit Code 0 무결성 통과**: `c_run_snow_correction_pipeline.py` 가동 전수 통과 (3초 완결).

---
**Last Updated**: 2026-10-20  
**Standard**: unoUtil Clean Architecture v3.49 & Single Baseline Law & Single Master MOC Law
