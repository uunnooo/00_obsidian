---
id: vt_acc_brk_naming_rule
title: vt_acc_brk 모듈 통합 표준 네이밍 규칙 및 Flat 저장 아키텍처
type: standard
category_main: 회사_업무
category_sub: unoUtil
date: 2026-10-16
status: 완료
tags:
  - 회사_업무
  - unoUtil
  - acc_brk
  - 네이밍룰
  - 아키텍처
  - 코딩표준
aliases:
  - vt_acc_brk_모듈_네이밍룰
  - vt_acc_brk_네이밍룰
  - acc_brk_naming_rule
---

# 🏷️ vt_acc_brk 모듈 통합 표준 네이밍 규칙 및 Flat 저장 아키텍처

본 문서는 사내 실차 가속(ACC) 및 제동(BRK) 통합 분석 프레임워크인 `unoUtil.vehicle.acc_brk` 모듈군(`vt_acc_brk`, `VTAccBrkTire`, `VTAccBrkProject`, `PlotterTire`, `PlotterProject`)에서 생성되는 **산출물 식별자(Stem), 디스크 저장 파일명, 시각화 이미지명, 차트 타이틀 및 폴더 구조**의 단일 진실 공급원(SSOT) 표준 헌장입니다.

---

## 🏛️ 1. 핵심 아키텍처 원칙 (Core Principles)

1. **식별자-파일명-차트 타이틀 1:1 완전 일치 원칙 (Single Stem Law)**:
   - 디스크에 저장되는 파일명(확장자 제외), 플롯 이미지 파일명(접두 일련번호 제외), 화면에 렌더링되는 차트 상단 제목(`suptitle`)은 반드시 **동일한 표준 식별자(Stem)**를 공유해야 합니다.
2. **단일 계층(Flat) 저장 원칙 (Flat Directory Law)**:
   - 과거 파일명 중복을 방지하기 위해 생성되던 임의의 속도별 하위 폴더(`0. db/brk_100-5/` 등)를 **완전 폐지**합니다.
   - 모든 산출물 파일명 자체에 시험 항목 및 속도 구간이 정규화되어 포함되므로, `0. db/`, `2. fig/`, `3. result/`의 **직하위 단일 계층(Flat)**에 파일들이 저장됩니다.
3. **무효 토큰 완전 제외 원칙 (Clean Token Law)**:
   - 메타데이터 조합 시 `None`, 빈 문자열(`""`), 공백, 문자열 `"None"`은 무조건 제외되며, 유효한 토큰만 언더스코어(`_`)로 결합합니다.
4. **시험 항목/거동 모드 자동 폴백 원칙 (Item-Mode Fallback Law)**:
   - 시험 항목(`item`)이 명시되지 않았거나 비어 있는 경우, 속도 증감에 따라 자동 감지된 물리 모드(`mode`: `'brk'` 또는 `'acc'`)가 기본값으로 자동 치환됩니다.

---

## 🏷️ 2. 통합 네이밍 종합 규격 매트릭스

| 대상 | 표준 식별자 (Stem) 조립 규칙 | 저장 파일명 | 이미지 파일명 (`.png`) | 차트 상단 타이틀 (`Title`) |
| :--- | :--- | :--- | :--- | :--- |
| **타이어 객체** | `[req]_[surface]_[item]_[cond]_[vel_tag]_{set}` | `{tire_stem}.tir` | `{플롯명}_{tire_stem}.png` | `{플롯명}_{tire_stem}` |
| **프로젝트 객체** | **1순위**: `pjt_name` (다중속도시 `_{vel_tag}` 추가)<br>**2순위**: `[req]_[surface]_[item]_[cond]_[vel_tag]`<br>**3순위**: `{최하위폴더명}_{item}_{vel_tag}` | `{pjt_stem}.pjt` | `{플롯명}_{pjt_stem}.png` | `{플롯명}_{pjt_stem}` |
| **원시 데이터** | `{base_test_name}` (사용자 `pjt_name` 또는 최하위 폴더명) | `{base_test_name}_raw.gz` | - | - |
| **보고서 엑셀** | `graph_{pjt_stem}.xlsx` | `graph_{pjt_stem}.xlsx` | - | 시트명: `Graph_{pjt_stem}`[:31] |

---

## 📂 3. 표준 디렉토리 구조 (Flat Architecture)

원천 계측 데이터가 위치한 루트 폴더(`dir_path`)를 기준으로, 3대 표준 작업 폴더의 직하위에 정갈하게 파일이 배치됩니다:

```text
📁 {dir_path} (사용자가 지정한 시험 데이터 루트 폴더, 예: D:/data/2026_Dry)
│
├── 📁 0. db/                                 <-- 데이터베이스 & 직렬화 캐시 (.gz, .tir, .pjt)
│   ├── 📄 2026_Dry_raw.gz                    <-- [원시 데이터 캐시] 폴더당 1회 압축 생성
│   ├── 📄 dry_brk_100-5_C1.tir               <-- [타이어 분석 객체] 표준 식별자 기반
│   ├── 📄 dry_brk_100-5_T1.tir
│   └── 📄 dry_brk_100-5.pjt                  <-- [통합 프로젝트 객체] 표준 식별자 기반
│
├── 📁 1. rawdata/                            <-- [원천 계측 파일] (.vbo, .vbb, .d7d)
│
├── 📁 2. fig/                                <-- 그래프 시각화 이미지 (.png)
│   ├── 🖼️ 0_accbrk_dry_brk_100-5_C1.png      <-- [타이어 차트] {일련번호_플롯명}_{tire_stem}.png
│   ├── 🖼️ 1_acceleration_dry_brk_100-5_C1.png
│   └── 🖼️ 8_Braking_Test_Result_dry_brk_100-5.png  <-- [프로젝트 비교 차트]
│
└── 📁 3. result/                             <-- 수치 결과 및 보고서
    └── 📊 graph_dry_brk_100-5.xlsx
```

---

## ⚙️ 4. 세부 식별자 조립 상세 규격

### 4.1 타이어 식별자 (`tire_name`)
$$\text{[req]} \rightarrow \text{[surface]} \rightarrow \text{[item]} \rightarrow \text{[cond]} \rightarrow \text{[vel\_tag]} \rightarrow \text{\{set\}}$$

1. **`req`**: 의뢰번호 (예: `REQ26001`)
2. **`surface`**: 노면 (예: `dry`, `wet`, `snow`, `ice`)
3. **`item`**: 시험 항목 (예: `brk`, `acc`, `surface`). 미입력 시 `mode` 반영
4. **`cond`**: 추가 시험 조건 (예: `normal`, `wetted`, `abs_off`)
5. **`vel_tag`**: 시험 속도 구간 문자열 (예: `'100-5'`, `'20-35'`)
6. **`set`**: 시편 세트명 (**필수**, 원천 파일명 마지막 언더스코어 뒷자리 자동 추출 또는 수동 입력, 예: `C1`, `T1`)

* **실제 생성 예시**:
  * 메타데이터 최소 상태: `C1` $\rightarrow$ `C1.tir`
  * 기본 조건만 있는 경우: `dry_brk_100-5_C1` $\rightarrow$ `dry_brk_100-5_C1.tir`
  * 전체 메타데이터 포함 시: `REQ26001_wet_brk_wetted_80-5_C2` $\rightarrow$ `REQ26001_wet_brk_wetted_80-5_C2.tir`

### 4.2 프로젝트 식별자 (`project_name`) (3단계 우선순위)
1. **1순위 (사용자 지정 `pjt_name`)**:
   * 단일 속도 시험: 사용자가 지정한 `pjt_name` 그대로 사용 (예: `MyProject`)
   * 다중 속도 시험: `f"{pjt_name}_{vel_tag}"` (예: `MyProject_100-5`, `MyProject_80-20`)
2. **2순위 (메타데이터 조합)**:
   * 타이어 템플릿에서 `{set}`만 제외한 조합: `[req]_[surface]_[item]_[cond]_[vel_tag]`
   * 예: `dry_brk_100-5`, `251230_snow_surface_20-5`
3. **3순위 (완전 디폴트 최후 보루)**:
   * 메타데이터와 `pjt_name`이 모두 부재할 경우: `{최하위폴더명}_{item}_{vel_tag}`
   * 예: `2026_Dry_brk_100-5`

---

## 💻 5. 실무 프로젝트 로드 레시피 (Loading Recipes)

### 5.1 명시적 파일명 지정 로드
```python
from unoUtil.vehicle.acc_brk import load_vt_acc_brk

# 1. 대상 프로젝트 파일 경로 지정 (Flat 디렉토리)
pjt_file = r"D:\data\251230\0. db\251230_snow_surface_20-5.pjt"

# 2. 로드 및 객체 추출
dict_pjt = load_vt_acc_brk(pjt_file)
pjt = dict_pjt['251230_snow_surface_20-5']

print("로드 완료 타이어 목록:", list(pjt.tire_analyzers.keys()))
print(pjt.result.summary[['TestTireSet', 'brk_mean', 'index_brk_mean']])
```

### 5.2 `0. db` 폴더 내 자동 탐색 로드 (가장 권장되는 패턴 ⭐️)
```python
from pathlib import Path
from unoUtil.vehicle.acc_brk import load_vt_acc_brk

folder = r"D:\data\251230"
db_dir = Path(folder) / "0. db"

# 0. db 폴더 내 .pjt 파일을 자동 검색하여 로드
pjt_files = list(db_dir.glob("*.pjt"))
if pjt_files:
    dict_pjt = load_vt_acc_brk(str(pjt_files[0]))
    pjt = next(iter(dict_pjt.values()))
    print("로드 성공:", pjt.prj_name)
```
