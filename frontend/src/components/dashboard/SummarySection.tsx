import { DollarSign, Home, MapPin } from "lucide-react";

import { formatCurrency } from "../../lib/formatters";
import type { DashboardSummary } from "../../types/dashboard";
import { SummaryCard } from "./SummaryCard";

interface SummarySectionProps {
  summary: DashboardSummary;
}

export function SummarySection({ summary }: SummarySectionProps) {
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