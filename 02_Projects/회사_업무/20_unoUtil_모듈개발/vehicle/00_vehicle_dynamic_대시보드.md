# 🏎️ unoUtil 실차 주행 동역학 및 조종안정성 도메인 대시보드 (vehicle_dynamic)

이 문서는 실차 주행 시험(조종안정성, 핸들링, 주행 동역학)에서 발생하는 센서 계측 데이터의 좌표계 변환, 회전 운동역학(Roll/Pitch/Yaw) 보정, 슬립각 및 하중 이동 연산, 컨트롤 타이어 대비 상대 성능 지수(Index) 산출, 그리고 조종안정성 비선형 커브피팅(Random Forest / Magic Formula)을 전담하는 `unoUtil.vehicle` 도메인의 마스터 MOC(Map of Content) 대시보드입니다.

---

## 📜 버전 이력 및 주요 개발 현황 (Changelog)

| 날짜 (Date) | 커밋 / 버전 | 변경 유형 | 작업 내역 및 아키텍처 개선 사항 | 상태 |
| :---: | :---: | :---: | :--- | :---: |
| **2026-09-28** | `b1a0eb3`<br/>`ab1132e`<br/>(`v3.2`) | `Feature & Docs` | **`vehicle` 도메인 4대 핵심 모듈 8대 동사 전면 표준화 및 원격 푸시 완결**<br>• `VehicleDynamic`: 좌표 정렬(`align_coordinate`), 회전 운동역학(`rotate_kinematics`), 원점 회전(`rotate_origin`), 센서 위치간 보간(`calc_p2p_inter_coordinate`), 슬립각(`calc_side_slip_angle`, `calc_slip_angle_fr`), 종하중이동(`calc_load_transfer_longitudinal`) 등 8대 표준 동사 선언 및 단일 클래스 캡슐화 완료<br>• `analysis_test_data`: `calc_performance`, `calc_compare`, `make_performance_df`, `make_compare_df` 표준화, LOGGER 적용 완료<br>• `hndl_test`: `calc_curvefit_rf`, `calc_curvefit_mf` 표준화, 비차단 시각화 저장 및 자가 구동 3-시나리오 검증<br>• `test_infor_res`: `TestInformation`, `TestResult` 데이터 클래스화 및 메타데이터 정합<br>• `vehicle/__init__.py`: v1 오리지널 레거시 브릿지(`_AnalysisTestData_`, `_HndlTest_`, `_TEST_INFOR_RES_`, `_BRKTest_`) 바인딩 완료<br>• 1:1 매뉴얼 4종 최신 사양 갱신 및 `00_vehicle_dynamic_대시보드.md` 신설 | **완료 (PASS)** |
| **2026-09-26** | `v2.9` | `Architecture` | **`VehicleDynamic` 단일 표준 클래스 캡슐화 및 Single Baseline Law 확립**<br>• 과도기적 미완성 코드의 별칭/브릿지 양산 원천 배제, v1 오리지널 레거시 단일 기준 호환 원칙 정립<br>• 외부 실차 로그 의존성 없는 3-시나리오 자립형 Mock 테스트 스위트 구축 | **완료** |

---

## 🧭 1. 도메인 아키텍처 및 파이프라인 (Architecture)

```mermaid
flowchart TD
    Raw["📁 실차 주행 센서 원시 시계열<br/>(가속도계, 자이로, GPS, 차속, 휠속, 조향각)"] --> VD["VehicleDynamic<br/>[차량 동역학 물리 연산 타워]"]

    subgraph Kinematics_Pipeline [1. 좌표계 정렬 및 운동역학 보정 파이프라인]
        VD --> AC["align_coordinate()<br/>(센서 장착각 교정 & ISO 차량 좌표계 정렬)"]
        AC --> RK["rotate_kinematics()<br/>(Roll/Pitch/Yaw 3축 오일러 회전 보정)"]
        RK --> SSA["calc_side_slip_angle() & calc_slip_angle_fr()<br/>(차체 횡슬립각 β 및 전/후륜 타이어 슬립각 α_f, α_r)"]
        SSA --> LT["calc_load_transfer_longitudinal()<br/>(가감속 피칭에 따른 전후륜 수직하중 이동량 ΔF_z)"]
    end

    subgraph Handling_Fitting [2. 조종안정성 특성 모델링 (hndl_test)]
        SSA --> HNDL["hndl_test (handling_test)"]
        HNDL --> RF["calc_curvefit_rf()<br/>(Random Forest 기반 횡가속도-슬립각 비선형 피팅)"]
        HNDL --> MF["calc_curvefit_mf()<br/>(Pacejka Magic Formula 기반 정상상태 특성 모델링)"]
    end

    subgraph Relative_Performance [3. 상대 성능 지수 평가 (analysis_test_data)]
        RF & MF --> ATD["analysis_test_data"]
        ATD --> CP["calc_performance()<br/>(Control 타이어 대비 Spec/시험 타이어 상대 지수화)"]
        ATD --> CC["calc_compare()<br/>(다차원 핸들링 성능 비교 매트릭스 도출)"]
    end

    subgraph Metadata_Capsule [4. 시험 조건 및 결과 캡슐 (test_infor_res)]
        CP & CC --> TI["TestInformation & TestResult<br/>(시험 환경, 노면 조건, 공기압, 타이어 메타데이터)"]
    end
```

---

## 📚 2. 서브모듈 상세 명세 및 1:1 매뉴얼 링크

| 모듈 | 핵심 클래스 / 함수 | 주요 기능 및 역할 | 1:1 기술 매뉴얼 |
| :--- | :--- | :--- | :---: |
| **`vehicle_dynamic`** | `VehicleDynamic`, `align_coordinate`, `rotate_kinematics`, `calc_side_slip_angle` | 센서 좌표 정렬, 3축 오일러 회전역학, 차체 및 전후륜 슬립각, 수직하중 이동 산출 | [[vehicle_dynamic|기술 문서]] |
| **`analysis_test_data`** | `calc_performance`, `calc_compare`, `make_performance_df` | 컨트롤(기준) 타이어 대비 시험 타이어 상대 성능 지수(Index 100 기준) 산출 및 비교 | [[analysis_test_data|기술 문서]] |
| **`hndl_test`** | `calc_curvefit_rf`, `calc_curvefit_mf` | Random Forest 머신러닝 및 Pacejka Magic Formula 기반 조종안정성 비선형 커브피팅 | [[hndl_test|기술 문서]] |
| **`test_infor_res`** | `TestInformation`, `TestResult` | 실차 주행 시험 환경 메타데이터(시험일시, 노면, 기상, 공기압) 및 분석 결과 캡슐화 | [[test_infor_res|기술 문서]] |
| **`acc_brk`** | `VTAccBrk`, `VTAccBrkTire`, `VTAccBrkProject` | 실차 가감속 및 제동 성능(ABS, 제동거리, MFDD) 종합 분석 서브시스템 | [[vehicle/acc_brk/00_vt_acc_brk_대시보드|ACCBRK 대시보드]] |

---

## 🚀 3. 핵심 사용법 및 워크플로우 (Quick Start)

### 3.1. 차량 동역학 좌표 정렬 및 슬립각 연산

```python
import numpy as np
import pandas as pd
from unoUtil.vehicle import VehicleDynamic, align_coordinate, calc_side_slip_angle

# 1. 원시 계측 신호 준비
df = pd.DataFrame({
    'Time': np.linspace(0, 10, 1000),
    'vx': np.full(1000, 27.78),  # 100 km/h (m/s)
    'vy': np.random.normal(0, 0.2, 1000),
    'yaw_rate': np.random.normal(0, 0.05, 1000),
    'ax': np.random.normal(0, 0.1, 1000),
    'ay': np.random.normal(0, 0.2, 1000),
})

# 2. 센서 장착각 오차 좌표 정렬 (8대 표준 동사)
df_aligned = align_coordinate(df, col_ax='ax', col_ay='ay', pitch_deg=0.5, roll_deg=0.2)

# 3. 차체 횡슬립각(Beta) 산출
beta_deg = calc_side_slip_angle(vx=df_aligned['vx'], vy=df_aligned['vy'])
print(f"최대 횡슬립각: {np.nanmax(np.abs(beta_deg)):.2f} deg")
```

### 3.2. 컨트롤 타이어 대비 상대 성능 지수 산출

```python
from unoUtil.vehicle import calc_performance, calc_compare

# 시험 결과 딕셔너리 구성 (Control vs Target)
df_res = pd.DataFrame({
    'Tire': ['Control', 'Pattern_A', 'Pattern_B'],
    'Stopping_Distance': [38.5, 37.2, 39.1],  # 낮을수록 우수 (lower_is_better)
    'Lateral_G': [0.92, 0.98, 0.90]           # 높을수록 우수 (higher_is_better)
})

# 상대 성능 지수 산출 (Control = 100 기준)
df_perf = calc_performance(
    df_res,
    col_control='Control',
    metrics={'Stopping_Distance': False, 'Lateral_G': True}
)
print(df_perf)
```

---
**Last Updated**: 2026-09-28  
**Standard**: unoUtil Clean Architecture v2.0 & Single Baseline Law
