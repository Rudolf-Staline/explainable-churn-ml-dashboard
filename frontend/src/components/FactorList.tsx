import type { Factor } from "../api/client";

type FactorListProps = {
  factors: Factor[];
};

export function FactorList({ factors }: FactorListProps) {
  return (
    <div className="panel">
      <p className="eyebrow">Local explanation</p>
      <h2>Top risk factors</h2>
      <div className="factor-list">
        {factors.map((factor) => (
          <div className="factor" key={`${factor.feature}-${factor.contribution}`}>
            <div>
              <strong>{factor.feature}</strong>
              <span>{factor.direction === "increases_risk" ? "Increases risk" : "Decreases risk"}</span>
            </div>
            <b className={factor.direction === "increases_risk" ? "danger" : "safe"}>{factor.contribution.toFixed(3)}</b>
          </div>
        ))}
      </div>
    </div>
  );
}
