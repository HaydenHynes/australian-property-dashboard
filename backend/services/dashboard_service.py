from backend.models.dashboard import DashboardSummary
from backend.services.analytics_service import AnalyticsService


class DashboardService:
    """Provides aggregated, quality-filtered dashboard metrics."""

    def __init__(self, analytics_service: AnalyticsService):
        self._analytics = analytics_service

    def get_summary(
        self,
        search: str | None = None,
        property_type: str | None = None,
        contract_year: int | None = None,
    ) -> DashboardSummary:
        metrics = self._analytics.get_summary_metrics(
            search=search,
            property_type=property_type,
            contract_year=contract_year,
        )
        return DashboardSummary(**metrics)
