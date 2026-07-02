"""
Preview a NSW Valuer General .DAT file inside a ZIP archive.
"""

from zipfile import ZipFile

from backend.core.config import RAW_DATA_DIR

NSW_ZIP_PATH = (
    RAW_DATA_DIR
    / "nsw_valuer_general"
    / "nsw_property_sales_weekly_2026-01-05.zip"
)

TARGET_DAT_FILE = "214_SALES_DATA_NNME_05012026.DAT"


def main() -> None:
    """Print the first few lines of a .DAT file without extracting it."""
    with ZipFile(NSW_ZIP_PATH, "r") as zip_file:
        with zip_file.open(TARGET_DAT_FILE) as dat_file:
            for line_number, raw_line in enumerate(dat_file, start=1):
                line = raw_line.decode("utf-8", errors="replace").strip()
                print(f"{line_number}: {line}")

                if line_number >= 10:
                    break


if __name__ == "__main__":
    main()