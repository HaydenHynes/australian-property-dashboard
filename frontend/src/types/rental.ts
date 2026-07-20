export interface RentalProfile {
  locality: string;
  postcodes: string[];
  dwelling_type: string;
  bedrooms: number | null;
  median_weekly_rent: number | null;
  lower_quartile_rent: number | null;
  upper_quartile_rent: number | null;
  lodgement_count: number;
  confidence: "low" | "medium" | "high";
  rent_growth_1y_pct: number | null;
  median_sale_price: number | null;
  gross_yield_pct: number | null;
  data_as_of: string | null;
}

export interface RentalTrendPoint {
  month: string;
  median_weekly_rent: number;
  lodgement_count: number;
  confidence: "low" | "medium" | "high";
}

export interface RentalScreenResult {
  locality: string;
  postcodes: string[];
  median_weekly_rent: number;
  median_sale_price: number;
  gross_yield_pct: number;
  rental_count: number;
  sales_count: number;
  confidence: "low" | "medium" | "high";
}

export interface RentalFilters {
  dwellingType?: string;
  bedrooms?: string;
}
