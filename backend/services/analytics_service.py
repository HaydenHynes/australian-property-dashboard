# ruff: noqa: E501
"""Investment-focused analytics over NSW property sales."""

from backend.database.connection import Database
from backend.models.analytics import (
    MarketTrendPoint,
    PropertyTypeSales,
    SalesByLocality,
    SuburbProfile,
    TopSale,
)

# Conservative analytics rule. Raw rows remain untouched. The dashboard includes only
# full-interest, uncoded transactions with enough information for market analysis.
MARKET_SALE_FILTER_SQL = """
purchase_price BETWEEN 50000 AND 20000000
AND contract_date IS NOT NULL
AND contract_date >= DATE '2001-01-01'
AND contract_date <= CURRENT_DATE
AND property_locality IS NOT NULL
AND COALESCE(TRIM(sale_code), '') = ''
AND COALESCE(NULLIF(TRIM(percent_interest_of_sale), ''), '0') IN ('0', '100')
"""

FILTERS_SQL = f"""
{MARKET_SALE_FILTER_SQL}
AND property_locality ILIKE %(search_pattern)s
AND nature_of_property LIKE %(property_type_filter)s
AND (
    CAST(%(contract_year)s AS integer) IS NULL
    OR contract_date >= MAKE_DATE(CAST(%(contract_year)s AS integer), 1, 1)
       AND contract_date < MAKE_DATE(CAST(%(contract_year)s AS integer) + 1, 1, 1)
)
"""

GET_SUMMARY_SQL = f"""
WITH filtered AS (
    SELECT purchase_price, contract_date, property_locality
    FROM property_sales
    WHERE {FILTERS_SQL}
), latest AS (
    SELECT MAX(contract_date) AS as_of_date FROM filtered
)
SELECT
    COUNT(*),
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY purchase_price),
    COUNT(DISTINCT property_locality),
    MAX(contract_date),
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY purchase_price)
        FILTER (
            WHERE contract_date > (SELECT as_of_date FROM latest) - INTERVAL '12 months'
        ),
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY purchase_price)
        FILTER (
            WHERE contract_date > (SELECT as_of_date FROM latest) - INTERVAL '24 months'
              AND contract_date <= (SELECT as_of_date FROM latest) - INTERVAL '12 months'
        )
FROM filtered;
"""

GET_RAW_MATCHING_COUNT_SQL = """
SELECT COUNT(*)
FROM property_sales
WHERE property_locality ILIKE %(search_pattern)s
  AND nature_of_property LIKE %(property_type_filter)s
  AND (
      CAST(%(contract_year)s AS integer) IS NULL
      OR contract_date >= MAKE_DATE(CAST(%(contract_year)s AS integer), 1, 1)
         AND contract_date < MAKE_DATE(CAST(%(contract_year)s AS integer) + 1, 1, 1)
  );
"""

GET_RECENT_SALES_SQL = f"""
SELECT DISTINCT
    property_locality,
    property_street_name,
    property_house_number,
    purchase_price,
    contract_date
FROM property_sales
WHERE {FILTERS_SQL}
ORDER BY contract_date DESC, purchase_price DESC
LIMIT %(limit)s;
"""

GET_SALES_BY_LOCALITY_SQL = f"""
SELECT property_locality, COUNT(*) AS sales_count
FROM property_sales
WHERE {FILTERS_SQL}
GROUP BY property_locality
ORDER BY sales_count DESC
LIMIT %(limit)s;
"""

GET_SALES_BY_PROPERTY_TYPE_SQL = f"""
SELECT nature_of_property, COUNT(*) AS sales_count
FROM property_sales
WHERE {FILTERS_SQL}
GROUP BY nature_of_property
ORDER BY sales_count DESC;
"""

GET_MARKET_TREND_SQL = f"""
SELECT
    DATE_TRUNC('quarter', contract_date)::date AS period,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY purchase_price),
    COUNT(*)
FROM property_sales
WHERE {FILTERS_SQL}
GROUP BY DATE_TRUNC('quarter', contract_date)
HAVING COUNT(*) >= 5
ORDER BY period;
"""

GET_SUBURB_PROFILE_SQL = f"""
WITH market AS (
    SELECT purchase_price, contract_date
    FROM property_sales
    WHERE {MARKET_SALE_FILTER_SQL}
      AND property_locality ILIKE %(exact_locality)s
      AND nature_of_property LIKE %(property_type_filter)s
), latest AS (
    SELECT MAX(contract_date) AS as_of_date FROM market
), medians AS (
    SELECT
        COUNT(*) FILTER (
            WHERE contract_date > (SELECT as_of_date FROM latest) - INTERVAL '12 months'
        ) AS sales_count,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY purchase_price)
            FILTER (
                WHERE contract_date > (SELECT as_of_date FROM latest) - INTERVAL '12 months'
            ) AS current_median,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY purchase_price)
            FILTER (
                WHERE contract_date > (SELECT as_of_date FROM latest) - INTERVAL '24 months'
                  AND contract_date <= (SELECT as_of_date FROM latest) - INTERVAL '12 months'
            ) AS median_1y,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY purchase_price)
            FILTER (
                WHERE contract_date > (SELECT as_of_date FROM latest) - INTERVAL '48 months'
                  AND contract_date <= (SELECT as_of_date FROM latest) - INTERVAL '36 months'
            ) AS median_3y,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY purchase_price)
            FILTER (
                WHERE contract_date > (SELECT as_of_date FROM latest) - INTERVAL '72 months'
                  AND contract_date <= (SELECT as_of_date FROM latest) - INTERVAL '60 months'
            ) AS median_5y
    FROM market
)
SELECT
    sales_count,
    current_median,
    (SELECT as_of_date FROM latest),
    CASE WHEN median_1y > 0
         THEN (current_median / median_1y - 1) * 100 END,
    CASE WHEN median_3y > 0
         THEN (POWER(current_median / median_3y, 1.0 / 3) - 1) * 100 END,
    CASE WHEN median_5y > 0
         THEN (POWER(current_median / median_5y, 1.0 / 5) - 1) * 100 END
FROM medians;
"""

GET_AVAILABLE_YEARS_SQL = f"""
SELECT DISTINCT EXTRACT(YEAR FROM contract_date)::int AS year
FROM property_sales
WHERE {MARKET_SALE_FILTER_SQL}
ORDER BY year DESC;
"""


class AnalyticsService:
    """Provides reusable, quality-filtered property market analytics."""

    def __init__(self, db: Database) -> None:
        self._db = db

    def get_summary_metrics(
        self,
        search: str | None = None,
        property_type: str | None = None,
        contract_year: int | None = None,
    ) -> dict:
        """Return headline metrics and transparent exclusion counts."""
        params = self._build_params(search, property_type, contract_year)
        with self._db.connection() as conn:
            row = conn.execute(GET_SUMMARY_SQL, params).fetchone()
            raw_count = conn.execute(GET_RAW_MATCHING_COUNT_SQL, params).fetchone()[0]

        median = self._as_float(row[1])
        current_median = self._as_float(row[4])
        previous_median = self._as_float(row[5])
        growth = self._growth(current_median, previous_median)
        return {
            "total_sales": row[0],
            "median_sale_price": median,
            "locality_count": row[2],
            "data_as_of": row[3],
            "annual_growth_pct": growth,
            "excluded_sales": max(raw_count - row[0], 0),
        }

    def get_total_sales(self, **filters) -> int:
        return self.get_summary_metrics(**filters)["total_sales"]

    def get_median_sale_price(self, **filters) -> float | None:
        return self.get_summary_metrics(**filters)["median_sale_price"]

    def get_locality_count(self, **filters) -> int:
        return self.get_summary_metrics(**filters)["locality_count"]

    def get_recent_sales(
        self,
        limit: int = 20,
        search: str | None = None,
        property_type: str | None = None,
        contract_year: int | None = None,
    ) -> list[TopSale]:
        """Return the latest comparable market sales."""
        params = self._build_params(search, property_type, contract_year)
        params["limit"] = limit
        with self._db.connection() as conn:
            rows = conn.execute(GET_RECENT_SALES_SQL, params).fetchall()
        return [TopSale(*row) for row in rows]

    # Kept for compatibility with the existing endpoint and frontend name.
    get_top_sales = get_recent_sales

    def get_sales_by_locality(
        self,
        limit: int = 20,
        search: str | None = None,
        property_type: str | None = None,
        contract_year: int | None = None,
    ) -> list[SalesByLocality]:
        params = self._build_params(search, property_type, contract_year)
        params["limit"] = limit
        with self._db.connection() as conn:
            rows = conn.execute(GET_SALES_BY_LOCALITY_SQL, params).fetchall()
        return [SalesByLocality(*row) for row in rows]

    def get_sales_by_property_type(
        self,
        search: str | None = None,
        property_type: str | None = None,
        contract_year: int | None = None,
    ) -> list[PropertyTypeSales]:
        params = self._build_params(search, property_type, contract_year)
        with self._db.connection() as conn:
            rows = conn.execute(GET_SALES_BY_PROPERTY_TYPE_SQL, params).fetchall()
        return [PropertyTypeSales(*row) for row in rows]

    def get_market_trend(
        self,
        search: str | None = None,
        property_type: str | None = None,
        contract_year: int | None = None,
    ) -> list[MarketTrendPoint]:
        params = self._build_params(search, property_type, contract_year)
        with self._db.connection() as conn:
            rows = conn.execute(GET_MARKET_TREND_SQL, params).fetchall()
        return [MarketTrendPoint(row[0], self._as_float(row[1]), row[2]) for row in rows]

    def get_suburb_profile(
        self,
        locality: str,
        property_type: str | None = "R",
    ) -> SuburbProfile:
        """Return trailing-period growth and liquidity metrics for one locality."""
        params = {
            "exact_locality": locality.strip(),
            "property_type_filter": self._build_property_type_filter(property_type),
        }
        with self._db.connection() as conn:
            row = conn.execute(GET_SUBURB_PROFILE_SQL, params).fetchone()
        return SuburbProfile(
            locality=locality.strip().upper(),
            median_sale_price=self._as_float(row[1]),
            sales_count_12m=row[0],
            data_as_of=row[2],
            growth_1y_pct=self._as_float(row[3]),
            growth_3y_annualised_pct=self._as_float(row[4]),
            growth_5y_annualised_pct=self._as_float(row[5]),
        )

    def get_available_years(self) -> list[int]:
        with self._db.connection() as conn:
            rows = conn.execute(GET_AVAILABLE_YEARS_SQL).fetchall()
        return [row[0] for row in rows]

    def _build_params(
        self,
        search: str | None,
        property_type: str | None,
        contract_year: int | None,
    ) -> dict:
        return {
            "search_pattern": f"%{search.strip()}%" if search else "%",
            "property_type_filter": self._build_property_type_filter(property_type),
            "contract_year": contract_year,
        }

    @staticmethod
    def _build_property_type_filter(property_type: str | None) -> str:
        return property_type if property_type else "%"

    @staticmethod
    def _as_float(value) -> float | None:
        return float(value) if value is not None else None

    @staticmethod
    def _growth(current: float | None, previous: float | None) -> float | None:
        if current is None or previous in (None, 0):
            return None
        return (current / previous - 1) * 100
