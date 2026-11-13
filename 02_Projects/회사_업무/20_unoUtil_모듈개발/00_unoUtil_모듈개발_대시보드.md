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

> [!NOTE]- 📜 v1.0 ~ v4.02 주요 개발 및 리팩토링 이력 [클릭하여 펼치기]
> | 버전 | 날짜 | 작업자 | 핵심 수정 및 개발 내역 (Changelog) | 상태 |
> | :--- | :---: | :---: | :--- | :---: |
> | **v4.03** | 2026-11-13 | uno &<br/>Gemini | 🏎️ **서킷 및 조종안정성 (`circuit`) 최상위 파이프라인 `vt_circuit` 전면 리팩토링 및 가감속(`vt_acc_brk`) 100% 동일 규격 표준화 (다중 경로 묶음 처리, 계층형 딕셔너리 파라미터 분기, 3대 표준 디렉터리, DB/캐시 제어 및 시각화 엔진 연동 완결)**<br/>• **다중 경로 묶음 처리 및 계층형 파라미터 분기 탑재 (`vt_circuit.py`, `resolve_hierarchy_param`)**: 단일 경로뿐만 아니라 `path={'technoring': ..., 'idiada': ...}` 다중 경로 딕셔너리 입력을 지원하고, 차량 제원(`wheel_base`, `cg_height`, `gear_ratio`, `sensor_pos`), 센서 지연(`delay_ms`, `col_target`), 컨트롤 타이어 키워드(`ref_kwd`), 보정 설정(`correct_type`, `correct_range`) 등을 서킷별/노면별 딕셔너리로 독립 주입하는 3계층 파라미터 해석 체계 완비. 단일 경로 입력 시 단일 `VTCircuitProject` 반환, 딕셔너리 경로 입력 시 `Dict[str, VTCircuitProject]` 반환으로 다형성 및 하위 호환성 100% 보장<br/>• **`vt_acc_brk` 100% 동일 기본값 및 DB/캐시 제어 인자 전수 정합**: `save_file`/`load_file` (원시 캐시 `0.db/*_raw.gz`), `save_tire`/`load_tire` (단품 객체 `0.db/*.tir`), `save_pjt`/`load_pjt` (프로젝트 `0.db/*.pjt`), `save_result` (`2.result/*.csv`), `restore`, `weather`, `excel` 지원 및 기본값(`False`/`None`) 완전 일원화<br/>• **3대 표준 디렉터리(`0.db/`, `1.figure/`, `2.result/`) 구축 및 시각화 트리거 완비**: `PlotterTire.all()` / `PlotterProject.all()` 신설 및 `plot`, `save_plot`, `close_tire`, `close_pjt` 파이프라인 직결 연동 (`plot=True` 시 GUI 화면 창 띄우기 지원, `save_plot=True` 시 `1.figure/` 직하위에 궤적·랩타임·마찰원·랩비교·5축레이더 고해상도 PNG 자동 저장)<br/>• **`VTCircuitTire` & `VTCircuitProject` 기능 보강**: `VTCircuitTire.tire_name` 표준 명명 규칙, `save()` / `load()` 직렬화/역직렬화 메서드, `VTCircuitProject.save_result()` CSV 익스포터 탑재<br/>• **VehicleDynamic 회전 좌표계 단위 누락 버그 원천 해결 및 마찰원 g 규격화**: `rotate_kinematics` 및 `rotate_origin`에서 `deg`/`deg/s` 단위가 라디안(`rad`)으로 변환되지 않아 `ReferAccLateral`이 5,426 m/s²(553g)로 폭발하고 슬립각이 3,272도로 왜곡되던 치명적 결함을 원천 해결(`ReferAccLateral` 18 m/s²(1.8g), `peak_grip` 2.16g, 슬립각 -15~+13도 정상 복원). `an_grip_limit.df`에 명시적 `g` 단위 컬럼(`Ay_g`, `Ax_g`) 수납 및 `PlotterProject.friction_circle()` 프로젝트 단위 전체 타이어 마찰원 비교 차트 신설<br/>• **실계측 데이터 기반 전수 검증 통과 및 1:1 기술 매뉴얼 최신화**: 한국테크노링 6개 VBO 실데이터 기반 Case 1(단일 원스톱), Case 1-1(3대 표준 디렉터리 산출물 검증), Case 2(load_pjt 캐시 초고속 복원), Case 3(다중 경로 묶음 처리) 및 `example_circuit.py` 100% 무결성 통과 (Exit Code 0), `vt_circuit.md` 순수 GFM 매뉴얼 동기화 완결 | ✅ 완료 |
> | **v4.02** | 2026-11-13 | uno &<br/>Gemini | 🖥️ **가감속/제동 대시보드 (`dashboard_app.py`) Load & Combination 탭 파일 관리 테이블 UI/UX 개편 및 Tire 탭 런 상세 테이블 규격 일원화**<br/>• **파일 선택 테이블 실시간 사파이어 블루 네온 하이라이트 탑재**: `style_tire_run_dataframe`을 `col_valid` 매개변수로 범용화하여 `Valid` 및 `선택` 컬럼을 모두 지원하고, 체크된 파일은 선명한 사파이어 블루(`#0E4F8B`) 네온 및 볼드 화이트, 체크 해제된 파일은 어두운 슬레이트(`#090D14`)로 실시간 하이라이트 반영<br/>• **Tire 탭 런 상세 테이블 규격 100% 동일화**: pinned=True 기반 선택열(100px) 안정적 고정(글자 잘림 원천 방지 및 grow:1 여백 분배 차단), 폴더명(650px) 반응형 최대폭 흡수 및 파일명(220px)·크기(85px) 황금 비율 레이아웃 완성, 컴포넌트 키(_v2) 갱신으로 브라우저 드래그 캐시 완전 리셋, 익스팬더 제목 [📋 계측/객체 파일 관리] 직관화, 인덱스 열 노출 및 높이(240px) 통일<br/>• **사이드바 메이저 60px + 마이너 20px 2중 사이버틱 HUD 테크 그리드 텍스처 대폭 강화 및 156px 전폭 3단 수평 구획(Top: 86px 프로젝트 구획(라벨-입력창 수직 층간 분리) + [활성 프로젝트] 라임 테마 네온 타이틀 중앙 정렬 및 콘솔창 [✕] 원클릭 닫기 버튼 장착<br/>• **메인 패널 최상단 사이버틱 HUD 테크 그리드 헤더 바 카드 구축**: 제목 행에 왼쪽과 일체화되는 2중 테크 그리드 배경(studio-top-header-card)을 주입하고 거대한 40px 섹션 구분선 및 과도한 상하 여유분을 완전 삭제하여 제목과 요약 정보를 수직 정중앙(Vertical Center)으로 완벽 정합 및 마우스 호버 헬프 툴팁 독립 렌더링, Mid: 5대 탭, Bottom: 60px 데모) 전면 개편**: 좌측 사이드바 배경을 딥 사이버 블루(#07192F ~ #040E1C)로 전환하고 우측 구분선을 완전 삭제하여 메인 홀로그램 캔버스와의 선명한 면(Surface) 대비 확립. 상단(프로젝트)과 하단(데모)에 동일한 52px 높이의 엣지 팟을 구축하여 요소를 수직 중앙 정렬하고, 중간 5대 아이콘 탭의 배치 갭과 시그니처 화살표(>>) 100% 보존<br/>• **전체 선택/해제 세션 동기화 안정화**: [전체 선택] 및 [전체 해제] 시 data_editor 캐시 키를 안전하게 리셋하여 즉시 하이라이트 갱신 보장<br/>• **1:1 기술 매뉴얼(`dashboard_app.md`) 최신화 및 py_compile 무결성 검증 통과** | ✅ 완료 |
> | **v4.01** | 2026-11-12 | uno &<br/>Gemini | 🖥️ **가감속/제동 대시보드 (dashboard_app.py) 계측 분석 & 객체 불러오기 전 구간 단일 표준 프로세스 확립, 탭 전환 입력 경로 100% 영구 보존, 원클릭 전체 비우기, 콘솔 자동 소멸 복원 완결**<br/>• **계측 데이터 분석 & 객체 불러오기 전 구간 동일 표준 프로세스 이식**: 하단 [프로젝트 및 타이어 불러오기] 섹션에도 상단 계측 분석과 100% 동일하게 객체 파일 현황 카드 노출, 폴더 전체 경로(폴더명)·파일명 표출, 폴더명 최대폭·파일명 중간폭·선택/크기 최소폭 비례 레이아웃 최적화, 중복 제거 가드, st.data_editor 기반 인터랙티브 선택/제거 관리기([전체 선택], [전체 해제], [🗑️ 선택 파일 제거]) 탑재, 그리고 [객체 불러오기] 클릭 시 선택된 객체 파일(.pjt / .tir)만 선별 로드되도록 프로세스 완벽 일원화<br/>• **디스크 원본 대조 선별 파일 서브셋 자동 스테이징 무결성 확립**: 목록에서 파일을 제외하거나 체크박스를 해제했을 때 원본 디스크 파일명 집합 대조를 통해 선택/남겨진 파일만 전용 서브셋 임시 폴더에 복사 투입하여 100% 선별 분석 보장<br/>• **콘솔창 2중 노출 완전 철거 및 성공 시 자동 소멸(placeholder.empty) 복원**: 직전 분석 콘솔 잔여 영역을 완전 철거하여 스피너 아래 단일 콘솔만 뜨고 정상 성공 시 0초 만에 자동으로 사라지도록 복원(오류/경고 시에만 유지)<br/>• **업로더 드롭존 뒤 모든 파일목록 완전 숨김(section ~ *)**: 팝오버 내부 업로더 파일 리스트 및 페이지네이션을 완전히 숨겨 심플한 드롭존만 노출하고 화살표 오작동 원천 차단<br/>• **1:1 코드 매뉴얼(dashboard_app.md) 최신화 및 py_compile 무결성 통과** | ✅ 완료 |
> | **v4.00** | 2026-11-12 | uno &<br/>Gemini | 🏁 **서킷 및 조종안정성(Handling) 전면 리팩토링 및 3대 공식 시험장(Technoring, IDIADA, Pferdsfeld) 실계측 데이터 엔드투엔드 파이프라인 완결, 가감속 대시보드 v2.0 고도화 완성**<br/>• **8대 공통 코어 완성 (`unoUtil.vehicle_test`)**: `BaseMemory`/`Correct` 최상단 승격, `BaseTire`/`BaseProject` 객체지향 기반 클래스 신설(가감속 및 서킷 공통 상속 완비), `VehicleDynamic` 기어비 반영 전륜 슬립각 및 횡하중 이동 확장, `sensor_sync` 2-Tier 스마트 지연 동기화 엔진 구축, `param_resolver` 3계층 파라미터 해석기, `ExcelReportBuilder` 기업 표준 서식 엑셀 빌더 완비<br/>• **서킷 6대 물리 서브 분석기 구축 (`circuit/analyzers/`)**: `AnLapTime`(랩타임·섹션시간·일관성), `AnSteeringDelay`(영점교차+미분피크+MAD 3.0 조향지연), `AnUndersteerGradient`($K_{us}$ 구배·MF/RF 피팅), `AnYawGainStability`(요게인·잔류요진동 감쇄안정성), `AnGripLimit`(피크·평균·p95 선회그립), `AnRacingLine`(k-d Tree 부호형 교차 궤적 편차 Signed CTE) 완결 및 단위 테스트 100% 통과<br/>• **서킷 오케스트레이터 및 시각화 플로터 구축**: `VTCircuitTire`(단일 타이어 26개 지표 요약 & 온디맨드 자가 복원), `VTCircuitProject`(멀티 타이어 관리, 컨트롤 타이어 시계열 선형 보간 및 엑셀 리포트 빌더), `PlotterTire`(궤적·랩타임·마찰원), `PlotterProject`(랩타임 비교 막대·5축 성능 레이더 차트) 완결<br/>• **가감속/제동 대시보드 (`dashboard_app.py`) v2.0 고도화 및 실시간 콘솔 스트리머 완성**: `StreamlitLiveConsole` 로그 심각도 정밀 판정(`_classify_line`, `has_warning`) 및 4색 뱃지/보더(ERROR/WARNING/STREAMING/COMPLETED) 실시간 UI 연동, 웹 드래그앤드롭 업로드 정규화(`_extract_latest_upload_batch`, `_normalize_uno_upload_relpath`) 및 텍스트 경로 수동 입력 동기화(`_pending_lc_meta_override`), 분석 스피너/콘솔 슬롯 분리 및 속도 대역 미검출 친절 가이드 안내 완비<br/>• **최상위 원스톱 래퍼 함수 `vt_circuit` 및 실무 예제/진입점 제공**: 5줄 원스톱 배치 멀티프로세싱 파이프라인 구현, `WetHD/Main.py` 및 `unoUtil/example/example_circuit.py` 탑재 완료<br/>• **VBO 파서 1열 시프트 버그 원천 해결 (`index_col=False`)**: `vbo_parser.py`의 `index_col=False` 누락으로 인한 90개 컬럼 1열 밀림 및 시간 파싱 오류를 원천 박멸하여 VBO 파싱 신뢰도 100% 달성<br/>• **3대 공식 시험장 실데이터 18개 VBO 일괄 엔드투엔드 검증 통과**: 한국테크노링(6 VBO, 62개 지표), 스페인 IDIADA(6 VBO, 62개 지표), 독일 페어츠펠트(6 VBO, 70개 지표) 전원 랩/섹션 분할 및 보정 완결 (Exit Code 0) | ✅ 완료 |
> | **v3.90** | 2026-11-12 | uno &<br/>Gemini | 🏎️ **`unoUtil.vehicle` ➔ `unoUtil.vehicle_test` 패키지 대개편, 공통 베이스 프레임워크(`BaseProject`/`BaseTire`) 구축, 서킷/핸들링 시험 모듈화(`circuit/`) 착수 및 가감속 대시보드 v2.0 홀로그램 UI 탑재**<br/>• **`unoUtil.vehicle` ➔ `unoUtil.vehicle_test` 공식 패키지 승격 및 Clean Architecture 재정립**: 실차 시험 종합 도메인으로 위상을 확립하고 `unoUtil/__init__.py`에서 `vehicle_test` 공식 노출 및 하위 호환 매핑 완료. `analysis_test_data.py`, `hndl_test.md` 등 과도기 레거시 파일 정리 및 소멸<br/>• **실차 시험 공통 베이스 프레임워크 구축 (`base_project.py`, `base_tire.py`, `param_resolver.py`, `sensor_sync.py`, `excel_report.py`)**: 단품 타이어 객체(`BaseTire`) 및 프로젝트 단위 취합/지수화 베이스(`BaseProject`)를 신설하여 향후 제동(`acc_brk`)과 서킷(`circuit`) 전반에 공통 객체지향 추상화 제공<br/>• **서킷 및 조종안정성(Handling) 전용 모듈화 신설 (`unoUtil.vehicle_test.circuit`)**: `circuit/` 패키지 신설, `func_circuit.py`(Haversine 거리, GPS 누적거리, 랩/섹션 자동 분할 `calc_lap_section_split`, 조향 응답 지연 `calc_steering_delay_zero/derivative`, 언더스티어 구배 `calc_understeer_gradient`, Pacejka MF / Random Forest 커브피팅, 요레이트 게인/안정성, 한계 그립 통계, Signed CTE 편차, Cohen's d, 시그모이드 점수화 등 13대 물리 연산 함수 완비), `circuit_cutpoint.py`(`CircuitCutpoint` 클래스: 한국테크노링, 스페인 이디아다, 독일 페어츠펠트, 파펜부르크 등 GPS 좌표 기반 서킷 자동 식별 및 랩/코너 섹션 컷포인트 피클 로더 구축)<br/>• **가감속/제동 대시보드 (`dashboard_app.py`) v2.0 정식 업데이트 및 미래형 다크 홀로그램 UI/UX 완성**: 2,500여 줄의 대규모 고도화, `acc_brk_hologram_bg.jpg` 배경 및 글래스모피즘 네온 UI/UX, Streamlit 1.50 최신 컴포넌트 최적화, 런 편집 인터랙션 및 시각화 저장 연동<br/>• **대규모 실차 시험 계측 데이터셋(VBB, VBO) 수납 및 체계화**: 스노우 가감속 지그재그(`snow_acc_brk/25RD120007EF/` run1/run2 C1, C2, T1, T2) 및 유럽/국내 주요 핸들링 서킷(IDIADA, Pferdsfeld, Technoring 각 T1~T6 18개 VBO) 계측 데이터 수납 완료 | ✅ 완료 |
> | **v3.87** | 2026-11-12 | uno &<br/>Gemini | ⚡ **`unoUtil.vehicle.acc_brk` 온디맨드 캐시 복원 시 서브분석기 지표 소실 원천 방지(`_get_synced_tire_summary`), 단일/복수 콘트롤 타이어 자동 판정 마스크 무결성 확립(`_find_reference_tire`), 프로젝트 다형성 커스텀 정렬(`sort(order=...)`) 및 PlotterProject 시각화 연계 정합, Streamlit 대시보드 UI/UX 대규모 최적화 완결**<br/>• **서브분석기 요약 지표 자동 복원 및 동기화 (`vt_acc_brk_project.py`, `vt_acc_brk_tire.py`)**: 온디맨드 캐시 복원(`result.df` 재생성) 또는 요약 갱신 시 `_result.summary`의 이전 값 선제 백업 및 보존, 하위 서브분석기(`acceleration`, `split_speed`, `slip_pdf`, `mu_drop`, `slip_mode`, `sys_response`, `curve_fit`)에 보존된 `_summary` 컬럼이 누락된 경우 이를 감지하여 자동 복원·병합하는 `_get_synced_tire_summary()` 신설 및 `update_summary()` 합집합 컬럼 정합 완결<br/>• **콘트롤/기준 타이어 자동 판정 마스크(`_find_reference_tire`) 무결성 확립 (`vt_acc_brk_project.py`)**: `ref_kwd` 매칭 시 모든 타이어가 기준 타이어 키워드에 매칭되는 경우(예: T1~T4 시험 세트) 첫 번째 행만 기준 타이어로 지정하여 나머지 타이어가 중복 콘트롤로 은닉되던 결함 해결, `mask_result = (~mask_ref_tire) | (~mask_ref_tire.duplicated(keep='first'))`로 인덱스 순서 100% 보존<br/>• **프로젝트 정렬 다형성 지원 및 시각화 마스크 동기화 (`vt_acc_brk_project.py`)**: `sort()` 메서드에 딕셔너리뿐만 아니라 리스트/튜플(`Union[Dict, List, tuple]`) 커스텀 순서 지정 지원(자동 순차 가중치 부여), 정렬 후 `mask_ref_tire`와 `mask_summary`를 필수 동기화하여 `PlotterProject`의 모든 프로젝트 비교 차트가 정렬된 순서 및 인덱스를 정확히 바라보도록 정합<br/>• **`correct.py` 및 `plotter_project.py` 안정성 강화**: `correct.py`에서 `_result.summary` 직접 갱신을 통한 불필요한 시계열 재복원 방지 및 타이어명 문자열 타입 캐스팅 통일, `plotter_project.py`의 `_plot_slip_ratio`에서 실제 슬립 분포 데이터가 존재하는 유효 타이어 세트만 동적 필터링하도록 방어<br/>• **Streamlit 웹 대시보드 UI/UX 및 렌더링 최적화 (`dashboard_app.py`)**: `st.data_editor` 실시간 편집 상태(`edited_rows`) 즉시 감지 및 셀 하이라이트 스타일러(`style_tire_run_dataframe`) 탑재, 250KB Base64 배경 및 SVG 스타일을 해시(`_static_theme_hash`) 기반으로 브라우저 부모 창 `head`에 1회만 주입하여 리런 깜빡임 및 지연 극소화, 폴더 선택 다이얼로그 연동(`_on_click_browse_tire_save_dir`, `_on_click_browse_save_tab_dir`), 별도 편집 체크박스 없이 즉시 편집 + [⚡ 선택 런으로 재분석] 일체형 1줄 UX, 타이어 그래프 설정을 `st.tabs` 규격으로 정돈, 타이어 DND 순서 정렬 안정화 | ✅ 완료 |
> | **v3.87** | 2026-11-12 | uno &<br/>Gemini | 🚀 **`unoUtil.file_reader` VBOParser 비정상 헤더 일시(`@ 45:52`) 파싱 예외 방어 로직 설계 및 `HydroplaningProgram` 레거시(v1) ➔ 차세대 12대 공식 도메인 패키지(v2.0) 전면 마이그레이션 기술 사양 연계 완결**<br/>• **`VBOParser._extract_save_date` 비정상 시간 헤더 방어 보강 설계 (`vbo_parser.py`)**: `hylat/C1.VBO` 등 일부 계측 파일 헤더에 비정상적인 시간(`File created on 45/25/2145 @ 45:52`)이 기록된 경우 `datetime.time(h_int, m_int, s_int)`에서 유발되던 `ValueError: hour must be in 0..23` 크래시를 방어하기 위해 `try ... except ValueError: t_time = datetime.time(0, 0)` 폴백을 설계하여 계측 파일 로드 100% 무중단 안정성 확보<br/>• **`HydroplaningProgram` 레거시 마이그레이션 사양 확립**: 과거 `unoUtil.readDataFile` 및 `unoUtil.unoPostProcessing` 호출부를 최신 `unoUtil.file_reader.FileDataReader` 객체지향 인스턴스 로딩 및 `unoUtil.signal_process.post_process`(`moving_average`, `merge_data`, `find_continuous_interval`) 공식 표준 API로 1:1 전면 전환하는 마이그레이션 아키텍처 및 상세 구현 계획서 수립 완결 | ✅ 완료 |
> | **v3.86** | 2026-11-06 | uno &<br/>Gemini | 🖥️ **unoUtil 대시보드 Streamlit 1.50 최신 엔진 승격, 실시간 다크 콘솔 스트리머 전 구간 탑재, n_jobs=-1 병렬 가속 완벽 호환 및 3단 Flexbox 무결점 UI 완성**<br/>• **Streamlit 1.50 최신 엔진 승격 및 st.data_editor 단일 표준화**: 구버전(1.22)의 무거운 리페인팅 병목을 타개하고 고속 바이너리 통신 엔진으로 승격, 런 편집 100% 정상 작동 보장<br/>• **실시간 다크 콘솔 스트리머 전 구간 탑재**: 파이참 터미널을 열 필요 없이 대시보드 화면 내에 독립 윈도우 스타일의 다크 터미널을 띄워 원본 로그를 실시간 스트리밍<br/>• **스마트 고정 프로그레스 바 탑재**: HTML 태그 노출 버그를 순수 압축 HTML로 회피하고, 콘솔창 하단 고정 네온 바에서 게이지가 제자리에서 솩솩 차오르는 완벽한 터미널 룩앤필 완성<br/>• **TestVelRange 갱신 버그 해결 및 런 테이블 하이브리드 UI 구축**: update_tire_runs에서 속도 변경 시 메타데이터를 즉각 동기화하도록 수정. 대제목 옆 [✏️ 런 편집] 토글 및 [⚡ 선택 런으로 재분석] 버튼 일체형 하이브리드 UX 완성<br/>• **멀티코어 병렬 가속 완벽 유지 및 피클·컨텍스트 에러 100% 영구 차단**: vt_acc_brk.__globals__ 직접 타겟팅 및 StreamlitSafeThreadPoolExecutor 구현으로 피클/컨텍스트 에러 물리적 차단 및 use_container_width 경고 박멸<br/>• **Modern CSS Flexbox 3단 레이아웃 정규화 및 차트 이미지 저장 기능 탑재**: position:fixed 조상 전파 결함을 완전 철거하고, 제동데모와 가속데모를 바닥 좌우 대칭(1줄)으로 완벽 밀착 복원. 차트 확대 창 헤더 메뉴에 고해상도 PNG 원클릭 다운로드 기능 탑재 | ✅ 완료 |
> | **v3.85** | 2026-11-06 | uno &<br/>Gemini | ⚡ **`unoUtil.vehicle.acc_brk` AnResponse 연산 75% 고속화, correct.py DataFrame 단편화 경고 박멸, 5대 `save_*` 및 `plot` 파라미터 직교 분리 및 기본값 `False` 단일 표준화, 시스템 코어 자동 감지 스마트 병렬화(`n_jobs: int = -1`) 탑재 및 0.db 분기 생성 완결**<br/>• **`AnResponse` 알고리즘 병목 규명 및 75% 고속화 (`func_acc_brk.py`)**: `calc_response` 내부에서 75만 행 전체 시계열 필터링을 런별 유효 슬라이스(`idx_start:idx_end` + 패딩) 1회 사전 필터링으로 개편하고 중복 `pd.concat` 블록을 1회로 통합하여, `AnResponse` 분석 소요 시간을 **2.36초 ➔ 0.58초 (약 75% 시간 단축, 4배 가속)**로 단축하고 수치 지표(`sys_response_time: 0.137`, `sys_rising_time: 0.23`, `sys_rising_slope: -3.862`) 100% 동일성 검증 완료<br/>• **`correct.py` DataFrame 파편화 경고(`PerformanceWarning`) 원천 소멸**: Control 보정 루프에서 컬럼 개별 insert 방식을 딕셔너리 수집 후 `pd.concat` 1회 일괄 병합(Batch Concat)으로 전면 리팩토링하여 경고 0건 및 메모리 복사 오버헤드 박멸<br/>• **5대 `save_*` 및 `plot` 파라미터 직교 분리 및 기본값 `False` 단일 표준화 (`vt_acc_brk.py`)**: `save_file`(캐시 .gz), `save_tire`(타이어 .tir), `save_pjt`(프로젝트 .pjt), `save_result`(결과 테이블 .csv 3종), `save_plot`(차트 이미지 .png), `plot`(화면 창 띄우기) 기본값을 모두 `False`로 통일하고, `plot=False, save_plot=True` 조합 시 GUI 팝업 없이 백그라운드 무음 저장이 가능하도록 완비<br/>• **100% 클린 인메모리 연산 실증 및 0.db 디렉터리 분기 생성**: 모든 `save_*` 옵션이 `False`일 때 `check_path(dir_db)` 무조건 호출 결함을 수정하여 `0.db`, `1.figure`, `2.result` 폴더가 단 하나도 남지 않는 완전한 클린 인메모리 실행 보장<br/>• **코어 수 자동 감지 기반 스마트 병렬 모드(`n_jobs: int = -1`) 탑재**: 파이썬 내장 `os.cpu_count()`(현재 PC 12코어) 기반으로 단일 타이어는 오버헤드 없는 순차 실행, 2개 이상 타이어는 `ProcessPoolExecutor` 멀티프로세싱 동시 병렬 처리를 지원하고 실측 VBO 2개 데이터 기반 순차 대비 수치 오차 0.000000 완전 일치 검증<br/>• **하위 모듈(`VTAccBrkTire`, `VTAccBrkProject`) 기본값 전수 통일 및 1:1 기술 매뉴얼 동기화**: `VTAccBrkTire.run` 및 `VTAccBrkProject.run` 시그니처와 구현에서 `save_result=False`, `plot=False`를 일괄 정합하고 소스 코드 저장소 내 1:1 기술 매뉴얼(`vt_acc_brk.md`, `vt_acc_brk_project.md`, `vt_acc_brk_tire.md`) 100% 동기화 완료 | ✅ 완료 |
> | **v3.83** | 2026-11-05 | uno &<br/>Gemini | 🎨 **`format_fig` 폰트 스타일링 개선(`pretty` 굵기 제어 및 누락 버그 해결), `PlotterTire`·`PlotterProject` 타이틀 일반 굵기(`normal`) 일괄 통일, `vt_acc_brk` 메인 함수 타이어 개별 그래프 저장 기본 활성화(`plot=True`) 및 스노우 제동 데이터(`snow_brk`) 123개 구버전 부산물 정비 완결**<br/>• **`format_fig` 폰트 스타일링 및 타이틀 누락 결함 개선 (`plotter.py`)**: `pretty=True`일 때만 볼드체(`bold`)를 적용하고, `pretty=False`일 때는 `title`과 `suptitle`, 축 라벨의 폰트 굵기를 강제로 볼드로 바꾸지 않고 일반 굵기(`normal`) 또는 원본 스타일을 보존하도록 개선. 아울러 `pretty=False` 지정 시 문자열 `title`이 누락되던 버그를 완벽 해결<br/>• **`PlotterTire` 서브플롯 타이틀 하드코딩 볼드체 전면 제거 (`plotter_tire.py`)**: `_plot_full_calibration_session` (4개 패널), `_plot_mu_drop_group` (3개 패널), `_plot_skewness_group` (2개 패널), `_plot_response_channel` (3개 패널)에 직접 명시되어 있던 `fontweight='bold'`를 전면 제거하여 전체 서브플롯 타이틀이 일관되게 일반 굵기로 렌더링되도록 정합<br/>• **`PlotterProject` 연동 정비 및 기본 굵기 통일 (`plotter_project.py`)**: 내부 공통 키워드 분리 헬퍼 `_make_format_fig_kwargs` 및 일괄 차트 생성 메서드 `all()`의 기본 옵션으로 `pretty=False`를 지정하여, 사용자가 명시하지 않아도 모든 프로젝트 비교 플롯의 타이틀/슈퍼타이틀이 균일한 일반 굵기로 출력되도록 표준화<br/>• **`vt_acc_brk` 메인 함수 `plot: bool = True` 기본값 변경 (`vt_acc_brk.py`)**: 배치 파이프라인 구동 시 별도 `plot=True` 옵션 없이도 개별 타이어 9대 시각화 그래프가 `1.figure/` 폴더에 기본 저장되도록 시그니처 및 docstring 갱신<br/>• **실측 스노우 제동 데이터(`snow_brk`) 41개 런 내 123개 분석 캐시/결과 폴더 정리**: 41개 `run*` 폴더에서 과거 생성된 `0.db`, `1.figure`, `2.result` 폴더 123개를 안전 삭제하여 원천 계측 파일(`*.vbo`/`*.vbb` 228개)을 보존한 초기 상태로 정비하고, 테크노링 기상 오염으로 Parquet 스키마 충돌을 일으키던 구버전 중복 프로젝트 파일 2건(`25OE120004EF_snow_run1.pjt`, `25RD120007EF_snow_run1.pjt`) 영구 삭제<br/>• **1:1 순수 기술 매뉴얼 동기화 (`plotter_tire.md`, `plotter_project.md`, `vt_acc_brk.md`)**: `pretty` 파라미터 명세 및 `vt_acc_brk` `plot` 기본값 최신화 완료 | ✅ 완료 |
> | **v3.82** | 2026-11-05 | uno &<br/>Gemini | 🖥️ **`unoUtil.vehicle.acc_brk` 통합 인터랙티브 웹 대시보드(`dashboard_app.py`, 5,300+ 라인) 신규 구축, 5대 네온 메달리온 UI 및 다크 홀로그램 글래스모피즘 테마 완성, 온디맨드 시각화·인터랙티브 런 편집(`_TIRE_RUN_TABLE_HTML`)·드래그앤드롭 정렬(`_DND_TIRE_HTML`)·새창 인터랙티브 뷰어(휠줌·팬·박스부분확대) 탑재, 스노우 가속 공식 표준속도(5-40) 코어모듈(get_default_test_vel) SSOT 일원화, 플로터 12×6 표준화 및 Tire 탭 파라미터 승계 결함 핫픽스 완결**<br/>• **대시보드 전용 독립 서브패키지 구축 (`unoUtil/vehicle/acc_brk/dashboard/`)**: `dashboard_app.py`, `dashboard_app.md`(1:1 순수 GFM 매뉴얼), `acc_brk_hologram_bg.jpg`를 모아 외부 의존성 없는 완결된 독립 패키지로 격리 수납 완성<br/>• **5대 통합 네비게이션 및 다크 홀로그램 글래스모피즘 테마**: 사이드바 5대 메뉴(Information, Load & Combination, Tire, Project, Save) 원형 네온 메달리온(평상시 Dimmed, 호버/활성 시 네온 라임 및 `>>` 더블 셰브론 인디케이터), 상단 `Acceleration / Braking Studio` 네온 타이틀, 전경 위젯 반투명 스모크 글래스(68~80%) 및 175px 파란색 알약형 메인 액션 버튼 우측 수직 밀착 완성<br/>• **초고속 인터랙티브 컴포넌트 탑재**: 체크박스 클릭 시 0ms 즉각 파란색 하이라이트 및 리런 없는 커스텀 테이블(`_TIRE_RUN_TABLE_HTML`), 마우스 드래그 앤 드롭 타이어 순서 정렬 바(`_DND_TIRE_HTML`), 옵션 변경 시 자동 렌더링을 차단하고 [그리기] 클릭 시에만 차트를 생성·캐싱하는 온디맨드 렌더링, 독립 팝업 브라우저 창에서 차트를 확대하는 새 창 뷰어(`_inject_chart_new_window_hook`) 완비<br/>• **플로터 규격 12×6 (2:1 비율) 일괄 통일**: `PlotterTire`, `PlotterProject`, `TireCurve`의 도화지 비율을 12×6으로 표준화하고 긴 타이틀 자동 줄바꿈 적용. `PlotterTire.accbrk()` 내 `#런번호 (수치)` 뱃지화 및 유효(파랑)/제외(빨강) 색상 분리, 3단 지그재그 높이 분산 배치 완결<br/>• **`vt_acc_brk.py` 하이브리드 병합 확장 및 표준 산출물 정합**: `calc_merged_project()`에 단품 `VTAccBrkTire`와 `VTAccBrkProject`를 자유롭게 혼합 병합하는 하이브리드 파이프라인 및 `use_suffix` 제어 탑재, 산출물 폴더 `0.db`, `1.figure`, `2.result` 표준 체계 확립<br/>• **Tire 탭 재분석 시 파라미터 승계 결함 핫픽스**: `cur_tp['kwargs']` 미조회로 인해 속도 조건 변경 시 `min_sec=0.5s`, `max_sec=15.0s`, `ws=10`이 강제 주입되어 유효 런이 탈락하던 버그를 해결하고 엔진 표준 기본값(`min_sec=1.0s`, 제동 `max_sec=10.0s`, 가속 `max_sec=25.0s`) 및 기존 분석 파라미터 정상 계승 완료 | ✅ 완료 |
> | **v3.81** | 2026-11-05 | uno &<br/>Gemini | ⚡ **`unoUtil.vehicle.acc_brk` 휠 가속도(`WA*`) 수치 미분(`np.gradient`) 연산 고정 샘플링 주기(`dt = 1/sr`) 단일 표준화, GPS 타임스탬프 중복($\Delta t = 0$)으로 인한 0으로 나누기 경고(`RuntimeWarning`) 원천 박멸 및 1:1 기술 매뉴얼(`func_acc_brk.md`) 동기화 완결**<br/>• **수치 미분 균일 간격(`uniform_spacing`) 단일 표준화 (`func_acc_brk.py`)**: `calc_slip` 및 `calc_wheel_delay_compensation`에서 차륜 가속도(`WA*`) 미분 시 비균일 시간 좌표(`df_work['Time']`)를 투입하던 방식을 전면 개편하여, 고정 샘플링 주기 `dt = 1.0 / float(sr)`(스칼라) 기반 균일 미분으로 일원화 완성<br/>• **분모 0 및 부동소수점 경고(`divide by zero`, `invalid value`) 원천 차단**: VBOX/GPS 계측 장비의 100Hz 로깅 시 패킷 지연 등으로 인해 발생하던 시간 컬럼 중복($\Delta t = 0$) 인덱스에서 NumPy 내부적으로 유발되던 `divide by zero encountered in divide` 및 `invalid value encountered in add` 경고와 가속도 채널 결측치(`inf`/`NaN`) 오염을 100% 원천 방지하고 연산 속도 대폭 향상<br/>• **실제 실측 타이어 데이터 기반 실증 검증 완료**: `25RD120004EF_snow_brk_run2_40-5_T2` 타이어 데이터(인덱스 29622의 $\Delta t = 0$ 중복)를 대상으로 실증 검증을 수행하여, 경고 발생 건수 기존 4~5회 ➔ 0건 완전 소멸, 정상 구간 수치 오차 $3.1 \times 10^{-9}$ 이하 동일성 및 `AnSlipPdf.analysis()` 100% 무경고 통과 확인<br/>• **1:1 순수 기술 매뉴얼 동기화 (`func_acc_brk.md`)**: `calc_slip` 동작 사양에 균일 샘플링 간격 기반 차륜 가속도 수치 미분 및 분모 0 방어 사양 명세 최신화 | ✅ 완료 |
> | **v3.80** | 2026-11-04 | uno &<br/>Gemini | 📁 **`unoUtil.vehicle.acc_brk` 표준 산출물 3단계 순차 넘버링(`0.db`, `1.figure`, `2.result`) 체계 확립, 엑셀 시각화 보고서(`1.figure`) 저장 경로 정합, 과도기적 폴백(Fallback) 및 레거시 호환 로직 전면 삭제(SSOT 확립), 실측 스노우 데이터(41개 run) 원시 파일 상위 이동 및 계층 깊이 평탄화(Flat) 완결**<br/>• **실측 스노우 제동 데이터(`snow_brk`) 41개 런 디렉토리 계층 평탄화(Flatting)**: `D:/uno/1. 2026/2. 25-26_Outdoor_Loop2/3. snow_brk` 하위 41개 `run*` 폴더에서 과거 분석 부산물(164개 항목)을 일괄 정리하고, `1. rawdata` 폴더 내 228개 원시 데이터 파일(`.vbb`, `.vbo`)을 바로 상위 `run*` 직속으로 이동시킨 후 빈 `1. rawdata` 디렉토리(41개)를 완전 삭제하여 폴더 탐색 깊이를 1단계 축소<br/>• **특이 파일명(`zigzag_*.VBB`) 16건 전수 식별 및 보존**: `25RD120004EF` 및 `25RD120007EF` 내 지그재그 회피 제동 시험 파일 16건을 정밀 식별하고 데이터 손실 없이 안전하게 상위 경로로 배치 보존<br/>• **표준 산출물 디렉토리 3단계 순차 넘버링 체계 확립 (`0.db`, `1.figure`, `2.result`)**: 기존 공백 혼용(`0. db`, `2. fig`, `3. result`) 및 번호 건너뜀을 정비하여, ① `0.db`(직렬화 캐시: `*.tir`, `*.pjt`, `*_raw.gz`), ② `1.figure`(그래프 이미지: `*.png` 및 엑셀 시각화 보고서: `graph_*.xlsx`), ③ `2.result`(최종 수치 및 CSV 요약: `result_*.csv`)로 직관적이고 순차적인 단일 표준 아키텍처 완성<br/>• **엑셀 시각화 보고서 피규어 폴더(`1.figure`) 저장 위치 일원화**: `vt_acc_brk` 배치 실행 시 자동 생성되는 `graph_{project_name}.xlsx`의 기본 저장 목적지를 `1.figure` 내부로 일원화하여 이미지와 엑셀을 한곳에서 즉시 검토 가능하도록 개선<br/>• **과도기적 폴백(Fallback) 및 레거시 호환 로직 전면 삭제 (Single Baseline Law 준수)**: `vt_acc_brk.py`에서 기존 폴더명(`0. db`, `2. fig`, `3. result`)을 감지하여 재사용하거나 마이그레이션하던 조건 루프를 완전히 삭제하고 순수 4줄 직결 코드로 정비(`dir_db_root`, `dir_fig_root`, `dir_res_root`). `common_data.py`의 `_find_existing_pjt()` 폴백 함수 삭제 및 `dashboard_app.py` 탐색 필터 단순화 완료<br/>• **통합 검증 및 도메인 무결성 확인**: `test_structure_integrity.py` 12대 공식 도메인 패키지 및 서브 모듈 무결성 테스트 100% 정상 통과 | ✅ 완료 |
> | **v3.75** | 2026-11-03 | uno &<br/>Gemini | 🏎️ **`unoUtil.vehicle.acc_brk` 실제 계측 제동 데이터 기반 듀얼 보정 모델(Control 시계열 선형 보간 & 노면온도 물리 팩터) 실증 파이프라인 탑재, 3대 실무 예제(`Case 8, 9, 10`) 구축 및 `correct.py` Pandas 2.0+ 기상 Datetime 병합 정밀도 결함 핫픽스 완결**<br/>• **실무 제동 데이터(BMW 320d Dry) 기반 Control 타이어 보정 실증 (`Case 8`)**: 실제 VBB 계측 데이터 및 캐시를 로드하여 Control 타이어(C1, C2) 시계열 선형 보간(`correct_type='control'`)을 수행하고 가상 기준값(`adj_refer_brk_mean`), 성능 지수(`index_brk_mean`), 보정 제동거리(`corr_brk_mean`) 산출 파이프라인 실증 성공<br/>• **노면온도(`BRK Dry Asp`) 물리 프로파일 보정 실증 (`Case 9`)**: 실측 기상 센서의 아스팔트 노면온도와 타이어 시험 시점을 결합하고, 마른 노면 표준 물리 계수(10℃당 1.0m 보정) 기반으로 기준온도 대비 편차(`factor_diff`) 및 온도 보정 제동거리를 자동 산출하는 물리 모델(`correct_type='factor'`) 파이프라인 완성<br/>• **기 저장된 프로젝트(`.pjt`) 로드 후 보정 모델 동적 변경 및 초고속 재계산 검증 (`Case 10`)**: 저장된 프로젝트를 0.05초 만에 역직렬화 로드한 뒤, 원시 계측 데이터 재분석 없이 보정 엔진(`correct_performance`)만 호출하여 Control ➔ Factor 모델로 동적 전환 및 즉시 재계산(0.1초) 완결<br/>• **`correct.py` Pandas 2.0+ Datetime dtype 불일치 결함 핫픽스**: 요약표의 `datetime64[us]`(마이크로초)와 기상 센서의 `datetime64[ns]`(나노초) 정밀도 차이로 인해 `connect_weather`(`merge_asof`) 시 발생하던 dtype 불일치 에러를 사전에 감지하여 자동 통일하도록 정합 완료 | ✅ 완료 |
> | **v3.74** | 2026-11-03 | uno &<br/>Gemini | 🏎️ **`unoUtil.vehicle.acc_brk` 유효 세션 선별(`sel_mode='max_min'`) 대칭 절사(Symmetrical Trimming) 단일 표준화 및 1:1 기술 매뉴얼 최신화**<br/>• **`_select_best_data` 대칭 절사(Symmetrical Trimming) 알고리즘 구현 (`func_acc_brk.py`)**: 기존 `sel_mode='max_min'` 설정 시 `valid_count`(선택 개수)와 무관하게 무조건 최솟값 1개와 최댓값 1개만 제외하던 로직을 전면 개선하여, 전체 시험 세션 수가 `valid_count`를 초과할 경우 상/하단 극단값을 균등하게 제외(`drop_total // 2`)하여 정확히 지정된 개수(`number`)만큼 선별하는 대칭 절사 방식으로 단일 표준화 완성. 전체 데이터 수가 부족하거나 미지정(`valid_count=None`) 시에는 최소/최대 각 1개를 제외하는 기존 안전 폴백을 유지<br/>• **통합 검증 및 단위 테스트 완료**: 가상 10회 주행 시계열 데이터 및 `calc_acc_brk` 실제 파이프라인에서 `valid_count=6` 지정 시 10회 중 상/하단 각 2개씩 총 4개 극단값을 배제하고 정확히 6개 유효 런(`EffNum`)을 선별함을 100% 검증 통과<br/>• **1:1 순수 기술 매뉴얼 최신화 (`func_acc_brk.md`)**: `calc_acc_brk`의 `sel_mode` 및 `valid_count` 파라미터 상세 설명에 대칭 절사 알고리즘의 동작 사양, 제외 규칙 및 폴백 메커니즘을 명확히 보강 명세 | ✅ 완료 |
> | **v3.73** | 2026-10-30 | uno &<br/>Gemini | 🏛️ **`unoUtil.vehicle.acc_brk` 6대 서브 분석기 4대 계층(`params`, `df`, `detail`, `summary`) 단일 표준화(SSOT), 8대 동사 기반 타겟 휠 판정 헬퍼(`get_target_wheels`) 신설, 비표준 `summary_detail` 전면 소멸 및 PlotterTire 9대 전 차트 무결성(46개 이미지 전수 생성) 완결**<br/>• **4대 계층 단일 표준화 (Zero-Alias / Zero-Fallback 헌장 준수)**: 모든 분석기를 ① `params`(설정값 컨테이너), ② `df`(순수 시계열, 대용량 캐시 소거 대상), ③ `detail`(회차/바퀴별 1행 상세 진단 요약, 영구 보존), ④ `summary`(전 차수/전 휠 종합 평균 1행 대표 지표, 영구 보존)로 엄격히 역할 분리하고, 과도기적 별칭(Alias)과 폴백(Fallback)을 일절 두지 않고 직교화 완성<br/>• **8대 표준 동사 헬퍼 `get_target_wheels()` 신설 (`func_acc_brk.py`)**: 단일 공학 물리 규칙에 따라, 사용자가 채널을 수동 지정하지 않는 한 제동(`brk`)은 전륜(`Front`: FL, FR), 가속(`acc`)은 차량 구동계에 따라 RWD ➔ `Rear`(RL, RR), AWD ➔ `All`, 기본/FWD ➔ `Front`를 전 분석기(`Response`, `SlipMode`, `SlipPdf`, `MuDrop`, `TireCurve`)가 100% 동일하게 공유하도록 일원화<br/>• **`AnResponse` 시계열 메타 오염 원천 박멸 및 `detail` 신설**: 시계열 `df`의 수천 행마다 반복 복사되던 스칼라 메타컬럼(`Base_Val`, `Offset_Vel_Base`, `Thresh_Start` 등)을 전면 제거하여 순수 파형만 보존하고, 회차(Run) x 바퀴(Position)별 1행 상세 진단 메타데이터 테이블(`tire.response.detail`)로 영구 보존<br/>• **`summary_detail` 완전 소멸 및 2대 표준 식별자(`Run`, `Position`) 통일**: `AnMuDrop`과 `AnSlipModeSkewness`의 비표준 속성명 `summary_detail`을 코드베이스(`*.py`, `*.md`)에서 100% 제거하고 `detail`로 단일화. 모든 `detail`의 1~2열을 `Run`(`1, 2...` 또는 `'All'`)과 `Position`(`FL`, `FR`, `Front`, `Rear`, `All` 등 7대 표준 키워드)으로 일원화<br/>• **`BaseMemory` 3중 온디맨드 복원 방어막 수립**: 복원 시도 즉시 선제적으로 빈 DataFrame(`_df`, `_detail`, `_summary`)을 초기화하고, `_is_restoring` 재귀 락(Lock)을 걸어 조기 반환이나 예외 발생 시에도 무한 루프가 원천 차단되도록 설계 (`target_attr_list = ['df']`로 대용량 시계열만 소거)<br/>• **소비자 코드(`PlotterTire`) 정비 및 실차 계측 배치 분석 무결성 검증**: `PlotterTire.sys_response()`가 `detail`에서 런 메타데이터를 직접 조회하도록 직교화하고, `mu_drop()`과 `slip_mode()`의 `detail` 연계를 정합하여 실제 BMW 320d 마른 노면 배치 파이프라인에서 9대 차트 경고 0건, 총 46개 이미지 100% 정상 생성 완료 | ✅ 완료 |
> | **v3.72** | 2026-10-30 | uno &<br/>Gemini | 🛞 **`unoUtil` 4대 핵심 모듈(Response, Mu-Drop, CurveFit 제동/가속) 알고리즘 고도화 보고서 볼트 이관, 날짜·버전·특정 알고리즘 중심 시계열 명명 체계 정립, 볼트 미러링 첨부파일 1:1 계층화(351개 이미지 전수 무결성) 완결**<br/>• **Response 전면 재설계 실측 검증 보고서 이관 (`30_response`)**: 저마찰 눈길 발진 역추적 창($\le 3.5\text{s}$) 및 적응형 기저점($A_{\text{base}}$), 휠 통신지연/극저속 슬립 복원, $d^2V/dt^2=0$ 1차 과도 피크 및 25~75% 적응형 타겟 대역 응답 지연($\Delta t_{\text{resp}}$)과 10~90% 라이징 기울기 회귀 실측 검증 보고서([[2026-10-30_v3.71_Response_시작점탐지_WSS딜레이복원_적응형구간_알고리즘전면재설계_검증보고서]]) 입고 및 전용 MOC([[00_response_보고서_통합_색인]]) 구축 완료<br/>• **Mu-Drop 강건 분석 실측 검증 보고서 이관 (`40_mu_drop`)**: 초기 제동 피칭 다이브 & 리바운드($14\%$ 스팬) 앵커링, 속도 축 등간격 빈($0.5\text{kph}$) 기반 영위상($\angle H = 0$) 추세선, 차륜 가속도 RMS 듀얼 오실레이션 포락선($Z_{\text{osc}}$) 및 3D 스무딩 상태 공간 K-Means + DT 분기 속도 실측 검증 보고서([[2026-10-30_v3.71_MuDrop_피칭보정_영위상추세선_오실레이션포락선_알고리즘고도화_검증보고서]]) 입고 및 전용 MOC([[00_mu_drop_보고서_통합_색인]]) 구축 완료<br/>• **CurveFit 제동 및 가속 듀얼 종합 개발 보고서 체계화 (`20_curve_fit`)**: 가속 휠 딜레이 보정 보고서([[2026-10-21_v3.60_CurveFit_가속_WSS시간지연물리보정_발진궤적복원_종합보고서]])에 대칭하여 제동 전용 Onset 복원·4대 랜드마크($L_0\to L_1\to L_2\to L_3$) 위상정렬·초기 과도 분리 및 스노우 웻지(Snow Wedge) 종합 개발 보고서([[2026-10-22_v3.66_CurveFit_제동_Jerk시작점_4대랜드마크위상정렬_과도분리_스노우웻지_종합개발보고서]]) 신규 입고 및 전용 MOC([[00_curve_fit_보고서_통합_색인]]) 갱신 완료<br/>• **볼트 미러링 첨부파일 계층화 및 시계열 명명 표준(SSOT) 확립**: `_attachments/{폴더경로}/{문서명}/` 거울 구조 확립, 미사용 고아 이미지(228개) 비파괴 격리(`_미참조_보관/`), 다중 참조 이미지 독립 복제 및 전수 검증 깨진 링크 0건(351개 이미지 100% 정상 작동) 무결성 완결 | ✅ 완료 |
> | **v3.71** | 2026-10-29 | uno &<br/>Gemini | 🏎️ **`unoUtil.vehicle.acc_brk` 보정 데이터 파이프라인 일원화 및 원본 보존, 하드코딩 없는 적응형(Data-Driven) 과도 응답 알고리즘 및 3열 다중 진단 시각화·2×2 보정 진단 대시보드 고도화 완결**<br/>• **보정 데이터 파이프라인 일원화 및 보정 전·후 원본 보존 (`an_slip_pdf.py`, `vt_acc_brk_tire.py`, `func_acc_brk.py`)**: CAN 통신 지연(약 20ms) 및 출발 직후 저속 휠속 센서 슬립(Wakeup) 보정이 완료된 정제 데이터를 응답성 분석(`AnResponse`) 및 커브피팅(`TireCurve`)에서도 그대로 승계하도록 단일 파이프라인을 확립하고, 보정 전 원본 휠속(`WS*_Raw`) 및 원본 슬립률(`SR*_Raw`) 컬럼을 영구 보존하여 언제든 보정 전·후 효과를 대조 가능하도록 완성<br/>• **하드코딩 제로 적응형(Data-Driven) 과도 응답 알고리즘 탑재 (`an_response.py`, `func_acc_brk.py`)**: 고정 임계값 대신 각 런의 피크 가속도 대비 적응형 타겟 대역(18% ~ 45%, 기저 노이즈 대비 최소 마진 보장)을 동적 산출하여 제동/가속 전 노면(Dry/Wet/Snow/Ice)에서 휠-차체 정합 지연(`sys_response_time`, `sys_response_dist`)을 흔들림 없이 계산하고, 평형 기저점(Median±MAD)부터 1차 과도 피크($d^2Vel = 0$)까지의 순수 진폭($\Delta A$) 기준 10% ~ 90% 라이징 타임과 상승/하강 기울기 완벽 산출<br/>• **제동 시 차량 역학적 물리 지연(~220ms) 공학적 규명 반영**: 20ms CAN 통신 지연 보정 후 남은 ~220ms는 센서 결함이 아닌 타이어 슬립 형성 ➔ 노면 마찰력 발생 ➔ 서스펜션 피칭 압축을 거쳐 차체 전체가 감속하기까지의 실제 차량 동역학적 과도 응답 시간임을 정확히 계측 및 반영<br/>• **3열 다중 진단 시각화 완성 (`PlotterTire.sys_response`)**: 1열(속도 프로파일 & CAN 지연 보정 전후 대조) + 2열(과도 가속도 & 적응형 지연 매칭) + 3열(기저점·1차피크·10~90% 라이징 회귀)의 3열 다중 진단 뷰를 구축하고, 모든 Run 행의 열별 Y축 스케일을 동적 100% 통일(하드코딩 Zero)하여 런 간 비교 직관성 극대화<br/>• **2×2 상세 보정 진단 대시보드 완성 (`PlotterTire.slip_check`)**: 전체 세션 속도 및 슬립률 요약(상단 1·2패널)과 첫 유효 런 과도 구간 초정밀 확대(하단 3·4패널: `WS_Raw vs WS`, `SR_Raw vs SR`, 저속 웨이크업 복원 구간 하이라이트)를 결합한 2×2 상세 보정 진단 체계 완비 | ✅ 완료 |
> | **v3.70** | 2026-10-29 | uno &<br/>Gemini | ⚡ **`unoUtil.file_reader` VBB 바이너리 타임스탬프 슬라이싱 결함(`minute/second must be in 0..59`) 원천 해결, `vt_acc_brk` 메인 타이어 분석 완료 INFO 로그 복원 및 가속(`acc`) 시험 시 Mu-Drop 물리 분석/플롯 원천 제외 최적화**<br/>• **`datetime_helper.py` VBB 타임스탬프 파싱 결함 원천 해결**: VBO(텍스트, `HHMMSS.sss`) 전용 문자열 슬라이싱 판정 분기에서 바이너리(`.vbb`) 파일을 분리(`is_vbb_file`)하여, 초 단위 누적 시간(`sec_total = float(first_time_val)`) 및 타임존 오프셋(핀란드 UTC+2h 등) 계산 로직으로 정확히 진입하도록 정정 (`minute/second must be in 0..59` 에러 및 데이터 Skip 버그 원천 박멸)<br/>• **`vt_acc_brk` 및 `VTAccBrkTire` 메인 분석(`analysis`) 완료 INFO 로그 복원**: 과거 DEBUG 레벨로 강등되어 서브 분석기 로그만 노출되던 결함을 해결하고, 타이어 단품 분석 완료 시 유효 런 회차(예: `유효 6/8회`) 및 대표 성능 지표(제동거리 평균 `brk_mean` 또는 가속시간 평균 `acc_time_mean`)를 포함한 표준 INFO 로그를 정식 복원<br/>• **가속(`acc`) 모드 시 Mu-Drop(마찰 저하) 분석 및 시각화 원천 제외**: 노면 마찰력 저하 및 제동거리 손실(Mu-Drop)은 급제동/ABS 전용 물리 거동이므로, `VTAccBrkTire.run()`에서 가속 모드일 때 불필요한 `AnMuDrop.analysis` 호출을 생략(`analyzer.mu_drop = None`)하고, `plotter_tire.py`의 렌더링 맵에서도 `is_acc` 시 `Mudrop_Distance` 차트 생성을 제외하여 무의미한 WARNING 경고 및 불필요 연산 부하를 100% 제거<br/>• **원천 계측 캐시 압축 저장 로그 명확화**: `vt_acc_brk.py`에서 원시 계측 데이터를 캐싱하는 `Raw Data 압축 저장` 로그를 `원천 계측 캐시 압축 저장`으로 명확히 정돈 | ✅ 완료 |
> | **v3.69** | 2026-10-29 | uno &<br/>Gemini | ⚡ **`unoUtil.vehicle.acc_brk` 7대 서브 분석기 및 `VTAccBrkTire` 온디맨드(On-demand) 하이브리드 캐싱 아키텍처 표준화 완결, 과도기 코드 전면 소멸, 선제적 빈 데이터프레임 초기화(Pre-emptive Initialization) 패턴 도입 및 도메인 지식 사전(`vt_acc_brk_사전.md`) Living Sync**<br/>• **`an_slip_pdf.py` 과도기 코드 및 무한 재호출 버그 원천 박멸**: 과거 휠 지연 보정 개발 시 임시로 삽입되었던 `not cached_df.attrs.get("wheel_delay_compensated", False)` 조건문 및 미정의 변수(`cur_df`)를 전면 삭제하고, 프로퍼티 레벨의 임시 가드(`_is_ready_to_analyze()`)를 걷어내어 순수 $O(1)$ 온디맨드 자가 복원 규격(`if self._df is None: ...`)으로 복원<br/>• **`VTAccBrkTire.analysis()` 선제적 빈 DF 초기화 도입**: `analysis()` 진입 즉시(try 블록 최상단) 모든 결과 필드(`_result.df`, `summary`, `summary_all`, `detail`, `detail_all`)를 빈 데이터프레임으로 선제 채움으로써, 유효 런 미검출 조기 반환 시 외부나 시각화 모듈(`PlotterTire`, `PlotterProject`)에서 `.summary.empty` 조회 시 발생하던 `AttributeError: NoneType` 다운을 100% 원천 차단<br/>• **하위 분석기 3종(`skewness`, `response`, `mu_drop`) 단일 위임(Single Delegation) 헌장 확립**: 상위 생성자(`AnSlipPdf`)가 휠속도 검증을 단독 전담하도록 하고, 하위 3개 모듈의 최상단 중복 가드를 제거하여 `if self.test.slip_pdf.df.empty: return self` 순수 단일 위임 코드로 롤백 (`func_acc_brk.py`의 `is_col_wheel_speed` 헬퍼 함수는 영구 보존)<br/>• **시각화 모듈 연계 멱등성(Idempotency) 완비**: 휠속도가 없는 시험 데이터에서 플로터의 다중 가드 조회 시 매번 `analysis()`가 강제 재기동되던 루프 폭포수를 완전 차단, 최초 1회만 경고 후 이후 조회는 0초 만에 빈 DF를 즉시 반환하여 평화롭게 플롯 스킵<br/>• **분석기 및 시각화 플로터 경고 메시지 단일 표준화**: 분석 모듈 5종(`Slip_PDF`, `Mu_Drop`, `Slip_Mode_Skewness`, `Response`, `TireCurve`)은 `[{self.name}] [원인]이(가) 없어 분석을 생략합니다.` 규격으로, 시각화 모듈 2종(`PlotterProject`, `PlotterTire`)은 `[{name}] 분석 결과 데이터가 없어 그래프 생성을 생략합니다.` 단일 표준 문장으로 완전 통일하여 영문/한글 혼용 및 '선행 분석 필요' 등 오해 소지 문구를 100% 박멸<br/>• **가속/제동 대표 성능 컬럼 네이밍 규격(`brk_mean` vs `acc_time_mean`) 및 KeyError 잠재 버그 소멸**: 제동 1순위 대표 지표인 제동거리(`brk_mean`, `corr_brk_mean`, `index_brk_mean`)와 가속 시간(`acc_time_mean`)의 물리적 네이밍 당위성을 규명 및 SSOT 확정하고, `VTAccBrkTire.analysis()` 내부에서 `brk_dist_mean`을 참조하던 오타를 `brk_mean`으로 바로잡아 로깅 포맷 완결<br/>• **도메인 지식 사전(`vt_acc_brk_사전.md`) 심층 지식화**: 온디맨드 캐싱에서 `None`(캐시 부재/복원 트리거)과 `pd.DataFrame()`(연산 완료 센티널/재연산 방어막)의 정반대 라이프사이클 모델과 선제적 초기화 패턴을 3.3절 및 5.4절에 공식 집대성 | ✅ 완료 |
> | **v3.68** | 2026-10-27 | uno &<br/>Gemini | 🏛️ **unoUtil v2.0 전면 레거시 소멸, 전 패키지 상대 참조 100% 절대 참조(`unoUtil.*`) 전환, 4대 대원칙 기반 과거 레거시 폴더/파일/별칭(32개 모듈) 전수 소멸, 최상위 루트 `__init__.py` 슬림화 및 SSOT 표준화 완결 종합 보고서([[01_unoUtil_v2_전면_레거시_소멸_및_SSOT_단일화_완결_보고서]]) 등재**<br/>• **전 패키지 상대 참조 100% 절대 참조 전환**: 33개 파일 내 `from .` 상대 참조를 `unoUtil.*` 절대 참조로 전수 치환하여 모듈 단위 독자 실행(`__main__`) 시 `attempted relative import` 에러를 원천 박멸<br/>• **4대 대원칙 기반 과거 레거시 전면 소멸**: 빈 `legacy/` 7개소, 과도기 브릿지 4종(`ai/*`, `curve_fit/tire_curve/fit_least_squares.py`), 잔여 `signal_process/curve_fit` 폴더, 백업(`.bak`) 및 임시 산출물(`1`, `.pytest_cache`, `egg-info`) 전수 삭제<br/>• **32개 모듈 내부 레거시 별칭(Aliases) 전수 제거**: 모듈 하단에 잔존하던 구버전 별칭(`Infor_Vehicle`, `VD_*` 8종, `SP_CurveFit_*` 4종, `CurveCombiner`, `MinimizeEstimator`, `SP_Resample`, `TireMagicFormula` 등) 전면 삭제 및 표준 명칭(SSOT) 단일화<br/>• **최상위 루트 `__init__.py` 250줄 슬림화**: 과거 메타패스 가상 리다이렉터 및 가상 모듈 바인딩 완전 제거, 12대 공식 도메인 순수 Facade(180줄)로 재탄생<br/>• **비매뉴얼 보고서 볼트 안전 이관**: `tire_curve_pipeline_and_real_data_issues.md`를 볼트 `25_실차_계측데이터_태생적_문제점과_8단계_통합파이프라인_백서.md`로 신규 이관, 코드 폴더에는 81개 순수 1:1 기술 매뉴얼만 격리 보존 | ✅ 완료 |
> | **v3.67** | 2026-10-27 | uno &<br/>Gemini | 🚀 **`unoUtil.file_reader` 이기종 계측 리더 전 파서 컬럼명 순수화 & units 단일 표준화, 비정형 TXT 지능형 헤더 탐색 엔진(`HeaderFinder`) 신설, 패키지 전수 절대 참조 전환, 순수 1:1 기술 매뉴얼 헌장(`code-manual-writer` 스킬) 및 도메인 지식 사전 상시 동기화(Living Sync) 완결**<br/>• **전 파서 컬럼명 순수화 & 단위 100% 분리**: VBB, VBO, DWD, TXT 전 파서에서 컬럼명의 대괄호/단위 기호(`[unit]`)를 완전 배제하고 순수 채널명 단일 레벨로 통일, 물리 단위는 `reader.units` (`Dict[str, str]`) 단일 표준 규격으로 일괄 분리 정합<br/>• **비정형 TXT 지능형 헤더 탐색 엔진 신설 (`header_finder.py`)**: unoUtil v1 레거시 거리 가중치 스코어링 공식($Score = L \times (1 - 0.1 \times D)$) 및 연속 수치 안정성 변곡점 분석을 모듈화하여 상단 주석이 긴 비정형 TXT 파일에서도 채널명/단위/데이터 시작점을 100% 자율 식별하고 공백 내 `Name [Unit]` 결합 파싱 및 중복 컬럼명 자동 고유화 방어 구현<br/>• **패키지 전수 절대 참조(`unoUtil.file_reader.*`) 전환**: 모든 서브파서 및 하위 유틸 내 상대 참조(`from .`)를 절대 참조로 100% 치환하여 모듈 단위 독자 실행(`__main__`) 및 단위 테스트 완벽 보장<br/>• **순수 1:1 기술 매뉴얼 작성 헌장 및 신규 전문 스킬 신설**: 옵시디언 위키링크를 배제한 순수 GFM 규격, 키워드 인자(`**kwargs`) 전수 명세표, 2-Track 실전 예제를 강제하는 `code-manual-writer` 스킬 및 마스터 룰북 조항 공식 등재<br/>• **레거시 코드, 별칭, 패칭 및 폴더 전면 삭제 (Clean v2 순수화)**: 빈 `legacy/` 폴더 물리적 완전 삭제, `__init__.py` 내 `sys.modules` 패칭 4개 행 및 `ReadDataFile` 별칭 제거, `file_data_reader.py` 내 `to_legacy_tuple`, `_CallableModule`, `print` 레거시 키워드 제거 및 `verbose` 단일 표준화, `base_parser.py` 내 `to_legacy_tuple` 제거, `standard_channel_pattern.py` 내 `funcChangeSignalName` 제거, `dwdReader.py` 내 `dwdRead`/`diagnoseDWD` 제거로 100% 직교적 단일 표준(SSOT) 완결<br/>• **도메인 지식 사전(`file_reader_사전.md`) Living Sync**: 신규 아키텍처 다이어그램 및 HeaderFinder 역할을 볼트 도메인 지식 사전에 직접 동기화 반영 | ✅ 완료 |
> | **v3.66** | 2026-10-22 | uno &<br/>Gemini | 🛞 **`unoUtil.curve_fit.tire_curve` 실차 계측 신호처리부터 구속조건 Magic Formula(MF) 피팅까지 8단계 통합 파이프라인 완결, 절제된 딥 네이비 단색 Chevron 화살표 PPTX 프레젠테이션 제작, 가속/제동 전 관점 통합 기술 백서(`tire_curve_pipeline_and_real_data_issues.md`) 수립 및 실측 로우 데이터 4대 태생적 한계 4분할(2×2) 종합 진단 차트(`plot_raw_data_limitations.py`) 실증 완결**<br/>• **8단계 통합 엔지니어링 파이프라인 수립**: ① 원시 신호 입력 & 휠속도 결측 가드(`ptp > 1e-3, std > 1e-4`) ➔ ② CAN 지연 보상(`wheel_delay_compensated`) 및 구동계(RWD/AWD/FWD) 슬립 채널 선별 ➔ ③ Jerk 도함수 융합 Onset($t_0$) 복원 및 이상 회차 배제 ➔ ④ 4대 과도응답 랜드마크($L0\to L1\to L2\to L3$) 위상 동기화 및 초기 탄성 강성($K_{\text{pk}}=\mu_{L2}/s_{L2}$) 확정 ➔ ⑤ 3단 데이터 분리(관성 데드존/과도 휠스파이크/차속 컷오프) 및 본체 0.15s 영위상 스무딩 ➔ ⑥ 슬립 구간 밀도 역가중치($w_i \propto 1/\text{count}^{0.65}$) & IQR 국소 이상치 감쇠 ➔ ⑦ 원점 강성 등식 제약($B = K_{\text{pk}} / (C \cdot D)$) 기반 3변수 $(C, D, E)$ `soft_l1` TRF 비선형 피팅 ➔ ⑧ 표준 6-파라미터 복원 및 대표 곡선 테이블 생성<br/>• **보고/발표용 맞물림 Chevron 화살표 슬라이드 제작 (`tire_curve_pipeline_flowchart.pptx`)**: 과도한 원색 및 자잘한 불릿 텍스트를 전면 배제하고, 차분한 모던 딥 네이비 단색 기반의 8단계 맞물림 갈매기형 화살표(`MSO_SHAPE.CHEVRON`) 프로세스 1페이지 압축 슬라이드 완성<br/>• **가속 및 제동 전 관점 통합 기술 백서 구축 (`tire_curve_pipeline_and_real_data_issues.md`)**: 실차 계측 데이터의 태생적 5대 한계 규명(운전자 조작 지터, 센서 딜레이, 관성 데드존/스파이크, 제어기 슬립 편중, 미분/유압 노이즈) 및 제동 vs 가속 12대 비교 매트릭스 집대성<br/>• **실측 로우 데이터 현상 실증 4분할(2×2) 종합 진단 차트 구축 (`plot_raw_data_limitations.py` ➔ `real_vehicle_raw_data_limitations.png`)**: 실측 제동(19,522개) 및 가속(32,753개) 데이터를 인위적 색상 구분 없이 '단일 회색(Gray) 산점도'로 표출하여 실차 데이터의 현실적 난점을 그대로 살리고, 레전드를 없애고 핵심 물리 현상 주석만 집중 배치: (a) 제동 슬립 산점도 4대 왜곡 & Naive 피팅 파탄, (b) 가속 노이즈 구름 & 트랙션 이탈, (c) 다중 런 조작 타이밍 지터($\sigma \approx 24.5\text{ms}$)와 단순 시간평균 시 피크 15~25% 상쇄 붕괴(Phase Blur), (d) 시간 경과에 따른 노면 마찰 드리프트($C1 \ne C2$)와 콘트롤 타이어(Control) 보정 필요성 실증 | ✅ 완료 |
> | **v3.65** | 2026-10-22 | uno &<br/>Gemini | 🛞 **`unoUtil.curve_fit` 타이어 커브 과도기 위상 동기화(Phase Alignment)·인덱스 정합 메커니즘 정립, 점 군집(Cluster) 이동 검증, 볼트 `20_curve_fit` 보고서 전 도판 18종 일괄 코드화(`run_all.py` 100% PASS), 콘트롤 타이어 보정(스케일링 동형성) 아키텍처 완결 및 `tire_curve_사전.md` 신설**<br/>• **과도기 위상 동기화 판정 기준 및 물리 랜드마크 교차 정합 정립 (`fig10_transient_sync_criteria.py`)**: 단일 신호 고정이 아니라, 차체 관성 지연 구간($L0 \to L1$)은 슬립(Slip) 극대($\max s$)를 기준, 타이어 바이트 구간($L1 \to L2$)은 감속도(Decel Mu) 극대($\max \mu$)를 교차 기준으로 동기화하는 물리적 랜드마크 정합 메커니즘 수립 및 실측 검증 도판 구축<br/>• **타이밍 지터(Jitter) 극복 38개 고정 인덱스($i=0\sim 37$) 정합 구조 규명 (`fig12_index_alignment_explained.py`, `fig14_acc_jitter_alignment.py`)**: 회차마다 27~33개(제동) 및 20~86개(가속)로 불균일한 원시 샘플을 38개 고정 인덱스로 리샘플링하여 피크를 28번 인덱스에 일제히 결집시킴으로써, 단순 시간 평균 시 발생하는 피크 평탄화(Phase Blur) 및 초기 강성($K_{\text{pk}}$) 왜곡을 완벽 소거. 특히 발진 시차 0.61초에 달하는 가속 시험에서 트랙션 무릎점($s_{\text{knee}}$) 및 구동 탄성 강성($K_x=2.66$) 복원 실증<br/>• **선(Line)의 흩어짐 착시 극복 및 인덱스별 점(Point) 군집 진화 검증 (`fig13_point_cluster_evolution.py`, `fig13b_acc_point_cluster_evolution.py`)**: 선으로 보면 루프 폭이 달라 흩어져 보이지만, 38개 인덱스 $i$ 순서대로 점을 찍으면 매 스텝마다 4~6개 런의 점들이 좁은 클러스터($\sigma_\mu \le 0.025\text{g}$)로 똘똘 뭉쳐서 이동함을 실측 데이터로 증명<br/>• **제동/가속 시작점 복원 및 4대 랜드마크 시계열 동시 표기 (`fig1a_brk_onset_recovery.py`, `fig1b_acc_onset_recovery.py`)**: 실제 물리적 $t_0$ Onset 시간축($t=0\text{s}$) 정합 리셋으로 수직 가이드라인과 곡선 피크의 100% 일치를 실현하고, 표준 속도 컷오프($50\to 8\text{kph}$, $0\to 40\text{kph}$)로 소실되던 초기 탄성 과도 구간을 완벽 회수<br/>• **볼트 `20_curve_fit` 4대 보고서 전 도판 파이썬 코드화 및 자립 구축 (18종 완비)**: 10호 보고서 휠속도 지연 보정 도판 5종(`report10_delay_compensation_figures.py`), 20/30호 보고서 타이어별/프로젝트별 도판 15종(`report20_30_batch_curve_fit_reports.py`), 40호 보고서 No-ABS 3대 추정기 도판 4종(`report40_noabs_strategy_comparison.py`)을 완비하고 통합 러너 `run_all.py` 18건 전수 100% PASS 검증 완료<br/>• **콘트롤 타이어 성능 보정(Control Correction) 스케일링 동형성 아키텍처 완비 (`cf_tire.md`, `tire_curve_사전.md`)**: Pacejka 비선형 Magic Formula에 보정 게인($\mu_{\text{corr}} = G_i \mu$)을 곱하는 것이 피크 계수($D \to G_i D$) 및 초기 강성($K \to G_i K$) 스케일링과 완벽히 동형(Isomorphic)임을 수학적으로 증명하고, `_save_raw_snapshot()` 멱등성 보장 및 프로젝트 단위 일괄 보정 연동 완결<br/>• **볼트 지식 사전 허브 확장 (`10_도메인_지식_사전/tire_curve_사전.md`)**: 객체 아키텍처, 멤버 변수 체계(로우 데이터 vs 피팅 결과), 과도기 싱크 기준, 콘트롤 보정 전용 챕터를 집대성한 전용 사전 신설 및 `curve_fit_사전.md` 상호 링크 완료 | ✅ 완료 |
> | **v3.60** | 2026-10-21 | uno &<br/>Gemini | 📈 **`unoUtil.curve_fit` 옵시디언 볼트 4대 보고서 지식 허브(`20_curve_fit`) 구축, `PlotterProject` 커브 피팅 & 슬립률 PDF 더블 Y축 복합 비교 플로터(`compare_curve_fit_pdf`) 신설 및 최상위 `vt_acc_brk` 17대 차트 자동 연동, `tire_curve/explain` 1파일 1그래프 공학 시각화 파이프라인(9종) 완결**<br/>• **옵시디언 볼트 `20_curve_fit` 지식 허브 및 4대 심층 보고서 구축**: `20_curve_fit` 폴더 신설 및 마스터 MOC([[00_curve_fit_보고서_통합_색인]]), 4대 보고서([[2026-10-21_v3.60_CurveFit_가속_WSS시간지연물리보정_발진궤적복원_종합보고서]], [[20_타이어_커브피팅_전면_개발스토리_및_공학검증보고서]], [[30_가속_시험_타이어_커브피팅_검증보고서]], [[40_NoABS_실측_VBB_타이어_커브피팅_검증보고서]]) 이관 및 36종 고해상도 차트(`_attachments/10_회사_업무/curve_fit/`) 100% 위키링크 연동 완료<br/>• **`PlotterProject.compare_curve_fit_pdf` 더블 Y축 복합 시각화 신설 및 다중 콘트롤 정규화 합성 (`plotter_project.py`, `plotter_project.md`)**: 좌측 Y축(Magic Formula 커브 피팅 곡선 + 피크 마커)과 우측 Y축(`twinx`, 실시간 주행 휠 슬립률 가우시안 확률 밀도 PDF 반투명 면적 채우기 `alpha=0.22` + 보조 점선)을 단일 X축(슬립률)에 동시 중첩 렌더링. 다중 콘트롤 타이어(C1, C2...)에 대한 곡선 평균화 및 슬립률 PDF 적분 면적 1.0 보존 정규화(NumPy 2.0+ `trapezoid` 호환) 완비로 단일 대표 객체 표현 확립<br/>• **최상위 배치 함수 `vt_acc_brk()` 및 `PlotterProject.all()` 17번째 공식 차트(`17_Curve_Fit_PDF`) 자동 연동**: `pjt.plot.all()` 및 `vt_acc_brk()` 배치 실행 시 가속 6대, 제동 10대 비교 차트로 자동 포함되어 이미지 및 엑셀 일괄 출력 파이프라인 완결 (`BMW320d_ADAC_Dry` 실측 VBB 데이터로 142KB 고해상도 차트 정상 생성 검증)<br/>• **`tire_curve/explain` 1파일 1그래프 공학 시각화 모듈 허브(9종) 구축**: `fig1_brk_onset_recovery.py` ~ `fig8_sr_dynamic_scaling_invariance.py` 및 사용자 질의 심층 분석기 `fig9_transient_landmark_deep_dive.py`($L0\to L1\to L2\to L3$ 타이밍 지터 정량화 및 4단계 과도 분리·본체 피팅 통합 가시화)를 1파일 1그래프 원칙으로 개별 모듈화하고 공통 데이터 로더(`common_data.py`), 일괄 배치 러너(`run_all.py`, 100% PASS), `README.md` 구축 완료 (볼트 보고서 4.3절 신규 수록) | ✅ 완료 |
> | **v3.50** | 2026-10-20 | uno &<br/>Antigravity | 📊 **가감속/제동(`vt_acc_brk`) 및 타이어 커브(`curve_fit`) 시각화 로깅 1줄 요약(`그래프 생성 중 .... 생성 완료.`) 전면 통일, `format_fig` 일원화(`Errno 22` 해결), 커스텀 범례 덮어쓰기 버그 및 경로 조작 취약점 완결**<br/>• **플로터 1줄 요약 로깅(`One-Line Summary Law`) 전면 통일 (`plotter_tire.py`, `plotter_project.py`)**: `PlotterTire` 9대 메서드 및 `PlotterProject` 13대 `compare_*` 메서드의 시작 로그를 `DEBUG`(`그래프 생성 시작...`)로 격하하고, 완료 로그를 `self.logger.info(f"[{name}] 그래프 생성 중 .... 생성 완료.")` 1줄 요약 포맷으로 전면 통일하여 콘솔 가독성 극대화 (`PlotterTire.all()` 내 전역 `logger` 오용도 `self.logger`로 정합)<br/>• **선택적 휠 채널/서브 분석 미실행 시 로그 레벨 `WARNING` 일원화 (`plotter_project.py`, `cf_tire.py`)**: `PlotterProject`의 4대 서브 분석 비교(`compare_slip_pdf`, `compare_mudrop_dist`, `compare_slip_mode_skewness`, `compare_response`) 데이터 부재 시 `ERROR` 대신 `WARNING`을 출력하도록 교정하고, `TireCurve.fit()`에서 휠 슬립 채널 부재로 스킵 시 `[Curve_Fit] 분석에 필요한 휠 슬립 채널 데이터가 존재하지 않아 분석을 건너뜁니다.` `WARNING` 안내 신설<br/>• **`TireCurve.plot()`의 `format_fig` 위임 일원화 및 `Errno 22` 저장 충돌 원천 차단 (`cf_tire.py`)**: `format_fig` 호출 후 중복 실행되던 수동 `plt.tight_layout()` 및 `fig.savefig()` 블록을 제거하고 `format_fig`로 저장·레이아웃·메모리 해제를 100% 일원화하여 파일 뷰어 열람 중 발생하던 `[Errno 22] Invalid argument` 충돌 및 이중 저장 오버헤드 완전 해결<br/>• **커스텀 범례(`legend`) 덮어쓰기 버그 및 경로 슬라이싱 취약점 해결 (`plotter_tire.py`, `plotter_project.py`)**: `format_fig` 기본값(`legend=True`)이 다크 테마/상단 커스텀 핸들 범례를 덮어쓰던 버그를 `kwargs.setdefault('legend', False)`(`slip_mode_skewness`, `sys_response`, `compare_slip_mode_skewness`, `compare_response`)로 해결하고, `save[:-4]` 문자열 슬라이싱을 `Path` 기반 `_format_save_path` 헬퍼로 교체 및 `"Aeceleration [g]"` 오타 수정 (`plotter_tire.md`, `plotter_project.md` 1:1 매뉴얼 동기화 및 자가 검증 통과) | ✅ 완료 |
> | **v3.49** | 2026-10-20 | uno &<br/>Antigravity | ⏱️ **가감속/제동(`vt_acc_brk`) 과도 응답성 분석기(`calc_response` in `func_acc_brk.py`) 유효 응답 및 Rising 구간 추출 4대 구조적 결함 해결 완결**<br/>• **저마찰(Snow/Ice 등) 임계값 비례 스케일링 및 역전 방지**: 목표 가감속도(`response_target`) 미달로 종료 임계값(`threshold_end`)이 완화될 때, 시작 임계값(`threshold_start`)도 완화 비율(`scale_ratio = threshold_end / target_limit`)에 맞추어 자동 비례 축소되도록 개선하여 시작점-종료점 임계값 역전 및 탈락 원천 해결<br/>• **`pre_sec` 구간 기저선(Baseline) 클리핑 정상화**: `pre_sec` 맨 앞의 첫 노이즈(`index[0]`)를 잘라내던 기존 오류를 수정하여, 유효 세션 시작점(`df_group.index[0]`) 직전의 마지막 영점/기저선(`index[-1]`) 이후부터 탐색하도록 정합하고 기저선 미교차 시 극값 폴백(`idxmax`/`idxmin`) 방어선 탑재<br/>• **단일 불량 차수로 인한 전체 조기 종료(`return dict_result`) 버그 수정**: 다중 차수(`EffNum`)·휠 채널 반복 루프 중 특정 1개 차수가 임계치 미달이더라도 전체 결과를 초기화하며 종료하지 않고 해당 차수만 `continue`로 스킵하여 정상 차수들의 분석 결과를 온전히 보존<br/>• **초기 Rising 구간 탐색 시 전역 노이즈 피크 오탐 방지**: 2차 미분(`d2_vel`) 극값 탐색 범위를 전체 주행 구간이 아닌 초기 과도 응답 구간(`idx_diff_vel_start` ~ `idx_diff_vel_end + 1.5s`)으로 한정하여 ABS 중후반부나 정지 직전 피칭 노이즈에 의한 Rising 구간 오탐 원천 차단 (`func_acc_brk.md` 1:1 매뉴얼 동기화 및 검증 완료) | ✅ 완료 |
> | **v3.48** | 2026-10-19 | uno &<br/>Antigravity | 🎯 **가감속/제동(`vt_acc_brk`) 7번째 공식 서브 분석기로서의 `curve_fit`(`TireCurve` v4.5) 전면 통합, `fit`/`predict` 분리, 구동방식(`TestVehicleLayout`) 기반 슬립 축 자동 선택, 프로젝트 콘트롤 보정 게인($G_i$) 동기화, 다중 타이어 비교 플로터(`compare_curve_fit`) 및 대표 래퍼(`vt_acc_brk`)·7대 1:1 매뉴얼 완결**<br/>• **`VTAccBrkTire.curve_fit` 서브 분석기 공식 통합 및 `fit()` vs `predict()` 책임 분리 (`cf_tire.py` v4.5, `vt_acc_brk_tire.py`)**: `VTAccBrkTire.run()` 실행 시 7번째 서브 분석기로 `self.curve_fit = TireCurve(self, ...)`을 자동 기동하여 요약(`summary.df`)에 `cf_B`~`cf_Sv`, `cf_peak_mu`, `cf_peak_slip`, `cf_stiffness`, `cf_r_squared`, `cf_rmse`, `cf_method`를 자동 산출. `fit()`은 6대 최적화 메서드(`'robust'`, `'binning'`, `'two_stage'`, `'ransac'`, `'lsq'`, `'custom'`)로 인자를 추정하고, `predict(x=None, interval=0.005)`는 기본 $[0.0, 1.0]$ 구간 또는 사용자 지정 구간(`[start, end]`)·배열(`np.ndarray`)에 대한 예측 곡선(`df[['Slip', 'Acc']]`)을 생성하도록 정립 (`BaseMemory` 호환 `clear_cache`/`restore_cache` 내장)<br/>• **휠스피드 부재 시 자동 Skip 및 시험 모드(`brk`/`acc`)·차량 구동방식(`TestVehicleLayout`) 연동 슬립 축 자동 결정**: 원시 데이터에 휠스피드/슬립 채널이 없으면 에러 없이 자동 Skip(`is_fitted = False`)하고, 제동(`brk`)은 전륜축(`FL`/`FR` 중 유효 채널 평균)을 기본 적용하되 가속(`acc`)은 `tire.infor.result` 내 `TestVehicleLayout`이 `RWD`/`FR`/`MR`/`RR`이면 후륜축(`RL`/`RR`), `AWD`/`4WD`이면 4륜 전체(`all`), `FWD`/미지정 시 전륜축(`front`)을 자동 선택 (`col_curve_fit_wheelslip` 명시 지정 시 최우선 오버라이드)<br/>• **프로젝트 콘트롤 타이어 보정(`Correct.run`) 동기화 및 요약 지표(`corr_cf_*`, `index_cf_*`) 산출 (`correct.py`, `vt_acc_brk_project.py`)**: 별도 재피팅 없이 콘트롤 타이어 선형 보간 게인($G_i = \text{corr\_Acc} / \text{mean\_Acc}$)을 각 타이어의 `curve_fit.df`(`corr_mean_Acc`, `corr_curve_Acc`), `df_raw`, `params`(`corr_D`, `corr_peak_mu`, `corr_stiffness`)에 동기화하고, 프로젝트 요약표에 `corr_cf_peak_mu`, `index_cf_peak_mu`, `corr_cf_stiffness`, `index_cf_stiffness`, `corr_cf_D`를 자동 산출<br/>• **단일 타이어(`PlotterTire`)·프로젝트(`PlotterProject`) 시각화 및 최상위 래퍼(`vt_acc_brk`) 연동**: `tire.plot.curve_fit(detail=False)`, `tire.plot.curve_fit_detail()` (6-패널 진단), `project.plot.compare_curve_fit(corr='mean', xlim=(0.0, 1.0), show_peak=True)` 신설 및 `vt_acc_brk()` 대표 함수에 `col_curve_fit_wheelslip`, `cf_method`, `cf_vel_range`, `cf_slip_range`, `cf_refine_start`, `cf_filter_transient` 3계층 분기 패스스루 완성<br/>• **7대 모듈 Docstring 및 1:1 기술 매뉴얼(`cf_tire.md` v4.5, `vt_acc_brk*.md`, `correct.md`, `plotter_*.md`), 도메인 사전([[vt_acc_brk_사전]], [[curve_fit_사전]]) 및 영구 지식 위키([[30_실차_가감속_성능변화_분석_및_보정_시스템]]) 전수 동기화 완료** | ✅ 완료 |
> | **v3.47** | 2026-10-19 | uno &<br/>Antigravity | ❄️ **스노우 노면·기상 환경 보정(`snow_condition`) 다중 스케일(`StandardScaler`) 자동 정규화 파이프라인(`correction_model.py`), 기상/노면 인자별 동적 축 범위·눈금·레이아웃 플로터(`correction_plotter.py`) 고도화 및 최신 DB 동기화 실증 완결**<br/>• **다중 스케일 피처 자동 정규화 파이프라인 구축 (`SnowCorrectionModel.train_models`)**: 기온($\Delta T \in [-10, +13]^\circ\text{C}$, $\sigma \approx 4.9$) 및 상대습도($\Delta RH \in [-15, +9]\%$, $\sigma \approx 4.9$) 등 입력 인자 간 물리적 단위 스케일이 큰 조합($\max(\sigma_X) > 2.5$)이 감지되면, 거리/커널 기반 모델인 `KNN Regressor`와 `SVR`에 `make_pipeline(StandardScaler(), ...)`을 자동 결합하고 `SVR` 무차원 유효 대역폭($\gamma_{\text{eff}} = 0.07 \times 1.28^2 \approx 0.1147$)을 주입하여 등고선 말림과 축 왜곡을 원천 차단 (기존 `[char_height, cd_test_ah]` 조합은 $\max(\sigma_X) \approx 1.54 \le 2.5$로 원시 스케일 100% 보존)<br/>• **기상/노면 인자별 동적 등고선 축 스케일링 및 타이틀 간섭 해소 (`SnowCorrectionPlotter`)**: `correction_map` 및 `correction_map_comparison(x_range=None, y_range=None)`에서 선택된 인자(`char_height`, `cd_test_ah`, `cd_test_temp`, `cd_test_hum`)의 실제 차분 분포와 인자별 전용 여백(Margin)·눈금 간격(Step)·한글 물리 단위 라벨을 자동 적용하고, 우측 공통 컬러바와 서브플롯 타이틀 간 겹침을 원천 차단<br/>• **VBO 날짜 교정 최신 DB(`3-1. df_combine_brk_surface_spec.pkl`) 기반 3종 보정 모델 전수 실증**: `Case 1 [눌림량+절대습도]` (`VIF = 1.07`, `RF` 제동거리 `0.516 m` / 지수 `2.887 %p`), `Case 2 [기온+절대습도]` (Sonntag 방정식 열역학 다중공선성 `VIF = 16.89` 규명), `Case 3 [기온+상대습도]` (`VIF = 2.53`, `RF` 제동거리 `0.495 m` [+43.6%] / 지수 `2.732 %p` [+20.6%]) 통합 비교 완결<br/>• **1:1 코드 매뉴얼(`correction_model.md`, `correction_plotter.md`), 도메인 지식 사전([[snow_condition_사전]]) 및 스노우 공학 영구 지식 위키([[31_스노우_노면_디지털트윈_및_제동성능_보정_위키]]) 동기화 완료** | ✅ 완료 |
> | **v3.46** | 2026-10-19 | uno &<br/>Antigravity | 🎯 **제동(`BRK`) 초기 과도 응답 4-랜드마크(`L0→L1→L2→L3`) 위상 정합(`calc_brk_transient_landmarks`), 2대 물리 지표($K_{\text{pk}}$ & $d\mu/dt$) 산출, 초기 과도 루프(`L0~L3`) 전체 분리 후 정상 상태(`L3~`) 본체 피팅(`filter_transient=True`), 고슬립 표본 밀도 역가중치·스노우 웻지(`enable_wedge=True`) 결합, 제외 로우 데이터(`✕`/`△`)·포함/제외 비교 시각화(`compare_unfiltered=True`) 및 VBO 날짜 파싱 3중 안전망(`datetime_helper.py`) 완결**<br/>• **제동 초기 과도 응답 4-랜드마크 위상 정합 및 2대 물리 지표 산출 (`calc_brk_transient_landmarks`)**: `unoUtil.signal_process.post_process.filters.moving_average_fast` 및 `get_col_slip`을 활용하여 회차별 `L0`(제동 시작점), `L1`(관성 불감대 종료 변곡점, $\mu \ge 0.035\text{g}$, 평균 $\Delta t_{L1} \approx 50\sim 80\,\text{ms}$), `L2`(1차 최대 마찰 피크), `L3`(1차 ABS 감압 골짜기)를 자동 검출하고 무차원 위상($s \in [0, 3]$)으로 동기화하여 대표 초기 루프를 복원. 슬립 축 유효 초기 강성인 **피크-코드 강성($K_{\text{pk}} = \mu_{L2}/\kappa_{L2}$)** 과 휠속도 노이즈에 무관한 **시간축 마찰 빌드업 속도($d\mu/dt = \Delta\mu_{10\to 90\%}/\Delta t$)** 를 동시 산출하여 타이어 초기 응답성 정량화<br/>• **초기 과도 루프(`L0~L3`) 전체 분리 후 정상 상태(`L3~`) 본체 피팅 (`filter_deadzone=True`, `filter_transient=True`)**: 초반 기울기($K_{x0}$) 추출에 사용된 `L0~L1` 관성 데드존(`self.deadzone_data`)과 `L1~L3` 1차 과도 스파이크(`self.transient_data`)가 저슬립 상단에 이질적 군집을 형성하여 본체 피팅을 왜곡하는 현상을 원천 해결하기 위해, `L0~L3` 전체를 본체 피팅에서 제외하고 `L3` 이후 정상 상태 제동 데이터만으로 피팅하도록 이원화 $\to$ `Snow_ACC_BRK` 4대 세트 전원에서 **피팅 오차(RMSE) $18.5\% \sim 23.7\%$ 대폭 감소** (C1: $0.0651\to 0.0522$, T1: $0.0715\to 0.0555$, T2: $0.0739\to 0.0564$, C2: $0.0729\to 0.0594$) 및 T2 고슬립 포화 마찰 추종성($0.404\text{g} \to 0.420\text{g}$) 완벽 복원<br/>• **고슬립($\kappa > 0.25$) 이격 해소: 구간 밀도 역가중치(`calc_bin_density_weights`) 및 스노우 웻지(`enable_wedge=True`) 결합**: ABS 제어 대역 편중($85\%$ 이상이 $\kappa < 0.25$)을 슬립 구간별 역제곱근 가중치($w_i \propto N_b^{-0.65}$)로 균등화하고, 고슬립 눈 쐐기(Snow Wedge) 선형 재상승 항($+W_{\text{snow}}\cdot\max(0, \kappa-\kappa_{\text{valley}})$)을 결합하여 고슬립 하향 이격(Gap) 완전 해소<br/>• **제외 로우 데이터 마커 분리 표시 및 초기 과도 포함 vs 제외 동시 비교 시각화 (`compare_unfiltered=True`)**: `TireCurve.plot()` 및 `plot_tire_set_curve_comparison()`에서 정상 피팅 데이터(차속 컬러맵 `●`)와 별도로 제외 데이터 ① 관성 데드존(`L0~L1`, 빨간색 `✕`) 및 제외 데이터 ② 초반 과도 스파이크(`L1~L3`, 주황색 `△`)를 분리 표시하고, 초기 과도 포함 Fit(보라색 파선 `--`)과 초기 과도 제외 최종 Fit(빨간색 실선 `—`)을 동시 오버레이 비교 (`04_BRK_TRANSIENT_INCLUDED_VS_EXCLUDED_COMPARISON.png` 등 생성 완료)<br/>• **VBO 날짜 파싱 3중 안전망(`datetime_helper.py`) 및 `CombinerEstimator` v4.1 정합**: ① 2-1단계 동계 시험 도메인 게이트(`snow`/`winter`/`핀란드`/`utac` 경로 감지 시 겨울철 11~4월 우선, 여름철 5~10월 배제), ② 2-2단계 장비 시그니처(`VBox Touch` $\to$ 미국식 `MM/DD`, `[SessionData]`/`Exported` $\to$ 유럽식 `DD/MM`), ③ 6단계 `mtime` 근접도 30일 이내 제한으로 17개 스노우 세션 날짜 불일치 100% 해결. `CombinerEstimator` 저슬립(`0~0.20`) 가중치(`wg=20`)·`TrendLine` 양수 기울기 클램핑(`[0.5, 25.0]`)·원점 `(0, 0)` 직선 보정 완성<br/>• **1:1 코드 매뉴얼(`cf_tire.md` v4.4, `combiner_estimator.md` v4.1, `magic_formula.md`, `datetime_helper.md` v3.46), 도메인 지식 사전(`curve_fit_사전.md`, `file_reader_사전.md`, `models_사전.md`) 및 제동 영구 지식 위키([[31_실차_제동_시작점_자동_탐지_및_과도응답_슬립_복원_공학]]) 동기화 완료** | ✅ 완료 |
> | **v3.45** | 2026-10-19 | uno &<br/>Antigravity | 🎯 **`TireCurve` 해법 C(2단계 강성 구속 단일 MF: `constrained_mf`) 공식 엔진 편입, 사용자 제안 2D 분포 분할 시그모이드 블렌딩(해법 A-v2: `split_blend`) 정식 구현 및 가속(`Snow_ACC_BRK`)·제동(`Snow_BRK_ABS`) 11종 전 케이스 원클릭 통합 리포팅 파이프라인 완결**<br/>• **해법 C (`method="constrained_mf"`) 공식 엔진 탑재 (`cf_tire.py`, `magic_formula.py`)**: 1단계로 저슬립 탄성 영역($0 \le x \le 0.035$)에서 원점 구속 RANSAC(`calc_initial_stiffness`)으로 초기 탄성 강성 $K = \frac{dy}{dx}\big|_{x=0}$를 확정하고, 2단계로 등식 제약 $B = \frac{K}{C \cdot D}$가 주입된 3파라미터 매직포뮬러(`constrained_magic_formula`)를 최적화하여 원점 정합 및 데이터 정중앙 관통을 보장하는 단일 해석 수식 엔진 완성<br/>• **사용자 제안 해법 A-v2 (`method="split_blend"`) 구현 및 전이부 Hump 원천 차단**: 1D 히스토그램 KDE 밀도 능선에서 제어 클러스터 진입 변곡점($x_{\text{kde\_onset}}$)을 포착하여 고슬립 클러스터($x \ge x_{\text{kde\_onset}}$) 데이터만으로 순수 4파라미터 MF($y_{\text{MF\_high}}$)를 독립 피팅한 뒤, 저슬립 직선($y = K \cdot x$)과의 실제 교차점($x_{\text{trans}}$)에서 시그모이드 가중치로 블렌딩함으로써 구형 해법 A의 전이부 상단 불룩함(Hump) 현상을 100% 제거 (`00_TIRE_CURVE_APPROACHES_C_VS_AV2.png` 4분할 정밀 대조 실증)<br/>• **극저속 휠스핀 노이즈 스마트 컷오프 및 단일 런 폴백 방어선 구축**: `TireCurve._extract_data_from_tire()`에 가속 시험 $V \ge 8.0\text{km/h}$, 제동 시험 $V \ge 3.0\text{km/h}$ 및 $0 < x \le 1.0$ 기본 필터링을 적용하여 출발 직후 분모 $V \to 0$에 의한 슬립 폭주 노이즈를 원천 차단하고, 단일 런 아웃라이어 판정 시 전체 검출 런으로 안전 폴백하는 방어 로직 탑재<br/>• **가속(`Snow_ACC_BRK` 8종) 및 제동(`Snow_BRK_ABS` 3종) 전 케이스 원클릭 리포팅 완결 (`example_acc_brk_start_points.py`)**: 전 11개 케이스에 대해 4대 모델(`constrained_mf`, `split_blend`, `combiner`, `least_squares`) 동시 피팅 검증, 세트별 통합 비교 차트(`curve_fit_comparison_Snow_ACC_5-40_AllSets.png`, `curve_fit_comparison_Snow_BRK_40-5_AllSets.png`) 및 정량 요약 CSV(`tire_curve_11cases_summary.csv`) 생성 완료 (Exit Code 0)<br/>• **1:1 코드 매뉴얼(`cf_tire.md` v4.2) 및 도메인 지식 사전(`curve_fit_사전.md`) 동기화 완료** | ✅ 완료 |
> | **v3.44** | 2026-10-19 | uno &<br/>Gemini | 🎯 **`curve_fit` 실차 데이터(제어 몰림 및 초기 급경사) MF 한계 극복 3대 대안(가중 블렌딩, 격자 빈 대표값, 2단계 강성구속 MF) 실증 비교, v1 원본(2025-12-01 커밋) 성공 커브 발굴 대조, 해법 C(2단계 강성구속 MF) 다각도 전수 검증 및 사용자 제안 2D 분포 분할(A 고도화) 아키텍처 정립 (안티그래비티 앱 연계 완결)**<br/>• **3대 대안 수치 비교 실증**: Baseline($K=0.62$, 강성 붕괴) vs 해법 A($K=4.84$, $\mu=0.181$, RMSE 0.0248) vs 해법 B($K=0.59$, 중앙값 상향 왜곡) vs 해법 C($K=4.70$, $\mu=0.176$, RMSE 0.0252)<br/>• **사용자 핵심 피드백 및 물리적 원인 규명**: 해법 A가 전이부($x \approx 0.04\sim 0.08$)에서 데이터 구름 상단을 스치며 위로 불룩해지는(Hump) 현상 규명(초반 0.13g 붕 뜬 Baseline MF 블렌딩 오염), 비닝 미디언(해법 B)이 저슬립 희소성으로 인해 중앙값이 0.14g로 과대평가되는 왜곡 규명, 해법 C가 원점 $(0, 0)$에서 시작하여 데이터 구름 정중앙을 가장 이상적으로 관통함을 확인<br/>• **v1 오리지널 성공 커브(2025-12-01 커밋 8cd7d5b) 발굴 대조**: 과거 성공 커브(`None-7. Curvefit.png`, `None-5. HermiteConnector.png`)의 실체가 횡력 슬립각 데이터(`ID-X55-P33-JF0_raw_raw.pkl`, $K \approx 20.9$, $\mu=0.82g$)였음을 전수 확인하고 거동 비교 기준선 확립<br/>• **해법 C 다각도 전수 검증 완결**: ① 과거 레거시 2종(SDF 횡력 $K=20.88$, VBO 가속 $K=2.03$), ② 실측 스노우 가속 4대 세트(C1: $K=4.57, \mu=0.178g$ / T1: $K=5.32, \mu=0.175g$ / T2: $K=5.64, \mu=0.167g$ / C2: $K=5.72, \mu=0.184g$ 성능 분별력 완벽 확보), ③ 차속 컷오프(4~12km/h) 전 대역 피팅 곡선 단일화 완벽 수렴 실증<br/>• **사용자 제안 2D 분포 분할(해법 A 고도화) 설계**: 2D 데이터 밀도 능선에서 직선-곡선 전이점($x_{\text{trans}}$)을 포착하여 저슬립 직선부와 순수 곡선부 MF를 분리 피팅 후 결합하는 무결점 아키텍처 정립<br/>• 🚩 **안티그래비티 앱 바통 터치 과제 (TODO)**: ① 해법 C의 $B \cdot C \cdot D = K$ 등식 제약 단일 MF 엔진을 `TireCurve` 공식 옵션으로 정식 탑재, ② 사용자 제안 2D 밀도 분기 기반 직선/곡선 분할 블렌딩(해법 A-v2) 프로토타입 구현 및 해법 C와의 1:1 최종 대조 | ✅ 완료 |
> | **v3.43** | 2026-10-18<br/>(야간) | uno &<br/>Gemini | 🎯 **`curve_fit` & `CombinerEstimator` 정밀 결함 추적, v1 오리지널 정통 2D 국소 에르미트 탐색 메커니즘 규명, 직선 쉬프트 버그 해소 및 차속 컷오프(4~12km/h) 5x5 매트릭스 진단 파이프라인 완성 (내일 작업 연계 쟁점 정립)**<br/>• **가속 시험 초반 휠스핀 노이즈($V < 6\text{km/h}$)와 차속 컷오프($V \ge 8\text{km/h}$) 효과 실증**: 슬립율 $0 \sim 278\%$ 폭주 및 분모 $V$ 극소 왜곡을 걷어내는 속도별($2 \sim 20\text{km/h}$) 10단계 피팅 비교 완료. $V \ge 8 \sim 10\text{km/h}$에서 타이어 형상이 가장 이상적으로 정돈됨을 입증<br/>• **v1 오리지널 레거시(`master` 브랜치: `unoUtil/curveFit/CurveCombiner/`) 전수 정밀 대조 분석**: 단위 체계(슬립율 $0 \sim 1.0$, 가속도 $[g]$ $\approx \mu$)가 최초 설계부터 SSOT였음을 주석과 코드로 100% 확인. 종방향 가속도 $Ax$에서 `d2y_nor`의 최저점이 원점에 위치하여 `ind_end_line == 0`으로 조기 탈출하던 v1의 숨은 결함을 규명하고 물리적 하한선($x \ge 0.015$)으로 방어. `clothoid_val = 0.03`의 본래 역할이 에르미트 품질 불량 시의 비상 대피소였으며, 직선 끝점 좌우 국소 구간($\Delta x \approx 0.015 \sim 0.035$)에서 2D 탐색 시 `score < 0.03`으로 에르미트가 본래 100% 정상 채택되었음을 수학적으로 증명<br/>• **직선 쉬프트(Left Shift) 버그 완벽 규명 및 RANSAC `model_line.predict(...)` 직접 적용**: 원점 $(0, 0)$을 강제하려 절편 $c$를 누락하여 발생했던 직선의 좌측 쉬프트를 RANSAC 모델 직접 적용으로 100% 해소하여 3열과 4/5열 직선을 완전 일치시킴<br/>• **에르미트 솟구침($y = 1.958\text{g}$) 원인 규명 및 Fritsch-Carlson 단조성 가드 탑재**: 브릿지가 피크점까지 길어져($\Delta x = 0.36$) $\Delta x \cdot m_0 \approx 5.4$로 폭발하던 Runge 현상을 천이 대역($x \le 0.075$) 캡핑 및 Fritsch-Carlson PCHIP 단조성 제약(기울기 $\le 2.5 \times \Delta y / \Delta x$)으로 원천 차단하여 실제 데이터($0.22\text{g}$) 스케일 안착<br/>• **v2 최신 표준 모듈 체계(SSOT) 준수**: 구형 레거시 명칭을 전면 배제하고 `LeastSquaresEstimator`, `scale_data`, `format_fig`, `LOGGER`로 일원화<br/>• **5x5 매트릭스 진단 차트(`00_COMBINER_STEPS_BY_SPEED_MATRIX_V2_OFFICIAL.png`) 및 11개 전 케이스 종합 비교 차트 갱신 완결**<br/>• 🚩 **내일(출근 후) 집중 검토 및 이어갈 잔여 쟁점 (TODO)**: ① "아직도 이상해": 현재 최종 곡선과 로우 데이터의 결합 부위가 사용자의 시각적/동역학적 기대치와 여전히 미세하게 불일치하는 지점 정밀 청취 (직선 구간의 시작점을 원점 0에서 시작하게 할지, RANSAC의 실제 영점 교차점 $x \approx 0.008$에서 시작하게 할지 등), ② 저슬립 영역의 가속도 데이터가 0 근처에 머무는 구동계 토크 지연 구간과 순수 타이어 탄성 강성 직선 간의 물리적 정합 기준선 확립, ③ 제동(`Snow_BRK_ABS`)과 가속(`Snow_ACC_BRK`)의 상호 간섭 없는 단일 파이프라인 최종 점검 | ✅ 완료 |
> | **v3.42** | 2026-10-18 | uno &<br/>Gemini | 🎯 **`curve_fit` & `acc_brk` 가감속 시작점(Onset) 도함수(Jerk) 융합 정밀화, 0 근처 평형 기저선 노면 떨림 밴드(`ax_smooth <= base_mean + 2*std`) 및 앞뒤 양방향(Bidirectional) Onset 탐색 구축, 시작점 가속도($Ax_{onset}$) 기반 이상치 판정 전면 전환, 콤바이너(Combiner) 초기 선형 강성 직선 복원 및 차속 컬러바 탑재 타이어 세트별 듀얼 모델(Combiner vs LeastSquares) 통합 비교 시각화 완결**<br/>• **타행 감속(Coasting/엔진 브레이크: $-0.02 \sim -0.04\text{g}$) 및 제동 전 가속 기저선 오염 원천 해결**: 제동 전 엑셀 가속 구간($A_x > +0.03\text{g}$)을 기저선 탐색에서 원천 배제하여, 반드시 $A_x \le 0.01\text{g}$ (0 근처 평형 대역)에서 평균(`base_mean`)과 노면 떨림 폭(`safe_std`)을 산출하도록 물리 가드 구축. 가속도가 줄어드는 1차 하강(엑셀 오프)은 무시하고, 유압 브레이크 인가로 급강하하는 Min Jerk 피크($-4.5 \sim -5.0\,\text{g/s}$)에서 역추적하여 평형 떨림 밴드($A_x \le \text{base\_mean} + 2\sigma$)로 진입하는 변곡점 Onset을 정밀 포착<br/>• **앞뒤 양방향(Bidirectional Window) 제동 Onset 탐색 구축**: 운전자가 목표 속도(예: 20kph)에 도달하기 전뿐만 아니라 도달한 직후(미래 0.8초)에 브레이크를 밟은 케이스(`NoABS_20_30_반복.VBB` 등)까지 완벽 포괄하도록 앞뒤 양방향 윈도우 탐색을 적용하여, 평형 구간 한가운데가 엉뚱하게 시작점으로 잡히던 결함을 100% 박멸<br/>• **시작점 순간 가속도($Ax_{onset}$) 기준 아웃라이어 판정 전면 전환**: 운전자의 진입 타이밍에 종속되던 $\Delta t$(시간차) 기준을 완전 폐기하고, 시작점 당시의 가속도가 0 근처 평형 상태($-0.09\text{g} \le Ax_{onset} \le +0.025\text{g}$) 및 그룹 IQR 범위 내에 있는지를 기준으로 불량 런을 칼같이 자동 선별하도록 개편<br/>• **콤바이너(Combiner) 초기 선형 구간(직선) 복원 및 원점 보정**: `ind_end_line == 0` 조기 탈출 버그를 제거하고, 저슬립 대역(0~2%)에서 `LineMaker`가 강건 회귀(RANSAC/ODR) 직선을 항상 추출한 뒤 `Hermite`/`Clothoid`로 접합하고 원점($x=0, y=0$) 연결 직선 보정을 거치도록 파이프라인을 완전 복원<br/>• **타이어 객체(`VTAccBrkTire`) ➔ 추정기(`TireCurve`) 직결 및 전용 `StartPointResult` 객체 구축**: `tire.curve_fit = TireCurve(tire=tire, method="combiner")`로 서브 분석기 패턴 직결. `fit()` 단 1회 호출로 [시작점 복원 ➔ $Ax_{onset}$ 이상치 필터링 ➔ 커브 피팅(기본 Combiner)] 원스톱 자동 완결. `tire.curve_fit.start_point`에 상세표(`.df`), 통계(`.summary`), 아웃라이어(`.outliers`), 줌인 차트(`.plot()`) 캡슐화<br/>• **차속 그라데이션 컬러 매핑(`hue="speed"`) 및 세트별 듀얼 모델(Combiner vs LeastSquares) 통합 비교 시각화 신설**: 로우 데이터에 주행 차속별 그라데이션 컬러 및 컬러바(`시험 차속 (제동: 40→5, 가속: 5→40) [km/h]`) 제공. 신설된 `plot_tire_set_curve_comparison`을 통해 한 피규어에 4개 타이어 세트(C1, T1, T2, C2)의 개별 듀얼 피팅과 전체 세트 오버레이 비교를 6분할로 조망하는 마스터 비교 차트 생성 완료<br/>• **11종 실제 VBB 데이터셋 일괄 재검증 및 차트 갱신 완료**: `Snow_ACC_BRK` 4종(8케이스) 및 `Snow_BRK_ABS` 3종 전체에 대한 파이프라인 무결성 검증 완료 | ✅ 완료 |
> | **v3.41** | 2026-10-18 | uno &<br/>Gemini | 🛰️ **`file_reader` VBO 계측 파일 날짜 파싱 모호성(DD/MM vs MM/DD) 7단계 지능형 판정 파이프라인(`_resolve_ambiguous_header_date`) 구축, 미래 날짜 배제(Future Date Gate) 절대 물리 법칙 탑재 및 12시간제(AM/PM) 파싱 완결**<br/>• **VBO 헤더 유럽식(DD/MM) vs 미국식(MM/DD) 파싱 왜곡 원천 해결**: VBOX 계측기 펌웨어 및 로케일에 따라 `01/06/2026`(1월 6일)이 6월 1일로 오판되던 결함을 숫자 범위 판정(`> 12`), 절대 물리 법칙(파일 시스템 `mtime` 및 오늘 날짜 대비 미래 날짜 배제), 파일명 크로스체크, 형제 파일(Sibling `.vbo`) 포맷 학습, 디렉터리 연/월 토큰 매칭, `mtime` 시간차 최소화, 영국 Racelogic 기본 폴백의 **7단계 스마트 판정 파이프라인**으로 100% 무결하게 해결<br/>• **미래 날짜 배제 절대 물리 법칙 (Future Date Gate) 탑재**: 계측 일시는 파일 시스템 생성/수정 일시(`mtime`) 또는 오늘보다 미래일 수 없다는 대원칙에 따라, 한 후보가 미래 날짜인 경우 유효한 과거 날짜로 즉시 일/월 자동 스왑 확정<br/>• **VBOParser 헤더 스캔 확장 및 12시간제 AM/PM 파싱 지원**: `_extract_save_date`에서 `lines[:120]`까지 스캔 범위를 넓혀 `[SessionData]` 보조 날짜(`Date:`, `Append:`) 크로스체크를 지원하고, `at 01:28:28 PM` 형식의 12시간제 표기를 24시간제(`13:28:28`)로 완벽 변환<br/>• **1:1 기술 매뉴얼(`datetime_helper.md`) 및 8대 엣지 케이스 자가 검증 스위트 완비**: 7단계 판정 파이프라인 아키텍처 다이어그램 및 시나리오 5 예제 코드 반영, `datetime_helper.py` 내 8대 엣지 케이스 단위 테스트 및 실제 `ExampleBrakeStop.vbo` 실측 계측 파이프라인(Shape 8582, 44채널) 연동 100% 무결성 통과 (Exit Code 0) | ✅ 완료 |
> | **v3.40** | 2026-10-18 | uno &<br/>Gemini | 📖 **unoUtil 12대 전 도메인 지식 사전(`[모듈명]_사전.md`) 신설, 템플릿 표준(`_System/Templates/`) 확립, 글로벌 룰북(`PYTHON_CODE_AGENT.md`) 및 감사 스킬 개정 완결**<br/>• **12대 핵심 도메인 지식 사전 구축 완결**: `snow_condition`, `vt_acc_brk`, `curve_fit`, `file_reader`, `signal_process`, `graphics`, `models`, `uncertainty`, `logger`, `gps`, `database`, `ai` 총 12개 전 도메인에 대해 5대 표준 섹션(설계 철학, 배경 이론, 아키텍처 다이어그램, 실전 워크플로우, 트러블슈팅)을 갖춘 `[모듈명]_사전.md` 신설 완료<br/>• **지식의 원자화(Knowledge Atomization) 및 영구 위키(04_Resources) 100% 연계**: 각 모듈 사전에 파편화된 이론을 방치하지 않고, `04_Resources` 내 25개 이상의 공학/물리/수학/아키텍처 영구 지식 노트로 상호 연결망 확립<br/>• **공식 템플릿(`💻 unoUtil_모듈_사전_템플릿.md`) 및 글로벌 거버넌스 헌장 집행**: 코드 매뉴얼 격리 보존 원칙(1:1 소스 매뉴얼)을 유지하면서도 볼트 내 도메인 지식 사전을 의무화하는 법률 제정 및 `code-audit-obsidian-docs` 스킬 동기화 완료 | ✅ 완료 |
> | **v3.39** | 2026-10-17 | uno &<br/>Gemini | 🎯 **`curve_fit` 차세대 3계층 메타 아키텍처(데이터/모델 주입 분리) 전면 재구조화, 3대 추정기(`LeastSquares`, `Optimize`, `Combiner`) 공통 프로토콜 정립, 단일 기준 불변 원칙(Single Baseline) 철저 집행 및 실차 제동 `find_brake_start_point` 완성**<br/>• **"데이터(x, y)와 모델 주입" 기반 3계층 아키텍처 확립**: 타이어 도메인(`tire_curve`)에 종속되어 있던 피팅 엔진들을 순수 수학적 범용 추정기 계층(`unoUtil.curve_fit.estimators`)으로 전면 승격 분리하고, 타이어 공학 지식(원점 구속, 초기 강성 $B \cdot C \cdot D$)을 담은 도메인 래퍼(`cf_tire.py`)와 완벽 분리<br/>• **Base Estimator Protocol (모든 추정기 규격 통일)**: `LeastSquaresEstimator`, `OptimizeEstimator`, `CombinerEstimator` 전원에 대해 `__init__(model_func)`, `.fit(x, y)`, `.predict(x)`, `self.rmse`(평균 제곱근 오차 필수 내장), `.plot(save, close=False)`, `is_fitted` 및 실측 데이터 연동 `__main__` 자가 검증 스위트 100% 장착<br/>• **`CombinerEstimator` 의존성 주입 혁신 및 연산 속도 극대화**: 내부의 `EstimatorMF` 하드코딩을 전면 제거하고, 주입받은 모델로 초기 선형(가중치)과 후반 곡선(가중치)을 분할 최적화하여 새로운 합성 회귀 모델(`Predictor`)을 도출하도록 재설계. 에르미트 접합 2D 탐색 다운샘플링으로 연산 속도를 5분$\to$**0.05초**로 비약적 단축 및 `__iter__` 튜플 언패킹 100% 무중단 호환 보존<br/>• **과도기적 레거시 및 별칭 전수 숙청 (Single Baseline Law 철저 준수)**: `fit_magic_formula`, `EstimatorMF`, `estimatorMF`, `EstimatorLeastSquares`, `MinimizeEstimator`, `FitMinimizeOptimization`, `CurveCombiner` 등 군더더기 별칭/래퍼를 전면 삭제하고 4대 공식 표준 클래스(`TireCurve`, `LeastSquaresEstimator`, `OptimizeEstimator`, `CombinerEstimator`)로 export 단일화 (`hndl_test.py` 등 호출부 전수 갱신)<br/>• **실차 제동 브레이크 시작점 자동 탐지 함수 신규 구축 (`find_brake_start_point`)**: `unoUtil.vehicle.acc_brk.func_acc_brk`에 3중 노이즈 방어(1차 11샘플 평활화 + 정속 1초 기저선 통계 추정 + 5샘플 연속 지속성 검증) 기반 브레이크 시작점 탐색 함수 구현 $\to$ 50km/h 고정 컷으로 잘려나가던 감속도 $0 \to 0.45\text{g}$ 및 슬립율 램프업 구간을 자동 역추적 복원하여 음수 슬립 외삽 클램핑 수평선 결함 원천 해결<br/>• **1:1 기술 매뉴얼 완비 및 실측 데이터 검증 보고서 배포**: `cf_tire.md`, `least_squares_estimator.md`, `optimize_estimator.md`(신규), `combiner_estimator.md`, `func_acc_brk.md` 1:1 매뉴얼 완비 (Code Manual Isolation Law 준수) 및 실측 VBB 데이터 기반 `TIRE_CURVE_FITTING_RESULT.md` 및 `fig/` 고해상도 차트 4종 생성 완료 | ✅ 완료 |
> | **v3.38** | 2026-10-16 | uno &<br/>Gemini | 🏛️ **가감속/제동(`vt_acc_brk`) 설정 가이드(`vt_acc_brk_config_guide.md`)의 `vt_acc_brk.md` 제3대단원 완전 통합 및 파이썬 모듈 1:1 SSOT 매뉴얼 체계 확립 완결**<br/>• **입력 설정 가이드 대단원 신설 및 완전 흡수 (`vt_acc_brk.md`)**: 기존에 별도 분리되어 관리되던 `vt_acc_brk_config_guide.md`의 핵심 내용(3계층 분기 깔때기 아키텍처 다이어그램, 4대 파라미터 입력 형태 규격, 전체 파라미터 상세 명세 및 스마트 디폴트 매트릭스, 물리 부호 자동 정규화 메커니즘, 다중 속도 및 아웃라이어 실전 레시피)을 `vt_acc_brk.md`의 `## 🎛️ 3. 계층형 파라미터 입력 체계 및 스마트 설정 종합 가이드 (Config Guide)`로 온전히 통합<br/>• **중복 파일 삭제 및 코드 매뉴얼 격리 보존 원칙(Code Manual Isolation Law) 정합**: 파이썬 패키지 내부의 파편화된 `vt_acc_brk_config_guide.md`를 영구 삭제하여, `unoUtil` 내 모든 파이썬 모듈이 `*.py` $\leftrightarrow$ `*.md` 1:1 단일 매뉴얼 원칙(SSOT)에 완벽히 부합하도록 정비 완료<br/>• **문서 목차 구조 일원화**: `1. 개요 및 3계층 아키텍처` $\to$ `2. 최상위 함수 인터페이스` $\to$ `3. 계층형 파라미터 입력 종합 가이드 (신설)` $\to$ `4. 유틸리티 함수 인터페이스` $\to$ `5. 실무 활용 시나리오` $\to$ `6. 표준 네이밍 및 Flat 저장 구조`로 일목요연하게 재정렬 | ✅ 완료 |
> | **v3.37** | 2026-10-16 | uno &<br/>Gemini | 🛠️ **가감속/제동(`vt_acc_brk`) 역직렬화·온디맨드 복원·캐시 소거 로깅 아키텍처 개편 및 INFO(상태 요약)/DEBUG(상세 데이터) 역할 완전 분리 완결**<br/>• **터미널 수백 줄 도배 원천 해소 및 INFO/DEBUG 계층화**: 프로젝트 및 타이어 역직렬화(`__setstate__`) 시 `tire_analyzers`와 `result.df` 전체를 덤프하여 콘솔을 수백 줄 도배하던 레거시 디버그 출력을 정리하고, 평상시에는 1줄 요약 브리핑(`INFO`), 상세 데이터 스펙 및 명판은 디버깅 모드(`DEBUG`)에서만 표출되도록 계층화 분리<br/>• **`VTAccBrkProject` 로깅 개편 (`vt_acc_brk_project.py`)**: `__setstate__` 시 `INFO`로 `[{prj_name}] 프로젝트 역직렬화 로드 완료 (타이어 {n}개: {t_keys})` 한 줄 요약만 출력하고, 수백 줄의 `tire_analyzers` 상세 명판은 `DEBUG` 모드로 완전 격리. `restore_cache` 호출 시 `INFO`로 `[{prj_name}] 전체 프로젝트 캐시 복원 완료` 출력<br/>• **`VTAccBrkTire` 로깅 개편 (`vt_acc_brk_tire.py`)**: `__setstate__` 시 `[result.df] 캐쉬 상태 : None` 2회 중복 출력을 제거하고 `DEBUG` 모드 1줄로 단정하게 정리. `result` 프로퍼티 온디맨드 복원 및 `restore_cache` 시 `INFO`로 `[Memory] {set}[ACC/BRK Test] : 대용량 캐시 복원 완료`, `DEBUG` 모드 시 실제 복원된 `result.df`의 `Shape` 및 `Columns` 상세 출력. `clear_cache` 시 `INFO`로 삭제 완료, `DEBUG`로 소거 상태(`df=None`) 확인 출력<br/>• **`calc_response` 가속/제동 Rising 슬라이싱 IndexError 핫픽스 및 `excel=False` 안전 방어**: `func_acc_brk.py`에서 가속/제동 초기 라이징 구간(`rising_target`) 탐색 시 목표 도달 데이터가 없어 발생하던 `IndexError: index -1 is out of bounds for axis 0 with size 0` 결함을 빈 매칭(`matched.empty`) 가드 및 차수별 `continue` 방어선으로 완벽 해결. `vt_acc_brk.py`의 `excel=False` 실행 시 `excel_raw` NoneType AttributeError 가드 탑재<br/>• **기본 로거 레벨 최적화 (`INFO`) 및 실무 파이프라인 실증**: `vt_acc_brk_project.py`와 `vt_acc_brk_tire.py`의 모듈 로거 기본 레벨을 `logging.INFO`로 정합하여 스노우 노면 특성 분석 파이프라인(`a_make_SnowSurfaceCharacteristic_DF.py`) 실행 시 터미널 가독성 극대화 (실제 `251230_snow_surface_20-5.pjt` 로드 및 온디맨드 복원 실증 완료) | ✅ 완료 |
> | **v3.36** | 2026-10-16 | uno &<br/>Gemini | ⚙️ **가감속/제동(`vt_acc_brk`) 폴더 $\to$ 속도/모드 $\to$ 타이어 3계층 파라미터 분기 단일 표준화 (`resolve_hierarchy_param`), 서브 분석기 스마트 디폴트·부호 자동 동기화(Auto-Sign Alignment) 및 종합 설정 매뉴얼(`vt_acc_brk_config_guide.md`) 완결**<br/>• **단일 표준 3계층 분기 엔진 구축 (`resolve_hierarchy_param`)**: 기존의 비대칭이던 `make_path_dict`와 `get_tire_value`를 단 하나의 일관된 SSOT 함수로 단일화 $\to$ `[1. 폴더/노면]` $\to$ `[2. 속도 조건(vel_tag) / 시험 모드(mode)]` $\to$ `[3. 타이어 시편(tire_set)]` 우선순위로 파라미터를 정밀 매핑하고 기존 함수는 호환 래퍼로 100% 하위 호환 보존<br/>• **서브 분석기 9대 파라미터 계층 분기 정식 편입**: `response_target`, `rising_target`, `vel_split`, `pre_sec`, `col_mudrop_wheelacc`, `col_slip_pdf_wheelslip`, `slip_range`, `slip_mode_vel_range`, `col_slip_mode_wheelslip` 등 서브 분석기 설정 전원을 `config_all_dict` 및 `tire_dict_maps`에 정식 등록하여 폴더별·속도별·타이어별 독립 분기 완비<br/>• **스마트 디폴트 및 물리 부호 자동 동기화 (Auto-Sign Alignment)**: `response_target` 미입력 시 현재 속도 방향에 맞춰 제동 `[-0.5, -0.2]`, 가속 `[0.2, 0.5]` 자동 분기 및 양수 `[0.2, 0.6]` 입력 시 제동 모드 음수 자동 반전 탑재 (`func_acc_brk.py`, `an_response.py` 공통 방어선 구축). `vel_split` 미입력 시 `test_vel`의 중간값으로 자동 스마트 계산 ([100,0] $\to$ 50.0, [20,35] $\to$ 27.5)<br/>• **입력 설정 종합 가이드 매뉴얼 완결 (`vt_acc_brk_config_guide.md`)**: 소스 코드 저장소 직하위에 4대 입력 형태(단일값, 모드별 dict, 폴더별 dict, 타이어별 복합 dict), 전체 파라미터 매트릭스, 스마트 디폴트 로직, 4대 실무 실전 코드 레시피를 집대성한 가이드라인 구축 완료 (Code Manual Isolation Law 준수)<br/>• **자가 진단 스위트 전수 통과**: Case 7(신규 계층 분기 실증), Case 1(Mock 제동 파이프라인), Case 2(다중 프로젝트 병합), Case 6(실무 VBB 가속 풀링 배치) Exit Code 0 무결성 통과 | ✅ 완료 |
> | **v3.35** | 2026-10-16 | uno &<br/>Gemini | 🏷️ **가감속/제동(`vt_acc_brk`) 통합 표준 네이밍 시스템 및 Flat(단일 계층) 저장 구조 구축, 메타데이터 `vel_range` 정규화 및 기술 백서(`vt_acc_brk_모듈_네이밍룰.md`) 확립 완결**<br/>• **식별자-파일명-차트 타이틀 1:1 완전 일치 원칙 (Single Stem Law) 집행**: 타이어 객체 표준 식별자 `[req]_[surface]_[item]_[cond]_[vel_tag]_{set}` 조립 및 `self.tire_name` 프로퍼티 신설, `.tir` 파일명 및 차트 이미지명/타이틀 완전 일치. 프로젝트 객체 3단계 우선순위(1순위: `pjt_name` $\to$ 2순위: 메타데이터 조합 $\to$ 3순위: `{최하위폴더명}_{item}_{vel_tag}`) 조립 및 `self.project_name` 프로퍼티 신설, `.pjt` 파일명 및 프로젝트 비교 차트 이미지명/타이틀 완전 일치<br/>• **단일 계층(Flat) 저장 아키텍처 전면 개편**: 과거 파일명 중복 방지용 임의 하위 폴더(`0. db/brk_100-5/` 등) 완전 폐지 $\to$ `0. db/`, `2. fig/`, `3. result/` 직하위 단일 계층에 정갈하게 보관<br/>• **속도 구간 메타데이터 `vel_range` / `vel_tag` 체계 공식 편입 (`test_infor_res.py`)**: `TestInformation`에 `vel_range` 필드 공식 추가, 리스트(`[100, 5]`) 및 문자열(`'100-5'`, `'20-35'`) 유연한 정규화 파서 탑재, `vel_tag` 프로퍼티 및 `METADATA_MAP['vel_range'] = 'TestVelRange'` 연동으로 요약 테이블 자동 표기<br/>• **오케스트레이터 및 시각화 전 도메인 정합**: `vt_acc_brk.py`에서 `curr_test_vel` 속도 조건을 `tire_infor['vel_range']`에 직통 주입, 캐시 로드(`load_tire`, `load_pjt`) 시 플랫 디렉토리 내 `vel_tag` 스마트 매칭 지원. `plotter_tire.py`, `plotter_project.py`의 `get_path()`, `get_title()` 표준 식별자 Stem 기반 1:1 매칭 연동<br/>• **전용 기술 헌장 및 매뉴얼 완결**: 볼트 프로젝트 폴더 내 **[[50_vt_acc_brk_표준_네이밍_규칙_및_저장_구조|표준 네이밍 룰]]** 영구 기술 백서 신설 (종합 매트릭스, Flat 구조도, 실무 로드 레시피 수록) 및 코드 1:1 매뉴얼(`vt_acc_brk.md`, `vt_acc_brk_tire.md`, `vt_acc_brk_project.md`), 독스트링 Google Style 100% 동기화 완료 | ✅ 완료 |
> | **v3.34** | 2026-10-15 | uno &<br/>Gemini | 🏎️ **가감속 속도 구간 분할 모듈(`segments.py`) 신설, acc_brk 속도 구간 모듈화 선행 리팩토링 및 `04_Resources` 영구 지식위키 거버넌스 전면 개편 완결**<br/>• **`unoUtil.signal_process.post_process.segments` 신규 구축**: 단조성 검사 기반 가감속 속도 구간 분할 알고리즘, 분할 경계 미세시간 선형 보간($\le 1\text{ms}$) 엔진 공식 탑재 (409줄 구축, `segments.py`) 및 마스터 MOC 8번 도메인 공식 편입<br/>• **`acc_brk` 및 `post_process` 속도 구간 모듈화 선행 리팩토링 (`e62e284`)**: `filters.py`, `outliers.py`, `resample.py`, `scaler.py` 및 6대 서브 분석기(`an_acceleration`, `an_mu_drop`, `an_response`, `an_skewness`, `an_slip_pdf`, `an_split_speed`), 코어 오케스트레이터(`func_acc_brk`, `vt_acc_brk*`, `plotter_*`) 총 47개 파일 9,101 라인 대대적 정합 및 속도 대역 모듈화 선행 완료<br/>• **`12_파이썬_소프트웨어_아키텍처_및_엔지니어링` 전용 지식 허브 신설**: 대규모 패키지 모듈화 및 무중단 아키텍처([[10_대규모_파이썬_패키지_모듈화_및_무중단_아키텍처]]), 엔터프라이즈 계층형 로깅 및 Non-blocking 시각화([[20_엔터프라이즈_계층형_로깅_및_무중단_시각화_패턴]]), 대용량 시계열 인메모리 프록시 및 비파괴 슬림 피클링([[30_대용량_시계열_인메모리_프록시_및_비파괴_캐싱_패턴]]) 3대 핵심 아키텍처 수립<br/>• **`13_시계열_신호처리_공학` 전용 지식 허브 신설**: Zero-Phase 필터링 및 위상지연 극복([[10_Zero_Phase_필터링_및_위상지연_극복_공학]]), 1D 웨이블렛 변환 디노이징 및 피크 G 보존([[20_1D_웨이블렛_변환_디노이징_및_피크_보존_수학]]), 적응형 KDE 고속화([[30_적응형_커널_밀도_추정_KDE_및_초고속_알고리즘]]), 다변량 이상치 탐지 및 속도 구간 분할([[40_다변량_센서_이상치_탐지_및_시계열_리샘플링_공학]]) 4대 마스터 위키 완결<br/>• **`21_제동` 30번 단일 마스터 백서 확립 및 구버전 파편 4종 영구 삭제**: 기존 40~43번 파편 문서 4종을 완전히 삭제하고, 오직 **[[30_실차_가감속_성능변화_분석_및_보정_시스템]]** 단 1개의 완결된 백서로 일원화 (콘트롤 타이어 시계열 조각 선형 보간, Polarity 상대 성능지수, 노면온도 감인성 m/℃, GPS 2포인트 공간QC, Mu-Drop 손실거리 분석 등 핵심 공학 이론 100% 보존)<br/>• **`11_회사_실차평가_데이터프레임` 계측 스키마 슬림화**: 승격 완료된 모듈화·로깅·신호처리·보정 중복 문서 4종을 안전 정리하고, VBOX/VBB/Dewesoft 계측 규격 및 표준 DataFrame 스키마([[00_실차평가_데이터프레임_통합_색인]])로 정체성 확립 | ✅ 완료 |
> | **v3.33** | 2026-10-14 | uno &<br/>Gemini | 🧹 **가감속/제동(`unoUtil.vehicle.acc_brk`) 전 도메인 레거시 연결·구버전 함수·과도기 별칭 전면 삭제 및 v2 순수 단일 표준(Single Baseline) 완결**<br/>• **불필요 브릿지/임시 파일 및 레거시 캐시 폴더 영구 삭제**: `correct_factors.py`, `correct_factors.md`, `yaml_test.py`, `legacy/` 디렉토리 및 구버전 `.pyc` 캐시 전수 삭제<br/>• **v2에서 대체 완료된 구버전(v1) 중복 함수·메서드 8종 전면 삭제**: `func_acc_brk.py` 및 `correct.py`의 `calc_braking`, `calc_acceleration`, `calc_kmeans`, `calc_partial_hydro`, `calc_reference_corrected`, `find_reference_tire`, `reorder_columns`와 `VTAccBrkProject.correct_control_tire` 삭제 (`calc_acc_brk`, `Correct.run` 단일 엔진으로 완전 일원화)<br/>• **패키지 전역 레거시 리다이렉트 및 대문자/구버전 별칭 전면 철폐**: `unoUtil/__init__.py`, `vehicle/__init__.py`, `acc_brk/__init__.py`, `analyzers/__init__.py` 및 14개 모듈 하단의 `_BRKTest_`, `ACCBRK`, `VT_ACCBRK*`, `AN_MEMORY`, `CORRECT`, `Cal_Control`, `PLOTTER_TIRE`, `PLOTTER_PROJECT`, `AN_*`, `PP_*`, `save_pjt`, `add_list_tire`, `plot_all`, `plt`, `flag_print`/`bool_print` 프로퍼티 등 모든 레거시 연결고리 100% 제거<br/>• **레거시 `**kwargs` 흡수 로직 제거 및 시그니처 순수화**: 전 모듈에서 `df_raw`, `df_input`, `print`, `flag_print`, `only_braking`, `sr`, `effNum` 등 과도기 인자 흡수 블록을 제거하고 `data: pd.DataFrame`, `bins: int = 100`, `level` 등 순수 v2 표준 시그니처로 정합 (`vt_acc_brk_tire.py` Case 4 `FileDataReader` 정합 포함)<br/>• **12종 1:1 기술 매뉴얼(`.md`) 전수 최신화 및 레거시 섹션 삭제**: `base_memory.md`, `correct.md`, `func_acc_brk.md`, `vt_acc_brk*.md`, `plotter_*.md`, `analyzers/an_*.md`의 시그니처·파라미터·반환 스키마를 실제 코드와 1:1 동기화하고 하위 호환성 섹션 전면 삭제 (전 모듈 단위 테스트 Exit Code 0 통과) | ✅ 완료 |
> | **v3.32** | 2026-10-13 | uno &<br/>Gemini | 🏎️ **가감속/제동(`vt_acc_brk`) 프로젝트 다중 타이어 비교 시각화 엔진(`plotter_project.py`) 가속 시험(Acceleration) 양수(+) 물리 부호 정합 및 속도 대역 정렬 완결**<br/>• **가속도 분포 차트(`compare_acceleration`) 가속 모드 양수 보존 및 정렬 완합**: 제동 전용 시절 하드코딩된 `-1 *` 부호 반전으로 인해 가속 시험 데이터($+0.16g$)가 음수($-0.16g$)로 거꾸로 그려지던 결함을 모드 판별(`mode == 'acc'`)을 통해 원시 양수 물리 부호 그대로 보존하도록 교정하고, 속도 구간 정렬을 가속 모드 시 저속$\to$고속 순방향(`reverse=False`, 예: 20_30 $\to$ 30_35)으로 자연스럽게 표시<br/>• **구간별 가속도 및 성능 지수 차트(`compare_split_acceleration`, `compare_index_split_acceleration`) 양수 정합**: 고속/저속 구간 가속도(`col_acc_high`, `col_acc_low`) 바 차트 및 지수 텍스트 라벨에서 `-1 *` 강제 반전을 제거하여 가속 시험 시 0 기준 위쪽(양수 막대)으로 정확히 렌더링되도록 개선 및 수직 텍스트 정렬(`va = 'bottom' if val >= 0 else 'top'`) 방어 구축<br/>• **가속 응답성 상승 기울기(`compare_rising_slope`) 물리 부호 정상화**: 시스템 응답성 비교 시 `mode == 'acc'`일 때 양의 상승 기울기($+g/\text{s}$)를 유지하도록 분기하여 음수 축소 결함 해결<br/>• **가속(Case 6) 및 제동(BMW 320d Dry) 듀얼 실측 시각화 검증 통과**: 스노우 가속 시험의 Acceleration Distribution($+0.16\sim +0.18g$), Split Acceleration($+0.17\sim +0.18g$) 양수 출력 및 제동 시험의 감속도 크기 양수 비교 정상 표출 100% 동시 검증 완료 | ✅ 완료 |
> | **v3.31** | 2026-10-13 | uno &<br/>Gemini | 🗺️ **GPS 로컬 직교 좌표계(`GPStoXYCord`) 시험장 자동 감지, 1000Hz$\to$100Hz 고속 보간 매핑(15ms)을 통한 좌표 슬라이싱 데이터 유실 버그 해결 및 테크노링 직선 시험로 회전각(`rotate = -0.4°`) 기하학적 정합 완결**<br/>• **1000Hz 리샘플 결과(`_result.df`) $\to$ 100Hz 원본 계측(`self.df`) 좌표 슬라이싱 버그 원천 해결 (`vt_acc_brk_tire.py`)**: `self.df[col] = self._result.df[col]` 단순 인덱스 슬라이싱으로 인해 10배 차이나는 행 개수(52,702 vs 527,011)로 앞쪽 10%(52초)만 복사되고 90% 데이터가 증발하던 치명적 결함을 시간 축(`Datetime`/`Time`) 기준 1D 고속 선형 보간(`np.interp`, 단 15ms)으로 완벽 해결 $\to$ T1~T4 모든 타이어의 가속 및 제동 궤적/유효 런(0~8) 100% 온전 복원<br/>• **GPS 시험장 프리셋 인접 자동 판별 기능 신규 탑재 (`GPStoXYCord.detect_preset`, `from_infer`)**: `local_pos=None` 지정 시 데이터 첫 지점 위경도를 기반으로 사내 시험장(테크노링, 테크노트랙 등)을 $\pm 0.05^\circ$ 반경 내에서 자동 감지하여 프리셋 좌표(`reflong`, `reflat`, `rotate`)를 자동 주입하는 편의성 제공<br/>• **Racelogic VBOX 포맷 음수 경도(-7580 분) 부호 보정 로직 보존 및 무결성 검증**: `01_C1.VBO` 실측 검증을 통해 `to_decimal_degrees`의 음수 경도 반전 처리와 정상적인 $+126.3353^\circ$ 변환 동작 재확인<br/>• **테크노링 직선 시험로 회전각 `rotate = -0.4°` 수학적/물리적 증명 및 시각화 검증 완료**: 트랙이 진북 대비 서쪽으로 기울어진 방위각 $\phi = -0.4^\circ$에 대해, 2D 회전 변환 행렬 적용 후 각도 $\phi_{new} = \phi - \theta$ 수식을 기하학적으로 증명 $\to$ 원래 트랙 각도를 빼줌($- (-0.4^\circ)$)으로써 $+0.4^\circ$ 적용 시 2배로 누워버리는 현상($-0.819^\circ$)을 배제하고, `-0.4°` 적용 시 잔여 각도 $-0.019^\circ$로 수직 기준선($X=0$)에 오차 $\pm 3\text{cm}$ 이내 칼같이 수직 정렬됨을 실측 데이터 1:1 비교 검증 완료 (`rotation_comparison_final.png`)<br/>• **가속/제동 전체 파이프라인 무결성 회복**: 예제 6번 등 프로젝트 단위 가속 시험 및 제동 시험에서 모든 타이어의 유효 런과 루프 형상 궤적이 정상 가동됨을 최종 검증 | ✅ 완료 |
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
> | **v3.20** | 2026-10-08 | uno &<br/>Gemini | 🏆 **SnowCorrectionModel 기본 주력 모델 SVR 공식 승격 및 RF / KNN 3대 모델 전수 하이퍼파라미터 그리드 서치(Grid Search) 최적화 기본값 반영**<br/>• **기본 모델 SVR 공식 승격**: `SnowCorrectionModel` 초기화 시 `target_model='SVR'` 및 `c_run_snow_correction_pipeline.py` 기본값을 `'SVR'`로 일원화 확정 (RBF 커널 $C=2.0, \gamma=0.07, \epsilon=0.10$으로 외삽 말림 0% 및 연속 매끄러운 물리 곡면 보장)<br/>• **Random Forest 그리드 서치 최적 규격 기본화**: `max_depth=4, min_samples_leaf=3, min_samples_split=6, n_estimators=100` 탑재 $\to$ 과적합/단차를 제거하고 외삽($h \ge +3.5\text{mm}$)에서도 $+0.56\text{m}$ 정상 양수 유지, 실차 복원 MAE $0.872\text{m} \to \mathbf{0.426\text{m}}$ (**+51.2% 개선**), $R^2: 0.580 \to \mathbf{0.831}$<br/>• **KNN Regressor 그리드 서치 최적 규격 기본화**: `n_neighbors=10, weights='distance', p=1` (Manhattan Distance) 탑재 $\to$ 기존 러프 평활화($k=30$, MAE $0.636\text{m}$) 대비 비약적 향상, 실차 복원 MAE $0.872\text{m} \to \mathbf{0.419\text{m}}$ (**+51.9% 개선**), 순위 보존도 Kendall $\tau=\mathbf{0.472}$ (3대 모델 중 최고 순위 보존력)<br/>• **타이어 스펙별 복원 거동 무결성 검증**: 의뢰 25RD110006EF의 C1~T4 전수 1:1 대조로 2차 온습도 상승($\Delta AH \approx +1.02\text{ g/m}^3$)에 따른 전 타이어 일관된 차감 보정($-0.6\sim -0.7\text{m}$) 무결성 확인 및 T1, T2의 실측 역주행 원인(타이어 고유 패턴 특성/1차 런 노이즈) 규명 완결 | ✅ 완료 |
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
>         V["🏎️ vehicle_test/ (실차 시험 & 동역학: acc_brk / circuit)"]
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
| **🏎️ vehicle_test** | [[vt_acc_brk_사전\|가감속/제동 사전]]<br/>[[circuit_사전\|서킷/핸들링 사전]] | 실차 시험 공통 베이스(`BaseProject`/`BaseTire`), 가감속/제동 동역학, 서킷 랩/섹션 분할 및 조향 지연/CTE 분석 | [[30_실차_가감속_성능변화_분석_및_보정_시스템\|실차 가감속 백서]]<br/>[[24_유노유틸_파일리더_표준채널명\|표준 채널 명세서]] |
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

## 🏎️ 3. vehicle_test 실차 시험 & 동역학 (acc_brk / circuit) 도메인

> 📑 **Dashboard(웹 대시보드) 심층 개발 보고서 허브 (MOC)**: [[00_dashboard_보고서_통합_색인|🖥️ 50_dashboard 보고서 통합 색인 바로가기]]
> • [[2026-11-05_v3.82_가감속제동_인터랙티브_웹대시보드_구축_및_스노우가속_표준속도정합_종합개발보고서|10. 가감속/제동(acc_brk) 통합 인터랙티브 웹 대시보드 구축 및 스노우 가속 표준 속도(5-40) 정합 종합개발보고서]]
>
> 📑 **Response(과도 응답성) 심층 검증 보고서 허브 (MOC)**: [[00_response_보고서_통합_색인|⏱️ 30_response 보고서 통합 색인 바로가기]]
> • [[2026-10-30_v3.71_Response_시작점탐지_WSS딜레이복원_적응형구간_알고리즘전면재설계_검증보고서|10. 가속·제동 휠 딜레이 보정 및 과도 응답(Response/Rising) 알고리즘 고도화 및 실측 검증 보고서]]
>
> 📑 **Mu-Drop(마찰 저하 분석) 심층 검증 보고서 허브 (MOC)**: [[00_mu_drop_보고서_통합_색인|🛞 40_mu_drop 보고서 통합 색인 바로가기]]
> • [[2026-10-30_v3.71_MuDrop_피칭보정_영위상추세선_오실레이션포락선_알고리즘고도화_검증보고서|10. Mu-Drop 강건(Robust) 분석 알고리즘 고도화 및 실측 검증 보고서: 피칭 보정 · 영위상 추세선 · 오실레이션 포락선]]

> [!NOTE]- 🏎️ vehicle_test 실차 시험 공통 베이스, acc_brk 및 circuit 모듈 소스 코드 목록 [클릭하여 펼치기]
> | 모듈 / 서브패키지 | 핵심 기능 및 역할 | 소스 코드 (Repo) |
> | :--- | :--- | :---: |
> | **`BaseProject`** | 실차 시험 다중 타이어 취합, 기준(Control) 타이어 성능 보정 및 지수화 공통 베이스 | [`base_project.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle_test/base_project.py) |
> | **`BaseTire`** | 단일 타이어 계측 시계열 데이터 캡슐화, 채널 매핑 및 시험 차수 분석 공통 베이스 | [`base_tire.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle_test/base_tire.py) |
> | **`VehicleDynamic`** | 실차 센서 장착점 ➔ 차량 무게중심(CG) 운동역학 변환 및 롤/피치 보정 | [`vehicle_dynamic.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle_test/vehicle_dynamic.py) |
> | **`test_infor_res`** | 평가 정보(`TestInformation`) 및 결과(`TestResult`) 메타데이터 컨테이너 | [`test_infor_res.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle_test/test_infor_res.py) |
> | **`param_resolver`** | 시험 파라미터 표준화 및 레거시 매핑 리졸버 | [`param_resolver.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle_test/param_resolver.py) |
> | **`sensor_sync`** | GPS/CAN/이종 센서 타임스탬프 동기화 및 리샘플링 | [`sensor_sync.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle_test/sensor_sync.py) |
> | **`excel_report`** | 실차 시험 종합 분석 결과 다중 시트 엑셀 보고서 일괄 출력 유틸리티 | [`excel_report.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle_test/excel_report.py) |
> | **`CircuitCutpoint`** | 서킷/트랙 GPS 좌표 기반 자동 판별 및 랩/섹션 분할선 게이트 관리 (`circuit`) | [`circuit_cutpoint.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle_test/circuit/circuit_cutpoint.py) |
> | **`func_circuit`** | 서킷 조종안정성 13대 물리 연산 함수군 (랩분할, 조향지연, K_us, MF/RF 피팅, CTE 등) | [`func_circuit.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle_test/circuit/func_circuit.py) |
> | **`vt_acc_brk`** | 가감속/제동 자동화 파이프라인 마스터 오케스트레이터 (`cf_*` 3계층 패스스루, 표준 네이밍: [[50_vt_acc_brk_표준_네이밍_규칙_및_저장_구조|표준 네이밍 룰]], 1:1 매뉴얼: [`vt_acc_brk.md`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle_test/acc_brk/vt_acc_brk.md)) | [`vt_acc_brk.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle_test/acc_brk/vt_acc_brk.py) |
> | **`vt_acc_brk_tire`** | 단일 타이어 동역학 분석, Wavelet 가속도 복원, 7대 서브 분석기(`curve_fit` 내장) 및 원천 데이터(`tire.df`) 시험 라벨링 | [`vt_acc_brk_tire.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle_test/acc_brk/vt_acc_brk_tire.py) |
> | **`vt_acc_brk_project`**| 다중 타이어 취합, 콘트롤 타이어 시계열 선형 보간 및 `curve_fit` 보정 지수(`index_cf_*`) 산출 엔진 | [`vt_acc_brk_project.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle_test/acc_brk/vt_acc_brk_project.py) |
> | **`correct`** | 시험 환경(온도, 노면) 프로파일(`correct_factor_basic`), 콘트롤 타이어 시계열 성능 지수 보정 및 `curve_fit` 게인($G_i$) 동기화 (`Correct`) | [`correct.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle_test/acc_brk/correct.py) |
> | **`base_memory`** | 대용량 실차 시계열 데이터 초고속 인메모리 관리 및 슬림 피클링 (`BaseMemory`) | [`base_memory.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle_test/acc_brk/base_memory.py) |
> | **`func_acc_brk`** | 가감속/제동 13대 핵심 동역학·신호처리·슬립·수막·응답성 계산 함수군 | [`func_acc_brk.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle_test/acc_brk/func_acc_brk.py) |
> | **`analyzers` (6대 서브) + `curve_fit`**| 가속대역, 감속응답, 슬립속도PDF, Mu-Drop, 왜도, 구간속도분할 및 Magic Formula 커브 피팅(`TireCurve`) 7대 전문 서브 분석기 | [`analyzers/`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle_test/acc_brk/analyzers/) |
> | **`plotter_tire` / `plotter_project`** | 단일 타이어 9대 분석 차트(`PlotterTire`: `curve_fit`, `curve_fit_detail` 포함) 및 프로젝트 9대 비교 플로터(`PlotterProject`: `compare_curve_fit` 포함) | [`plotter_tire.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle_test/acc_brk/plotter_tire.py) · [`plotter_project.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle_test/acc_brk/plotter_project.py) |
> | **`dashboard` (acc_brk)** | 미래형 다크 홀로그램 스타일 가감속/제동 통합 인터랙티브 웹 대시보드 (`dashboard_app.py`) | [`dashboard_app.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/vehicle_test/acc_brk/dashboard/dashboard_app.py) |

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
> • [[2026-10-21_v3.60_CurveFit_가속_WSS시간지연물리보정_발진궤적복원_종합보고서|10. 휠 속도 시간 지연(Time-Delay) 물리 보정 및 커브 피팅 종합 보고서]]
> • [[20_타이어_커브피팅_전면_개발스토리_및_공학검증보고서|20. 타이어 커브 피팅 전면 고도화 개발 스토리 및 물리/공학 검증 종합 보고서]]
> • [[25_실차_계측데이터_태생적_문제점과_8단계_통합파이프라인_백서|25. 실차 계측 데이터의 태생적 문제점과 tire_curve 8단계 통합 파이프라인 백서]]
> • [[2026-10-22_v3.66_CurveFit_제동_Jerk시작점_4대랜드마크위상정렬_과도분리_스노우웻지_종합개발보고서|26. 실차 제동 타이어 커브피팅 알고리즘 고도화 종합 개발 보고서]]
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
> | **`outliers`** | 이상치 자동 검출 및 연속 결측 구간 정제 | [`outliers.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/signal_process/post_process/outliers.py) |
> | **`segments`** | 가감속 속도 구간 분할(Speed Segments), 단조성 검사 및 정밀 시간 보간 엔진 | [`segments.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/signal_process/post_process/segments.py) |
> | **`scaler`** | MinMax, Standard, Robust 시계열 신호 정규화 | [`scaler.py`](file:///D:/uno/Python/Projects/unoUtil/unoUtil/signal_process/post_process/scaler.py) |
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

### [2026-11-13] v4.02 - 가감속/제동 대시보드(dashboard_app.py) Load & Combination 탭 파일 관리 테이블 UI/UX 개편 및 Tire 탭 런 상세 테이블 규격 일원화
- **파일 선택 테이블 실시간 사파이어 블루 네온 하이라이트 탑재 (`dashboard_app.py`)**:
  - `style_tire_run_dataframe` 함수에 `col_valid: str = "Valid"` 매개변수를 추가하고, `target_col` 동적 판정 로직을 탑재하여 타이어 런 테이블(`Valid`)과 계측/객체 파일 테이블(`선택`)을 모두 아우르는 단일 표준 스타일러로 확장.
  - 선택된 파일 행은 선명한 사파이어 블루 네온(`background-color: #0E4F8B; color: #F0F9FF; font-weight: bold;`), 제외된 파일 행은 어두운 슬레이트(`background-color: #090D14; color: #475569;`)로 대비 렌더링.
  - `st.session_state` 내 `raw_files_interactive_editor` 및 `obj_files_interactive_editor`의 `edited_rows`를 실시간 주입하여 체크박스 조작 즉시 화면 하이라이트가 즉각 반응하도록 구현.
- **Tire 탭 런 상세 테이블 형태 및 선택열 너비 100% 정합**:
  - 익스팬더 타이틀을 `📋 계측 파일 관리` 및 `📋 객체 파일 관리`로 직관적 단축 정비.
  - 컬럼 비례 너비 및 반응형 최적화: `선택` 열에 `pinned=True, width=100`을 부여하여 한글 헤더 라벨("선택")과 체크박스가 여유롭고 안정적으로 표출되면서도 Glide Data Grid의 잔여 여백 균등 분배(`grow: 1`)를 원천 차단하고 초소형 폭으로 좌측에 완벽 고정. `크기 (MB)`(85px) 열도 헤더 잘림 없이 최소 폭으로 축소하고, `폴더명`(650px) 열이 화면 창 크기 확대 시 발생하는 남는 공간을 시원하게 흡수하도록 반응형 황금 비율 레이아웃 확립, `파일명`(220px) 열 넉넉 배치.
  - 컴포넌트 키 갱신(`raw_files_interactive_editor_v4`, `obj_files_interactive_editor_v4`): 브라우저 로컬 메모리에 남아있던 이전 마우스 수동 드래그 기억 상태를 완전히 리셋하여 새 비율 규격(선택 100px, 폴더명 650px, 파일명 220px, 크기 85px)이 화면에 즉시 100% 강제 반영되도록 정합.
- **사이드바 사이버틱 HUD 테크 그리드 배경 및 3단 수평 구획(Top/Mid/Bottom Zone) 전면 개편 (`_get_dashboard_css`)**:
  - 좌측 사이드바 전체 배경에 메이저 60px + 마이너 20px 2중 사이버틱 HUD 테크 그리드 패턴(`rgba(56, 189, 248, 0.22/0.09)`) 및 코발트 방사형 글로우 그라디언트(`#0A1E3F` ~ `#020710`)를 주입하여 사이버틱 입체 텍스처를 대폭 강화하고, 우측 메인의 실차 홀로그램 캔버스와 확연히 차별화되는 미래형 콕핏 컨트롤 텍스처를 확립하고 우측 구분선 완전 삭제.
  - 상단 프로젝트 선택 상자와 하단 데모 버튼 박스를 답답했던 상하 네모칸을 완전히 철거하고 사이드바 가로 156px 전폭을 활용하는 **3단 수평 구획(Top Zone: 62px 프로젝트 구획 / Mid Zone: 5대 탭 그리드 구획 / Bottom Zone: 60px 데모 구획)**으로 전면 개편. 상단은 86px 높이로 시원하게 확장하여 아이콘을 제거하고 [활성 프로젝트] 순수 라임 테마 네온 타이틀(#BEF264)을 중앙 정렬하고 셀렉트박스 입력창과 수직 층간(Vertical Tier)을 완벽 분리 배치하며, 마우스 호버 시 상세 헬프 툴팁 안내를 지원하고, 콘솔창에 [✕] 원클릭 즉시 소멸 닫기 버튼 장착 및 Matplotlib 메인스레드 안내 경고 원천 필터링을 완결하고, 메인 패널 최상단 제목 행에 왼쪽과 동일한 2중 사이버틱 HUD 테크 그리드 배경을 가진 독립 헤더 카드(studio-top-header-card)를 구축하여 기존의 거대한 40px 마진 section-divider 수평선 및 불필요한 공백 줄을 완전 삭제함으로써 제목과 요약 정보가 상하 대칭 12px 패딩 안에서 수직 정중앙(Vertical Center)에 정확히 안착하도록 정합하였으며, 146px 전폭 셀렉트박스로 프로젝트명 1줄 가독성을 극대화하며, 하단은 70px씩 전폭을 할당하여 데모 버튼 글씨가 2줄로 꺾이던 현상을 100% 원천 박멸.
  - 중간 5대 아이콘 탭은 상하 엣지 팟과 균형 잡힌 갭(`top: 68px; bottom: 68px;`)을 유지하며 화면 세로 중앙에 모여 있는 원래 배치를 100% 보존하고, 시그니처 더블 쉐브론(`>>`) 화살표도 완벽 유지.
  - 타이어 테이블과 동일하게 `hide_index=True`를 제거하고 `disabled=["_index"] + [c for c in df.columns if c != "선택"]`을 적용하여 행 순번 인덱스(0, 1, 2...) 노출 및 정돈된 테이블 룩앤필 확립.
  - 테이블 높이를 타이어 런 상세 테이블과 동일한 240px(`height=240`)로 규격화.
- **[전체 선택] / [전체 해제] 시 data_editor 캐시 세션 리셋**:
  - 일괄 선택 및 해제 버튼 클릭 시 세션 키를 안전하게 초기화(`pop`)하여 이전 `edited_rows` 잔여 상태로 인한 깜빡임 방지 및 즉각 동기화 완결.
- **1:1 순수 기술 매뉴얼(`dashboard_app.md`) 최신화 및 py_compile 무결성 통과**:
  - 공개 API 레퍼런스 표에 `style_tire_run_dataframe` 시그니처 및 확장 명세 반영, 파이썬 바이트코드 컴파일 100% 통과.

### [2026-11-12] v4.00 - 서킷 및 조종안정성(Handling) 전면 리팩토링, 3대 공식 시험장 실데이터 파이프라인 완결 및 가감속 대시보드 v2.0 고도화 완결
- **8대 공통 코어 아키텍처 완성 (`unoUtil.vehicle_test`)**:
  - `BaseMemory`, `Correct`: 최상단 승격 완료.
  - `BaseTire`, `BaseProject`: 신규 객체지향 기반 클래스 구현 및 `VTAccBrkTire`, `VTAccBrkProject`, `VTCircuitTire`, `VTCircuitProject` 공통 상속 완결.
  - `VehicleDynamic`: 조향 기어비(`gear_ratio`) 반영 전륜 타이어 슬립각(`ReferSlipFrontTire`) 산출 및 횡하중 이동(`calc_load_transfer_lateral`) 확장.
  - `sensor_sync`: GPS 차속 vs CAN 휠속 2-Tier 스마트 동기화 엔진 구축 (수동 `delay_ms` 최우선 지원).
  - `param_resolver`: 노면 ➔ 모드 ➔ 시편 3계층 자동 해석기 구축.
  - `ExcelReportBuilder`: 기업 표준 서식 다중 시트 엑셀 보고서 공통 빌더 완비.
- **서킷 6대 물리 서브 분석기 구축 (`circuit/analyzers/`)**:
  - `AnLapTime`: 랩 및 코너 섹션 주행시간, IQR 이상치 필터링, 주행 일관성 지수.
  - `AnSteeringDelay`: 영점교차 + 미분피크 결합 및 MAD 3.0 조향 응답 지연 (Ay, Yaw).
  - `AnUndersteerGradient`: 선회 횡가속도 대 조향각 선형 언더스티어 구배($K_{us}$) 및 Pacejka MF / Random Forest 비선형 피팅.
  - `AnYawGainStability`: 정상 선회 요레이트 게인 및 코너 탈출 요진동 감쇄 안정성 지수.
  - `AnGripLimit`: 피크, 평균, p95 한계 선회 횡가속도 그립 통계.
  - `AnRacingLine`: 기준 랩 대비 k-d Tree 기반 부호형 교차 궤적 편차(Signed CTE).
- **가감속/제동 대시보드 (`dashboard_app.py`) v2.0 고도화 및 실시간 콘솔 스트리머 완성**:
  - `StreamlitLiveConsole` 로그 심각도 정밀 판정(`_classify_line`, `has_warning`) 도입으로 경고(WARNING, 노랑)와 오류(ERROR, 빨강)를 분리하고 4색 뱃지/보더 실시간 전환.
  - 파일 업로드 및 데이터 경로 정규화: 웹 드래그앤드롭 시 최신 배치 추출(`_extract_latest_upload_batch`, `_normalize_uno_upload_relpath`) 및 수동 경로 입력 시 즉각적인 시그니처 해제·메타데이터 재파싱(`_pending_lc_meta_override`) 연동.
  - 스피너 컨테이너(`spinner_slot`)와 실시간 콘솔 슬롯 분리, 예외 메시지 가시화 및 속도 대역 미검출(`all_empty`) 시 친절한 원인/해결 가이드 경고 표출.
  - PyCharm 디버거 몽키패치 해제 및 Streamlit 서브프로세스 런처(`launch_dashboard`) 안정성 확보.
- **최상위 원스톱 파이프라인 래퍼 (`vt_circuit.py`) & 실무 진입점 제공**:
  - 5줄 코드로 파일 스캔, 멀티프로세싱 병렬 전처리, 6대 물리 분석, 컨트롤 타이어 시계열 선형 보간 및 엑셀 리포트 일괄 출력 완결 (`WetHD/Main.py`, `example_circuit.py`).
- **VBO 파서 1열 시프트 버그 원천 해결 (`index_col=False`)**:
  - `vbo_parser.py` 내부 `pd.read_csv`의 `index_col=False` 누락으로 인한 90개 컬럼 1열 밀림 및 시간 파싱 오류를 완벽 박멸.
- **3대 공식 시험장 실계측 데이터(18개 VBO) 엔드투엔드 검증 100% 통과**:
  - 한국테크노링(6 VBO, 62개 지표), 스페인 IDIADA(6 VBO, 62개 지표), 독일 페어츠펠트(6 VBO, 70개 지표) 전원 랩/섹션 분할 및 보정 완결 (Exit Code 0).

### [2026-11-12] v3.90 - unoUtil.vehicle ➔ unoUtil.vehicle_test 대개편, 공통 베이스 프레임워크(BaseProject/BaseTire) 구축, 서킷/핸들링 시험 모듈화(circuit/) 착수 및 가감속 대시보드 v2.0 홀로그램 UI 탑재
- **`unoUtil.vehicle` ➔ `unoUtil.vehicle_test` 공식 패키지 승격 및 Clean Architecture 재정립**:
  - 실차 시험 종합 도메인으로 위상을 확립하고 `unoUtil/__init__.py`에서 `vehicle_test` 공식 노출 및 하위 호환 매핑 완료. `analysis_test_data.py`, `hndl_test.md` 등 과도기 레거시 파일 정리 및 소멸.
- **실차 시험 공통 베이스 프레임워크 구축 (`base_project.py`, `base_tire.py`, `param_resolver.py`, `sensor_sync.py`, `excel_report.py`)**:
  - 단품 타이어 객체(`BaseTire`) 및 프로젝트 단위 취합/지수화 베이스(`BaseProject`)를 신설하여 향후 제동(`acc_brk`)과 서킷(`circuit`) 전반에 공통 객체지향 추상화 제공.
- **서킷 및 조종안정성(Handling) 전용 모듈화 신설 (`unoUtil.vehicle_test.circuit`)**:
  - `circuit/` 패키지 신설, `func_circuit.py`(Haversine 거리, GPS 누적거리, 랩/섹션 자동 분할 `calc_lap_section_split`, 조향 응답 지연 `calc_steering_delay_zero/derivative`, 언더스티어 구배 `calc_understeer_gradient`, Pacejka MF / Random Forest 커브피팅, 요레이트 게인/안정성, 한계 그립 통계, Signed CTE 편차, Cohen's d, 시그모이드 점수화 등 13대 물리 연산 함수 완비), `circuit_cutpoint.py`(`CircuitCutpoint` 클래스: 한국테크노링, 스페인 이디아다, 독일 페어츠펠트, 파펜부르크 등 GPS 좌표 기반 서킷 자동 식별 및 랩/코너 섹션 컷포인트 피클 로더 구축).
- **가감속/제동 대시보드 (`dashboard_app.py`) v2.0 정식 업데이트 및 미래형 다크 홀로그램 UI/UX 완성**:
  - 2,500여 줄의 대규모 고도화, `acc_brk_hologram_bg.jpg` 배경 및 글래스모피즘 네온 UI/UX, Streamlit 1.50 최신 컴포넌트 최적화, 런 편집 인터랙션 및 시각화 저장 연동.
- **대규모 실차 시험 계측 데이터셋(VBB, VBO) 수납 및 체계화**:
  - 스노우 가감속 지그재그(`snow_acc_brk/25RD120007EF/` run1/run2 C1, C2, T1, T2) 및 유럽/국내 주요 핸들링 서킷(IDIADA, Pferdsfeld, Technoring 각 T1~T6 18개 VBO) 계측 데이터 수납 완료.

### [2026-11-06] v3.86 - unoUtil 대시보드 Streamlit 1.50 최신 엔진 승격, 실시간 다크 콘솔 스트리머 전 구간 탑재 및 집에서 이어서 작업할 4대 수정 레시피

# 🛠️ 메인 버튼 이중 렌더링 박멸, 사이드바 5대 고유 아이콘 복원 및 Tire 탭 상시 체크/재분석 UI 계획

## 1. 스크린샷 정밀 분석 및 결함 원인 (Root Cause Analysis)

사용자께서 첨부해 주신 스크린샷(`clipboard-1793948886968.png`)을 정밀 분석하여 4대 결함의 원인을 100% 명확히 규명했습니다:

### 📍 [결함 1] 메인 버튼([재분석], [타이어 저장])이 2개씩 쌍둥이로 복제되어 보이는 현상
- **원인 규명**:
  - CSS에서 `div[data-testid="stFormSubmitButton"]` (부모 컨테이너)와 그 자식 `button` **둘 다에게** `width: 175px`, `border: 1.6px solid ...`, `background: linear-gradient(...)` 스타일을 걸어버렸습니다.
  - 그 결과 부모 div도 알약 버튼 모양으로 그려지고, 자식 button도 알약 버튼 모양으로 그려져서, **버튼 1개가 2개로 복제되어 나란히 서 있었던 것**입니다!
- **해결 방안**:
  - 부모 div(`stFormSubmitButton`)의 배경과 테두리를 완전히 투명화(`background: transparent !important; border: none !important;`)하고, **오직 실제 `button` 요소에만 단일 스타일을 적용**하여 이중 복제 현상을 100% 박멸합니다!

---

### 📍 [결함 2] 사이드바 모든 버튼이 Tire 아이콘으로 덮어씌워지고 데모 버튼에도 침범한 현상
- **원인 규명**:
  - Streamlit 1.50에서는 각 버튼마다 개별 `div.stButton` 래퍼로 감싸져 있어서, 모든 버튼이 자신의 부모 입장에서 **무조건 `:nth-of-type(1)`** 이었습니다.
  - 이로 인해 마지막으로 적용된 `Tire` 아이콘 규칙이 사이드바의 1번~5번 메뉴 버튼과 데모 버튼 2개까지 **총 7개 버튼 전체에 일괄 덮어씌워진 것**입니다!
- **해결 방안 (고유 앵커 직결 바인딩)**:
  - 파이썬 코드에서 5대 메뉴 버튼 바로 앞에 고유 앵커(`sb-nav-anchor-1` ~ `sb-nav-anchor-5`)를 주입하고,
  - CSS에서 인접 형제 선택자(`div:has(> .sb-nav-anchor-N) + div button::before`)로 1:1 직결 매핑하여:
    - 1번: `Information` 아이콘
    - 2번: `Load & Combination` 아이콘
    - 3번: `Tire` 아이콘
    - 4번: `Project` 아이콘
    - 5번: `Save` 아이콘
    이 단 1개의 오차도 없이 각자의 고유 아이콘으로 정확하게 복원되며, **데모 버튼에는 앵커가 없으므로 아이콘이 일절 침범하지 않습니다!**

---

### 📍 [결함 3] 사이드바 하단 데모 버튼 바닥 밀착 레이아웃 복원
- `제동데모`와 `가속데모`를 `st.columns(2)`로 가로 1줄에 50%씩 깔끔하게 나란히 안착.

---

### 📍 [결함 4] Tire 탭 테이블: Information 탭과 동일하게 '런 편집' 토글 제거 & 상시 체크박스 및 대제목 옆 [선택 런 재분석] 일체형 UI 전환
- **사용자 요구사항**:
  - "타이어 탭 테이블 수정 방식과 표시 방식을 지금 Information 탭처럼 변경해줘: **그냥 바로 선택 체크/해제할 수 있고, 선택 런 재분석 버튼을 만들어 선택한 런들에 대해 재분석할 수 있게!**"
- **구현 방안**:
  1. `[ ] 런 편집` 토글 체크박스를 **완전히 삭제**합니다.
  2. 테이블은 **상시 `st.data_editor`로 렌더링**되어 첫 번째 열 `Valid`의 체크박스를 마우스로 즉시 체크/해제할 수 있습니다. (나머지 열은 읽기 전용 보호)
  3. 상단 헤더 1줄 레이아웃:
     `[테이블 ({sel_tire_key} 런별 상세 결과)]  [⚡ 선택 런으로 재분석]  ----------------  [⛶ 새창 확대]`
  4. 테이블에서 체크박스를 수정하자마자 **대제목 바로 옆에 초록색 네온 `[⚡ 선택 런으로 재분석]` 버튼이 뙇! 활성화**되어 원클릭으로 선택된 런들만 즉시 재연산됩니다!
  5. 테이블 밑에 불필요한 줄바꿈이 전혀 생기지 않아 화면이 극도로 쾌적해집니다!

---

## 2. 검증 계획 (Verification)
1. 메인 화면에서 `[재분석]` 및 `[타이어 저장]` 버튼이 2개가 아니라 **단 1개로 깔끔하게 렌더링되는지 확인**.
2. 사이드바의 5대 메뉴 버튼이 각각 고유한 아이콘(Information, Load, Tire, Project, Save)으로 정상 복원되는지 확인.
3. 사이드바 데모 버튼에 원형 아이콘이 침범하지 않고 깔끔한 직사각형 버튼으로 바닥에 안착되는지 확인.
4. Tire 탭에서 토글 체크박스 없이 테이블의 `Valid` 체크박스를 바로 껐다 켤 수 있고, 대제목 바로 옆의 `[⚡ 선택 런으로 재분석]` 버튼으로 즉시 재분석되는지 확인.
5. 단위 테스트 스위트(`--test`) 100% 통과 확인.


---

### [2026-11-06] v3.85 - unoUtil.vehicle.acc_brk AnResponse 연산 75% 고속화, correct.py DataFrame 단편화 경고 박멸, 5대 save_* 및 plot 파라미터 직교 분리 및 기본값 False 단일 표준화, 시스템 코어 자동 감지 스마트 병렬화(n_jobs=-1) 탑재 및 0.db 분기 생성 완결
* **`AnResponse` 알고리즘 병목 규명 및 75% 연산 가속 (`func_acc_brk.py`)**:
  - `calc_response` 내부에서 75만 행 전체 시계열 필터링을 런별 유효 슬라이스(`idx_start:idx_end` + 패딩) 1회 사전 필터링으로 개편하고 중복 `pd.concat` 블록을 1회로 통합.
  - `AnResponse` 분석 소요 시간을 **2.36초 ➔ 0.58초 (약 75% 시간 단축, 4배 가속)**로 단축하고 수치 지표(`sys_response_time: 0.137`, `sys_rising_time: 0.23`, `sys_rising_slope: -3.862`) 100% 동일성 검증 완료.
* **`correct.py` DataFrame 파편화 경고(`PerformanceWarning`) 원천 소멸**:
  - Control 보정 루프에서 컬럼 개별 insert 방식을 딕셔너리 수집 후 `pd.concat` 1회 일괄 병합(Batch Concat)으로 전면 리팩토링하여 경고 0건 및 메모리 복사 오버헤드 박멸.
* **5대 `save_*` 및 `plot` 파라미터 직교 분리 및 기본값 `False` 단일 표준화 (`vt_acc_brk.py`)**:
  - `save_file`(캐시 .gz), `save_tire`(타이어 .tir), `save_pjt`(프로젝트 .pjt), `save_result`(결과 테이블 .csv 3종), `save_plot`(차트 이미지 .png), `plot`(화면 창 띄우기) 기본값을 모두 `False`로 통일.
  - `plot=False, save_plot=True` 조합 시 GUI 팝업 없이 백그라운드 무음 저장이 가능하도록 완비.
  - 모든 `save_*` 옵션이 `False`일 때 `check_path(dir_db)` 무조건 호출 결함을 수정하여 `0.db`, `1.figure`, `2.result` 폴더가 단 하나도 남지 않는 완전한 클린 인메모리 실행 보장.
* **코어 수 자동 감지 기반 스마트 병렬 모드(`n_jobs: int = -1`) 탑재**:
  - 파이썬 내장 `os.cpu_count()`(현재 PC 12코어) 기반으로 단일 타이어는 오버헤드 없는 순차 실행, 2개 이상 타이어는 `ProcessPoolExecutor` 멀티프로세싱 동시 병렬 처리 가속 탑재.
  - 실측 VBO 2개 데이터(C1, T1) 기반 순차(`n_jobs=1`) 대비 병렬(`n_jobs=2`) 수치 오차 0.000000 완전 일치 검증 완료.
* **하위 모듈(`VTAccBrkTire`, `VTAccBrkProject`) 기본값 전수 통일 및 1:1 기술 매뉴얼 동기화**:
  - `VTAccBrkTire.run` 및 `VTAccBrkProject.run` 시그니처와 구현에서 `save_result=False`, `plot=False`를 일괄 정합하고 소스 코드 저장소 내 1:1 기술 매뉴얼(`vt_acc_brk.md`, `vt_acc_brk_project.md`, `vt_acc_brk_tire.md`) 100% 동기화 완료.

---

### [2026-11-12] v3.87 - unoUtil.vehicle.acc_brk 온디맨드 캐시 복원 시 서브분석기 지표 소실 원천 방지(_get_synced_tire_summary), 기준 타이어 자동 판정 마스크 무결성 확립(_find_reference_tire), 프로젝트 정렬 다형성 지원 및 Streamlit 대시보드 UI/UX 대규모 최적화
* **서브분석기 요약 지표 자동 복원 및 동기화 (`vt_acc_brk_project.py`, `vt_acc_brk_tire.py`)**:
  - 온디맨드 캐시 복원(`result.df` 재생성) 또는 요약 테이블 갱신 시 `_result.summary`의 이전 값을 선제 백업 및 보존.
  - 하위 서브분석기(`acceleration`, `split_speed`, `slip_pdf`, `mu_drop`, `slip_mode`, `sys_response`, `curve_fit`)에 보존된 `_summary` 컬럼이 누락된 경우 이를 감지하여 자동 복원·병합하는 `_get_synced_tire_summary()` 신설.
  - `update_summary()`에서 모든 타이어 요약 컬럼의 합집합(`all_cols_ordered`)을 보존하여 특정 타이어의 부분 컬럼 누락 시에도 전체 지표가 증발하지 않도록 안전장치 구축.
* **기준/콘트롤 타이어 자동 판정 마스크(`_find_reference_tire`) 무결성 확립 (`vt_acc_brk_project.py`)**:
  - `ref_kwd` 매칭 시 모든 타이어가 기준 타이어 키워드에 매칭되는 경우(예: T1~T4 시험 세트에서 `ref_kwd='T'`), 첫 번째 행만 대표 기준 타이어로 지정하여 나머지 시험 타이어가 중복 콘트롤로 간주되어 숨겨지는 결함 해결.
  - `mask_result = (~mask_ref_tire) | (~mask_ref_tire.duplicated(keep='first'))`로 원본 데이터의 인덱스 순서를 100% 보존.
* **프로젝트 정렬 다형성 지원 및 시각화 마스크 동기화 (`vt_acc_brk_project.py`)**:
  - `sort()` 메서드의 `order` 파라미터에 딕셔너리뿐만 아니라 리스트/튜플(`Union[Dict[str, int], List[str], tuple]`) 입력을 지원하여 순서 리스트 전달 시 1부터 순차 가중치를 자동 부여.
  - 정렬 완료 후 정렬된 `summary_all` 및 `summary` 인덱스에 맞추어 `mask_ref_tire`와 `mask_summary`를 필수 동기화하여 `PlotterProject`의 모든 프로젝트 비교 차트가 정렬된 순서 및 인덱스를 정확히 바라보도록 정합.
* **`correct.py` 및 `plotter_project.py` 안정성 강화**:
  - `correct.py`에서 `analyzer._result.summary`를 직접 갱신하여 불필요한 시계열 재복원 연산 오버헤드 차단 및 `TestTireSet` 컬럼 비교 시 문자열 타입 캐스팅 통일.
  - `plotter_project.py`의 `_plot_slip_ratio`에서 `slip_pdf.pdf` 및 `summary`가 유효하게 존재하는 타이어 세트만 동적 필터링하여 빈 데이터로 인한 크래시 방어.
* **Streamlit 웹 대시보드 UI/UX 및 렌더링 최적화 (`dashboard_app.py`)**:
  - `st.data_editor` 실시간 편집 상태(`edited_rows`) 즉시 감지 및 셀 사파이어 블루 하이라이트 스타일러(`style_tire_run_dataframe`) 탑재.
  - 테마 최적화: 250KB Base64 배경 및 SVG 스타일을 해시(`_static_theme_hash`) 기반으로 브라우저 부모 창 `head`에 1회만 주입하여 리런 깜빡임 및 지연 극소화.
  - 폴더 선택 다이얼로그 연동(`_on_click_browse_tire_save_dir`, `_on_click_browse_save_tab_dir`).
  - Tire 탭 & Project 탭: 별도 편집 체크박스 없이 즉시 편집 + [⚡ 선택 런으로 재분석] 일체형 1줄 UX, 타이어 그래프 설정을 `st.tabs` 규격으로 정돈, 타이어 DND 순서 정렬 안정화.

### [2026-11-06] v3.86 - unoUtil 대시보드 Streamlit 1.50 최신 엔진 승격, 실시간 다크 콘솔 스트리머 전 구간 탑재, n_jobs=-1 병렬 가속 완벽 호환 및 3단 Flexbox 무결점 UI 완성
* **Streamlit 1.50 최신 엔진 승격 및 st.data_editor 단일 표준화**: 구버전(1.22)의 무거운 리페인팅 병목을 타개하고 고속 바이너리 통신 엔진으로 승격, 런 편집 100% 정상 작동 보장.
* **실시간 다크 콘솔 스트리머 전 구간 탑재**: 파이참 터미널을 열 필요 없이 대시보드 화면 내에 독립 윈도우 스타일의 다크 터미널을 띄워 원본 로그를 실시간 스트리밍.
* **스마트 고정 프로그레스 바 탑재**: HTML 태그 노출 버그를 순수 압축 HTML로 회피하고, 콘솔창 하단 고정 네온 바에서 게이지가 제자리에서 솩솩 차오르는 완벽한 터미널 룩앤필 완성.
* **TestVelRange 갱신 버그 해결 및 런 테이블 하이브리드 UI 구축**: update_tire_runs에서 속도 변경 시 메타데이터를 즉각 동기화하도록 수정. 대제목 옆 [✏️ 런 편집] 토글 및 [⚡ 선택 런으로 재분석] 버튼 일체형 하이브리드 UX 완성.
* **멀티코어 병렬 가속 완벽 유지 및 피클·컨텍스트 에러 100% 영구 차단**: vt_acc_brk.__globals__ 직접 타겟팅 및 StreamlitSafeThreadPoolExecutor 구현으로 피클/컨텍스트 에러 물리적 차단 및 use_container_width 경고 박멸.
* **Modern CSS Flexbox 3단 레이아웃 정규화 및 차트 이미지 저장 기능 탑재**: position:fixed 조상 전파 결함을 완전 철거하고, 제동데모와 가속데모를 바닥 좌우 대칭(1줄)으로 완벽 밀착 복원. 차트 확대 창 헤더 메뉴에 고해상도 PNG 원클릭 다운로드 기능 탑재.

### [2026-11-05] v3.82 - unoUtil.vehicle.acc_brk 통합 인터랙티브 웹 대시보드(Streamlit) 신규 구축, 5대 네온 메달리온 UI 및 다크 홀로그램 글래스모피즘 테마 완성, 온디맨드 렌더링·인터랙티브 런 편집·드래그앤드롭 정렬 탑재, 플로터 12×6 표준화 및 Tire 탭 파라미터 승계 결함 핫픽스
> 📑 **상세 종합 개발 보고서**: [[2026-11-12_v4.00_대시보드_v2.0_실시간콘솔_경로정규화_안정화_종합개발보고서|가감속/제동 대시보드 v2.0 실시간 콘솔 스트리머·경로 정규화 및 런처 안정화 종합개발보고서]] · [[2026-11-05_v3.82_가감속제동_인터랙티브_웹대시보드_구축_및_스노우가속_표준속도정합_종합개발보고서|가감속/제동 통합 인터랙티브 웹 대시보드 구축 및 스노우 가속 표준 속도(5-40) 정합 종합개발보고서]]

* **대시보드 전용 독립 서브패키지 신설 (`unoUtil/vehicle/acc_brk/dashboard/`)**:
  - `dashboard_app.py` (약 5,300+ 라인의 인터랙티브 대시보드), `dashboard_app.md` (순수 GFM 1:1 기술 매뉴얼), `acc_brk_hologram_bg.jpg` (배경 이미지)를 `acc_brk/dashboard/` 서브패키지로 독립 수납.
  - 외부 볼트 파일 경로 의존성을 완전히 제거하고 패키지 내부 상대경로를 1순위로 로드하도록 설계하여, 옵시디언 볼트가 없는 다른 PC나 배포 환경에서도 모듈과 `dashboard/` 폴더만 있으면 100% 자가 구동 가능하도록 완성.
* **5대 네온 원형 메달리온 UI 및 다크 홀로그램 글래스모피즘 테마 완성**:
  - 좌측 사이드바: 5대 메뉴(Information, Load & Combination, Tire, Project, Save) 원형 메달리온 아이콘을 코드 내장 SVG(Base64)로 탑재. 평상시 Dimmed(투명도 0.42, 흑백 채도), 마우스 호버 및 선택 시 네온 라임 하이라이트와 본문 방향을 가리키는 `>>` 더블 셰브론 인디케이터 장착.
  - 상단 헤더: `Acceleration / Braking Studio` (블루 네온) & `Analysis Tool ver 1.0` (라임 그린) 헤더 및 좌측 패널 최상단 `프로젝트` 선택창 정렬.
  - 전경 위젯 글래스모피즘: 입력창, 테이블, 대제목 리본에 반투명 다크 스모크 글래스(투명도 68~80%)를 적용하여 배경의 홀로그램 스포츠카와 6대 HUD 차트가 자연스럽게 투과되는 일체형 텔레메트리 뷰 구축.
  - 175px 파란색 알약형 메인 액션 버튼(`정보변경`, `분석 실행`, `객체 불러오기`, `통합 / 병합 실행`, `재분석`, `그리기`, `보정 적용`) 우측 끝 수직 밀착 일원화.
* **초고속 인터랙티브 컴포넌트 & 온디맨드 시각화 체계**:
  - **Tire 탭 런별 선별 테이블 (`_TIRE_RUN_TABLE_HTML`)**: `st.data_editor`의 잦은 리런 및 체크 상태 초기화 버그를 해결한 커스텀 컴포넌트 탑재. 유효 런(Valid=True) 행 0ms 실시간 사파이어 블루 하이라이트 및 `[재분석]` 클릭 시에만 서버 재연산 수행.
  - **Project 탭 순서 정렬 (`_DND_TIRE_HTML`)**: 마우스 드래그 앤 드롭으로 타이어 표시 순서를 즉시 재배열하고 `[정렬 반영]` 클릭 시 요약표와 차트에 일괄 반영.
  - **온디맨드 [그리기] 렌더링**: 그래프 옵션 변경 시의 불필요한 자동 재렌더링을 차단하고, `[그리기]` 버튼 클릭 시에만 Matplotlib 차트를 생성하여 세션 메모리에 캐싱.
  - **전문 인터랙티브 새 창 뷰어 (`_inject_chart_new_window_hook`, `Blob URL`)**:
    * 팝업 차단기를 100% 우회하는 Blob URL + 링크 트리거 방식으로 어떤 브라우저에서도 차단 없이 독립 새 창 오픈.
    * 창 크기에 맞춘 화면 가득 꽉 찬 뷰(Fit to Screen) 기본 렌더링.
    * 마우스 휠 부드러운 연속 줌인/줌아웃 (0.15배 ~ 15.0배 자유 스케일링).
    * 마우스 드래그를 통한 상하좌우 패닝 이동 (grab/grabbing 커서).
    * `Shift + 마우스 드래그` 또는 `[⛶ 부분 확대]` 버튼으로 사각형 영역을 지정하여 해당 파형 구간만 화면 전체에 꽉 채우는 박스 줌(Box Zoom) 탑재.
    * 더블클릭 화면 맞춤 리셋, 1:1 원본 해상도 뷰, 실시간 배율 표시 배지, ESC 키 닫기 완비.
* **플로터 규격 12×6 (2:1 비율) 일괄 표준화 및 런 넘버링 배지 오버레이**:
  - `plotter_tire.py`, `plotter_project.py`, `cf_tire.py`의 기본 도화지 크기를 `12 x 6` 와이드 비율로 통일하고 긴 1줄 요약 타이틀 자동 개행(`
`) 적용.
  - `PlotterTire.accbrk()`: 각 주행 런에 `#런번호 (수치)` 단일 텍스트 뱃지를 오버레이하고, 유효 런(파랑 `#1D4ED8`)과 제외 런(빨강 `#DC2626`) 색상 구분 및 3단 지그재그(0.62, 0.38, 0.80) 높이 분산 배치로 텍스트 겹침 완전 방지.
* **Tire 탭 재분석 시 파라미터 승계 결함 핫픽스**:
  - `cur_tp['kwargs']` 미조회로 인해 속도 조건 변경 시 `min_sec=0.5s`, `max_sec=15.0s`, `ws=10`이 강제 주입되어 유효 런이 탈락하던 버그를 해결.
  - 기존 분석 파라미터를 우선 승계하고, 엔진 표준 기본값(제동: `min_sec=1.0s`, `max_sec=10.0s` / 가속: `max_sec=25.0s`)을 정상 바인딩하여 런 수 왜곡 원천 차단.

### [2026-11-03] v3.75 - unoUtil.vehicle.acc_brk 실무 제동 데이터 기반 듀얼 보정 모델(Control 시계열 선형 보간 & 노면온도 물리 팩터) 실증 파이프라인 탑재, 3대 실무 예제(Case 8, 9, 10) 구축 및 correct.py 기상 Datetime 병합 결함 핫픽스
* **실무 제동 데이터 기반 듀얼 보정 모델 파이프라인 실증 (`vt_acc_brk.py`)**:
  - 실제 시험 데이터(`test_data/acc_brk/brk/260311_BMW320d_ADAC_Dry`)를 활용하여 사내 표준 가감속/제동 엔진의 2대 보정 모델을 원클릭으로 구동하는 실무 테스트 케이스를 구축.
  - **Case 8 (`case_8_real_braking_control_correction`)**: Control 타이어(C1, C2) 사이의 노면 마찰력 변화(Mu-Drift)를 시계열 1차 선형 보간(`interpolate(method='linear')`)하여 시험 시점 기준 가상 기준값(`adj_refer_brk_mean`)과 제동거리 성능 지수(`index_brk_mean`)를 도출.
  - **Case 9 (`case_9_real_braking_temperature_factor_correction`)**: 시험장 기상 센서의 아스팔트 노면온도(`BRK Dry Asp`)를 결합하고 노면온도 10℃ 변화당 제동거리 1.0m를 보정하는 물리 프로파일(`gain=1.0, step=10.0`)을 적용하여 기준온도 대비 편차(`factor_diff`)와 보정 제동거리(`corr_brk_mean`)를 완벽 산출.
* **기 저장된 프로젝트(`.pjt`) 로드 후 보정 모델 동적 변경 및 즉시 재계산 실증 (`Case 10`)**:
  - 이미 분석 완료되어 `0. db/`에 저장된 `dry_brk_100-5.pjt` 파일을 `VTAccBrkProject().load(..., restore=False)`로 0.05초 만에 초고속 로드.
  - 대용량 원시 데이터(VBO/VBB) 파싱을 다시 수행하지 않고, `project.correct_performance(correct_type='factor', col_factor='BRK Dry Asp', correct_factor='dry')` 호출만으로 보정 방식을 Control에서 Factor로 동적 전환하여 0.1초 만에 전체 결과표를 최신으로 갱신함을 실증 완료.
* **`correct.py` Pandas 2.0+ Datetime dtype 불일치 결함 핫픽스**:
  - `df_summary`의 시계열 인덱스(`datetime64[us]`)와 `df_weather`의 타임스탬프(`datetime64[ns]`) 간 단위 정밀도 차이로 인해 `connect_weather`(`pd.merge_asof`) 시 발생하던 `incompatible merge keys dtype('<M8[us]') and dtype('<M8[ns]')` 결함을 발견하여 사전에 `astype`으로 단위를 통일하도록 정합 완료.

### [2026-11-03] v3.74 - unoUtil.vehicle.acc_brk 유효 세션 선별(sel_mode='max_min') 대칭 절사(Symmetrical Trimming) 단일 표준화 및 1:1 기술 매뉴얼 최신화
* **`_select_best_data` 대칭 절사(Symmetrical Trimming) 알고리즘 구현 (`func_acc_brk.py`)**:
  - 기존 `sel_mode='max_min'` 설정 시 `valid_count`(선택 개수) 파라미터와 무관하게 무조건 최솟값 1개와 최댓값 1개만 제외하던 레거시 동작을 전면 개편.
  - 전체 시험 세션 수가 `valid_count`보다 많을 경우, 상/하단 극단값을 균등하게 제외(`drop_total // 2`)하여 정확히 지정된 개수(`number`)만큼의 유효 세션을 선별하는 대칭 절사(Symmetrical Trimming) 방식으로 직교화.
  - 전체 데이터 수가 부족하거나 `valid_count=None`인 경우, 최소/최대 각 1개를 제외하는 기존 기본 모드로 안전하게 자동 폴백(Fallback).
* **통합 검증 및 단위 테스트 무결성 확인**:
  - 가상 10회 제동 시계열 데이터 및 `calc_acc_brk` 파이프라인 통합 테스트 수행.
  - `valid_count=6` 지정 시 10회 시험 중 상/하단 각 2개씩 총 4개의 극단값(최단/최장 제동거리)을 배제하고 정확히 중앙 6개 유효 런(`EffNum: [0.0, 1.0, 2.0, 5.0, 6.0, 7.0]`)을 선별함을 100% 검증 통과.
* **1:1 순수 기술 매뉴얼 최신화 (`func_acc_brk.md`)**:
  - `calc_acc_brk` 함수의 `sel_mode` 및 `valid_count` 파라미터 명세에 대칭 절사 방식의 구체적 동작 원리 및 폴백 조건을 상세히 기술하여 코드와 문서의 1:1 SSOT 동기화 완료.

### [2026-10-30] v3.73 - unoUtil.vehicle.acc_brk 6대 서브 분석기 4대 계층(params, df, detail, summary) 단일 표준화(SSOT), 8대 동사 헬퍼 get_target_wheels 신설 및 summary_detail 전면 소멸
* **4대 계층 단일 표준화 (Zero-Alias / Zero-Fallback 헌장 집행)**:
  - 6대 서브 분석기(`AnResponse`, `AnMuDrop`, `AnSlipModeSkewness`, `AnSlipPdf`, `AnAcceleration`, `AnSplitSpeed`) 및 `BaseMemory`를 ① `params`(설정값 딕셔너리), ② `df`(순수 시계열, 대용량 캐시 소거 대상), ③ `detail`(회차/바퀴별 1행 상세 진단 요약, 영구 보존), ④ `summary`(전 차수/전 휠 종합 평균 1행 대표 지표, 영구 보존)로 엄격히 역할 분리.
  - 과도기적 별칭(Alias)이나 폴백(Fallback)을 일절 두지 않고, 모든 코드와 소비자 모듈을 단일 표준으로 직교화 정비.
* **8대 표준 동사 헬퍼 `get_target_wheels()` 신설 (`func_acc_brk.py`)**:
  - 단일 공학 물리 규칙에 따라, 사용자가 채널을 수동 지정하지 않는 한 **제동(`brk`)은 무조건 전륜(`Front`: FL, FR)**, **가속(`acc`)은 차량 구동계에 따라 RWD ➔ `Rear`(RL, RR), AWD ➔ `All`, 기본/FWD ➔ `Front`**를 전 분석기(`Response`, `SlipMode`, `SlipPdf`, `MuDrop`, `TireCurve`)가 100% 동일하게 공유하도록 일원화.
* **`AnResponse` 시계열 메타 오염 원천 박멸 및 `detail` 신설**:
  - 시계열 `df`의 수천 행마다 반복 복사되던 스칼라 메타컬럼(`Base_Val`, `Offset_Vel_Base`, `Thresh_Start` 등)을 전면 제거하여 순수 파형만 보존.
  - 회차(Run) x 바퀴(Position)별 1행 상세 진단 메타데이터 테이블(`tire.response.detail`)로 영구 보존하여 `PlotterTire.sys_response()`에서 0초 만에 직접 조회.
* **`summary_detail` 완전 소멸 및 2대 표준 식별자(`Run`, `Position`) 통일**:
  - `AnMuDrop`과 `AnSlipModeSkewness`의 비표준 속성명 `summary_detail`을 코드베이스(`*.py`, `*.md`)에서 100% 제거하고 `detail`로 단일화.
  - 모든 `detail`의 1~2열을 `Run`(`1, 2...` 또는 `'All'`)과 `Position`(`FL`, `FR`, `Front`, `Rear`, `All` 등 7대 표준 키워드)으로 일원화.
* **`BaseMemory` 3중 온디맨드 복원 방어막 수립**:
  - 복원 시도 즉시 선제적으로 빈 DataFrame(`_df`, `_detail`, `_summary`)을 초기화하고, `_is_restoring` 재귀 락(Lock)을 걸어 조기 반환이나 예외 발생 시에도 무한 루프가 원천 차단되도록 설계 (`target_attr_list = ['df']`로 대용량 시계열만 소거).
* **소비자 코드(`PlotterTire`) 정비 및 실차 계측 배치 분석 무결성 검증**:
  - `PlotterTire.sys_response()`가 `detail`에서 런 메타데이터를 직접 조회하도록 직교화하고, `mu_drop()`과 `slip_mode()`의 `detail` 연계를 정합하여 실제 BMW 320d 마른 노면 배치 파이프라인에서 9대 차트 경고 0건, 총 46개 이미지 100% 정상 생성 완료.

### [2026-10-30] v3.72 - unoUtil 4대 핵심 모듈(Response, Mu-Drop, CurveFit 제동/가속) 알고리즘 고도화 보고서 볼트 이관, 시계열 명명 체계 정립 및 볼트 미러링 첨부파일 1:1 계층화 완결
* **Response 전면 재설계 실측 검증 보고서 이관 (`30_response`)**: 저마찰 눈길 발진 역추적 창($\le 3.5	ext{s}$) 및 적응형 기저점($A_{	ext{base}}$), 휠 통신지연/극저속 슬립 복원, $d^2V/dt^2=0$ 1차 과도 피크 및 25~75% 적응형 타겟 대역 응답 지연($\Delta t_{	ext{resp}}$)과 10~90% 라이징 기울기 회귀 실측 검증 보고서([[2026-10-30_v3.71_Response_시작점탐지_WSS딜레이복원_적응형구간_알고리즘전면재설계_검증보고서]]) 입고 및 전용 MOC([[00_response_보고서_통합_색인]]) 구축 완료.
* **Mu-Drop 강건 분석 실측 검증 보고서 이관 (`40_mu_drop`)**: 초기 제동 피칭 다이브 & 리바운드($14\%$ 스팬) 앵커링, 속도 축 등간격 빈($0.5	ext{kph}$) 기반 영위상($ngle H = 0$) 추세선, 차륜 가속도 RMS 듀얼 오실레이션 포락선($Z_{	ext{osc}}$) 및 3D 스무딩 상태 공간 K-Means + DT 분기 속도 실측 검증 보고서([[2026-10-30_v3.71_MuDrop_피칭보정_영위상추세선_오실레이션포락선_알고리즘고도화_검증보고서]]) 입고 및 전용 MOC([[00_mu_drop_보고서_통합_색인]]) 구축 완료.
* **CurveFit 제동 및 가속 듀얼 종합 개발 보고서 체계화 (`20_curve_fit`)**: 가속 휠 딜레이 보정 보고서([[2026-10-21_v3.60_CurveFit_가속_WSS시간지연물리보정_발진궤적복원_종합보고서]])에 대칭하여 제동 전용 Onset 복원·4대 랜드마크($L_0	o L_1	o L_2	o L_3$) 위상정렬·초기 과도 분리 및 스노우 웻지(Snow Wedge) 종합 개발 보고서([[2026-10-22_v3.66_CurveFit_제동_Jerk시작점_4대랜드마크위상정렬_과도분리_스노우웻지_종합개발보고서]]) 신규 입고 및 전용 MOC([[00_curve_fit_보고서_통합_색인]]) 갱신 완료.
* **볼트 미러링 첨부파일 계층화 및 시계열 명명 표준(SSOT) 확립**: `_attachments/{폴더경로}/{문서명}/` 거울 구조 확립, 미사용 고아 이미지(228개) 비파괴 격리(`_미참조_보관/`), 다중 참조 이미지 독립 복제 및 전수 검증 깨진 링크 0건(351개 이미지 100% 정상 작동) 무결성 완결.

### [2026-10-29] v3.71 - unoUtil.vehicle.acc_brk 보정 데이터 파이프라인 일원화, 하드코딩 없는 적응형(Data-Driven) 과도 응답 알고리즘 및 3열 다중 진단 시각화·2×2 보정 진단 대시보드 고도화
* **보정 데이터 파이프라인 일원화 및 원본 보존 (`an_slip_pdf.py`, `vt_acc_brk_tire.py`, `func_acc_brk.py`)**:
  - CAN 통신 지연(약 20ms) 및 출발 직후 저속 휠속 센서 슬립(Wakeup) 보정이 완료된 정합 데이터를 응답성 분석(`AnResponse`) 및 커브피팅(`TireCurve`)에서도 그대로 사용하도록 파이프라인을 일원화.
  - 보정 전 원본 휠속(`WS*_Raw`) 및 원본 슬립률(`SR*_Raw`) 컬럼을 함께 보존하여 언제든 보정 전·후 차이를 대조할 수 있도록 데이터 구조 완결.
  - `calc_wheel_delay_compensation`: CAN 통신 지연 추정 시 제동 시 전륜 슬립(WS < Vel) 특성을 고려하여 완만한 양(+)의 가속 구간(0.02 ~ 0.18g) 최우선 활용 및 타력/초기 감속 구간(-0.08 ~ -0.015g) 폴백 추정 구축, 가속 발진 시 정차 출발점(i_rest)부터 첫 웨이크업 펄스(t_true)까지 C1 연속 램프로 저속 웨이크업 구간 복원.
* **하드코딩 없는 적응형(Data-Driven) 과도 응답 알고리즘 (`an_response.py`, `func_acc_brk.py`)**:
  - **제동/가속 전 노면(Dry/Wet/Snow/Ice) 대응**: 고정 임계값 없이 각 런의 피크 가속도 대비 적응형 타겟 대역(18% ~ 45%, 기저 노이즈 대비 최소 마진 보장)에서 휠 가속도와 차체 가속도의 정합 지연(`sys_response_time`, `sys_response_dist`)을 산출.
  - **실제 발현 기저점(`A_base`) 및 1차 과도 피크(`d²Vel = 0`) 검출**: 트리거 이전 2.0s까지 탐색 윈도우를 확보하고, 평형 기저점(`Median ± MAD`)부터 첫 번째 물리적 변곡 피크까지의 순수 진폭(`ΔA = A_peak - A_base`) 기준 10% ~ 90% 구간에서 라이징 타임과 기울기를 흔들림 없이 산출.
  - **제동 시 물리적 지연(`~220ms`) 규명 반영**: 20ms CAN 통신 지연 보정 후 남은 ~220ms는 센서/통신 딜레이가 아니라 타이어 슬립 형성 ➔ 노면 마찰력 발생 ➔ 서스펜션 피칭 압축을 거쳐 차체 전체가 감속하기까지의 실제 차량 동역학적 과도 응답 시간임을 정확히 계측.
  - 런별 정밀 진단 메타데이터(`Offset_Eff_Zero`, `Offset_Vel_Base`, `Offset_Ws_Base`, `Offset_Peak_L2`, `Base_Val`, `Base_Thresh`, `Peak_Val`, `Thresh_Start`, `Thresh_End`, `Rising_Min_Val`, `Rising_Max_Val`, `Run_Response_Time`, `Run_Rising_Time`, `Run_Rising_Slope`) 데이터프레임 내 보존.
* **상세 진단 시각화 완성 (`plotter_tire.py`)**:
  - **`PlotterTire.sys_response`**: 3열 다중 진단 뷰(1열: 속도 프로파일 & CAN 보정 전후 대조, 2열: 과도 가속도 & 적응형 지연 매칭, 3열: 기저점·피크·10~90% 라이징 회귀) 적용 및 **모든 Run 행의 열별 Y축 스케일 동적 100% 통일(하드코딩 Zero)** 완료.
  - **`PlotterTire.slip_check`**: 전체 세션 요약(상단 1·2패널)과 첫 유효 런 과도 구간 초정밀 확대(하단 3·4패널: `WS_Raw vs WS`, `SR_Raw vs SR`, 저속 웨이크업 복원 구간 하이라이트)를 결합한 **2×2 상세 보정 진단 대시보드** 완료.

### [2026-10-29] v3.70 - unoUtil.file_reader VBB 바이너리 타임스탬프 슬라이싱 결함 원천 해결, vt_acc_brk 메인 타이어 분석 완료 INFO 로그 복원 및 가속 모드 Mu-Drop 최적화
* **`datetime_helper.py` VBB 타임스탬프 파싱 결함 원천 해결**: VBO(텍스트, `HHMMSS.sss`) 전용 문자열 슬라이싱 판정 분기에서 바이너리(`.vbb`) 파일을 분리(`is_vbb_file`)하여, 초 단위 누적 시간(`sec_total = float(first_time_val)`) 및 타임존 오프셋(핀란드 UTC+2h 등) 계산 로직으로 정확히 진입하도록 정정 (`minute/second must be in 0..59` 에러 및 데이터 Skip 버그 원천 박멸).
* **`vt_acc_brk` 및 `VTAccBrkTire` 메인 분석(`analysis`) 완료 INFO 로그 복원**: 과거 DEBUG 레벨로 강등되어 서브 분석기 로그만 노출되던 결함을 해결하고, 타이어 단품 분석 완료 시 유효 런 회차(예: `유효 6/8회`) 및 대표 성능 지표(제동거리 평균 `brk_mean` 또는 가속시간 평균 `acc_time_mean`)를 포함한 표준 INFO 로그를 정식 복원.
* **가속(`acc`) 모드 시 Mu-Drop(마찰 저하) 분석 및 시각화 원천 제외**: 노면 마찰력 저하 및 제동거리 손실(Mu-Drop)은 급제동/ABS 전용 물리 거동이므로, `VTAccBrkTire.run()`에서 가속 모드일 때 불필요한 `AnMuDrop.analysis` 호출을 생략(`analyzer.mu_drop = None`)하고, `plotter_tire.py`의 렌더링 맵에서도 `is_acc` 시 `Mudrop_Distance` 차트 생성을 제외하여 무의미한 WARNING 경고 및 불필요 연산 부하를 100% 제거.
* **원천 계측 캐시 압축 저장 로그 명확화**: `vt_acc_brk.py`에서 원시 계측 데이터를 캐싱하는 `Raw Data 압축 저장` 로그를 `원천 계측 캐시 압축 저장`으로 명확히 정돈.

### [2026-10-29] v3.69 - unoUtil.vehicle.acc_brk 온디맨드 캐싱 아키텍처 표준화, 과도기 코드 전면 소멸, 선제적 빈 DF 초기화 도입 및 대시보드 타임테이블 마크다운 완전 복구
* **`an_slip_pdf.py` 과도기 코드 및 무한 재호출 루프 원천 제거**:
  - 과거 휠 지연 보정 개발 시 임시로 삽입되었던 `not cached_df.attrs.get("wheel_delay_compensated", False)` 조건문 및 미정의 변수(`cur_df`)를 전면 삭제하고, 프로퍼티 레벨의 임시 가드(`_is_ready_to_analyze()`)를 걷어내어 순수 $O(1)$ 온디맨드 자가 복원 규격(`if self._df is None: ...`)으로 복원.
* **`VTAccBrkTire.analysis()` 선제적 빈 DF 초기화(Pre-emptive Initialization) 도입**:
  - `analysis()` 진입 즉시(try 블록 최상단) 모든 결과 필드(`_result.df`, `summary`, `summary_all`, `detail`, `detail_all`)를 빈 데이터프레임으로 선제 채움으로써, 유효 런 미검출 조기 반환 시 외부나 시각화 모듈(`PlotterTire`, `PlotterProject`)에서 `.summary.empty` 조회 시 발생하던 `AttributeError: NoneType` 다운을 100% 원천 차단.
* **하위 분석기 3종(`skewness`, `response`, `mu_drop`) 단일 위임(Single Delegation) 헌장 확립**:
  - 상위 생성자(`AnSlipPdf`)가 휠속도 검증을 단독 전담하도록 하고, 하위 3개 모듈의 최상단 중복 가드를 제거하여 `if self.test.slip_pdf.df.empty: return self` 순수 단일 위임 코드로 롤백 (`func_acc_brk.py`의 `is_col_wheel_speed` 헬퍼 함수는 영구 보존).
* **시각화 모듈 연계 멱등성(Idempotency) 완비**:
  - 휠속도가 없는 시험 데이터에서 플로터의 다중 가드 조회 시 매번 `analysis()`가 강제 재기동되던 루프 폭포수를 완전 차단, 최초 1회만 경고 후 이후 조회는 0초 만에 빈 DF를 즉시 반환하여 평화롭게 플롯 스킵.
* **분석기 및 시각화 플로터 경고 메시지 단일 표준화**:
  - 분석 모듈 5종(`Slip_PDF`, `Mu_Drop`, `Slip_Mode_Skewness`, `Response`, `TireCurve`)은 `[{self.name}] [원인]이(가) 없어 분석을 생략합니다.` 규격으로, 시각화 모듈 2종(`PlotterProject`, `PlotterTire`)은 `[{name}] 분석 결과 데이터가 없어 그래프 생성을 생략합니다.` 단일 표준 문장으로 완전 통일하여 영문/한글 혼용 및 '선행 분석 필요' 등 오해 소지 문구를 100% 박멸.
* **도메인 지식 사전(`vt_acc_brk_사전.md`) 심층 지식화**:
  - 온디맨드 캐싱에서 `None`(캐시 부재/복원 트리거)과 `pd.DataFrame()`(연산 완료 센티널/재연산 방어막)의 정반대 라이프사이클 모델과 선제적 초기화 패턴을 3.3절 및 5.4절에 공식 집대성.
* **마스터 대시보드 타임테이블 마크다운 구문 파손 전면 복구**:
  - 옵시디언 Collapsible Callout 인용 부호(`> `) 누락 정합, `v3.65` 행의 문자열 제어문자(`\r`, `\t`, `\f`) 치환 및 실제 개행(LF) 분열 복구, LaTeX 물리 랜드마크 수식 및 파일명 백틱 인라인 정규화 완료.

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
    1. [[2026-10-21_v3.60_CurveFit_가속_WSS시간지연물리보정_발진궤적복원_종합보고서]] (WSS ZOH 스텝 홀드 $\Delta t_{\text{step}}/2$ 및 CAN 지연 결합 규명, 비구동 후륜 Bias $0.00\text{ km/h}$ 완전 소거 검증)
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
**Last Updated**: 2026-11-12  
**Standard**: unoUtil Clean Architecture v3.69 & Single Baseline Law & Single Master MOC Law