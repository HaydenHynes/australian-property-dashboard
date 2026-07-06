import { useEffect, useState } from "react";
import "./App.css";
import { getDashboardSummary } from "./api/dashboard";
import type { DashboardSummary } from "./types/dashboard";
import { getTopSales } from "./api/analytics";
import { TopSalesTable } from "./components/dashboard/TopSalesTable";
import type { TopSale } from "./types/property";
import { getSalesByLocality } from "./api/analytics";
import type { SalesByLocality } from "./types/property";
import { getSalesByPropertyType } from "./api/analytics";
import type { PropertyTypeSales } from "./types/property";
import { DashboardHeader } from "./components/dashboard/DashboardHeader";
import { SummarySection } from "./components/dashboard/SummarySection";
import { ChartsSection } from "./components/dashboard/ChartsSection";
import { DashboardToolbar } from "./components/dashboard/DashboardToolbar";
import { useDebouncedValue } from "./hooks/useDebouncedValue";

function App() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [topSales, setTopSales] = useState<TopSale[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [salesByLocality, setSalesByLocality] = useState<SalesByLocality[]>([]);
  const [propertyTypeSales, setPropertyTypeSales] = useState<PropertyTypeSales[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const debouncedSearchTerm = useDebouncedValue(searchTerm, 300);
  const [topSalesLimit, setTopSalesLimit] = useState(10);

  useEffect(() => {
    async function loadChartsData() {
      try {
        const [salesByLocalityData, propertyTypeSalesData] =
          await Promise.all([
            getSalesByLocality(10, debouncedSearchTerm),
            getSalesByPropertyType(debouncedSearchTerm),
          ]);

        setSalesByLocality(salesByLocalityData);
        setPropertyTypeSales(propertyTypeSalesData);
      } catch (error) {
        console.error(error);
        setError("Failed to load chart data.");
      }
    }

    loadChartsData();
  }, [debouncedSearchTerm]);

useEffect(() => {
  async function loadSummaryData() {
    try {
      const summaryData = await getDashboardSummary(debouncedSearchTerm);
      setSummary(summaryData);
    } catch (error) {
      console.error(error);
      setError("Failed to load dashboard summary.");
    }
  }

  loadSummaryData();
}, [debouncedSearchTerm]);

  useEffect(() => {
    async function loadTopSales() {
      try {
        const topSalesData = await getTopSales(topSalesLimit, debouncedSearchTerm);
        setTopSales(topSalesData);
      } catch (error) {
        console.error(error);
        setError("Failed to load top sales.");
      }
    }

    loadTopSales();
  }, [topSalesLimit, debouncedSearchTerm]);

  if (error) {
    return <p className="status-message">{error}</p>;
  }

  if (!summary) {
    return <p className="status-message">Loading dashboard...</p>;
  }

  return (
    <main className="dashboard-page">
      <DashboardHeader />

      <SummarySection summary={summary} />

      <DashboardToolbar
        searchTerm={searchTerm}
        onSearchTermChange={setSearchTerm}
        topSalesLimit={topSalesLimit}
        onTopSalesLimitChange={setTopSalesLimit}
      />

      <ChartsSection
        salesByLocality={salesByLocality}
        propertyTypeSales={propertyTypeSales}
      />

      <TopSalesTable sales={topSales} />
    </main>
  );
}

export default App;