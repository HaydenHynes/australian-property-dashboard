import { ChartNoAxesCombined, CircleDollarSign, Home, MapPin } from "lucide-react";

import { formatCurrency, formatDate, formatPercent } from "../../lib/formatters";
import type { DashboardSummary } from "../../types/dashboard";
import { SummaryCard } from "./SummaryCard";

interface SummarySectionProps {
  summary: DashboardSummary | null;
  loading: boolean;
}

export function SummarySection({ summary, loading }: SummarySectionProps) {
  if (loading || !summary) {
    return (
      <section className="summary-grid">
        {[1, 2, 3, 4].map((item) => (
          <div
            key={item}
            className="h-36 animate-pulse rounded-xl border border-slate-700 bg-slate-900"
          />
        ))}
      </section>
    );
  }

  return (
    <section className="summary-grid">
      <SummaryCard
        title="Total Sales"
        value={summary.total_sales.toLocaleString()}
        caption={`${summary.excluded_sales.toLocaleString()} non-market records excluded`}
        icon={Home}
      />

      <SummaryCard
        title="Median Sale Price"
        value={formatCurrency(summary.median_sale_price)}
        caption="Less affected by extreme transactions"
        icon={CircleDollarSign}
      />

      <SummaryCard
        title="Annual Growth"
        value={formatPercent(summary.annual_growth_pct)}
        caption="Latest trailing 12 months versus prior year"
        icon={ChartNoAxesCombined}
      />

      <SummaryCard
        title="Localities"
        value={summary.locality_count.toLocaleString()}
        caption={`Data through ${formatDate(summary.data_as_of)}`}
        icon={MapPin}
      />
    </section>
  );
}
