# 🏁 circuit 모듈 전면 고도화 및 정합성 완성 구현 계획서
(circuit Enhancement & Harmonization Implementation Plan)

- **문서 번호**: PLAN-CIRCUIT-20261120
- **대상 모듈**: `unoUtil.vehicle_test.circuit`
- **벤치마크 대상**: `unoUtil.vehicle_test.acc_brk` (동일 아키텍처 준수)
- **원본 소스**: `D:\uno\Python\Projects\WetHD` (도메인 수학 및 분석 알고리즘 SSOT)
- **구동 환경**: Python 3.12.4 / pandas 3.0.6 / NumPy 2.5.4 / SciPy 1.18.1 / Matplotlib 3.11.2
- **특기 사항**: 사용자의 명시적 지시 전까지 **옵시디언 볼트 위키 업데이트는 일체 진행하지 않음** (일괄 진행 원칙).

---

## 1. 배경 및 목적 (Background & Objectives)

본 작업은 실차 서킷 주행 시험 분석 모듈인 `circuit`을 완성하는 작업이다.
`circuit` 모듈은 `acc_brk` 모듈과 동일한 클린 아키텍처를 공유하여 단품 타이어 객체(`VTCircuitTire`)와 프로젝트 객체(`VTCircuitProject`)를 완벽하게 상호 운용할 수 있어야 하며, 원본 소스(`WetHD`)에서 개발된 정밀한 차량 동역학 분석 지표들과 풍부한 시각화 차트들이 누락 없이 통합되어야 한다.
또한, 최근 업그레이드된 Python 3.12 및 pandas 3.0 / NumPy 2.x 환경에서 어떠한 호환성 경고나 오동작 없이 초고속·무결점으로 구동되도록 완성도를 극대화한다.

---

## 2. 주요 개선 영역 및 세부 과제 (Key Improvement Areas)

### 영역 1. 🏗️ `acc_brk` 모듈과의 구조적 정합성 및 상호 운용성 확보
`VTAccBrkProject` 및 `VTAccBrkTire`와 100% 동일한 인터페이스 규격을 갖추어, 타이어와 프로젝트 객체를 단독 또는 묶음으로 자유롭게 사용할 수 있도록 편의 메서드를 전면 보강한다.

1. **`VTCircuitProject` 편의 메서드 추가**:
   - `add_tire_file(file: str | Path, tire: Optional[str] = None)`: `.tir` 파일 경로만 지정하여 프로젝트에 단품 타이어를 즉시 로드·편입하는 기능.
   - `collect_tire_df(cols: Optional[list] = None)`: 프로젝트 내 등록된 모든 타이어의 시계열 데이터를 타이어 세트명(`TestTireSet`) 태그와 함께 단일 통합 DataFrame으로 취합.
   - `make_summary(cols: Optional[list] = None, dropna: bool = True)`: 관심 컬럼 목록만 선택하여 정제된 요약 테이블 반환.
   - `make_summary_all(dropna: bool = True)`: 모든 원시 지표 및 보정 지표가 망라된 전체 요약 테이블 반환.
   - `make_summary_index(cols: Optional[list] = None, dropna: bool = True)`: 100 기준 상대 성능 지수(`index_*`) 컬럼만 필터링 추출.
   - `plot_index(col: str, **kwargs)`: 특정 지표의 타이어별 인덱스 비교 바 차트를 원클릭 렌더링.
   - `view_correction() -> str`: 컨트롤 타이어 대비 각 타이어의 보정 전/후 값 및 적용 계수를 정돈된 텍스트 표로 반환.
   - `save_tires(path: str | Path)`: 프로젝트에 보관된 모든 타이어 객체를 개별 `.tir` 파일들로 일괄 분할 저장.
   - `sort(by: str, ascending: bool = True)`: 타이어 순서 정렬 기능.
   - `level` 프로퍼티 (Getter/Setter): 로거 레벨을 프로젝트 및 하위 타이어들에 일괄 전파.

2. **`VTCircuitTire` 편의 메서드 추가**:
   - `add_summary(data: Optional[pd.DataFrame] = None, pattern: str = '', **kwargs)`: 외부에서 추가 산출된 요약 지표를 타이어 객체에 등록하는 기능.
   - `get_summary_keys(pattern: str = '')`: 정규식을 기반으로 타이어 요약 지표 컬럼 목록을 검색하는 편의 헬퍼.
   - `restore_cache()`: 역직렬화 로드 시 서브 분석기들의 온디맨드 캐시를 완벽 복원.

---

### 영역 2. 🔍 `WetHD` 원본 분석 알고리즘 및 핵심 지표 복원
원본 `WetHD`의 `Func_analysis_circuit.py`, `0. Main.py`, `1. Main_Lap.py`에서 개발된 핵심 알고리즘 중 간소화되거나 누락된 항목들을 정밀 복원한다.

1. **직진 오프셋 0점 보정 (`analysis_straight_cut`) 복원**:
   - 서킷 주행 중 센서 드리프트 및 타이어 정렬 오차로 발생하는 슬립각 오프셋 제거.
   - 직진 구간(예: 70m 이상) 데이터를 추출하여 `ReferSlipCOG`, `ReferSlipFront`, `ReferSlipRear`의 센서 0점을 계산하고 오프셋 보정(`DF_cut[cols] = DF_cut[cols] - offset`).
   - 유효 랩의 직진 시간 비율 `StraightRatio = (lapt['AbsLapT'] / lapt['StraightT']).mean()` 산출.

2. **다변량 동역학 이상치 정제 파이프라인 (`StatsParallelDF`) 복원**:
   - `VehSWA`, `ReferAccLateral`, `ReferSlipCOG`, `ReferSlipFront`, `ReferSlipRear` 5대 채널 결합 z-score(threshold=2.5) 필터링 파이프라인 구축.
   - 스핀, 코스 이탈, 조향 급변 구간 등의 이상치 행을 정제한 클린 데이터셋(`DF_result`) 생성 후 분석기 입력으로 전달.

3. **조향 응답 지연시간 (Steering Delay) 앙상블 알고리즘 복원**:
   - **(1) 영교차 지연 (`analysis_delay_zero`)**: SWA가 0점을 지나는 순간과 횡가속도(Ay)/요레이트(AngrZ)가 0점을 지나는 시점 간의 시간차 산출 (`ReferAccLateral_zero_delay`, `AngrZ_zero_delay`).
   - **(2) 조향 기울기 피크 지연 (`analysis_delay`)**: 조향각 변화 속도(Slope_VehSWA) 피크와 차량 응답 피크 간의 시간차 산출 (`ReferAccLateral_delay`, `AngrZ_delay`).
   - 두 지연을 결합하여 `calculate_dominant_value_kde`를 통한 KDE 밀도함수 피크(`Peak`, `Left`, `Right`) 지표 전수 산출.

4. **전/후륜 슬립각 구배(FSG, RSG) 및 KDE 피크 복원**:
   - 기존의 종합 언더스티어 구배($K_{us}$) 외에 **전륜 슬립각 구배(FSG, `ReferSlipFront_grad_raw`)** 및 **후륜 슬립각 구배(RSG, `ReferSlipRear_grad_raw`)** 산출.
   - `VehSWA_grad_raw`, `ReferSlipFront_grad_raw`, `ReferSlipRear_grad_raw` 3대 구배에 대해 KDE `Peak`, `Left`, `Right` 지표 산출.

5. **요 거동 피팅 및 시그모이드 차량 밸런스 세부 지표 복원**:
   - 이론 중립 조향선($K=0$) 대비 실제 요게인 오차 곡선(`Yawrate_error_fit`).
   - 속도/가속도 구간별 Binning 데이터(`Yawrate_gain_bin`) 및 피팅 곡선(`Yawrate_gain_fit`, `Yawrate_gain_normal_fit`).
   - 차량 밸런스 지표군 확장: `Balance`, `Balance_high`, `Balance_low` 외에 `Balance_change` (언더/오버 전이폭), `Balance_min`, `Balance_max`, `Balance_normal` 복원.

6. **전반 3랩 vs 후반 3랩 열화 분석 (Front vs Rear Laps Degradation)**:
   - `WetHD/1. Main_Lap.py`의 랩 분할 로직 복원: 총 6랩 주행 시 전반 3랩(`front_df`)과 후반 3랩(`rear_df`)을 분리.
   - 웜업 후 초기 성능 대비 후반부 타이어 열화에 따른 랩타임 드롭(`lap_time_drop`) 및 그립 저하(`grip_drop`) 지표 산출.

7. **코너 탈출 횡편차 세부 지표 (`CourseOut_Inside/Outside_Mean`)**:
   - 컨트롤 타이어 궤적 대비 코너 탈출 시 밖으로 밀려나는 양(Outside Under)과 안으로 감기는 양(Inside Over)을 정밀 산출하여 요약 테이블 및 시각화에 반영.

---

### 영역 3. 📈 시각화 (Plotter) 전면 고도화 및 WetHD 그래프 복원
단품 타이어(`PlotterTire`)와 프로젝트 비교(`PlotterProject`) 모두에 전문가용 고품질 시각화 메서드를 확충한다.
(원칙: 클래스명 접두사 중복 배제 - `plot_` 대신 행위/목적어 위주 명명)

#### 1) `PlotterTire` (단일 타이어 전용)
- **기존 8대 대시보드 유지·개선**: `lap_times`, `steering_delay`, `course_in_out`, `understeer_curve`, `yaw_dynamics`, `friction_circle`, `racing_line`, `acceleration_track_map`.
- **신규 추가 메서드**:
  1. `dynamics_3d(x_col, y_col, z_col)`: `ReferVelLateral` vs `VehSWA_grad_raw` vs `VelHorizontal` 등 3차원 산점도 및 컬러바 동역학 맵 (`plt_3D_Colorbar` 계승).
  2. `straight_offset()`: 직진 오프셋 보정 전(Raw) vs 보정 후(Offset)의 `ReferAccLateral` vs `ReferSlipFront/Rear` 비교 산점도.
  3. `gradient_kde()`: SWA 구배, 전륜 슬립각 구배(FSG), 후륜 슬립각 구배(RSG)의 KDE 밀도곡선 3분할 대시보드.

#### 2) `PlotterProject` (멀티 타이어 비교 전용)
- **기존 6대 메서드 유지·개선**: `lap_comparison`, `friction_circle`, `understeer_curve`, `course_in_out`, `side_slip`, `radar_summary`.
- **신규 추가 메서드 (WetHD 핵심 비교 차트 전수 구현)**:
  1. `yaw_comparison()` (`plt_compare_parameter_Yaw` 복원):
     - 4분할 레이아웃: (1) 이론선 대비 요게인 실측선 중첩 + (2) 요게인 피팅 곡선 비교 + (3) 마찰원 경계선 비교 + (4) 주요 지표(`LapTime`, `YawGain_G0`, `YawGain_Slope`) 바 차트.
  2. `parameter_bars()` (`plt_compare_parameter_bar` 복원):
     - Bar Group 1 (조향/그립): `VehSWA`, `Slope_VehSWA`, `Slope_VehSWA_peak`, `LateralGrip_abs_max`, `LongGrip_brk_min`, `GG_area`.
     - Bar Group 2 (안정성/구배): `count_level`, `VehSWA_grad_raw`, `ReferSlipRear_grad_raw`, `ReferAccLateral_delay`, `Yawrate_stability`, `Yawrate_range`.
  3. `balance_comparison()` (`plt_compare_balance` / `horizontal` 복원):
     - 시그모이드 차량 밸런스(`Balance`, `Balance_low`, `Balance_high`) 에러바/구간 비교 막대 차트.
  4. `racing_line_comparison()`:
     - 모든 타이어의 대표 랩 GPS 주행 궤적(PosX, PosY) 및 기준선 대비 Signed CTE 편차 중첩 비교 차트.
  5. `plot_index(metric_col)`:
     - 특정 성능 지표의 100 기준 상대 지수(`index_*`) 비교 바 차트.

---

### 영역 4. 🐍 Python 3.12 / pandas 3.0 / NumPy 2.5 환경 최적화
- **pandas 3.0 Copy-on-Write (CoW)**:
  - 체인드 인덱싱 완전 제거 및 모든 값 대입 시 `.loc[mask, col] = val` 표준 문법 적용.
  - `groupby().mean()`, `groupby().std()` 호출 시 `numeric_only=True` 전수 명시.
- **SciPy 1.18 ODR 감가 경고 대응**:
  - `from scipy import odr` 대신 `scipy.optimize.curve_fit` 기반의 견고한 비선형 피팅으로 전환 및 안전한 예외 fallback 처리.
- **NumPy 2.x 규격 준수**:
  - `np.NaN`, `np.float_` 등 레거시 별칭 사용 방지, `np.nan`, `float`, `int`, `np.float64` 일관 적용.
- **멀티프로세싱 안정성**:
  - `_analyze_single_circuit_tire_worker`의 Top-level 함수 배치 유지 및 직렬화 안전성(Pickleability) 보장.

---

## 3. 단계별 상세 구현 로드맵 (Phased Implementation Plan)

```
[Phase 1: 코어 알고리즘]
  ├─ func_circuit.py: 직진 오프셋, 다변량 이상치, 영교차/슬로프 결합 지연, FSG/RSG 구배 함수 구현
  └─ analyzers/: an_lap_time, an_steering_delay, an_understeer_gradient, an_yaw_gain_stability 고도화
       ↓
[Phase 2: Tire & Project 객체 인터페이스 완성]
  ├─ vt_circuit_tire.py: 전처리 오프셋/이상치 연동, 전/후반 랩 분할, add_summary, get_summary_keys 구현
  └─ vt_circuit_project.py: add_tire_file, collect_tire_df, make_summary 계열, view_correction, save_tires 구현
       ↓
[Phase 3: 시각화 엔진 고도화]
  ├─ plotter_tire.py: dynamics_3d, straight_offset, gradient_kde 추가
  └─ plotter_project.py: yaw_comparison, parameter_bars, balance_comparison, racing_line_comparison 추가
       ↓
[Phase 4: 실데이터 통합 검증 및 테스트]
  ├─ Technoring 실데이터(VBO 6개) 기반 원스톱 배치 분석 검증
  ├─ 단품 타이어 캐시(.tir) 및 프로젝트 캐시(.pjt) 저장/복원 검증
  └─ 차트 이미지(1.figure) 및 결과 테이블(2.result) 무결성 확인
       ↓
[Phase 5: 순수 1:1 코드 매뉴얼 최신화]
  └─ vt_circuit.md, vt_circuit_tire.md, vt_circuit_project.md 등 기술 매뉴얼 최신화
       (※ 옵시디언 볼트 위키 업데이트는 사용자 지시 전까지 보류)
```

---

## 4. 검증 및 테스트 전략 (Verification Strategy)

1. **단위 테스트 (Unit Verification)**:
   - 각 analyzer의 `analysis()` 메서드가 확장된 지표들을 올바르게 계산하여 `self.summary`에 반환하는지 검증.
   - `VTCircuitProject`의 편의 메서드(`add_tire_file`, `collect_tire_df`, `make_summary`, `view_correction`) 단위 검증.
2. **실데이터 통합 회귀 테스트 (End-to-End Regression Test)**:
   - `D:\uno\Python\Projects\unoUtil\test_data\handling\Technoring`의 6개 타이어 실데이터(`TR-T1` ~ `TR-T6`)를 대상으로 `vt_circuit()` 전체 파이프라인 구동.
   - 3대 표준 디렉터리(`0.db`, `1.figure`, `2.result`) 산출물 검증:
     - `0.db/*.tir`, `0.db/*.pjt` 정상 직렬화 및 `load_pjt=True`, `load_tire=True` 초고속 복원 확인.
     - `1.figure/*.png` 모든 신규 대시보드 및 비교 차트 정상 렌더링 확인.
     - `2.result/*.csv` 100여 개 핵심 지표 및 보정 지표의 완전성 확인.
3. **Python 3.12 환경 경고 제로 검증**:
   - `python -W error::DeprecationWarning` 수준의 엄격 모드에서 실행하여 deprecation 경고가 발생하지 않는지 확인.
