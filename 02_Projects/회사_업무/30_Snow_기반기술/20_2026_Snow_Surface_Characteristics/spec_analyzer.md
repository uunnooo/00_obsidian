# ❄️ spec_analyzer.py 로컬 개발 매뉴얼

이 모듈은 스노우 제동 성능 보정 전/후의 타이어 사양(컴파운드, 패턴, 규격) 영향도를 분석하고, 보정 알고리즘을 거친 제동 성능 지표의 분산 감소 효과 및 순위 일관성(상관 계수)을 정량 검증하기 위한 데이터 분석 및 시각화 전용 클래스입니다.

---

## 🏛️ 1. API 명세 및 상세 설계

### 1.1 `calc_spec_distributions(df, spec_col, raw_col, corr_col, **kwargs)`
각 사양별로 보정 전과 보정 후의 평균, 표준편차, 변동계수(C.V, %)를 비교 집계하고, **군집 내 분산 감소율(Variance Reduction Ratio, %)**을 산출합니다.
* **인자**:
  * `df (pd.DataFrame)`: 분석 대상 제동 통합 데이터프레임 (제동 1회 단위)
  * `spec_col (str)`: 사양 구분 컬럼명 (기본값: `'infor_CTB_COMPOUND'`)
  * `raw_col (str)`: 보정 전 제동거리 컬럼명 (기본값: `'char_brk_dist'`)
  * `corr_col (str)`: 보정 후 제동거리 컬럼명 (기본값: `'char_brk_dist_corr'`)
  * `**kwargs`: 구버전 파라미터 `df_input` 및 `str_spec_col` 등을 유연하게 흡수하기 위한 가변 사전
* **반환값**:
  * `pd.DataFrame`: 사양별 통계요약 및 분산감소율 표
* **하위 호환성 에일리어스**:
  * `compare_spec_distributions`

### 1.2 `calc_ranking_consistency(df, spec_col, raw_col, corr_col, **kwargs)`
보정 전/후의 사양별 평균 제동거리를 기준으로 순위를 매긴 뒤, 순위 상관 계수인 **스피어만 랭크 계수(Spearman's Rho)**와 **켄달 타우(Kendall's Tau)**를 구하여 순위 일관성을 분석합니다.
* **인자**:
  * `df (pd.DataFrame)`: 분석 대상 제동 통합 데이터프레임
  * `spec_col (str)`: 사양 구분 컬럼명 (기본값: `'infor_CTB_COMPOUND'`)
  * `raw_col (str)`: 보정 전 제동거리 컬럼명
  * `corr_col (str)`: 보정 후 제동거리 컬럼명
* **반환값**:
  * `Dict[str, float]`: `spearman_rho`, `kendall_tau`, `p_value` 정보를 담은 사전
* **하위 호환성 에일리어스**:
  * `check_ranking_consistency`

### 1.3 `plot_spec_boxplots(df, spec_col, raw_col, corr_col, title, save, close)`
각 사양별 보정 전(Raw) vs 보정 후(Corrected)의 제동거리 데이터 분포를 나란히 배치한 비교 박스플롯을 플로팅합니다.
* **인자**:
  * `save (Union[bool, str, Path])`: 저장 다형성 옵션
  * `close (bool)`: 시각화 자원 해제 여부 (기본값: `True`)
* **반환값**:
  * `Tuple[plt.Figure, plt.Axes]`

### 1.4 `plot_residual_dependency(df, env_col, raw_col, corr_col, title, save, close)`
특정 환경 변수(예: 눈 침하 깊이 `char_height`)에 대한 제동거리의 추세 기울기(Slope)가 보정 후에 0으로 완벽히 수렴하여 환경 의존성이 해제되었음을 입증하는 산점도를 그립니다.
* **인자**:
  * `env_col (str)`: 분석 대상 환경 인자 (기본값: `'char_height'`)
* **반환값**:
  * `Tuple[plt.Figure, axes]`

---

## 💻 2. 실무 활용 예제

```python
import pandas as pd
from Snow_braking_relate_condition.spec_analyzer import SnowSpecAnalyzer

# 1. 분석기 생성 및 데이터 로드
analyzer = SnowSpecAnalyzer()
df_corrected_runs = pd.read_pickle("./df_corrected.pkl")

# 2. 사양별 분산 감소 효과 및 통계량 산출
df_summary = analyzer.calc_spec_distributions(
    df=df_corrected_runs,
    spec_col='infor_CTB_COMPOUND'
)
print(df_summary[['Spec', 'Var_Reduction(%)']])

# 3. 보정 전/후 순위 일관성 지표 분석
rank_metrics = analyzer.calc_ranking_consistency(df_corrected_runs)
print(f"Spearman's Rho: {rank_metrics['spearman_rho']:.4f}")

# 4. Non-blocking 시각화 및 자동 저장
fig, ax = analyzer.plot_spec_boxplots(
    df=df_corrected_runs,
    save=True,  # 디폴트 사내 보관함에 자동 저장
    close=True  # 메모리 누수 방지를 위한 Close 처리
)
```
