"""
Export parsed NSW property sales records to a processed CSV file.
"""
import csv
from dataclasses import asdict
from pathlib import Path

from backend.core.config import PROCESSED_DATA_DIR
from backend.services.transform_service import transform_sales_record
from scripts.processing.parse_dat_file import NSW_ZIP_PATH, parse_all_b_records_from_zip

OUTPUT_DIR = PROCESSED_DATA_DIR / "nsw_valuer_general"
OUTPUT_CSV_PATH = OUTPUT_DIR / "nsw_property_sales_weekly_2026-01-05.csv"


def export_records_to_csv(records: list[object], output_path: Path) -> None:
    """Export parsed records to a CSV file."""
    if not records:
        raise ValueError("No records available to export.")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    record_dicts = [asdict(record) for record in records]
    fieldnames = list(record_dicts[0].keys())

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(record_dicts)


def main() -> None:
    """Parse, transform, and export NSW sales records to CSV."""
    records = parse_all_b_records_from_zip(NSW_ZIP_PATH)
    transformed_records = [
        transform_sales_record(record)
        for record in records
    ]

    export_records_to_csv(transformed_records, OUTPUT_CSV_PATH)

    print(f"Exported {len(transformed_records)} records to: {OUTPUT_CSV_PATH}")

if __name__ == "__main__":
    main()