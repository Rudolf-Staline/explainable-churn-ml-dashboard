from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from app.config import METADATA_PATH, MODEL_PATH, MODELS_DIR, PREPROCESSOR_PATH, RAW_DATA_DIR, SAMPLE_DATA_PATH, TARGET_COLUMN


def find_dataset() -> Path:
    raw_files = sorted(RAW_DATA_DIR.glob("*.csv"))
    return raw_files[0] if raw_files else SAMPLE_DATA_PATH


def load_dataset() -> pd.DataFrame:
    data_path = find_dataset()
    frame = pd.read_csv(data_path)
    if TARGET_COLUMN not in frame.columns:
        raise ValueError(f"Target column `{TARGET_COLUMN}` not found in {data_path}")
    frame["TotalCharges"] = pd.to_numeric(frame["TotalCharges"], errors="coerce")
    return frame


def prepare_data(frame: pd.DataFrame):
    y = frame[TARGET_COLUMN].map({"Yes": 1, "No": 0}).astype(int)
    X = frame.drop(columns=[TARGET_COLUMN])
    if "customerID" in X.columns:
        X = X.drop(columns=["customerID"])

    numeric_columns = X.select_dtypes(include=["number"]).columns.tolist()
    categorical_columns = [column for column in X.columns if column not in numeric_columns]

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, numeric_columns),
            ("categorical", categorical_pipeline, categorical_columns),
        ]
    )
    return X, y, preprocessor, numeric_columns, categorical_columns


def evaluate_model(model, X_test, y_test, threshold: float = 0.5) -> dict:
    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = (probabilities >= threshold).astype(int)
    return {
        "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
        "precision": round(float(precision_score(y_test, predictions, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, predictions, zero_division=0)), 4),
        "f1": round(float(f1_score(y_test, predictions, zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, probabilities)), 4) if len(np.unique(y_test)) > 1 else 0.0,
        "confusion_matrix": confusion_matrix(y_test, predictions).tolist(),
    }


def train_and_save() -> dict:
    frame = load_dataset()
    X, y, preprocessor, numeric_columns, categorical_columns = prepare_data(frame)
    stratify = y if y.nunique() > 1 and y.value_counts().min() >= 2 else None
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=stratify)

    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    candidates = {
        "LogisticRegression": LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42),
        "RandomForestClassifier": RandomForestClassifier(n_estimators=120, class_weight="balanced", random_state=42),
        "GradientBoostingClassifier": GradientBoostingClassifier(random_state=42),
    }

    results = {}
    trained_models = {}
    for name, model in candidates.items():
        model.fit(X_train_processed, y_train)
        trained_models[name] = model
        results[name] = evaluate_model(model, X_test_processed, y_test)

    best_name = sorted(results, key=lambda name: (results[name]["roc_auc"], results[name]["recall"], results[name]["f1"]), reverse=True)[0]
    best_model = trained_models[best_name]
    feature_count = len(preprocessor.get_feature_names_out())

    metadata = {
        "model_version": datetime.now(timezone.utc).strftime("%Y.%m.%d.%H%M"),
        "training_date": datetime.now(timezone.utc).isoformat(),
        "model_type": best_name,
        "metrics": results[best_name],
        "all_model_metrics": results,
        "feature_count": feature_count,
        "target": TARGET_COLUMN,
        "threshold": 0.5,
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
        "dataset_source": str(find_dataset().relative_to(Path.cwd().parent if Path.cwd().name == "backend" else Path.cwd())),
    }

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_model, MODEL_PATH)
    joblib.dump(preprocessor, PREPROCESSOR_PATH)
    with METADATA_PATH.open("w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2)
    return metadata


if __name__ == "__main__":
    saved_metadata = train_and_save()
    print(json.dumps(saved_metadata, indent=2))
