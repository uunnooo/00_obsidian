---
id: "00_snow_condition_대시보드"
title: "❄️ unoUtil.snow_condition 도메인 대시보드"
type: domain_dashboard
category_main: 20_unoUtil_모듈개발
domain: snow_condition
date: 2026-10-01
status: 활성
tags:
  - unoUtil
  - snow_condition
  - 대시보드
  - MOC
  - 디지털트윈
  - 노면보정
---

# ❄️ `unoUtil.snow_condition` 도메인 대시보드 (MOC)

> **패키지 위치:** `unoUtil.snow_condition`  
> **책임 영역:** 스노우 노면 3D/4D 시공간 디지털 트윈 복원, Sonntag 수증기압/과포화도/접지압 물리 역학 연산, 47대 SSOT 데이터 조화(Harmonization), 6대 머신러닝 차분 노면 환경 보정 및 1st vs 2nd 대조 검증

---

## 🗺️ 1. 모듈 아키텍처 및 세부 문서 링크

| 파일명 | 역할 및 핵심 기능 | 상세 문서 링크 |
| :--- | :--- | :--- |
| `schema.py` | 47대 SSOT 표준 컬럼 명세, 중복 컬럼 충돌 방어, `harmonize_snow_dataframe` 단일 관문 | [[schema\|schema 매뉴얼]] |
| `preprocessor.py` | 기온 정상/이상 구간, 강설 여부, 타이어 카테고리별 사전 독립 선처리 필터 (`filter_snow_conditions`) | [[preprocessor\|preprocessor 매뉴얼]] |
| `physics.py` | Sonntag 빙점하 포화수증기압, 절대습도(AH), 과포화도(AHE), 정적/동적 접지압, 밀도 추정 | [[physics\|physics 매뉴얼]] |
| `surface_interpolator.py` | 6채널 센서 오프셋 정합, 3D 격자 보간 복원, 시험 묶음 시작 시각 기반 단일 세션 결합 (`SnowSurfaceInterpolator`) | [[surface_interpolator\|surface_interpolator 매뉴얼]] |
| `surface_animator.py`| Plotly 기반 4D 시공간 슬라이더 애니메이션 대시보드 및 HTML 인터랙티브 뷰어 | [[surface_animator\|surface_animator 매뉴얼]] |
| `correction_model.py`| [방법 1] 6대 ML 회귀 모델(RF, SVR, Ridge, Lasso, ElasticNet, KNN) 차분 학습 및 예측 코어 엔진 | [[correction_model\|correction_model 매뉴얼]] |
| `slope_model.py` | [방법 2] 동일 스펙(`SPEC_NO`) 중심화 1변수 독립 물리 기울기($k_{\text{air}}, k_{\text{ah}}$) 및 기준 환경 정규화 엔진 (`SnowSlopeModel`, `SnowSlopePlotter`) | [[slope_model\|slope_model 매뉴얼]] |
| `correction_validator.py`| 1st vs 2nd 세트 매칭 대조표(Excel) 산출, MAE/표준편차 개선율 검증 | [[correction_validator\|correction_validator 매뉴얼]] |
| `correction_plotter.py` | No Redundant Prefix Law 준수 Figure 1~3 (차분산점도, 1st vs 2nd 복원 오버플롯, 2D 등고선 맵) 렌더링 (`SnowCorrectionPlotter`) | [[correction_plotter\|correction_plotter 매뉴얼]] |

---

## 📜 2. 버전 이력 및 주요 개발 현황 (Changelog)

### [2026-10-02] v1.6.0 - 방법 2 동일스펙 2D-KNN 러프 평활화 모델 확정, 10~35m 이상치 필터링 복원, 복원 전·후 R² 및 산포개선율 단일 마스터 통합보고서 완성
- **방법 2 동일스펙 2D-KNN 러프 평활화 모델 최종 확정**:
  - 사용자 요구에 따라 별도 래퍼 클래스 증설 없이 사내 공식 표준 `SnowCorrectionModel(target_model='KNN Regressor')` 단일 엔진으로 방법 2 모델링 일원화.
  - 국소적 소용돌이(아일랜드) 현상을 방지하기 위해 이웃수를 대폭 상향($k=40\sim 150$, 유효 데이터의 20%)하고 `weights='uniform'`을 적용하여 완만하고 물리적으로 신뢰할 수 있는 2차원 공간 반응면 도출.
  - 사내 공통 기준 환경($-8.0^\circ\text{C}, 1.5\text{ g/m}^3$) 대비 절대 오프셋 보정 수식 정립 (`BRK_DIST_METHOD2_CORR_REF`).
- **제동거리 10m~35m 정상 평가 구간 필터링 복원**:
  - 50m 수준의 비정상 제동거리 이상치를 사전 차단하여 머신러닝 회귀면 및 표준편차 산포 지표 왜곡 원천 제거.
- **보고서 및 시각화 전수 단일화 (개별 파편 파일 100% 정화)**:
  - 분산된 개별 보고서 3종을 영구 폐기하고, 모든 데이터 인벤토리, 방법 1 복원 전·후 $R^2$($0.70\sim 0.91$) 및 $r$($0.86\sim 0.96$) 표, 방법 2 스펙별 표준편차($\sigma$) 산포개선율 표를 `00_과거_스노우_제동_환경보정_종합_통합보고서.md` 단일 마스터로 통합.
  - **심층 공학 분석 섹션 신설 (Section 2.2)**: 방법 1(RF)을 절대 보정(-8℃ 기준)으로 적용 시 발생하는 비선형 가산성 결핍 및 양측 오차 누적(MAE 0.608m vs 1.110m, 오차 +29.2% 폭증) 실증 규명 및 역할 분담의 수학적 필연성 기술 완비.
  - 51종 시각화 그래프 전수 재동기화 및 16개 시트 다중 엑셀/피클 배포 완료.

### [2026-10-02] v1.5.0 - 선처리 모듈(preprocessor) 분리, 방법 2 동일스펙 독립기울기 엔진(slope_model) 정식 편입, No Redundant Prefix Law 표준화
- **선처리 전담 모듈 (`preprocessor.py`) 신규 분리 및 설계**:
  - `filter_snow_conditions()` 함수 구현: 모델 내부의 하드코딩 필터링을 완전히 제거하고, 단일 책임 원칙(SRP)에 따라 데이터 선처리를 분리하여 모델 범용성 확보.
  - 기온 구간(`temp_mode='in_range'` vs `'out_of_range'`), 강설 여부(`snowfall_mode='exclude_snow'` vs `'snow_only'`), 타이어 카테고리 선처리 완비.
- **방법 2 전용 엔진 (`slope_model.py`) 신규 구현 및 정식 편입**:
  - `SnowSlopeModel`: 동일 스펙(`SPEC_NO`) 중심화 기반 1변수 독립 OLS 기울기($k_{\text{air}}, k_{\text{ah}}$) 및 $p$-value 산출, 기준 환경($-8^\circ\text{C}, 1.5\text{ g/m}^3$) 일괄 보정 (`correct_dataframe`).
  - `SnowSlopePlotter`: 동일 스펙 물리 기울기 산점도(`slope_scatter`), 기준 환경 대비 2D 등고선 맵(`correction_map`), 동일 스펙 분산 감소율 박스플롯(`variance_reduction`) 지원.
- **클래스 역할 내포 시 메서드 접두사 중복 방지 원칙 (No Redundant Prefix Law) 전면 적용**:
  - `SnowCorrectionPlotter` 및 `SnowSlopePlotter` 내의 모든 메서드에서 `plot_` 접두사를 영구 삭제 (`delta_prediction_scatter`, `scatter_restoration`, `scatter_overplot`, `correction_map`, `slope_scatter`, `variance_reduction`).
  - 과도기적 레거시 alias 완전 폐기 및 직교적 v2 단일 규격(SSOT) 확립.
- **과거 7개년 스노우 제동 데이터 전면 재구축 및 8대 데이터셋/시각화 완료**:
  - `run_full_snow_correction_matrix.py` 파이프라인 전면 리팩토링 및 정상 가동 (Exit Code 0).
  - 방법 1 vs 방법 2 4대 시나리오별 비교 매트릭스 완성 및 8대 데이터셋(pkl/xlsx), 90여 종의 시각화 차트 옵시디언 볼트 실시간 배포 완료.

### [2026-10-01] v1.4.0 - 센서 연산 완전 분리, char_* 단일 표준화 및 3중 결측/이상치(np.clip) 방어 가드
- **센서 하드웨어 연산 완전 제거 및 관심사 분리(SoC)**:
  - `SnowSurfaceInterpolator` 내부에서 센서 하드웨어에 종속되던 계산 로직(`Height1~6` 차이 수식, `Temp1~2` 뺄셈, `h_left`, `h_right`, `h_out`, `h_tire` 등)을 100% 완전 삭제.
  - 센서 가공은 데이터 생성 전처리 단계(`a_make_SnowSurfaceCharacteristic_DF.py`)로 명확히 격리하고, 보간기는 순수 3D 공간 보간 모델에만 전념하도록 정립.
- **`char_*` 단일 명명 체계 (SSOT) 전면 일원화**:
  - `calc_h_diff`, `calc_t_diff`, `HeightDiffAver`, `TempDiffAver` 등 파편화된 과도기적 별칭을 영구 폐기.
  - `fit()`의 기본 인자를 `height_col='char_height'`, `temp_col='char_temp'`, `cond_id_col='Cond_ID'`로 표준화하여 사전 전처리 결과와 1:1 완벽 직결.
  - 내부 격자 모델 학습 및 제동 데이터 결합 시에도 일관되게 `char_height`, `char_temp` 단일 컬럼명 유지.
- **3중 결측치 및 범위 밖 이상 데이터 안전 정제 파이프라인 (`_sanitize_feature`, `np.clip`) 탑재**:
  - 1단계: 비수치/무한대(inf) $\to$ NaN 변환 (`pd.to_numeric`).
  - 2단계: 센서 결측치(NaN) $\to$ 세션 중앙값(median) 자동 대치 (`fillna`).
  - 3단계: 물리적 유효 허용 범위 밖의 극단적 이상치 $\to$ `np.clip` 상/하한 안전 제한.
- **실데이터 엔드투엔드 파이프라인 전수 검증 통과 (Exit Code 0)**:
  - `b_combine_surface_performance_spec.py`: 노면 스냅샷 53개(22개 세션) 학습 및 1,964건 제동 데이터 전수 매칭 완결.
  - `c_run_snow_correction_pipeline.py`: 6대 머신러닝 모델 학습, 95개 세트 대조표 및 4종 시각화 리포트 정상 출력.

### [2026-10-01] v1.3.0 - 동적 특성 인자 리스트(x_cols, y_col) 지원, 결측치(NaN) 방어 가드 및 시각화 동적화
- **동적 특성 인자 리스트 인터페이스 (`x_cols: List[str]`, `y_col: str`) 혁신**:
  - 기존의 고정 키워드(`x_1`, `x_2`) 대신 파이썬 리스트 형태의 `x_cols: Optional[List[str]]` 및 `y_col: str` 표준 인터페이스 도입.
  - 침하 깊이, 노면 온도, 기온, 절대습도 등 임의의 실험 인자 조합은 물론 3개 이상의 다변량 피처 확장까지 완전 지원.
- **결측치(NaN) 자동 정제 및 무결성 예외 가드 (`missing_strategy='drop'`)**:
  - 계측 센서 누락 또는 비정상 입력값(NaN)을 사전에 자동 필터링하여 경고 로그와 함께 유효 데이터만 학습에 반영.
  - 전체가 결측치(All NaN)이거나 유효 데이터가 부족한 경우 명시적인 `ValueError`를 발생시켜 모델 오류 사전 방어.
- **다형성 예측 인터페이스 (`predict_delta`) 구축**:
  - 스칼라 가변인자(`*args`), 딕셔너리(`dict`), 1D/2D NumPy 배열, Pandas DataFrame 입력을 모두 단일 함수에서 자동 판별하여 처리.
- **시각화 플로터 및 검증기 100% 동적 라벨링 연동**:
  - `SnowCorrectionPlotter`: Figure 1(산점도), Figure 3(등고선 맵), 오버플랏 플롯의 축 라벨 및 타이틀이 모델의 `x_cols`, `y_col` 명칭으로 자동 치환.
  - `SnowCorrectionValidator`: `col_dist`, `col_corr` 매개변수 지원으로 제동거리 외 임의의 성능 지표 대조표 산출 가능.
- **전체 무결성 검증 통과 (Exit Code 0)**:
  - `correction_model.py`, `correction_plotter.py`, `correction_validator.py` 자가 구동 테스트 전수 통과.
  - 다변량/NaN 주입 종합 단위 테스트 및 실데이터(1,964건) 통합 파이프라인 완벽 완주.

### [2026-10-01] v1.2.0 - SnowSurfaceInterpolator 직관적 단일 표준 확립 및 12:30 세션 쪼개짐 원천 해결
- **추상적 Twin 명칭 폐기 및 `SnowSurfaceInterpolator` 단일 표준 확립**:
  - 기존의 추상적인 `SurfaceConditionTwin` 및 `surface_twin.py`를 과도기적 잔재 없이 완전 폐기하고, 사이킷런 표준 인터페이스 기반의 직관적인 **`SnowSurfaceInterpolator`** (`surface_interpolator.py`)로 전면 개편.
  - `fit(df_surface)` $\to$ `transform(df_brk)` 구조로 표준화하여 `b_combine_surface_performance_spec.py`의 수동 for 루프를 단 2줄로 경량화.
- **시험 묶음 최초 시작 시각(`min(Datetime)`) 기반 단일 세션 결합 (`transform`)**:
  - `Date + ReqNo + TestOrder` 그룹별로 평가 시작 시각을 감지하여 세션(`test_cond_id`)을 판별.
  - 12:30 전후로 걸쳐 진행된 제동 시험 세트(예: 2026-01-13 10:07~12:34)가 런별 단순 시각 비교로 인해 am/pm으로 분열되던 중대 결함을 100% 원천 해결.
- **파이프라인 무결성 검증 완결**:
  - `surface_interpolator.py`, `surface_animator.py` 자가 구동 테스트 전수 통과 (Exit Code 0).
  - 실차 제동 1,964건 전수 보간 매칭 완결 및 2026-01-13 단일 세션 유지 완벽 검증.

### [2026-10-01] v1.1.0 - a_/b_ 전처리 파이프라인 직렬 연계 및 중복 컬럼 완전 정화
- **a_/b_ 전처리 직렬 연계 완결**:
  - 스노우 프로젝트 내 `a_make_SnowAccBrkTest_DF.py`, `a_make_SnowSurfaceCharacteristic_DF.py`, `a_make_SRTT_DF.py`의 최종 저장 관문에 `harmonize_snow_dataframe` 연계.
  - `b_combine_surface_performance_spec.py`에서 과거 레거시 파사드를 완전 걷어내고 `SurfaceConditionTwin` 직렬 구축 $\to$ 1:1 시공간 보간 $\to$ `1. df_combine_test_surface_spec.pkl` 완벽 생성 (Exit Code 0).
- **중복 컬럼(`duplicated`) 충돌 방어**:
  - 레거시 컬럼 매핑 시 다대일 매핑(`TestTireSet`, `TestSet` $\to$ `infor_TIRE_SET`)으로 발생하던 컬럼 중복 버그 원천 해결.
  - `COL_47_ORDER` 표준 컬럼 정렬 상수를 `schema.py` 및 최상위 `__init__.py`에 공식 탑재.
- **통합 파이프라인 무결성 검증**:
  - `c_run_snow_correction_pipeline.py` 가동 $\to$ Exit Code 0 (소요시간 3초, 1,964건 전수 통과).

### [2026-10-01] v1.0.0 - 사내 표준 제12대 공식 도메인 승격 및 통합 이관
- 스노우 프로젝트의 노면 디지털 트윈, 물리 연산, ML 차분 보정 코드를 `unoUtil.snow_condition`으로 100% 완전 이관.
- 컴포지션(Composition) 아키텍처로 `SnowCorrectionEngine` 완성.
