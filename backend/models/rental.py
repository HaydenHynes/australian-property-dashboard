"""Rental investment analytics models."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class RentalProfile:
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


@dataclass(frozen=True)
class RentalTrendPoint:
    month: date
    median_weekly_rent: float
    lodgement_count: int
    confidence: str


@dataclass(frozen=True)
class RentalScreenResult:
    locality: str
    postcodes: list[str]
    median_weekly_rent: float
    median_sale_price: float
    gross_yield_pct: float
    rental_count: int
    sales_count: int
    confidence: str
