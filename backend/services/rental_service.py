# ruff: noqa: E501
"""Postcode-aware rental investment analytics."""

from backend.database.connection import Database
from backend.models.rental import (
    RentalProfile,
    RentalScreenResult,
    RentalTrendPoint,
)
from backend.services.analytics_service import (
    MARKET_SALE_FILTER_SQL,
    AnalyticsService,
)

PROFILE_SQL = """
WITH mapped AS (
    SELECT postcode
    FROM suburb_postcodes
    WHERE locality = UPPER(TRIM(%(locality)s))
), scoped AS (
    SELECT lodgement_date, weekly_rent
    FROM rental_bond_lodgements
    WHERE postcode IN (SELECT postcode FROM mapped)
      AND weekly_rent BETWEEN 50 AND 5000
      AND dwelling_type IN ('F', 'H', 'T')
      AND (
          CAST(%(dwelling_type)s AS text) IS NULL
          OR dwelling_type = CAST(%(dwelling_type)s AS text)
      )
      AND (
          CAST(%(bedrooms)s AS integer) IS NULL
          OR bedrooms = CAST(%(bedrooms)s AS integer)
      )
), latest AS (
    SELECT MAX(lodgement_date) AS as_of_date FROM scoped
)
SELECT
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY weekly_rent)
        FILTER (WHERE lodgement_date > (SELECT as_of_date FROM latest) - INTERVAL '3 months'),
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY weekly_rent)
        FILTER (WHERE lodgement_date > (SELECT as_of_date FROM latest) - INTERVAL '3 months'),
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY weekly_rent)
        FILTER (WHERE lodgement_date > (SELECT as_of_date FROM latest) - INTERVAL '3 months'),
    COUNT(*) FILTER (
        WHERE lodgement_date > (SELECT as_of_date FROM latest) - INTERVAL '3 months'
    ),
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY weekly_rent)
        FILTER (
            WHERE lodgement_date > (SELECT as_of_date FROM latest) - INTERVAL '15 months'
              AND lodgement_date <= (SELECT as_of_date FROM latest) - INTERVAL '12 months'
        ),
    (SELECT as_of_date FROM latest)
FROM scoped;
"""

POSTCODES_SQL = """
SELECT postcode
FROM suburb_postcodes
WHERE locality = UPPER(TRIM(%s))
ORDER BY supporting_sales DESC, postcode;
"""

TREND_SQL = """
WITH mapped AS (
    SELECT postcode FROM suburb_postcodes WHERE locality = UPPER(TRIM(%(locality)s))
), monthly AS (
    SELECT
        DATE_TRUNC('month', lodgement_date)::date AS month,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY weekly_rent) AS median_rent,
        COUNT(*) AS lodgement_count
    FROM rental_bond_lodgements
    WHERE postcode IN (SELECT postcode FROM mapped)
      AND weekly_rent BETWEEN 50 AND 5000
      AND dwelling_type IN ('F', 'H', 'T')
      AND (
          CAST(%(dwelling_type)s AS text) IS NULL
          OR dwelling_type = CAST(%(dwelling_type)s AS text)
      )
      AND (
          CAST(%(bedrooms)s AS integer) IS NULL
          OR bedrooms = CAST(%(bedrooms)s AS integer)
      )
    GROUP BY DATE_TRUNC('month', lodgement_date)
    HAVING COUNT(*) >= 5
)
SELECT month, median_rent, lodgement_count
FROM monthly
ORDER BY month DESC
LIMIT 36;
"""

SCREEN_SQL = f"""
WITH latest_rent AS (
    SELECT MAX(lodgement_date) AS max_date FROM rental_bond_lodgements
), postcode_rents AS (
    SELECT
        postcode,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY weekly_rent) AS median_rent,
        COUNT(*) AS rental_count
    FROM rental_bond_lodgements
    WHERE weekly_rent BETWEEN 50 AND 5000
      AND dwelling_type IN ('F', 'H', 'T')
      AND (
          CAST(%(dwelling_type)s AS text) IS NULL
          OR dwelling_type = CAST(%(dwelling_type)s AS text)
      )
      AND (
          CAST(%(bedrooms)s AS integer) IS NULL
          OR bedrooms = CAST(%(bedrooms)s AS integer)
      )
      AND lodgement_date > (SELECT max_date FROM latest_rent) - INTERVAL '3 months'
    GROUP BY postcode
    HAVING COUNT(*) >= %(min_rental_count)s
), suburb_rents AS (
    SELECT
        mapping.locality,
        ARRAY_AGG(DISTINCT mapping.postcode ORDER BY mapping.postcode) AS postcodes,
        SUM(rents.median_rent * rents.rental_count) / SUM(rents.rental_count) AS median_rent,
        SUM(rents.rental_count)::int AS rental_count
    FROM postcode_rents rents
    JOIN suburb_postcodes mapping ON mapping.postcode = rents.postcode
    GROUP BY mapping.locality
), latest_sale AS (
    SELECT MAX(contract_date) AS max_date FROM property_sales WHERE {MARKET_SALE_FILTER_SQL}
), suburb_sales AS (
    SELECT
        UPPER(TRIM(property_locality)) AS locality,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY purchase_price) AS median_price,
        COUNT(*)::int AS sales_count
    FROM property_sales
    WHERE {MARKET_SALE_FILTER_SQL}
      AND nature_of_property = 'R'
      AND contract_date > (SELECT max_date FROM latest_sale) - INTERVAL '12 months'
    GROUP BY UPPER(TRIM(property_locality))
    HAVING COUNT(*) >= %(min_sales_count)s
), results AS (
    SELECT
        sales.locality,
        rents.postcodes,
        rents.median_rent,
        sales.median_price,
        rents.median_rent * 52 / sales.median_price * 100 AS gross_yield,
        rents.rental_count,
        sales.sales_count
    FROM suburb_sales sales
    JOIN suburb_rents rents ON rents.locality = sales.locality
)
SELECT * FROM results
WHERE median_price <= %(max_price)s
  AND gross_yield >= %(min_yield)s
ORDER BY gross_yield DESC, rental_count DESC
LIMIT %(limit)s;
"""


class RentalService:
    def __init__(self, db: Database, analytics: AnalyticsService) -> None:
        self._db = db
        self._analytics = analytics

    def get_profile(
        self,
        locality: str,
        dwelling_type: str | None = None,
        bedrooms: int | None = None,
    ) -> RentalProfile:
        params = {
            "locality": locality,
            "dwelling_type": dwelling_type,
            "bedrooms": bedrooms,
        }
        with self._db.connection() as conn:
            row = conn.execute(PROFILE_SQL, params).fetchone()
            postcodes = [
                item[0]
                for item in conn.execute(POSTCODES_SQL, (locality,)).fetchall()
            ]
        median_rent = self._as_float(row[0])
        previous_rent = self._as_float(row[4])
        sale_profile = self._analytics.get_suburb_profile(locality, "R")
        gross_yield = None
        if median_rent is not None and sale_profile.median_sale_price:
            gross_yield = median_rent * 52 / sale_profile.median_sale_price * 100
        return RentalProfile(
            locality=locality.strip().upper(),
            postcodes=postcodes,
            dwelling_type=dwelling_type or "ALL",
            bedrooms=bedrooms,
            median_weekly_rent=median_rent,
            lower_quartile_rent=self._as_float(row[1]),
            upper_quartile_rent=self._as_float(row[2]),
            lodgement_count=row[3],
            confidence=self._confidence(row[3]),
            rent_growth_1y_pct=self._growth(median_rent, previous_rent),
            median_sale_price=sale_profile.median_sale_price,
            gross_yield_pct=gross_yield,
            data_as_of=row[5],
        )

    def get_trend(
        self,
        locality: str,
        dwelling_type: str | None = None,
        bedrooms: int | None = None,
    ) -> list[RentalTrendPoint]:
        with self._db.connection() as conn:
            rows = conn.execute(
                TREND_SQL,
                {
                    "locality": locality,
                    "dwelling_type": dwelling_type,
                    "bedrooms": bedrooms,
                },
            ).fetchall()
        return [
            RentalTrendPoint(
                month=row[0],
                median_weekly_rent=float(row[1]),
                lodgement_count=row[2],
                confidence=self._confidence(row[2]),
            )
            for row in reversed(rows)
        ]

    def compare(
        self,
        localities: list[str],
        dwelling_type: str | None = None,
        bedrooms: int | None = None,
    ) -> list[RentalProfile]:
        return [
            self.get_profile(locality, dwelling_type, bedrooms)
            for locality in localities
        ]

    def screen(
        self,
        max_price: int = 1_500_000,
        min_yield: float = 3.0,
        min_rental_count: int = 30,
        min_sales_count: int = 20,
        dwelling_type: str | None = None,
        bedrooms: int | None = None,
        limit: int = 25,
    ) -> list[RentalScreenResult]:
        with self._db.connection() as conn:
            rows = conn.execute(
                SCREEN_SQL,
                {
                    "max_price": max_price,
                    "min_yield": min_yield,
                    "min_rental_count": min_rental_count,
                    "min_sales_count": min_sales_count,
                    "dwelling_type": dwelling_type,
                    "bedrooms": bedrooms,
                    "limit": limit,
                },
            ).fetchall()
        return [
            RentalScreenResult(
                locality=row[0],
                postcodes=list(row[1]),
                median_weekly_rent=float(row[2]),
                median_sale_price=float(row[3]),
                gross_yield_pct=float(row[4]),
                rental_count=row[5],
                sales_count=row[6],
                confidence=self._confidence(row[5]),
            )
            for row in rows
        ]

    @staticmethod
    def _confidence(count: int) -> str:
        if count >= 30:
            return "high"
        if count >= 10:
            return "medium"
        return "low"

    @staticmethod
    def _growth(current: float | None, previous: float | None) -> float | None:
        if current is None or previous in (None, 0):
            return None
        return (current / previous - 1) * 100

    @staticmethod
    def _as_float(value) -> float | None:
        return float(value) if value is not None else None
