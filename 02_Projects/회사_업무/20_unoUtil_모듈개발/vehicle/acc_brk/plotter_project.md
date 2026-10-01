#### 4단 백틱 규칙에 따라 문서 전체를 하나의 블록으로 제공합니다.

# 📊 PLOTTER_PROJECT: 다중 타이어 비교 분석 시각화 엔진

**PLOTTER_PROJECT**는 프로젝트 단위로 수집된 여러 타이어의 성능 데이터를 통합하여, 타이어 간의 상대적 우위와 물리적 거동 차이를 한눈에 파악할 수 있도록 설계된 **전문 비교 시각화 라이브러리**입니다.

---

## 🏛️ 시스템 아키텍처 (Architecture Flow)

이 모듈은 대규모 프로젝트 데이터를 실무자 관점에서 직관적으로 재구성하기 위해 3단계 시각화 전략을 채택합니다.

### Layer 1. DATA FILTERING (데이터 정제 및 필터링)
* **목적**: 프로젝트 전체 데이터 중 시각화에 적합한 대표값 및 보정값만 선별합니다.
* **주요 작업**: 
    - `mask_summary`를 통해 중복된 콘트롤 타이어 데이터를 제거하고 유니크한 타이어 셋만 추출합니다.
    - `mask_ref_tire`를 참조하여 기준(Control) 타이어를 시각적으로 강조(회색 처리 등)할 준비를 합니다.

### Layer 2. LOGIC LAYOUT (비교 로직 설계)
* **목적**: 절대 수치(m, g)와 상대 지수(%)를 결합하여 입체적인 분석 틀을 제공합니다.
* **주요 작업**:
    - **병렬 배치**: 실측 제동거리와 성능 지수를 1x2 축에 나란히 배치하여 분석의 다각화를 꾀합니다.
    - **스택 분석**: 제동 성능을 고속/저속 구간으로 분리(Split)하여 각 타이어가 강점을 보이는 영역을 파악합니다.

### Layer 3. ADVANCED RENDERING (고급 시각화 및 리포팅)
* **목적**: IT 매거진 수준의 고해상도 리포트용 그래프를 생성합니다.
* **주요 작업**:
    - **Ridgeline Plot**: 슬립 분포를 산맥 형태로 쌓아 올려 타이어 간의 거동 안정성을 비교합니다.
    - **Rectangle Annotation**: 가속 트렌드 차트에 사각형 마커를 입혀 특정 속도 대역의 가속력을 강조합니다.



---

## 🪄 핵심 키워드 및 공통 옵션 (Global Options)

| 키워드 | 용도 | 기본값 | 비고 |
| :--- | :--- | :--- | :--- |
| `col_tire` | 타이어 식별 컬럼명 | `'TestTireSet'` | X/Y축 레이블로 활용될 그룹 기준 |
| `ax` | 외부 Axes 전달 | `None` | 사용자가 정의한 Layout에 그래프를 삽입할 때 사용 |
| `width` | 바 차트 너비 | `0.4` or `0.6` | 그래프의 밀도 조절 (가독성 관련) |
| `cmap` | 컬러맵 설정 | `'tab10'` | 타이어별 색상 구분 테마 |

---

## 📖 주요 함수 상세 가이드

### ### 1. `compare_braking` (제동 성능 통합 비교)
* 💡 **기능 (Pain Point Killer)**: "보정 전후 수치가 얼마나 다른가?" 그리고 "기준 대비 몇 % 좋아졌는가?"라는 질문에 동시에 답합니다. 실측값(Measured)과 보정값(Corrected)을 나란히 배치하여 분석의 신뢰성을 보여줍니다.
* ⚙️ **모듈 전용 키워드**: `col_dist` (기준이 되는 제동 거리 컬럼 지정).
* 🎨 **추천 스타일 키워드**: `Corrected`는 주황색, `Measured`는 회색으로 고정되어 시각적 대비를 극대화합니다.
* 📚 **데이터 해석 팁**: 우측 지수(Index) 차트에서 100% 라인(Red Line)보다 바가 길면 기준 타이어보다 제동 성능이 우수함을 의미합니다.

### ### 2. `compare_acceleration` (가속도 트렌드 맵)
* 💡 **기능 (Pain Point Killer)**: 속도 대역별로 타이어 성능이 역전되는 구간을 포착합니다. 단순히 점을 찍는 것이 아니라 **Rectangle Bar**를 사용하여 특정 속도 구간의 가속 성능을 영역으로 표현합니다.
* ⚙️ **모듈 전용 키워드**: 숫자를 자동 추출하여 고속에서 저속 순으로 X축을 정렬합니다.
* 📚 **데이터 해석 팁**: 라인이 교차하는 지점을 확인하세요. 고속에서는 강하지만 저속에서 힘이 빠지는 타이어 등 세부적인 특성 파악이 가능합니다.


### ### 3. `compare_slip_pdf` (슬립 분포 Ridgeline)
* 💡 **기능 (Pain Point Killer)**: 여러 타이어의 슬립 특성을 한 축에 그리면 겹쳐서 보기 힘듭니다. 이 함수는 산맥 모양의 **Ridgeline Plot**을 사용하여 각 타이어의 슬립 밀도를 층층이 쌓아 올려 비교합니다.
* ⚙️ **모듈 전용 키워드**: `h` (겹침 정도 조절), `xlim` (슬립 영역 제한).
* 🎨 **추천 스타일 키워드**: 최빈값(Mode)과 평균(Mean) 가이드라인이 자동으로 그려져 분포의 편향성을 즉시 확인할 수 있습니다.
* 📚 **데이터 해석 팁**: 분포가 왼쪽으로 좁게 형성될수록 슬립이 적고 안정적인 타이어입니다.


---

## 🛡️ 실무자를 위한 퀵 가이드 및 안전망

> **[실무 안전망 안내]**
> * **자동 컬럼 탐색**: `corr_`, `index_` 등 접두사가 붙은 보정 컬럼을 시스템이 알아서 찾아 매칭하므로, 사용자가 복잡한 컬럼명을 외울 필요가 없습니다.
> * **Control 타이어 강조**: 보정의 기준이 된 타이어는 항상 회색(`grey`)으로 표시되어, 어떤 타이어가 성능 비교의 기준점인지 직관적으로 알 수 있습니다.
> * **레이아웃 보호**: `_make_format_fig_kwargs`가 내부에서 작동하여, 다중 그래프 생성 시 전체 타이틀(Suptitle)이 중복으로 찍혀 지저분해지는 현상을 원천 차단합니다.

### 🎯 시각화 목적별 함수 매칭 테이블
| 시각화 목적 | 사용 함수 | 주요 시각화 요소 |
| :--- | :--- | :--- |
| **보정 전/후 제동거리 비교** | `compare_braking()` | Measured vs Corrected 병렬 바 |
| **타이어별 상대 성능 순위 확인** | `compare_index_braking()` | 거리 수치가 포함된 단일 지수 바 |
| **고속/저속 제동 기여도 분석** | `compare_split_distance()` | Stacked Bar (Salmon/Seagreen) |
| **타이어별 슬립 제어 특성 비교** | `compare_slip_pdf()` | Ridgeline & Overlay PDF |
| **환경 변화에 대한 강건성 평가** | `compare_mudrop_dist()` | Mu-Drop 손실 거리 분리 표기 |

---

## 🛠️ 5. PlotterProject 클래스 인터페이스 및 메서드 명세 (No Redundant Prefix)

`PlotterProject` 클래스는 프로젝트 내 다중 타이어 간 성능 비교 시각화를 전담하는 엔진입니다.

| 메서드명 | 비교 대상(목적어) | 설명 |
| :--- | :--- | :--- |
| `__init__(project, level=None, **kwargs)` | 생성자 | 부모 프로젝트 인스턴스 바인딩 및 로깅 레벨 설정 (부모 `project.level` 상속) |
| `all(save=None, excel=None, html=False, close=True, level=None)` | 통합 비교 전체 | 8대 프로젝트 비교 그래프 일괄 렌더링 및 저장 |
| `compare_braking(...)` | 제동 성능 비교 | 보정 전/후 제동거리 및 상대 지수(%) 병렬 비교 바 차트 |
| `compare_acceleration(...)` | 가속도 트렌드 | 속도 대역별 가속도 트렌드 및 역전 구간 비교 |
| `compare_split_distance(...)` | 분할 제동거리 | 고속/저속 구간별 제동 기여도 스택 바 차트 |
| `compare_split_acceleration(...)` | 분할 감속도 | 속도 대역 분할 감속도 지수 비교 |
| `compare_slip_pdf(...)` | 슬립 분포 산맥도 | 4륜 슬립률 확률밀도함수(PDF) Ridgeline 비교 |
| `compare_mudrop_dist(...)` | 뮤드롭 손실 거리 | 수막현상 마찰 급감에 따른 손실 거리 비교 |
| `compare_slip_mode_skewness(...)` | 슬립 모드 왜도 | 2D 슬립 지형도 및 왜도 지표 비교 |
| `compare_response(...)` | 제동 응답성 비교 | 초기 제동 반응 지연 시간 및 기울기 비교 |

---

## 💻 실무 밀착형 종합 예제 코드

```python
import logging
from unoUtil.vehicle.acc_brk import VTAccBrkProject

# 1. 프로젝트 객체 생성 및 타이어 등록 (로거 레벨 지정)
pjt = VTAccBrkProject(name="PJT_SUMMER_TEST", level=logging.INFO)
pjt.add_tire(t_c1)
pjt.add_tire(t_t1)
pjt.add_tire(t_c2)

# 2. 성능 보정 연산 수행
pjt.correct_performance()

# 3. 8대 통합 비교 리포트 일괄 출력 (No Redundant Prefix: pjt.plot.all())
pjt.plot.all(save="./plots_project", level=logging.INFO)

# 4. 개별 특화 비교 그래프 단독 생성
fig_brk = pjt.plot.compare_braking()
fig_ridge = pjt.plot.compare_slip_pdf(xlim=(0, 20), h=-0.6)
```

**Documented by your Coding Partner & Technical Writer, uno.**