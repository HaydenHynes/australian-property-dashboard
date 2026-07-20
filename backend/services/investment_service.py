# ruff: noqa: E501
"""ABS demographics and explainable investment rankings."""

from backend.database.connection import Database
from backend.database.demographic_loader import SCORE_WEIGHTS
from backend.models.investment import (
    DemographicProfile,
    InvestmentScore,
    ScoreComponent,
)

DEMOGRAPHICS_SQL = """
WITH postcode_values AS (
    SELECT
        mapping.locality,
        mapping.postcode,
        mapping.supporting_sales,
        MAX(demographics.population) FILTER (
            WHERE demographics.census_year = 2016
        ) AS population_2016,
        MAX(demographics.population) FILTER (
            WHERE demographics.census_year = 2021
        ) AS population_2021,
        MAX(demographics.median_household_income_weekly) FILTER (
            WHERE demographics.census_year = 2016
        ) AS income_2016,
        MAX(demographics.median_household_income_weekly) FILTER (
            WHERE demographics.census_year = 2021
        ) AS income_2021,
        geography.latitude,
        geography.longitude
    FROM suburb_postcodes mapping
    JOIN postcode_demographics demographics
        ON demographics.postcode = mapping.postcode
    JOIN postcode_geography geography ON geography.postcode = mapping.postcode
    WHERE mapping.locality = UPPER(TRIM(%(locality)s))
    GROUP BY
        mapping.locality,
        mapping.postcode,
        mapping.supporting_sales,
        geography.latitude,
        geography.longitude
), aggregate_values AS (
    SELECT
        locality,
        ARRAY_AGG(postcode ORDER BY postcode) AS postcodes,
        SUM(population_2016)::int AS population_2016,
        SUM(population_2021)::int AS population_2021,
        SUM(income_2016 * population_2016)
            / NULLIF(SUM(population_2016), 0) AS income_2016,
        SUM(income_2021 * population_2021)
            / NULLIF(SUM(population_2021), 0) AS income_2021,
        SUM(latitude * supporting_sales)
            / NULLIF(SUM(supporting_sales), 0) AS latitude,
        SUM(longitude * supporting_sales)
            / NULLIF(SUM(supporting_sales), 0) AS longitude
    FROM postcode_values
    WHERE population_2016 > 0
      AND population_2021 > 0
      AND income_2016 > 0
      AND income_2021 > 0
    GROUP BY locality
)
SELECT
    locality,
    postcodes,
    population_2016,
    population_2021,
    (population_2021::double precision / population_2016 - 1) * 100,
    (POWER(population_2021::double precision / population_2016, 1.0 / 5) - 1) * 100,
    income_2016,
    income_2021,
    (income_2021::double precision / income_2016 - 1) * 100,
    (POWER(income_2021::double precision / income_2016, 1.0 / 5) - 1) * 100,
    latitude,
    longitude
FROM aggregate_values;
"""

SCORE_COLUMNS = """
locality,
postcodes,
latitude,
longitude,
median_weekly_rent,
rent_growth_1y_pct,
rental_count,
median_sale_price,
price_growth_5y_annualised_pct,
sales_count,
gross_yield_pct,
population_2021,
population_growth_5y_pct,
median_household_income_weekly,
income_growth_5y_pct,
yield_score,
price_growth_score,
rent_growth_score,
population_growth_score,
income_growth_score,
evidence_score,
investment_score,
confidence,
rental_data_as_of,
sales_data_as_of,
demographic_data_as_of
"""

RANKING_SORTS = {
    "score": "investment_score DESC, rental_count DESC",
    "yield": "gross_yield_pct DESC, investment_score DESC",
    "price_growth": "price_growth_5y_annualised_pct DESC, investment_score DESC",
    "rent_growth": "rent_growth_1y_pct DESC, investment_score DESC",
    "population_growth": "population_growth_5y_pct DESC, investment_score DESC",
    "income_growth": "income_growth_5y_pct DESC, investment_score DESC",
}


class InvestmentService:
    def __init__(self, db: Database) -> None:
        self._db = db

    def get_demographics(self, locality: str) -> DemographicProfile | None:
        with self._db.connection() as conn:
            row = conn.execute(DEMOGRAPHICS_SQL, {"locality": locality}).fetchone()
        if not row:
            return None
        return DemographicProfile(
            locality=row[0],
            postcodes=list(row[1]),
            population_2016=row[2],
            population_2021=row[3],
            population_growth_5y_pct=float(row[4]),
            population_growth_annualised_pct=float(row[5]),
            median_household_income_2016=float(row[6]),
            median_household_income_2021=float(row[7]),
            income_growth_5y_pct=float(row[8]),
            income_growth_annualised_pct=float(row[9]),
            latitude=float(row[10]),
            longitude=float(row[11]),
        )

    def get_rankings(
        self,
        max_price: int = 1_500_000,
        min_yield: float = 0,
        min_score: float = 0,
        search: str | None = None,
        sort: str = "score",
        limit: int = 100,
    ) -> list[InvestmentScore]:
        order_by = RANKING_SORTS.get(sort, RANKING_SORTS["score"])
        query = f"""
            SELECT {SCORE_COLUMNS}
            FROM investment_scores
            WHERE median_sale_price <= %(max_price)s
              AND gross_yield_pct >= %(min_yield)s
              AND investment_score >= %(min_score)s
              AND locality ILIKE %(search)s
            ORDER BY {order_by}
            LIMIT %(limit)s
        """
        with self._db.connection() as conn:
            rows = conn.execute(
                query,
                {
                    "max_price": max_price,
                    "min_yield": min_yield,
                    "min_score": min_score,
                    "search": f"%{search.strip()}%" if search else "%",
                    "limit": limit,
                },
            ).fetchall()
        return [self._score_from_row(row) for row in rows]

    def get_profile(self, locality: str) -> InvestmentScore | None:
        with self._db.connection() as conn:
            row = conn.execute(
                f"""
                SELECT {SCORE_COLUMNS}
                FROM investment_scores
                WHERE locality = UPPER(TRIM(%s))
                """,
                (locality,),
            ).fetchone()
        return self._score_from_row(row) if row else None

    def compare(self, localities: list[str]) -> list[InvestmentScore]:
        normalised = [locality.strip().upper() for locality in localities]
        with self._db.connection() as conn:
            rows = conn.execute(
                f"""
                SELECT {SCORE_COLUMNS}
                FROM investment_scores
                WHERE locality = ANY(%s)
                """,
                (normalised,),
            ).fetchall()
        by_locality = {row[0]: self._score_from_row(row) for row in rows}
        return [by_locality[item] for item in normalised if item in by_locality]

    @staticmethod
    def _component(
        key: str,
        label: str,
        raw_value: float,
        score: float,
        explanation: str,
    ) -> ScoreComponent:
        weight = SCORE_WEIGHTS[key]
        return ScoreComponent(
            key=key,
            label=label,
            raw_value=raw_value,
            percentile_score=score,
            weight_pct=weight * 100,
            contribution=score * weight,
            explanation=explanation,
        )

    @classmethod
    def _score_from_row(cls, row) -> InvestmentScore:
        components = [
            cls._component(
                "yield",
                "Gross rental yield",
                float(row[10]),
                float(row[15]),
                "Relative gross yield percentile across eligible NSW localities.",
            ),
            cls._component(
                "price_growth",
                "Price growth",
                float(row[8]),
                float(row[16]),
                "Relative five-year annualised residential price-growth percentile.",
            ),
            cls._component(
                "rent_growth",
                "Rent growth",
                float(row[5]),
                float(row[17]),
                "Relative one-year median-rent growth percentile.",
            ),
            cls._component(
                "population_growth",
                "Population growth",
                float(row[12]),
                float(row[18]),
                "Relative 2016 to 2021 ABS Census population-growth percentile.",
            ),
            cls._component(
                "income_growth",
                "Household income growth",
                float(row[14]),
                float(row[19]),
                "Relative nominal weekly household-income growth percentile.",
            ),
            cls._component(
                "evidence",
                "Evidence strength",
                float(row[20]),
                float(row[20]),
                "Rental and sales observations, with full credit at 100 of each.",
            ),
        ]
        return InvestmentScore(
            locality=row[0],
            postcodes=list(row[1]),
            latitude=float(row[2]),
            longitude=float(row[3]),
            median_weekly_rent=float(row[4]),
            rent_growth_1y_pct=float(row[5]),
            rental_count=row[6],
            median_sale_price=float(row[7]),
            price_growth_5y_annualised_pct=float(row[8]),
            sales_count=row[9],
            gross_yield_pct=float(row[10]),
            population_2021=row[11],
            population_growth_5y_pct=float(row[12]),
            median_household_income_weekly=float(row[13]),
            income_growth_5y_pct=float(row[14]),
            investment_score=float(row[21]),
            confidence=row[22],
            rental_data_as_of=row[23],
            sales_data_as_of=row[24],
            demographic_data_as_of=row[25],
            components=components,
        )
