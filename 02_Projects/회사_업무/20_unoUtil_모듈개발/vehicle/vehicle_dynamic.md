# 🧭 VehicleDynamic 차량 운동역학 및 기하 변환 연산 엔진 매뉴얼 (vehicle_dynamic.md)

## 📌 1. 개요 및 목적 (Overview)
`vehicle_dynamic` 모듈은 실차 주행 시험 중 취득되는 물리 센서 신호(가속도, 속도, 각속도 등)를 기반으로 **차량 좌표계 변환(ISO $\rightarrow$ SAE), 3차원 회전 운동역학(Rotational Kinematics), 종방향 하중 이동량(Load Transfer) 및 중심점(COG)/차축(FA/RA) 횡슬립각(Side-Slip Angle)**을 정밀 연산하는 사내 표준 차량 동역학 분석 엔진입니다.

v2 아키텍처에서는 기존의 함수형 나열 방식에서 벗어나, **`VehicleDynamic` 단일 표준 클래스** 내부에 모든 동역학 알고리즘을 캡슐화하였습니다. 이를 통해 클래스 메서드(`VehicleDynamic.align_coordinate()`)를 통한 일회성 직관적 호출과, 인스턴스 셋업(`vd = VehicleDynamic(...)`)을 통한 파라미터 기반 반복 연산을 모두 지원합니다.

---

## 🛠️ 2. 핵심 클래스 및 API 명세 (API Specifications)

### 2.1. `VehicleDynamic` 클래스 인터페이스

| 메서드명 (8대 표준 동사) | v1 오리지널 레거시 별칭 | 주요 인자 규격 | 반환값 | 설명 |
| :--- | :--- | :--- | :---: | :--- |
| **`align_coordinate`** | `VD_AlignCoordinate` | `data: pd.DataFrame, plot=False, save=None, close=True` | `pd.DataFrame` | RT 센서 등의 ISO 좌표계를 사내 표준 SAE 직교 좌표계로 정렬하고 단위를 표준화 |
| **`rotate_kinematics`** | `VD_RotKinematics` | `p2p, o, a, vs, p=0.005, method='vel', ...` | `np.ndarray` / `DataFrame` | 센서 장착점과 기준점 사이의 레버암(Lever-arm) 벡터를 감안한 상대 속도/가속도 보정 |
| **`rotate_origin`** | `VD_RotOrigin` | `data, angle, method='xy', ...` | `np.ndarray` / `DataFrame` | 차량 롤/피치/요 오일러 회전각을 반영하여 3축 거동을 절대 수평 좌표계로 회전 |
| **`calc_p2p_inter_coordinate`** | `VD_CalP2PInterCoordinate` | `data: pd.DataFrame, p2p, plot=False, ...` | `pd.DataFrame` | 차체 계측점 데이터를 관성 기준점의 상대 속도 및 가속도로 좌표 변환 |
| **`calc_side_slip_angle`** | `VD_CalSideSlipAngle` | `data, vel_forward, vel_lateral, limit_vel_forward=1.0` | `pd.DataFrame` | 종/횡속도를 기반으로 COG 중심의 차량 횡슬립각(deg) 산출 |
| **`calc_slip_angle_fr`** | `VD_CalSlipAngleFR` | `data, a=1.5, b=1.5, angr_z='AngrZ', ...` | `pd.DataFrame` | 2-DOF 자전거 모델 기하학을 바탕으로 전륜 축(FA) 및 후륜 축(RA)의 슬립각 계산 |
| **`calc_load_transfer_longitudinal`** | `VD_CalLoadTransferLongi`| `mass, height, wheel_base, accel` | `np.ndarray` | 실시간 종가속도 변동에 따른 전/후륜 축 하중 이동량 $\Delta F_z(t)$ (N) 연산 |
| **`make_standard_df`** | `makeStandardDF` | `data, wheel_base=2.86, cg_height=0.4, weight=None, sensor_pos=None, plot_summary=False` | `pd.DataFrame` | **[통합 파이프라인]** 좌표계 정렬, 상대 좌표 변환, 슬립각 산출을 원스톱 일괄 수행 |

---

## 🎯 3. v1 레거시 하위 호환성 단일 기준 원칙 (Single Baseline Law)
* **v1 오리지널 레거시 100% 보장**:
  - `unoUtil.vehicleTest.VehicleDynamic` 및 `unoUtil.vehicle.vehicle_dynamic`에서 과거 사용하던 `VD_AlignCoordinate`, `VD_RotKinematics`, `makeStandardDF` 등 대문자 함수 호출을 모듈 레벨에서 100% 유지합니다.
  - 구버전 헝가리안 인자(`rawDF`, `wheelBase`, `cgH`, `sensor`, `plot_summarize`, `flagPlot`)는 `**kwargs` 흡수 패턴을 통해 무중단으로 신규 표준 인자에 자동 매핑됩니다.
* **과도기적 미완성 코드의 레거시 취급 배제**:
  - v2 개발 도중 임시로 제안되었던 불필요한 별칭(`calc_vd_...` 등)이나 임시 브릿지 파일은 남기지 않고 단일 표준 `VehicleDynamic` 클래스로 직교화되었습니다.

---

## 💻 4. 실무 활용 3대 다변화 시나리오 (Multi-case Examples)

### 4.1. [시나리오 1] `VehicleDynamic.align_coordinate()` 좌표계 자동 정렬 및 단위 변환
```python
import pandas as pd
from unoUtil.vehicle.vehicle_dynamic import VehicleDynamic

# 1. 원시 주행 데이터 로드 (ISO 기준)
df_raw = pd.DataFrame({
    "VelForward": [20.0, 22.0, 25.0],
    "VelLateral": [0.1, 0.2, -0.1],
    "AccLateral": [0.5, 0.8, -0.4],
    "AccDown": [9.81, 9.80, 9.81],
    "AngrZ": [2.1, 3.5, -1.8],
    "VehSWA": [15.0, 25.0, -12.0]
})

# 2. 클래스 메서드를 통한 SAE 좌표계 정렬 및 부호/단위 통일
df_aligned = VehicleDynamic.align_coordinate(df_raw, plot=False)
print("✅ 좌표계 정렬 완료! 정렬된 컬럼:", df_aligned.columns.tolist())
```

### 4.2. [시나리오 2] 횡슬립각 산출 및 종방향 하중 이동량 $\Delta F_z(t)$ 연산
```python
import numpy as np
from unoUtil.vehicle.vehicle_dynamic import VehicleDynamic

# 1. COG 횡슬립각 산출
df_slip = VehicleDynamic.calc_side_slip_angle(
    df_aligned,
    vel_forward="VelForward",
    vel_lateral="VelLateral"
)
print(f"📊 최대 횡슬립각: {df_slip.iloc[:, 0].abs().max():.2f} deg")

# 2. 실시간 급제동 종가속도(-9.8 m/s^2)에 따른 전/후륜 축 하중 이동량 계산 (Passat B9 Variant 기준)
delta_fz = VehicleDynamic.calc_load_transfer_longitudinal(
    mass=1725.0,      # 차량 중량 (kg)
    height=0.55,      # 무게중심 높이 (m)
    wheel_base=2.837, # 휠베이스 (m)
    accel=np.array([-1.0, -5.0, -9.8]) # 제동 감속도 (m/s^2)
)
print(f"🚨 최대 제동 시 후륜 ➔ 전륜 축 하중 이동량: {np.abs(delta_fz).max():.1f} N")
```

### 4.3. [시나리오 3] `make_standard_df` 통합 전처리 및 비차단(Non-blocking) 요약 저장
```python
from pathlib import Path
from unoUtil.vehicle.vehicle_dynamic import VehicleDynamic

# 1. 4륜 윤하중 및 센서 오프셋 제원을 반영한 원스톱 통합 전처리 파이프라인 가동
df_standard = VehicleDynamic.make_standard_df(
    data=df_aligned,
    wheel_base=2.84,
    cg_height=0.52,
    weight=[498, 481, 306, 305],  # FL, FR, RL, RR 윤하중 (kg)
    sensor_pos=[2.64, 0.0, 0.73], # 센서 장착 상대 위치 (m)
    plot_summary=True,
    save=Path("./test_output/standard_vd_summary.png"), # Non-blocking 자동 저장
    close=True  # 메모리 즉시 회수
)

print(f"🎉 통합 표준 DF 빌드 완료! 전체 피처 수: {df_standard.shape[1]}")
```

---
**Last Updated**: 2026-09-26  
**Module**: `unoUtil.vehicle.vehicle_dynamic`  
**Standard**: unoUtil Clean Architecture v2.0
