# Demand and Investment Score Methodology

## ABS demographic inputs

Milestone 3 uses Australian Bureau of Statistics 2016 and 2021 Census General
Community Profile DataPacks for NSW Postal Areas. Population is read from table
`G01` (`Tot_P_P`). Median weekly personal and household income are read from
table `G02`; the dashboard uses median weekly household income for demand and
scoring.

- DataPacks: https://www.abs.gov.au/census/find-census-data/datapacks
- Postal Area definition: https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs/edition-3-july-2021-june-2026/non-abs-structures/postal-areas
- Digital boundaries: https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs/edition-3-july-2021-june-2026/access-and-downloads/digital-boundary-files

Imports are repeatable and checksum-validated. The raw ZIP files remain in the
gitignored `data/raw/abs_demographics` directory.

## Geographic mapping

ABS Postal Areas approximate postcode boundaries; they are not legal postcode
or suburb boundaries. Each property-sales locality is joined to its observed
postcode through `suburb_postcodes`. A postcode can map to multiple localities,
so localities sharing a postcode can display identical demographic, rental and
map values. Where a locality maps to multiple postcodes:

- population is summed;
- median household income is population-weighted; and
- the map point is weighted by supporting property-sale records.

The 2016 and 2021 Postal Area classifications are separate Census geographies.
Growth uses matching four-digit codes and should be treated as indicative where
boundaries changed. Census counts are also perturbed by the ABS for privacy.

## Growth metrics

- **Population growth:** `(population 2021 / population 2016 - 1) × 100`.
- **Annualised population growth:** the five-year compound annual growth rate.
- **Household income growth:** `(median weekly household income 2021 /
  median weekly household income 2016 - 1) × 100`.
- **Income growth is nominal:** it is not adjusted for inflation.

## Explainable investment score

The score is a relative screening score from 0 to 100. It is not a forecast of
capital growth or total return. Eligible localities require at least 30 recent
rental-bond lodgements, 20 recent residential sales, comparable rent data one
year earlier, five-year sale history, Census data and a map point.

Each market and demand metric is converted to its percentile rank across all
eligible NSW localities. The final score is the weighted sum:

| Component | Weight | Raw metric |
|---|---:|---|
| Gross rental yield | 30% | Recent median rent × 52 ÷ recent median price |
| Price growth | 20% | Five-year annualised residential price growth |
| Rent growth | 15% | Recent three-month median vs equivalent prior-year window |
| Population growth | 15% | ABS Census 2016 to 2021 growth |
| Household income growth | 10% | Nominal ABS Census 2016 to 2021 growth |
| Evidence strength | 10% | Rental and sales samples, capped at 100 each |

Every API result returns the raw value, percentile score, weight, contribution
and explanation for all six components. Component contributions sum to the
displayed investment score.

## Map, watchlists and exports

Map points are representative points calculated from the largest polygon in the
official ABS 2021 Postal Area boundary file. The base map uses OpenStreetMap
tiles. Watchlists are stored only in browser `localStorage`; there is no account
or server-side personal-data storage. Suburb, ranking and watchlist reports are
downloaded as CSV files containing the visible metrics and methodological notes.

## Limitations

The score does not include vacancy, expenses, property condition, zoning,
planning constraints, infrastructure delivery risk, financing, tax or an
investor's individual circumstances. It must be used as a shortlist generator,
followed by property-level due diligence. It is general information, not
financial advice.
