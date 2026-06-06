# Model Report — Explainable Churn ML Dashboard

## 1. Business objective

The objective is to predict whether a customer is likely to churn so retention teams can prioritize outreach. The model is intended as a decision-support layer, not as an automatic customer treatment engine.

## 2. Dataset

The project expects a churn CSV in `data/raw/`. If no raw dataset exists, the training pipeline uses `data/sample/sample_churn.csv`, a small synthetic sample that mirrors common telecom churn columns. The target is `Churn` with `Yes` / `No` labels.

## 3. Preprocessing

The pipeline converts `TotalCharges` to numeric, maps `Churn` to 1/0, drops `customerID`, imputes missing numerical values with the median, scales numerical features, imputes categorical values with the most frequent category, and applies one-hot encoding with unknown-category handling.

## 4. Models tested

- Logistic Regression with balanced class weights.
- Random Forest with balanced class weights.
- Gradient Boosting Classifier.

## 5. Metrics

The model is evaluated with accuracy, precision, recall, F1, ROC-AUC, and a confusion matrix. Recall and ROC-AUC are emphasized because churn detection has asymmetric costs: failing to identify a real churn risk can be more expensive than flagging an extra customer for review.

## 6. Best model

The training routine selects the model with the best ROC-AUC, then recall, then F1. This prioritizes ranking quality and risk capture over plain accuracy.

## 7. Explainability method

Local explanations return the top five factors for an individual prediction. If the best model exposes coefficients, contributions are approximated with transformed feature values multiplied by model coefficients. For tree models, transformed feature values are weighted by feature importances. This is a pragmatic explanation layer for a dashboard; it is not a causal proof.

## 8. API integration

FastAPI exposes health, single prediction, batch prediction, and model metadata endpoints. Prediction responses include churn probability, binary prediction, risk level, top factors, and model version.

## 9. Dashboard integration

The React dashboard consumes the API, displays model KPIs, scores an individual customer, renders a risk gauge, and lists the most important local risk factors.

## 10. Limitations

- The sample dataset is intentionally small and is only suitable for smoke tests.
- Explanations are model-based approximations, not causal explanations.
- Real deployment would require calibration, monitoring, drift checks, fairness analysis, and business validation.
- A churn model can identify risk patterns but cannot prove why a customer will leave.

## 11. Future work

- Add probability calibration and threshold tuning by campaign capacity.
- Add SHAP visualizations when the environment and model type support them reliably.
- Add batch CSV upload in the dashboard.
- Add experiment tracking and data validation.
- Add production monitoring for data drift and performance decay.
