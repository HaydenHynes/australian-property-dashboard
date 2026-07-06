"""
Analytics API routes.
"""

from fastapi import APIRouter, Depends

from backend.api.dependencies import get_analytics_service
from backend.api.schemas import (
    AveragePriceByLocalityResponse,
    PropertyTypeSalesResponse,
    SalesByLocalityResponse,
    TopSaleResponse,
    TotalSalesResponse,
)
from backend.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get(
    "/total-sales",
    response_model=TotalSalesResponse,
)
def total_sales(
    analytics: AnalyticsService = Depends(get_analytics_service),
) -> dict[str, int]:
    """Return the total number of property sales."""
    return {"total_sales": analytics.get_total_sales()}

@router.get(
    "/top-sales",
    response_model=list[TopSaleResponse],
)
def top_sales(
    limit: int = 20,
    search: str | None = None,
    analytics: AnalyticsService = Depends(get_analytics_service),
):
    """Return top property sales."""
    return analytics.get_top_sales(limit=limit, search=search)


@router.get(
    "/sales-by-locality",
    response_model=list[SalesByLocalityResponse],
)
def sales_by_locality(
    limit: int = 20,
    search: str | None = None,
    analytics: AnalyticsService = Depends(get_analytics_service),
):
    """Return sales counts by locality."""
    return analytics.get_sales_by_locality(limit=limit, search=search)


@router.get(
    "/average-price-by-locality",
    response_model=list[AveragePriceByLocalityResponse],
)
def average_price_by_locality(
    limit: int = 20,
    analytics: AnalyticsService = Depends(get_analytics_service),
):
    """Return average purchase price by locality."""
    return analytics.get_average_price_by_locality(limit=limit)


@router.get(
    "/sales-by-property-type",
    response_model=list[PropertyTypeSalesResponse],
)
def sales_by_property_type(
    search: str | None = None,
    analytics: AnalyticsService = Depends(get_analytics_service),
):
    """Return sales counts by property type."""
    return analytics.get_sales_by_property_type(search=search)