export type CustomerInput = {
  gender: string;
  SeniorCitizen: number;
  Partner: string;
  Dependents: string;
  tenure: number;
  PhoneService: string;
  MultipleLines: string;
  InternetService: string;
  OnlineSecurity: string;
  OnlineBackup: string;
  DeviceProtection: string;
  TechSupport: string;
  StreamingTV: string;
  StreamingMovies: string;
  Contract: string;
  PaperlessBilling: string;
  PaymentMethod: string;
  MonthlyCharges: number;
  TotalCharges: number;
};

export type Factor = {
  feature: string;
  contribution: number;
  direction: "increases_risk" | "decreases_risk";
};

export type PredictionResponse = {
  churn_probability: number;
  churn_prediction: "Yes" | "No";
  risk_level: "Low" | "Medium" | "High";
  top_factors: Factor[];
  model_version: string;
};

export type ModelInfo = {
  model_type: string;
  training_date: string;
  metrics: Record<string, number | number[][]>;
  feature_count: number;
  target: string;
  threshold: number;
  model_version: string;
};

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(error.detail ?? "API request failed");
  }
  return response.json() as Promise<T>;
}

export function predictCustomer(customer: CustomerInput): Promise<PredictionResponse> {
  return request<PredictionResponse>("/predict", { method: "POST", body: JSON.stringify(customer) });
}

export function getModelInfo(): Promise<ModelInfo> {
  return request<ModelInfo>("/model-info");
}

export function healthCheck(): Promise<{ status: string; model_loaded: boolean }> {
  return request<{ status: string; model_loaded: boolean }>("/health");
}
