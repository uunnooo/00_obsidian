"""
Module: correction_model
Description: 스노우 노면 환경 차분 머신러닝 보정 코어 엔진 (SnowCorrectionModel).
             동일 타이어 반복 시험 간의 환경 및 제동거리 차분(Delta) 데이터셋 구축, 6대 머신러닝 회귀 학습,
             기준 환경 기반 데이터 일괄 정규화 보정을 전담합니다.
             컴포지션 패턴(Composition Pattern)에 따라 수치 검증기(self.validator)와 시각화 플로터(self.plot)를 합성하여 제공합니다.
Date: 2026-09-30
"""

# 2단계: 임포트 영역
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Tuple

import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

from unoUtil.logger import LOGGER
from unoUtil.snow_condition.schema import harmonize_snow_dataframe
from unoUtil.snow_condition.correction_validator import SnowCorrectionValidator
from unoUtil.snow_condition.correction_plotter import SnowCorrectionPlotter

# 3단계: 전역 상수 및 로거
DEFAULT_MODEL_SAVE_DIR = Path("D:/uno/1. 2026/2. 25-26_Outdoor_Loop2/0. db/saved_models")
logger = LOGGER("CorrModel", root_name="SnowCondition")


class SnowCorrectionModel:
    """
    스노우 노면 환경 차분 보정 코어 엔진 (SnowCorrectionModel).
    
    컴포지션 패턴 (Composition Pattern):
    - self.validator: SnowCorrectionValidator (수치 정량 검증 및 대조표)
    - self.plot: SnowCorrectionPlotter (전문 시각화 플로터)
    """

    def __init__(
        self,
        x_cols: Optional[List[str]] = None,
        y_col: str = "char_brk_dist",
        target_model: str = "SVR",
        missing_strategy: str = "drop",
        feature_cols: Optional[List[str]] = None,
        target_col: Optional[str] = None
    ) -> None:
        """
        초기화 메서드.

        Args:
            x_cols (Optional[List[str]]): 노면/환경 특성 입력 컬럼명 리스트 (기본값: ['char_height', 'cd_test_ah']).
            y_col (str): 보정 대상 성능 결과 컬럼명 (기본값: 'char_brk_dist').
            target_model (str): 대표 학습 모델명 (기본값: 'SVR').
            missing_strategy (str): 결측치(NaN) 처리 전략 ('drop', 'fill_mean', 'fill_zero', 기본값: 'drop').
            feature_cols (Optional[List[str]]): 하위 호환성용 차분 피처 컬럼 리스트.
            target_col (Optional[str]): 하위 호환성용 차분 타깃 컬럼명.
        """
        self.target_model_name = target_model
        self.x_cols: List[str] = list(x_cols) if x_cols is not None else ['char_height', 'cd_test_ah']
        self.y_col: str = y_col
        self.missing_strategy: str = missing_strategy

        # 동적 차분(Delta) 컬럼명 자동 매핑 (SSOT)
        self.diff_x_cols: List[str] = feature_cols or [f'diff_{c}' for c in self.x_cols]
        self.diff_y_col: str = target_col or f'diff_{self.y_col}'
        self.feature_cols: List[str] = self.diff_x_cols
        self.target_col: str = self.diff_y_col

        self.models: Dict[str, Any] = {}
        self.metrics: Dict[str, Dict[str, float]] = {}
        self.best_model_name: str = target_model
        self.is_fitted: bool = False

        self.df_diff: Optional[pd.DataFrame] = None
        self.reference_conditions: Dict[str, float] = {}

        # 컴포지션 객체 합성
        self.validator: SnowCorrectionValidator = SnowCorrectionValidator(self)
        self.plot: SnowCorrectionPlotter = SnowCorrectionPlotter(self)

    def calc_difference_dataset(
        self,
        data: pd.DataFrame,
        ref_order: str = '1st',
        corr_order: str = '2nd',
        req_col: str = 'infor_REQ_NO',
        set_col: str = 'infor_TIRE_SET',
        x_cols: Optional[List[str]] = None,
        y_col: Optional[str] = None
    ) -> pd.DataFrame:
        """
        동일 의뢰/타이어 1st(Ref) vs 2nd(Corr) 반복 평가 간의 환경(x_cols) 및 성능(y_col) 차분(Delta) 데이터셋을 동적으로 구축합니다.
        결측치(NaN) 및 빈 데이터에 대한 사전 방어 가드가 내장되어 있습니다.
        """
        df = harmonize_snow_dataframe(data)
        use_x = list(x_cols) if x_cols is not None else self.x_cols
        use_y = y_col or self.y_col

        # 1. 필수 식별 컬럼 탐색
        order_col = 'test_order' if 'test_order' in df.columns else ('Order' if 'Order' in df.columns else None)
        if order_col is None:
            raise KeyError("시험 차수 식별 컬럼('test_order' 또는 'Order')이 존재하지 않습니다.")

        r_col = req_col if req_col in df.columns else ('REQ_NO' if 'REQ_NO' in df.columns else 'infor_REQ_NO')
        s_col = set_col if set_col in df.columns else ('TIRE_SET' if 'TIRE_SET' in df.columns else 'infor_TIRE_SET')

        # 2. 필수 인자 존재 유무 검증 (Missing Column Guard)
        missing_cols = [c for c in [order_col, r_col, s_col] + use_x + [use_y] if c not in df.columns]
        if missing_cols:
            raise KeyError(f"필수 입력 컬럼이 데이터프레임에 존재하지 않습니다: {missing_cols}")

        # 3. 결측치(NaN) 정제 및 빈 데이터 방어 가드
        df_clean = df[[order_col, r_col, s_col] + use_x + [use_y]].copy()

        # 전체 NaN 컬럼 검사
        all_nan_cols = [c for c in use_x + [use_y] if df_clean[c].isna().all()]
        if all_nan_cols:
            raise ValueError(f"지정된 컬럼 {all_nan_cols}에 유효한 수치 데이터가 전혀 없습니다. (All NaN)")

        nan_mask = df_clean[use_x + [use_y]].isna().any(axis=1)
        nan_count = int(nan_mask.sum())
        if nan_count > 0:
            if self.missing_strategy == 'drop':
                df_clean = df_clean[~nan_mask].copy()
                logger.warning(f"환경/성능 결측치(NaN) {nan_count}행을 안전하게 제거했습니다. (남은 유효 데이터: {len(df_clean):,}행)")
            elif self.missing_strategy == 'fill_mean':
                df_clean[use_x + [use_y]] = df_clean[use_x + [use_y]].fillna(df_clean[use_x + [use_y]].mean())
                logger.info(f"환경/성능 결측치(NaN) {nan_count}행을 컬럼 평균값으로 대체했습니다.")
            elif self.missing_strategy == 'fill_zero':
                df_clean[use_x + [use_y]] = df_clean[use_x + [use_y]].fillna(0.0)
                logger.info(f"환경/성능 결측치(NaN) {nan_count}행을 0.0으로 대체했습니다.")

        if len(df_clean) == 0:
            raise ValueError("결측치 정제 후 유효한 데이터가 0건입니다. 데이터를 확인하십시오.")

        df_1st = df_clean[df_clean[order_col] == ref_order].copy()
        df_2nd = df_clean[df_clean[order_col] == corr_order].copy()

        if df_1st.empty or df_2nd.empty:
            raise ValueError(f"차분 비교를 위한 데이터 부족: {ref_order}({len(df_1st)}건) vs {corr_order}({len(df_2nd)}건)")

        # 4. 동일 타이어(Run 단위) 평균 집계
        agg_cols = use_x + [use_y]
        grp_1st = df_1st.groupby([r_col, s_col])[agg_cols].mean().reset_index()
        grp_2nd = df_2nd.groupby([r_col, s_col])[agg_cols].mean().reset_index()

        merged = pd.merge(grp_1st, grp_2nd, on=[r_col, s_col], suffixes=('_1st', '_2nd'), how='inner')
        if merged.empty:
            raise ValueError(f"동일 의뢰/타이어 매칭 결과가 비어있습니다 ({r_col}, {s_col} 불일치).")

        # 5. 동적 Delta 계산 (2nd - 1st)
        diff_x = []
        for col in use_x:
            diff_col_name = f'diff_{col}'
            merged[diff_col_name] = merged[f'{col}_2nd'] - merged[f'{col}_1st']
            diff_x.append(diff_col_name)

        diff_y_name = f'diff_{use_y}'
        merged[diff_y_name] = merged[f'{use_y}_2nd'] - merged[f'{use_y}_1st']

        # 모델 내부 상태 갱신
        self.x_cols = use_x
        self.y_col = use_y
        self.diff_x_cols = diff_x
        self.diff_y_col = diff_y_name
        self.feature_cols = diff_x
        self.target_col = diff_y_name
        self.df_diff = merged

        logger.info(f"동일 타이어 {ref_order} vs {corr_order} 차분 데이터셋 구축 완료: 총 {len(merged)}개 매칭 (X: {diff_x}, Y: {diff_y_name})")
        return merged

    def train_models(
        self,
        df_diff: Optional[pd.DataFrame] = None,
        knn_neighbors: Optional[int] = None,
        knn_weights: str = 'uniform',
        knn_p: int = 2,
        rf_params: Optional[Dict[str, Any]] = None,
        svr_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Dict[str, float]]:
        """
        6종 머신러닝 회귀 모델(RF, KNN, SVR, Ridge, Lasso, ElasticNet)을 학습하고 성능 지표를 산출합니다.
        결측치 및 빈 데이터 안전 가드가 적용되어 있습니다.

        Parameters
        ----------
        df_diff : Optional[pd.DataFrame]
            학습할 차분 데이터셋
        knn_neighbors : Optional[int]
            KNN 회귀 이웃 수. 기본값 None 시 국소 아일랜드/분화구 노이즈를 배제하는 광역 완만화 규격(k=25)으로 자동 설정됩니다.
        knn_weights : str
            KNN 가중치 모드. 기본값 'uniform'으로 특정 샘플의 노이즈 과적합을 차단하고 광역 거시 평균 반응면을 형성합니다.
        knn_p : int
            KNN 거리 척도. 기본값 2 (유클리디안 거리).
        rf_params : Optional[Dict[str, Any]]
            Random Forest 파라미터. 기본값은 자잘한 계단/타일 구역 쪼개짐을 방지하고 물리적 거시 영역을 형성하는 러프 규격:
            n_estimators=100, max_depth=3, min_samples_leaf=6, min_samples_split=12.
        svr_params : Optional[Dict[str, Any]]
            SVR 파라미터. 기본값은 최외곽(Extrapolation) 영역에서의 가우시안 급격 감쇠 및 등고선 말림(Curling) 방지 규격:
            C=2.0, epsilon=0.1, gamma=0.07.
        """
        data = df_diff if df_diff is not None else self.df_diff
        if data is None or data.empty:
            raise ValueError("학습할 차분 데이터셋이 제공되지 않았습니다.")

        # 결측치 2차 방어
        clean_data = data.dropna(subset=self.diff_x_cols + [self.diff_y_col]).copy()
        if len(clean_data) < 2:
            raise ValueError(f"학습에 필요한 유효 데이터가 부족합니다 (유효 샘플: {len(clean_data)}건). 최소 2건 이상 필요.")

        X = clean_data[self.diff_x_cols].values
        y = clean_data[self.diff_y_col].values

        if knn_neighbors is not None:
            k_neighbors = min(len(X), max(1, knn_neighbors))
        else:
            # KNN 광역 완만화 러프 규격: k=25 (국소 아일랜드 완전 배제 + 거시 트렌드 유지)
            k_neighbors = min(len(X), max(3, 25))

        default_rf_kwargs = {
            'n_estimators': 100,
            'max_depth': 3,
            'min_samples_leaf': 6,
            'min_samples_split': 12,
            'random_state': 42
        }
        if rf_params:
            default_rf_kwargs.update(rf_params)

        default_svr_kwargs = {
            'C': 2.0,
            'epsilon': 0.1,
            'gamma': 0.07  # 외삽 말림(Curling) 방지 및 실차 복원율 극대화 최적 균형 규격 (Grid Search 최적해)
        }
        if svr_params:
            default_svr_kwargs.update(svr_params)

        candidate_models = {
            "Random Forest": RandomForestRegressor(**default_rf_kwargs),
            "KNN Regressor": KNeighborsRegressor(n_neighbors=k_neighbors, weights=knn_weights, p=knn_p),
            "SVR": SVR(**default_svr_kwargs),
            "Ridge": Ridge(alpha=1.0),
            "Lasso": Lasso(alpha=0.1),
            "ElasticNet": ElasticNet(alpha=0.1, l1_ratio=0.5)
        }

        best_score = -float('inf')
        self.metrics.clear()
        self.models.clear()

        for name, model in candidate_models.items():
            model.fit(X, y)
            preds = model.predict(X)
            clean_data[f'pred_{name}'] = preds

            r2 = r2_score(y, preds)
            mae = mean_absolute_error(y, preds)
            rmse = np.sqrt(mean_squared_error(y, preds))

            self.models[name] = model
            self.metrics[name] = {
                'r2': round(float(r2), 4),
                'mae': round(float(mae), 4),
                'rmse': round(float(rmse), 4)
            }

            if r2 > best_score:
                best_score = r2
                self.best_model_name = name

        self.df_diff = clean_data
        self.is_fitted = True
        logger.info(f"6종 모델 학습 완료! 최고 R² 모델: {self.best_model_name} (R²={best_score:.4f}, 피처 수={len(self.diff_x_cols)})")
        for m, met in self.metrics.items():
            logger.info(f"  - {m:<15}: R²={met['r2']:.4f}, MAE={met['mae']:.4f}, RMSE={met['rmse']:.4f}")

        return self.metrics

    def set_reference_conditions(self, conditions: Dict[str, float]) -> None:
        """
        보정에 적용할 기준 환경 프로파일을 등록합니다.
        """
        self.reference_conditions = conditions.copy()
        logger.info(f"기준 환경 프로파일 등록 완료: {self.reference_conditions}")

    def predict_delta(
        self,
        *args: Any,
        model_name: Optional[str] = None,
        **kwargs: Any
    ) -> Union[float, np.ndarray]:
        """
        환경 인자 차분값(ΔX)에 따른 타깃 성능 변화량(ΔY)을 예측합니다.
        단일 스칼라들, 1D/2D numpy 배열, pandas DataFrame, dict 등 유연한 입력을 지원합니다.
        """
        if not self.is_fitted:
            raise RuntimeError("모델이 아직 학습되지 않았습니다. train_models()를 먼저 실행하십시오.")

        m_name = model_name or self.best_model_name
        model = self.models.get(m_name)
        if model is None:
            raise KeyError(f"모델 '{m_name}'이 존재하지 않습니다.")

        # 입력 형태 해석
        if len(args) == 1 and isinstance(args[0], pd.DataFrame):
            # 1. DataFrame 입력
            df_in = args[0]
            cols = []
            for c in self.diff_x_cols:
                if c in df_in.columns:
                    cols.append(c)
                elif c.replace('diff_', '') in df_in.columns:
                    cols.append(c.replace('diff_', ''))
                elif f'diff_{c}' in df_in.columns:
                    cols.append(f'diff_{c}')
                else:
                    break
            if len(cols) == len(self.diff_x_cols):
                X_in = df_in[cols].fillna(0.0).values
            elif df_in.shape[1] >= len(self.diff_x_cols):
                X_in = df_in.iloc[:, :len(self.diff_x_cols)].fillna(0.0).values
            else:
                raise KeyError(f"입력 DataFrame에 필수 피처 {self.diff_x_cols}가 충분하지 않습니다 (제공 컬럼: {list(df_in.columns)}).")
            is_scalar = False
        elif len(args) == 1 and isinstance(args[0], dict):
            # 2. dict 입력
            d = args[0]
            row = [d.get(c, d.get(c.replace('diff_', ''), 0.0)) for c in self.diff_x_cols]
            X_in = np.array([row])
            is_scalar = True
        elif len(args) == 1 and isinstance(args[0], (np.ndarray, list, tuple)):
            # 3. 배열 / 리스트 입력
            arr = np.asarray(args[0])
            if arr.ndim == 1:
                if len(arr) == len(self.diff_x_cols):
                    X_in = arr.reshape(1, -1)
                    is_scalar = True
                else:
                    raise ValueError(f"입력 피처 수({len(arr)})가 모델 피처 수({len(self.diff_x_cols)})와 다릅니다.")
            else:
                X_in = arr
                is_scalar = False
        elif len(args) > 1:
            # 4. 여러 개별 인자 전달 (예: predict_delta(diff_h, diff_ah))
            cols_stacked = [np.atleast_1d(a) for a in args]
            X_in = np.column_stack(cols_stacked)
            is_scalar = all(np.isscalar(a) for a in args)
        elif kwargs:
            # 5. kwargs 전달
            row = [kwargs.get(c, kwargs.get(c.replace('diff_', ''), 0.0)) for c in self.diff_x_cols]
            X_in = np.array([row])
            is_scalar = True
        else:
            raise ValueError("예측을 위한 입력 데이터가 전달되지 않았습니다.")

        # 결측치 방어
        X_in = np.nan_to_num(X_in, nan=0.0)
        preds = model.predict(X_in)
        return float(preds[0]) if is_scalar and len(preds) == 1 else preds

    def correct_dataframe(
        self,
        data: pd.DataFrame,
        out_col: Optional[str] = None,
        reference_condition: Optional[Dict[str, float]] = None,
        model_name: Optional[str] = None
    ) -> pd.DataFrame:
        """
        제동 데이터프레임의 성능 결과(y_col)를 환경 차분 보정 모델을 통해 보정합니다.
        동적 x_cols를 기반으로 차분을 산출하며, 결측치가 있을 경우에도 안전하게 방어합니다.
        """
        if not self.is_fitted:
            raise RuntimeError("보정을 수행하기 위한 모델이 학습되지 않았습니다.")

        df = harmonize_snow_dataframe(data).copy()
        m_name = model_name or getattr(self, 'target_model_name', None) or self.best_model_name
        target_out_col = out_col or f"{self.y_col}_corr"
        ref_cond = reference_condition or self.reference_conditions

        # 기준 환경 프로파일 존재 여부 확인
        has_full_ref = ref_cond and all(c in ref_cond for c in self.x_cols)

        if has_full_ref:
            # 1) 기준 환경 기반 일괄 정규화
            diff_arrays = []
            for c in self.x_cols:
                ref_val = ref_cond[c]
                d = (df[c] - ref_val).fillna(0.0).values
                diff_arrays.append(d)
            X_diff = np.column_stack(diff_arrays)
            delta_pred = self.predict_delta(X_diff, model_name=m_name)
            df[target_out_col] = df[self.y_col] - delta_pred
            logger.info(f"기준 환경 기반 전체 데이터 일괄 정규화 완료: 총 {len(df):,}행 (out_col='{target_out_col}')")
        else:
            # 2) 1st 기준 상대 차분 차감 보정
            order_col = 'test_order' if 'test_order' in df.columns else ('Order' if 'Order' in df.columns else None)
            req_col = 'infor_REQ_NO' if 'infor_REQ_NO' in df.columns else 'REQ_NO'
            set_col = 'infor_TIRE_SET' if 'infor_TIRE_SET' in df.columns else 'TIRE_SET'

            if order_col is None or req_col not in df.columns or set_col not in df.columns:
                raise KeyError(f"1st 상대 보정에 필요한 식별 컬럼({order_col}, {req_col}, {set_col})이 부족합니다.")

            # 1st 환경 평균 산출
            df_1st = df[df[order_col] == '1st']
            if df_1st.empty:
                logger.warning("1st 차수 데이터가 없어 원본 값을 그대로 유지합니다.")
                df[target_out_col] = df[self.y_col]
                return df

            env_1st = df_1st.groupby([req_col, set_col])[self.x_cols].mean().reset_index()
            rename_map = {c: f'{c}_ref' for c in self.x_cols}
            env_1st.rename(columns=rename_map, inplace=True)

            merged = pd.merge(df, env_1st, on=[req_col, set_col], how='left')

            diff_arrays = []
            for c in self.x_cols:
                d = (merged[c] - merged[f'{c}_ref']).fillna(0.0).values
                diff_arrays.append(d)
            X_diff = np.column_stack(diff_arrays)
            delta_pred = self.predict_delta(X_diff, model_name=m_name)

            # 1st는 보정하지 않고 2nd(및 이후)만 차분 차감
            is_corr_target = (df[order_col] != '1st').values
            df[target_out_col] = df[self.y_col]
            df.loc[is_corr_target, target_out_col] = df.loc[is_corr_target, self.y_col] - delta_pred[is_corr_target]
            logger.info(f"1st 대비 2nd 상대 환경 차분 차감 보정 완료: 총 {len(df):,}행 (out_col='{target_out_col}')")

        return df

    def save_models(self, save_dir: Union[str, Path] = DEFAULT_MODEL_SAVE_DIR) -> Path:
        """학습된 모델들을 영속화 저장합니다."""
        p = Path(save_dir)
        p.mkdir(parents=True, exist_ok=True)
        for name, model in self.models.items():
            safe_name = name.replace(" ", "_").lower()
            joblib.dump(model, p / f"{safe_name}.joblib")
        logger.info(f"모델 {len(self.models)}종 영속화 저장 완료: {p}")
        return p

    def load_models(self, filepath: Union[str, Path]) -> bool:
        """저장된 모델 파일을 로드합니다."""
        p = Path(filepath)
        if not p.exists():
            logger.error(f"모델 파일이 존재하지 않습니다: {p}")
            return False
        model = joblib.load(p)
        name = p.stem.replace("_", " ").title()
        self.models[name] = model
        self.best_model_name = name
        self.is_fitted = True
        logger.info(f"모델 로드 완료: {name} ({p})")
        return True

    # ==========================================================================
    # 🔗 편의 위임 메서드 (Delegation to self.validator & self.plot)
    # ==========================================================================
    def calc_corrected_comparison_table(self, *args: Any, **kwargs: Any) -> pd.DataFrame:
        """[Validator 위임] 1차 vs 2차 정밀 대조표를 산출합니다."""
        return self.validator.calc_corrected_comparison_table(*args, **kwargs)

    def plot_delta_prediction_scatter(self, *args: Any, **kwargs: Any) -> Tuple[plt.Figure, plt.Axes]:
        """[Plotter 위임] Figure 1 차분 산점도를 시각화합니다."""
        return self.plot.plot_delta_prediction_scatter(*args, **kwargs)

    def plot_scatter_restoration(self, *args: Any, **kwargs: Any) -> Tuple[plt.Figure, Any]:
        """[Plotter 위임] Figure 2 복원율 산점도를 시각화합니다."""
        return self.plot.plot_scatter_restoration(*args, **kwargs)

    def plot_1st_2nd_scatter_overplot(self, *args: Any, **kwargs: Any) -> Tuple[plt.Figure, plt.Axes]:
        """[Plotter 위임] 1st vs 2nd 산점도 오버플랏을 시각화합니다."""
        return self.plot.plot_1st_2nd_scatter_overplot(*args, **kwargs)

    def plot_correction_map(self, *args: Any, **kwargs: Any) -> Tuple[plt.Figure, plt.Axes]:
        """[Plotter 위임] Figure 3 등고선 보정 맵을 시각화합니다."""
        return self.plot.plot_correction_map(*args, **kwargs)

    def plot_delta_braking_bar(self, *args: Any, **kwargs: Any) -> Tuple[plt.Figure, plt.Axes]:
        """[Plotter 위임] 편차 바차트를 시각화합니다."""
        return self.plot.plot_delta_braking_bar(*args, **kwargs)

    def plot_residual_dependency(self, *args: Any, **kwargs: Any) -> Tuple[plt.Figure, Any]:
        """[Plotter 위임] 잔차 환경 의존성 플롯을 시각화합니다."""
        return self.plot.plot_residual_dependency(*args, **kwargs)

    def plot_model_comparison(self, *args: Any, **kwargs: Any) -> Tuple[plt.Figure, Any]:
        """[Plotter 위임] 모델 성능 비교 바차트를 시각화합니다."""
        return self.plot.plot_model_comparison(*args, **kwargs)

    def plot_tire_subsets_comparison(self, *args: Any, **kwargs: Any) -> Tuple[plt.Figure, Any]:
        """[Plotter 위임] 의뢰번호 및 타이어 세트별 보정 전/후 비교 차트를 시각화합니다."""
        return self.plot.plot_tire_subsets_comparison(*args, **kwargs)

    def plot_tire_set_correction(self, *args: Any, **kwargs: Any) -> Tuple[plt.Figure, Any]:
        """[Plotter 위임] plot_tire_subsets_comparison의 직관적 별칭입니다."""
        return self.plot.plot_tire_subsets_comparison(*args, **kwargs)

    def scatter_restoration_comparison(self, *args: Any, **kwargs: Any) -> Tuple[plt.Figure, Any]:
        """[Plotter 위임] 3대 모델 1차 vs 2차 복원 수렴도 산점도 비교 차트를 시각화합니다."""
        return self.plot.scatter_restoration_comparison(*args, **kwargs)


# ==============================================================================
# # region [자가 구동 테스트]
# ==============================================================================
if __name__ == "__main__":
    logger.info("=== [자가 구동 테스트] SnowCorrectionModel (컴포지션 패턴) ===")
    np.random.seed(42)
    n = 40
    mock_df = pd.DataFrame({
        'infor_REQ_NO': ['REQ_001'] * n,
        'infor_TIRE_SET': [f'C{i%10+1}' for i in range(n)],
        'test_order': ['1st'] * (n // 2) + ['2nd'] * (n // 2),
        'char_brk_dist': np.random.normal(17.5, 1.2, n),
        'char_height': np.random.normal(5.0, 0.5, n),
        'cd_test_ah': np.random.normal(2.0, 0.3, n)
    })

    # 1. 모델 초기화
    model = SnowCorrectionModel()
    
    # 2. 차분 데이터셋 및 모델 학습
    df_diff = model.calc_difference_dataset(mock_df)
    metrics = model.train_models(df_diff)
    
    # 3. 보정 적용
    df_corr = model.correct_dataframe(mock_df)
    
    # 4. 컴포지션 검증기 호출
    df_comp = model.validator.calc_corrected_comparison_table(df_corr)
    logger.info(f"대조표 행 수: {len(df_comp)}")
    
    # 5. 컴포지션 플로터 호출 (Non-blocking)
    fig1, ax1 = model.plot.delta_prediction_scatter(df_diff, close=True)
    fig2, ax2 = model.plot.correction_map(close=True)
    logger.info("플로터 시각화 성공")

    logger.info("=== SnowCorrectionModel 자가 구동 테스트 통과 (Code 0) ===")
# endregion
