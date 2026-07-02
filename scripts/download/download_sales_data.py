"""
Download NSW property sales data.

Downloads weekly NSW property sales data from the NSW Valuer General.
"""

from backend.core.config import RAW_DATA_DIR
from backend.services.download_service import download_file

NSW_RAW_DATA_DIR = RAW_DATA_DIR / "nsw_valuer_general"

NSW_WEEKLY_SALES_URL = (
    "https://www.valuergeneral.nsw.gov.au/__psi/weekly/20260105.zip"
)

OUTPUT_FILENAME = "nsw_property_sales_weekly_2026-01-05.zip"


def main() -> None:
    """Download the NSW weekly property sales dataset."""
    output_path = download_file(
        url=NSW_WEEKLY_SALES_URL,
        destination_dir=NSW_RAW_DATA_DIR,
        filename=OUTPUT_FILENAME,
    )

    print(f"Downloaded NSW property sales data to: {output_path}")


if __name__ == "__main__":
    main()