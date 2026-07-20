from unittest.mock import Mock

from backend.services.dashboard_service import DashboardService


def test_dashboard_summary_uses_single_consistent_metric_query() -> None:
    analytics = Mock()
    analytics.get_summary_metrics.return_value = {
        "total_sales": 100,
        "median_sale_price": 850_000.0,
        "annual_growth_pct": 4.5,
        "locality_count": 1,
        "excluded_sales": 5,
        "data_as_of": None,
    }

    result = DashboardService(analytics).get_summary("Sydney", "R", 2025)

    assert result.median_sale_price == 850_000.0
    analytics.get_summary_metrics.assert_called_once_with(
        search="Sydney",
        property_type="R",
        contract_year=2025,
    )
