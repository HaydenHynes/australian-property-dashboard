/* eslint-disable react-hooks/set-state-in-effect -- effects intentionally reset remote request state */
import { useEffect, useState } from "react";
import "./App.css";
import {
  getAvailableYears,
  getMarketTrend,
  getSalesByLocality,
  getSalesByPropertyType,
  getSuburbProfile,
  getTopSales,
} from "./api/analytics";
import { getDashboardSummary } from "./api/dashboard";
import { ChartsSection } from "./components/dashboard/ChartsSection";
import { DashboardHeader } from "./components/dashboard/DashboardHeader";
import { DashboardToolbar } from "./components/dashboard/DashboardToolbar";
import { MarketTrendChart } from "./components/dashboard/MarketTrendChart";
import { SuburbProfileSection } from "./components/dashboard/SuburbProfileSection";
import { SummarySection } from "./components/dashboard/SummarySection";
import { TopSalesTable } from "./components/dashboard/TopSalesTable";
import { useDebouncedValue } from "./hooks/useDebouncedValue";
import type { DashboardSummary } from "./types/dashboard";
import type {
  MarketTrendPoint,
  PropertyTypeSales,
  SalesByLocality,
  SuburbProfile,
  TopSale,
} from "./types/property";

function ErrorPanel({ message }: { message: string }) {
  return (
    <p className="mt-8 rounded-xl border border-red-500/40 bg-red-950/30 p-4 text-red-200">
      {message}
    </p>
  );
}

function App() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [topSales, setTopSales] = useState<TopSale[]>([]);
  const [salesByLocality, setSalesByLocality] = useState<SalesByLocality[]>([]);
  const [propertyTypeSales, setPropertyTypeSales] = useState<PropertyTypeSales[]>([]);
  const [marketTrend, setMarketTrend] = useState<MarketTrendPoint[]>([]);
  const [suburbProfile, setSuburbProfile] = useState<SuburbProfile | null>(null);
  const [availableYears, setAvailableYears] = useState<number[]>([]);

  const [searchTerm, setSearchTerm] = useState("");
  const [topSalesLimit, setTopSalesLimit] = useState(10);
  const [propertyType, setPropertyType] = useState("R");
  const [contractYear, setContractYear] = useState("");
  const debouncedSearchTerm = useDebouncedValue(searchTerm, 350);

  const [loadingSummary, setLoadingSummary] = useState(true);
  const [loadingCharts, setLoadingCharts] = useState(true);
  const [loadingTopSales, setLoadingTopSales] = useState(true);
  const [loadingProfile, setLoadingProfile] = useState(false);
  const [summaryError, setSummaryError] = useState<string | null>(null);
  const [chartsError, setChartsError] = useState<string | null>(null);
  const [salesError, setSalesError] = useState<string | null>(null);

  useEffect(() => {
    getAvailableYears().then(setAvailableYears).catch(() => setAvailableYears([]));
  }, []);

  useEffect(() => {
    let active = true;
    setLoadingSummary(true);
    setSummaryError(null);
    getDashboardSummary(debouncedSearchTerm, propertyType, contractYear)
      .then((data) => active && setSummary(data))
      .catch(() => active && setSummaryError("Summary metrics could not be loaded."))
      .finally(() => active && setLoadingSummary(false));
    return () => { active = false; };
  }, [debouncedSearchTerm, propertyType, contractYear]);

  useEffect(() => {
    let active = true;
    setLoadingCharts(true);
    setChartsError(null);
    Promise.all([
      getSalesByLocality(10, debouncedSearchTerm, propertyType, contractYear),
      getSalesByPropertyType(debouncedSearchTerm, propertyType, contractYear),
      getMarketTrend(debouncedSearchTerm, propertyType, contractYear),
    ])
      .then(([localities, types, trend]) => {
        if (!active) return;
        setSalesByLocality(localities);
        setPropertyTypeSales(types);
        setMarketTrend(trend);
      })
      .catch(() => active && setChartsError("Market charts could not be loaded."))
      .finally(() => active && setLoadingCharts(false));
    return () => { active = false; };
  }, [debouncedSearchTerm, propertyType, contractYear]);

  useEffect(() => {
    let active = true;
    setLoadingTopSales(true);
    setSalesError(null);
    getTopSales(topSalesLimit, debouncedSearchTerm, propertyType, contractYear)
      .then((data) => active && setTopSales(data))
      .catch(() => active && setSalesError("Recent comparable sales could not be loaded."))
      .finally(() => active && setLoadingTopSales(false));
    return () => { active = false; };
  }, [topSalesLimit, debouncedSearchTerm, propertyType, contractYear]);

  useEffect(() => {
    let active = true;
    if (debouncedSearchTerm.trim().length < 2) {
      setSuburbProfile(null);
      return;
    }
    setLoadingProfile(true);
    getSuburbProfile(debouncedSearchTerm, propertyType)
      .then((data) => active && setSuburbProfile(data))
      .catch(() => active && setSuburbProfile(null))
      .finally(() => active && setLoadingProfile(false));
    return () => { active = false; };
  }, [debouncedSearchTerm, propertyType]);

  const clearFilters = () => {
    setSearchTerm("");
    setPropertyType("R");
    setContractYear("");
    setTopSalesLimit(10);
  };

  return (
    <main className="dashboard-page">
      <DashboardHeader />

      {summaryError ? <ErrorPanel message={summaryError} /> : (
        <SummarySection summary={summary} loading={loadingSummary} />
      )}

      <DashboardToolbar
        searchTerm={searchTerm}
        onSearchTermChange={setSearchTerm}
        topSalesLimit={topSalesLimit}
        onTopSalesLimitChange={setTopSalesLimit}
        propertyType={propertyType}
        onPropertyTypeChange={setPropertyType}
        contractYear={contractYear}
        onContractYearChange={setContractYear}
        availableYears={availableYears}
        onClear={clearFilters}
      />

      <SuburbProfileSection
        profile={suburbProfile}
        loading={loadingProfile}
        hasSearch={debouncedSearchTerm.trim().length >= 2}
      />

      {chartsError ? <ErrorPanel message={chartsError} /> : (
        <>
          <MarketTrendChart data={marketTrend} loading={loadingCharts} />
          <ChartsSection
            salesByLocality={salesByLocality}
            propertyTypeSales={propertyTypeSales}
            loading={loadingCharts}
          />
        </>
      )}

      {salesError ? <ErrorPanel message={salesError} /> : (
        <TopSalesTable sales={topSales} loading={loadingTopSales} />
      )}
    </main>
  );
}

export default App;
