from __future__ import annotations

import json
from functools import lru_cache

import joblib
import pandas as pd
from fastapi import HTTPException

from .config import DEFAULT_THRESHOLD, METADATA_PATH, MODEL_PATH, MODEL_VERSION_FALLBACK, PREPROCESSOR_PATH, RISK_THRESHOLDS
from .explain_service import explain_prediction
from .schemas import CustomerInput


class ModelArtifactsMissing(RuntimeError):
    pass


def _ensure_artifacts_exist() -> None:
    missing = [str(path) for path in (MODEL_PATH, PREPROCESSOR_PATH, METADATA_PATH) if not path.exists()]
    if missing:
        raise ModelArtifactsMissing(
            "Model artifacts are missing. Run `cd backend && python train_model.py` or execute the notebook first. "
            f"Missing: {', '.join(missing)}"
        )


@lru_cache(maxsize=1)
def load_artifacts():
    _ensure_artifacts_exist()
    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    with METADATA_PATH.open("r", encoding="utf-8") as file:
        metadata = json.load(file)
    return model, preprocessor, metadata


def is_model_loaded() -> bool:
    try:
        load_artifacts()
        return True
    except Exception:
        return False


def get_model_info() -> dict:
    try:
        model, preprocessor, metadata = load_artifacts()
    except ModelArtifactsMissing as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {
        "model_type": metadata.get("model_type", type(model).__name__),
        "training_date": metadata.get("training_date"),
        "metrics": metadata.get("metrics", {}),
        "feature_count": metadata.get("feature_count", len(getattr(preprocessor, "get_feature_names_out", lambda: [])())),
        "target": metadata.get("target", "Churn"),
        "threshold": metadata.get("threshold", DEFAULT_THRESHOLD),
        "model_version": metadata.get("model_version", MODEL_VERSION_FALLBACK),
    }


def _risk_level(probability: float) -> str:
    if probability >= RISK_THRESHOLDS["high"]:
        return "High"
    if probability >= RISK_THRESHOLDS["medium"]:
        return "Medium"
    return "Low"


def predict_churn(input_data: CustomerInput) -> dict:
    try:
        model, preprocessor, metadata = load_artifacts()
    except ModelArtifactsMissing as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    try:
        frame = pd.DataFrame([input_data.model_dump()])
        transformed = preprocessor.transform(frame)
        probability = float(model.predict_proba(transformed)[0][1])
        threshold = float(metadata.get("threshold", DEFAULT_THRESHOLD))
        prediction = "Yes" if probability >= threshold else "No"
        factors = explain_prediction(model, preprocessor, frame)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}") from exc

    return {
        "churn_probability": round(probability, 4),
        "churn_prediction": prediction,
        "risk_level": _risk_level(probability),
        "top_factors": factors,
        "model_version": metadata.get("model_version", MODEL_VERSION_FALLBACK),
    }
