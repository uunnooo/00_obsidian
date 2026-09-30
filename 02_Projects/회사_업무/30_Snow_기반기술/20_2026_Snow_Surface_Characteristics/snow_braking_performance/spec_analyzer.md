# 🔬 snow_braking_performance.spec_analyzer 기술 매뉴얼

이 문서는 환경 보정 모델 적용 전/후 타이어 사양(컴파운드, 패턴, 규격)별 분산 감소율, 변동계수(CV), 순위 일관성(Spearman, Kendall) 정량 검정 및 비교 시각화를 수행하는 **`SnowSpecAnalyzer`** 모듈의 명세 및 사용법을 정의합니다.

---

## 1. 📌 핵심 개요

노면 환경 보정이 성공적으로 이루어졌는지를 검증하는 핵심 척도는 두 가지입니다:
1. **분산 감소율 (Variance Reduction Ratio, %)**: 환경 노이즈가 제거되어 동일 사양 내에서의 제동거리 편차가 축소되었는가?
   $$\text{Var Reduction} = \left(1 - \frac{\sigma_{\text{corr}}^2}{\sigma_{\text{raw}}^2}\right) \times 100\,\%$$
2. **순위 일관성 (Ranking Consistency)**: 환경 보정으로 인해 원래 타이어 사양 고유의 성능 서열이 왜곡되지 않고 온전히 유지되었는가? (Spearman $\rho \ge 0.90$)

---

## 2. 🛠️ 핵심 클래스 및 API

### `SnowSpecAnalyzer`

| 메서드명 | 역할 | 주요 인자 | 반환값 |
| :--- | :--- | :--- | :--- |
| `calc_spec_distributions(data, spec_col='infor_CTB_COMPOUND')` | 사양별 보정 전/후 평균, 표준편차, CV 및 분산 감소율 집계 | `data`, `spec_col`, `raw_col`, `corr_col` | `pd.DataFrame` (요약 테이블) |
| `calc_ranking_consistency(data, spec_col='infor_CTB_COMPOUND')` | 사양별 보정 전/후 평균 순위의 Spearman $\rho$ 및 Kendall $\tau$ 검정 | `data`, `spec_col`, `raw_col`, `corr_col` | `Dict[str, float]` (상관계수) |
| `plot_spec_boxplots(data, spec_col='infor_CTB_COMPOUND', save=False)` | 사양별 보정 전/후 박스플롯 분포 나란히 시각화 | `data`, `spec_col`, `save`, `close` | `Tuple[plt.Figure, plt.Axes]` |
| `plot_tire_subsets_comparison(data, req_no=..., save=False)` | 의뢰서별 타이어 세트 비교 서브플롯 (1st vs 2nd_Raw vs 2nd_Corr, Figure 4) | `data`, `req_no`, `save`, `close` | `Tuple[plt.Figure, Any]` |
| `plot_track_position_braking_map(data, req_no=..., save=False)` | 트랙 좌표계(PosX, PosY)상 타이어 세트별 제동거리 공간 분포 맵 | `data`, `req_no`, `tire_set`, `save`, `close` | `Tuple[plt.Figure, Any]` |
| `plot_residual_dependency(data, env_col='char_height', save=False)` | 환경 인자와의 상관 추세 기울기(Slope) 소거 산점도 검증 | `data`, `env_col`, `save`, `close` | `Tuple[plt.Figure, Any]` |

---

## 3. 💡 실무 사용 예제

```python
import pandas as pd
from snow_braking_performance.spec_analyzer import SnowSpecAnalyzer

# 1. 사양 분석기 인스턴스 초기화
analyzer = SnowSpecAnalyzer()

# 2. 컴파운드별 분산 감소율 산출
df_spec_summary = analyzer.calc_spec_distributions(df_corrected, spec_col='infor_CTB_COMPOUND')
print(df_spec_summary[['Spec', 'Raw_Std(m)', 'Corr_Std(m)', 'Var_Reduction(%)']])

# 3. 순위 일관성 검정
ranking = analyzer.calc_ranking_consistency(df_corrected, spec_col='infor_CTB_COMPOUND')
print(f"Spearman Rho: {ranking['spearman_rho']:.4f}")

# 4. 박스플롯 및 환경 잔차 소거 산점도 시각화
fig1, ax1 = analyzer.plot_spec_boxplots(df_corrected, save="./reports/spec_boxplots.png", close=True)
fig2, ax2 = analyzer.plot_residual_dependency(df_corrected, env_col='char_height', save="./reports/residual_trend.png", close=True)
```
