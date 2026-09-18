---
id: "vbb_reader"
title: "vbb_reader VBOX 바이너리(VBB) 고속 무손실 파싱 및 전원 차단 복구 엔진"
type: resource
category_main: 회사_업무
category_sub: unoUtil
aliases:
  - "VBBReader"
  - "vbb_reader"
  - "vbb_parser"
---

# 📖 VBBReader: VBOX 바이너리(VBB) 고속 무손실 파싱 및 전원 차단 복구 엔진 (`vbb_reader.py`)

## 1. 📌 개요
`VBBReader`는 영국 Racelogic 사의 **VBOX 계측기에서 생성되는 독점 바이너리 포맷인 `.vbb` 파일을 파싱하여 unoUtil 표준 데이터프레임으로 변환하는 핵심 엔진**입니다.

텍스트 기반 `.vbo` 파일 대비 약 60%의 용량 절감 효과를 갖는 바이너리 스트림을 다루며, 실차 시험 현장에서 빈번히 발생하는 **전원 급차단(Power Cut / Truncated File)** 상황에서도 VBOX Test Suite 소프트웨어와 동등한 수준으로 데이터를 안전하게 복구합니다.

---

## 2. ⚡ 핵심 아키텍처 및 개선 사항

### 2.1 전원 급차단(Power-cut) 3중 방어 메커니즘
실차 시험 중 차량 시동 꺼짐이나 케이블 탈락으로 파일 쓰기가 도중에 중단된 경우:
1. **바이너리 EOF 사전 검사**: `read_sample_group_locations`에서 마지막 샘플 그룹의 잔여 바이트가 `groupLength - 6`보다 작으면 불완전한 레코드를 버리고 즉시 안전 종료합니다.
2. **`None` 비교 예외 원천 차단**: 파일 말미에서 `read_vbb_value('u1')`가 `None`을 반환할 때 발생할 수 있는 `TypeError: '>=' not supported between 'NoneType' and 'int'`를 선제 방어합니다.
3. **손상 바이트 스킵 및 싱크 복원**: 알 수 없는 레코드 ID나 손상 바이트가 유입되어도 0x09 싱크 바이트를 능동 재탐색하여 유효 구간을 끝까지 추출합니다.

### 2.2 초고속 무손실 벡터 정합 (Vector Direct Assembly)
- **기존 병목**: 50여 개 채널 각각에 대해 개별 DataFrame을 생성하고 `pd.concat`으로 외부 조인 후 `.dropna()`를 수행하여 1.45초가 소요되었고, 채널 간 1~2샘플 시차로 인해 데이터가 유실되는 버그가 존재했습니다.
- **개선 알고리즘**:
  - 유효 채널들을 1회 순회하여 메타데이터와 타임스탬프를 수집.
  - 최다 샘플을 보유한 채널을 마스터 타임라인(Master Timeline)으로 지정.
  - 길이가 동일한 대다수 채널(90% 이상)은 메모리 직접 할당(Vector Packing)으로 0.001초 내 배치.
### 2.3 bytes 버퍼 직접 인덱싱 및 룩업 테이블(LUT) 기반 10.7배 파싱 가속
- **기존 병목**: `read_sample_group_locations()`에서 10만여 개 레코드를 순회할 때 매 샘플마다 파이썬 함수(`read_vbb_value`, `advance_through_file`) 호출과 딕셔너리 해시 조회가 약 60만 회 반복되어 2.5초 이상의 불필요한 인터프리터 오버헤드가 발생했습니다.
- **개선 알고리즘**:
  - `bytes` 버퍼 직접 참조(C-레벨 $O(1)$ 정수 인덱싱)로 파이썬 슬라이싱 및 함수 호출 오버헤드를 완전 제거.
  - 채널 그룹 정의 크기(256 슬롯)의 정수 룩업 테이블(LUT)을 미리 구축하여 딕셔너리 탐색 지연 제거.
  - 전원 급차단 방어 및 미정의 그룹 ID 회피 로직을 100% 동일하게 유지.
- **성능**: 9.5만~13.8만 행 기준 샘플 스캔 시간 **2.41초 $\rightarrow$ 0.22초 (10.75배 가속)**, VBB 전체 로딩 시간 **3.32초 $\rightarrow$ 1.1초대 (3배 이상 가속)**.

---

## 3. 🛠️ API 레퍼런스

### `VBBReader` Class
```python
from unoUtil.fileDataReader.vbbTopython.VBBReader import VBBReader

reader = VBBReader()
reader.read_vbb_file("path/to/sample.VBB")
result = reader.get_dict_uno_data(drop=True)
```

#### `get_dict_uno_data(drop=False, align_mode="ffill") -> Optional[dict]`
- **설명**: 파싱된 바이너리 채널 데이터를 단일 표준 데이터프레임으로 결합하고 메타데이터를 추출합니다.
- **매개변수**:
  - `drop` (bool): `Timestamp(s)` 기준 시간 컬럼을 최종 DataFrame에서 제거할지 여부. 기본값 `False`.
  - `align_mode` (str): 샘플 길이 차이 보정 방식. `'ffill'`(직전값 유지/후방보강, 무손실 복원) 또는 `'none'`.
- **반환값** (`dict`):
  - `'data'` (`pd.DataFrame`): 시간축 정합이 완료된 다채널 센서 데이터프레임.
  - `'saveDate'` (`datetime` or `None`): VBOX 기록 시작 일시.
  - `'samplingRate'` (`float`): 동적 산출된 주 샘플링 주파수 (Hz 단위, 예: 100.0).

---

## 4. 🧪 자가 검증 결과 (`__main__`)

`VBBReader.py` 하단의 `# region` 자가 검증 스위트를 통해 다음 항목이 100% 검증되었습니다:
- **Case 1 (실차 정상 파일)**: 137,953행 $\times$ 51채널 로딩 성공, 결측치(NaN) 0개, 100.0 Hz 동적 산출.
- **Case 2 (전원 급차단 시뮬레이션)**: 파일 끝 17바이트를 임의 절단한 불완전 VBB 파일에 대해서도 크래시 없이 137,953행 전체 안전 복구 확인.
- **연계 호환성**: `FileDataReader` 및 `VT_ACCBRK` 제동 평가 파이프라인(8개 세션 탐색 및 6개 유효 랩 산출) 연동 100% 무결점 통과.

---

## 5. 🔗 관련 문서 및 영구 도메인 지식
- [[21_바이너리_파일_IO_및_VBB_데이터_포맷_구조]] : 바이너리 파일 I/O 아키텍처 및 VBB 포맷 심층 분석
- [[20_VBOX_계측_데이터_규격_및_GPS좌표계]] : VBO vs VBB 바이너리 구조 및 서경 부호/전원 차단 복구 이론
- [[00_unoUtil_모듈개발_대시보드]] : unoUtil 모듈 개발 현황 대시보드
- [[FileDataReader]] : 차세대 객체지향 통합 데이터 로딩 인터페이스
- [[ReadDataFile]] : 레거시 통합 데이터 로딩 인터페이스
