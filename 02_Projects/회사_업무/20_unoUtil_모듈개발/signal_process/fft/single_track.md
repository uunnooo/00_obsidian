# 🧭 SingleTrack Bicycle Model 차량 횡동역학 시뮬레이션 매뉴얼 (single_track.md)

## 📌 1. 개요 및 목적 (Overview)
`single_track` 모듈은 실차 횡운동 성능 평가 전, 선행 동역학 거동 예측 및 선회 안정성 분석을 위해 **2자유도 자전거 모델(Bicycle Model / Single-Track Model) 기반 차량 횡동역학 물리 시뮬레이션 엔진(`SingleTrack`)**을 제공합니다.

실차 조종안정성(Handling) 주행 시 발생하는 차량의 횡슬립각(Side-slip angle) 및 요레이트(Yaw rate) 거동은 타이어 비선형 슬립 강성과 조향 입력에 밀접하게 맞물려 움직입니다. 
본 모듈은 차량 질량, 관성 모멘트, 전/후 타이어 횡슬립 강성을 입력받아 상태공간(State-Space) 선형 미분방정식을 4차 룽게-쿠타(Runge-Kutta 4th Order) 수치해석 엔진으로 고속 시뮬레이션하여 차량의 정상 상태 선회 거동 및 동적 횡안정성을 무결하게 물리 예측해 줍니다.

---

## 🛠️ 2. 핵심 API 명세 (API Specifications)

### 2.1. `SingleTrack` 클래스 및 글로벌 시뮬레이션 인터페이스

| 메서드 / 함수명 | 타입 | 설명 |
| :--- | :---: | :--- |
| `simulate_single_track(...)` | 글로벌 함수 | 차량 질량, 관성모멘트, 차속, 조향각 등을 일괄 입력받아 2자유도 거동 시뮬레이션 시계열 데이터프레임 및 물리 그래프 반환 |
| `SingleTrack` | 클래스 | 자전거 모델 물리 시뮬레이터 객체 |
| `SingleTrack.simulate()` | 메서드 | 설정된 차량 스펙에 기반하여 룽게-쿠타 상태방정식 적분을 가동하고 요레이트, 횡가속도, 횡슬립각 데이터프레임 도출 |

---

## 📋 3. 입력 파라미터 상세 정의 (Arguments)

1. **`m` (`float` - 필수)**: 차량의 총 질량 (Mass, kg 단위).
2. **`iz` (`float` - 필수)**: 차량의 수직축 요 관성 모멘트 (Yaw Inertia, kg*m^2 단위).
3. **`a` / `b` (`float` - 필수)**: 무게중심(CoG)에서 각각 전륜 축(a) 및 후륜 축(b)까지의 수평 거리 (m 단위).
4. **`cf` / `cr` (`float` - 필수)**: 전륜 타이어(cf) 및 후륜 타이어(cr)의 코너링 강성 (Cornering Stiffness, N/rad 단위).
5. **`vx` (`float` - 필수)**: 주행 차량 속도 (Longitudinal Velocity, m/s 또는 km/h 단위).
6. **`steering_angle_deg` (`float` - 필수)**: 전륜 조향 타이어 실각도 (Steering angle, deg 단위).

---

## 💻 4. 실무 활용 예제 (Multi-case Examples)

### 4.1. [시나리오 1] 표준 소형 차종 횡동역학 시뮬레이션 및 요레이트 예측
```python
from unoUtil.signal_process.fft.single_track import simulate_single_track

# 1. 일반 준중형 차량 물리 동역학 파라미터 정의
m_kg = 1500.0      # 질량
iz_kgm2 = 2500.0   # 요 관성모멘트
front_a = 1.2      # 무게중심-전륜 거리 (m)
rear_b = 1.4       # 무게중심-후륜 거리 (m)
cf_stiff = 80000.0 # 전륜 코너링 강성 (N/rad)
cr_stiff = 75000.0 # 후륜 코너링 강성 (N/rad)

# 2. 80km/h 주행 속도(22.2 m/s)에서 전륜 2도 급조향 시 시뮬레이션 기동
df_dynamic = simulate_single_track(
    m=m_kg, iz=iz_kgm2, a=front_a, b=rear_b,
    cf=cf_stiff, cr=cr_stiff,
    vx=22.2,
    steering_angle_deg=2.0,
    total_time=5.0,  # 5초 시뮬레이션
    n_points=500,
    plot=False
)

print(f"📊 횡동역학 시뮬레이션 완료! 결과 행수: {len(df_dynamic)}")
print(f"📈 최대 수렴 Yaw Rate: {df_dynamic['YawRate'].max():.3f} rad/s")
```

### 4.2. [시나리오 2] 선회 궤적 및 횡가속도 프로파일 3D 차트 저장 (Non-blocking)
```python
# 조향 선회 궤적 시뮬레이션 시각화 자동 저장 기동
simulate_single_track(
    m=m_kg, iz=iz_kgm2, a=front_a, b=rear_b,
    cf=cf_stiff, cr=cr_stiff,
    vx=22.2, steering_angle_deg=2.0,
    plot=True,
    save_path=True  # default 시각화 폴더로 안전 비블로킹 저장 처리
)

print("💾 2자유도 자전거 모델 선회 거동 시각화 저장이 완료되었습니다.")
```

### 4.3. [시나리오 3] 고속/저속 및 오버스티어/언더스티어 물리 인자 비교 시뮬레이션
```python
# 후륜 코너링 강성이 낮아 언더스티어가 나기 쉬운 타이어 조합 가상 시뮬레이션
under_cr_stiff = 45000.0  # 후륜 강성 의도적 축소

df_under = simulate_single_track(
    m=m_kg, iz=iz_kgm2, a=front_a, b=rear_b,
    cf=cf_stiff, cr=under_cr_stiff,
    vx=30.0,  # 108km/h 고속 영역 선회
    steering_angle_deg=1.5,
    plot=False
)

print(f"🛡️ 고속 불안정 한계 분석! 정상 상태 횡슬립각: {df_under['Sideslip'].iloc[-1]:.4f} rad")
```
