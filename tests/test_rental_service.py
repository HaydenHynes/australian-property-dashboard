import pytest

from backend.services.rental_service import RentalService


@pytest.mark.parametrize(
    ("count", "expected"),
    [(5, "low"), (10, "medium"), (29, "medium"), (30, "high")],
)
def test_confidence_thresholds(count: int, expected: str) -> None:
    assert RentalService._confidence(count) == expected


def test_rent_growth() -> None:
    assert RentalService._growth(660, 600) == pytest.approx(10)
    assert RentalService._growth(660, 0) is None
