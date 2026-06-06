import type { ModelInfo } from "../api/client";

type MetricsCardsProps = {
  modelInfo?: ModelInfo;
  apiHealthy: boolean;
};

export function MetricsCards({ modelInfo, apiHealthy }: MetricsCardsProps) {
  const metrics = modelInfo?.metrics ?? {};
  return (
    <section className="metrics-grid">
      <article className="metric-card">
        <span>Model</span>
        <strong>{modelInfo?.model_type ?? "Not trained"}</strong>
      </article>
      <article className="metric-card">
        <span>ROC-AUC</span>
        <strong>{typeof metrics.roc_auc === "number" ? metrics.roc_auc.toFixed(3) : "—"}</strong>
      </article>
      <article className="metric-card">
        <span>Recall priority</span>
        <strong>{typeof metrics.recall === "number" ? metrics.recall.toFixed(3) : "—"}</strong>
      </article>
      <article className="metric-card">
        <span>API status</span>
        <strong className={apiHealthy ? "safe" : "danger"}>{apiHealthy ? "Online" : "Offline"}</strong>
      </article>
      <article className="metric-card">
        <span>Features</span>
        <strong>{modelInfo?.feature_count ?? "—"}</strong>
      </article>
    </section>
  );
}
