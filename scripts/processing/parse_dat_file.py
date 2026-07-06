"""
Parse B records from NSW Valuer General property sales ZIP files.

Supports:
- ZIP files containing .DAT files directly
- Annual ZIP files containing nested weekly ZIP files
"""

from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from backend.core.config import RAW_DATA_DIR

NSW_ZIP_PATH = (
    RAW_DATA_DIR
    / "nsw_valuer_general"
    / "nsw_property_sales_weekly_2026-01-05.zip"
)

RECORD_TYPE_INDEX = 0
DISTRICT_CODE_INDEX = 1
PROPERTY_ID_INDEX = 2
SALE_COUNTER_INDEX = 3
DOWNLOAD_DATETIME_INDEX = 4
PROPERTY_NAME_INDEX = 5
PROPERTY_UNIT_NUMBER_INDEX = 6
PROPERTY_HOUSE_NUMBER_INDEX = 7
PROPERTY_STREET_NAME_INDEX = 8
PROPERTY_LOCALITY_INDEX = 9
PROPERTY_POSTCODE_INDEX = 10
AREA_INDEX = 11
AREA_TYPE_INDEX = 12
CONTRACT_DATE_INDEX = 13
SETTLEMENT_DATE_INDEX = 14
PURCHASE_PRICE_INDEX = 15
ZONING_INDEX = 16
NATURE_OF_PROPERTY_INDEX = 17
PRIMARY_PURPOSE_INDEX = 18
STRATA_LOT_NUMBER_INDEX = 19
COMPONENT_CODE_INDEX = 20
SALE_CODE_INDEX = 21
PERCENT_INTEREST_OF_SALE_INDEX = 22
DEALING_NUMBER_INDEX = 23


def parse_b_record(line: str) -> dict[str, str]:
    """Parse a B record into a dictionary."""
    fields = line.split(";")

    return {
        "record_type": fields[RECORD_TYPE_INDEX],
        "district_code": fields[DISTRICT_CODE_INDEX],
        "property_id": fields[PROPERTY_ID_INDEX],
        "sale_counter": fields[SALE_COUNTER_INDEX],
        "download_datetime": fields[DOWNLOAD_DATETIME_INDEX],
        "property_name": fields[PROPERTY_NAME_INDEX],
        "property_unit_number": fields[PROPERTY_UNIT_NUMBER_INDEX],
        "property_house_number": fields[PROPERTY_HOUSE_NUMBER_INDEX],
        "property_street_name": fields[PROPERTY_STREET_NAME_INDEX],
        "property_locality": fields[PROPERTY_LOCALITY_INDEX],
        "property_postcode": fields[PROPERTY_POSTCODE_INDEX],
        "area": fields[AREA_INDEX],
        "area_type": fields[AREA_TYPE_INDEX],
        "contract_date": fields[CONTRACT_DATE_INDEX],
        "settlement_date": fields[SETTLEMENT_DATE_INDEX],
        "purchase_price": fields[PURCHASE_PRICE_INDEX],
        "zoning": fields[ZONING_INDEX],
        "nature_of_property": fields[NATURE_OF_PROPERTY_INDEX],
        "primary_purpose": fields[PRIMARY_PURPOSE_INDEX],
        "strata_lot_number": fields[STRATA_LOT_NUMBER_INDEX],
        "component_code": fields[COMPONENT_CODE_INDEX],
        "sale_code": fields[SALE_CODE_INDEX],
        "percent_interest_of_sale": fields[PERCENT_INTEREST_OF_SALE_INDEX],
        "dealing_number": fields[DEALING_NUMBER_INDEX],
    }


def parse_b_records_from_dat_bytes(dat_bytes: bytes) -> list[dict[str, str]]:
    """Parse all B records from raw .DAT file bytes."""
    records = []

    for raw_line in dat_bytes.splitlines():
        line = raw_line.decode("utf-8", errors="replace").strip()

        if not line.startswith("B;"):
            continue

        records.append(parse_b_record(line))

    return records


def parse_b_records_from_open_zip(zip_file: ZipFile) -> list[dict[str, str]]:
    """Parse B records from .DAT files inside an already-open ZIP file."""
    records = []

    for filename in zip_file.namelist():
        if not filename.upper().endswith(".DAT"):
            continue

        dat_bytes = zip_file.read(filename)
        records.extend(parse_b_records_from_dat_bytes(dat_bytes))

    return records


def parse_all_b_records_from_zip(zip_path: Path) -> list[dict[str, str]]:
    """Parse B records from a ZIP file, including nested ZIP files."""
    all_records = []

    with ZipFile(zip_path, "r") as outer_zip:
        direct_dat_records = parse_b_records_from_open_zip(outer_zip)
        all_records.extend(direct_dat_records)

        for filename in outer_zip.namelist():
            if not filename.lower().endswith(".zip"):
                continue

            nested_zip_bytes = outer_zip.read(filename)

            with ZipFile(BytesIO(nested_zip_bytes), "r") as nested_zip:
                nested_records = parse_b_records_from_open_zip(nested_zip)
                all_records.extend(nested_records)

    return all_records


def main() -> None:
    """Parse and preview B records from a property sales ZIP archive."""
    records = parse_all_b_records_from_zip(NSW_ZIP_PATH)

    print(f"Parsed {len(records)} B records from ZIP archive.")
    print()

    for record in records[:5]:
        print(record)


if __name__ == "__main__":
    main()