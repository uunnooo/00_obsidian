---
id: "excel_20260920"
title: "excel (Matplotlib 엑셀 이미지 자동 삽입 유틸리티) 상세 매뉴얼"
type: resource
category_main: 회사_업무
category_sub: 개발매뉴얼
date: 2026-09-20
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - 유틸리티
  - 엑셀
  - 매뉴얼
project_link: "[[unoUtil]]"
---

# 📊 excel (Matplotlib 엑셀 이미지 자동 삽입 유틸리티) 상세 매뉴얼

> [!ABSTRACT] 📌 개요
> Matplotlib을 통해 시각화된 주행/제동 데이터 피규어 객체를 사내 표준 보고서 양식인 Excel 파일의 특정 시트와 셀에 자동 정렬 삽입하고, 인접 여백을 고려한 다음 상/하/좌/우 셀 주소를 계산해 내는 엑셀 리포팅 연동 모듈입니다.
> 
> * **상위 대시보드**: [[00_utils_대시보드]] | [[00_unoUtil_모듈개발_대시보드]]

---

## 1. ⚙️ 주요 API 규격

### 1.1. `insert_figure_to_excel(excel_path, sheet_name, fig_object, start_cell, ...)`
* **기능**: Matplotlib `plt.Figure` 객체를 고해상도 PNG(300dpi)로 엑셀에 삽입하고, 이미지 점유 셀 면적을 픽셀(px) 단위로 연산하여 인접한 상/하/좌/우의 다음 삽입 셀 좌표를 자동으로 반환합니다.
* **매개변수**:
  - `excel_path (str)`: 저장할 엑셀 파일의 절대 또는 상대 경로.
  - `sheet_name (str)`: 이미지가 삽입될 엑셀 시트 이름 (미존재 시 자동 생성).
  - `fig_object (plt.Figure)`: Matplotlib 피규어 인스턴스.
  - `start_cell (str)`: 좌상단 기준 이미지 삽입을 시작할 셀 좌표 (예: `'B2'`).
  - `width (float, optional)`: 이미지 가로 너비(mm 단위를 엑셀 px로 변환). 기본값 `150.0`.
  - `height (float, optional)`: 이미지 세로 높이(mm). width와 상호 배타적 적용.
  - `overwrite (bool)`: 기존 파일을 지우고 새 빈 워크북으로 시작할지 여부. 기본값 `False`.
  - `workbook (openpyxl.Workbook, optional)`: 외부에서 이미 열어놓은 openpyxl 워크북 객체 전달 시, 중복 로드 파일 I/O를 전면 배제하여 속도를 개선합니다.
  - `save (bool)`: 이미지 병합 반영 후 디바이스 디스크에 즉시 물리 저장할지 여부. 기본값 `True`.
* **반환값**: 성공 여부 및 다음 삽입 셀 주소를 포함한 딕셔너리:
  ```python
  {
      'success': True,
      'up': 'B1',        # 이미지 위 여백 셀
      'down': 'B16',     # 이미지 아래 여백 셀
      'right': 'I2',     # 이미지 오른쪽 여백 셀
      'left': 'A2',      # 이미지 왼쪽 여백 셀
      'workbook': wb     # 처리된 openpyxl Workbook 인스턴스
  }
  ```

---

## 💻 2. 호출 예제 (Usage Example)

```python
import matplotlib.pyplot as plt
import pandas as pd
from unoUtil.utils.excel import insert_figure_to_excel

# 1. 시각화 피규어 객체 생성
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot([1, 2, 3], [10, 20, 30], label="Braking Distance")
ax.legend()

# 2. 첫 번째 그래프를 B2 셀에 삽입 (물리 저장 생략 후 워크북 객체 재사용)
res_first = insert_figure_to_excel(
    excel_path="test_report.xlsx",
    sheet_name="BrakingReport",
    fig_object=fig,
    start_cell="B2",
    width=100.0,
    overwrite=True,
    save=False
)

# 3. 계산된 'down' 셀을 활용하여 두 번째 그래프를 엑셀 파일에 이어서 기입하고 최종 물리 저장(save=True)
if res_first["success"]:
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.plot([1, 2, 3], [30, 20, 10], color="red", label="Mu-Drop")
    ax2.legend()
    
    insert_figure_to_excel(
        excel_path="test_report.xlsx",
        sheet_name="BrakingReport",
        fig_object=fig2,
        start_cell=res_first["down"],  # B16 셀에 이어서 삽입
        width=100.0,
        workbook=res_first["workbook"], # 워크북 인스턴스 공유 (연속 I/O 최적화)
        save=True
    )
    plt.close(fig2)

plt.close(fig)
```
