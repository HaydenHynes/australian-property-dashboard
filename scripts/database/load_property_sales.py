"""
Load NSW property sales records into PostgreSQL.
"""

from backend.database.connection import Database
from backend.database.loader import load_property_sales
from backend.services.transform_service import transform_sales_record
from scripts.processing.parse_dat_file import NSW_ZIP_PATH, parse_all_b_records_from_zip


def main() -> None:
    """Parse, transform, and load NSW property sales records."""
    raw_records = parse_all_b_records_from_zip(NSW_ZIP_PATH)
    sales = [transform_sales_record(record) for record in raw_records]

    db = Database()
    db.open()

    try:
        load_property_sales(db, sales)
        print(f"Loaded {len(sales)} property sales into PostgreSQL.")
    finally:
        db.close()


if __name__ == "__main__":
    main()