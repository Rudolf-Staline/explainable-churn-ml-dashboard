from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline


def _feature_names(preprocessor) -> list[str]:
    if hasattr(preprocessor, "get_feature_names_out"):
        return [name.replace("categorical__", "").replace("numeric__", "") for name in preprocessor.get_feature_names_out()]
    return []


def _extract_estimator(model):
    if isinstance(model, Pipeline):
        return model.steps[-1][1]
    return model


def explain_prediction(model, preprocessor, input_frame: pd.DataFrame, top_n: int = 5) -> list[dict]:
    transformed = preprocessor.transform(input_frame)
    if hasattr(transformed, "toarray"):
        transformed = transformed.toarray()
    transformed = np.asarray(transformed)
    feature_names = _feature_names(preprocessor)
    estimator = _extract_estimator(model)

    if hasattr(estimator, "coef_"):
        weights = estimator.coef_[0]
        contributions = transformed[0] * weights
    elif hasattr(estimator, "feature_importances_"):
        importances = estimator.feature_importances_
        baseline = np.nanmean(transformed, axis=0) if transformed.shape[0] > 1 else np.zeros(transformed.shape[1])
        contributions = (transformed[0] - baseline) * importances
    else:
        contributions = np.zeros(transformed.shape[1])

    if not feature_names or len(feature_names) != len(contributions):
        feature_names = [f"feature_{idx}" for idx in range(len(contributions))]

    ranked = np.argsort(np.abs(contributions))[::-1][:top_n]
    factors = []
    for idx in ranked:
        contribution = float(contributions[idx])
        factors.append(
            {
                "feature": feature_names[idx],
                "contribution": round(contribution, 4),
                "direction": "increases_risk" if contribution >= 0 else "decreases_risk",
            }
        )
    return factors
