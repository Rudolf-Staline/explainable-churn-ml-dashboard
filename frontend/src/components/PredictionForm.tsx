import { FormEvent, useState } from "react";
import type { CustomerInput } from "../api/client";

const defaultCustomer: CustomerInput = {
  gender: "Female",
  SeniorCitizen: 0,
  Partner: "No",
  Dependents: "No",
  tenure: 3,
  PhoneService: "Yes",
  MultipleLines: "No",
  InternetService: "Fiber optic",
  OnlineSecurity: "No",
  OnlineBackup: "No",
  DeviceProtection: "No",
  TechSupport: "No",
  StreamingTV: "No",
  StreamingMovies: "No",
  Contract: "Month-to-month",
  PaperlessBilling: "Yes",
  PaymentMethod: "Electronic check",
  MonthlyCharges: 74.4,
  TotalCharges: 229.55,
};

const selectOptions: Record<keyof CustomerInput, string[] | undefined> = {
  gender: ["Female", "Male"],
  SeniorCitizen: undefined,
  Partner: ["Yes", "No"],
  Dependents: ["Yes", "No"],
  tenure: undefined,
  PhoneService: ["Yes", "No"],
  MultipleLines: ["No", "Yes", "No phone service"],
  InternetService: ["DSL", "Fiber optic", "No"],
  OnlineSecurity: ["No", "Yes", "No internet service"],
  OnlineBackup: ["No", "Yes", "No internet service"],
  DeviceProtection: ["No", "Yes", "No internet service"],
  TechSupport: ["No", "Yes", "No internet service"],
  StreamingTV: ["No", "Yes", "No internet service"],
  StreamingMovies: ["No", "Yes", "No internet service"],
  Contract: ["Month-to-month", "One year", "Two year"],
  PaperlessBilling: ["Yes", "No"],
  PaymentMethod: ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"],
  MonthlyCharges: undefined,
  TotalCharges: undefined,
};

const fields = Object.keys(defaultCustomer) as (keyof CustomerInput)[];

export function PredictionForm({ onSubmit, loading }: { onSubmit: (customer: CustomerInput) => void; loading: boolean }) {
  const [customer, setCustomer] = useState<CustomerInput>(defaultCustomer);

  function updateField(field: keyof CustomerInput, value: string) {
    const numericFields = ["SeniorCitizen", "tenure", "MonthlyCharges", "TotalCharges"];
    setCustomer((current) => ({ ...current, [field]: numericFields.includes(field) ? Number(value) : value }));
  }

  function submit(event: FormEvent) {
    event.preventDefault();
    onSubmit(customer);
  }

  return (
    <form className="panel prediction-form" onSubmit={submit}>
      <div className="section-heading">
        <p className="eyebrow">Single customer scoring</p>
        <h2>Prediction form</h2>
      </div>
      <div className="form-grid">
        {fields.map((field) => (
          <label key={field}>
            <span>{field}</span>
            {selectOptions[field] ? (
              <select value={String(customer[field])} onChange={(event) => updateField(field, event.target.value)}>
                {selectOptions[field]?.map((option) => <option key={option}>{option}</option>)}
              </select>
            ) : (
              <input type="number" step="0.01" value={customer[field]} onChange={(event) => updateField(field, event.target.value)} />
            )}
          </label>
        ))}
      </div>
      <button type="submit" disabled={loading}>{loading ? "Scoring..." : "Predict churn risk"}</button>
    </form>
  );
}
