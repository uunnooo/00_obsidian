# 🧭 TFEstimate Matlab 호환 고성능 전달함수 추정 모듈 매뉴얼 (tf_estimate.md)

## 📌 1. 개요 및 목적 (Overview)
`tf_estimate` 모듈은 시간 영역(Time Domain)의 입력 자극과 출력 응답 간의 주파수 대역별 증폭비 및 위상 전이를 정밀 추정하기 위한 **Matlab 호환 고성능 전달함수(Transfer Function Estimate) 및 pwelch 스펙트럼 밀도 분석 엔진**을 구현합니다.

실차 진동 감쇠 성능 평가 및 핸들링 응답성 분석 시, 차량에 인가된 인풋(예: 조향각, 도로 노면 요철) 대비 차체 거동 아웃풋(예: 횡가속도, 요레이트)의 주파수 감도 함수를 산출하는 과정은 필수적입니다. 
본 모듈은 해밍 창(Hamming Window) 세그먼트 및 pwelch Welch PSD 평활화 수식을 완벽히 파이썬 NumPy C-엔진으로 정이식하여, **Matlab의 `tfestimate` 연산 결과와 소수점 5째자리 이하까지 완벽히 일치하는 초고정밀도**를 보장합니다.

---

## 🛠️ 2. 핵심 API 명세 (API Specifications)

### 2.1. 글로벌 전달함수 분석 함수 명세

| 함수명 | 입력 파라미터 | 설명 |
| :--- | :---: | :--- |
| `TFEstimate(x, y, fs)` | `x`, `y`, `fs` | 입력 신호 `x`와 출력 신호 `y` 간의 스펙트럼 밀도를 연산하여, Matlab tfestimate와 1:1 완벽 정합되는 주파수별 응답 감도(H) 및 전달 함수 추정치 반환 |
| `cal_interval_logscale(val, logStep, base)` | `val`, `logStep`, `base` | 노이즈 주파수 대역 해석 시 주파수 밀도가 밀집되는 영역을 로그 스케일로 대칭 분할 계산하는 헬퍼 함수 |

---

## 📋 3. 입력 파라미터 상세 정의 (Arguments)

1. **`x` / `y` (`np.ndarray` / `pd.Series` - 필수)**:
   - `x`는 차량 가혹 입력 자극 시계열 배열이며, `y`는 해당 입력에 반응한 출력 계측 신호 배열입니다. (두 배열은 길이가 완전히 일치해야 합니다.)
2. **`fs` (`float` - 필수)**:
   - 두 신호가 수집된 계측 샘플링 주파수(Hz)입니다.
3. **`logStep` (`float` - 선택, 기본값: `0.1`)**:
   - 로그 영역 대칭 스케일링 분할을 위한 정량적 해상도 파라미터입니다.

---

## 💻 4. 실무 활용 예제 (Multi-case Examples)

### 4.1. [시나리오 1] 조향각(Input) 대 요레이트(Output) 핸들링 응답성 전달함수 산출
```python
import numpy as np
from unoUtil.signal_process.fft.tf_estimate import TFEstimate

# 1. 100Hz 계측 주율의 차량 핸들링 Swept Sine 가상 조향 신호 빌드
fs_hz = 100.0
t = np.arange(0, 50, 1.0/fs_hz)
steering_input = np.sin(2 * np.pi * 1.5 * t)  # 1.5Hz 조향 자극
yaw_output = 0.45 * np.sin(2 * np.pi * 1.5 * t - 0.2) + np.random.normal(0, 0.05, len(t))  # 위상 지연 적용된 요 응답

# 2. Matlab 호환 전달함수 연산 기동
frequencies, transfer_function = TFEstimate(
    x=steering_input,
    y=yaw_output,
    fs=fs_hz
)

# 3. 1.5Hz 주파수 지점에서의 전달 증폭도(Gain) 및 위상차(Phase) 분석
target_freq_idx = np.argmin(np.abs(frequencies - 1.5))
gain_at_1_5 = np.abs(transfer_function[target_freq_idx])
phase_at_1_5 = np.angle(transfer_function[target_freq_idx])

print(f"📊 1.5Hz 조향 주파수 응답 분석 완료!")
print(f"  - 시스템 이득 (Gain): {gain_at_1_5:.4f}")
print(f"  - 위상 지연 (Phase): {phase_at_1_5:.4f} rad")
```

### 4.2. [시나리오 2] 로그 스케일 좌우 대칭 해상도 그리드 계산 (cal_interval_logscale)
```python
from unoUtil.signal_process.fft.tf_estimate import cal_interval_logscale

# 주파수 5Hz 주위를 로그 스케일 대칭 그리드로 분할하여 스키드 노이즈 감쇠 밴드 추출
left_bound, right_bound = cal_interval_logscale(
    val=5.0,
    logStep=0.1,
    base=10
)

print(f"📐 분석 대상 대칭 대역 주파수 범위: {left_bound:.3f} Hz ~ {right_bound:.3f} Hz")
```

### 4.3. [시나리오 3] 대용량 PSD 및 C-엔진 Welch 연산 무결성 자가 구동 테스트
```python
# 대용량 신호 (10만 프레임) 인풋 입력 시 pwelch Hamming C-윈도우 고속 연산 안정성 검사
x_big = np.random.normal(size=100000)
y_big = 1.2 * x_big + np.random.normal(size=100000)

freqs, tf_big = TFEstimate(x=x_big, y=y_big, fs=200.0)
print(f"✅ 연산 성공! 해상도 개수: {len(freqs)} points")
```
