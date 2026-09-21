# ❄️ snow_braking_performance.py 로컬 개발 매뉴얼

이 모듈은 스노우 노면 상태 계측 데이터와 실차 제동 평가 데이터의 수집 및 전처리, 3D 시공간 디지털 트윈 보간 맵 빌드, 차분 머신러닝 성능 보정, 그리고 타이어 스펙 영향도 정량 검증까지 분석 프로세스 전반을 단일 파사드(Facade) 아키텍처로 원스톱 제어하는 통합 마스터 클래스(`SnowBrakingPerformance`)와 전문 시각화 플로터(`SnowBrakingPerformancePlotter`)를 구현하고 있습니다.

---

## 🏛️ 1. API 명세 및 상세 설계

### 1.1 `SnowBrakingPerformance`
플랫폼을 통합 관장하는 마스터 파사드 클래스입니다.
* **주요 등록 및 맵 빌더**:
  * `add_surface_data(data)`: 노면 계측 데이터프레임 또는 파일을 등록합니다.
  * `add_braking_data(data)`: 실차 제동 평가 데이터를 등록합니다.
  * `set_weather_data(df_weather)`: 기상관측 데이터를 연동하고 과포화 습도를 분석합니다.
  * `set_spec_data(df_spec)`: 타이어 사양(컴파운드, 패턴, 규격) 메타데이터를 등록합니다.
  * `calc_surface_maps(method, group_col)`: 노면 디지털 트윈 격자를 빌드합니다. (하위 호환성 에일리어스: `build_surface_maps`)
* **핵심 연산 및 보정**:
  * `calc_matched_performance()`: 제동 시험 좌표와 시각에 정밀 대응되는 실시간 노면 데이터를 매칭 결합합니다. (하위 호환성 에일리어스: `match_performance_to_surface`)
  * `calc_trained_correction_model(model_type, features, target)`: 차분법 기반 머신러닝 보정 모델을 학습시킵니다. (하위 호환성 에일리어스: `train_correction_model`)
  * `calc_corrected_braking_distance(raw_dist, cur_condition, ref_condition)`: 현재 시험 조건에 대한 실시간 제동거리 보정치를 산출합니다. (하위 호환성 에일리어스: `correct_braking_distance`)
  * `calc_corrected_dataframe(out_col, ref_condition)`: 전체 제동 데이터를 일괄 정규화 보정합니다. (하위 호환성 에일리어스: `correct_dataframe`)
  * `calc_spec_impact(spec_col)`: 보정 전/후 컴파운드별 분산 감소 효과 및 순위 일관성을 분석합니다. (하위 호환성 에일리어스: `analyze_spec_impact`)

### 1.2 `SnowBrakingPerformancePlotter`
마스터 클래스 내부의 데이터 및 분석 엔진을 사용하여 차트를 생성하는 전용 플로터 클래스입니다. (`sbp.plot` 멤버 변수를 통해 구동)
* **모든 플롯 함수는 `save: Union[bool, str, Path] = False` 및 `close: bool = True` 파라미터를 탑재하고 있어 백그라운드 구동(Non-blocking)과 4단계 저장 다형성을 완벽하게 보장합니다.**
* **제공 시각화 맵**:
  * `plot_session_3d_map(date, period)`: 세션별 3D 보간 투영 및 실측 3D 매칭 도트 맵 가시화.
  * `plot_session_2d_overlay(date, period)`: 개별 런의 제동거리, 좌/우 침하 텍스트가 조밀하게 오버레이된 2D 평면 등고선 맵.
  * `plot_tire_subplot_scatters(req_no)`: 의뢰번호별 타이어 세트를 다중 서브플롯(예: 2x2 격자)에 시각화.
  * `plot_delta_correction_map()`: 오전/오후 재현 평가의 편차(Delta) 데이터를 활용한 다변량 등고선 보정 맵.
  * `surface_map()`, `correction_map()`, `spec_boxplots()`, `residual_dependency()`, `model_comparison()`, `spec_analysis()`: 하위 엔진의 개별 시각화 프록시 메서드.

---

## 💻 2. 실무 활용 예제

```python
import pandas as pd
from Snow_braking_relate_condition.snow_braking_performance import SnowBrakingPerformance

# 1. 마스터 플랫폼 객체 생성
sbp = SnowBrakingPerformance(name="SnowPlatform_2026")

# 2. 노면, 제동, 기상 및 스펙 데이터 연동 및 주입
sbp.add_surface_data("./df_surface_raw.pkl")
sbp.add_braking_data("./df_braking_raw.pkl")
sbp.set_weather_data("./df_weather_kma.pkl")
sbp.set_spec_data("./df_spec_meta.pkl")

# 3. 3D 디지털 트윈 구축 및 실시간 노면 조건 1:1 GPS 매칭 결합
sbp.calc_surface_maps(method='RF')
sbp.calc_matched_performance()

# 4. 차분법 머신러닝 학습 및 일괄 정규화 보정
sbp.calc_trained_correction_model(model_type='Random Forest')
df_normalized = sbp.calc_corrected_dataframe(out_col='char_brk_dist_corr')

# 5. 컴파운드 사양별 영향 분석 및 분산 감소율 집계
df_summary, ranking_metrics = sbp.calc_spec_impact(spec_col='infor_CTB_COMPOUND')
print(df_summary[['Spec', 'Var_Reduction(%)']])

# 6. 정밀 시각화 맵 생성 및 자동 저장 (Non-blocking)
sbp.plot.plot_session_2d_overlay(
    date="2026-01-20", 
    period="am", 
    save=True,  # 사내 디폴트 저장 폴더에 저장
    close=True  # 메모리 완전 해제 및 hang 차단
)
```
