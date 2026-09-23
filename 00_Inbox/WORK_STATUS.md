# 📝 [WORK STATUS] 2026-09-23 (수) 스노우 노면 특성 디지털트윈 전처리 초고속화 및 시각화 아키텍처 정립

## 📅 1. 작업 개요
* **일자:** 2026년 9월 23일 (수)
* **작업자:** uno & Gemini CLI
* **과제명:** 2026 Snow Surface Characteristics (스노우 노면 특성 디지털트윈 및 제동 성능 환경 보정)
* **목표:** 
  1. `unoUtil.resample_data` 1ms 고속화 리팩터링 및 PyDev 디버거 3초 타임아웃 해소
  2. `VT_ACCBRK` 대용량 캐시 온디맨드 복원 버그(`KeyError: 'Datetime'`) 근본 원인 분석 및 완치
  3. `a_make_SnowSurfaceCharacteristic_DF.py` 파이프라인 통합 (원천 1ms 시계열 생성과 1회당 대표값 추출을 단일 스트림으로 일원화하여 연산 속도 100배 단축)
  4. 노면 디지털 트윈 3D/2D 시각화 스위트 및 시공간 2단계 보간(Spatio-Temporal Decoupling) 구조 정립
  5. 스노우 제동-노면 차분 머신러닝 보정 통합 파이프라인(`c_run_snow_correction_pipeline.py`) 및 보정 대조 데이터 테이블(`calc_corrected_comparison_table`) 모듈화

---

## 🛠️ 2. 핵심 작업 및 기술 성과

### ① `unoUtil.signal_process.post_process.resample_data` 초고속 리팩터링 (30~50배 가속)
* **문제 현상:** PyCharm/VSCode 디버깅 중 `df_raw_inter = resample_data(df_raw, '1ms')` 평가 시 3초 타임아웃 경고 발생 (`Evaluating ... did not finish after 3.00 seconds`).
* **근본 원인 분석:** 
  - CAN/GPS 등 센서 계측 데이터의 마이크로초 단위 불규칙 타임스탬프(Irregular Timeseries)를 정규 격자로 복원하기 위해 Pandas의 `resample().asfreq()`, `combine_first()`, `interpolate(method='time')`, 다시 `resample().asfreq()`라는 무거운 4단계 인덱스 병합 파이프라인을 순차 수행하고 있었음.
* **해결 조치:**
  - NumPy C-API 기반의 1차원 선형 보간기(`np.interp`)와 $O(\log N)$ 최근접 이진 탐색(`np.searchsorted`)으로 전면 재설계.
  - 시간축을 나노초 정수 배열(`view('int64')`)로 변환하여 순수 C-레벨 연속 메모리에서 $\Delta t$ 비례 선형 보간을 단숨에 완수.
  - 단조 증가 정렬 및 중복 타임스탬프 자동 보존 방어 로직 추가.
  - **결과:** 30만 행 `1ms` 리샘플링 기준 실행 시간 **3.0초 이상 ➡ 0.08초(83ms)로 30~50배 단축** (수치 오차 `0.000000` 무결성 검증 완료).

### ② `VT_ACCBRK` 온디맨드 대용량 캐시 복원 버그 완치 (`KeyError: 'Datetime'`)
* **문제 현상:** `obj_tire.result.df` 호출 시 `[Test] 0000 결과 복원 중 오류 발생하여 프로세스를 보호하기 위해 복원 비활성화: 'Datetime'` 경고가 뜨며 캐시 복원이 취소되고 `result.df`가 계속 `None`으로 남는 현상 발생.
* **근본 원인 분석:**
  - `resample_data` 고속화 당시 `pd.date_range()` 생성자에서 원본 인덱스의 명칭(`name=work_data.index.name`)을 지정하지 않아 `None`으로 유실됨.
  - `AN_ACCBRK` 내부에서 `resample_data` 수행 후 `df.reset_index(inplace=True)`를 실행했을 때 컬럼명이 `'Datetime'`이 아니라 `'index'`로 바뀌면서 `KeyError: 'Datetime'`이 발생, 무한 재시도 방지 안전장치에 의해 복원이 차단되었음.
* **해결 조치:**
  - `target_idx = pd.date_range(..., name=work_data.index.name)`로 인덱스 명칭을 완벽히 보존하도록 수정.
  - 67만 행 제동 시험 캐시 데이터가 즉시 에러 없이 정상 복원됨을 검증.

### ③ `a_make_SnowSurfaceCharacteristic_DF.py` 파이프라인 통합 및 대폭 가속 (100배 단축)
* **문제 현상:**
  - 29개 전체 센서 컬럼을 1ms로 리샘플링하여 메모리 낭비.
  - `groupby('TestNum')` 내부에서 컬럼 8개마다 `remove_outliers(..., method='isol')` 머신러닝 모델을 매번 새로 학습(fit)하여 수천 번 피팅이 발생, 스크립트 실행에 수십 분 소요.
  - `df_surface_raw` 저장 후 바로 다음 줄에서 디스크로부터 다시 읽는 불필요한 I/O 중복.
  - `Date` → `TestTireSet` → `TestNum`의 3중 중첩 for-loop 및 더미 `groupby(lambda x: 0)`로 인한 막대한 루프 오버헤드.
* **해결 조치 (Single-Pass 통합 파이프라인):**
  1. 필요한 높이/온도 컬럼(`col_raw_to_res`)만 사전에 슬라이싱하여 리샘플링 투입.
  2. **독립적 백분위수 벡터 마스킹:** 1차원 센서의 이상치는 Isolation Forest 대신 컬럼별 독립 분위수(`quantile` 0.05~0.95) 마스킹 후 `interpolate(method='time')`로 처리. 센서 간 연대책임 오염을 100% 차단하면서도 **130배 이상 가속**.
  3. **디스크 재로딩 제거 및 3중 루프 ➡ 단일 GroupBy 압축:** 디스크 재로딩 없이 메모리 상의 `df_surface_raw`에 대해 단 1줄의 Pandas 네이티브 `groupby.agg()`로 0.03초 만에 1회당 대표값(`df_surface`) 요약 완료 (30배 가속).
  4. **결과:** 전체 파이프라인 실행 시간 **수십 분 ➡ 수십 초로 98% 단축**.

### ④ 노면 3D/2D 디지털 트윈 시각화 및 시공간 보간 아키텍처 정립
* **스냅샷 vs 세션 맵의 개념적 차이 정립:**
  - `SurfaceGridSnapshot`: 특정 시점($t$)에서 트랙 전역의 격자 맵을 보유한 **순수 2D 공간 내삽/외삽기** (`query(pos_yx)`로 $(X,Y)$ 좌표의 눌림량/온도 반환).
  - `SurfaceConditionTwin`: 스냅샷들을 시간순으로 엮어 **시간 보간 함수(`interp1d`)**를 실시간 가동하는 **시공간 총괄 관리자** (`get_surface_condition(time, x, y)`).
* **2단계 시공간 디커플링 메커니즘 확인:**
  - 1단계 `sbp.build_surface_maps(method='RF')`: 각 타이어 세트 주행 단위의 정밀 공간 격자 스냅샷 생성.
  - 2단계 `sbp.match_performance_to_surface()`: 동일 세션(AM/PM) 내 스냅샷 사이에서 실시간 초 단위 선형 시간 보간 수행 (정비 리셋 물리 경계 차단).
* **`sbp.plot` 시각화 스위트 정리 및 노면 온도 시각화 가이드:**
  - `sbp.plot.surface_dashboard()`: Dash 기반 3D 실시간 인터랙티브 회전 및 시간 슬라이더 대시보드
  - `sbp.plot.map_2d(channel='temp')`: 노면 온도 2D 등고선 맵 및 `all_in_session=True` 다중 스냅샷 비교
  - `sbp.plot.map_3d(channel='temp')`: 3D 노면 온도 입체 서피스 투영 맵
  - 트랙 위치별 눌림량(`diff_height`) 및 제동거리(`BrkDist`) 산점도 오버레이 확인.

### ⑤ 스노우 제동-노면 차분 머신러닝 보정 통합 파이프라인 및 대조 데이터 테이블 모듈화
* **배경 및 목적:**
  - 분산되어 있던 `c_plot_correction_verification.py`(4대 검증 시각화)와 `c_train_correction_and_plot_maps.py`(ML 학습 및 사양 분석)를 파사드(`SnowBrakingPerformance`) 기반 단일 통합 러너(`c_run_snow_correction_pipeline.py`)로 일원화.
  - 의뢰번호 / 세트 / run(1st, 2nd) / 원래 제동거리 / 보정 제동거리 / 기상환경을 종합 대조하는 데이터 테이블 생성 기능 모듈화.
  - 슬라이드 6번 표준 등고선 맵 규격(min=0 shift, 1단위 ticks, KNN 보간)을 엔진 레벨에 표준 탑재.
* **해결 및 구현 조치:**
  1. **`calc_corrected_comparison_table()` 구현**:
     - 1st 시험: 베이스라인 기준으로 원래 제동거리 유지 ($D_{\text{corr}} = D_{\text{raw}}$, $\Delta D = 0.0$).
     - 2nd 시험: 환경 차분에 따른 모델 예측치 반영 ($D_{\text{corr}} = D_{\text{raw}} - \Delta D_{\text{pred}}$).
     - 1st와 2nd 전수 수록(209건) 및 Excel(`.xlsx`), CSV, Pickle 다형성 저장 지원.
  2. **4대 핵심 검증 시각화 모듈화 및 파사드 위임**:
     - `plot_delta_prediction_scatter`: 실측 차분치 vs 예측 차분치 $y=x$ 산점도 (Figure 1).
     - `plot_delta_braking_bar`: 타이어 세트별 제동거리 차분 바 차트 (양수: Red, 음수: Blue).
     - `plot_scatter_restoration`: 1차(Ref) vs 2차(Actual / Corrected) 제동거리 산점도 및 Adjusted $R^2$ 복원 (Figure 2).
     - `plot_correction_map`: 슬라이드 6번 표준 등고선 맵 (X/Y min=0 시프트, Z 실측 차분 유지, 10x10 격자, 1단위 눈금/레벨, Figure 3).
     - `plot_tire_subsets_comparison`: 의뢰서별 타이어 세트 실측치 vs 모델 예측치 2x2 서브플롯 (Figure 4).
  3. **통합 러너 스크립트 구축 (`c_run_snow_correction_pipeline.py`)**:
     - 데이터 로드 ➡ ML 모델 학습 ➡ 대조 엑셀 테이블 생성 ➡ 4대 검증 시각화 저장 ➡ 전수 정규화 및 세트별 분산 감소율 분석 ➡ 마크다운 보고서(`snow_correction_report.md`) 및 모델 영속화의 10단계 파이프라인 완비.
  4. **한글 글리프 누락 워닝 원천 해결**:
     - Windows `Malgun Gothic` 등 플랫폼별 한글 폰트 및 `axes.unicode_minus = False` 자동 적용.
  5. **로컬 1:1 마크다운 매뉴얼 동기화**:
     - `Snow_braking_relate_condition/correction_engine.md` 최신화
     - `Snow_braking_relate_condition/snow_braking_performance.md` 최신화
     - `c_run_snow_correction_pipeline.md` 신규 생성

---

## 🧪 3. 검증 결과 및 벤치마크

| 항목 | 기존 (AS-IS) | 개선 후 (TO-BE) | 개선 효과 |
| :--- | :---: | :---: | :---: |
| **`resample_data` (30만 행)** | 3.0초 이상 (디버거 타임아웃) | **0.08초 (83ms)** | **30~50배 가속** (오차 0.000000) |
| **`VT_ACCBRK` 캐시 복원** | `KeyError: 'Datetime'` 실패 | **정상 복원 완료 (67만 행)** | 무결성 완치 |
| **이상치 필터링 (8개 센서)** | 3.43초 (머신러닝 반복 학습) | **0.026초 (독립 분위수 벡터 연산)** | **132배 가속** (독립성 100% 보장) |
| **대표값 집계 (`df_surface`)** | 0.94초 (3중 루프 + 더미 groupby) | **0.031초 (단일 네이티브 groupby.agg)** | **30배 가속** |
| **제동-노면 차분 파이프라인** | 2개 스크립트 분산 및 수동 연산 | **단일 통합 러너 및 파사드 1줄 호출** | **원스톱 자동화 (Code 0)** |
| **보정 대조 데이터 테이블** | 미지원 (수동 집계 필요) | **1st/2nd 전수 대조 엑셀 자동 산출** | **209건 완벽 추적성 확보** |
| **등고선 보정 맵 (Figure 3)** | 음수/양수 혼재, 눈금 불일치 | **min=0 정규화 + 1단위 눈금/레벨** | **슬라이드 6번 표준 100% 일치** |
| **한글 차트 렌더링** | Glyph missing UserWarning 발생 | **Malgun Gothic 자동 바인딩** | **워닝 0건 (Clean Log)** |

---

## 🧭 4. 향후 조치 사항 및 연계 로드맵
1. **옵시디언 위키 일괄 동기화 (SSOT)**: 마크다운 매뉴얼 및 산출물 배치 미러링.
2. **현업 제동 성능 보고서 배포**: 생성된 `corrected_braking_comparison_table.xlsx` 및 4대 검증 차트를 활용하여 실무 발표 자료 최신화.
