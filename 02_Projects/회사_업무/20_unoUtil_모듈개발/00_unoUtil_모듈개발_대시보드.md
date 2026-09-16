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

> [!ABSTRACT] 🛠️ 프레임워크 개요
> **unoUtil**은 사내 실차 시험 계측 데이터 수집, 신호 전처리, 동역학 물리 분석, 시험 환경 보정, 그리고 시각화 리포팅을 표준화하기 위한 사내 통합 파이썬 라이브러리 개발 프로젝트입니다.

---

## 📦 패키지 서브모듈 구조 및 현황

```text
📂 unoUtil/
├── 🏎️ vehicleTest/             # 실차 시험 종합 분석 패키지 (Active)
│   └── 🏁 ACCBRK/             # 실차 가감속 / 제동 성능 정밀 분석 엔진
│       ├── 00_VT_ACCBRK_대시보드.md
│       ├── 10_VT_ACCBRK.md (통합 파이프라인)
│       ├── 11_VT_ACCBRK_TIRE.md (단일 타이어 분석)
│       ├── 12_VT_ACCBRK_PROJECT.md (취합 및 보정)
│       ├── 20_VT_ACCBRK_SUB_ANALYZERS.md (7대 전문 서브 분석기)
│       ├── 21_CORRECT.md (환경 및 콘트롤 성능 보정)
│       ├── 22_Func_ACCBRK.md (공통 연산 유틸리티)
│       ├── 30_PLOTTER_TIRE.md / 31_PLOTTER_PROJECT.md (시각화 플로터)
│       └── 90_ACCBRK_사용자매뉴얼.md (실무 사용자 매뉴얼)
├── 🛰️ gpsProcessing/          # GNSS / VBOX 공간 데이터 및 WGS84 좌표 투영 엔진 (Active)
│   ├── 00_gpsProcessing_대시보드.md (통합 허브 & MOC)
│   └── 10_GPStoXYCord.md (WGS84 타원체 벡터화 투영 엔진)
├── 🚀 fileDataReader/          # 차세대 객체지향 이종 계측 데이터 통합 리더 (Active ⭐ 완전 독립)
│   ├── FileDataReader.md (VBO, VBB, D7D, TXT/CSV 통합 파서 & 플루언트 파이프라인)
│   ├── 📂 vbbTopython/        # VBB 바이너리 초고속 파서 & 전원차단 복구 엔진 내재화
│   │   └── VBBReader.md
│   └── 📂 DWDataReader_v5_0_8/ # Dewesoft D7D C-DLL 디코더 & 비동기 정합 엔진 내재화
│       └── dwdReader.md
├── 💾 readDataFile/            # 계측기 원본 데이터 로더 (⚠️ 폐기 예정 / Deprecated)
│   ├── ReadDataFile.md (모놀리식 ReadDataFile 레거시 레퍼런스)
│   └── 📂 vbbTopython/
│       └── VBBReader.md (레거시 보존)
└── 🔧 (확장 예정 모듈)         # convenienceFunction, unoAI, Lateral 등
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
  * **안전망 조치**: `unoUtil/__init__.py`에서 `try...except ImportError`로 분리되어 향후 폴더가 삭제되어도 전체 패키지 무중단 구동 보장
  * 모든 신규 분석 및 배치 파이프라인은 [[FileDataReader]]로 완전 대체 완료


---

## 📐 2. 개발 및 엔지니어링 표준

* 📘 **[[Gemini_Python_코드_생성_규칙|Python 코드 품질 및 작성 가이드라인]]**
  * Type Hinting 전수 적용
  * Google Style Docstring 표준
  * `# region Test` 기반 단위 검증 코드 필수 탑재
  * 옵시디언 기술 문서 실시간 이중 동기화 프로토콜 준수
