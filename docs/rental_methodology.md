# Rental Investment Methodology

## Source and coverage

Rental inputs are NSW Fair Trading residential rental-bond lodgements from
January 2021 through June 2026. Annual workbooks are used for 2021-2025 and
monthly workbooks for 2026. The repeatable download manifest points to the
official NSW Government files.

Source: https://www.nsw.gov.au/housing-and-construction/rental-forms-surveys-and-data/rental-bond-data

Agents and landlords provide the dwelling type, bedroom count and weekly rent
when a bond is lodged. The data therefore describes newly lodged tenancies, not
every occupied or advertised rental property.

## Cleaning rules

- A valid row requires a lodgement date, four-digit postcode and numeric rent.
- Raw valid rents from $1 to $50,000 are preserved in `rental_bond_lodgements`.
- Investor analytics use weekly rents from $50 to $5,000.
- Dwelling types are Flat/unit (`F`), House (`H`), Terrace/townhouse/semi (`T`),
  Other (`O`) and Unknown (`U`). Investor metrics default to `F`, `H` and `T`.
- Unknown bedroom values are stored as null.
- Imports are idempotent and verified with a SHA-256 checksum per workbook.

## Postcode-to-locality mapping

Rental records identify postcode, not suburb. The `suburb_postcodes` mapping is
derived from the postcode/locality combinations present in NSW property sales.
One postcode can map to multiple localities. Consequently, localities sharing a
postcode may display the same rental statistics. This limitation is shown in the
dashboard and must not be hidden.

## Metrics

- **Median weekly rent:** median of valid lodgements in the latest three months.
- **Rent range:** 25th to 75th percentile in the same three-month period.
- **Annual rent growth:** latest three-month median versus the equivalent window
  one year earlier.
- **Gross rental yield:** median weekly rent multiplied by 52, divided by the
  trailing 12-month median residential sale price.
- **Confidence:** high for at least 30 lodgements, medium for 10-29 and low for
  fewer than 10.
- **Trend:** monthly median rent and lodgement count, with months below five
  observations omitted.

## Screening methodology

The screener combines recent postcode rent aggregates with trailing 12-month
locality sale medians. Where a locality maps to multiple postcodes, postcode
medians are weighted by lodgement count. Results are ordered by gross yield and
then rental sample size. Minimum rental and sales sample controls are applied.

Gross yield excludes vacancy, management fees, strata, maintenance, insurance,
rates, finance and tax. It is a screening metric, not a forecast or net return.
Information is general analysis and not financial advice.
