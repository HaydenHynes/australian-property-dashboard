import { apiClient } from "./client";
import type {
  PropertyTypeSales,
  SalesByLocality,
  TopSale,
} from "../types/property";

export async function getTopSales(
  limit = 10,
  search = "",
  propertyType = "",
): Promise<TopSale[]> {
  const response = await apiClient.get<TopSale[]>("/analytics/top-sales", {
    params: {
      limit,
      search,
      property_type: propertyType,
    },
  });

  return response.data;
}

export async function getSalesByLocality(
  limit = 10,
  search = "",
  propertyType = "",
): Promise<SalesByLocality[]> {
  const response = await apiClient.get<SalesByLocality[]>(
    "/analytics/sales-by-locality",
    {
      params: {
        limit,
        search,
        property_type: propertyType,
      },
    },
  );

  return response.data;
}

export async function getSalesByPropertyType(
  search = "",
  propertyType = "",
): Promise<PropertyTypeSales[]> {
  const response = await apiClient.get<PropertyTypeSales[]>(
    "/analytics/sales-by-property-type",
    {
      params: {
        search,
        property_type: propertyType,
      },
    },
  );

  return response.data;
}