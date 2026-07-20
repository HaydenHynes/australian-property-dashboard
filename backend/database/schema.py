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

CREATE_RENTAL_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS rental_data_imports (
    source_file TEXT PRIMARY KEY,
    source_url TEXT NOT NULL,
    sha256 TEXT NOT NULL,
    row_count INTEGER NOT NULL,
    imported_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS rental_bond_lodgements (
    id BIGSERIAL PRIMARY KEY,
    source_file TEXT NOT NULL REFERENCES rental_data_imports(source_file),
    source_row INTEGER NOT NULL,
    lodgement_date DATE NOT NULL,
    postcode CHAR(4) NOT NULL,
    dwelling_type CHAR(1),
    bedrooms SMALLINT,
    weekly_rent NUMERIC(10, 2) NOT NULL,
    UNIQUE (source_file, source_row)
);

CREATE TABLE IF NOT EXISTS suburb_postcodes (
    locality TEXT NOT NULL,
    postcode CHAR(4) NOT NULL,
    supporting_sales INTEGER NOT NULL,
    PRIMARY KEY (locality, postcode)
);

CREATE TABLE IF NOT EXISTS rental_market_monthly (
    month DATE NOT NULL,
    postcode CHAR(4) NOT NULL,
    dwelling_type CHAR(1) NOT NULL,
    bedrooms SMALLINT NOT NULL,
    median_weekly_rent NUMERIC(10, 2) NOT NULL,
    lower_quartile_rent NUMERIC(10, 2),
    upper_quartile_rent NUMERIC(10, 2),
    lodgement_count INTEGER NOT NULL,
    PRIMARY KEY (month, postcode, dwelling_type, bedrooms)
);

CREATE INDEX IF NOT EXISTS idx_rental_bonds_postcode_date
    ON rental_bond_lodgements (postcode, lodgement_date);
CREATE INDEX IF NOT EXISTS idx_rental_bonds_type_date
    ON rental_bond_lodgements (dwelling_type, lodgement_date);
CREATE INDEX IF NOT EXISTS idx_suburb_postcodes_postcode
    ON suburb_postcodes (postcode);
CREATE INDEX IF NOT EXISTS idx_rental_market_postcode_month
    ON rental_market_monthly (postcode, month);
"""

CREATE_INVESTMENT_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS abs_demographic_imports (
    source_file TEXT PRIMARY KEY,
    source_url TEXT NOT NULL,
    sha256 TEXT NOT NULL,
    census_year SMALLINT,
    row_count INTEGER NOT NULL,
    imported_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS postcode_demographics (
    postcode CHAR(4) NOT NULL,
    census_year SMALLINT NOT NULL,
    population INTEGER NOT NULL,
    median_personal_income_weekly INTEGER,
    median_household_income_weekly INTEGER,
    PRIMARY KEY (postcode, census_year)
);

CREATE TABLE IF NOT EXISTS postcode_geography (
    postcode CHAR(4) PRIMARY KEY,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    area_sq_km DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS investment_scores (
    locality TEXT PRIMARY KEY,
    postcodes TEXT[] NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    median_weekly_rent NUMERIC(10, 2) NOT NULL,
    rent_growth_1y_pct DOUBLE PRECISION NOT NULL,
    rental_count INTEGER NOT NULL,
    median_sale_price NUMERIC(14, 2) NOT NULL,
    price_growth_5y_annualised_pct DOUBLE PRECISION NOT NULL,
    sales_count INTEGER NOT NULL,
    gross_yield_pct DOUBLE PRECISION NOT NULL,
    population_2021 INTEGER NOT NULL,
    population_growth_5y_pct DOUBLE PRECISION NOT NULL,
    median_household_income_weekly NUMERIC(10, 2) NOT NULL,
    income_growth_5y_pct DOUBLE PRECISION NOT NULL,
    yield_score DOUBLE PRECISION NOT NULL,
    price_growth_score DOUBLE PRECISION NOT NULL,
    rent_growth_score DOUBLE PRECISION NOT NULL,
    population_growth_score DOUBLE PRECISION NOT NULL,
    income_growth_score DOUBLE PRECISION NOT NULL,
    evidence_score DOUBLE PRECISION NOT NULL,
    investment_score DOUBLE PRECISION NOT NULL,
    confidence TEXT NOT NULL,
    rental_data_as_of DATE NOT NULL,
    sales_data_as_of DATE NOT NULL,
    demographic_data_as_of SMALLINT NOT NULL,
    refreshed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_postcode_demographics_year
    ON postcode_demographics (census_year, postcode);
CREATE INDEX IF NOT EXISTS idx_investment_scores_score
    ON investment_scores (investment_score DESC);
CREATE INDEX IF NOT EXISTS idx_investment_scores_yield
    ON investment_scores (gross_yield_pct DESC);
CREATE INDEX IF NOT EXISTS idx_investment_scores_price
    ON investment_scores (median_sale_price);
"""


def create_tables(db: Database) -> None:
    """Create database tables."""
    with db.connection() as conn:
        conn.execute(CREATE_PROPERTY_SALES_TABLE_SQL)
        conn.execute(CREATE_ANALYTICS_INDEXES_SQL)
        conn.execute(CREATE_RENTAL_TABLES_SQL)
        conn.execute(CREATE_INVESTMENT_TABLES_SQL)
        conn.commit()
