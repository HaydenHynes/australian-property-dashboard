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