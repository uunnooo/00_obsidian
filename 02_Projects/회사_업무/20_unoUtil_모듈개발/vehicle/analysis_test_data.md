# 📚 VCTA 타이어 성능 분석 모듈 문서 (`_AnalysisTestData_.py`)

이 모듈은 타이어 성능 시험 데이터의 **선형 보정, 통계 분석 및 리포트 생성**을 위한 전문적인 유틸리티 함수들을 제공합니다. `pandas`, `numpy`를 활용하여 데이터의 신뢰성을 확보하고, 컨트롤 타이어 기반의 성능 지수(Index)를 자동으로 산출합니다.

---

## 📊 데이터 처리 및 보정 함수

### 1. astype_float(df_input)
데이터프레임의 모든 열에 대해 수치형(float) 변환을 시도합니다.
* **기능**: 숫자로 변환 가능한 문자열은 `float64`로 변환하고, 변환 불가능한 텍스트 데이터는 원본을 유지하여 데이터 유실을 방지합니다.
* **매개변수**:
    * `df_input` : `pd.DataFrame` (수치형으로 변환할 대상 데이터프레임)
* **반환**:
    * `pd.DataFrame` : 변환 가능한 데이터가 수치형으로 변경된 데이터프레임.
* **예시**:
    ```python
    import pandas as pd
    # BrkDist와 Noise 컬럼의 타입을 수치형으로 정제
    df_raw_data[['BrkDist', 'Noise']] = astype_float(df_raw_data[['BrkDist', 'Noise']])
    ```

### 2. calc_performance (make_performance_df)(df_input, str_result_col, str_name_col, str_test_seq='Datetime', str_refer_kwd='c')
컨트롤 타이어 간 성능 변화를 선형 보정(Linear Interpolation)하여 시험 타이어의 상대 성능 지수를 산출합니다.
* **기능**: 환경 변화를 제거하기 위해 가상의 컨트롤 기준값(`adj_`)을 계산하고, 이를 기반으로 100 기준의 성능 지수(`per_`)를 생성하여 원본 데이터프레임에 추가합니다.
* **보정 수식**:
    * 예상 컨트롤($adj$) = $C_{start} + (C_{end} - C_{start}) \times \frac{현재순번 - 시작순번}{전체간격}$
    * 성능 지수($Index$) = $(adj / Measured\_Value) \times 100$
* **매개변수**:
    * `df_input` : `pd.DataFrame` (전체 시험 결과 데이터)
    * `str_result_col` : `str` (분석 대상 지표 컬럼명, 예: 'BrkDist')
    * `str_name_col` : `str` (타이어 세트 이름 컬럼명)
    * `str_refer_kwd` : `str` (컨트롤 타이어 식별 키워드, 기본 'c')
* **반환**:
    * `pd.DataFrame` : 보정값(`adj_`)과 성능 지수(`per_`) 컬럼이 추가된 데이터프레임.
* **예시**:
    ```python
    # 'c'로 시작하는 타이어를 기준으로 제동거리(BrkDist) 지수 산출
    df_perf = calc_performance (make_performance_df)(df_raw, 'BrkDist', 'tireSet', str_refer_kwd='c')
    ```

### 3. calc_compare (make_compare_df)(list_dfs, list_comp_cols, list_sel_cols, **kwargs)
전달받은 비교 기준을 열(Column)로 펼치고, 선택 지표(Metric)를 행(Index)으로 구성한 최종 비교 리포트를 생성합니다.
* **기능**: 여러 데이터를 통합하고 `unstack`과 `stack` 과정을 통해 지표 중심의 계층 구조를 만듭니다. 동일 조건의 반복 데이터는 평균값으로 집계합니다.
* **매개변수**:
    * `list_dfs` : `list of pd.DataFrame` (병합할 데이터프레임 리스트)
    * `list_comp_cols` : `list` (가로 열로 펼쳐 비교할 기준 컬럼명 리스트, 예: ['Test_Round', 'tireSet'])
    * `list_sel_cols` : `list` (세로 행으로 보낼 지표명 리스트, 예: ['BrkDist', 'per_BrkDist'])
    * `list_del_cols` : `list`, optional (그룹화 과정에서 제외할 컬럼 리스트)
* **반환**:
    * `df_compare` : `pd.DataFrame` (지표 중심의 타이어별 비교 리포트)
    * `df_static` : `pd.DataFrame` (리포트 데이터를 기반으로 산출된 요약 통계표)
* **예시**:
    ```python
    # 차수(Test_Round)와 타이어(tireSet)별로 4개 지표를 통합 비교 리포트 생성
    list_metrics = ['BrkDist', 'per_BrkDist', 'Noise', 'per_Noise']
    df_compare, df_static = calc_compare (make_compare_df)([df_input], ['Test_Round', 'tireSet'], list_metrics)
    ```

### 4. get_staticks_df(df_source)
데이터프레임의 수치형 컬럼들에 대해 10가지 주요 통계 지표를 계산합니다.
* **기능**: 평균, 범위, IQR, 표준편차, 최대, 최소, 사분위수(Q1, Q3), 중앙값, 개수를 계산하여 반환합니다.
* **매개변수**:
    * `df_source` : `pd.DataFrame` (통계량을 계산할 데이터프레임)
* **반환**:
    * `pd.DataFrame` : 10가지 통계 지표가 행(Index)으로 구성된 요약 통계표.
* **예시**:
    ```python
    # 생성된 비교표를 바탕으로 타이어군별 통계 요약표 생성
    df_static_summary = get_staticks_df(df_compare)
    ```

### 5. agg_mean(df_target)
데이터프레임의 열별 평균을 계산하며, 비수치형 데이터에 대한 예외 처리를 수행합니다.
* **기능**: 평균 계산 시도 후 실패 시 최댓값을 반환하여 데이터 유실 없이 대표값을 추출합니다.
* **매개변수**:
    * `df_target` : `pd.DataFrame` (집계 대상 데이터프레임)
* **반환**:
    * `pd.Series` : 열별 평균값 또는 최댓값이 담긴 시리즈.
* **예시**:
    ```python
    # 제동거리와 소음의 단순 열별 평균값 확인
    ser_agg_result = agg_mean(df_raw_data[['BrkDist', 'Noise']])
    ```

---

## 📋 리포트 출력 예시 (Sample Output)

`calc_compare (make_compare_df)` 함수를 통해 생성된 최종 리포트는 아래와 같은 구조를 가집니다.

| parameter | R1_Control | R1_t_01 | R2_Control | R2_t_01 |
| :--- | :---: | :---: | :---: | :---: |
| **BrkDist** | 40.30 | 42.25 | 40.50 | 42.50 |
| **per_BrkDist** | 100.00 | 95.38 | 100.00 | 95.29 |
| **Noise** | 70.65 | 68.10 | 70.80 | 68.00 |
| **per_Noise** | 100.00 | 101.45 | 100.00 | 101.32 |

---
**Last Updated**: 2026-09-18  
**Department**: VCTA (Vehicle Characteristic Test & Analysis)  
**Author**: Yunho Jung

## 🔗 관련 문서 및 옵시디언 백링크
* 📚 **영구 도메인 지식**: [[27_실차_제동가감속_성능지수_수학적모델_및_시계열_선형보정_이론|27_실차 제동·가감속 성능지수 수학적 모델 및 시계열 선형 보정 이론]]
* 🏛️ **표준화 총괄 가이드**: [[00_unoUtil_PEP8_표준화_총괄_가이드|unoUtil PEP 8 표준화 총괄 가이드]]
* 📐 **컨트롤 타이어 선형 보정 모듈**: [[cal_control|cal_control 모듈 매뉴얼]]
* 🏎️ **가감속/제동 종합 분석 프레임워크**: [[vt_acc_brk|vt_acc_brk 모듈 매뉴얼]]