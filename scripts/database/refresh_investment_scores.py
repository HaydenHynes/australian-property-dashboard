"""Refresh explainable investment scores after sales or rental imports."""

from backend.database.connection import Database
from backend.database.demographic_loader import refresh_investment_scores


def main() -> None:
    db = Database()
    db.open()
    try:
        count = refresh_investment_scores(db)
        print(f"Refreshed {count:,} explainable investment scores")
    finally:
        db.close()


if __name__ == "__main__":
    main()
