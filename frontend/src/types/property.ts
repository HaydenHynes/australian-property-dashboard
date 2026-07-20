export interface TopSale {
  locality: string | null;
  street_name: string | null;
  house_number: string | null;
  purchase_price: number | null;
  contract_date: string | null;
}

export interface SalesByLocality {
  locality: string | null;
  sales_count: number;
}

export interface PropertyTypeSales {
  property_type: string | null;
  sales_count: number;
}

export interface MarketTrendPoint {
  period: string;
  median_sale_price: number | null;
  sales_count: number;
}

export interface SuburbProfile {
  locality: string;
  median_sale_price: number | null;
  sales_count_12m: number;
  data_as_of: string | null;
  growth_1y_pct: number | null;
  growth_3y_annualised_pct: number | null;
  growth_5y_annualised_pct: number | null;
}
