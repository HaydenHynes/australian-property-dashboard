"""
Dashboard service.

Composes analytics into dashboard-ready responses.
"""

from backend.models.dashboard import DashboardSummary
from backend.services.analytics_service import AnalyticsService


class DashboardService:
    """Provides dashboard-focused summary data."""

    def __init__(self, analytics: AnalyticsService) -> None:
        """Initialize the dashboard service."""
        self._analytics = analytics

    def get_summary(self) -> DashboardSummary:
      """Return high-level dashboard summary metrics."""
      return DashboardSummary(
          total_sales=self._analytics.get_total_sales(),
          highest_sale_price=self._analytics.get_highest_sale_price(),
          locality_count=self._analytics.get_locality_count(),
      )