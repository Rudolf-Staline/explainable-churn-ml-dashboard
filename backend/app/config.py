from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = BASE_DIR.parent
MODELS_DIR = BASE_DIR / "models"
MODEL_PATH = MODELS_DIR / "churn_model.joblib"
PREPROCESSOR_PATH = MODELS_DIR / "preprocessor.joblib"
METADATA_PATH = MODELS_DIR / "model_metadata.json"
RAW_DATA_DIR = REPO_ROOT / "data" / "raw"
SAMPLE_DATA_PATH = REPO_ROOT / "data" / "sample" / "sample_churn.csv"

TARGET_COLUMN = "Churn"
MODEL_VERSION_FALLBACK = "not-trained"
DEFAULT_THRESHOLD = 0.50
RISK_THRESHOLDS = {
    "medium": 0.35,
    "high": 0.65,
}
