from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class DashboardSummary:
    """High-level dashboard summary metrics."""

    total_sales: int
    median_sale_price: float | None
    annual_growth_pct: float | None
    locality_count: int
    excluded_sales: int
    data_as_of: date | None
