# 🧭 VBBParser VBOX Binary 포맷 브릿지 파서 매뉴얼 (vbb_parser.md)

## 📌 1. 개요 및 목적 (Overview)
`vbb_parser` 모듈은 Racelogic VBOX Binary 로그 포맷(`.vbb`, `.VBB`) 전용 브릿지 파서 엔지니어링 클래스(`VBBParser`)를 제공합니다.

VBOX 계측 파일 중 바이너리로 암호화되어 기록되는 `.vbb` 파일은 일반적인 텍스트 파서로 디코딩이 불가능합니다. 
본 모듈은 사내에 구축된 핵심 디코딩 엔진인 `VBBReader` 클래스와의 유기적인 연동을 조율하는 어댑터 브릿지 역할을 담당합니다. 멀티 채널 그룹을 고속으로 불러와 결측치 발생 시 시계열이 왜곡되지 않도록 **전방 전파 보간(`align_mode='ffill'`)**을 적용하고, 이종 장비 데이터 합성 시의 시간 축 정합 문제를 원천 해결해 줍니다.

---

## 🛠️ 2. 핵심 API 명세 (API Specifications)

### 2.1. `VBBParser` 클래스 인터페이스

| 메서드명 | 타입 | 설명 |
| :--- | :---: | :--- |
| `can_parse(file_path)` | `Method` | 파일 확장자가 `.vbb` 또는 `.VBB` 인지 감지하여 구동 여부 판단 (True/False 반환) |
| `parse(file_path, drop, align_mode)` | `Method` | `VBBReader`를 기동하여 암호화 바이너리를 디코딩하고 정렬 및 전방 보간이 완료된 Pandas DataFrame 반환 |

---

## 📋 3. 입력 파라미터 및 속성 상세 정의 (Arguments)

1. **`file_path` (`str` / `Path` - 필수)**:
   - 복구 및 파싱할 암호화 바이너리 `.vbb` 파일의 경로입니다.
2. **`drop` (`List[str]` / `None` - 선택, 기본값: `None`)**:
   - 연산 최적화를 위해 메모리에 로드하지 않고 버릴 무의미한 노이즈 채널 목록입니다.
3. **`align_mode` (`str` - 선택, 기본값: `'ffill'`)**:
   - VBOX 위성 통신 일시 끊김으로 인해 누락된 수치(NaN)를 전방 값으로 채우는 시간 동기화 보간 모드입니다. (`'ffill'`, `'bfill'`, 또는 보간 안 할 시 `None`)

---

## 💻 4. 실무 활용 예제 (Multi-case Examples)

### 4.1. [시나리오 1] 암호화 VBB 바이너리 파일 복구 및 Pandas 변환
```python
from unoUtil.file_reader.parsers.vbb_parser import VBBParser

# 바이너리 어댑터 파서 인스턴스화
vbb_parser = VBBParser()

vbb_path = "D:/test_data/session_wet_braking.vbb"

if vbb_parser.can_parse(vbb_path):
    # C-바이너리 스트림 연동을 통해 복구 및 파싱 집행
    df_raw = vbb_parser.parse(file_path=vbb_path)
    
    print(f"💾 바이너리 파싱 성공! Shape: {df_raw.shape}")
    print(f"🛰️ 복원된 위성 수신 채널 수: {len(df_raw.columns)}")
```

### 4.2. [시나리오 2] 특정 노이즈 채널 누락 및 전방 보간 결측치 채우기
```python
# 연산 부하를 줄이기 위해 무의미한 위성 고도 및 상태 플래그 채널 제외 로딩
unnecessary_channels = ['Height', 'Satellites', 'Status']

df_aligned = vbb_parser.parse(
    file_path=vbb_path,
    drop=unnecessary_channels,
    align_mode='ffill'  # 위성 일시 수신 이상 구간 전방 값 복사 보간 적용
)

print(f"✅ 정합 완료! 누락 채널 제외 확인: {not any(col in df_aligned.columns for col in unnecessary_channels)}")
```

### 4.3. [시나리오 3] 보간 없는 원시 데이터프레임 디코딩 (Raw Stream)
```python
# 결측치 보정이나 채우기 없이, 순수한 센서 끊김 유무를 분석하기 위해 원시 데이터 그대로 파싱
df_raw_stream = vbb_parser.parse(
    file_path=vbb_path,
    align_mode=None  # 결측치 보간 비활성화
)

nan_count = df_raw_stream['GPS_Speed'].isna().sum()
print(f"🛰️ GPS 일시 음영/수신불량 유실 프레임 수: {nan_count} frames")
```
