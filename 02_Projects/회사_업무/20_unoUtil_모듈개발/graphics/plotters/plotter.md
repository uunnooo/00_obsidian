---
id: "plotter_20260918"
title: "Plotter (실차 시각화 플로터 엔진) 상세 매뉴얼"
type: resource
category_main: 회사_업무
category_sub: 개발매뉴얼
date: 2026-09-18
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - 시각화
  - Plotter
  - Matplotlib
  - 매뉴얼
project_link: "[[unoUtil]]"
---

# 📊 Plotter (실차 시각화 플로터 엔진) 상세 매뉴얼

> [!ABSTRACT] 📌 개요
> 실차 주행 시험의 다축 시계열(속도, 가속도, 제동압력 등)을 표준 규격으로 렌더링하고, **GUI 프로세스 블로킹을 원천 차단하는 Non-blocking 시각화 엔진**입니다.  
> 
> * **영구 공학 지식 레퍼런스**: [[26_대규모_파이썬_패키지_모듈화_및_무중단_하위호환_아키텍처#4-시각화-무중단non-blocking-엔지니어링-표준]]
> * **상위 대시보드**: [[00_graphics_대시보드]] | [[00_unoUtil_모듈개발_대시보드]]

---

## 1. ⚙️ 주요 API 규격

### 1.1. `Plotter` 클래스 (`_Plotter_`)
* **기능**: 다채널 플롯 생성, 서브플롯 배치, 범례/축 라벨 자동 정합, 테마 서식 적용.
* **주요 메서드**:
  - `plot(...)`: 데이터프레임 시계열 플롯 렌더링.
  - `save_figure(path, ...)`: 고해상도(300 DPI) 이미지 디스크 저장.
  - `format_fig(...)`: 표준 폰트 및 스타일 적용.

### 1.2. 🚫 Non-blocking 원칙 준수
`Plotter`는 프로세스 정지(Hang)를 유발하는 `plt.show()` 호출을 일체 배제하며, figure 객체를 반환하거나 `save_figure()` 후 `plt.close(fig)`를 수행하여 메모리 누수를 원천 방지합니다.

---

## 2. 💻 호출 예제 (Usage Example)

```python
import pandas as pd
from unoUtil.graphics.plotters import Plotter

df = pd.DataFrame({"Time": [0, 1, 2], "Speed": [100, 50, 0]})
plotter = Plotter()
fig, ax = plotter.plot(df, x="Time", y="Speed", title="Braking Profile", save="brake.png")
```
