import type { PredictionResponse } from "../api/client";
import { RiskGauge } from "./RiskGauge";

type PredictionResultProps = {
  prediction?: PredictionResponse;
};

export function PredictionResult({ prediction }: PredictionResultProps) {
  if (!prediction) {
    return (
      <div className="panel result-empty">
        <p className="eyebrow">Decision cockpit</p>
        <h2>Run a customer scenario</h2>
        <p>Submit the form to estimate churn probability and inspect the top local drivers.</p>
      </div>
    );
  }

  return (
    <div className="panel result-card">
      <RiskGauge probability={prediction.churn_probability} riskLevel={prediction.risk_level} />
      <div className="verdict">
        <span>Prediction</span>
        <strong>{prediction.churn_prediction === "Yes" ? "Likely to churn" : "Likely retained"}</strong>
        <small>Model version {prediction.model_version}</small>
      </div>
    </div>
  );
}
