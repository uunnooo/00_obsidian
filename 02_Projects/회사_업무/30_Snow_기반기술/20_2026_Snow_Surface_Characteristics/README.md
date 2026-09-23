# ❄️ Snow_braking_relate_condition 패키지 매뉴얼

스노우 노면 특성 디지털 트윈, 실차 제동 성능 보정 및 사양 영향도 분석 통합 모듈입니다.  
기존 개별 분석 스크립트들을 단일 파사드(Facade) 클래스인 **`SnowBrakingPerformance`**로 유기적으로 엮어 원스톱 관리할 수 있도록 설계되었습니다.

---

## 📁 1. 패키지 모듈 아키텍처

```text
Snow_braking_relate_condition/
├── __init__.py                     # 패키지 진입점 및 모듈/함수 export
├── Snow_Braking_Performance.py     # [통합 파사드] SnowBrakingPerformance 마스터 컨트롤러
├── surface_condition_twin.py       # [디지털 트윈] 센서 오프셋 보정, 3D 트랙 격자 맵, 시공간 보간
├── correction_engine.py            # [보정 엔진] 차분법(Difference Method) 머신러닝 보정 (RF, KNN, SVR)
├── spec_analyzer.py                # [스펙 분석] 보정 전/후 사양별 분산 감소율, CV%, 순위 일관성 분석
├── snow_physics_utils.py           # [물리 유틸] Libbrecht 과포화도, 눈 압축률 및 밀도 역추정식
└── README.md                       # 패키지 구조 및 활용 가이드 (본 문서)
```

---

## 🚀 2. 주요 클래스 및 워크플로우

### 2.1 통합 마스터 클래스: `SnowBrakingPerformance`
- **데이터 등록 (Ingestion)**:
  - `add_surface_data(data)`: 노면 계측 로우데이터프레임 또는 `VT_ACCBRK` 계측 객체 등록
  - `add_braking_data(data)`: 제동 평가 데이터프레임 또는 `VT_ACCBRK_PROJECT` / `VT_ACCBRK_TIRE` 객체 등록
  - `set_weather_data(df_weather)`: 기상청 데이터 등록 (과포화도/절대습도 자동 계산)
  - `set_spec_data(df_spec)`: 컴파운드, 패턴, 규격 메타데이터 등록
- **노면 디지털 트윈 (Digital Twin)**:
  - `build_surface_maps(method='RF')`: 센서 오프셋 정렬 및 트랙 전역 3D 노면 맵 생성
  - `match_performance_to_surface()`: 제동 시험 좌표 및 시각을 1:1 결합 (`char_height`, `char_temp`)
- **차분 보정 머신러닝 (ML Correction)**:
  - `train_correction_model(model_type='Random Forest')`: 동일 타이어 반복 차분 학습
  - `generate_correction_map()`: 3D 보정 등고선 맵 생성
- **제동거리 정규화 보정 (Correction Prediction)**:
  - `correct_braking_distance(raw_dist, cur_condition, ref_condition)`: 실시간 단일 보정 질의
  - `correct_dataframe(out_col='char_brk_dist_corr')`: 전체 데이터프레임 일괄 보정
- **타이어 사양 영향도 분석 (Spec Impact)**:
  - `analyze_spec_impact(spec_col='infor_CTB_COMPOUND')`: 분산 감소율 및 순위 상관관계 산출
- **전용 시각화 및 인터랙티브 대시보드 제품군 (Visualization Suite)**:
  - `plot_2d_map(date, set, ...)`: 2D 평면 등고선/서피스 맵 (단일 세트, 세션 전체 서브플롯, 센서 도트 오버레이)
  - `plot_3d_map(date, set, ...)`: 3D 공간 입체 서피스 맵 (바닥면 2D 등고선 투영, 센서 도트 3D 산점도)
  - `launch_surface_dashboard(port=8050)`: Dash 기반 노면 시공간 대시보드 웹 앱 자동 구동
  - `plot_track_position_braking_map()`: 트랙 좌표계(PosX, PosY) 상의 2D/3D 제동거리 공간 분포 맵
  - `plot_correction_map()`: 노면 높이차 vs 절대습도차에 따른 제동거리 변화량(ΔBrkDist) 3D 등고선 보정맵
  - `plot_spec_boxplots(spec_col)`: 보정 전(Raw) vs 보정 후(Corrected) 사양별 박스플롯 비교
  - `plot_residual_dependency(env_col)`: 환경 인자와의 잔차/기울기 소거(Slope=0) 검증 산점도
  - `plot_model_comparison()`: Random Forest, KNN, SVR 등 머신러닝 모델 성능(R², MAE) 비교

---

## 📐 2.2 입력 데이터 단위 및 규격 (Data Granularity)
- **단위**: **제동 1회(Run) = 1개 행(Row)**
  - 세트 평균(Mean)이 아닌, **개별 1회 제동(Run)**마다의 초 단위 `Datetime`, `PosX`, `PosY`, 실측 제동거리 `char_brk_dist`가 들어갑니다.
  - 이렇게 해야 각 제동이 일어난 트랙 상의 정확한 지점(X, Y)과 시각의 노면 침하 깊이 및 기상 조건을 1:1로 정밀 결합할 수 있습니다.
  - `VT_ACCBRK_PROJECT`나 `VT_ACCBRK_TIRE` 객체를 그대로 인입하면 내부의 개별 런(`result.df`)을 자동으로 추출하여 결합합니다.

## 💡 3. 실제 사용 예시 코드

```python
from Snow_braking_relate_condition import SnowBrakingPerformance

# 1. 통합 컨트롤러 객체 생성
sbp = SnowBrakingPerformance(name="SnowPlatform_2026")

# 2. 노면 및 제동(ACCBRK 객체) 데이터 추가
sbp.add_surface_data(df_surface_raw)   # 또는 ACCBRK 노면 계측 객체
sbp.add_braking_data(obj_accbrk_pjt)   # VT_ACCBRK_PROJECT 또는 VT_ACCBRK_TIRE 객체
sbp.set_weather_data(df_weather)       # 기상청 데이터 (과포화도 자동 산출)
sbp.set_spec_data(df_spec)             # 타이어 규격 메타데이터

# 3. 3D 노면 디지털 트윈 생성 및 제동 데이터와 매칭
sbp.build_surface_maps(method='RF')
df_matched = sbp.match_performance_to_surface()

# 4. 차분 머신러닝 보정 모델 학습
metrics = sbp.train_correction_model(model_type='Random Forest')
print("모델 평가:", metrics)

# 5. 원하는 조건으로 즉시 제동거리 보정
corr_dist = sbp.correct_braking_distance(
    raw_dist=24.5,
    cur_condition={'char_height': 3.8, 'cd_test_ah': 2.1},
    ref_condition={'char_height': 3.0, 'cd_test_ah': 1.5}
)
print(f"보정된 제동거리: {corr_dist:.2f} m")

# 6. 전체 데이터프레임 일괄 보정 및 스펙 영향도 분석
df_all_corr = sbp.correct_dataframe()
summary, rank_metrics = sbp.analyze_spec_impact(spec_col='infor_CTB_COMPOUND')
print(summary)

# 7. 분석 상태 저장 및 리포트
sbp.summary()
sbp.save("./saved_platforms/snow_platform_2026.pkl")
```

---

## 🌲 4. 계층형 로거(`LOGGER`) 및 정량적 벤치마크

패키지 전역에 `unoUtil.convenienceFunction.logger.LOGGER`가 적용되어, 날것의 `print` 없이 구조화된 계층 로그 및 구간 소요 시간 측정을 제공합니다.

### 4.1 로거 트리 구조
```text
[SnowBraking] (Root)
 ├── [SnowBraking.Master]    : Snow_Braking_Performance.py
 ├── [SnowBraking.Twin]      : surface_condition_twin.py
 ├── [SnowBraking.Engine]    : correction_engine.py
 ├── [SnowBraking.Spec]      : spec_analyzer.py
 ├── [SnowBraking.Physics]   : snow_physics_utils.py
 └── [SnowBraking.Dashboard] : surface_dashboard.py
```

### 4.2 실행 안정성 특징
- **모듈/스크립트 양방향 지원**: `try...except ImportError` fallback 내장으로 패키지 임포트 및 단독 스크립트 실행 모두 지원
- **인자 Alias 호환**: `correct_braking_distance`의 `reference_condition` 및 `ref_condition` 키워드 지원
- **Windows 인코딩 방어**: 터미널 `cp949` 환경 시 유니코드/이모지 출력 에러 완전 차단
- **무중단 시각화**: 모든 시각화 함수는 GUI를 블로킹하지 않고 Figure 객체 반환 또는 비차단 방식으로 작동

