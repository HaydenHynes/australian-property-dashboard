export interface DashboardSummary {
  total_sales: number;
  median_sale_price: number | null;
  annual_growth_pct: number | null;
  locality_count: number;
  excluded_sales: number;
  data_as_of: string | null;
}
