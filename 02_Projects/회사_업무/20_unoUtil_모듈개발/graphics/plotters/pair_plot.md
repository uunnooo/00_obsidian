# 📊 graphics.plotters.pair_plot (PairPlot with Correlation & Scatter)

## 1. 개요
`unoUtil.graphics.plotters.pair_plot` 모듈은 다변량(Multivariate) 데이터의 상관 분석을 위해
- **하삼각(Lower Triangle)**: 피어슨 상관계수(r) 크기 및 유의수준(p-value)에 비례하는 컬러 히트맵 사각형
- **상삼각(Upper Triangle)**: 투명도가 적용된 정밀 산점도(Scatter Plot)
- **대각선(Diagonal)**: 변수별 분포를 나타내는 히스토그램(KDE 결합)
을 하나의 일체형 Seaborn `PairGrid`로 시각화하는 고성능 플로터입니다.
과거 `unoUtil.graphicTools._PairPlotCorrWithScatter_`의 100% 하위 호환을 지원하며, Matplotlib Non-blocking 표준을 준수합니다.

---

## 2. 주요 기능 및 API

### `PairPlotCorrWithScatter(df: pd.DataFrame, vars: Optional[List[str]] = None, r_threshold: Optional[float] = None, base_per_subplot: float = 0.5, dpi: int = 100) -> sns.PairGrid`
- **Args**:
  - `df` (`pd.DataFrame`): 시각화 대상 데이터프레임.
  - `vars` (`List[str]`, optional): 시각화에 포함할 변수 컬럼 리스트. 기본값은 모든 수치형 컬럼.
  - `r_threshold` (`float`, optional): 상관계수 필터링 임계값. 이 값 이상의 강한 상관관계를 가진 변수 조합만 필터링.
  - `base_per_subplot` (`float`): 서브플롯 1개당 인치 크기 배율. 기본값 `0.5`.
  - `dpi` (`int`): 플롯 해상도 DPI. 기본값 `100`.

- **Returns**:
  - `sns.PairGrid`: 생성된 페어그리드 객체 (`g.fig.savefig(...)`로 저장 가능).

```python
import pandas as pd
from unoUtil.graphics.plotters.pair_plot import PairPlotCorrWithScatter
# 또는 레거시 호환 경로
from unoUtil.graphicTools._PairPlotCorrWithScatter_ import PairPlotCorrWithScatter

df = pd.DataFrame({
    'Speed': [50, 60, 70, 80],
    'Dist': [15, 22, 31, 42],
    'Temp': [20, 22, 21, 23]
})
g = PairPlotCorrWithScatter(df)
g.fig.savefig("correlation_analysis.png", dpi=150)
```

---

## 3. 관련 문서
- [[unoUtil/graphics/plotters/plotter|Plotter 기본 매뉴얼]]
- [[unoUtil/graphics/format_fig|Figure 포맷터 매뉴얼]]
