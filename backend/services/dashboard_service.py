from backend.models.dashboard import DashboardSummary


class DashboardService:
    """Provides aggregated dashboard data."""

    def __init__(self, analytics_service):
        self._analytics = analytics_service

    def get_summary(self, search: str | None = None) -> DashboardSummary:
        """Return high-level dashboard summary metrics."""
        return DashboardSummary(
            total_sales=self._analytics.get_total_sales(search=search),
            highest_sale_price=self._analytics.get_highest_sale_price(search=search),
            average_sale_price=self._analytics.get_average_sale_price(search=search),
            locality_count=self._analytics.get_locality_count(search=search),
        )