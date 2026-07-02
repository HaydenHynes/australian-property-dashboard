"""
Create database tables.
"""

from backend.database.connection import Database
from backend.database.schema import create_tables


def main() -> None:
    """Create all database tables."""
    db = Database()
    db.open()

    try:
        create_tables(db)
        print("Database tables created successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    main()