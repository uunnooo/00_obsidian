# 🧭 make_cmp_plotly Matplotlib-to-Plotly 컬러맵 자동 번역 헬퍼 매뉴얼 (plotly_tools.md)

## 📌 1. 개요 및 목적 (Overview)
`plotly_tools` 모듈은 로컬 시각화에 널리 쓰이는 Matplotlib의 고정밀 그라데이션 컬러맵(Colormap, 예: `'jet'`, `'viridis'`, `'RdYlGn'`) 정보들을 웹 브라우저 기반 반응형 시각화 라이브러리인 **Plotly 전용 인터랙티브 컬러맵 데이터 규격으로 100% 자동 번역 및 가공**해 주는 시각화 연동 유틸리티 함수(`make_cmp_plotly`)를 제공합니다.

정적인 Matplotlib 3D 분석 그래프를 동적인 Plotly HTML 웹 그래프로 확장 연동할 때, Matplotlib의 전형적인 컬러맵 주소 리스트는 Plotly에서 규격이 달라 색상이 완전히 왜곡되어 표현됩니다. 
본 모듈은 Matplotlib의 컬러 해상도 단계(`pl_entries`)별 RGBA 불투명도 수치를 계산하여, Plotly가 온전히 해석할 수 있는 투명도 포함 컬러맵 스케일(Color Scale)로 완벽하게 포맷 정합을 수행해 줍니다.

---

## 🛠️ 2. 핵심 API 명세 (API Specifications)

### 2.1. 글로벌 컬러맵 번역 함수 명세

| 함수명 | 입력 파라미터 | 설명 |
| :--- | :---: | :--- |
| `make_cmp_plotly(cmap_name, pl_entries)` | `cmap_name`, `pl_entries` | Matplotlib 전용 컬러맵 이름과 가공할 보간 단계 수를 입력받아, Plotly가 100% 웹 브라우저 상에 렌더링할 수 있는 `[[비율, 'rgba(r,g,b,a)'], ...]` 스케일 리스트 데이터로 자동 번역하여 반환 |

---

## 📋 3. 입력 파라미터 상세 정의 (Arguments)

1. **`cmap_name` (`str` - 필수)**:
   - 가공 대상이 될 Matplotlib 공식 컬러맵 명칭입니다. (예: `'jet'`, `'plasma'`, `'coolwarm'`)
2. **`pl_entries` (`int` - 선택, 기본값: `255`)**:
   - 컬러맵을 분할할 그라데이션 밀도 정밀도 수치입니다. 이 값이 커질수록 브라우저 상의 색상 변환이 부드럽고 매끄러워집니다.

---

## 💻 4. 실무 활용 예제 (Multi-case Examples)

### 4.1. [시나리오 1] Matplotlib 'Viridis' 컬러맵의 Plotly 웹 스케일 자동 번역 및 데이터 추출
```python
from unoUtil.graphics.web.plotly_tools import make_cmp_plotly

# Matplotlib의 'viridis' 고정밀 컬러맵 정보를 가져와 10단계 Plotly 스케일로 초고속 번역!
plotly_viridis_scale = make_cmp_plotly(
    cmap_name='viridis',
    pl_entries=10
)

# 번역 결과 구조 확인 (Plotly 전용 그라데이션 비율과 rgba가 합성된 데이터)
print(f"🎨 번역된 Plotly 컬러 스케일 정보:")
for entry in plotly_viridis_scale:
    print(f"  - 비율: {entry[0]:.2f} ➡️ 색상코드: {entry[1]}")
```

### 4.2. [시나리오 2] 번역된 컬러맵을 Plotly 3D Surface 접지압 웹 그래프에 실시간 바인딩
```python
import plotly.graph_objects as go
import numpy as np

# 3D 타이어 접지압 평면 웹용 가상 데이터
z_mesh = np.random.randn(50, 50)

# Matplotlib 'RdYlGn' (Red-Yellow-Green)을 웹 브라우저용 Plotly 컬러 스케일로 정합 번역
plotly_rdylgn = make_cmp_plotly(cmap_name='RdYlGn', pl_entries=255)

# Plotly 인터랙티브 3D Surface 생성 시 colorscale 인자에 다이렉트 주입!
fig_plotly = go.Figure(data=[
    go.Surface(
        z=z_mesh,
        colorscale=plotly_rdylgn  # 번역된 명품 컬러맵 바인딩 성공!
    )
])

# 백그라운드 무인 웹 리소스 내보내기 검증
fig_plotly.write_html("./test_output/interactive_pressure_web.html")
print("💾 브라우저용 Plotly 3D 접지압 그래프 웹 파일 내보내기가 완료되었습니다.")
```

### 4.3. [시나리오 3] 존재하지 않는 Matplotlib 컬러맵 에러 가드
```python
# 잘못되거나 사내 폐기된 컬러맵 명칭이 입력되었을 때, 시스템 크래시를 방지하기 위해 'jet' 기본값으로 안전 우회 디폴트 기동
try:
    plotly_scale = make_cmp_plotly(cmap_name="invalid_cmap_name", pl_entries=100)
except KeyError:
    # 안전 우회 디폴트 바인딩 실행
    plotly_scale = make_cmp_plotly(cmap_name="jet", pl_entries=100)
    print("🛡️ 안전 예외 가드 작동: 'invalid_cmap_name' 대신 'jet' 컬러맵으로 우회 정합 성공!")
```
