"""Rental investment analysis API routes."""

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query

from backend.api.dependencies import get_rental_service
from backend.api.schemas import (
    RentalProfileResponse,
    RentalScreenResultResponse,
    RentalTrendPointResponse,
)
from backend.services.rental_service import RentalService

router = APIRouter(prefix="/rental", tags=["rental"])
DwellingType = Literal["F", "H", "T"] | None
Bedrooms = Annotated[int | None, Query(ge=0, le=10)]


@router.get("/profile", response_model=RentalProfileResponse)
def rental_profile(
    locality: Annotated[str, Query(min_length=2, max_length=100)],
    dwelling_type: DwellingType = None,
    bedrooms: Bedrooms = None,
    rental: RentalService = Depends(get_rental_service),
):
    return rental.get_profile(locality, dwelling_type, bedrooms)


@router.get("/trend", response_model=list[RentalTrendPointResponse])
def rental_trend(
    locality: Annotated[str, Query(min_length=2, max_length=100)],
    dwelling_type: DwellingType = None,
    bedrooms: Bedrooms = None,
    rental: RentalService = Depends(get_rental_service),
):
    return rental.get_trend(locality, dwelling_type, bedrooms)


@router.get("/compare", response_model=list[RentalProfileResponse])
def rental_compare(
    localities: Annotated[list[str], Query(min_length=2, max_length=4)],
    dwelling_type: DwellingType = None,
    bedrooms: Bedrooms = None,
    rental: RentalService = Depends(get_rental_service),
):
    return rental.compare(localities, dwelling_type, bedrooms)


@router.get("/screen", response_model=list[RentalScreenResultResponse])
def rental_screen(
    max_price: Annotated[int, Query(ge=100_000, le=20_000_000)] = 1_500_000,
    min_yield: Annotated[float, Query(ge=0, le=20)] = 3.0,
    min_rental_count: Annotated[int, Query(ge=5, le=500)] = 30,
    min_sales_count: Annotated[int, Query(ge=5, le=500)] = 20,
    dwelling_type: DwellingType = None,
    bedrooms: Bedrooms = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 25,
    rental: RentalService = Depends(get_rental_service),
):
    return rental.screen(
        max_price,
        min_yield,
        min_rental_count,
        min_sales_count,
        dwelling_type,
        bedrooms,
        limit,
    )
