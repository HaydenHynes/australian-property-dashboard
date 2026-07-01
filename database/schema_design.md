# Database Schema Design

## Planned Tables

### suburbs

Stores one record for every suburb.

Fields:

- suburb_id
- suburb_name
- postcode
- state
- latitude
- longitude

---

### property_sales

Stores every historical sale.

Fields:

- sale_id
- suburb_id
- property_type
- bedrooms
- bathrooms
- car_spaces
- land_size
- sale_price
- sale_date

---

### rental_market

Stores rental statistics.

Fields:

- suburb_id
- median_rent
- rental_yield
- vacancy_rate

---

### demographics

Stores ABS information.

Fields:

- suburb_id
- population
- median_income
- unemployment_rate
- median_age

---

### infrastructure

Stores planned infrastructure projects.

Fields:

- project_id
- suburb_id
- project_name
- completion_year