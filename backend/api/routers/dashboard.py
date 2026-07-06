"""
Dashboard API routes.
"""

from fastapi import APIRouter, Depends

from backend.api.dependencies import get_analytics_service
from backend.models.dashboard import DashboardSummary
from backend.services.analytics_service import AnalyticsService
from backend.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get(
    "/summary",
    response_model=DashboardSummary,
)
def dashboard_summary(
    search: str | None = None,
    property_type: str | None = None,
    analytics: AnalyticsService = Depends(get_analytics_service),
) -> DashboardSummary:
    """Return dashboard summary metrics."""
    dashboard = DashboardService(analytics)
    return dashboard.get_summary(
        search=search,
        property_type=property_type,
    )