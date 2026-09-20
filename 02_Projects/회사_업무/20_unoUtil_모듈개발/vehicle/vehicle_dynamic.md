# 🧭 vehicle_dynamic 차량 운동역학 및 하중 이동 연산 모듈 매뉴얼 (vehicle_dynamic.md)

## 📌 1. 개요 및 목적 (Overview)
`vehicle_dynamic` 모듈은 실차 주행 시험 중 계측되는 물리 센서 값을 기반으로 **차량 좌표계 변환(ISO-SAE), 3차원 회전 운동역학(Rotational Kinematics), 종방향 하중 이동량(Load Transfer) 및 횡슬립각(Side-Slip Angle) 연산**을 수행하는 사내 통합 횡/종 차량 운동 동역학 연산 패키지입니다.

주행 시험기에서 출력되는 가속도 및 속도 센서 값은 계측 장비의 장착 위치(측정점)와 차량의 실제 물리적 거동 중심인 무게중심(Center of Gravity, COG - 기준점) 사이에 공간적 오차가 존재합니다. 
본 모듈은 측정점-기준점 사이의 상대 가속도/속도 벡터 기하 변환 수식을 가동하여, 오차를 완벽히 소거한 순수한 COG 물리 계측치(`makeStandardDF`)를 도출해 내며, 실시간 종가속도 변동에 따른 4륜 수직하중 이동 변동량을 기하학적으로 연산해 줍니다.

---

## 🛠️ 2. 핵심 API 명세 (API Specifications)

### 2.1. 글로벌 차량 동역학 함수 명세

| 함수명 | 입력 파라미터 | 설명 |
| :--- | :---: | :--- |
| `VD_AlignCoordinate(rawDF)` | `rawDF` | Oxford RT 등에서 나오는 ISO 표준 좌표계 데이터를 사내 표준인 SAE 직교 좌표계로 정렬 변환 |
| `VD_RotKinematics()` | `**kwargs` | 약속된 레버 암(Lever-arm) 벡터 거리를 감안하여 측정점의 속도/가속도를 COG 기준점 물리 변수로 기하 변환 |
| `VD_RotOrigin(rawDF, angle)` | `rawDF`, `angle`, `**kwargs` | 차량의 롤(Roll), 피치(Pitch), 요(Yaw) 회전 각도를 반영하여 3축 가속도를 절대 수평 좌표계로 회전 변환 |
| `VD_CalSideSlipAngle(rawDF)` | `rawDF`, `**kwargs` | 전/후륜 차속 성분을 기반으로 주행 중 차량의 횡슬립각(Side-slip Angle) 도출 |
| `VD_CalLoadTransferLongi(m, h, L, a)` | `m`, `h`, `L`, `a` | 차량 질량(m), 무게중심 높이(h), 휠베이스(L) 및 실시간 종가속도(a)를 토대로 가감속 시 전/후륜 축 하중 이동량 $\Delta F_z(t)$ 계산 |
| `makeStandardDF(rawDF)` | `rawDF`, `**kwargs` | **[통합 전처리 엔진]** ISO 변환, COG 상대 변환, 회전 보정을 연속 수행하여 표준 데이터프레임 도출 |

---

## 📋 3. 입력 파라미터 상세 정의 (Arguments)

1. **`rawDF` (`pd.DataFrame` - 필수)**:
   - 전처리할 원시 실차 주행 센서 시계열 데이터프레임입니다.
2. **`L` / `h` (`float` - `VD_CalLoadTransferLongi` 필수)**:
   - 축간거리(휠베이스, L) 및 지면으로부터의 무게중심 높이(h) 기하 스펙 상수입니다.

---

## 💻 4. 실무 활용 예제 (Multi-case Examples)

### 4.1. [시나리오 1] 가감속 시 전/후륜 종방향 하중 이동량 실시간 연산
```python
import pandas as pd
from unoUtil.vehicle.vehicle_dynamic import VD_CalLoadTransferLongi

# 1. 수집된 100Hz 종가속도 데이터프레임 빌드 (급제동 가혹 가속도 입력)
df_acc = pd.DataFrame({"Ax": [-0.1, -0.5, -0.9, -1.0, -1.0]})

# 2. 시험 차량 제원 정의 (예: Passat B9 Variant)
mass_kg = 1725.0
wheelbase_m = 2.84
cog_height_m = 0.52

# 3. 실시간 축하중 이동 변동량(N) 계산 기동
df_load = VD_CalLoadTransferLongi(
    m=mass_kg,
    h=cog_height_m,
    L=wheelbase_m,
    a=df_acc['Ax']
)

print(f"📊 최대 제동 시 후륜 ➔ 전륜 하중 이동량: {df_load.max():.2f} N")
```

### 4.2. [시나리오 2] 원시 데이터프레임의 COG 기준 표준 좌표계 및 물리 변환 일괄 전처리
```python
from unoUtil.vehicle.vehicle_dynamic import makeStandardDF

# 센서 픽셀 측정 좌표를 COG 절대 3축 물리값으로 연쇄 기하 전처리 수행
df_standard = makeStandardDF(
    rawDF=df_raw,
    lever_arm_x=0.15,  # 센서와 COG 사이의 x축 이격 거리 (m)
    lever_arm_y=0.0,
    lever_arm_z=-0.05
)

print(f"✅ 전처리 정합 완료! COG 속도 변환 확인: {list(df_standard.columns[:4])}")
```

### 4.3. [시나리오 3] 횡슬립각(Side-Slip Angle) 수학적 도출 및 무중단 저장
```python
from unoUtil.vehicle.vehicle_dynamic import VD_CalSideSlipAngle

# 선회 주행 횡슬립 분석 실행
df_slip = VD_CalSideSlipAngle(rawDF=df_raw)

# 횡안정성 분석 시각화 무중단 저장
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot(df_slip.index, df_slip['SideSlip_deg'])
fig.savefig("./test_output/sideslip_stability.png", dpi=200)
plt.close(fig)  # 백그라운드 무중단 해제

print("💾 실차 선회 슬립 각 거동 차트 저장이 성공적으로 완료되었습니다.")
```
