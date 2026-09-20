# 🧭 text_offset 포인트(pt) 단위 미세 텍스트 오프셋 배치 매뉴얼 (text_offset.md)

## 📌 1. 개요 및 목적 (Overview)
`text_offset` 모듈은 Matplotlib 챠트 드로잉 시 특정 중요 데이터 지점에 텍스트 라벨이나 가리키는 지시 화살표(Annotation)를 추가할 때, **데이터 수치나 그래프 픽셀선과 텍스트가 겹치지 않도록 포인트(pt) 단위의 정교한 미세 가로/세로 오프셋 보정 배치**를 수행하는 시각화 미세 텍스트 보정 유틸리티 함수(`text_offset`, `annotate_offset`)를 제공합니다.

가감속 제동 최대 감속도 점이나 트랙 궤적의 랜드마크 점에 수치 텍스트를 단순 데이터 좌표로 배치하면, 데이터 포인트 마커 기호와 문자가 완전히 겹쳐서 그래프의 가독성이 심각하게 파괴됩니다. 
본 모듈은 디스플레이 해상도(DPI)에 영향받지 않는 독립적인 포인트 단위 물리 레이아웃 연산을 수행하여, 마커 바로 위/옆에 영롱하고 정갈한 텍스트 배치를 안전하게 구현해 줍니다.

---

## 🛠️ 2. 핵심 API 명세 (API Specifications)

### 2.1. 글로벌 텍스트 오프셋 함수 명세

| 함수명 | 입력 파라미터 | 설명 |
| :--- | :---: | :--- |
| `text_offset(ax, x, y, s, offset_x, offset_y)` | `ax`, `x`, `y`, `s`, `offset_x`, `offset_y` | 데이터 좌표 `(x, y)` 로부터 지정된 포인트(pt) 시차 `(offset_x, offset_y)` 만큼 떨어트려 가독성 높게 라벨 텍스트 배치 |
| `annotate_offset(ax, x, y, s, offset_x, offset_y)` | `ax`, `x`, `y`, `s`, `offset_x`, `offset_y` | 데이터 좌표 `(x, y)` 지점을 가리키는 접선 화살표와 텍스트를 포인트 오프셋 기반으로 안전 렌더링 배치 |

---

## 📋 3. 입력 파라미터 상세 정의 (Arguments)

1. **`ax` (`plt.Axes` - 필수)**:
   - 텍스트 오프셋을 드로잉할 Matplotlib 축 객체입니다.
2. **`x` / `y` (`float` - 필수)**:
   - 텍스트가 가리킬 데이터 자체의 원시 가로, 세로 좌표값입니다.
3. **`s` (`str` - 필수)**:
   - 축 위에 정합 표기할 실제 수치 문자열입니다 (예: `'-1.25 g'`).
4. **`offset_x` / `offset_y` (`float` - 필수)**:
   - 데이터 포인트로부터 글꼴 텍스트를 밀어낼 포인트(pt) 기준 오프셋 수치입니다. (예: `offset_y=10` 은 마커 위로 10pt 공간 확보)

---

## 💻 4. 실무 활용 예제 (Multi-case Examples)

### 4.1. [시나리오 1] 최대 감속도 극점 위치 위로 10포인트 텍스트 오프셋 배치
```python
import matplotlib.pyplot as plt
from unoUtil.graphics.plotters.text_offset import text_offset

fig, ax = plt.subplots(figsize=(10, 6))

# 제동 감속도 곡선 가상 타점
brake_time = 4.5
max_decel_g = -1.15
ax.plot(brake_time, max_decel_g, 'bo', label='Peak Decel')

# 마커 기호와 글자가 겹치지 않도록 위로 12포인트(offset_y=12) 텍스트 이동 정밀 배치!
text_offset(
    ax=ax,
    x=brake_time,
    y=max_decel_g,
    s=f"Peak: {max_decel_g} g",
    offset_x=0,
    offset_y=12  # 위로 12pt 평행이동
)

ax.legend()
plt.close(fig)  # 백그라운드 무중단 메모리 해제
```

### 4.2. [시나리오 2] 데이터 점을 가리키는 Annotation 화살표와 설명 라벨 포인트 오프셋 배치
```python
from unoUtil.graphics.plotters.text_offset import annotate_offset

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [10, 20, 30], 'g-')

# 변곡점 (2, 20)을 안전하게 가리키는 지시 화살표 및 설명 라벨 배치
annotate_offset(
    ax=ax,
    x=2.0,
    y=20.0,
    s="Inflexion Point",
    offset_x=20,  # 우측으로 20pt 밀어냄
    offset_y=20   # 위로 20pt 밀어냄
)

plt.close(fig)
```

### 4.3. [시나리오 3] 대량 타점 오프셋 자동 렌더링 및 비블로킹 저장 검증
```python
fig, ax = plt.subplots()
times = [1.2, 3.4, 7.8]
speeds = [90.5, 45.2, 0.0]

ax.plot(times, speeds, 'kx')

# 수십 개 극점에 루프 돌며 안전 시차 텍스트 일괄 드로잉
for t, sp in zip(times, speeds):
    text_offset(ax, t, sp, f"{sp}km/h", offset_x=5, offset_y=5)

# 무중단 파일 저장 및 RAM 완전 소거
fig.savefig("./test_output/peak_annotated_profile.png", dpi=200, bbox_inches='tight')
plt.close(fig)

print("💾 텍스트 오프셋이 적용된 주행 프로파일 이미지가 안전하게 저장되었습니다.")
```
