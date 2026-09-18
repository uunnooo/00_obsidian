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
aliases:
  - unoUtil_모듈개발_대시보드
  - unoUtil개발허브
---

# 💼 unoUtil 사내 파이썬 통합 프레임워크 개발 프로젝트

> [!SUCCESS] 🎉 unoUtil v2.0 전면 리팩토링 및 10대 도메인 아키텍처 개편 완료 (2026-09-18)
> - **상세 결과 보고서**: [[UNOUTIL_V2_REFACTORING_REPORT]] (10대 계획 100% 집행 & 전수 검증 통과)
> - **패키지 다이어트**: 패키지 내 분산된 1GB+ 거대 데이터 제거 $\rightarrow$ 15.62MB 순수 파이썬 초경량화 (98.5% 절감)
> - **100% 무중단 하위 호환**: 기존 사내 스크립트 수정 없는 `sys.modules` 및 위임 래퍼 지원

> [!ABSTRACT] 🛠️ 프레임워크 개요
> **unoUtil**은 사내 실차 시험 계측 데이터 수집, 신호 전처리, 동역학 물리 분석, 시험 환경 보정, 그리고 시각화 리포팅을 표준화하기 위한 사내 통합 파이썬 라이브러리 개발 프로젝트입니다.

---

## 📦 패키지 서브모듈 구조 및 현황 (v2.0 Clean Architecture)

```text
📂 unoUtil/
├── 🏎️ vehicle_test/            # 실차 시험 종합 분석 패키지 (Active, 구 vehicleTest)
│   └── 🏁 ACCBRK/             # 실차 가감속 / 제동 성능 정밀 분석 엔진
│       ├── base_memory.py     # BaseMemory (구 _AN_MEMORY_)
│       └── 📂 analyzers/      # 6대 전문 물리 분석 엔진
├── 🛰️ gps/                     # GNSS / VBOX 공간 데이터 및 WGS84 좌표 투영 엔진 (Active, 구 gpsProcessing)
│   └── gps_to_xy.py          # WGS84 타원체 벡터화 투영 엔진 (GPStoXYCord)
├── 🚀 file_reader/             # 차세대 객체지향 이종 계측 데이터 통합 리더 (Active, 구 fileDataReader)
│   ├── FileDataReader.py      # 플루언트 파이프라인
│   └── 📂 parsers/            # base, vbo, vbb, dwd, text 분리 파서
├── 📶 signal_process/          # 신호처리 종합 패키지 (Active)
│   ├── 📂 post_process/       # filters, resample, scaler, outliers (구 _UnoPP_)
│   ├── 📂 curve_fit/          # 다항식/지수 피팅
│   └── 📂 fft/                # 주파수 스펙트럼 분석
├── 🎨 graphics/                # 실차 시각화 및 상호작용 패키지 (Active, 구 graphicTools)
│   ├── 📂 plotters/           # Plotter, text_offset, surface_3d
│   ├── 📂 controls/           # cursor_mode, range_selector
│   └── 📂 web/                # plotly_tools
├── 📊 statistics/              # 통계 분석 및 측정불확도 패키지 (Active)
│   ├── summary.py             # 10대 요약 기술통계 (get_statistics_df)
│   └── 📂 uncertainty/        # GUM / ISO 98-3 정밀 측정불확도
├── 🛠️ utils/                   # 사내 통합 공통 유틸리티 (Active, 구 convenienceFunction)
│   ├── files.py / excel.py / dataframe_utils.py / console_style.py / weather.py
├── 📝 logger/                  # GUI 창/콘솔 일체형 고성능 로깅 시스템
├── 🤖 ai/                      # 머신러닝/딥러닝 동역학 모델링 (구 unoAI)
├── 🗄️ db/                      # 시험 데이터베이스 연동 (구 unoDB)
└── 💾 readDataFile/            # (⚠️ 폐기 예정 / Deprecated - FileDataReader로 대체)
```

---

## 🚀 1. 핵심 활성 모듈: VT_ACCBRK, gpsProcessing, fileDataReader & readDataFile

### 🏎️ 1.1 VT_ACCBRK (실차 가감속 / 제동 분석 엔진)
* 🏎️ **[[00_VT_ACCBRK_대시보드|VT_ACCBRK 통합 실차 성능 분석 시스템 대시보드]]**
  * **전체 파이프라인**: [[10_VT_ACCBRK]]
  * **개별 물리 분석**: [[11_VT_ACCBRK_TIRE]]
  * **프로젝트 취합 및 선형 보간**: [[12_VT_ACCBRK_PROJECT]]
  * **서브 분석 모듈**: [[20_VT_ACCBRK_SUB_ANALYZERS]]
  * **시각화 플로터**: [[31_PLOTTER_PROJECT]], [[30_PLOTTER_TIRE]]
  * **보정 알고리즘**: [[21_CORRECT]]
* 📜 **품질 혁신 및 체인지로그**: [[00_VT_ACCBRK_대시보드#5-버전-이력-및-주요-품질-혁신-내역-changelog--quality-audit|VT_ACCBRK v2.0 대규모 리팩토링 및 품질 혁신 내역]]

### 🛰️ 1.2 gpsProcessing (공간 데이터 처리 및 좌표 변환 엔진)
* 🛰️ **[[00_gpsProcessing_대시보드|gpsProcessing 공간 데이터 처리 및 평면 좌표계 투영 엔진 대시보드]]**
  * **핵심 투영 엔진**: [[10_GPStoXYCord]] (WGS84 타원체 정밀 벡터화, 기존 대비 5.9배 고속화, 0.06mm 정밀도)
  * **데이터 방어 필터**: VBOX 종료 시점 0.0 노이즈 격리 및 DataFrame 인덱스 100% 보존
  * **트랙 좌표계 정렬**: 테크노링 직선 제동로 기준점 및 회전각($\theta = -0.4^\circ$) 표준화

### 🚀 1.3 fileDataReader (차세대 이종 계측 데이터 객체지향 리더 프레임워크) ⭐
* 🚀 **[[FileDataReader|FileDataReader (이종 계측 데이터 통합 객체지향 로더)]]**
  * **전략 패턴 파서 라우팅**: VBO, VBB, Dewesoft(D7D), TXT/CSV 자동 식별 및 고속 파싱
  * **하위 패키지 완전 내재화 (Zero-Dependency)**: [[VBBReader]] 바이너리 파서 및 [[dwdReader]] C-DLL 디코더를 완전히 내장하여 `readDataFile` 의존도 0% 달성
  * **GPS 스마트 타임존**: 글로벌 주요 시험장(태안, 이발로, IDIADA, ATP) 바운딩 박스 기반 동적 서머타임(DST) 자동 보정
  * **Dewesoft 비동기 채널 정합**: `pd.merge_asof` 기반 고속 타임라인 보간 (15만 행 2.05초)
  * **플루언트 API & 일괄 스캔**: 메서드 체이닝 및 `scan_dir` 멀티파일 예외 격리 배치 로딩
  * **대규모 마이그레이션**: 사내 24개 모듈(`VT_ACCBRK`, `2025_Autobuild`, `Snow`, `MakeBRKResult`) 무중단 전면 전환 완료
  * **하위 디코더 엔진**:
    * 📂 **[[VBBReader]]**: VBOX 바이너리(.vbb) 고속 파서 및 전원 급차단 3중 방어 복구 엔진
    * 📂 **[[dwdReader]]**: Dewesoft D7D C-DLL 연동 및 비동기 CAN/GPS 채널 고속 정합 엔진
  * **영구 도메인 지식 연계**: [[23_이종_계측_데이터_통합_파이프라인_및_대규모_마이그레이션_엔지니어링]], [[22_GPS_좌표_기반_타임존_자동_판별_및_시계열_합성_이론]], [[20_VBOX_계측_데이터_규격_및_GPS좌표계]], [[21_바이너리_파일_IO_및_VBB_데이터_포맷_구조]]

### 💾 1.4 readDataFile (레거시 데이터 로더 보존 및 향후 폐기 예정 영역)
* 💾 **[[ReadDataFile|ReadDataFile (모놀리식 레거시 데이터 로더)]]**
  * **상태**: ⚠️ 레거시 유지 관리 및 향후 완전 삭제 예정 (Deprecated)
  * 모든 신규 분석 및 배치 파이프라인은 [[FileDataReader]]로 완전 대체 완료

### 📶 1.5 signal_process (신호 후처리, 커브피팅 및 주파수 분석)
* 📶 **[[00_post_process_대시보드|post_process (신호 후처리 패키지 대시보드)]]**
  * **[[filters|filters (Zero-Phase 이동평균 필터)]]**: 위상 지연 없는 양방향 필터(`filtfilt`) 및 SOS 고속 필터
  * **[[resample|resample (비수치 보존 리샘플링)]]**: 이종 센서 비동기 정합 및 메타데이터 무손실 보존
  * **[[outliers|outliers (다변량 이상치 정제)]]**: Percentile, Z-score, iForest, Extended IF 및 유효 제동 구간 색출
  * **[[scaler|scaler (데이터 정규화)]]**: MinMax, Standard, Robust 스케일링
  * **영구 도메인 지식 연계**: [[25_실차_신호처리_및_시계열_데이터_정제_공학]]

### 🎨 1.6 graphics (실차 시각화 및 상호작용 인터랙션)
* 🎨 **[[00_graphics_대시보드|graphics (시각화 패키지 대시보드)]]**
  * **[[plotters/plotter|plotters (렌더링 플로터)]]**: Non-blocking 시각화 엔진, 텍스트 오프셋, 3D 서피스
  * **[[controls/cursor_mode|controls (상호작용 제어기)]]**: 십자선 커서 모드, 마우스 드래그 관심구간(ROI) 추출
  * **web**: 브라우저 기반 대화형 Plotly 차트
  * **영구 도메인 지식 연계**: [[26_대규모_파이썬_패키지_모듈화_및_무중단_하위호환_아키텍처#4-시각화-무중단non-blocking-엔지니어링-표준]]

### 📊 1.7 statistics (통계 분석 및 측정불확도)
* 📊 **[[summary|summary (10대 요약 기술통계량)]]**: `get_statistics_df` (`get_statics_df`)
* 🎯 **uncertainty**: GUM / ISO 98-3 가이드라인 기반 합성표준불확도 및 확장불확도 평가

### 🛠️ 1.8 utils (사내 통합 공통 유틸리티)
* 🛠️ **[[00_utils_대시보드|utils (유틸리티 패키지 대시보드)]]**
  * **[[files|files (경로 점검 및 파일 탐색)]]**, **[[dataframe_utils|dataframe_utils (DF 헬퍼 & 비율 연산)]]**, **excel**, **weather**

---

## 📐 2. 개발 및 엔지니어링 표준

* 📘 **[[Gemini_Python_코드_생성_규칙|Python 코드 품질 및 작성 가이드라인]]**
* 🏗️ **[[26_대규모_파이썬_패키지_모듈화_및_무중단_하위호환_아키텍처|대규모 파이썬 패키지 모듈화 및 무중단 하위호환 아키텍처]]**
  * Type Hinting 전수 적용 및 8대 동사 접두사 / 4대 불변 키워드 인자 표준화
  * Google Style Docstring 표준 및 Non-blocking 시각화 (`plt.close(fig)`) 필수
  * `# region Test` 기반 단위 검증 코드 필수 탑재
  * 옵시디언 기술 문서 실시간 이중 동기화 프로토콜 준수
