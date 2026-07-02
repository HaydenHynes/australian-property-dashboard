"""
Property sale domain model.
"""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class PropertySale:
    """Represents a typed NSW property sale record."""

    record_type: str
    district_code: str
    property_id: str
    sale_counter: str
    download_datetime: str
    property_name: str | None
    property_unit_number: str | None
    property_house_number: str | None
    property_street_name: str | None
    property_locality: str | None
    property_postcode: str | None
    area: float | None
    area_type: str | None
    contract_date: date | None
    settlement_date: date | None
    purchase_price: int | None
    zoning: str | None
    nature_of_property: str | None
    primary_purpose: str | None
    strata_lot_number: str | None
    component_code: str | None
    sale_code: str | None
    percent_interest_of_sale: str | None
    dealing_number: str | None