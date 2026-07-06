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