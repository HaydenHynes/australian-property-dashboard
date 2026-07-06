import { apiClient } from "./client";
import type { DashboardSummary } from "../types/dashboard";

export async function getDashboardSummary(
  search = "",
  propertyType = "",
): Promise<DashboardSummary> {
  const response = await apiClient.get<DashboardSummary>(
    "/dashboard/summary",
    {
      params: {
        search,
        property_type: propertyType,
      },
    },
  );

  return response.data;
}