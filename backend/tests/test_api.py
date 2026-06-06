from fastapi.testclient import TestClient

from app.main import app
from app.model_service import load_artifacts
from train_model import train_and_save


VALID_CUSTOMER = {
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "No",
    "Dependents": "No",
    "tenure": 3,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "No",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "No",
    "StreamingMovies": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 74.4,
    "TotalCharges": 229.55,
}


def setup_module():
    train_and_save()
    load_artifacts.cache_clear()


def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["model_loaded"] is True


def test_predict_endpoint_with_valid_customer():
    client = TestClient(app)
    response = client.post("/predict", json=VALID_CUSTOMER)
    payload = response.json()
    assert response.status_code == 200
    assert 0 <= payload["churn_probability"] <= 1
    assert payload["churn_prediction"] in {"Yes", "No"}
    assert payload["risk_level"] in {"Low", "Medium", "High"}
    assert len(payload["top_factors"]) <= 5


def test_predict_endpoint_rejects_invalid_input():
    client = TestClient(app)
    invalid_customer = {**VALID_CUSTOMER, "tenure": -1}
    response = client.post("/predict", json=invalid_customer)
    assert response.status_code == 422
