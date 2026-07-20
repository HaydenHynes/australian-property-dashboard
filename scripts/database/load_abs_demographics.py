"""Load ABS Census demographics and refresh the investment score snapshot."""

from backend.core.config import RAW_DATA_DIR
from backend.database.connection import Database
from backend.database.demographic_loader import (
    load_abs_demographics,
    refresh_investment_scores,
)


def main() -> None:
    db = Database()
    db.open()
    try:
        census_count, geography_count = load_abs_demographics(
            db, RAW_DATA_DIR / "abs_demographics"
        )
        score_count = refresh_investment_scores(db)
        print(f"Loaded {census_count:,} ABS Census records")
        print(f"Loaded {geography_count:,} NSW Postal Area map points")
        print(f"Refreshed {score_count:,} explainable investment scores")
    finally:
        db.close()


if __name__ == "__main__":
    main()
