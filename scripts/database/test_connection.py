"""
Test PostgreSQL database connection.
"""

from backend.database.connection import Database


def main() -> None:
    """Open a database connection and run a test query."""
    db = Database()
    db.open()

    try:
        with db.connection() as conn:
            result = conn.execute("SELECT version();").fetchone()
            print(result[0])
    finally:
        db.close()


if __name__ == "__main__":
    main()