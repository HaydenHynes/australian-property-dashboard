"""
FastAPI response schemas.
"""

from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class TotalSalesResponse(BaseModel):
    """Total sales response."""

    total_sales: int


class TopSaleResponse(BaseModel):
    """Top sale response."""

    locality: str | None
    street_name: str | None
    house_number: str | None
    purchase_price: int | None
    contract_date: date | None


class SalesByLocalityResponse(BaseModel):
    """Sales by locality response."""

    locality: str | None
    sales_count: int


class AveragePriceByLocalityResponse(BaseModel):
    """Average price by locality response."""

    locality: str | None
    average_purchase_price: Decimal | None


class PropertyTypeSalesResponse(BaseModel):
    """Property type sales response."""

    property_type: str | None
    sales_count: int


class MarketTrendPointResponse(BaseModel):
    """Quarterly median sale price and sales volume."""

    period: date
    median_sale_price: float | None
    sales_count: int


class SuburbProfileResponse(BaseModel):
    """Investor-oriented suburb profile."""

    locality: str
    median_sale_price: float | None
    sales_count_12m: int
    data_as_of: date | None
    growth_1y_pct: float | None
    growth_3y_annualised_pct: float | None
    growth_5y_annualised_pct: float | None


class AvailableYearsResponse(BaseModel):
    years: list[int]


class RentalProfileResponse(BaseModel):
    locality: str
    postcodes: list[str]
    dwelling_type: str
    bedrooms: int | None
    median_weekly_rent: float | None
    lower_quartile_rent: float | None
    upper_quartile_rent: float | None
    lodgement_count: int
    confidence: str
    rent_growth_1y_pct: float | None
    median_sale_price: float | None
    gross_yield_pct: float | None
    data_as_of: date | None


class RentalTrendPointResponse(BaseModel):
    month: date
    median_weekly_rent: float
    lodgement_count: int
    confidence: str


class RentalScreenResultResponse(BaseModel):
    locality: str
    postcodes: list[str]
    median_weekly_rent: float
    median_sale_price: float
    gross_yield_pct: float
    rental_count: int
    sales_count: int
    confidence: str


class DemographicProfileResponse(BaseModel):
    locality: str
    postcodes: list[str]
    population_2016: int
    population_2021: int
    population_growth_5y_pct: float
    population_growth_annualised_pct: float
    median_household_income_2016: float
    median_household_income_2021: float
    income_growth_5y_pct: float
    income_growth_annualised_pct: float
    latitude: float
    longitude: float
    data_as_of: int
    geography_level: str


class ScoreComponentResponse(BaseModel):
    key: str
    label: str
    raw_value: float
    percentile_score: float
    weight_pct: float
    contribution: float
    explanation: str


class InvestmentScoreResponse(BaseModel):
    locality: str
    postcodes: list[str]
    latitude: float
    longitude: float
    median_weekly_rent: float
    rent_growth_1y_pct: float
    rental_count: int
    median_sale_price: float
    price_growth_5y_annualised_pct: float
    sales_count: int
    gross_yield_pct: float
    population_2021: int
    population_growth_5y_pct: float
    median_household_income_weekly: float
    income_growth_5y_pct: float
    investment_score: float
    confidence: str
    rental_data_as_of: date
    sales_data_as_of: date
    demographic_data_as_of: int
    components: list[ScoreComponentResponse]
