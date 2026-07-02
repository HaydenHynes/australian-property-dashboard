"""
Transform parsed NSW property sales records into typed values.
"""

from datetime import date, datetime

from backend.models.property_sale import PropertySale


def empty_string_to_none(value: str) -> str | None:
    """Convert empty strings to None."""
    return None if value == "" else value


def parse_int(value: str) -> int | None:
    """Convert a string to an integer."""
    if value == "":
        return None

    return int(value)


def parse_float(value: str) -> float | None:
    """Convert a string to a float."""
    if value == "":
        return None

    return float(value)


def parse_yyyymmdd(value: str) -> date | None:
    """Convert a YYYYMMDD string to a date."""
    if value == "":
        return None

    return datetime.strptime(value, "%Y%m%d").date()


def transform_sales_record(record: dict[str, str]) -> PropertySale:
        return PropertySale(
          record_type=record["record_type"],
          district_code=record["district_code"],
          property_id=record["property_id"],
          sale_counter=record["sale_counter"],
          download_datetime=record["download_datetime"],
          property_name=empty_string_to_none(record["property_name"]),
          property_unit_number=empty_string_to_none(record["property_unit_number"]),
          property_house_number=empty_string_to_none(record["property_house_number"]),
          property_street_name=empty_string_to_none(record["property_street_name"]),
          property_locality=empty_string_to_none(record["property_locality"]),
          property_postcode=empty_string_to_none(record["property_postcode"]),
          area=parse_float(record["area"]),
          area_type=empty_string_to_none(record["area_type"]),
          contract_date=parse_yyyymmdd(record["contract_date"]),
          settlement_date=parse_yyyymmdd(record["settlement_date"]),
          purchase_price=parse_int(record["purchase_price"]),
          zoning=empty_string_to_none(record["zoning"]),
          nature_of_property=empty_string_to_none(record["nature_of_property"]),
          primary_purpose=empty_string_to_none(record["primary_purpose"]),
          strata_lot_number=empty_string_to_none(record["strata_lot_number"]),
          component_code=empty_string_to_none(record["component_code"]),
          sale_code=empty_string_to_none(record["sale_code"]),
          percent_interest_of_sale=empty_string_to_none(
              record["percent_interest_of_sale"]
          ),
          dealing_number=empty_string_to_none(record["dealing_number"]),
      )