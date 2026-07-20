import { apiClient } from "./client";
import type {
  RentalFilters,
  RentalProfile,
  RentalScreenResult,
  RentalTrendPoint,
} from "../types/rental";

function rentalFilters(filters: RentalFilters) {
  return {
    dwelling_type: filters.dwellingType || undefined,
    bedrooms: filters.bedrooms || undefined,
  };
}

export async function getRentalProfile(
  locality: string,
  filters: RentalFilters = {},
): Promise<RentalProfile> {
  const response = await apiClient.get<RentalProfile>("/rental/profile", {
    params: { locality, ...rentalFilters(filters) },
  });
  return response.data;
}

export async function getRentalTrend(
  locality: string,
  filters: RentalFilters = {},
): Promise<RentalTrendPoint[]> {
  const response = await apiClient.get<RentalTrendPoint[]>("/rental/trend", {
    params: { locality, ...rentalFilters(filters) },
  });
  return response.data;
}

export async function compareRentals(
  localities: string[],
  filters: RentalFilters = {},
): Promise<RentalProfile[]> {
  const response = await apiClient.get<RentalProfile[]>("/rental/compare", {
    params: { localities, ...rentalFilters(filters) },
    paramsSerializer: { indexes: null },
  });
  return response.data;
}

export async function screenRentals(params: {
  maxPrice: number;
  minYield: number;
  minRentalCount: number;
  dwellingType?: string;
  bedrooms?: string;
}): Promise<RentalScreenResult[]> {
  const response = await apiClient.get<RentalScreenResult[]>("/rental/screen", {
    params: {
      max_price: params.maxPrice,
      min_yield: params.minYield,
      min_rental_count: params.minRentalCount,
      dwelling_type: params.dwellingType || undefined,
      bedrooms: params.bedrooms || undefined,
    },
  });
  return response.data;
}
