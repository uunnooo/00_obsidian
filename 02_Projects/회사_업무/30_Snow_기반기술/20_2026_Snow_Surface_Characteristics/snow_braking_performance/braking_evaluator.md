# 🎯 snow_braking_performance.braking_evaluator 기술 매뉴얼

이 문서는 스노우 실차 제동 평가에서 1차 기준(Ref)과 2차 평가(Corr)의 원본 및 환경 보정 제동거리를 1:1 대조하고, 편차 감소율 및 원형 복원율($R^2$)을 정량 평가하는 **`SnowBrakingEvaluator`** 모듈의 명세 및 사용법을 정의합니다.

---

## 1. 📌 핵심 개요

동일 타이어를 오전(1차)과 오후(2차)에 반복 평가할 때, 트랙 다져짐 및 외기 온습도 상승으로 인해 2차 평가 시 제동거리가 변화합니다. `SnowBrakingEvaluator`는 다음의 평가 테이블 및 3대 핵심 시각화를 제공합니다:
1. **1차 vs 2차 정밀 대조표 (`calc_corrected_comparison_table`)**: 타이어 세트별 원본 오차($\Delta D_{\text{raw}}$), 보정 후 잔여 오차($\Delta D_{\text{corr}}$), 및 오차 개선율(%) 산출.
2. **편차 비교 바차트 (`plot_delta_braking_bar`)**: 보정 전 편차가 보정 후 0선으로 얼마나 근접했는지 시각화.
3. **복원율 산점도 (`plot_scatter_restoration`)**: 1차 기준 제동거리와 2차 제동거리 간의 이상적 $y=x$ 선 일치도($R^2$) 시각화.
4. **트랙 공간 제동 맵 (`plot_track_position_braking_map`)**: 트랙 위치 좌표계(PosX, PosY) 상에서의 제동거리 분포 시각화.

---

## 2. 🛠️ 핵심 클래스 및 API

### `SnowBrakingEvaluator`

| 메서드명 | 역할 | 주요 인자 | 반환값 |
| :--- | :--- | :--- | :--- |
| `calc_corrected_comparison_table(data)` | 동일 의뢰/타이어 1차 vs 2차 정밀 대조표 산출 | `data: pd.DataFrame`, `ref_order='1st'`, `corr_order='2nd'` | `pd.DataFrame` (대조표) |
| `plot_delta_braking_bar(df_comp=None, save=False)` | 타이어 세트별 보정 전/후 편차 바차트 비교 | `df_comp`, `title`, `save`, `close` | `Tuple[plt.Figure, plt.Axes]` |
| `plot_scatter_restoration(df_comp=None, save=False)` | 1차 vs 2차 복원율 산점도 ($y=x$ 대각선 대조) | `df_comp`, `title`, `save`, `close` | `Tuple[plt.Figure, Any]` |
| `plot_track_position_braking_map(data, save=False)` | 트랙 좌표계 상의 제동거리 공간 분포 맵 | `data`, `req_no`, `tire_set`, `save`, `close` | `Tuple[plt.Figure, Any]` |

---

## 3. 💡 실무 사용 예제

```python
import pandas as pd
from snow_braking_performance.braking_evaluator import SnowBrakingEvaluator

# 1. 평가기 인스턴스 초기화
evaluator = SnowBrakingEvaluator()

# 2. 보정 완료 데이터로부터 1차 vs 2차 정밀 대조표 산출
df_comp = evaluator.calc_corrected_comparison_table(df_corrected)
print(df_comp[['infor_REQ_NO', 'infor_TIRE_SET', 'Raw_Diff(m)', 'Corr_Diff(m)', 'Error_Reduction(%)']])

# 3. 핵심 3대 검증 차트 생성 및 저장
fig1, ax1 = evaluator.plot_delta_braking_bar(df_comp, save="./reports/delta_braking_bar.png", close=True)
fig2, axes2 = evaluator.plot_scatter_restoration(df_comp, save="./reports/scatter_restoration.png", close=True)
fig3, ax3 = evaluator.plot_track_position_braking_map(df_corrected, save="./reports/track_braking_map.png", close=True)
```
