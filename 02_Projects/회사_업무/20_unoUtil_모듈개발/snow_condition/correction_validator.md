# 📘 SnowCorrectionValidator (스노우 보정 모델 정량 수치 검증기)

## 📌 개요
`SnowCorrectionValidator`는 스노우 노면 환경 보정 모델의 유효성을 수치적으로 정밀 검증하는 전문 평가기 클래스입니다.
동일 의뢰/타이어의 1차 시험(1st Ref) 대비 2차 원본(2nd Raw) 및 2차 보정본(2nd Corr)의 1:1 정밀 대조표를 산출하고, 환경 변화로 인한 오차의 복원 및 감소율(Error Reduction Ratio, %)을 계산합니다.

---

## ⚙️ 주요 API 규격

### 1. `calc_corrected_comparison_table(data, model_name=None, save=False, ...)`
* **설명**: 1차(Ref) vs 2차(Raw/Corr) 정밀 대조표를 산출합니다.
* **매개변수**:
  * `data` (`pd.DataFrame`): 통합 제동 데이터프레임
  * `model_name` (`Optional[str]`): 특정 회귀 모델 지정 (기본값: 최적 모델)
  * `save` (`Union[bool, str, Path]`): Excel(`.xlsx`) 또는 `.csv` 파일 저장 경로 (다형성 지원)
* **산출 컬럼**:
  * `1st_Ref(m)`: 1차 기준 제동거리
  * `2nd_Raw(m)`: 2차 원본 실측 제동거리
  * `2nd_Corr(m)`: 2차 환경 보정 제동거리
  * `Raw_Diff(m)`: 원본 편차 ($2nd\_Raw - 1st\_Ref$)
  * `Corr_Diff(m)`: 보정 편차 ($2nd\_Corr - 1st\_Ref$)
  * `Error_Reduction(%)`: 오차 감소율 ($100 \times (1 - |\text{Corr\_Diff}| / |\text{Raw\_Diff}|)$)
* **반환값**: `pd.DataFrame`

### 2. `calc_error_reduction_summary(df_comp=None)`
* **설명**: 보정 전/후 MAE 및 표준편차(Std) 축소율을 요약 딕셔너리로 산출합니다.
* **반환값**: `Dict[str, float]`
