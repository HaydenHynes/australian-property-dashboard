"""Demographic demand and explainable investment-ranking routes."""

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Query

from backend.api.dependencies import get_investment_service
from backend.api.schemas import (
    DemographicProfileResponse,
    InvestmentScoreResponse,
)
from backend.services.investment_service import InvestmentService

router = APIRouter(prefix="/investment", tags=["investment"])
RankingSort = Literal[
    "score",
    "yield",
    "price_growth",
    "rent_growth",
    "population_growth",
    "income_growth",
]


@router.get("/demographics", response_model=DemographicProfileResponse)
def demographic_profile(
    locality: Annotated[str, Query(min_length=2, max_length=100)],
    investment: InvestmentService = Depends(get_investment_service),
):
    result = investment.get_demographics(locality)
    if result is None:
        raise HTTPException(status_code=404, detail="No mapped ABS data found")
    return result


@router.get("/profile", response_model=InvestmentScoreResponse)
def investment_profile(
    locality: Annotated[str, Query(min_length=2, max_length=100)],
    investment: InvestmentService = Depends(get_investment_service),
):
    result = investment.get_profile(locality)
    if result is None:
        raise HTTPException(status_code=404, detail="No eligible score found")
    return result


@router.get("/rankings", response_model=list[InvestmentScoreResponse])
def investment_rankings(
    max_price: Annotated[int, Query(ge=100_000, le=20_000_000)] = 1_500_000,
    min_yield: Annotated[float, Query(ge=0, le=20)] = 0,
    min_score: Annotated[float, Query(ge=0, le=100)] = 0,
    search: Annotated[str | None, Query(max_length=100)] = None,
    sort: RankingSort = "score",
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
    investment: InvestmentService = Depends(get_investment_service),
):
    return investment.get_rankings(
        max_price=max_price,
        min_yield=min_yield,
        min_score=min_score,
        search=search,
        sort=sort,
        limit=limit,
    )


@router.get("/compare", response_model=list[InvestmentScoreResponse])
def compare_investments(
    localities: Annotated[list[str], Query(min_length=1, max_length=20)],
    investment: InvestmentService = Depends(get_investment_service),
):
    return investment.compare(localities)
