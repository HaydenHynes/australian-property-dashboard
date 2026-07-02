"""
Parse B records from a NSW Valuer General .DAT file.

Field positions are based on the official NSW Valuer General
Current Property Sales Data File format.
"""

from pathlib import Path
from zipfile import ZipFile

from backend.core.config import RAW_DATA_DIR

NSW_ZIP_PATH = (
    RAW_DATA_DIR
    / "nsw_valuer_general"
    / "nsw_property_sales_weekly_2026-01-05.zip"
)

TARGET_DAT_FILE = "214_SALES_DATA_NNME_05012026.DAT"

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


def parse_b_records_from_zip(zip_path: Path, dat_filename: str) -> list[dict[str, str]]:
    """Parse all B records from a .DAT file inside a ZIP archive."""
    records = []

    with ZipFile(zip_path, "r") as zip_file:
        with zip_file.open(dat_filename) as dat_file:
            for raw_line in dat_file:
                line = raw_line.decode("utf-8", errors="replace").strip()

                if not line.startswith("B;"):
                    continue

                records.append(parse_b_record(line))

    return records

def get_dat_filenames(zip_path: Path) -> list[str]:
    """Return all .DAT filenames from a ZIP archive."""
    with ZipFile(zip_path, "r") as zip_file:
        return [
            filename
            for filename in zip_file.namelist()
            if filename.upper().endswith(".DAT")
        ]

def parse_all_b_records_from_zip(zip_path: Path) -> list[dict[str, str]]:
    """Parse B records from all .DAT files inside a ZIP archive."""
    all_records = []

    for dat_filename in get_dat_filenames(zip_path):
        records = parse_b_records_from_zip(
            zip_path=zip_path,
            dat_filename=dat_filename,
        )
        all_records.extend(records)

    return all_records

def main() -> None:
    """Parse and preview B records from all .DAT files in the ZIP archive."""
    records = parse_all_b_records_from_zip(NSW_ZIP_PATH)

    print(f"Parsed {len(records)} B records from all .DAT files.")
    print()

    for record in records[:5]:
        print(record)


if __name__ == "__main__":
    main()