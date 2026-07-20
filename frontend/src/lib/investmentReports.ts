import type {
  DemographicProfile,
  InvestmentScore,
} from "../types/investment";

function escapeCsv(value: unknown): string {
  const text = value === null || value === undefined ? "" : String(value);
  return /[",\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function downloadCsv(filename: string, rows: unknown[][]) {
  const contents = rows.map((row) => row.map(escapeCsv).join(",")).join("\n");
  const blob = new Blob([`\uFEFF${contents}`], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}

export function downloadSuburbReport(
  locality: string,
  demographics: DemographicProfile | null,
  score: InvestmentScore | null,
) {
  const rows: unknown[][] = [
    ["Australian Property Dashboard - Suburb Investment Report"],
    ["Locality", locality.toUpperCase()],
    ["Generated", new Date().toISOString()],
    [],
    ["Metric", "Value", "Period / basis"],
  ];
  if (score) {
    rows.push(
      ["Investment score", score.investment_score, "Relative score out of 100"],
      ["Median sale price", score.median_sale_price, `12 months to ${score.sales_data_as_of}`],
      ["Gross rental yield %", score.gross_yield_pct, "Gross; excludes ownership costs"],
      ["Median weekly rent", score.median_weekly_rent, `3 months to ${score.rental_data_as_of}`],
      ["Rent growth %", score.rent_growth_1y_pct, "Equivalent three-month windows"],
      ["Price growth % p.a.", score.price_growth_5y_annualised_pct, "Five-year annualised"],
      ["Rental observations", score.rental_count, "Recent window"],
      ["Sales observations", score.sales_count, "Recent window"],
    );
  }
  if (demographics) {
    rows.push(
      ["Population 2016", demographics.population_2016, "ABS Census Postal Area"],
      ["Population 2021", demographics.population_2021, "ABS Census Postal Area"],
      ["Population growth %", demographics.population_growth_5y_pct, "2016 to 2021"],
      ["Median household income 2021", demographics.median_household_income_2021, "Weekly, nominal"],
      ["Household income growth %", demographics.income_growth_5y_pct, "2016 to 2021, nominal"],
    );
  }
  if (score) {
    rows.push([], ["Score component", "Raw value", "Percentile", "Weight %", "Contribution"]);
    score.components.forEach((component) => rows.push([
      component.label,
      component.raw_value,
      component.percentile_score,
      component.weight_pct,
      component.contribution,
    ]));
  }
  rows.push(
    [],
    ["Important", "Indicative screening analysis only; not financial advice."],
    ["Geography note", "Rental and Census data are postcode-level and may be shared by multiple localities."],
  );
  downloadCsv(`${locality.toLowerCase().replaceAll(" ", "-")}-investment-report.csv`, rows);
}

export function downloadRankingReport(
  filename: string,
  results: InvestmentScore[],
) {
  downloadCsv(filename, [
    [
      "Rank",
      "Locality",
      "Postcodes",
      "Investment score",
      "Median price",
      "Gross yield %",
      "Price growth % p.a.",
      "Rent growth %",
      "Population 2021",
      "Population growth %",
      "Household income / week",
      "Income growth %",
      "Rental samples",
      "Sales samples",
      "Confidence",
    ],
    ...results.map((item, index) => [
      index + 1,
      item.locality,
      item.postcodes.join(" "),
      item.investment_score,
      item.median_sale_price,
      item.gross_yield_pct,
      item.price_growth_5y_annualised_pct,
      item.rent_growth_1y_pct,
      item.population_2021,
      item.population_growth_5y_pct,
      item.median_household_income_weekly,
      item.income_growth_5y_pct,
      item.rental_count,
      item.sales_count,
      item.confidence,
    ]),
  ]);
}
