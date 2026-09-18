---
id: "cursor_mode_20260918"
title: "cursor_mode & range_selector (상호작용 제어기) 상세 매뉴얼"
type: resource
category_main: 회사_업무
category_sub: 개발매뉴얼
date: 2026-09-18
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - 시각화
  - 커서모드
  - 마우스상호작용
  - 매뉴얼
project_link: "[[unoUtil]]"
---

# 🖱️ cursor_mode & range_selector (상호작용 제어기) 상세 매뉴얼

> [!ABSTRACT] 📌 개요
> Matplotlib 기반 플롯에서 십자선 커서 표시, 실시간 좌표 읽기, 마우스 드래그/클릭을 통한 관심 구간(ROI) 선택을 지원하는 컨트롤 패키지입니다.  
> 
> * **상위 대시보드**: [[00_graphics_대시보드]] | [[00_unoUtil_모듈개발_대시보드]]

---

## 1. ⚙️ 주요 API 규격

### 1.1. `set_cursor_mode(ax, ...)` (`SetCursorMode`)
* **기능**: 특정 서브플롯 축(`ax`)에 마우스 커서 호버 시 실시간 수치 좌표 툴팁 및 십자선을 활성화합니다.

### 1.2. `RangeSelectorMouseClick` (`SelRangeMouseClick`)
* **기능**: 사용자가 차트 위에서 마우스 클릭으로 시작점($x_1$)과 종료점($x_2$)을 지정하여 시험 분석 구간을 대화형으로 선정합니다.
