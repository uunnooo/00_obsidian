---
id: "work_2026_snow_braking_performance_module"
title: "20_SnowBrakingPerformance 통합 모듈 매뉴얼"
type: project
category_main: 회사_업무
category_sub: SnowSurface
topic: 스노우_제동_통합모듈
date: 2026-09-15
status: 완료
tags:
  - 회사_업무
  - SnowSurface
  - SnowBrakingPerformance
  - 머신러닝보정
  - 디지털트윈
  - ACCBRK
aliases:
  - "SnowBrakingPerformance_매뉴얼"
  - "20_SnowBrakingPerformance_통합모듈_매뉴얼"
---

# ❄️ SnowBrakingPerformance 통합 모듈 매뉴얼

> [!ABSTRACT] 🏔️ 단일 통합 관리 플랫폼 구축 완료
> 기존에 분산되어 있던 **노면 특성 계측 데이터(센서 변위/온도)**와 **실차 제동 평가 데이터(VT_ACCBRK 객체)**를 단일 클래스 `SnowBrakingPerformance`로 엮어, **노면 디지털 트윈 맵 생성 ➡️ 차분 머신러닝 보정 ➡️ 실시간 제동거리 보정 ➡️ 타이어 사양(컴파운드/패턴) 영향도 분석**을 원스톱으로 관리하는 전용 파이썬 패키지입니다.

---

## 🏛️ 1. 패키지 및 모듈 아키텍처

기존 분석 스크립트는 전혀 수정하지 않고, 전용 폴더 **`Snow_braking_relate_condition/`** 아래에 6개 전문 모듈로 모듈화하여 구축되었습니다:

```text
📁 2026_Snow_RoadSurface_characteristics/
└── 📂 Snow_braking_relate_condition/
    ├── __init__.py                     # 패키지 진입점 및 주요 클래스/유틸 함수 export
    ├── Snow_Braking_Performance.py     # [통합 파사드] SnowBrakingPerformance 마스터 컨트롤러
    ├── surface_condition_twin.py       # [디지털 트윈] 센서 오프셋 보정, 3D 트랙 격자 맵, 시공간 보간
    ├── correction_engine.py            # [보정 엔진] 차분법(Difference Method) 머신러닝 보정 (RF, KNN, SVR)
    ├── spec_analyzer.py                # [스펙 분석] 보정 전/후 사양별 분산 감소율, CV%, 순위 일관성 분석
    ├── snow_physics_utils.py           # [물리 유틸] Libbrecht 과포화도, 눈 압축률 및 밀도 역추정식
    └── README.md                       # 패키지 구조 및 활용 가이드
```

---

## ⚙️ 2. 핵심 인터페이스 및 기능 명세

### 1) 데이터 수집 및 등록 (`add_*`, `set_*`)
* `add_surface_data(data)`: 다채널 변위/온도 노면 계측 로우데이터(DataFrame, 파일, 또는 `VT_ACCBRK` 계측 객체)를 누적 추가합니다.
* `add_braking_data(data)`: 실차 제동 평가 데이터(DataFrame, 파일, 또는 `VT_ACCBRK_PROJECT`, `VT_ACCBRK_TIRE` 객체)를 누적 추가합니다.
* `set_weather_data(df_weather)`: 기상 데이터를 연동하며, Libbrecht 결정학 기반 과포화도(Supersaturation) 및 절대습도(AH, AH_Excess)를 자동 연산하여 부착합니다.
* `set_spec_data(df_spec)`: 컴파운드(CTB, SUT), 패턴, 규격 등의 타이어 사양 메타데이터를 연동합니다.

### 2) 3D 시공간 디지털 트윈 구축 (`build_surface_maps`, `match_*`)
* `build_surface_maps(method='RF')`:
  * 기구적 센서 장착 오차(Out vs Tire)를 자동 정렬하여 순수 눈 침하 깊이(HeightDiffAver)를 산출합니다.
  * 트랙 전역(X: 0~415m, Y: 45~90m) 격자 맵을 Random Forest/KNN 기반으로 3D 공간 확장합니다.
  * 복수 시점의 노면 스냅샷을 `scipy interp1d`로 시간 보간하여 시공간 연속체를 형성합니다.
* `match_performance_to_surface()`:
  * 각 제동 시험의 정확한 타임스탬프와 VBOX GPS 좌표(PosX, PosY)를 기반으로 해당 순간의 노면 침하 깊이(`char_height`)와 노면 온도(`char_temp`)를 1:1 결합합니다.

### 3) 차분 머신러닝 보정 및 보정맵 (`train_correction_model`, `generate_correction_map`)
* `train_correction_model(model_type='Random Forest')`:
  * 동일 타이어 1차 vs 2차 반복 시험의 차분값($\Delta \text{Height}, \Delta \text{AH} \to \Delta \text{BrkDist}$)을 추출하여 타이어 고유 실력을 완전 소거합니다.
  * Random Forest(과적합 방지 트리 깊이 규제), KNN(등고선 맵용), SVR, 선형 회귀 등을 자동 학습하고 $R^2$, MAE, MSE를 평가합니다.
* `generate_correction_map()`:
  * 눈 침하 깊이 차이 vs 절대습도 차이에 따른 제동거리 변화량($\Delta \text{BrkDist}$, m) 3D 등고선 보정 맵을 생성합니다.

### 4) 실시간 및 일괄 제동거리 보정 (`correct_*`)
* `correct_braking_distance(raw_dist, cur_condition, ref_condition)`:
  * 입력받은 환경 조건(또는 기준 조건과의 차이)에 대해 수식 $D_{\text{corr}} = D_{\text{raw}} - \Delta D_{\text{pred}}(\text{Current} - \text{Reference})$을 즉시 계산하여 환경 편차가 제거된 제동거리를 반환합니다.
* `correct_dataframe()`:
  * 전체 데이터프레임의 모든 평가에 대해 보정 제동거리 컬럼(`char_brk_dist_corr`)을 일괄 생성합니다.

### 5) 타이어 스펙 영향도 분석 (`analyze_spec_impact`)
* `analyze_spec_impact(spec_col='infor_CTB_COMPOUND')`:
  * 컴파운드/패턴별 보정 전/후 평균, 표준편차, 변동계수(C.V, %) 및 **군집 내 분산 감소율(Variance Reduction, %)**을 정량 산출합니다.
  * 스피어만(Spearman) 순위 상관계수와 켄달 타우(Kendall Tau)를 통해 보정 후 순위 역전(Rank Inversion) 방지 및 일관성을 검증합니다.

### 6) 전용 시각화 제품군 (`plot_*`)
* `plot_surface_map(snapshot_idx=0, channel='height')`: 트랙 전역 3D 공간 노면 침하량 및 온도차 등고선 맵
* `plot_correction_map()`: 노면 침하차 vs 절대습도차에 따른 제동거리 변화량($\Delta \text{BrkDist}$) 3D 등고선 보정맵
* `plot_spec_boxplots(spec_col)`: 보정 전(Raw) vs 보정 후(Corrected) 타이어 사양별 박스플롯 비교
* `plot_residual_dependency(env_col)`: 보정 후 환경 인자와의 잔차/기울기 소거($\text{Slope}=0$) 검증 산점도
* `plot_model_comparison()`: Random Forest, KNN, SVR 모델 간 R² 및 MAE 성능 비교 차트

---

## 📐 2.1 입력 데이터 단위 및 규격 (Data Granularity)

> [!IMPORTANT] 🎯 데이터 기본 단위: **제동 1회 (1 Run) = 1개 행 (1 Row)**
> * **이유**: 하나의 타이어 세트(T1) 안에서도 8~12회의 반복 제동(Run 1, 2, ..., 10)이 일어날 때, **매 1회 제동마다 시험 시각(Datetime)과 트랙 상의 GPS 위치(PosX, PosY)가 실시간으로 달라집니다.**
> * 세트 평균으로 뭉뚱그려 넣지 않고 **제동 1회 단위**로 넣어야, 그 순간 그 위치의 노면 침하 깊이(`char_height`) 및 기상 인자를 3D 노면 디지털 트윈에서 1:1로 정확하게 핀포인트 매칭할 수 있습니다.
> * `VT_ACCBRK_PROJECT`나 `VT_ACCBRK_TIRE` 객체를 그대로 전달하면, 객체 내부의 개별 런(`result.df`)을 자동으로 추출하여 결합합니다.

---

## 💻 3. 원스톱 코드 사용 예시

```python
from Snow_braking_relate_condition import SnowBrakingPerformance

# 1. 마스터 플랫폼 생성
sbp = SnowBrakingPerformance(name="SnowPlatform_2026")

# 2. 노면 및 제동(ACCBRK) 데이터 등록
sbp.add_surface_data(df_surface_raw)   # 또는 VT_ACCBRK 노면 계측 객체
sbp.add_braking_data(obj_accbrk_pjt)   # VT_ACCBRK_PROJECT 또는 TIRE 객체
sbp.set_weather_data(df_weather)       # 기상청 데이터 (과포화도 자동 연산)
sbp.set_spec_data(df_spec)             # 타이어 규격 메타데이터

# 3. 3D 노면 디지털 트윈 생성 및 1:1 시공간 매칭
sbp.build_surface_maps(method='RF')
df_matched = sbp.match_performance_to_surface()

# 4. 차분 머신러닝 보정 모델 학습
metrics = sbp.train_correction_model(model_type='Random Forest')
print("모델 평가 결과:", metrics)

# 5. 임의 조건 제동거리 실시간 보정 질의
corrected_dist = sbp.correct_braking_distance(
    raw_dist=24.5,
    cur_condition={'char_height': 3.8, 'cd_test_ah': 2.1},
    ref_condition={'char_height': 3.0, 'cd_test_ah': 1.5}
)
print(f"환경 정규화된 제동거리: {corrected_dist:.2f} m")

# 6. 전체 데이터 일괄 보정 및 컴파운드 영향도 분석
df_all_corr = sbp.correct_dataframe()
summary, rank_stats = sbp.analyze_spec_impact(spec_col='infor_CTB_COMPOUND')
print(summary)

# 7. 상태 요약 및 영속성 저장
sbp.summary()
sbp.save("./saved_platforms/snow_platform_2026.pkl")
```

---

## 🌲 4. 계층형 로거(`LOGGER`) 및 런타임 벤치마크 모니터링 체계

`Snow_braking_relate_condition` 패키지는 전 모듈에 걸쳐 `unoUtil.convenienceFunction.logger.LOGGER`를 표준 로깅 프레임워크로 채택하였습니다.  
기존의 날것의 `print` 문을 100% 제거하고, 소요 시간 자동 측정 컨텍스트 매니저(`with logger.measure()`)와 계층형 네임스페이스 트리를 구축했습니다.

### 4.1. 계층형 로거 네임스페이스 트리
```text
[SnowBraking] (Root Namespace)
 ├── [SnowBraking.Master]    : Snow_Braking_Performance.py (엔드-투-엔드 오케스트레이션)
 ├── [SnowBraking.Twin]      : surface_condition_twin.py (3D 시공간 디지털 트윈)
 ├── [SnowBraking.Engine]    : correction_engine.py (차분 머신러닝 보정 엔진)
 ├── [SnowBraking.Spec]      : spec_analyzer.py (사양별 분산 및 순위 일관성)
 ├── [SnowBraking.Physics]   : snow_physics_utils.py (설면 열역학 & 눈 밀도 역추정)
 └── [SnowBraking.Dashboard] : surface_dashboard.py (4D 대시보드 웹 서버)
```

### 4.2. 실행 안전성 및 호환성 보강
1. **단독 스크립트 실행 및 패키지 모듈 실행 양방향 호환**:
   `try...except ImportError` 상대 임포트 fallback을 구성하여, `python -m Snow_braking_relate_condition.Snow_Braking_Performance`와 `python Snow_Braking_Performance.py` 직접 실행이 모두 원활히 동작합니다.
2. **파라미터 Alias 지원**:
   `correct_braking_distance()` 호출 시 `reference_condition`과 `ref_condition` 키워드를 모두 유연하게 지원하도록 개선되었습니다.
3. **콘솔 다국어/이모지 인코딩 안전성**:
   Windows 기본 콘솔(`cp949`) 환경에서 눈꽃(❄️) 등의 유니코드 출력 시 발생할 수 있는 `UnicodeEncodeError`를 시스템 수준(`errors='replace'`)에서 완벽 방어하였습니다.

### 4.3. 엔드-투-엔드 자가 검증 런타임 결과 (Exit code 0)
```text
17:11:30 [INFO   ] [SnowBraking.Master] ============================================================
17:11:30 [INFO   ] [SnowBraking.Master]  [Snow_Braking_Performance] 엔드-투-엔드 통합 파이프라인 검증
17:11:30 [INFO   ] [SnowBraking.Master] ============================================================
17:11:30 [INFO   ] [SnowBraking.Master] [OK] Step 1~4: Mock 노면/기상/제동 데이터 등록 완료 (0.041s)
17:11:30 [INFO   ] [SnowBraking.Twin  ] 디지털 트윈 생성 완료: 총 1개 시공간 스냅샷 구축 (RF 방식)
17:11:30 [INFO   ] [SnowBraking.Master] 노면-제동 매칭 완료: 총 60건 결합
17:11:30 [INFO   ] [SnowBraking.Master] [OK] Step 5: 디지털 트윈 생성 및 노면 매칭 완료 (0.479s)
17:11:30 [INFO   ] [SnowBraking.Master]   - Random Forest       : R²=-1.3201, MAE=0.5347
17:11:30 [INFO   ] [SnowBraking.Master]   - KNN Regressor       : R²=-1.5474, MAE=0.5902
17:11:30 [INFO   ] [SnowBraking.Master]   - Decision Tree       : R²=-2.6155, MAE=0.6692
17:11:30 [INFO   ] [SnowBraking.Master]   - Linear Regression   : R²=-1.2568, MAE=0.5440
17:11:30 [INFO   ] [SnowBraking.Master]   - SVR                 : R²=-2.6381, MAE=0.7179
17:11:30 [INFO   ] [SnowBraking.Master] [OK] Step 6: 머신러닝 보정 모델 학습 완료 (0.300s)
17:11:30 [INFO   ] [SnowBraking.Master] 실시간 보정 질의: 실측 25.00m -> 보정 24.50m (Δ=-0.50m)
17:11:31 [INFO   ] [SnowBraking.Engine] 데이터프레임 일괄 보정 완료: 60건 (신규 컬럼: 'char_brk_dist_corr')
17:11:31 [INFO   ] [SnowBraking.Master] 스펙별 보정 전/후 성능 비교 요약 표:
        Spec  Count  Raw_Mean(m)  Raw_Std(m)  Corr_Std(m)  Var_Reduction(%)
0  Comp_Base     20        23.34       0.441        0.438               1.4
1  Comp_Hard     20        23.13       0.485        0.481               1.7
2  Comp_Soft     20        23.35       0.468        0.469              -0.3
17:11:31 [INFO   ] [SnowBraking.Master] [OK] Step 7~8: 보정 질의 및 일괄 보정/스펙 분석 완료 (0.063s)
17:11:31 [INFO   ] [SnowBraking.Master] 
==========================================================
 [*] SnowPlatform_TestRunner 상태 요약 리포트
==========================================================
 1. 노면 계측 데이터: 20 행 (1개 시공간 스냅샷)
 2. 제동 평가 데이터 (제동 1회 단위): 60 행
 3. 기상 데이터 연동: 완료
 4. 노면 디지털 트윈 매칭: 완료
 5. 차분 보정 머신러닝 모델: ['Random Forest', 'KNN Regressor', 'Decision Tree', 'Linear Regression', 'SVR']
==========================================================
17:11:31 [INFO   ] [SnowBraking.Master] ============================================================
17:11:31 [SUCCESS] [SnowBraking.Master] SnowBrakingPerformance 통합 마스터 클래스 정상 작동 확인.
17:11:31 [INFO   ] [SnowBraking.Master] ============================================================
```

---

## 🔗 연관 문서 및 대시보드

* 📊 **[[00_2026_Snow_Surface_Characteristics_대시보드|2026 Snow Surface Characteristics 프로젝트 대시보드]]**
* 🧠 **[[30_Snow_제동성능보정_알고리즘|Snow제동성능보정 알고리즘 (2-Stage Architecture)]]**
* ❄️ **[[04_Resources/30_스노우_노면_공학/00_스노우_노면_공학_통합_색인|스노우 노면 공학 통합 지식 색인 (MOC)]]**
* 🧭 **[[Logger|unoUtil 통합 로깅 및 콘솔 모니터링 모듈 (LOGGER)]]**
* 🧠 **[[24_파이썬_로깅_엔진_원리와_실시간_성능_프로파일링_설계|파이썬 로깅 엔진 원리와 실시간 성능 프로파일링 설계]]**
