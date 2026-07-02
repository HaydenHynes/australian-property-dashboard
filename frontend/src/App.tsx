import { useEffect, useState } from "react";
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
    return <p>{error}</p>;
  }

  if (!summary) {
    return <p>Loading dashboard...</p>;
  }

  return (
    <main>
      <h1>Australian Property Dashboard</h1>

      <section>
        <div>
          <h2>Total Sales</h2>
          <p>{summary.total_sales}</p>
        </div>

        <div>
          <h2>Highest Sale</h2>
          <p>${summary.highest_sale_price?.toLocaleString()}</p>
        </div>

        <div>
          <h2>Localities</h2>
          <p>{summary.locality_count}</p>
        </div>
      </section>
    </main>
  );
}

export default App;