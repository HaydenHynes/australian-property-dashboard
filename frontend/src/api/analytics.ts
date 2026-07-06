import { apiClient } from "./client";
import type { PropertyTypeSales, SalesByLocality, TopSale } from "../types/property";


export async function getTopSales(
  limit = 10,
  search = "",
): Promise<TopSale[]> {
  const response = await apiClient.get<TopSale[]>("/analytics/top-sales", {
    params: {
      limit,
      search,
    },
  });

  return response.data;
}

export async function getSalesByLocality(
  limit = 10,
): Promise<SalesByLocality[]> {
  const response = await apiClient.get<SalesByLocality[]>(
    "/analytics/sales-by-locality",
    {
      params: { limit },
    },
  );

  return response.data;
}

export async function getSalesByPropertyType(): Promise<PropertyTypeSales[]> {
  const response = await apiClient.get<PropertyTypeSales[]>(
    "/analytics/sales-by-property-type",
  );

  return response.data;
}