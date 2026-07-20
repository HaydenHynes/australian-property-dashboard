# Data Sources

## Confirmed Sources

| Data | Source | Status |
|------|--------|--------|
| Property Sales | NSW Valuer General | ✅ |
| Rental Bond Lodgements | NSW Fair Trading | ✅ |
| Population and Household Income | ABS Census DataPacks | ✅ |
| Interest Rates | RBA | ⏳ |
| Inflation | ABS | ⏳ |
| Infrastructure | TBD | ⏳ |
| Vacancy Rates | TBD | ⏳ |

---

## Notes

This document records every dataset used by the project.

Only verified and trustworthy data sources will be used.

### Rental bond lodgements

- Official page: https://www.nsw.gov.au/housing-and-construction/rental-forms-surveys-and-data/rental-bond-data
- Coverage imported: January 2021 to June 2026
- Geography: postcode
- Fields used: lodgement date, postcode, dwelling type, bedrooms and weekly rent
- Important limitation: values are supplied by agents or landlords at lodgement.

### ABS Census demographics

- DataPacks: https://www.abs.gov.au/census/find-census-data/datapacks
- Coverage imported: 2016 and 2021 Census General Community Profiles
- Geography: NSW Postal Areas, mapped to property-sales locality/postcode pairs
- Fields used: total population, median weekly personal income and median weekly
  household income
- Map source: official ABS 2021 Postal Area GDA2020 shapefile
- Important limitation: Postal Areas approximate postcodes and are not exact
  suburb boundaries; income growth is nominal.
