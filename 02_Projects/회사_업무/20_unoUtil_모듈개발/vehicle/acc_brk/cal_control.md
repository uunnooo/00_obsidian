---
id: "cal_control_legacy_module"
title: "Cal_Control 레거시 콘트롤 타이어 보정 모듈 매뉴얼"
type: manual
category_main: 회사_업무
category_sub: VT_ACCBRK
topic: 콘트롤타이어_시계열보정
date: 2026-09-18
status: 완료
tags:
  - 회사_업무
  - VT_ACCBRK
  - Cal_Control
  - 성능보정
  - 레거시호환
aliases:
  - Cal_Control
  - Cal_Control.py
  - 레거시보정모듈
---

# 📐 Cal_Control 레거시 콘트롤 타이어 보정 모듈 매뉴얼

> [!WARNING] ⚠️ 레거시 모듈 안내 및 신규 표준 권장
> 본 모듈은 과거 버전과의 하위 호환성을 위해 유지되는 레거시 함수형 보정 모듈입니다.  
> 현재 `unoUtil`의 공식 표준 보정 엔진은 객체 지향 구조, 환경 인자(기온, 노면온도 등) 연계 및 다양한 물리 프로파일 보정을 완벽히 지원하는 **`unoUtil.vehicleTest.ACCBRK._CORRECT_.CORRECT`** 클래스입니다.  
> 신규 분석 파이프라인 개발 시에는 **[[21_CORRECT|CORRECT]]** 클래스 사용을 적극 권장합니다.

---

## 🏛️ 1. 아키텍처 및 역할

`Cal_Control.py`는 실차 가속 및 제동 시험에서 시험 시간 경과에 따른 노면 마찰력 및 외기 환경의 변화를 상쇄하기 위해, 시험 주기 사이에 배치된 **콘트롤 타이어(Reference Tire)**의 측정값을 시계열(Datetime) 축 기준으로 **선형 보간(Linear Interpolation)**하여 각 테스트 타이어의 상대 성능 지수(Index)와 보정 성능값(Corrected Value)을 도출합니다.

```mermaid
graph LR
    Raw[원시 시험 요약 데이터] --> Mask[find_reference_tire: 콘트롤 타이어 식별]
    Mask --> Interp[시계열 선형 보간: adj_refer_* 생성]
    Interp --> Calc[지수 산출: Positive / Negative 지표]
    Calc --> Reorder[reorder_columns: 표준 컬럼 순서 재배치]
    Reorder --> Result[전체 보정표 & 최종 요약본 반환]
```

---

## 🛠️ 2. 핵심 함수 명세 (API Specification)

### 2.1 `find_reference_tire`
* **기능**: 타이어 세트명(`TestTireSet`) 패턴을 분석하여 전체 콘트롤 타이어 행 마스크와 최종 보고서 요약용 마스크를 생성합니다.
* **시그니처**:
  ```python
  def find_reference_tire(df_input: pd.DataFrame, ptn_refer: str = 'c') -> Tuple[pd.Series, pd.Series]:
  ```
* **반환값**:
  - `mask_ref_tire`: 콘트롤 타이어에 해당하는 전체 행 Boolean 마스크.
  - `mask_summary`: 첫 번째 콘트롤 타이어 1개 + 모든 테스트 타이어를 포함하는 요약용 마스크.

### 2.2 `reorder_columns`
* **기능**: 데이터프레임의 컬럼 순서를 `[Basic -> Target -> Target Add -> 나머지]` 우선순위로 일관되게 재배치합니다.
* **시그니처**:
  ```python
  def reorder_columns(df_input: pd.DataFrame, col_basic: list, col_target: list = None, col_target_add: list = None) -> pd.DataFrame:
  ```

### 2.3 `cal_reference_corrected`
* **기능**: 콘트롤 타이어 기반 시계열 선형 보간을 수행하여 정규화 성능 지수 및 보정값을 산출합니다.
* **시그니처**:
  ```python
  def cal_reference_corrected(
      df_input: pd.DataFrame,
      col_seq: str = 'Datetime',
      col_target_positive: Optional[list] = None,  # 클수록 좋은 지표 (가속도 'Ax' 등)
      col_target_negative: Optional[list] = None,  # 작을수록 좋은 지표 (제동거리 'Dist' 등)
      col_basic: Optional[list] = None,
      col_target_add: Optional[list] = None,
      inverse: bool = False,                       # 음의 지표 역수 비례 공식 사용 여부
      flag_print: bool = True,                     # 로깅 활성화 플래그
      **kwargs: Any
  ) -> Tuple[pd.DataFrame, pd.DataFrame]:
  ```
* **수학적 계산식**:
  - **Positive 지표 (가속도 등)**:
    $$\text{Index} = \frac{\text{Value}}{\text{Adj\_Refer}} \times 100$$
    $$\text{Corrected} = \text{Control\_Mean} \times \frac{\text{Index}}{100}$$
  - **Negative 지표 (제동거리 등, inverse=False 기본)**:
    $$\text{Index} = \frac{2 \times \text{Adj\_Refer} - \text{Value}}{\text{Adj\_Refer}} \times 100$$
    $$\text{Corrected} = \text{Control\_Mean} + \text{Control\_Mean} \times \left(1 - \frac{\text{Index}}{100}\right)$$
  - **Negative 지표 (inverse=True 역수 비례 옵션)**:
    $$\text{Index} = \frac{\text{Adj\_Refer}}{\text{Value}} \times 100$$

---

## 📢 3. 엔터프라이즈 로깅 전환 내역

기존 `print()` 기반 콘솔 출력을 전면 제거하고 표준 로거로 일원화하였습니다:

```python
import logging
from unoUtil.logger import LOGGER

logger = LOGGER("CalControl", root_name="VT_ACCBRK", level=logging.DEBUG)
```

* `logger.info`: 보정 연산 시작/완료 상태.
* `logger.warning`: 콘트롤 타이어 부재 시 첫 행을 임의 기준으로 사용하는 방어 로직 경고.
* `logger.error`: 입력 데이터프레임 부재 시 에러 알림.
* `logger.debug`: 보정 결과 테이블 및 요약 데이터 상세 덤프.

---

## 💻 4. 자가 구동 검증 예제 (`__main__`)

외부 파일 의존성 없이 독립 검증이 가능한 Mock 시나리오가 내장되어 있습니다:

```python
if __name__ == "__main__":
    logger.info(" [Cal_Control] 레거시 콘트롤 타이어 보정 모듈 검증 및 예제")

    dates = pd.date_range('2026-03-11 09:00', periods=4, freq='30min')
    df_sample = pd.DataFrame({
        'Datetime': dates,
        'TestReqNo': ['REQ-2026-001'] * 4,
        'TestTireSet': ['C1_1st', 'T1', 'T2', 'C1_2nd'],
        'Dist': [40.0, 42.5, 39.2, 41.0],      # 제동거리 (Negative 지표)
        'Ax': [0.82, 0.76, 0.84, 0.79]         # 감속도 (Positive 지표)
    })

    # [시나리오 A] 기본 콘트롤 타이어 보정 (제동거리 & 감속도 동시 산출)
    df_full, df_sum = cal_reference_corrected(
        df_sample,
        col_target_negative=['Dist'],
        col_target_positive=['Ax'],
        flag_print=True
    )

    # [시나리오 B] 역수 지수 (inverse=True) 옵션 적용 검증
    df_inv, _ = cal_reference_corrected(
        df_sample,
        col_target_negative=['Dist'],
        col_target_positive=['Ax'],
        inverse=True,
        flag_print=False
    )
    logger.success("[SUCCESS] Cal_Control 모든 시나리오 검증 성공!")
```

---

## 🔗 5. 관련 문서 및 옵시디언 백링크
* 📚 **영구 도메인 지식**: [[27_실차_제동가감속_성능지수_수학적모델_및_시계열_선형보정_이론|27_실차 제동·가감속 성능지수 수학적 모델 및 시계열 선형 보정 이론]]
* 🏛️ **표준화 총괄 가이드**: [[00_unoUtil_모듈개발_대시보드#3-개발-및-코딩-표준-헌장-pep-8--clean-code|unoUtil PEP 8 & Clean Code 코딩 표준 헌장]]
* 📊 **상위 대시보드**: [[00_vt_acc_brk_대시보드]]
* 🏎️ **신규 표준 보정 엔진**: [[correct]]
* 🏛️ **프로젝트 통합 클래스**: [[vt_acc_brk_project]]

