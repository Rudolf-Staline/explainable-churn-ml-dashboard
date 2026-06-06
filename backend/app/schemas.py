from pydantic import BaseModel, Field, field_validator


class CustomerInput(BaseModel):
    gender: str
    SeniorCitizen: int = Field(ge=0, le=1)
    Partner: str
    Dependents: str
    tenure: int = Field(ge=0)
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float = Field(ge=0)
    TotalCharges: float = Field(ge=0)

    @field_validator(
        "gender",
        "Partner",
        "Dependents",
        "PhoneService",
        "MultipleLines",
        "InternetService",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies",
        "Contract",
        "PaperlessBilling",
        "PaymentMethod",
    )
    @classmethod
    def non_empty_string(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("value must be a non-empty string")
        return value.strip()


class Factor(BaseModel):
    feature: str
    contribution: float
    direction: str


class PredictionResponse(BaseModel):
    churn_probability: float
    churn_prediction: str
    risk_level: str
    top_factors: list[Factor]
    model_version: str
