import { apiClient } from "./client";
import type { DashboardSummary } from "../types/dashboard";

export async function getDashboardSummary(
  search = "",
  propertyType = "",
  contractYear = "",
): Promise<DashboardSummary> {
  const response = await apiClient.get<DashboardSummary>(
    "/dashboard/summary",
    {
      params: {
        search: search || undefined,
        property_type: propertyType || undefined,
        contract_year: contractYear || undefined,
      },
    },
  );

  return response.data;
}
