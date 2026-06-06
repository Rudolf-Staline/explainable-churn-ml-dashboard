import type { CSSProperties } from "react";

type RiskGaugeProps = {
  probability: number;
  riskLevel: string;
};

export function RiskGauge({ probability, riskLevel }: RiskGaugeProps) {
  const percentage = Math.round(probability * 100);
  return (
    <div className="risk-gauge" style={{ "--risk": `${percentage}%` } as CSSProperties}>
      <div className="risk-gauge__ring">
        <span>{percentage}%</span>
      </div>
      <div>
        <p className="eyebrow">Churn probability</p>
        <h3 className={`risk risk--${riskLevel.toLowerCase()}`}>{riskLevel} risk</h3>
      </div>
    </div>
  );
}
