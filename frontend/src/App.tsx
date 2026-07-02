import { useEffect, useState } from "react";
import "./App.css";
import { getDashboardSummary } from "./api/dashboard";
import type { DashboardSummary } from "./types/dashboard";

function App() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getDashboardSummary()
      .then(setSummary)
      .catch(() => {
        setError("Failed to load dashboard summary.");
      });
  }, []);

  if (error) {
    return <p className="status-message">{error}</p>;
  }

  if (!summary) {
    return <p className="status-message">Loading dashboard...</p>;
  }

  return (
    <main className="dashboard-page">
      <section className="hero">
        <p className="eyebrow">Australian Property Intelligence</p>
        <h1>Property Market Dashboard</h1>
        <p className="hero-description">
          NSW property sales data processed from Valuer General source files.
        </p>
      </section>

      <section className="summary-grid">
        <article className="summary-card">
          <p className="card-label">Total Sales</p>
          <h2>{summary.total_sales.toLocaleString()}</h2>
          <p className="card-caption">Loaded property sale records</p>
        </article>

        <article className="summary-card">
          <p className="card-label">Highest Sale</p>
          <h2>${summary.highest_sale_price?.toLocaleString()}</h2>
          <p className="card-caption">Highest purchase price</p>
        </article>

        <article className="summary-card">
          <p className="card-label">Localities</p>
          <h2>{summary.locality_count.toLocaleString()}</h2>
          <p className="card-caption">Distinct NSW localities</p>
        </article>
      </section>
    </main>
  );
}

export default App;