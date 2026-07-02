"""
Demo analytics service queries.
"""

from backend.database.connection import Database
from backend.services.analytics_service import AnalyticsService


def main() -> None:
    """Run analytics service demo."""
    db = Database()
    db.open()

    try:
        analytics = AnalyticsService(db)

        total_sales = analytics.get_total_sales()
        print(f"Total sales: {total_sales}")

        print()
        print("Top sales:")
        for sale in analytics.get_top_sales(limit=5):
            print(sale)

        print()
        print("Sales by locality:")
        for locality in analytics.get_sales_by_locality(limit=5):
            print(locality)
            
        print()
        print("Average price by locality:")
        for locality in analytics.get_average_price_by_locality(limit=5):
            print(locality)
        
        print()
        print("Sales by property type:")
        for property_type in analytics.get_sales_by_property_type():
            print(property_type)

    finally:
        db.close()


if __name__ == "__main__":
    main()