"""
FastAPI dependencies.
"""

from fastapi import Request

from backend.database.connection import Database
from backend.services.analytics_service import AnalyticsService
from backend.services.investment_service import InvestmentService
from backend.services.rental_service import RentalService


def get_database(request: Request) -> Database:
    """Return the database connection manager from app state."""
    return request.app.state.db


def get_analytics_service(request: Request) -> AnalyticsService:
    """Return an analytics service using the app database."""
    db = get_database(request)
    return AnalyticsService(db)


def get_rental_service(request: Request) -> RentalService:
    db = get_database(request)
    return RentalService(db, AnalyticsService(db))


def get_investment_service(request: Request) -> InvestmentService:
    return InvestmentService(get_database(request))
