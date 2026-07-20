"""Import ABS Census demographics and build explainable investment scores."""

from __future__ import annotations

import csv
import hashlib
import io
import math
import tempfile
import zipfile
from pathlib import Path

import shapefile

from backend.database.connection import Database
from backend.services.analytics_service import MARKET_SALE_FILTER_SQL
from scripts.download.download_abs_demographics import FILES

SCORE_WEIGHTS = {
    "yield": 0.30,
    "price_growth": 0.20,
    "rent_growth": 0.15,
    "population_growth": 0.15,
    "income_growth": 0.10,
    "evidence": 0.10,
}

REFRESH_INVESTMENT_SCORES_SQL = f"""
TRUNCATE investment_scores;
WITH rental_latest AS (
    SELECT MAX(lodgement_date) AS as_of_date
    FROM rental_bond_lodgements
), postcode_rent AS (
    SELECT
        postcode,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY weekly_rent)
            FILTER (
                WHERE lodgement_date >
                    (SELECT as_of_date FROM rental_latest) - INTERVAL '3 months'
            ) AS current_median,
        COUNT(*) FILTER (
            WHERE lodgement_date >
                (SELECT as_of_date FROM rental_latest) - INTERVAL '3 months'
        ) AS current_count,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY weekly_rent)
            FILTER (
                WHERE lodgement_date >
                    (SELECT as_of_date FROM rental_latest) - INTERVAL '15 months'
                  AND lodgement_date <=
                    (SELECT as_of_date FROM rental_latest) - INTERVAL '12 months'
            ) AS previous_median,
        COUNT(*) FILTER (
            WHERE lodgement_date >
                (SELECT as_of_date FROM rental_latest) - INTERVAL '15 months'
              AND lodgement_date <=
                (SELECT as_of_date FROM rental_latest) - INTERVAL '12 months'
        ) AS previous_count
    FROM rental_bond_lodgements
    WHERE weekly_rent BETWEEN 50 AND 5000
      AND dwelling_type IN ('F', 'H', 'T')
      AND lodgement_date >
          (SELECT as_of_date FROM rental_latest) - INTERVAL '15 months'
    GROUP BY postcode
), suburb_rent AS (
    SELECT
        mapping.locality,
        SUM(rent.current_median * rent.current_count)
            / NULLIF(SUM(rent.current_count), 0) AS median_weekly_rent,
        SUM(rent.current_count)::int AS rental_count,
        SUM(rent.previous_median * rent.previous_count)
            / NULLIF(SUM(rent.previous_count), 0) AS previous_weekly_rent
    FROM postcode_rent rent
    JOIN suburb_postcodes mapping ON mapping.postcode = rent.postcode
    WHERE rent.current_median IS NOT NULL
      AND rent.previous_median IS NOT NULL
    GROUP BY mapping.locality
), sale_latest AS (
    SELECT MAX(contract_date) AS as_of_date
    FROM property_sales
    WHERE {MARKET_SALE_FILTER_SQL}
      AND nature_of_property = 'R'
), suburb_sales AS (
    SELECT
        UPPER(TRIM(property_locality)) AS locality,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY purchase_price)
            FILTER (
                WHERE contract_date >
                    (SELECT as_of_date FROM sale_latest) - INTERVAL '12 months'
            ) AS current_median,
        COUNT(*) FILTER (
            WHERE contract_date >
                (SELECT as_of_date FROM sale_latest) - INTERVAL '12 months'
        )::int AS sales_count,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY purchase_price)
            FILTER (
                WHERE contract_date >
                    (SELECT as_of_date FROM sale_latest) - INTERVAL '72 months'
                  AND contract_date <=
                    (SELECT as_of_date FROM sale_latest) - INTERVAL '60 months'
            ) AS historic_median
    FROM property_sales
    WHERE {MARKET_SALE_FILTER_SQL}
      AND nature_of_property = 'R'
      AND contract_date >
          (SELECT as_of_date FROM sale_latest) - INTERVAL '72 months'
    GROUP BY UPPER(TRIM(property_locality))
), demographic_postcodes AS (
    SELECT
        postcode,
        MAX(population) FILTER (WHERE census_year = 2016) AS population_2016,
        MAX(population) FILTER (WHERE census_year = 2021) AS population_2021,
        MAX(median_household_income_weekly)
            FILTER (WHERE census_year = 2016) AS income_2016,
        MAX(median_household_income_weekly)
            FILTER (WHERE census_year = 2021) AS income_2021
    FROM postcode_demographics
    GROUP BY postcode
), suburb_demographics AS (
    SELECT
        mapping.locality,
        ARRAY_AGG(DISTINCT mapping.postcode ORDER BY mapping.postcode) AS postcodes,
        SUM(demo.population_2016)::int AS population_2016,
        SUM(demo.population_2021)::int AS population_2021,
        SUM(demo.income_2016 * demo.population_2016)
            / NULLIF(SUM(demo.population_2016), 0) AS income_2016,
        SUM(demo.income_2021 * demo.population_2021)
            / NULLIF(SUM(demo.population_2021), 0) AS income_2021,
        SUM(geo.latitude * mapping.supporting_sales)
            / NULLIF(SUM(mapping.supporting_sales), 0) AS latitude,
        SUM(geo.longitude * mapping.supporting_sales)
            / NULLIF(SUM(mapping.supporting_sales), 0) AS longitude
    FROM suburb_postcodes mapping
    JOIN demographic_postcodes demo ON demo.postcode = mapping.postcode
    JOIN postcode_geography geo ON geo.postcode = mapping.postcode
    WHERE demo.population_2016 > 0
      AND demo.population_2021 > 0
      AND demo.income_2016 > 0
      AND demo.income_2021 > 0
    GROUP BY mapping.locality
), raw_metrics AS (
    SELECT
        sales.locality,
        demographics.postcodes,
        demographics.latitude,
        demographics.longitude,
        rent.median_weekly_rent,
        (rent.median_weekly_rent / rent.previous_weekly_rent - 1) * 100
            AS rent_growth_1y_pct,
        rent.rental_count,
        sales.current_median AS median_sale_price,
        (POWER(sales.current_median / sales.historic_median, 1.0 / 5) - 1) * 100
            AS price_growth_5y_annualised_pct,
        sales.sales_count,
        rent.median_weekly_rent * 52 / sales.current_median * 100
            AS gross_yield_pct,
        demographics.population_2021,
        (demographics.population_2021::double precision
            / demographics.population_2016 - 1) * 100 AS population_growth_5y_pct,
        demographics.income_2021 AS median_household_income_weekly,
        (demographics.income_2021::double precision
            / demographics.income_2016 - 1) * 100 AS income_growth_5y_pct,
        LEAST(rent.rental_count / 100.0, 1.0) * 50
            + LEAST(sales.sales_count / 100.0, 1.0) * 50 AS evidence_score
    FROM suburb_sales sales
    JOIN suburb_rent rent ON rent.locality = sales.locality
    JOIN suburb_demographics demographics
        ON demographics.locality = sales.locality
    WHERE sales.current_median > 0
      AND sales.historic_median > 0
      AND sales.sales_count >= 20
      AND rent.median_weekly_rent > 0
      AND rent.previous_weekly_rent > 0
      AND rent.rental_count >= 30
      AND demographics.population_2021 >= 500
), component_scores AS (
    SELECT
        raw_metrics.*,
        PERCENT_RANK() OVER (ORDER BY gross_yield_pct) * 100 AS yield_score,
        PERCENT_RANK() OVER (ORDER BY price_growth_5y_annualised_pct) * 100
            AS price_growth_score,
        PERCENT_RANK() OVER (ORDER BY rent_growth_1y_pct) * 100
            AS rent_growth_score,
        PERCENT_RANK() OVER (ORDER BY population_growth_5y_pct) * 100
            AS population_growth_score,
        PERCENT_RANK() OVER (ORDER BY income_growth_5y_pct) * 100
            AS income_growth_score
    FROM raw_metrics
    WHERE gross_yield_pct BETWEEN 0.5 AND 20
      AND price_growth_5y_annualised_pct BETWEEN -30 AND 60
      AND rent_growth_1y_pct BETWEEN -50 AND 100
      AND population_growth_5y_pct BETWEEN -75 AND 250
      AND income_growth_5y_pct BETWEEN -25 AND 250
)
INSERT INTO investment_scores (
    locality,
    postcodes,
    latitude,
    longitude,
    median_weekly_rent,
    rent_growth_1y_pct,
    rental_count,
    median_sale_price,
    price_growth_5y_annualised_pct,
    sales_count,
    gross_yield_pct,
    population_2021,
    population_growth_5y_pct,
    median_household_income_weekly,
    income_growth_5y_pct,
    yield_score,
    price_growth_score,
    rent_growth_score,
    population_growth_score,
    income_growth_score,
    evidence_score,
    investment_score,
    confidence,
    rental_data_as_of,
    sales_data_as_of,
    demographic_data_as_of
)
SELECT
    locality,
    postcodes,
    latitude,
    longitude,
    median_weekly_rent,
    rent_growth_1y_pct,
    rental_count,
    median_sale_price,
    price_growth_5y_annualised_pct,
    sales_count,
    gross_yield_pct,
    population_2021,
    population_growth_5y_pct,
    median_household_income_weekly,
    income_growth_5y_pct,
    yield_score,
    price_growth_score,
    rent_growth_score,
    population_growth_score,
    income_growth_score,
    evidence_score,
    yield_score * {SCORE_WEIGHTS["yield"]}
        + price_growth_score * {SCORE_WEIGHTS["price_growth"]}
        + rent_growth_score * {SCORE_WEIGHTS["rent_growth"]}
        + population_growth_score * {SCORE_WEIGHTS["population_growth"]}
        + income_growth_score * {SCORE_WEIGHTS["income_growth"]}
        + evidence_score * {SCORE_WEIGHTS["evidence"]} AS investment_score,
    CASE
        WHEN rental_count >= 100 AND sales_count >= 50 THEN 'high'
        ELSE 'medium'
    END AS confidence,
    (SELECT as_of_date FROM rental_latest),
    (SELECT as_of_date FROM sale_latest),
    2021
FROM component_scores;
"""


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _normalise_postcode(value: str | None) -> str | None:
    if not value:
        return None
    postcode = value.strip().upper().removeprefix("POA")
    return postcode if len(postcode) == 4 and postcode.isdigit() else None


def _normalise_int(value: str | None, *, positive: bool = False) -> int | None:
    try:
        number = int(float(str(value).strip()))
    except (TypeError, ValueError):
        return None
    if positive and number <= 0:
        return None
    return number


def _find_member(archive: zipfile.ZipFile, suffix: str) -> str:
    matches = [name for name in archive.namelist() if name.endswith(suffix)]
    if len(matches) != 1:
        raise ValueError(f"Expected one {suffix} file, found {len(matches)}")
    return matches[0]


def read_census_demographics(path: Path, year: int) -> list[tuple]:
    """Read population and income columns from one ABS GCP DataPack."""
    with zipfile.ZipFile(path) as archive:
        population_member = _find_member(archive, f"{year}Census_G01_NSW_POA.csv")
        income_member = _find_member(archive, f"{year}Census_G02_NSW_POA.csv")

        with archive.open(population_member) as raw:
            population_reader = csv.DictReader(
                io.TextIOWrapper(raw, encoding="utf-8-sig", newline="")
            )
            populations = {
                postcode: _normalise_int(row.get("Tot_P_P"))
                for row in population_reader
                if (postcode := _normalise_postcode(row.get(f"POA_CODE_{year}")))
            }

        with archive.open(income_member) as raw:
            income_reader = csv.DictReader(
                io.TextIOWrapper(raw, encoding="utf-8-sig", newline="")
            )
            incomes = {
                postcode: (
                    _normalise_int(
                        row.get("Median_tot_prsnl_inc_weekly"), positive=True
                    ),
                    _normalise_int(row.get("Median_tot_hhd_inc_weekly"), positive=True),
                )
                for row in income_reader
                if (postcode := _normalise_postcode(row.get(f"POA_CODE_{year}")))
            }

    return [
        (postcode, year, population, *incomes.get(postcode, (None, None)))
        for postcode, population in populations.items()
        if population is not None and postcode in incomes
    ]


def _ring_centroid(points: list[tuple[float, float]]) -> tuple[float, float, float]:
    area_twice = 0.0
    x_sum = 0.0
    y_sum = 0.0
    for index, (x1, y1) in enumerate(points):
        x2, y2 = points[(index + 1) % len(points)]
        cross = x1 * y2 - x2 * y1
        area_twice += cross
        x_sum += (x1 + x2) * cross
        y_sum += (y1 + y2) * cross
    if math.isclose(area_twice, 0.0):
        xs, ys = zip(*points, strict=True)
        return (sum(xs) / len(xs), sum(ys) / len(ys), 0.0)
    return (
        x_sum / (3 * area_twice),
        y_sum / (3 * area_twice),
        abs(area_twice),
    )


def _shape_centroid(shape) -> tuple[float, float]:
    boundaries = [*shape.parts, len(shape.points)]
    rings = [
        shape.points[start:end]
        for start, end in zip(boundaries[:-1], boundaries[1:], strict=True)
        if end - start >= 3
    ]
    if not rings:
        xmin, ymin, xmax, ymax = shape.bbox
        return ((xmin + xmax) / 2, (ymin + ymax) / 2)
    centroids = [_ring_centroid(ring) for ring in rings]
    longitude, latitude, _ = max(centroids, key=lambda item: item[2])
    return longitude, latitude


def read_postcode_geography(path: Path, allowed_postcodes: set[str]) -> list[tuple]:
    """Read representative Postal Area points from the ABS shapefile."""
    with tempfile.TemporaryDirectory(prefix="abs-poa-") as temporary:
        with zipfile.ZipFile(path) as archive:
            archive.extractall(temporary)
        shape_path = next(Path(temporary).glob("*.shp"))
        reader = shapefile.Reader(str(shape_path))
        results = []
        for shape_record in reader.iterShapeRecords():
            record = shape_record.record.as_dict()
            postcode = _normalise_postcode(str(record.get("POA_CODE21", "")))
            if postcode not in allowed_postcodes:
                continue
            longitude, latitude = _shape_centroid(shape_record.shape)
            if not (140 <= longitude <= 154 and -38.5 <= latitude <= -27.5):
                continue
            results.append(
                (
                    postcode,
                    latitude,
                    longitude,
                    float(record["AREASQKM21"])
                    if record.get("AREASQKM21") is not None
                    else None,
                )
            )
        reader.close()
    return results


def load_abs_demographics(db: Database, directory: Path) -> tuple[int, int]:
    """Atomically replace derived Census and geography tables."""
    census_rows = []
    import_rows = []
    for year in (2016, 2021):
        filename = f"{year}_GCP_POA_for_NSW_short-header.zip"
        path = directory / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing ABS DataPack: {path}")
        rows = read_census_demographics(path, year)
        census_rows.extend(rows)
        import_rows.append((filename, FILES[filename], _sha256(path), year, len(rows)))

    boundary_filename = "POA_2021_AUST_GDA2020_SHP.zip"
    boundary_path = directory / boundary_filename
    if not boundary_path.exists():
        raise FileNotFoundError(f"Missing ABS boundary file: {boundary_path}")
    postcodes_2021 = {row[0] for row in census_rows if row[1] == 2021}
    geography_rows = read_postcode_geography(boundary_path, postcodes_2021)
    import_rows.append(
        (
            boundary_filename,
            FILES[boundary_filename],
            _sha256(boundary_path),
            None,
            len(geography_rows),
        )
    )

    with db.connection() as conn:
        existing = {
            row[0]: row[1]
            for row in conn.execute(
                "SELECT source_file, sha256 FROM abs_demographic_imports"
            ).fetchall()
        }
        for source_file, _, checksum, _, _ in import_rows:
            if source_file in existing and existing[source_file] != checksum:
                raise ValueError(f"ABS source changed since import: {source_file}")

        conn.execute("TRUNCATE investment_scores")
        conn.execute("TRUNCATE postcode_demographics")
        conn.execute("TRUNCATE postcode_geography")
        with conn.cursor() as cursor:
            cursor.executemany(
                """
                INSERT INTO postcode_demographics (
                    postcode, census_year, population,
                    median_personal_income_weekly,
                    median_household_income_weekly
                ) VALUES (%s, %s, %s, %s, %s)
                """,
                census_rows,
            )
            cursor.executemany(
                """
                INSERT INTO postcode_geography (
                    postcode, latitude, longitude, area_sq_km
                ) VALUES (%s, %s, %s, %s)
                """,
                geography_rows,
            )
            cursor.executemany(
                """
                INSERT INTO abs_demographic_imports (
                    source_file, source_url, sha256, census_year, row_count
                ) VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (source_file) DO UPDATE SET
                    source_url = EXCLUDED.source_url,
                    census_year = EXCLUDED.census_year,
                    row_count = EXCLUDED.row_count,
                    imported_at = NOW()
                """,
                import_rows,
            )
        conn.commit()
    return len(census_rows), len(geography_rows)


def refresh_investment_scores(db: Database) -> int:
    with db.connection() as conn:
        conn.execute(REFRESH_INVESTMENT_SCORES_SQL)
        count = conn.execute("SELECT COUNT(*) FROM investment_scores").fetchone()[0]
        conn.commit()
    return count
