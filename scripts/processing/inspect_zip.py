"""
Inspect the contents of a NSW property sales ZIP file.
"""

import sys
import zipfile
from pathlib import Path

from scripts.processing.parse_dat_file import NSW_ZIP_PATH


def inspect_zip(zip_path: Path) -> None:
    """Print file names and sizes inside a ZIP archive."""
    print(f"Inspecting: {zip_path.resolve()}")
    print()

    with zipfile.ZipFile(zip_path) as archive:
        for file_info in archive.infolist():
            print(f"File: {file_info.filename}")
            print(f"Size: {file_info.file_size:,} bytes")
            print()


def main() -> None:
    """Inspect a ZIP file passed by argument, or the default weekly ZIP."""
    zip_path = Path(sys.argv[1]) if len(sys.argv) > 1 else NSW_ZIP_PATH
    inspect_zip(zip_path)


if __name__ == "__main__":
    main()