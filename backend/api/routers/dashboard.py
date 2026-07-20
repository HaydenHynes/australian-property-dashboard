"""Dashboard API routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from backend.api.dependencies import get_analytics_service
from backend.models.dashboard import DashboardSummary
from backend.services.analytics_service import AnalyticsService
from backend.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def dashboard_summary(
    search: Annotated[str | None, Query(max_length=100)] = None,
    property_type: Annotated[str | None, Query(pattern=r"^(R|V|3)?$")] = None,
    contract_year: Annotated[int | None, Query(ge=2001, le=2100)] = None,
    analytics: AnalyticsService = Depends(get_analytics_service),
) -> DashboardSummary:
    return DashboardService(analytics).get_summary(
        search=search,
        property_type=property_type,
        contract_year=contract_year,
    )
