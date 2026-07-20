import zipfile
from types import SimpleNamespace

import pytest

from backend.database.demographic_loader import (
    SCORE_WEIGHTS,
    _normalise_postcode,
    _shape_centroid,
    read_census_demographics,
)


def test_score_weights_sum_to_one() -> None:
    assert sum(SCORE_WEIGHTS.values()) == pytest.approx(1)


def test_normalises_abs_postal_area_code() -> None:
    assert _normalise_postcode("POA2300") == "2300"
    assert _normalise_postcode("ZZZZ") is None


def test_shape_centroid_uses_polygon_ring() -> None:
    shape = SimpleNamespace(
        parts=[0],
        points=[(150.0, -34.0), (151.0, -34.0), (151.0, -33.0), (150.0, -33.0)],
        bbox=[150.0, -34.0, 151.0, -33.0],
    )
    longitude, latitude = _shape_centroid(shape)
    assert longitude == pytest.approx(150.5)
    assert latitude == pytest.approx(-33.5)


def test_reads_population_and_income_from_abs_datapack(tmp_path) -> None:
    archive_path = tmp_path / "2021_GCP_POA_for_NSW_short-header.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr(
            "data/2021Census_G01_NSW_POA.csv",
            "POA_CODE_2021,Tot_P_P\nPOA2300,12058\n",
        )
        archive.writestr(
            "data/2021Census_G02_NSW_POA.csv",
            "POA_CODE_2021,Median_tot_prsnl_inc_weekly,Median_tot_hhd_inc_weekly\n"
            "POA2300,892,1933\n",
        )
    assert read_census_demographics(archive_path, 2021) == [
        ("2300", 2021, 12058, 892, 1933)
    ]
