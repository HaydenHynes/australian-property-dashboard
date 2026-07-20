"""Download official ABS Census demographic and Postal Area boundary files."""

from pathlib import Path

from backend.core.config import RAW_DATA_DIR
from backend.services.download_service import download_file

SOURCE_PAGE = "https://www.abs.gov.au/census/find-census-data/datapacks"
BOUNDARY_SOURCE_PAGE = (
    "https://www.abs.gov.au/statistics/standards/"
    "australian-statistical-geography-standard-asgs/"
    "edition-3-july-2021-june-2026/access-and-downloads/"
    "digital-boundary-files"
)

FILES = {
    "2021_GCP_POA_for_NSW_short-header.zip": (
        "https://www.abs.gov.au/census/find-census-data/datapacks/download/"
        "2021_GCP_POA_for_NSW_short-header.zip"
    ),
    "2016_GCP_POA_for_NSW_short-header.zip": (
        "https://www.abs.gov.au/census/find-census-data/datapacks/download/"
        "2016_GCP_POA_for_NSW_short-header.zip"
    ),
    "POA_2021_AUST_GDA2020_SHP.zip": (
        "https://www.abs.gov.au/statistics/standards/"
        "australian-statistical-geography-standard-asgs/"
        "edition-3-july-2021-june-2026/access-and-downloads/"
        "digital-boundary-files/POA_2021_AUST_GDA2020_SHP.zip"
    ),
}


def download_all(destination: Path, overwrite: bool = False) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for filename, url in FILES.items():
        target = destination / filename
        if target.exists() and not overwrite:
            print(f"Already downloaded: {filename}")
            continue
        download_file(url, destination, filename, overwrite=overwrite)
        print(f"Downloaded: {filename}")


if __name__ == "__main__":
    download_all(RAW_DATA_DIR / "abs_demographics")
