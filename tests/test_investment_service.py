from datetime import date

import pytest

from backend.services.investment_service import InvestmentService


def test_score_breakdown_is_auditable() -> None:
    row = (
        "NEWCASTLE",
        ["2300"],
        -32.93,
        151.77,
        700,
        5,
        278,
        1_027_500,
        6,
        250,
        3.54,
        12_058,
        13.99,
        1_933,
        16.94,
        60,
        70,
        50,
        80,
        40,
        100,
        65.5,
        "high",
        date(2026, 6, 30),
        date(2025, 12, 30),
        2021,
    )
    score = InvestmentService._score_from_row(row)
    assert sum(component.weight_pct for component in score.components) == pytest.approx(
        100
    )
    assert sum(
        component.contribution for component in score.components
    ) == pytest.approx(65.5)
    assert score.investment_score == pytest.approx(65.5)
    assert score.components[0].label == "Gross rental yield"
