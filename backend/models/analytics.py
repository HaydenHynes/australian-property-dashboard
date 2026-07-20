"""
Analytics response models.
"""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class TopSale:
    """Represents a high-value property sale."""

    locality: str | None
    street_name: str | None
    house_number: str | None
    purchase_price: int | None
    contract_date: date | None


@dataclass(frozen=True)
class SalesByLocality:
    """Represents sales volume for a locality."""

    locality: str | None
    sales_count: int


@dataclass(frozen=True)
class AveragePriceByLocality:
    """Represents average purchase price for a locality."""

    locality: str | None
    average_purchase_price: Decimal | None


@dataclass(frozen=True)
class PropertyTypeSales:
    """Represents sales volume by property type."""

    property_type: str | None
    sales_count: int


@dataclass(frozen=True)
class MarketTrendPoint:
    """Quarterly median price and market liquidity."""

    period: date
    median_sale_price: float | None
    sales_count: int


@dataclass(frozen=True)
class SuburbProfile:
    """Investor-oriented metrics for a single locality."""

    locality: str
    median_sale_price: float | None
    sales_count_12m: int
    data_as_of: date | None
    growth_1y_pct: float | None
    growth_3y_annualised_pct: float | None
    growth_5y_annualised_pct: float | None
