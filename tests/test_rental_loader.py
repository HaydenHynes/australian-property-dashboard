from datetime import date, datetime
from decimal import Decimal

from backend.database.rental_loader import (
    _normalise_bedrooms,
    _normalise_date,
    _normalise_postcode,
    _normalise_rent,
)


def test_normalises_source_values() -> None:
    assert _normalise_date(datetime(2026, 6, 30)) == date(2026, 6, 30)
    assert _normalise_postcode(800) == "0800"
    assert _normalise_rent("$1,250") == Decimal("1250")
    assert _normalise_bedrooms("3") == 3


def test_rejects_invalid_source_values() -> None:
    assert _normalise_date("unknown") is None
    assert _normalise_postcode("20A0") is None
    assert _normalise_rent("U") is None
    assert _normalise_bedrooms("U") is None
