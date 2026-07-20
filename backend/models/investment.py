"""Demographic and explainable investment-ranking models."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class DemographicProfile:
    locality: str
    postcodes: list[str]
    population_2016: int
    population_2021: int
    population_growth_5y_pct: float
    population_growth_annualised_pct: float
    median_household_income_2016: float
    median_household_income_2021: float
    income_growth_5y_pct: float
    income_growth_annualised_pct: float
    latitude: float
    longitude: float
    data_as_of: int = 2021
    geography_level: str = "ABS Postal Area"


@dataclass(frozen=True)
class ScoreComponent:
    key: str
    label: str
    raw_value: float
    percentile_score: float
    weight_pct: float
    contribution: float
    explanation: str


@dataclass(frozen=True)
class InvestmentScore:
    locality: str
    postcodes: list[str]
    latitude: float
    longitude: float
    median_weekly_rent: float
    rent_growth_1y_pct: float
    rental_count: int
    median_sale_price: float
    price_growth_5y_annualised_pct: float
    sales_count: int
    gross_yield_pct: float
    population_2021: int
    population_growth_5y_pct: float
    median_household_income_weekly: float
    income_growth_5y_pct: float
    investment_score: float
    confidence: str
    rental_data_as_of: date
    sales_data_as_of: date
    demographic_data_as_of: int
    components: list[ScoreComponent]
