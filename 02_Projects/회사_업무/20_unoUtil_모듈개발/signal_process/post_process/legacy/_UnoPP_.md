# 🚀 _UnoPP_ Guide

---
### 🏛️ 시스템 흐름 (Architecture Layer)

효율적인 데이터 처리를 위해 본 모듈은 다음과 같은 **3단계 계층 구조**를 가집니다.

1.  **준비 계층 (Ready Layer)**: `SP_Normal`, `SP_Interpolation`
    * 원본 데이터의 스케일을 맞추거나, 분석하기 좋은 시간 간격으로 재정렬하여 기초 체력을 다집니다.
2.  **핵심 계층 (Core Layer)**: `SP_MovingAverage`, `SP_Merge`
    * 신호의 노이즈를 걷어내고 부드러운 곡선을 추출하는 핵심 엔진 역할을 수행합니다.
3.  **실행 계층 (Action Layer)**: `SP_RMOutlier`, `SP_FindContinue`
    * 최종적으로 이상치를 제거하고 의미 있는 연속 데이터 구간을 추출하여 실무 의사결정을 지원합니다.

---

### 🪄 공통 마법 키워드 (Global Options)

모든 함수는 기존 라이브러리와의 **100% 호환성**을 유지하며, `**kwargs`를 통해 **무한한 스타일 커스텀 자유도**를 제공합니다.

| 키워드 | 타입 | 기본값 | 설명 |
| :--- | :--- | :--- | :--- |
| `plot` | `bool` | `False` | **True** 설정 시 처리 전후를 즉시 시각화하여 검토 가능 |
| `ws` | `int` | `10` | 윈도우 사이즈(Window Size). 값이 클수록 그래프가 부드러워짐 |
| `method` | `str` | - | 알고리즘 선택 (함수별로 상이) |

> **💡 실무자 안심 포인트**
> * 데이터에 **결측치(NaN)**가 포함되어 있어도 내부적으로 선형 보간 및 전후 채우기(`ffill`, `bfill`)를 수행하여 에러 없이 작동합니다.
> * 시각화 시 별도의 폰트 설정이 없어도 기본 설정을 최적화하여 출력합니다.

---

### 📖 함수별 상세 가이드

### 1. SP_Normal (데이터 정규화)
💡 **기능**: 서로 다른 단위를 가진 데이터(예: 온도와 압력)를 동일한 범위로 맞춰 비교 분석을 가능하게 합니다.
* **모듈 전용 키워드**: `range` (MinMaxScaler 사용 시 변환할 최소/최대 범위 설정)
* **추천 스타일**: `cmap='viridis'`, `alpha=0.7`
* **데이터 해석 팁**: 데이터의 분포가 한쪽으로 쏠려 있다면 `robu`(RobustScaler)를 사용하여 이상치의 영향을 최소화하세요.

```python
# 실전 응용 예시
df_source_raw = pd.DataFrame({'Temp': [20, 25, 30], 'Press': [1000, 1010, 1020]})
df_result_scaled = SP_Normal(
    df_raw=df_source_raw, 
    str_scaler_type="range", 
    range=(0, 1), 
    plot=True
)
```

### 2. SP_MovingAverage (제로 페이즈 이동평균)
💡 **기능**: 데이터의 급격한 변동(노이즈)을 제거하면서도, 일반적인 이동평균과 달리 **위상 지연(시간 밀림) 없이** 정확한 시점을 유지해 줍니다.
* **모듈 전용 키워드**: `ws` (필터링 강도 조절)
* **추천 스타일**: `color='red'`, `lw=2` (결과선 강조)
* **데이터 해석 팁**: 원본 데이터(Blue)와 필터 데이터(Red)를 겹쳐 보았을 때, 피크 지점이 일치하는지 확인하세요.

```python
# 실전 응용 예시
df_source_signal = pd.DataFrame(np.random.randn(100, 1))
df_result_smooth = SP_MovingAverage(
    df_raw=df_source_signal, 
    ws=20, 
    plot=True, 
    index=True
)
```

### 3. SP_Merge (데이터 정렬 및 병합)
💡 **기능**: 뒤죽박죽 섞인 시계열 데이터를 정렬하고, 양 끝단의 왜곡을 방지하는 패딩 기술을 적용해 매끄러운 통합 곡선을 만듭니다.
* **모듈 전용 키워드**: `pad` (True 설정 시 경계 부분의 왜곡을 방지하는 Edge 패딩 적용)
* **추천 스타일**: `ms=1` (산점도 점 크기 최소화로 흐름 강조)
* **데이터 해석 팁**: 여러 센서에서 수집되어 겹치는 구간이 많은 데이터를 하나로 합칠 때 유용합니다.

```python
# 실전 응용 예시
df_result_merged = SP_Merge(
    df_raw=df_source_messy, 
    ws=15, 
    pad=True, 
    plot=True
)
```

### 4. SP_FindContinue (연속 구간 탐색)
💡 **기능**: "데이터가 언제부터 언제까지 안정적이었나?" 혹은 "어느 시점에 갑자기 변했나?"를 자동으로 찾아 리스트로 반환합니다.
* **모듈 전용 키워드**: `clv` (연속 임계치), `clen` (최소 유지 길이)
* **추천 스타일**: `csign='+'` (증가하는 구간만 탐색)
* **데이터 해석 팁**: 추출된 리스트의 개수가 예상보다 적다면 `clv` 값을 높여 보세요.

```python
# 실전 응용 예시
list_result_segments = SP_FindContinue(
    df_raw=df_source_sensor, 
    mode='value', 
    clv=0.5, 
    clen=50, 
    plot=True
)
```

### 5. SP_RMOutlier (다차원 이상치 제거)
💡 **기능**: 단순한 상하한 컷팅부터 AI 기반(Isolation Forest) 탐지까지 사용하여 데이터의 '불순물'을 완벽히 제거합니다.
* **모듈 전용 키워드**: `method` ('percentile', 'median', 'isol', 'eif')
* **추천 스타일**: `conta=0.05` (예상 오염도 5% 설정)
* **데이터 해석 팁**: 단순 변수는 `median`을, 여러 변수가 얽힌 복합적 이상치는 `eif` 방식을 추천합니다.

```python
# 실전 응용 예시
df_result_cleaned = SP_RMOutlier(
    df_raw=df_source_multidim, 
    list_col_name=['Signal', 'Data2'], 
    method='isol', 
    conta=0.01, 
    plot=True
)
```

### 6. SP_Interpolation (지능형 보간)
💡 **기능**: 듬성듬성한 데이터를 촘촘하게 메우거나, 서로 다른 샘플링 주기를 가진 데이터를 동기화합니다.
* **모듈 전용 키워드**: `newsamplerate` (목표 Hz), `multiple` (배수 보간)
* **추천 스타일**: `method='polynomial'`, `order=3` (부드러운 곡선 보간)
* **데이터 해석 팁**: 보간 후 원본 데이터의 물리적 특성이 왜곡되지 않았는지 시각화로 반드시 확인하십시오.

```python
# 실전 응용 예시
df_result_resampled = SP_Interpolation(
    df_raw=df_source_low_freq, 
    str_col_name="Time", 
    newsamplerate=100, 
    method='linear', 
    plot=True
)
```

---

### 🛡️ 실무 목적별 퀵 가이드

| 나의 분석 목적은? | 추천 함수 | 핵심 인자 |
| :--- | :--- | :--- |
| **데이터 범위 통일** | `SP_Normal` | `str_scaler_type="range"` |
| **노이즈 제거/매끄럽게** | `SP_MovingAverage` | `ws=15` |
| **튀는 값(이상치) 제거** | `SP_RMOutlier` | `method='isol'` |
| **비어있는 시간 채우기** | `SP_Interpolation` | `newtimeinterval=0.1` |
| **특정 동작 구간 추출** | `SP_FindContinue` | `mode='value', clen=10` |

**Documented by your Coding Partner & Technical Writer, uno.**