import { useEffect, useState } from "react";
import "./App.css";
import {
  getSalesByLocality,
  getSalesByPropertyType,
  getTopSales,
} from "./api/analytics";
import { getDashboardSummary } from "./api/dashboard";
import { ChartsSection } from "./components/dashboard/ChartsSection";
import { DashboardHeader } from "./components/dashboard/DashboardHeader";
import { DashboardToolbar } from "./components/dashboard/DashboardToolbar";
import { SummarySection } from "./components/dashboard/SummarySection";
import { TopSalesTable } from "./components/dashboard/TopSalesTable";
import { useDebouncedValue } from "./hooks/useDebouncedValue";
import type { DashboardSummary } from "./types/dashboard";
import type {
  PropertyTypeSales,
  SalesByLocality,
  TopSale,
} from "./types/property";

function App() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [topSales, setTopSales] = useState<TopSale[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [salesByLocality, setSalesByLocality] = useState<SalesByLocality[]>([]);
  const [propertyTypeSales, setPropertyTypeSales] = useState<PropertyTypeSales[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [topSalesLimit, setTopSalesLimit] = useState(10);
  const [propertyType, setPropertyType] = useState("");

  const debouncedSearchTerm = useDebouncedValue(searchTerm, 300);

  useEffect(() => {
    async function loadChartsData() {
      try {
        const [salesByLocalityData, propertyTypeSalesData] =
          await Promise.all([
            getSalesByLocality(10, debouncedSearchTerm, propertyType),
            getSalesByPropertyType(debouncedSearchTerm, propertyType),
          ]);

        setSalesByLocality(salesByLocalityData);
        setPropertyTypeSales(propertyTypeSalesData);
      } catch (error) {
        console.error(error);
        setError("Failed to load chart data.");
      }
    }

    loadChartsData();
  }, [debouncedSearchTerm, propertyType]);

  useEffect(() => {
    async function loadSummaryData() {
      try {
        const summaryData = await getDashboardSummary(
          debouncedSearchTerm,
          propertyType,
        );
        setSummary(summaryData);
      } catch (error) {
        console.error(error);
        setError("Failed to load dashboard summary.");
      }
    }

    loadSummaryData();
  }, [debouncedSearchTerm, propertyType]);

  useEffect(() => {
  async function loadTopSales() {
    try {
      const topSalesData = await getTopSales(
        topSalesLimit,
        debouncedSearchTerm,
        propertyType,
      );

      console.log("Top sales returned:", topSalesData);

      setTopSales(topSalesData);
    } catch (error) {
      console.error(error);
      setError("Failed to load top sales.");
    }
  }

  loadTopSales();
}, [topSalesLimit, debouncedSearchTerm, propertyType]);

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
        propertyType={propertyType}
        onPropertyTypeChange={setPropertyType}
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