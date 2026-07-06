"""
Load NSW property sales records into PostgreSQL.
"""

from pathlib import Path

from backend.core.config import RAW_DATA_DIR
from backend.database.connection import Database
from backend.database.loader import load_property_sales
from backend.services.transform_service import transform_sales_record
from scripts.processing.parse_dat_file import parse_all_b_records_from_zip

RAW_SALES_DIR = RAW_DATA_DIR / "nsw_valuer_general"


def load_zip_file(db: Database, zip_path: Path) -> int:
    """Parse, transform, and load records from one ZIP file."""
    raw_records = parse_all_b_records_from_zip(zip_path)
    sales = [transform_sales_record(record) for record in raw_records]

    load_property_sales(db, sales)

    return len(sales)


def main() -> None:
    """Parse, transform, and load every NSW property sales ZIP file."""
    zip_paths = sorted(RAW_SALES_DIR.glob("*.zip"))

    if not zip_paths:
        print(f"No ZIP files found in {RAW_SALES_DIR}")
        return

    db = Database()
    db.open()

    try:
        total_records = 0

        for zip_path in zip_paths:
            print(f"Loading {zip_path.name}...")
            record_count = load_zip_file(db, zip_path)
            total_records += record_count
            print(f"Processed {record_count} records from {zip_path.name}")

        print(f"Finished processing {len(zip_paths)} ZIP files.")
        print(f"Total parsed records: {total_records}")
    finally:
        db.close()


if __name__ == "__main__":
    main()