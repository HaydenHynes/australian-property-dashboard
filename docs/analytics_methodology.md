# Sales Analytics Methodology

## Purpose

The investment dashboard separates raw NSW Valuer General records from a
conservative set of transactions used for market analytics. Raw source rows are
never deleted or modified by these rules.

## Valid market-sale rule

A transaction is included in headline metrics, trends and comparable sales when:

- purchase price is between $50,000 and $20,000,000;
- contract date is present, between 1 January 2001 and today;
- locality is present;
- `sale_code` is blank;
- percentage interest is blank, `0`, or `100` (treated as full interest); and
- it matches the selected nature-of-property filter.

The price bounds are conservative analytical guardrails, not assertions that
transactions outside them are invalid. Coded and partial-interest transactions
remain in `property_sales` and are counted as excluded in dashboard summaries.

## Metrics

- **Median sale price:** middle purchase price among included transactions.
- **Annual growth:** median of the latest trailing 12 months compared with the
  preceding 12 months.
- **Three- and five-year growth:** compound annual growth rate between the latest
  trailing 12-month median and equivalent 12-month windows three or five years
  earlier.
- **Sales volume:** number of included transactions.
- **Quarterly trend:** quarterly median and volume; quarters with fewer than five
  included transactions are omitted to reduce unstable points.
- **Data as of:** latest included contract date for the selected filters.

## Property classifications

The source defines `R` as residence, `V` as vacant and `3` as other. These do not
provide a reliable house-versus-unit classification. Until a documented mapping
using strata and primary-purpose fields is implemented, the dashboard must not
label `R` records as houses.

## Limitations

- The rules are deliberately conservative and require further validation against
  official sale-code definitions.
- Median prices do not control for changes in the mix or quality of properties sold.
- Recent periods may be incomplete due to reporting delays.
- Historical growth is descriptive and is not a forecast.
- Dashboard information is general analysis, not financial advice.
