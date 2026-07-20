# Australian Property Investment Dashboard

## Overview

The Australian Property Investment Dashboard is an end-to-end data analytics platform designed to help analyse the Australian property market using verified public data.

## Investor analytics

The dashboard uses a documented, non-destructive market-sale filter and provides:

- median sale prices and annual growth;
- quarterly median-price and sales-volume trends;
- exact suburb profiles with 1-, 3-, and 5-year growth;
- recent comparable transactions;
- transparent exclusion counts and data coverage dates.

See [Sales Analytics Methodology](docs/analytics_methodology.md) for definitions,
quality rules and limitations.

## Rental investment analysis

Milestone 2 adds official NSW rental-bond analytics:

- three-month median weekly rent and interquartile range;
- annual rent growth and gross rental yield;
- postcode-to-locality mapping with visible confidence counts;
- 36-month rent and lodgement trends;
- two-to-four suburb comparison; and
- an adjustable price/yield/sample screener.

To download and load the rental source history:

```bash
python -m scripts.download.download_rental_bonds
python -m scripts.database.create_tables
python -m scripts.database.load_rental_bonds
```

Imports are idempotent. Source workbooks are kept under the gitignored
`data/raw/rental_bonds` directory. See
[Rental Investment Methodology](docs/rental_methodology.md) for calculations and
limitations.

## Demand and investment ranking

Milestone 3 adds official ABS Census demographics and research tools:

- 2016–2021 population and nominal household-income growth;
- an explainable six-component investment score;
- an interactive NSW opportunity map and ranking filters;
- browser-local saved watchlists; and
- downloadable suburb, ranking and watchlist CSV reports.

To download and load the ABS inputs and refresh scores:

```bash
python -m scripts.download.download_abs_demographics
python -m scripts.database.create_tables
python -m scripts.database.load_abs_demographics
```

After later sales or rental imports, rebuild scores with:

```bash
python -m scripts.database.refresh_investment_scores
```

See [Demand and Investment Score Methodology](docs/investment_score_methodology.md)
for score weights, eligibility rules, source definitions and geographic caveats.

## Author

Hayden Hynes
