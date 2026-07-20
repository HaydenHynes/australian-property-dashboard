import {
  Bar,
  CartesianGrid,
  ComposedChart,
  Line,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { MarketTrendPoint } from "../../types/property";

interface MarketTrendChartProps {
  data: MarketTrendPoint[];
  loading: boolean;
}

export function MarketTrendChart({ data, loading }: MarketTrendChartProps) {
  if (loading) {
    return <div className="mt-8 h-96 animate-pulse rounded-xl border border-slate-700 bg-slate-900" />;
  }

  const chartData = data.map((item) => ({
    ...item,
    label: new Intl.DateTimeFormat("en-AU", {
      month: "short",
      year: "2-digit",
      timeZone: "UTC",
    }).format(new Date(item.period)),
  }));

  return (
    <section className="mt-8 rounded-xl border border-slate-700 bg-slate-900 p-6">
      <div className="mb-6">
        <p className="text-xs font-bold uppercase tracking-[0.16em] text-sky-400">Market trend</p>
        <h2 className="mt-1 text-2xl font-semibold">Quarterly median price and liquidity</h2>
        <p className="mt-1 text-sm text-slate-400">Bars show valid sales; the line shows median sale price.</p>
      </div>
      {chartData.length === 0 ? (
        <p className="py-24 text-center text-slate-400">No trend data matches these filters.</p>
      ) : (
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={chartData} margin={{ top: 10, right: 24, bottom: 25, left: 24 }}>
              <CartesianGrid stroke="#334155" strokeDasharray="3 3" />
              <XAxis dataKey="label" stroke="#94a3b8" minTickGap={28} />
              <YAxis
                yAxisId="price"
                stroke="#38bdf8"
                tickFormatter={(value: number) => `$${Math.round(value / 1000)}k`}
              />
              <YAxis yAxisId="sales" orientation="right" stroke="#a78bfa" allowDecimals={false} />
              <Tooltip
                contentStyle={{ backgroundColor: "#0f172a", borderColor: "#475569", borderRadius: 10 }}
              />
              <Bar yAxisId="sales" dataKey="sales_count" name="Valid sales" fill="#8b5cf6" opacity={0.35} />
              <Line
                yAxisId="price"
                type="monotone"
                dataKey="median_sale_price"
                name="Median price"
                stroke="#38bdf8"
                strokeWidth={3}
                dot={false}
              />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
      )}
    </section>
  );
}
