from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .model_service import get_model_info, is_model_loaded, predict_churn
from .schemas import CustomerInput, PredictionResponse

app = FastAPI(
    title="Project 02 — Explainable ML Dashboard",
    description="Explainable churn prediction API for a portfolio-grade ML product.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict:
    info = get_model_info() if is_model_loaded() else {"model_version": "not-trained"}
    return {
        "project": "Project 02 — Explainable ML Dashboard",
        "status": "ready" if is_model_loaded() else "model_missing",
        "model_version": info.get("model_version"),
    }


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "model_loaded": is_model_loaded()}


@app.post("/predict", response_model=PredictionResponse)
def predict(customer: CustomerInput) -> PredictionResponse:
    return PredictionResponse(**predict_churn(customer))


@app.post("/predict-batch", response_model=list[PredictionResponse])
def predict_batch(customers: list[CustomerInput]) -> list[PredictionResponse]:
    return [PredictionResponse(**predict_churn(customer)) for customer in customers]


@app.get("/model-info")
def model_info() -> dict:
    return get_model_info()
