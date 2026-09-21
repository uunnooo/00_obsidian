# 🧭 brk_test 제동 시험 분석 래퍼 브릿지 매뉴얼 (brk_test.md)

## 📌 1. 개요 및 목적 (Overview)
`brk_test` 모듈은 사내 실차 제동 시험 분석 파이프라인과의 하위 호환성을 보장하기 위해 기존 레거시 함수형 엔지니어링 인터페이스를 전격 흡수하는 **제동 시험 분석 전용 프록시 브릿지 래퍼 모듈**입니다.

사내의 수많은 기존 제동 자동화 스크립트들과 주피터 노트북은 과거의 파일 및 함수 구조를 다이렉트로 가져와 호출하도록 빌드되어 있어, 패키지를 V2.0 Clean Architecture로 개편할 때 심각한 마이그레이션 다운타임 에러가 발생할 수 있습니다. 
본 모듈은 구버전 호출 구문을 100% 무중단 지원하며, 모든 실제 제동 물리 연산 및 분석 로직은 차세대 표준 엔진인 **`unoUtil.vehicle.ACCBRK.func_acc_brk`** 패키지로 투명하게 자동 위임(Forwarding delegation)을 처리하여 무결점 마이그레이션을 보장합니다.

---

## 🛠️ 2. 핵심 API 명세 (API Specifications)

### 2.1. 위임 브릿지 인터페이스 명세

| 함수명 | 입력 파라미터 | 위임 대상 (New Standard API) | 설명 |
| :--- | :---: | :--- | :--- |
| `calc_braking_performance(...)` | `raw_df`, `**kwargs` | `unoUtil.vehicle.ACCBRK.func_acc_brk.calc_performance` | 제동 개시 시점 감지 및 6대 성능 수치 자동 집계 위임 |
| `calc_corrected_reference(...)`| `df_day`, `**kwargs` | `unoUtil.vehicle.ACCBRK.cal_control.calc_reference_corrected` | 컨트롤 타이어의 시계열 선형 보간 및 보정 수치 계산 위임 |

---

## 📋 3. 입력 파라미터 상세 정의 (Arguments)

1. **`raw_df` (`pd.DataFrame` - 필수)**:
   - 전처리할 원시 제동 시험 데이터프레임입니다.
2. **`**kwargs` (선택 - 레거시 헝가리안 인자 흡수)**:
   - `df_input`, `str_col`, `flag_print` 등의 레거시 구버전 파라미터를 내부에서 신규 단어형 인자로 100% 자동 매핑 및 변환 처리합니다.

---

## 💻 4. 실무 활용 예제 (Multi-case Examples)

### 4.1. [시나리오 1] 레거시 스크립트 형태 그대로 제동 성능 계산 (무중단 가동)
```python
import pandas as pd
from unoUtil.vehicle.legacy.brk_test import calc_braking_performance

# 1. 기존 사내 주피터 노트북에 적혀 있던 옛날 방식 그대로 호출 기동!
legacy_vbox_df = pd.DataFrame({"GPS_Speed": [100.0, 50.0, 0.0]})

# 2. 내부 위임 브릿지에 의해 최신 ACCBRK 고속 C-엔진으로 자동 리다이렉트 연산됨
df_result = calc_braking_performance(
    raw_df=legacy_vbox_df,
    target_col="GPS_Speed"
)

print(f"📊 제동 감정 완료! 하위 호환 가동 확인: Rows={len(df_result)}")
```

### 4.2. [시나리오 2] `**kwargs` 호환 변환을 통한 헝가리안 레거시 파라미터 자동 흡수 검증
```python
# 구버전 전용 인자인 'df_input', 'flag_print'를 그대로 전달하여 호출
df_legacy_res = calc_braking_performance(
    df_input=legacy_vbox_df,  # 구버전 전용 키워드 인자 수용
    flag_print=True
)

print("🛡️ 구버전 헝가리안 파라미터가 최신 단어형 인자로 안전 자동 흡수되었습니다.")
```

### 4.3. [시나리오 3] 컨트롤 타이어의 선형 조각 보정 자동 위임 (calc_corrected_reference)
```python
from unoUtil.vehicle.legacy.brk_test import calc_corrected_reference

# 하루 제동 시험 시퀀스 데이터프레임
df_day_sequence = pd.DataFrame({"ReqNo": [1, 2, 3], "BrakingDist": [35.5, 36.2, 34.8]})

# 구버전 선형 보정 브릿지 함수 호출 실행
df_corrected = calc_corrected_reference(
    df_day=df_day_sequence,
    refer_kwd="control"
)

print(f"✅ 보정 연산 위임 완료! 보정된 제동거리: {list(df_corrected['BrakingDist_adj'])}")
```
