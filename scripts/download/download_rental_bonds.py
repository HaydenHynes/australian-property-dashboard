"""Download official NSW Fair Trading rental-bond lodgement workbooks."""

from pathlib import Path

from backend.core.config import RAW_DATA_DIR
from backend.services.download_service import download_file

SOURCE_PAGE = (
    "https://www.nsw.gov.au/housing-and-construction/"
    "rental-forms-surveys-and-data/rental-bond-data"
)

WORKBOOKS = {
    "rental_bond_lodgements_2021.xlsx": (
        "https://www.nsw.gov.au/sites/default/files/noindex/2023-11/"
        "Rental-bond-lodgements-year-2021.xlsx"
    ),
    "rental_bond_lodgements_2022.xlsx": (
        "https://www.nsw.gov.au/sites/default/files/noindex/2023-11/"
        "RentalBond_Lodgements_Year_2022.xlsx"
    ),
    "rental_bond_lodgements_2023.xlsx": (
        "https://www.nsw.gov.au/sites/default/files/noindex/2024-05/"
        "RentalBond_Lodgements_Year_2023.xlsx"
    ),
    "rental_bond_lodgements_2024.xlsx": (
        "https://www.nsw.gov.au/sites/default/files/noindex/2025-01/"
        "rental-bond-lodgements-year-2024_1.xlsx"
    ),
    "rental_bond_lodgements_2025.xlsx": (
        "https://www.nsw.gov.au/sites/default/files/noindex/2026-01/"
        "rentalbond_lodgements_year_2025.xlsx"
    ),
    "rental_bond_lodgements_2026_01.xlsx": (
        "https://www.nsw.gov.au/sites/default/files/noindex/2026-02/"
        "rentalbond_lodgements_january_2026.xlsx"
    ),
    "rental_bond_lodgements_2026_02.xlsx": (
        "https://www.nsw.gov.au/sites/default/files/noindex/2026-03/"
        "rentalbond_lodgements_february_2026.xlsx"
    ),
    "rental_bond_lodgements_2026_03.xlsx": (
        "https://www.nsw.gov.au/sites/default/files/noindex/2026-04/"
        "rentalbond_lodgements_march_2026.xlsx"
    ),
    "rental_bond_lodgements_2026_04.xlsx": (
        "https://www.nsw.gov.au/sites/default/files/noindex/2026-05/"
        "rentalbond_lodgements_april_2026.xlsx"
    ),
    "rental_bond_lodgements_2026_05.xlsx": (
        "https://www.nsw.gov.au/sites/default/files/noindex/2026-06/"
        "rentalbond_lodgements_may_2026.xlsx"
    ),
    "rental_bond_lodgements_2026_06.xlsx": (
        "https://www.nsw.gov.au/sites/default/files/noindex/2026-07/"
        "rentalbond_lodgements_june_2026.xlsx"
    ),
}


def download_all(destination: Path, overwrite: bool = False) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for filename, url in WORKBOOKS.items():
        target = destination / filename
        if target.exists() and not overwrite:
            print(f"Already downloaded: {filename}")
            continue
        download_file(url, destination, filename, overwrite=overwrite)
        print(f"Downloaded: {filename}")


if __name__ == "__main__":
    download_all(RAW_DATA_DIR / "rental_bonds")
