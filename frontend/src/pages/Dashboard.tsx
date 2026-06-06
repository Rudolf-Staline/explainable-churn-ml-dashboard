import { useEffect, useState } from "react";
import type { CustomerInput, ModelInfo, PredictionResponse } from "../api/client";
import { getModelInfo, healthCheck, predictCustomer } from "../api/client";
import { DemoCustomersTable } from "../components/DemoCustomersTable";
import { FactorList } from "../components/FactorList";
import { MetricsCards } from "../components/MetricsCards";
import { PredictionForm } from "../components/PredictionForm";
import { PredictionResult } from "../components/PredictionResult";

export function Dashboard() {
  const [modelInfo, setModelInfo] = useState<ModelInfo>();
  const [apiHealthy, setApiHealthy] = useState(false);
  const [prediction, setPrediction] = useState<PredictionResponse>();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>();

  useEffect(() => {
    healthCheck().then((health) => setApiHealthy(health.status === "ok" && health.model_loaded)).catch(() => setApiHealthy(false));
    getModelInfo().then(setModelInfo).catch((err) => setError(err.message));
  }, []);

  async function score(customer: CustomerInput) {
    setLoading(true);
    setError(undefined);
    try {
      setPrediction(await predictCustomer(customer));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Prediction failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="dashboard-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">Project 02 · Explainable ML Dashboard</p>
          <h1>Customer churn risk cockpit</h1>
          <p>Score customer churn risk, inspect model confidence, and surface the factors that drive retention decisions.</p>
        </div>
        <div className="status-pill">{apiHealthy ? "API connected" : "API/model unavailable"}</div>
      </header>

      {error && <div className="error-banner">{error}</div>}
      <MetricsCards modelInfo={modelInfo} apiHealthy={apiHealthy} />

      <section className="workspace-grid">
        <PredictionForm onSubmit={score} loading={loading} />
        <div className="right-rail">
          <PredictionResult prediction={prediction} />
          {prediction && <FactorList factors={prediction.top_factors} />}
          <DemoCustomersTable onSelect={score} />
          <div className="panel report-summary">
            <p className="eyebrow">Model report</p>
            <h2>Operating note</h2>
            <p>Recall and ROC-AUC are prioritized because missing a truly at-risk customer is more costly than flagging a customer for follow-up.</p>
          </div>
        </div>
      </section>
    </main>
  );
}
