"""
Test the reusable download service.
"""

from backend.core.config import RAW_DATA_DIR
from backend.services.download_service import download_file


def main() -> None:
    """Run a basic download test."""
    test_url = "https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore"
    output_path = download_file(
        url=test_url,
        destination_dir=RAW_DATA_DIR,
        filename="test_python_gitignore.txt",
    )

    print(f"Downloaded file to: {output_path}")


if __name__ == "__main__":
    main()