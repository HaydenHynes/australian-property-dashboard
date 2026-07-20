import pytest

from backend.services.analytics_service import (
    MARKET_SALE_FILTER_SQL,
    AnalyticsService,
)


def test_growth_returns_percentage_change() -> None:
    assert AnalyticsService._growth(880_000, 800_000) == pytest.approx(10)


def test_growth_handles_missing_or_zero_baseline() -> None:
    assert AnalyticsService._growth(None, 800_000) is None
    assert AnalyticsService._growth(800_000, None) is None
    assert AnalyticsService._growth(800_000, 0) is None


def test_market_rule_is_transparent_and_full_interest_only() -> None:
    assert "purchase_price BETWEEN 50000 AND 20000000" in MARKET_SALE_FILTER_SQL
    assert "sale_code" in MARKET_SALE_FILTER_SQL
    assert "percent_interest_of_sale" in MARKET_SALE_FILTER_SQL
    assert "DATE '2001-01-01'" in MARKET_SALE_FILTER_SQL
