import { DollarSign, Home, MapPin } from "lucide-react";

import { formatCurrency } from "../../lib/formatters";
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
        {[1, 2, 3].map((item) => (
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
        caption="Loaded property sale records"
        icon={Home}
      />

      <SummaryCard
        title="Highest Sale"
        value={formatCurrency(summary.highest_sale_price)}
        caption="Highest purchase price"
        icon={DollarSign}
      />

      <SummaryCard
        title="Localities"
        value={summary.locality_count.toLocaleString()}
        caption="Distinct NSW localities"
        icon={MapPin}
      />
    </section>
  );
}