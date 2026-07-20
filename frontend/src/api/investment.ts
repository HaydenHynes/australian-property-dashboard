import { apiClient } from "./client";
import type {
  DemographicProfile,
  InvestmentScore,
  RankingFilters,
} from "../types/investment";

export async function getDemographicProfile(
  locality: string,
): Promise<DemographicProfile> {
  const response = await apiClient.get<DemographicProfile>(
    "/investment/demographics",
    { params: { locality } },
  );
  return response.data;
}

export async function getInvestmentProfile(
  locality: string,
): Promise<InvestmentScore> {
  const response = await apiClient.get<InvestmentScore>("/investment/profile", {
    params: { locality },
  });
  return response.data;
}

export async function getInvestmentRankings(
  filters: RankingFilters,
): Promise<InvestmentScore[]> {
  const response = await apiClient.get<InvestmentScore[]>(
    "/investment/rankings",
    {
      params: {
        max_price: filters.maxPrice,
        min_yield: filters.minYield,
        min_score: filters.minScore,
        search: filters.search || undefined,
        sort: filters.sort,
        limit: filters.limit ?? 150,
      },
    },
  );
  return response.data;
}

export async function compareInvestments(
  localities: string[],
): Promise<InvestmentScore[]> {
  const response = await apiClient.get<InvestmentScore[]>("/investment/compare", {
    params: { localities },
    paramsSerializer: { indexes: null },
  });
  return response.data;
}
