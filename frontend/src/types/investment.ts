export interface DemographicProfile {
  locality: string;
  postcodes: string[];
  population_2016: number;
  population_2021: number;
  population_growth_5y_pct: number;
  population_growth_annualised_pct: number;
  median_household_income_2016: number;
  median_household_income_2021: number;
  income_growth_5y_pct: number;
  income_growth_annualised_pct: number;
  latitude: number;
  longitude: number;
  data_as_of: number;
  geography_level: string;
}

export interface ScoreComponent {
  key: string;
  label: string;
  raw_value: number;
  percentile_score: number;
  weight_pct: number;
  contribution: number;
  explanation: string;
}

export interface InvestmentScore {
  locality: string;
  postcodes: string[];
  latitude: number;
  longitude: number;
  median_weekly_rent: number;
  rent_growth_1y_pct: number;
  rental_count: number;
  median_sale_price: number;
  price_growth_5y_annualised_pct: number;
  sales_count: number;
  gross_yield_pct: number;
  population_2021: number;
  population_growth_5y_pct: number;
  median_household_income_weekly: number;
  income_growth_5y_pct: number;
  investment_score: number;
  confidence: string;
  rental_data_as_of: string;
  sales_data_as_of: string;
  demographic_data_as_of: number;
  components: ScoreComponent[];
}

export type RankingSort =
  | "score"
  | "yield"
  | "price_growth"
  | "rent_growth"
  | "population_growth"
  | "income_growth";

export interface RankingFilters {
  maxPrice: number;
  minYield: number;
  minScore: number;
  search?: string;
  sort: RankingSort;
  limit?: number;
}
