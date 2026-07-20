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

CREATE_ANALYTICS_INDEXES_SQL = """
CREATE INDEX IF NOT EXISTS idx_property_sales_contract_date
    ON property_sales (contract_date);
CREATE INDEX IF NOT EXISTS idx_property_sales_locality
    ON property_sales (property_locality);
CREATE INDEX IF NOT EXISTS idx_property_sales_nature_date
    ON property_sales (nature_of_property, contract_date);
CREATE INDEX IF NOT EXISTS idx_property_sales_market_lookup
    ON property_sales (
        property_locality,
        nature_of_property,
        contract_date,
        purchase_price
    );
"""


def create_tables(db: Database) -> None:
    """Create database tables."""
    with db.connection() as conn:
        conn.execute(CREATE_PROPERTY_SALES_TABLE_SQL)
        conn.execute(CREATE_ANALYTICS_INDEXES_SQL)
        conn.commit()
