import { CalendarDays, ChartNoAxesCombined, CircleDollarSign, Gauge } from "lucide-react";

import { formatCurrency, formatDate, formatPercent } from "../../lib/formatters";
import type { SuburbProfile } from "../../types/property";

interface SuburbProfileSectionProps {
  profile: SuburbProfile | null;
  loading: boolean;
  hasSearch: boolean;
}

export function SuburbProfileSection({ profile, loading, hasSearch }: SuburbProfileSectionProps) {
  if (!hasSearch) return null;
  if (loading) return <div className="mt-8 h-56 animate-pulse rounded-xl border border-slate-700 bg-slate-900" />;
  if (!profile || profile.sales_count_12m === 0) {
    return (
      <section className="mt-8 rounded-xl border border-amber-500/30 bg-amber-950/20 p-6">
        <h2 className="font-semibold text-amber-100">No exact suburb profile found</h2>
        <p className="mt-1 text-sm text-amber-200/70">Enter a complete NSW locality name, such as Newcastle or Parramatta.</p>
      </section>
    );
  }

  const metrics = [
    { label: "Median price", value: formatCurrency(profile.median_sale_price), icon: CircleDollarSign },
    { label: "Sales (12 months)", value: profile.sales_count_12m.toLocaleString(), icon: Gauge },
    { label: "1-year growth", value: formatPercent(profile.growth_1y_pct), icon: ChartNoAxesCombined },
    { label: "3-year annualised", value: formatPercent(profile.growth_3y_annualised_pct), icon: ChartNoAxesCombined },
    { label: "5-year annualised", value: formatPercent(profile.growth_5y_annualised_pct), icon: ChartNoAxesCombined },
    { label: "Data through", value: formatDate(profile.data_as_of), icon: CalendarDays },
  ];

  return (
    <section className="mt-8 rounded-xl border border-sky-500/30 bg-gradient-to-br from-sky-950/40 to-slate-900 p-6">
      <p className="text-xs font-bold uppercase tracking-[0.16em] text-sky-400">Suburb profile</p>
      <h2 className="mt-1 text-3xl font-semibold">{profile.locality}</h2>
      <p className="mt-2 text-sm text-slate-400">Trailing-period residential market metrics based on valid full-interest sales.</p>
      <div className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-6">
        {metrics.map(({ label, value, icon: Icon }) => (
          <div key={label} className="rounded-lg border border-slate-700/70 bg-slate-950/55 p-4">
            <Icon className="h-5 w-5 text-sky-400" />
            <p className="mt-4 text-sm text-slate-400">{label}</p>
            <p className="mt-1 text-xl font-semibold text-slate-100">{value}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
