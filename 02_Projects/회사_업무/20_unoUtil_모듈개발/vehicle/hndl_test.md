# 🧭 HandlingTest 조종안정성 커브피팅 연산 엔진 매뉴얼 (hndl_test.md)

## 📌 1. 개요 및 목적 (Overview)
`hndl_test` 모듈은 실차 정상원선회(Constant Radius Cornering) 및 조종안정성(Handling) 시험에서 취득된 **조향각(SWA) - 횡가속도(Ay)** 또는 **횡슬립각(Side-Slip) - 횡가속도(Ay)** 간의 비선형 거동을 정밀 피팅하여 **언더스티어 커브(Understeer Gradient Curve)** 및 타이어 한계 특성을 모델링하는 전문 연산 엔진입니다.

v2 아키텍처에서는 기존의 비표준 `plt.show()` 호출을 전면 배제하여 백그라운드 파이프라인 정지 현상을 원천 방어하고, **`calc_curvefit_rf` (B-Spline + Random Forest 하이브리드)**와 **`calc_curvefit_mf` (Pacejka Magic Formula 비선형 최적화)** 두 가지 표준 8대 동사 API로 정비되었습니다.

---

## 🛠️ 2. 핵심 함수 및 API 명세 (API Specifications)

| 함수명 (8대 표준 동사) | v1 오리지널 레거시 별칭 | 주요 인자 규격 (헝가리안 배제) | 반환값 | 알고리즘 특성 |
| :--- | :--- | :--- | :---: | :--- |
| **`calc_curvefit_rf`** | `SP_CurveFit_RF` | `data: pd.DataFrame, depth=4, window_size=100, num_points=None, plot=False, save=None, close=True` | `pd.DataFrame` | 초반 완만한 영역은 B-spline으로 곡률 보존, 한계 포화 영역(85% 이상)은 depth 제약된 Random Forest로 계단식 수평 직선 융합 |
| **`calc_curvefit_mf`** | `SP_CurveFit_MF` | `data: pd.DataFrame, min_range=5.0, acc_unit='g', num_points=1000, bayesian=False, plot=False` | `Tuple[X, Y, Estimator]` | Pacejka Magic Formula 비선형 타이어 거동 최적화. 그리드 서치 및 베이지안 탐색을 통한 파라메터 자동 추정 |

---

## 🎯 3. v1 레거시 하위 호환성 단일 기준 원칙 (Single Baseline Law)
* **v1 오리지널 레거시 호환 100% 보장**:
  - `unoUtil.vehicleTest._HndlTest_` 및 기존 코드에서 쓰이던 `SP_CurveFit_RF`, `SP_CurveFit_MF` 함수명을 모듈 최하단에 100% 호환 별칭으로 제공합니다.
  - 구버전 헝가리안 인자(`df_raw`, `df`, `peakratio`, `ws`, `intnum`, `deplot`, `minrange`, `acc_unit_change`, `inter`)는 `**kwargs` 흡수 블록을 통해 신규 표준 인자로 무중단 자동 변환됩니다.
* **과도기적 미완성 코드의 레거시 취급 배제**:
  - v2 개발 과정 중의 임시 파라미터나 불필요한 별칭은 남기지 않고 단일 표준 형태로 정합되었습니다.

---

## 💻 4. 실무 활용 3대 다변화 시나리오 (Multi-case Examples)

### 4.1. [시나리오 1] `calc_curvefit_rf` 하이브리드 언더스티어 커브 피팅
```python
import pandas as pd
from unoUtil.vehicle.hndl_test import calc_curvefit_rf

# 1. 조향각(SWA)과 횡가속도(Ay) 데이터프레임 준비
df_swa_ay = pd.DataFrame({
    "VehSWA": [0.0, 10.0, 25.0, 50.0, 80.0, 110.0, 130.0],
    "AccLateral": [0.0, 0.15, 0.38, 0.65, 0.82, 0.88, 0.89]
})

# 2. RF 최대 깊이를 4로 제한하여 한계 영역의 진동을 제거하고 매끄러운 커브 산출
res_df = calc_curvefit_rf(
    data=df_swa_ay,
    depth=4,
    window_size=10,
    plot=False
)
print(f"✅ 커브 피팅 완료! 피팅 포인트 수: {len(res_df)}")
```

### 4.2. [시나리오 2] `calc_curvefit_mf` Magic Formula 최적화 및 타겟 값 역추정
```python
from unoUtil.vehicle.hndl_test import calc_curvefit_mf

# 1. Magic Formula 비선형 피팅 수행
x_opt, y_opt, estimator = calc_curvefit_mf(
    data=df_swa_ay,
    acc_unit="g",
    num_points=500,
    plot=False
)

# 2. 임의의 조향각(SWA = 40 deg)에 대한 횡가속도 예측 (predict)
pred_ay = estimator.predict([40.0])
print(f"📊 SWA 40 deg 예측 횡가속도: {pred_ay[0]:.3f} g")

# 3. 임의의 횡가속도(Ay = 0.5 g)를 달성하기 위한 요구 조향각 역추정 (inverse)
req_swa = estimator.inverse([0.5])
print(f"🎯 Ay 0.5 g 달성 요구 조향각: {req_swa[0]:.1f} deg")
```

### 4.3. [시나리오 3] v1 레거시 별칭 호출 및 비차단(Non-blocking) 파일 저장
```python
from pathlib import Path
from unoUtil.vehicle.hndl_test import SP_CurveFit_RF

# v1 레거시 인자명(df_raw, ws, deplot)으로 호출하면서 비차단 차트 저장 수행
legacy_result = SP_CurveFit_RF(
    df_raw=df_swa_ay,
    ws=10,
    depth=3,
    plot=True,
    save=Path("./test_output/legacy_rf_curve.png"),
    close=True  # 메모리 즉시 해제
)
print("🎉 v1 레거시 호출 및 비차단 그래프 저장 성공!")
```

---
**Last Updated**: 2026-09-26  
**Module**: `unoUtil.vehicle.hndl_test`  
**Standard**: unoUtil Clean Architecture v2.0
