# Project 02 — Explainable ML Dashboard

A full-stack portfolio project that turns a tabular churn model into a usable product: reproducible training, FastAPI inference, local explanations, and a React/TypeScript dashboard.

## 1. Business objective

Customer churn prediction helps retention teams identify accounts that deserve proactive follow-up. This project predicts `Churn = Yes/No`, returns a churn probability, assigns a risk level, and explains the main factors behind each prediction.

The project emphasizes recall and ROC-AUC because detecting customers at risk is more important than maximizing accuracy on already-stable customers.

## 2. Architecture overview

```text
CSV data -> preprocessing pipeline -> model comparison -> saved artifacts
                                      -> FastAPI inference API
                                      -> React decision dashboard
```

- `data/raw/`: optional real CSV files, ignored by Git.
- `data/sample/`: small synthetic CSV used when no raw dataset exists.
- `backend/train_model.py`: trains and saves the model artifacts.
- `backend/app/`: API, schemas, prediction service, and explanation service.
- `frontend/`: Vite React dashboard.
- `reports/`: written ML report.

## 3. Technical stack

**Backend**: Python, pandas, numpy, scikit-learn, joblib, FastAPI, Pydantic, uvicorn, pytest.

**Frontend**: React, TypeScript, Vite, Recharts-ready dependency set, custom CSS.

**ML**: Logistic Regression, Random Forest, Gradient Boosting, accuracy, precision, recall, F1, ROC-AUC, confusion matrix, feature contribution approximations.

## 4. Repository structure

```text
explainable-churn-ml-dashboard/
├── README.md
├── ROADMAP.md
├── .gitignore
├── docker-compose.yml
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── schemas.py
│   │   ├── model_service.py
│   │   ├── explain_service.py
│   │   └── config.py
│   ├── models/
│   │   └── .gitkeep
│   ├── requirements.txt
│   ├── train_model.py
│   └── tests/
├── frontend/
│   ├── package.json
│   ├── index.html
│   └── src/
├── notebooks/
│   └── 01_training_and_explainability.ipynb
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
├── reports/
│   └── model_report.md
└── screenshots/
```

## 5. Dataset

Place a customer churn CSV in `data/raw/`. If multiple CSV files exist, the training script uses the first file sorted by name. If no raw CSV exists, it falls back to `data/sample/sample_churn.csv`.

Expected target column:

- `Churn` with values `Yes` / `No`.

Typical supported columns include `gender`, `SeniorCitizen`, `Partner`, `Dependents`, `tenure`, `InternetService`, `Contract`, `PaymentMethod`, `MonthlyCharges`, and `TotalCharges`. `TotalCharges` is converted to numeric during training.

## 6. Backend installation

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 7. Frontend installation

```bash
cd frontend
npm install
```

## 8. Train the model

From the repository root or from `backend/`:

```bash
cd backend
python train_model.py
```

This saves:

- `backend/models/churn_model.joblib`
- `backend/models/preprocessor.joblib`
- `backend/models/model_metadata.json`

Model artifacts are ignored by Git because they are generated files.

## 9. Launch the API

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

API URL: `http://localhost:8000`

## 10. Launch the dashboard

```bash
cd frontend
npm run dev
```

Dashboard URL: `http://localhost:5173`

The frontend uses `VITE_API_BASE_URL` when provided and defaults to `http://localhost:8000`.

## 11. API endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/` | Project status and model version. |
| `GET` | `/health` | API health and model-loaded status. |
| `POST` | `/predict` | Score one customer. |
| `POST` | `/predict-batch` | Score a list of customers. |
| `GET` | `/model-info` | Model type, training date, metrics, feature count, target, threshold. |

Example request:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "gender":"Female",
    "SeniorCitizen":0,
    "Partner":"No",
    "Dependents":"No",
    "tenure":3,
    "PhoneService":"Yes",
    "MultipleLines":"No",
    "InternetService":"Fiber optic",
    "OnlineSecurity":"No",
    "OnlineBackup":"No",
    "DeviceProtection":"No",
    "TechSupport":"No",
    "StreamingTV":"No",
    "StreamingMovies":"No",
    "Contract":"Month-to-month",
    "PaperlessBilling":"Yes",
    "PaymentMethod":"Electronic check",
    "MonthlyCharges":74.4,
    "TotalCharges":229.55
  }'
```

## 12. ML metrics

The training pipeline reports:

- Accuracy
- Precision
- Recall
- F1
- ROC-AUC
- Confusion matrix

Model selection sorts candidates by ROC-AUC, then recall, then F1. This reflects the business priority: rank churn risk well and capture at-risk customers.

## 13. Interpretability

The API returns the top five local factors for each prediction.

- Logistic Regression: approximate contributions with transformed feature values multiplied by coefficients.
- Tree models: approximate contributions with transformed feature values weighted by feature importances.

These explanations describe model behavior for a prediction. They do not prove causal reasons for customer churn.

## 14. Tests

```bash
cd backend
pytest
```

The tests train artifacts from the sample dataset if needed, then verify `/health`, `/predict`, and invalid input handling.

## 15. Docker Compose

```bash
docker compose up --build
```

This starts:

- backend on `http://localhost:8000`
- frontend on `http://localhost:5173`

The compose workflow installs dependencies and trains a demo model from the available dataset before launching the API.

## 16. Notebook

```bash
jupyter notebook notebooks/01_training_and_explainability.ipynb
```

The notebook mirrors the training workflow and documents EDA, preprocessing, model comparison, explainability, and artifact saving.

## 17. Current limitations

- The bundled sample dataset is small and synthetic; it is for functional validation only.
- Local explanations are approximations unless a future SHAP integration is added and validated.
- The default threshold is `0.50`; production retention workflows should tune this threshold against capacity and costs.
- No model monitoring, drift detection, fairness assessment, or experiment tracking is included yet.

## 18. Next improvements

- Add probability calibration and threshold tuning.
- Add batch CSV upload and export in the dashboard.
- Add SHAP charts or permutation importance visuals.
- Add data validation before training.
- Add MLflow or a lightweight experiment registry.
- Add production Dockerfiles and deployment documentation.
