# Australian Property Investment Dashboard

## System Overview

The application consists of five major components.

```
                Data Sources
                     │
                     ▼
          Data Collection Pipeline
                     │
                     ▼
             Data Cleaning (Python)
                     │
                     ▼
          PostgreSQL Database
                     │
                     ▼
           FastAPI Backend API
                     │
                     ▼
        Streamlit Analytics Dashboard
```

---

## Component 1

### Data Sources

Responsible for collecting verified Australian property market data.

Examples:

- NSW Property Sales
- ABS
- CoreLogic (future)
- SQM Research (future)
- RBA
- Census Data

---

## Component 2

### Data Pipeline

Python scripts that

- download data
- clean data
- validate data
- transform data
- prepare data for storage

---

## Component 3

### Database

Stores

- suburbs
- sales
- rental information
- demographics
- investment scores

---

## Component 4

### API

Provides data to the dashboard.

Example endpoints

/api/suburbs

/api/sales

/api/investment-score

---

## Component 5

### Dashboard

Displays

- charts
- maps
- rankings
- suburb comparisons
- investment analysis