"""Quality-filtered property analytics API routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from backend.api.dependencies import get_analytics_service
from backend.api.schemas import (
    AvailableYearsResponse,
    MarketTrendPointResponse,
    PropertyTypeSalesResponse,
    SalesByLocalityResponse,
    SuburbProfileResponse,
    TopSaleResponse,
    TotalSalesResponse,
)
from backend.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"])

Search = Annotated[str | None, Query(max_length=100)]
PropertyType = Annotated[str | None, Query(pattern=r"^(R|V|3)?$")]
ContractYear = Annotated[int | None, Query(ge=2001, le=2100)]
Limit = Annotated[int, Query(ge=1, le=100)]


@router.get("/total-sales", response_model=TotalSalesResponse)
def total_sales(
    search: Search = None,
    property_type: PropertyType = None,
    contract_year: ContractYear = None,
    analytics: AnalyticsService = Depends(get_analytics_service),
) -> dict[str, int]:
    return {
        "total_sales": analytics.get_total_sales(
            search=search,
            property_type=property_type,
            contract_year=contract_year,
        )
    }


@router.get("/top-sales", response_model=list[TopSaleResponse])
def recent_sales(
    limit: Limit = 20,
    search: Search = None,
    property_type: PropertyType = None,
    contract_year: ContractYear = None,
    analytics: AnalyticsService = Depends(get_analytics_service),
):
    """Return latest comparable sales (legacy URL retained)."""
    return analytics.get_recent_sales(limit, search, property_type, contract_year)


@router.get("/sales-by-locality", response_model=list[SalesByLocalityResponse])
def sales_by_locality(
    limit: Limit = 20,
    search: Search = None,
    property_type: PropertyType = None,
    contract_year: ContractYear = None,
    analytics: AnalyticsService = Depends(get_analytics_service),
):
    return analytics.get_sales_by_locality(limit, search, property_type, contract_year)


@router.get(
    "/sales-by-property-type",
    response_model=list[PropertyTypeSalesResponse],
)
def sales_by_property_type(
    search: Search = None,
    property_type: PropertyType = None,
    contract_year: ContractYear = None,
    analytics: AnalyticsService = Depends(get_analytics_service),
):
    return analytics.get_sales_by_property_type(search, property_type, contract_year)


@router.get("/market-trend", response_model=list[MarketTrendPointResponse])
def market_trend(
    search: Search = None,
    property_type: PropertyType = None,
    contract_year: ContractYear = None,
    analytics: AnalyticsService = Depends(get_analytics_service),
):
    return analytics.get_market_trend(search, property_type, contract_year)


@router.get("/suburb-profile", response_model=SuburbProfileResponse)
def suburb_profile(
    locality: Annotated[str, Query(min_length=2, max_length=100)],
    property_type: PropertyType = "R",
    analytics: AnalyticsService = Depends(get_analytics_service),
):
    return analytics.get_suburb_profile(locality, property_type)


@router.get("/available-years", response_model=AvailableYearsResponse)
def available_years(
    analytics: AnalyticsService = Depends(get_analytics_service),
) -> dict[str, list[int]]:
    return {"years": analytics.get_available_years()}
