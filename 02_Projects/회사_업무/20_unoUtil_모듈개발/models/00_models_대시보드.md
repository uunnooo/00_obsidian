---
id: "00_models_대시보드"
aliases:
  - models 대시보드
  - 공학 모델링 허브
tags:
  - unoUtil
  - models
  - MagicFormula
  - BicycleModel
  - 대시보드
  - MOC
  - SSOT
created: 2026-09-28
updated: 2026-09-29
version: v3.4
---

# 📐 unoUtil 공학 수학 모델 (models) 대시보드 (MOC)

> **상위 허브**: [[00_unoUtil_모듈개발_대시보드|unoUtil 모듈개발 마스터 허브]]  
> **패키지 경로**: `unoUtil.models`  
> **역할**: Pacejka Magic Formula, 2-DoF 차량 횡운동 자전거 모델(`BicycleModel`) 등 **순수 공학 지배 방정식(SSOT)** 및 머신러닝 신경망 모델을 정의하는 공학 수학 모델 도메인  
> **연관 도메인**: 데이터 기반 최적화 및 타이어 곡선 피팅은 [[00_curve_fit_대시보드|unoUtil.curve_fit]]에서 총괄합니다.

---

## 🏛️ 모델링 아키텍처 및 역할 분담

```mermaid
flowchart TD
    subgraph Models_Domain [unoUtil.models (순수 공학 지배 수식 SSOT)]
        subgraph Mathematical [1. mathematical/ 공학 지배 수식]
            MF["magic_formula.py<br/>(Pacejka MF 코어 수식 SSOT: Fx, Fy, Mu, Fz)"]
            BM["bicycle_model.py<br/>(2자유도 자전거 모델 Bicycle Model 지배 수식)"]
        end

        subgraph ML [2. neural_net/ 머신러닝 모델]
            NN["fit_nn.py<br/>(다층 신경망 MLP 회귀 모델)"]
        end
    end

    subgraph CurveFit_Domain [unoUtil.curve_fit (데이터 피팅 전담)]
        TC["tire_curve.py (TireCurve 총괄 피팅 클래스)"]
    end

    Mathematical -.수식 및 파라미터 규격 주입.-> TC
    RawData["계측 산점도 데이터"] --> TC
    TC --> Result["최적 파라미터 및 물리 특성치 도출"]
```

---

## 📜 버전 이력 및 주요 개발 현황 (Changelog)

| 버전 | 일자 | 작업자 | 주요 변경 및 승격 내역 | 상태 |
| :--- :| :---: | :---: | :--- | :---: |
| **v3.4** | 2026-09-29 | uno & Gemini | **models(수식)와 curve_fit(피팅) 도메인 역할 완벽 분리**<br>- 피팅 엔진 및 `TireCurve`를 `unoUtil.curve_fit` 도메인으로 이전 완료<br>- `models`는 순수 지배 방정식(Pacejka MF, 2-DoF Bicycle Model) 및 신경망 모델의 **단일 진실 공급원(SSOT)**으로 정체성 확립<br>- `unoUtil.models`에서 편의용 `TireCurve` re-export 호환성 100% 유지 | ✅ 배포 완료 |
| **v3.3** | 2026-09-28 | uno & Gemini | **Pacejka MF SSOT 및 Bicycle Model 표준화**<br>- 2-DoF 횡운동 모델의 자동차공학 국제 표준 용어인 **`bicycle_model`**로 정규화 완료<br>- Pacejka Magic Formula 단일 코어 연산 엔진(`calc_magic_formula`) 확립 | ✅ 완료 |

---

## 📂 서브모듈 구성 및 1:1 기술 매뉴얼

### 1. 공학 지배 수식 (`mathematical/`) - 단일 진실 공급원 (SSOT)
* [[magic_formula|📐 magic_formula: Pacejka Magic Formula 표준 지배 수식 및 메타데이터]]
* [[bicycle_model|🚲 bicycle_model: 2자유도 차량 횡운동 자전거 모델 (Bicycle Model) 및 요레이트]]

### 2. 기계학습 신경망 (`neural_net/`)
* [[fit_nn|🧠 fit_nn: Keras/Sklearn 기반 다층 신경망(MLP) 회귀 모델]]

---

## 💡 Quick Start

```python
import numpy as np
from unoUtil.models import BicycleModel, calc_magic_formula

# 1. 2-DoF Bicycle Model을 이용한 정상 상태 요레이트 연산
bm = BicycleModel(vel_unit=1.0, angr_unit=1.0)
steering = np.full(50, 2.0)  # 2도 조향
speed = np.linspace(20, 100, 50)  # 20~100 km/h
yaw_rate = bm.predict(steering, speed)

# 2. 순수 Pacejka Magic Formula 이론 곡선 연산
slip = np.linspace(0.0, 0.3, 100)
force = calc_magic_formula(slip, B=10.0, C=1.3, D=1.1, E=0.1)
```
