"""
Analytics service.

Provides reusable analytics queries for property sales data.
"""

from backend.database.connection import Database
from backend.models.analytics import (
    AveragePriceByLocality,
    PropertyTypeSales,
    SalesByLocality,
    TopSale,
)

GET_TOTAL_SALES_SQL = """
SELECT COUNT(*)
FROM property_sales
WHERE property_locality ILIKE %(search_pattern)s
  AND nature_of_property LIKE %(property_type_filter)s;
"""

GET_TOP_SALES_SQL = """
SELECT DISTINCT
    property_locality,
    property_street_name,
    property_house_number,
    purchase_price,
    contract_date
FROM property_sales
WHERE purchase_price IS NOT NULL
  AND property_locality ILIKE %(search_pattern)s
  AND nature_of_property LIKE %(property_type_filter)s
ORDER BY purchase_price DESC
LIMIT %(limit)s;
"""

GET_SALES_BY_LOCALITY_SQL = """
SELECT
    property_locality,
    COUNT(*) AS sales_count
FROM property_sales
WHERE property_locality ILIKE %(search_pattern)s
  AND nature_of_property LIKE %(property_type_filter)s
GROUP BY property_locality
ORDER BY sales_count DESC
LIMIT %(limit)s;
"""

GET_AVERAGE_PRICE_BY_LOCALITY_SQL = """
SELECT
    property_locality,
    ROUND(AVG(purchase_price), 2) AS average_purchase_price
FROM property_sales
WHERE purchase_price IS NOT NULL
GROUP BY property_locality
ORDER BY average_purchase_price DESC
LIMIT %(limit)s;
"""

GET_SALES_BY_PROPERTY_TYPE_SQL = """
SELECT
    nature_of_property,
    COUNT(*) AS sales_count
FROM property_sales
WHERE property_locality ILIKE %(search_pattern)s
  AND nature_of_property LIKE %(property_type_filter)s
GROUP BY nature_of_property
ORDER BY sales_count DESC;
"""

GET_HIGHEST_SALE_PRICE_SQL = """
SELECT MAX(purchase_price)
FROM property_sales
WHERE purchase_price IS NOT NULL
  AND property_locality ILIKE %(search_pattern)s
  AND nature_of_property LIKE %(property_type_filter)s;
"""

GET_LOCALITY_COUNT_SQL = """
SELECT COUNT(DISTINCT property_locality)
FROM property_sales
WHERE property_locality IS NOT NULL
  AND property_locality ILIKE %(search_pattern)s
  AND nature_of_property LIKE %(property_type_filter)s;
"""

GET_AVERAGE_SALE_PRICE_SQL = """
SELECT ROUND(AVG(purchase_price), 2)
FROM property_sales
WHERE purchase_price IS NOT NULL
  AND property_locality ILIKE %(search_pattern)s
  AND nature_of_property LIKE %(property_type_filter)s;
"""

class AnalyticsService:
    """Provides analytics queries over property sales."""

    def __init__(self, db: Database) -> None:
        """Initialize the analytics service."""
        self._db = db

    def get_total_sales(
        self,
        search: str | None = None,
        property_type: str | None = None,
    ) -> int:
        """Return the total number of property sales."""
        search_pattern = self._build_search_pattern(search)
        property_type_filter = self._build_property_type_filter(property_type)

        with self._db.connection() as conn:
            result = conn.execute(
                GET_TOTAL_SALES_SQL,
                {
                    "search_pattern": search_pattern,
                    "property_type_filter": property_type_filter,
                },
            ).fetchone()

        return result[0]

    def get_top_sales(
        self,
        limit: int = 20,
        search: str | None = None,
        property_type: str | None = None,
    ) -> list[TopSale]:
        """Return the highest property sales by purchase price."""
        search_pattern = self._build_search_pattern(search)
        property_type_filter = self._build_property_type_filter(property_type)

        with self._db.connection() as conn:
            rows = conn.execute(
                GET_TOP_SALES_SQL,
                {
                    "limit": limit,
                    "search_pattern": search_pattern,
                    "property_type_filter": property_type_filter,
                },
            ).fetchall()

        return [
            TopSale(
                locality=row[0],
                street_name=row[1],
                house_number=row[2],
                purchase_price=row[3],
                contract_date=row[4],
            )
            for row in rows
        ]

    def get_sales_by_locality(
        self,
        limit: int = 20,
        search: str | None = None,
        property_type: str | None = None,
    ) -> list[SalesByLocality]:
        """Return sales counts grouped by locality."""
        search_pattern = self._build_search_pattern(search)
        property_type_filter = self._build_property_type_filter(property_type)

        with self._db.connection() as conn:
            rows = conn.execute(
                GET_SALES_BY_LOCALITY_SQL,
                {
                    "limit": limit,
                    "search_pattern": search_pattern,
                    "property_type_filter": property_type_filter,
                },
            ).fetchall()

        return [
            SalesByLocality(
                locality=row[0],
                sales_count=row[1],
            )
            for row in rows
        ]

    def get_average_price_by_locality(
        self,
        limit: int = 20,
    ) -> list[AveragePriceByLocality]:
        """Return average purchase price grouped by locality."""
        with self._db.connection() as conn:
            rows = conn.execute(
                GET_AVERAGE_PRICE_BY_LOCALITY_SQL,
                {"limit": limit},
            ).fetchall()

        return [
            AveragePriceByLocality(
                locality=row[0],
                average_purchase_price=row[1],
            )
            for row in rows
        ]

    def get_sales_by_property_type(
        self,
        search: str | None = None,
        property_type: str | None = None,
    ) -> list[PropertyTypeSales]:
        """Return sales counts grouped by property type."""
        search_pattern = self._build_search_pattern(search)
        property_type_filter = self._build_property_type_filter(property_type)

        with self._db.connection() as conn:
            rows = conn.execute(
                GET_SALES_BY_PROPERTY_TYPE_SQL,
                {
                    "search_pattern": search_pattern,
                    "property_type_filter": property_type_filter,
                },
            ).fetchall()

        return [
            PropertyTypeSales(
                property_type=row[0],
                sales_count=row[1],
            )
            for row in rows
        ]

    def get_highest_sale_price(
        self,
        search: str | None = None,
        property_type: str | None = None,
    ) -> int | None:
        """Return the highest sale price."""
        search_pattern = self._build_search_pattern(search)
        property_type_filter = self._build_property_type_filter(property_type)

        with self._db.connection() as conn:
            result = conn.execute(
                GET_HIGHEST_SALE_PRICE_SQL,
                {
                    "search_pattern": search_pattern,
                    "property_type_filter": property_type_filter,
                },
            ).fetchone()

        return result[0]


    def get_locality_count(
        self,
        search: str | None = None,
        property_type: str | None = None,
    ) -> int:
        """Return the number of distinct localities."""
        search_pattern = self._build_search_pattern(search)
        property_type_filter = self._build_property_type_filter(property_type)

        with self._db.connection() as conn:
            result = conn.execute(
                GET_LOCALITY_COUNT_SQL,
                {
                    "search_pattern": search_pattern,
                    "property_type_filter": property_type_filter,
                },
            ).fetchone()

        return result[0]


    def get_average_sale_price(
        self,
        search: str | None = None,
        property_type: str | None = None,
    ):
        """Return the average sale price."""
        search_pattern = self._build_search_pattern(search)
        property_type_filter = self._build_property_type_filter(property_type)

        with self._db.connection() as conn:
            result = conn.execute(
                GET_AVERAGE_SALE_PRICE_SQL,
                {
                    "search_pattern": search_pattern,
                    "property_type_filter": property_type_filter,
                },
            ).fetchone()

        return result[0]

    def _build_search_pattern(self, search: str | None) -> str:
        """Build a SQL search pattern for locality filtering."""
        return f"%{search}%" if search else "%"
    
    def _build_property_type_filter(self, property_type: str | None) -> str:
        """Build a SQL property type filter."""
        return property_type if property_type else "%"