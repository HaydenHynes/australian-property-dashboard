import { apiClient } from "./client";
import type { SalesByLocality, TopSale } from "../types/property";

export async function getTopSales(limit = 10): Promise<TopSale[]> {
  const response = await apiClient.get<TopSale[]>("/analytics/top-sales", {
    params: { limit },
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