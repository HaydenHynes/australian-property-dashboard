"""
Transform parsed NSW property sales records into typed values.
"""

from datetime import date, datetime


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


def transform_sales_record(record: dict[str, str]) -> dict[str, object]:
    """Transform a raw parsed sales record into typed values."""
    transformed_record = {
        key: empty_string_to_none(value)
        for key, value in record.items()
    }

    transformed_record["purchase_price"] = parse_int(record["purchase_price"])
    transformed_record["area"] = parse_float(record["area"])
    transformed_record["contract_date"] = parse_yyyymmdd(record["contract_date"])
    transformed_record["settlement_date"] = parse_yyyymmdd(record["settlement_date"])

    return transformed_record