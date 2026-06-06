import type { CustomerInput } from "../api/client";

const demoCustomers: CustomerInput[] = [
  {
    gender: "Female",
    SeniorCitizen: 0,
    Partner: "No",
    Dependents: "No",
    tenure: 2,
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
    MonthlyCharges: 70.7,
    TotalCharges: 151.65,
  },
  {
    gender: "Male",
    SeniorCitizen: 0,
    Partner: "Yes",
    Dependents: "Yes",
    tenure: 69,
    PhoneService: "Yes",
    MultipleLines: "Yes",
    InternetService: "No",
    OnlineSecurity: "No internet service",
    OnlineBackup: "No internet service",
    DeviceProtection: "No internet service",
    TechSupport: "No internet service",
    StreamingTV: "No internet service",
    StreamingMovies: "No internet service",
    Contract: "Two year",
    PaperlessBilling: "No",
    PaymentMethod: "Mailed check",
    MonthlyCharges: 25.35,
    TotalCharges: 1715.1,
  },
];

export function DemoCustomersTable({ onSelect }: { onSelect: (customer: CustomerInput) => void }) {
  return (
    <div className="panel demo-table">
      <p className="eyebrow">Demo batch</p>
      <h2>Example customer profiles</h2>
      <table>
        <thead>
          <tr>
            <th>Profile</th>
            <th>Contract</th>
            <th>Tenure</th>
            <th>Monthly</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {demoCustomers.map((customer, index) => (
            <tr key={`${customer.Contract}-${customer.tenure}`}>
              <td>{index === 0 ? "At-risk new fiber customer" : "Stable long-term customer"}</td>
              <td>{customer.Contract}</td>
              <td>{customer.tenure} mo</td>
              <td>${customer.MonthlyCharges}</td>
              <td><button className="ghost" onClick={() => onSelect(customer)}>Score</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
