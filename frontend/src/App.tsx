import { useEffect, useState } from "react";
import "./App.css";
import { getDashboardSummary } from "./api/dashboard";
import type { DashboardSummary } from "./types/dashboard";
import { SummaryCard } from "./components/dashboard/SummaryCard";
import { getTopSales } from "./api/analytics";
import { TopSalesTable } from "./components/dashboard/TopSalesTable";
import type { TopSale } from "./types/property";
import { getSalesByLocality } from "./api/analytics";
import { SalesByLocalityChart } from "./components/dashboard/SalesByLocalityChart";
import type { SalesByLocality } from "./types/property";

function App() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [topSales, setTopSales] = useState<TopSale[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [salesByLocality, setSalesByLocality] = useState<SalesByLocality[]>([]);

  useEffect(() => {
  async function loadDashboardData() {
    try {
      const [summaryData, topSalesData, salesByLocalityData] = await Promise.all([
        getDashboardSummary(),
        getTopSales(10),
        getSalesByLocality(10),
      ]);

      setSummary(summaryData);
      setTopSales(topSalesData);
      setSalesByLocality(salesByLocalityData);
    } catch (error) {
      console.error(error);
      setError("Failed to load dashboard data.");
    }
  }

  loadDashboardData();
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
        <SummaryCard
          title="Total Sales"
          value={summary.total_sales.toLocaleString()}
          caption="Loaded property sale records"
        />

        <SummaryCard
          title="Highest Sale"
          value={`$${summary.highest_sale_price?.toLocaleString()}`}
          caption="Highest purchase price"
        />

        <SummaryCard
          title="Localities"
          value={summary.locality_count.toLocaleString()}
          caption="Distinct NSW localities"
        />
      </section>
      <TopSalesTable sales={topSales} />
      <SalesByLocalityChart data={salesByLocality} />
    </main>
  );
}

export default App;