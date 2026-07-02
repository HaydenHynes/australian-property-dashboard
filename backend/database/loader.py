"""
Database loading utilities.
"""

from dataclasses import asdict

from backend.database.connection import Database
from backend.models.property_sale import PropertySale

INSERT_PROPERTY_SALE_SQL = """
INSERT INTO property_sales (
    record_type,
    district_code,
    property_id,
    sale_counter,
    download_datetime,
    property_name,
    property_unit_number,
    property_house_number,
    property_street_name,
    property_locality,
    property_postcode,
    area,
    area_type,
    contract_date,
    settlement_date,
    purchase_price,
    zoning,
    nature_of_property,
    primary_purpose,
    strata_lot_number,
    component_code,
    sale_code,
    percent_interest_of_sale,
    dealing_number
)
VALUES (
    %(record_type)s,
    %(district_code)s,
    %(property_id)s,
    %(sale_counter)s,
    %(download_datetime)s,
    %(property_name)s,
    %(property_unit_number)s,
    %(property_house_number)s,
    %(property_street_name)s,
    %(property_locality)s,
    %(property_postcode)s,
    %(area)s,
    %(area_type)s,
    %(contract_date)s,
    %(settlement_date)s,
    %(purchase_price)s,
    %(zoning)s,
    %(nature_of_property)s,
    %(primary_purpose)s,
    %(strata_lot_number)s,
    %(component_code)s,
    %(sale_code)s,
    %(percent_interest_of_sale)s,
    %(dealing_number)s
)
ON CONFLICT (property_id, sale_counter, dealing_number)
DO NOTHING;
"""


def load_property_sales(db: Database, sales: list[PropertySale]) -> None:
    """Load property sales records into PostgreSQL."""
    sale_dicts = [asdict(sale) for sale in sales]

    with db.connection() as conn:
        with conn.cursor() as cursor:
            cursor.executemany(INSERT_PROPERTY_SALE_SQL, sale_dicts)

        conn.commit()