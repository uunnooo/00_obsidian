# 📋 WORK STATUS: unoUtil.snow_condition & Snow Project Refactoring

- **일시**: 2026-10-01
- **작업자**: uno & Gemini (Antigravity)
- **작업 도메인**: `unoUtil.snow_condition` (`surface_interpolator.py`) 및 `2026_Snow_RoadSurface_characteristics`

---

## 🎯 1. 작업 개요 및 핵심 목적
1. **센서 하드웨어 연산의 완전한 분리 (Separation of Concerns)**:
   - 보간기(`SnowSurfaceInterpolator`) 내부에 잔존하던 센서 하드웨어 채널 계산(`Height1~6` 좌/우/외측 오프셋, `Temp1~2` 온도 센서 뺄셈)을 100% 완전 제거.
   - 센서 계측치 가공은 사전 전처리(`a_make_SnowSurfaceCharacteristic_DF.py`)의 고유 영역으로 명확히 격리하고, 보간기는 순수한 3D 시공간 격자 보간에만 전념하도록 정립.
2. **`char_*` 단일 표준 명명 체계 (SSOT) 전면 일원화**:
   - `calc_h_diff`, `calc_t_diff`, `HeightDiffAver`, `TempDiffAver` 등 파편화되었던 과도기적 별칭을 영구 정리.
   - 특성치 컬럼(`char_height`, `char_temp`), 세션 식별자(`Cond_ID`)를 인터페이스 및 내부 모델 학습 전반의 단일 표준으로 통일.
3. **3중 결측치 및 이상치 안전 정제 파이프라인 (`_sanitize_feature`, `np.clip`) 탑재**:
   - 비수치/무한대(inf) $\to$ NaN 변환 (`pd.to_numeric`).
   - 센서 단선 및 결측치 $\to$ 세션 중앙값(median) 자동 대치 (`fillna`).
   - 물리적 유효 허용 범위 이탈값 $\to$ `np.clip` 상/하한 안전 제한.
4. **실데이터 엔드투엔드 파이프라인 전수 검증 (Exit Code 0)**:
   - `b_combine_surface_performance_spec.py` 및 `c_run_snow_correction_pipeline.py` 전수 완주.

---

## 🛠️ 2. 상세 수정 내역

### 1) `unoUtil/snow_condition/surface_interpolator.py`
- **센서 잔재 필드 및 하드웨어 파라미터 완전 삭제**:
  - `SurfaceGridSnapshot` 데이터 구조체에서 `z_temp_out`, `z_temp_tire`, `z_height_left`, `z_height_right` 삭제.
  - `SnowSurfaceInterpolator.__init__`에서 `range_temp_tire`, `range_temp_out` 파라미터 삭제.
- **3중 이상치·결측 정제 헬퍼 `_sanitize_feature` 신설**:
  - `pd.to_numeric(..., errors='coerce')` + `fillna(median)` + `np.clip(valid_range)`
- **`fit()` 인터페이스 및 내부 격자 학습 단일화**:
  - 기본 파라미터: `height_col='char_height'`, `temp_col='char_temp'`, `cond_id_col='Cond_ID'`
  - 내부 격자 모델 학습: `model_h.fit(pts, group['char_height'])`, `model_t.fit(pts, group['char_temp'])`
- **미사용 스키마 임포트 정리**: `COL_TEMP_OUT`, `COL_TEMP_TIRE` 제거.

### 2) `2026_Snow_RoadSurface_characteristics/b_combine_surface_performance_spec.py`
- `interp.fit(df_raw_sur, height_col='char_height', temp_col='char_temp', cond_id_col='Cond_ID', method='RF')` 완벽 연동.
- 1,964건 제동 데이터 전수 매칭 및 50개 컬럼 생성 완결.

### 3) 1:1 기술 매뉴얼 최신화
- `unoUtil/snow_condition/surface_interpolator.md`: 센서 연산 배제 및 `char_*` 단일 명명 체계 반영.

---

## 🧪 3. 무결성 검증 결과 (Verification)

| 실행 스크립트 | 대상 데이터 | 실행 결과 | 비고 |
| :--- | :--- | :---: | :--- |
| `b_combine_surface_performance_spec.py` | 87,831행 노면 + 1,964행 제동 | **Exit Code 0** | 53개 스냅샷 학습, 1,964건 전수 결합 완료 |
| `c_run_snow_correction_pipeline.py` | 1,964행 통합 데이터셋 | **Exit Code 0** | 6대 ML 학습, 1st vs 2nd 오차 66.14% 개선, 리포트 출력 |

---

## 📁 4. 옵시디언 볼트 동기화 완료 현황
- `D:\00_obsidian\00_Inbox\WORK_STATUS.md` 배포 완료.
- `D:\00_obsidian\02_Projects\회사_업무\20_unoUtil_모듈개발\snow_condition\00_snow_condition_대시보드.md` (v1.4.0 갱신).
- `D:\00_obsidian\02_Projects\회사_업무\20_unoUtil_모듈개발\00_unoUtil_모듈개발_대시보드.md` (v3.10 갱신).
- `surface_interpolator.md` 볼트 미러링 완료.
