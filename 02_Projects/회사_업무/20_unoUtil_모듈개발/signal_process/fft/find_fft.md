# 🧭 find_fft 고속 푸리에 변환 및 변곡점 탐색 모듈 매뉴얼 (find_fft.md)

## 📌 1. 개요 및 목적 (Overview)
`find_fft` 모듈은 계측 신호의 시계열 노이즈 분포를 주파수 공간 상에서 해석하기 위한 **고속 푸리에 변환(Fast Fourier Transform, FFT) 연산 및 주파수 대역별 급증 지점(변곡점) 자동 탐색 엔진**을 구현합니다.

실차 거동 분석 중 서스펜션 진동, 차체 롤/요 동역학 및 센서 고주파 노이즈의 원인을 규명하기 위해선 시간 영역(Time Domain)을 주파수 영역(Frequency Domain)으로 변환하는 처리가 필수적입니다. 
본 모듈은 Numpy FFT C-엔진을 기동하여 고속 주파수 스펙트럼(Power Spectral Density)을 산출하고, 진동 급증 지점을 정밀 분석하여 백그라운드 무중단 시각화 및 자동 저장 파이프라인을 보장해 줍니다.

---

## 🛠️ 2. 핵심 API 명세 (API Specifications)

### 2.1. 글로벌 FFT 함수 명세

| 함수명 | 입력 파라미터 | 설명 |
| :--- | :---: | :--- |
| `find_fft(signal, fs, plot, save_path)` | `signal`, `fs`, `plot`, `save_path` | 1차원 시계열 센서 데이터를 입력받아 고속 FFT를 수행하고 주파수 진폭 급증 변곡점을 탐색하여 주파수 배열 및 진폭 스펙트럼 반환 |

---

## 📋 3. 입력 파라미터 상세 정의 (Arguments)

1. **`signal` (`np.ndarray` / `None` - 필수)**:
   - 분석할 1차원 계측 센서 시계열 신호 배열입니다. `None` 일 경우 자가 검증용 고주파 노이즈 합성 신호가 자동 생성됩니다.
2. **`fs` (`float` - 필수)**:
   - 신호의 계측 샘플링 주파수(Sampling Rate, Hz 단위) 정보입니다. (예: `100.0`, `200.0`)
3. **`save_path` (`Union[str, Path, None]` - 선택)**:
   - 다형성 `save` 파라미터 규격을 만족하며, FFT 진폭 스펙트럼 시각화 이미지의 저장 경로를 통제합니다.

---

## 💻 4. 실무 활용 예제 (Multi-case Examples)

### 4.1. [시나리오 1] 센서 진동 데이터의 고속 FFT 변환 및 주파수 해석
```python
import numpy as np
from unoUtil.signal_process.fft.find_fft import find_fft

# 1. 200Hz 주율의 가상 서스펜션 진동 노이즈 데이터 빌드
fs_hz = 200.0
t = np.arange(0, 10, 1.0/fs_hz)
raw_signal = np.sin(2 * np.pi * 15 * t) + 0.5 * np.random.normal(size=len(t))  # 15Hz 진동 성분 주입

# 2. FFT 연산 기동
freqs, amplitudes = find_fft(
    signal=raw_signal,
    fs=fs_hz,
    plot=False
)

# 3. 최대 우세 진동 주파수(Dominant Frequency) 탐색
max_idx = np.argmax(amplitudes[1:]) + 1  # DC 성분 제외
print(f"🎯 검출된 최대 지배 주파수: {freqs[max_idx]:.2f} Hz (실제 주입: 15.0Hz)")
```

### 4.2. [시나리오 2] Non-blocking FFT 스펙트럼 차트 생성 및 무중단 자동 저장
```python
# 다형성 save=True 및 close=True를 통한 백그라운드 스펙트럼 차트 내보내기 자동 수행
freqs, amplitudes = find_fft(
    signal=raw_signal,
    fs=fs_hz,
    plot=True,
    save_path=True,  # default 시각화 저장 디렉터리로 자동 이관 분기
)

print("💾 주파수 PSD 분석 차트 저장이 완벽하게 완료되었습니다.")
```

### 4.3. [시나리오 3] `None` 입력을 통한 자가 검증용 노이즈 합성 주파수 오토 빌드
```python
# signal에 None을 전달하면, FFT 모듈 내부의 검증 시나리오에 의해 고주파 50Hz 진동 합성 신호가 자동 생성 및 구동됨
test_freqs, test_amps = find_fft(
    signal=None,
    fs=100.0,
    plot=True,
    save_path="./test_output/auto_fft_verify.png"
)

print(f"🛡️ 자가 진단 완료! 생성된 테스트 주파수 해상도 수: {len(test_freqs)} points")
```
