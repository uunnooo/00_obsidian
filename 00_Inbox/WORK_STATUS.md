# 📋 unoUtil 작업 진행 현황 및 무결성 검증 일지 (WORK_STATUS)

- **작성 일시**: 2026-10-12 18:10:00 (KST)
- **작업자**: uno & Gemini (Antigravity)
- **작업 브랜치**: `refactor-v2`
- **목표 버전**: `unoUtil v3.24`
- **핵심 작업 도메인**: 
  - `unoUtil.vehicle.acc_brk` (가감속 및 실차 제동 분석)
  - `unoUtil.file_reader` (이기종 계측 데이터 파일 리더 및 Datetime 시계열 헬퍼)

---

## 🎯 1. 오늘 주요 작업 및 결함 수정 요약 (Changelog)

### ① VBOX GPS 시간 파싱 및 타임존 계산 결함 원천 해결 (`datetime_helper.py`, `file_data_reader.py`)
- **문제점 규명**:
  - `07_C2.VBO` 파일 내부 GPS 원시 시각은 `053648.720` (UTC 05시 36분 48.72초)로, 한국 시각(+9h) 환산 시 **14시 36분 48초**가 되어야 함.
  - 그러나 Pandas가 수치(float)로 읽으면서 앞의 0이 제거되어 `53648.72`가 되었고, 기존 로직에서 `zfill(6)`을 수행하지 않고 앞 2자리(`str_val[:2] = "53"`)를 시간으로 검증함에 따라 `53 < 24` 조건이 **False**가 되어 VBOX 포맷 판정에서 탈락함.
  - VBOX 판정 탈락으로 인해 초 단위(Seconds since midnight)로 오판되어 `53648.72초`($\approx 14$시간 54분)에 타임존 +9시간이 더해져 **23시 54분 08초**라는 엉뚱한 심야 시각이 생성됨. (마찬가지로 `01_C1.VBO`의 `005056.980`도 `5056.98` 길이 4로 인해 탈락)
- **개선 조치**:
  - `datetime_helper.resolve_base_time`에서 정수부 문자열을 반드시 **`str_val.zfill(6)`**을 거치도록 수정하여 `053648` $\to$ `H=05, M=36, S=48`로 완벽 분해.
  - 파일 확장자(`.vbo`, `.vbb`) 및 VBOX 고유 컬럼(`sats`, `velocity`, `vert-vel` 등) 감지 로직을 추가하여 VBOX 표준 규격(`HHMMSS.sss`)을 100% 식별.
  - `01_C1.VBO` (09:50:56), `02_T1.VBO` (10:25:11), `07_C2.VBO` (14:36:48)로 한국 표준시 기준 완벽 정상화.

### ② 타임존 오프셋 가산 및 자정 통과 시 일자(`Day`) 자동 롤오버 보존
- **타임존 오프셋 가산 시**:
  - 야간 시험(예: UTC 20시) 시 한국 시간(+9h) 가산 시 파이썬 `datetime.timedelta(hours=final_offset)` 연산으로 익일 새벽 05시로 날짜가 자동으로 1일 증가.
  - `resolve_base_time`에 `return_datetime=True` 옵션을 신설하고 `FileDataReader.add_datetime`에서 보정된 날짜를 온전히 수신하여 `self.save_date` 및 `Datetime` 컬럼에 보존.
- **단일 주행 중 자정 통과 시**:
  - `build_datetime_series`의 Pandas C-엔진 `pd.date_range` 타임스탬프 누적 방식을 통해 23:59:59 다음 샘플이 자동으로 익일 00:00:00으로 롤오버됨을 단위 테스트로 검증 완료.
- **프로젝트 단위 타이어 세트 정렬 시**:
  - `VTAccBrkProject`는 날짜와 시간이 포함된 `Datetime` 타임스탬프(`pd.Timestamp`)를 기준으로 오름차순 정렬하므로, 자정을 넘긴 시험 세트도 시간 역전 없이 완벽하게 정렬 및 선형 보간 수행.

### ③ 슬립률 분포 분석 구간 기본값 개선 (`an_slip_pdf.py`, `an_skewness.py`)
- **속도 구간 동적 연동**:
  - 기존 하드코딩된 임의 속도(80~5kph)를 제거하고, 사용자가 지정한 시험 속도(`test_vel`, 예: 100~1kph)를 기본 분석 구간으로 동적 연동.
- **최소 속도(min_vel) 안정화 가드 및 주석 명시**:
  - 0kph 완전 정지 부근에서 발생하는 휠 슬립률 분모 0 발산 및 휠 락 노이즈를 방어하기 위해 최소 속도(min_vel=1kph)를 필수 보장하도록 설계하고, 해당 공학적 사유를 코드 주석 및 닥스트링에 상세 기술.

### ④ 자동 `am`/`pm` 접미사 제거 및 `cond` 수동 처리 규격화
- **불필요 접미사 제거**:
  - 13:00 분기 기반 임의 `am`/`pm` 자동 생성 로직을 전면 삭제하고, 사용자가 명시적으로 전달한 `cond` 값만 수용.
  - 미입력 시 파일명 및 그래프 타이틀에 `_am`, `_pm`, `_None` 등의 불필요한 문자열이 일절 들어가지 않도록 `vt_acc_brk.py`, `vt_acc_brk_tire.py`, `plotter_tire.py`, `plotter_project.py` 필터링 정비.

---

## 🧪 2. 무결성 검증 결과 (Verification Results)

1. **`DateTimeHelper` 자가 구동 테스트**:
   - Case 1: GPS 좌표 기반 타임존 자동 식별 (한국 테크노링 +9h, 핀란드 이발로 +2h) 통과
   - Case 2: 날짜(Date) 추출 우선순위 통과
   - Case 3: VBOX GPS 시간 파싱 및 타임존 오프셋 가산 통과
   - Case 4: 100,000행 초고속 Datetime 생성 벤치마크 (0.001초 완료, Pass!)
2. **날짜 롤오버 및 자정 통과 시뮬레이션**:
   - `UTC 20:00 + 9h` $\to$ `2026-03-11 05:00:00` (Pass!)
   - `23:59:58` 주행 시작 $\to$ `00:00:02.990` 자정 통과 익일 전환 (Pass!)
3. **실차 제동 데이터 통합 분석 파이프라인 (Case 4 - BMW 320d ADAC Dry)**:
   - C1 (09:51:36) $\to$ T1 (10:26:18) $\to$ C2 (14:37:47) 순서 정렬 및 분석 완주
   - 제어 타이어 보정(`control`) 정상 산출 및 `graph.xlsx` (41개 시각화 이미지 삽입) 생성 완결.
   - 전체 프로세스 종료 코드: `Exit Code 0`

---

## 📂 3. 변경 파일 목록 (Git Status)

- `unoUtil/file_reader/datetime_helper.py` (VBOX zfill(6) 시간 파싱, return_datetime 지원)
- `unoUtil/file_reader/file_data_reader.py` (보정된 combined_dt 및 save_date 갱신)
- `unoUtil/vehicle/acc_brk/analyzers/an_slip_pdf.py` (test_vel 기본 구간 연동, min_vel 주석 명시)
- `unoUtil/vehicle/acc_brk/analyzers/an_skewness.py` (속도 구간 정합)
- `unoUtil/vehicle/acc_brk/vt_acc_brk.py` (자동 am/pm 제거, 수동 cond만 처리)
- `unoUtil/vehicle/acc_brk/vt_acc_brk_tire.py` (cond None 파일명 방어)
- `unoUtil/vehicle/acc_brk/plotter_tire.py` (파일명 및 제목 None 필터링)
- `unoUtil/vehicle/acc_brk/plotter_project.py` (파일명 및 제목 None 필터링)
