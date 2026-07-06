from dataclasses import dataclass


@dataclass(frozen=True)
class DashboardSummary:
    """High-level dashboard summary metrics."""

    total_sales: int
    highest_sale_price: int | None
    average_sale_price: int | None
    locality_count: int