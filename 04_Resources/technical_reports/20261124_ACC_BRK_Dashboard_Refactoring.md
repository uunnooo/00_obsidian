# [마스터 기술 명세] ACC/BRK 대시보드 UI 컴포넌트 아키텍처 (v4.34 - 확장판)

## 1. 개요
본 문서는 대시보드 UI 시스템의 전수 조사에 기반한 계층 구조를 정의합니다. 모든 UI 요소는 Tier 체계에 따라 디자인 시스템을 상속받으며, `components.py`, `ui.py`, `theme.py` 내의 표준화된 인터페이스를 통해 제어됩니다.

## 2. 포괄적 UI 컴포넌트 계층 상세 매트릭스

| 기능 영역 | UI 컴포넌트 타입 | Tier | 단계 | 제어 파라미터 및 CSS 규격 | 구현 전략 및 위치 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **폼 입력** | `st.text_input`, `st.number_input` | 1 | 1 | `h:42px`, `bg:#030814`, 입체 슬레이트 보더 | 전역 CSS 토큰 기반 모델(`theme.py`) |
| **선택 입력** | `st.selectbox` | 1 | 1 | `h:42px`, `bg:#030814`, 1차 자손 타겟팅 정밀 정렬 | BaseWeb 스타일 오버라이드(`theme.py`) |
| **핵심 버튼** | `st.button`, `st.form_submit_button` | 1 | 1 | `h:42px`, `bg:#0c284e`, `border:#38BDF8`, 네온 글로우 | 사각 테크 뱃지 표준(`components.py`) |
| **복합 제어** | `st.multiselect` | 2 | 2 | `h:auto`, `min-h:42px`, 태그 칩 네온 사파이어 | 태그 레이아웃 가변 확장 엔진(`components.py`) |
| **데이터 관리** | `st.data_editor` (상세 테이블) | 2 | 2 | `bg:#0B1321`, `row_hover:#142035`, 1:1 무결성 복원 | 편집 상태 실시간 동기화(`engine.py`) |
| **상태 제어** | `st.toggle` / `st.checkbox` | 2 | 2 | `active: #A3FF12` (Neon Lime), 슬레이트 톤 | 불리언 네온 색상 맵핑(`theme.py`) |
| **도구 뷰어** | `st.button` (확대/저장 툴바) | 3 | 3 | `132x38px`, 딥 사파이어, 네온 시안 호버 | 탭별 인스턴스 강제 오버라이드(`ui.py`) |
| **그래픽 시각화** | `st.image`, `st.plotly_chart` | 3 | 3 | 1:1비율 고정, 줌/팬 이벤트 실시간 감지 | 캡션 연동 타이틀 자동화(`components.py`) |
| **상태 피드백** | `st.spinner`, `st.toast` | 1 | 3 | 네온 라임 회전 바, 성공/경고 아이콘 매핑 | 작업 상태 머신 연동(`theme.py` 토스트 뱃지) |
| **컨테이너** | `st.container`, `st.columns` | 1 | 1 | 5열 마스터 그리드(20% 균등), flex-grow:0 고정 | CSS Flex-box 기반 강제 수직/수평 칼 정렬 |

## 3. UI 계층화 및 구현 전략 상세

### 3.1 Tier 상세 정의
- **Tier 1 (시스템 기본)**: 대시보드의 전역 Look & Feel을 결정합니다. 모든 폼 컨트롤(Input, Select, Button)은 `components.py`의 `render` 함수군과 `theme.py`의 CSS f-string 템플릿을 통해 일괄 제어됩니다.
- **Tier 2 (도메인 기능)**: 데이터와 복합적으로 상호작용합니다. `MultiSelect`는 태그 칩을, `DataEditor`는 편집 로직을, `Toggle`은 상태 머신을 처리하며, 이들은 `engine.py`의 데이터 처리 로직과 실시간 연동됩니다.
- **Tier 3 (문맥/특수 UI)**: 탭별 특수 툴바(새창 뷰어, 확대 버튼, 저장 툴), 시각화 피규어 타이틀, 그리고 로딩/상태 피드백(Spinner) 등 사용자 인터랙션을 완결 짓는 도메인 특화 요소입니다.

### 3.2 핵심 모듈 연계 (The Architecture Flow)
1. **정의(`theme.py`)**: 디자인 시스템 토큰(CSS, 색상, 애니메이션) 선언.
2. **구현(`components.py`, `ui.py`)**: Tier별 원자 단위 컴포넌트(렌더링 함수) 정의.
3. **조립(`tabs/`)**: `engine.py`에서 계산된 데이터를 Tier 1/2/3 컴포넌트들과 결합하여 탭별 뷰 완성.
4. **통제(`dashboard_app.py`)**: 위 모든 모듈을 `sys.modules` 및 `session_state` 기반으로 유기적으로 구동 및 핫 리로드 제어.
