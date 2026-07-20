"""Load downloaded NSW rental-bond workbooks into PostgreSQL."""

from backend.core.config import RAW_DATA_DIR
from backend.database.connection import Database
from backend.database.rental_loader import load_all_rental_workbooks


def main() -> None:
    db = Database()
    db.open()
    try:
        total = load_all_rental_workbooks(db, RAW_DATA_DIR / "rental_bonds")
        print(f"Rental-bond rows available: {total:,}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
