---
id: "snow_braking_performance_20260923"
title: "snow_braking_performance 상세 매뉴얼"
type: resource
category_main: 회사_업무
category_sub: 개발매뉴얼
date: 2026-09-23
status: 완료
tags:
  - 회사_업무
  - SnowSurface
  - 통합파사드
  - 제동보정
  - 매뉴얼
project_link: "[[00_2026_Snow_Surface_Characteristics_대시보드]]"
---

# ❄️ snow_braking_performance.py 로컬 개발 매뉴얼

이 모듈은 스노우 노면 상태 계측 데이터와 실차 제동 평가 데이터의 수집 및 전처리, 3D 시공간 디지털 트윈 보간 맵 빌드, 차분 머신러닝 성능 보정, 종합 대조 데이터 테이블 생성, 4대 핵심 검증 시각화, 그리고 타이어 스펙 영향도 정량 검증까지 분석 프로세스 전반을 단일 파사드(Facade) 아키텍처로 원스톱 제어하는 통합 마스터 클래스(`SnowBrakingPerformance`)와 전문 시각화 플로터(`SnowBrakingPerformancePlotter`)를 구현하고 있습니다.

---

## 🏛️ 1. API 명세 및 상세 설계

### 1.1 `SnowBrakingPerformance`
플랫폼을 통합 관장하는 마스터 파사드 클래스입니다.

#### [데이터 적재 및 맵 빌더]
* `load_combined_data(path_or_df)`: 통합 데이터셋(제동+노면+기상+스펙)을 1줄로 로드, 검증 및 `is_performance_matched = True` 동기화.
* `add_surface_data(data)`: 노면 계측 데이터프레임 또는 파일을 등록합니다.
* `add_braking_data(data)`: 실차 제동 평가 데이터를 등록합니다.
* `set_weather_data(df_weather)`: 기상관측 데이터를 연동하고 과포화 습도를 분석합니다.
* `set_spec_data(df_spec)`: 타이어 사양(컴파운드, 패턴, 규격) 메타데이터를 등록합니다.
* `calc_surface_maps(method, group_col)`: 노면 디지털 트윈 격자를 빌드합니다. (에일리어스: `build_surface_maps`)

#### [핵심 연산, 머신러닝 및 데이터 테이블]
* `calc_matched_performance()`: 제동 시험 좌표와 시각에 정밀 대응되는 실시간 노면 데이터를 매칭 결합합니다. (에일리어스: `match_performance_to_surface`)
* `train_correction_model(model_type, features, target, auto_tune=False, model_params=None, cv=5)`: 차분법 기반 머신러닝 보정 모델을 학습시킵니다. 5-Fold 교차검증 기반 오토 튜닝(`auto_tune=True`) 및 수동 튜닝(`model_params`) 지원.
* `calc_corrected_comparison_table(df=None, model_name=None, save=False, **kwargs)`: 🚀 **[2026 신설]** 의뢰번호, 타이어 세트별 1st와 2nd 시험의 원래 제동거리, 보정 제동거리, 예측 변화량, 기상/노면 환경 요인을 종합 대조하는 분석 데이터프레임을 생성하고 엑셀/CSV/Pickle로 다형성 저장합니다.
  * 1st 시험은 기준 베이스라인(보정치=원래치, 변화량=0.0)
  * 2nd 시험은 1st 기준 환경으로 정규화 ($D_{\text{corr}} = D_{\text{raw}} - \Delta D_{\text{pred}}$)
* `correct_dataframe(out_col, ref_condition)`: 전체 제동 데이터를 일괄 정규화 보정합니다. (에일리어스: `calc_corrected_dataframe`)
* `analyze_spec_impact(spec_col)`: 보정 전/후 컴파운드별 분산 감소 효과 및 순위 일관성을 분석합니다. (에일리어스: `calc_spec_impact`)
* `save_report_md(save=True, figure_dir=None)`: 모델 메트릭, 최적 파라미터, 기준 조건, 타이어별 산포 감소율, 차트 링크를 종합 마크다운(.md) 보고서로 자동 생성 및 저장합니다.

#### [핵심 검증 시각화 (4대 차트)]
모든 시각화 메서드는 Non-blocking(`close=True`) 및 다형성 저장(`save`)을 표준 지원합니다.
* `plot_delta_prediction_scatter(save, close)`: 차분 예측 모델 성능 검증 (실측 차분 vs 예측 차분 산점도, $y=x$ 기준선).
* `plot_delta_braking_bar(save, close)`: 동일 타이어 반복 시험 간 제동거리 차이($\Delta\text{BrkDist}$) 세트별 바 차트.
* `plot_scatter_restoration(save, close)`: 1차(Ref) vs 2차(Actual: 빨강 / Corrected: 파랑) 제동거리 산점도 및 Adjusted $R^2$ 복원 성능.
* `plot_correction_map(model_name, shift_min_zero=True, resolution=10, ...)`: 환경 인자 변화량에 따른 제동거리 변화량 2D 등고선 보정 맵 (슬라이드 6번 표준 사양).
* `plot_tire_subsets_comparison(req_no, save, close)`: 의뢰서 내 주요 타이어 세트(C1, C2, T1, T2)별 실측치 vs 모델 예측치 2x2 서브플롯.

---

## 💻 2. 실무 활용 예제

```python
from pathlib import Path
from Snow_braking_relate_condition.snow_braking_performance import SnowBrakingPerformance

# 1. 마스터 플랫폼 객체 생성
sbp = SnowBrakingPerformance(name="SnowPlatform_2026")

# 2. 통합 데이터셋 1줄 적재 (1964행 자동 정합성 검증)
sbp.load_combined_data(r"D:\uno\1. 2026\2. 25-26_Outdoor_Loop2\0. db\1. df_combine_test_surface_spec.pkl")

# 3. 차분 머신러닝 모델 학습 (Random Forest 등 다중 모델)
metrics = sbp.train_correction_model(
    model_type='Random Forest',
    features=['char_height', 'cd_test_ah'],
    target='char_brk_dist'
)

# 4. 보정 대조 데이터 테이블 생성 및 엑셀 저장
df_table = sbp.calc_corrected_comparison_table(
    save=Path("./output/corrected_comparison_table.xlsx")
)

# 5. 4대 핵심 검증 시각화 생성 및 일괄 저장
output_dir = Path("./figures")
sbp.plot_delta_prediction_scatter(save=output_dir / "1_Diff_Actual_vs_Predicted.png", close=True)
sbp.plot_scatter_restoration(save=output_dir / "2_Final_Correction_1st_vs_2nd.png", close=True)
sbp.plot_correction_map(model_name='KNN Regressor', shift_min_zero=True, save=output_dir / "3_Snow_Contour.png", close=True)
sbp.plot_tire_subsets_comparison(req_no='25RD110006EF', save=output_dir / "4_Tire_Subplots_25RD110006EF.png", close=True)

# 6. 종합 마크다운 보고서 저장
sbp.save_report_md(save=Path("./output/snow_correction_report.md"), figure_dir=output_dir)
```
