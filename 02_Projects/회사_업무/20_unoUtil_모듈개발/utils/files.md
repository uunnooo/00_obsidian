---
id: "utils_files_20260918"
title: "files (파일 및 디렉터리 조작 유틸리티) 상세 매뉴얼"
type: resource
category_main: 회사_업무
category_sub: 개발매뉴얼
date: 2026-09-18
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - 유틸리티
  - 파일
  - 매뉴얼
project_link: "[[unoUtil]]"
---

# 📁 files (파일 및 디렉터리 조작 유틸리티) 상세 매뉴얼

> [!ABSTRACT] 📌 개요
> 대용량 시험 데이터 경로 탐색, 디렉터리 자동 생성, 파일 패턴 필터링 및 일괄 이름 변경을 수행하는 표준 파일 시스템 헬퍼 모듈입니다.  
> 
> * **상위 대시보드**: [[00_utils_대시보드]] | [[00_unoUtil_모듈개발_대시보드]]

---

## 1. ⚙️ 주요 API 규격

### 1.1. `check_path(path, create=True, ...)`
* **기능**: 대상 경로(파일 또는 디렉터리)의 존재 여부를 점검하고, 부모 디렉터리가 없을 경우 안전하게 자동 생성합니다.

### 1.2. `get_file_names(directory, extensions=None, recursive=False, ...)`
* **기능**: 특정 디렉터리 내에서 지정된 확장자(`.vbo`, `.csv`, `.d7d` 등)를 가진 파일 경로 리스트를 반환합니다.

### 1.3. `rename_files(file_list, pattern, replacement, ...)`
* **기능**: 정규식 또는 문자열 치환을 통해 시험 데이터 파일명을 일괄 변경합니다.
