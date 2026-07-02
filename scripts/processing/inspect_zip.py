"""
Inspect the contents of a ZIP file without extracting it.
"""

from zipfile import ZipFile

from backend.core.config import RAW_DATA_DIR

NSW_ZIP_PATH = (
    RAW_DATA_DIR
    / "nsw_valuer_general"
    / "nsw_property_sales_weekly_2026-01-05.zip"
)


def main() -> None:
    """List the contents of the NSW property sales ZIP file."""
    with ZipFile(NSW_ZIP_PATH, "r") as zip_file:
        print(f"Inspecting: {NSW_ZIP_PATH}")
        print()

        for file_info in zip_file.infolist():
            print(f"File: {file_info.filename}")
            print(f"Size: {file_info.file_size:,} bytes")
            print()


if __name__ == "__main__":
    main()