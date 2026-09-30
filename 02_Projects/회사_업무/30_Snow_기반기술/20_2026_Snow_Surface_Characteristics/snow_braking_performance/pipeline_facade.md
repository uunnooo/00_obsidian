# 🏛️ snow_braking_performance.pipeline_facade 기술 매뉴얼

이 문서는 스노우 노면 환경 디지털 트윈(`snow_condition`)과 타이어 제동 성능 분석(`snow_braking_performance`)의 모든 서브모듈을 유기적으로 결합하여 데이터 로드부터 보정 모델 학습, 대조표 산출, 4대 핵심 검증 차트 렌더링까지 일원화 제어하는 **`SnowBrakingPerformance`** 마스터 파사드의 명세 및 사용법을 정의합니다.

---

## 1. 📌 핵심 개요

사용자는 복잡한 서브모듈들을 일일이 호출하지 않고도, `SnowBrakingPerformance` 단일 파사드 객체를 통해 전체 스노우 제동 보정 및 스펙 분석 파이프라인을 원스톱으로 관제할 수 있습니다.
또한 `sbp.plot.*` 네임스페이스를 통해 4대 종합 대시보드 및 각 하위 모듈의 시각화 기능을 일괄 제어할 수 있습니다.

---

## 2. 🛠️ 핵심 클래스 및 API

### `SnowBrakingPerformance`

| 메서드명 | 역할 | 반환값 |
| :--- | :--- | :--- |
| `load_and_prepare_data(file_path_or_df)` | 원본 데이터를 로드하고 47대 SSOT 표준 규격으로 일원화 | `pd.DataFrame` |
| `fit_correction(feature_cols=None)` | 동일 타이어 1차/2차 차분 데이터셋을 생성하고 6종 머신러닝 보정 모델 학습 | `Dict` (모델 평가지표) |
| `apply_correction(model_name=None)` | 최적 보정 모델을 전체 데이터에 적용하여 보정 제동거리 산출 및 정밀 대조표 생성 | `Tuple[pd.DataFrame, pd.DataFrame]` |
| `correct_dataframe(out_col=..., reference_condition=...)` | 전체 제동 데이터프레임의 모든 시험 데이터를 정량 일괄 보정하여 정규화 컬럼 추가 | `pd.DataFrame` |
| `analyze_spec_impact(spec_col=...)` | 보정 전/후 타이어 사양별 분산 감소율 및 순위 일관성 정량 분석 | `Tuple[pd.DataFrame, Dict[str, float]]` |
| `save_models(save_dir=...)` | 학습된 머신러닝 보정 모델들을 개별 바이너리(.joblib)로 영속화 저장 | `Path` |
| `save_report_md(save=..., figure_dir=...)` | 모델 평가 지표, 4대 핵심 검증 차트가 임베딩된 종합 마크다운 보고서 생성 및 다형성 저장 | `Union[Path, str]` |
| `print_summary()` | 보정 모델 R², 편차 복원율, 컴파운드 분산 감소율 종합 요약 보고서 출력 | `None` |

### `SnowBrakingPerformancePlotter` (`sbp.plot`)

| 메서드명 | 역할 |
| :--- | :--- |
| `summary_4panel(save=False)` | 4대 종합 검증 패널(복원 산점도, 편차 바차트, 박스플롯, 보정 맵) 일괄 시각화 |
| `model_comparison(save=False)` | 6종 머신러닝 회귀 모델 R² 및 MAE 바차트 |
| `correction_map(save=False)` | $\Delta H$ vs $\Delta \text{AH}$에 따른 $\Delta D$ 3D/2D 등고선 보정 맵 |
| `spec_boxplots(save=False)` | 컴파운드/패턴 사양별 보정 전/후 제동거리 박스플롯 |
| `residual_dependency(save=False)` | 환경 인자(침하 깊이)에 대한 잔차 상관성 소거 검증 차트 |
| `scatter_restoration(save=False)` | 1차 기준 제동거리 vs 2차 제동거리 원형 복원 산점도 |
| `delta_braking_bar(save=False)` | 타이어 세트별 보정 전 편차 vs 보정 후 편차 비교 바차트 |
| `surface_snapshots(idx=0, ...)` | 노면 계측 차량 2D 등고선 디지털 트윈 맵 |

---

## 3. 💡 실무 사용 예제

```python
from snow_braking_performance.pipeline_facade import SnowBrakingPerformance

# 1. 파이프라인 파사드 초기화
sbp = SnowBrakingPerformance(
    path_root="D:/uno/1. 2026/2. 25-26_Outdoor_Loop2",
    pair_mode="req_tire"
)

# 2. 데이터 적재 및 표준화
sbp.load_and_prepare_data()

# 3. 보정 모델 학습 및 데이터 보정 적용
sbp.fit_correction()
df_corr, df_comp = sbp.apply_correction()

# 4. 4대 마스터 검증 대시보드 저장
sbp.plot.summary_4panel(save="./reports/snow_master_dashboard.png", close=True)

# 5. 종합 결과 리포트 출력
sbp.print_summary()
```
