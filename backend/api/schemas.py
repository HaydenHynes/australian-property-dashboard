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
