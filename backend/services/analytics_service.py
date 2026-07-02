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
FROM property_sales;
"""

GET_TOP_SALES_SQL = """
SELECT
    property_locality,
    property_street_name,
    property_house_number,
    purchase_price,
    contract_date
FROM property_sales
WHERE purchase_price IS NOT NULL
ORDER BY purchase_price DESC
LIMIT %(limit)s;
"""

GET_SALES_BY_LOCALITY_SQL = """
SELECT
    property_locality,
    COUNT(*) AS sales_count
FROM property_sales
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
GROUP BY nature_of_property
ORDER BY sales_count DESC;
"""

class AnalyticsService:
    """Provides analytics queries over property sales."""

    def __init__(self, db: Database) -> None:
        """Initialize the analytics service."""
        self._db = db

    def get_total_sales(self) -> int:
        """Return the total number of property sales."""
        with self._db.connection() as conn:
            result = conn.execute(GET_TOTAL_SALES_SQL).fetchone()

        return result[0]
    
    def get_top_sales(self, limit: int = 20) -> list[TopSale]:
      """Return the highest property sales by purchase price."""
      with self._db.connection() as conn:
          rows = conn.execute(
              GET_TOP_SALES_SQL,
              {"limit": limit},
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
    
    def get_sales_by_locality(self, limit: int = 20) -> list[SalesByLocality]:
      """Return sales counts grouped by locality."""
      with self._db.connection() as conn:
          rows = conn.execute(GET_SALES_BY_LOCALITY_SQL, {"limit": limit}).fetchall()

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
      
    def get_sales_by_property_type(self) -> list[PropertyTypeSales]:
      """Return sales counts grouped by property type."""
      with self._db.connection() as conn:
          rows = conn.execute(GET_SALES_BY_PROPERTY_TYPE_SQL).fetchall()

      return [
          PropertyTypeSales(
              property_type=row[0],
              sales_count=row[1],
          )
          for row in rows
      ]