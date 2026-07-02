"""
Database schema management.
"""

from backend.database.connection import Database

CREATE_PROPERTY_SALES_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS property_sales (
    id SERIAL PRIMARY KEY,
    record_type TEXT NOT NULL,
    district_code TEXT NOT NULL,
    property_id TEXT NOT NULL,
    sale_counter TEXT NOT NULL,
    download_datetime TEXT NOT NULL,
    property_name TEXT,
    property_unit_number TEXT,
    property_house_number TEXT,
    property_street_name TEXT,
    property_locality TEXT,
    property_postcode TEXT,
    area NUMERIC,
    area_type TEXT,
    contract_date DATE,
    settlement_date DATE,
    purchase_price INTEGER,
    zoning TEXT,
    nature_of_property TEXT,
    primary_purpose TEXT,
    strata_lot_number TEXT,
    component_code TEXT,
    sale_code TEXT,
    percent_interest_of_sale TEXT,
    dealing_number TEXT,
    UNIQUE (property_id, sale_counter, dealing_number)
);
"""


def create_tables(db: Database) -> None:
    """Create database tables."""
    with db.connection() as conn:
        conn.execute(CREATE_PROPERTY_SALES_TABLE_SQL)
        conn.commit()