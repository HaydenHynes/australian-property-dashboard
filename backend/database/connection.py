"""
Database connection management.

Provides a pooled PostgreSQL connection interface for the application.
"""

from collections.abc import Generator
from contextlib import contextmanager

import psycopg
from psycopg_pool import ConnectionPool

from backend.core.config import DATABASE_URL


class Database:
    """PostgreSQL database connection manager."""

    def __init__(self, database_url: str | None = DATABASE_URL) -> None:
        """Initialize the database connection manager."""
        if not database_url:
            raise ValueError("DATABASE_URL is not set.")

        self._pool = ConnectionPool(
            conninfo=database_url,
            min_size=1,
            max_size=5,
            open=False,
        )

    def open(self) -> None:
        """Open the database connection pool."""
        self._pool.open()

    def close(self) -> None:
        """Close the database connection pool."""
        self._pool.close()

    @contextmanager
    def connection(self) -> Generator[psycopg.Connection, None, None]:
        """Borrow a connection from the pool and return it automatically."""
        with self._pool.connection() as conn:
            yield conn