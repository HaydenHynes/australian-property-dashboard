import { apiClient } from "./client";
import type {
  MarketTrendPoint,
  PropertyTypeSales,
  SalesByLocality,
  SuburbProfile,
  TopSale,
} from "../types/property";

function filters(search: string, propertyType: string, contractYear = "") {
  return {
    search: search || undefined,
    property_type: propertyType || undefined,
    contract_year: contractYear || undefined,
  };
}

export async function getTopSales(
  limit = 10,
  search = "",
  propertyType = "",
  contractYear = "",
): Promise<TopSale[]> {
  const response = await apiClient.get<TopSale[]>("/analytics/top-sales", {
    params: { limit, ...filters(search, propertyType, contractYear) },
  });
  return response.data;
}

export async function getSalesByLocality(
  limit = 10,
  search = "",
  propertyType = "",
  contractYear = "",
): Promise<SalesByLocality[]> {
  const response = await apiClient.get<SalesByLocality[]>(
    "/analytics/sales-by-locality",
    { params: { limit, ...filters(search, propertyType, contractYear) } },
  );
  return response.data;
}

export async function getSalesByPropertyType(
  search = "",
  propertyType = "",
  contractYear = "",
): Promise<PropertyTypeSales[]> {
  const response = await apiClient.get<PropertyTypeSales[]>(
    "/analytics/sales-by-property-type",
    { params: filters(search, propertyType, contractYear) },
  );
  return response.data;
}

export async function getMarketTrend(
  search = "",
  propertyType = "",
  contractYear = "",
): Promise<MarketTrendPoint[]> {
  const response = await apiClient.get<MarketTrendPoint[]>(
    "/analytics/market-trend",
    { params: filters(search, propertyType, contractYear) },
  );
  return response.data;
}

export async function getSuburbProfile(
  locality: string,
  propertyType = "R",
): Promise<SuburbProfile> {
  const response = await apiClient.get<SuburbProfile>(
    "/analytics/suburb-profile",
    { params: { locality, property_type: propertyType || undefined } },
  );
  return response.data;
}

export async function getAvailableYears(): Promise<number[]> {
  const response = await apiClient.get<{ years: number[] }>(
    "/analytics/available-years",
  );
  return response.data.years;
}
