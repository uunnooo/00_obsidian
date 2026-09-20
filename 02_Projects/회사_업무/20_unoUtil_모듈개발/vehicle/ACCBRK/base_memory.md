# 🧭 BaseMemory / AN_MEMORY 최상위 기반 클래스 매뉴얼 (base_memory.md)

## 📌 1. 개요 및 목적 (Overview)
`base_memory` 모듈은 실차 가감속 및 제동 시험 데이터를 다루는 모든 하위 물리 분석 서브패키지들(Acceleration, Mu-Drop, Response, Skewness, Slip PDF, Split Speed 등)의 **RAM(메모리) 누수 차단, 저장 용량 다이어트, 피클 직렬화 호환 및 캐시 온디맨드 복원**을 총괄하는 가상 최상위 기반 클래스 (`BaseMemory` / `AN_MEMORY`)를 정의합니다.

대용량 100Hz 이상 실차 계측 데이터프레임을 입체적으로 가공하다 보면 RAM 메모리가 급격히 누적되어 프로세스가 다운되는 크래시가 유발될 수 있습니다. 
본 모듈은 자주 쓰이는 대용량 연산 결과를 '메모이제이션(메모리 캐싱)'하되 파일 저장 시에는 자동으로 소거하는 라이프사이클을 안전하게 구현하였으며, 상위 인스턴스인 `VT_ACCBRK_TIRE`를 **약한 참조(weakref)**로 결속하여 순환 참조로 인한 메모리 누수를 원천적으로 방지합니다.

---

## 🛠️ 2. 핵심 API 명세 (API Specifications)

### 2.1. `BaseMemory` (구 `AN_MEMORY`) 클래스 인터페이스

| 메서드 / 속성 | 타입 | 설명 |
| :--- | :---: | :--- |
| `target_attr_list` | `List[str]` | 클래스 변수. 피클링 시 대용량을 날려버릴 타겟 변수명 리스트 (기본값: `['df', 'summary']`) |
| `__init__(obj_tire, **kwargs)` | 생성자 | 부모 타이어 인스턴스를 약한 참조로 안전 결속하고 서브 모듈 이름과 디버그 플래그 지정 |
| `test` | `property` | 부모 객체 접근 안전 통로. 부모 객체 소멸 시 `ReferenceError`를 예쁘게 던짐 |
| `clear_cache()` | 메서드 | RAM 점유율을 즉시 회수하기 위해 대용량 메모리 캐시를 강제로 비우고 `None` 처리 |
| `restore_cache()` | 메서드 | 온디맨드 복원을 수동으로 강제 기동하여 캐시 데이터를 메모리 위에 다시 빌드 |
| `has_active_cache(name)` | 메서드 | 연산 복원 동작(analysis)을 깨우지 않고 쥐 죽은 듯이 캐시 적재 유무만 True/False 판별 |
| `__getstate__()` | 특수 메서드 | 피클 파일 저장 시 호출되어 대용량 변수를 날리고 weakref를 임시 강한 참조로 해제하여 포장 |
| `__setstate__(state)` | 특수 메서드 | 피클 로드 시 호출되어 레거시 속성을 복원하고 부모 인스턴스를 다시 안전한 `weakref`로 재바인딩 |

---

## 📋 3. 입력 파라미터 및 속성 상세 정의 (Arguments)

1. **`obj_tire` (`Any` - 필수)**: 
   - 자식 분석 모듈을 생성할 때 전달하는 상위 `VT_ACCBRK_TIRE` 인스턴스입니다.
   - 내부 변수 `_test_ref` 에 `weakref.ref(obj_tire)` 로 바인딩되어 메모리 소멸(가비지 컬렉터) 시 자동으로 RAM에서 가비지 수집되도록 통제합니다.
2. **`**kwargs` (선택)**:
   - `name` (`str` - 기본값 `None`): 서브 모듈을 식별하기 위한 문자열 명칭 (예: `'Acceleration'`).
   - `print` (`bool` - 기본값 `False`): 콘솔 디버그 로그 출력 여부를 나타내는 플래그.

---

## 💻 4. 실무 활용 예제 (Multi-case Examples)

### 4.1. [시나리오 1] 자식 분석 모듈 상속 및 약한 참조 기반 부모 안전 접근
```python
import pandas as pd
from unoUtil.vehicle.ACCBRK.base_memory import BaseMemory

class MyCustomAnalyzer(BaseMemory):
    # 피클 저장 시 다이어트할 변수명 지정 (backing field는 앞에 밑줄이 붙은 '_df', '_summary'가 됨)
    target_attr_list = ['df', 'summary']
    
    def __init__(self, obj_tire):
        # 상위 생성자에 부모 타이어 객체 전달 및 모듈명 지정
        super().__init__(obj_tire, name='CustomAnalyzer', print=True)
        self._df = None
        self._summary = None
        
    @property
    def df(self):
        # 데이터가 비어있을 때만 온디맨드 복원 연산 가동!
        if self._df is None:
            # self.test 프로퍼티를 통해 부모 타이어 인스턴스의 정보에 메모리 안전하게 접근
            tire_set_name = self.test.information.set
            print(f"[{self.name}] {tire_set_name} 원본 데이터로 고속 연산 수행 중...")
            self._df = pd.DataFrame({'Velocity': [100, 50, 0]})
        return self._df
```

### 4.2. [시나리오 2] 온디맨드 수동 캐시 소거 및 복원 제어
```python
# 가상의 모의 테스트
parent_tire = MockTireInstance()
analyzer = MyCustomAnalyzer(parent_tire)

# 1. 속성 호출 시 온디맨드로 데이터가 살아납니다.
data_df = analyzer.df  # [CustomAnalyzer] Test_Tire 원본 데이터로 고속 연산 수행 중...

# 2. 대량 시뮬레이션 직후 RAM을 비우기 위해 수동으로 강제 소거합니다.
analyzer.clear_cache()
print(analyzer.has_active_cache('_df'))  # Output: False (연산을 방해하지 않고 쥐죽은 듯 유무만 검사)

# 3. 백그라운드 수동 캐시 복원을 강제 기동합니다.
analyzer.restore_cache()
print(analyzer.has_active_cache('_df'))  # Output: True (자동으로 @property를 호출하여 복원됨)
```

### 4.3. [시나리오 3] 피클 직렬화 저장 용량 다이어트 및 레거시 복원
```python
import pickle

# analyzer.df가 수백 MB의 대용량 데이터를 메모리에 쥐고 있다고 가상
_ = analyzer.df

# 피클 덤프 시 내부적으로 __getstate__가 기동되어 대용량 변수를 None으로 비우고,
# 피클 포장지 내부 용량을 단 수십 KB 수준의 초경량 팩으로 바꿉니다.
serialized_bytes = pickle.dumps(analyzer)
print(f"저장용 파일 용량: {len(serialized_bytes):,} bytes (다이어트 완료)")

# 피클 로드 시 내부적으로 __setstate__가 기동되어,
# 구버전 피클 속성을 신규 비공개 필드로 자동 복원하고 이중 weakref를 차단하는 재설정이 완결됩니다.
loaded_analyzer = pickle.loads(serialized_bytes)
print(f"로드된 분석기 명칭: {loaded_analyzer.name}")
print(f"로드 직후 캐시 상태: {loaded_analyzer.has_active_cache('_df')}")  # Output: False (초경량 복원 성공!)
```
