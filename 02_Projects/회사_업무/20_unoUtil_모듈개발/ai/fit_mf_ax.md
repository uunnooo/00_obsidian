---
id: "fit_mf_ax_20260920"
title: "fit_mf_ax (타이어 Magic Formula 수식 최적화 피팅) 상세 매뉴얼"
type: resource
category_main: 회사_업무
category_sub: 개발매뉴얼
date: 2026-09-20
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - 매뉴얼
  - AI
  - 기계학습
  - 최적화
  - MagicFormula
project_link: "[[unoUtil]]"
---

# 🛞 fit_mf_ax (타이어 Magic Formula 수식 최적화 피팅) 상세 매뉴얼

> [!ABSTRACT] 📌 개요
> 타이어의 횡력/종력 비선형 마찰 한계 특성을 산출하는 세계 표준 Pacejka Magic Formula (MF) 모델을 설계하고, 실시간 계측 데이터로부터 `scipy.optimize.minimize` (Nelder-Mead 기법)를 사용해 최적 물리 계수 조합을 자동 역추정하는 최적화 엔진입니다.
> 
> * **상위 대시보드**: [[00_unoUtil_모듈개발_대시보드]]

---

## 1. ⚙️ Pacejka 수식의 공학적 원리

### 1.1. Magic Formula (MF) 수식 수렴도
$$F_x = D_x \cdot \sin\left(C_x \cdot \arctan\left(B_x \cdot x - E_x \cdot \left(B_x \cdot x - \arctan(B_x \cdot x)\right)\right)\right)$$

- **$D_x$ (Peak Factor)**: 최대 종방향/횡방향 마찰 한계치 결정 (타이어가 노면에 발휘할 수 있는 최대 G값).
- **$C_x$ (Shape Factor)**: 횡방향 기울기와 피크 곡선의 포화 형태 비선형 제어.
- **$B_x$ (Stiffness Factor)**: 원점 부근 슬립율 극초반의 마찰력 강성 기울기(Slip Stiffness).
- **$E_x$ (Curvature Factor)**: 피크 한계 도달 이후 슬립 마찰력의 감소 곡선 하강 기울기 및 곡률 거동 제어.

---

## 2. ⚙️ 주요 API 규격

### 2.1. `calculate_Fx(Bx, Ex, Dx, Cx, x)`
* **기능**: 입력 슬립율(또는 슬립각) `x`에 대해 Pacejka Magic Formula 수식을 적용하여 힘(Fx)을 계산해 반환합니다.
* **하위 호환 별칭**: `calculate_fx`

### 2.2. `optimize_and_plot(x, actual_Fx, initial_params, ...)`
* **기능**: 실제 계측된 힘 `actual_Fx`와 입력 슬립 `x` 간의 잔차 제곱합을 비용 함수(Cost function)로 삼아 최적의 (Bx, Ex, Dx, Cx) 물리 상수를 수렴 완료합니다.
* **매개변수**:
  - `x (np.ndarray)`: 시험장 계측 슬립 비율 배열.
  - `actual_Fx (np.ndarray)`: 계측된 타이어 실제 힘 배열.
  - `initial_params (Tuple)`: 최적화 초깃값 튜플 (Bx, Ex, Dx, Cx).
  - `plot (bool)`: 1000포인트 해상도 보간 곡선 오버레이 시각화 여부.
  - `save (str | Path | bool, optional)`: 이미지 저장 경로 설정 및 다형성 활성화 여부.
  - `close (bool)`: 플롯 닫기 (시각화 무중단 원칙 준수 기본값 `True`).
* **반환값**: 수렴 완료된 최적 파라미터 배열(`optimized_params`) 및 예측 힘 곡선 배열(`predicted_Fx`).
* **하위 호환 별칭**: `fit_mf_ax`

---

## 💻 3. 호출 예제 (Usage Example)

```python
import numpy as np
from unoUtil.ai.fit_mf_ax import optimize_and_plot

# 1. 가상 계측 데이터셋 준비
slip_ratio = np.array([-0.15, -0.1, -0.05, 0.0, 0.05, 0.1, 0.15])
measured_fx = np.array([-0.98, -0.85, -0.55, 0.0, 0.58, 0.86, 0.99])

# 2. Nelder-Mead 최적화 계수 피팅 실행
initial_guess = [10.0, 0.1, 1.0, 1.5]
opt_params, interpolated_curve = optimize_and_plot(
    x=slip_ratio,
    actual_Fx=measured_fx,
    initial_params=initial_guess,
    plot=True,
    save=True,  # 디폴트 폴더에 자동 차트 이미지 기록
    close=True
)

print(f"추정 완료된 피크 마찰 계수 Dx: {opt_params[2]:.4f}")
```

---

## 4. 📝 이중 동기화 프로토콜 준수사항
- 이 매뉴얼 파일(`fit_mf_ax.md`)은 동일 로컬 디렉터리(`unoUtil/ai/`) 내에 1:1 대응하여 보관되며, 최종 작업 완료 선언 시 옵시디언 볼트로 일괄 배치 동기화 처리됩니다.
