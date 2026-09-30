---
id: "unoutil_snow_condition_moc"
title: "unoUtil snow_condition 도메인 대시보드 (MOC)"
type: moc
category_main: 회사_업무
category_sub: unoUtil
date: 2026-09-30
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - snow_condition
  - 노면컨디션
  - 대시보드
  - MOC
  - 머신러닝보정
aliases:
  - 00_snow_condition_대시보드
  - snow_condition_대시보드
  - snow_condition_MOC
---

# ❄️ unoUtil.snow_condition 노면 환경 & 머신러닝 보정 도메인 (MOC)

> 사내 노면 환경 계측(침하 깊이, 표면 온도, 대기 절대습도), 물리 역학 계산(Sonntag 증기압, 과포화도, 접지압), 시공간 3D 디지털 트윈, 4D 시각화 대시보드, 그리고 **컴포지션 패턴(Composition Pattern) 기반 스노우 제동거리 환경 차분 머신러닝 보정 엔진**을 전담하는 공식 도메인입니다.

---

## 🏛️ 1. 도메인 아키텍처 구성

```
unoUtil.snow_condition/
├── schema.py & .md              # SSOT 47대 표준 컬럼 및 harmonize_snow_dataframe 단일 관문
├── physics.py & .md             # Sonntag 증기압, 과포화도, 접지압 물리 역학 수식
├── surface_twin.py & .md        # 센서 좌표계 복원, 3D 시공간 디지털 트윈
├── dashboard.py & .md           # Plotly 기반 4D 시공간 노면 환경 애니메이션
├── correction_model.py & .md    # 머신러닝 회귀 보정 코어 엔진 (RF, KNN, SVR, Ridge 등)
│   ├── self.validator           ──► SnowCorrectionValidator (정량 검증, 1st vs 2nd 대조표)
│   └── self.plot                ──► SnowCorrectionPlotter (Figure 1~4 시각화 플로터)
├── correction_validator.py & .md# 정밀 대조표 산출, 엑셀/CSV 내보내기, 오차 감소율 요약
├── correction_plotter.py & .md  # 다형성 비교 플롯, 오버플랏 산점도, 2D 등고선 보정 맵
└── __init__.py                  # 8대 핵심 클래스/함수 패키지 최상위 바인딩
```

---

## 📚 2. 핵심 모듈별 기술 매뉴얼

| 모듈명 | 핵심 클래스 / 함수 | 주요 역할 | 매뉴얼 링크 |
| :--- | :--- | :--- | :--- |
| **`schema`** | `harmonize_snow_dataframe`<br/>`COL_*` 상수 47종 | 컬럼 표준 정규화 및 결측 보정 SSOT 단일 관문 | [[schema\|schema.md]] |
| **`physics`** | `calc_saturation_vapor_pressure_ice`<br/>`calc_actual_vapor_pressure`<br/>`calc_supersaturation`<br/>`calc_ground_contact_pressure` | Sonntag 수증기압, 과포화도, 타이어 접지압 물리 계산 | [[physics\|physics.md]] |
| **`surface_twin`** | `SnowSurfaceTwin` | 센서 오프셋 보정, 3D 시공간 디지털 트윈 복원 | [[surface_twin\|surface_twin.md]] |
| **`dashboard`** | `SnowSurfaceDashboard` | 4D 시공간 인터랙티브 Plotly 대시보드 생성 | [[dashboard\|dashboard.md]] |
| **`correction_model`** | `SnowCorrectionModel` | 6대 ML 회귀 훈련, 보정 적용, 컴포지션 허브 | [[correction_model\|correction_model.md]] |
| **`correction_validator`** | `SnowCorrectionValidator` | 1st vs 2nd 대조표 산출, 엑셀 저장, 오차 감소율 | [[correction_validator\|correction_validator.md]] |
| **`correction_plotter`** | `SnowCorrectionPlotter` | Fig 1(차분 산점도), Fig 2(오버플랏 복원), Fig 3(등고선 맵), Fig 4(의뢰/세트별 추세선) | [[correction_plotter\|correction_plotter.md]] |

---

## 📜 3. 버전 이력 및 주요 개발 현황 (Changelog)

> [!NOTE]- 📜 [2026-09-30] v1.0: `unoUtil.snow_condition` 패키지 신설 및 컴포지션 패턴 구축 [클릭하여 펼치기]
> * ❄️ **패키지 정식 편입**: `2026_Snow_RoadSurface_characteristics`에서 노면 환경 및 보정 모듈을 `unoUtil`로 전면 승격 이관.
> * 🧩 **`acc_brk` 스타일 컴포지션 패턴(Composition Pattern) 완결**:
>   - 코어 모델(`SnowCorrectionModel`), 검증기(`SnowCorrectionValidator`), 플로터(`SnowCorrectionPlotter`) 3대 클래스로 역할 분리.
>   - `model.validator.calc_corrected_comparison_table()` 및 `model.plot.plot_scatter_restoration()` 직관적 위임 바인딩.
> * 📊 **의뢰번호 및 타이어 세트별 비교 플롯 다형성 신설**:
>   - `plot_tire_subsets_comparison(req_no, tire_set, style='trend'|'bar')` 구현.
>   - 의뢰번호만 지정 시 전체 세트 서브플롯, 특정 세트 지정 시 단일 상세 플롯 렌더링.
>   - 1st Ref 기준 수평선 + 2nd Raw 점선 + 2nd Corr 실선 복원 궤적 + 개별 Run 산점도 + 오차개선율(%) 일체형 표기.
> * 🧪 **무결성 검증 통과 (Exit Code 0)**: 실데이터 1,964건 통합 파이프라인 전수 완주 및 1:1 매뉴얼 7종 완비.
