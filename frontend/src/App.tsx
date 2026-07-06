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

  const [loadingSummary, setLoadingSummary] = useState(true);
  const [loadingCharts, setLoadingCharts] = useState(true);
  const [loadingTopSales, setLoadingTopSales] = useState(true);
  const [contractYear, setContractYear] = useState("");

  useEffect(() => {
    async function loadChartsData() {
      try {
        const [salesByLocalityData, propertyTypeSalesData] =
          await Promise.all([
            getSalesByLocality(10, debouncedSearchTerm, propertyType, contractYear,),
            getSalesByPropertyType(debouncedSearchTerm, propertyType, contractYear,),
          ]);

        setSalesByLocality(salesByLocalityData);
        setPropertyTypeSales(propertyTypeSalesData);
      } catch (error) {
        console.error(error);
        setError("Failed to load chart data.");
      } finally {
        setLoadingCharts(false);
      }
    }

    loadChartsData();
  }, [debouncedSearchTerm, propertyType, contractYear]);

  useEffect(() => {
    async function loadSummaryData() {
      try {
        const summaryData = await getDashboardSummary(
          debouncedSearchTerm,
          propertyType,
          contractYear,
        );

        setSummary(summaryData);
      } catch (error) {
        console.error(error);
        setError("Failed to load dashboard summary.");
      } finally {
        setLoadingSummary(false);
      }
    }

    loadSummaryData();
  }, [debouncedSearchTerm, propertyType, contractYear]);

  useEffect(() => {
    async function loadTopSales() {
      try {
        const topSalesData = await getTopSales(
          topSalesLimit,
          debouncedSearchTerm,
          propertyType,
          contractYear,
        );

        setTopSales(topSalesData);
      } catch (error) {
        console.error(error);
        setError("Failed to load top sales.");
      } finally {
        setLoadingTopSales(false);
      }
    }

    loadTopSales();
  }, [topSalesLimit, debouncedSearchTerm, propertyType, contractYear]);

  if (error) {
    return <p className="status-message">{error}</p>;
  }

  return (
    <main className="dashboard-page">
      <DashboardHeader />

      <SummarySection summary={summary} loading={loadingSummary} />

      <DashboardToolbar
        searchTerm={searchTerm}
        onSearchTermChange={setSearchTerm}
        topSalesLimit={topSalesLimit}
        onTopSalesLimitChange={setTopSalesLimit}
        propertyType={propertyType}
        onPropertyTypeChange={setPropertyType}
        contractYear={contractYear}
        onContractYearChange={setContractYear}
      />

      <ChartsSection
        salesByLocality={salesByLocality}
        propertyTypeSales={propertyTypeSales}
        loading={loadingCharts}
      />

      <TopSalesTable sales={topSales} loading={loadingTopSales} />
    </main>
  );
}

export default App;