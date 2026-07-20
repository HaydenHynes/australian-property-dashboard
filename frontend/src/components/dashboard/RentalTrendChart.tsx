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

import type { RentalTrendPoint } from "../../types/rental";

export function RentalTrendChart({ data }: { data: RentalTrendPoint[] }) {
  const chartData = data.map((item) => ({
    ...item,
    label: new Intl.DateTimeFormat("en-AU", {
      month: "short",
      year: "2-digit",
      timeZone: "UTC",
    }).format(new Date(item.month)),
  }));
  return (
    <div className="h-80">
      <ResponsiveContainer width="100%" height="100%">
        <ComposedChart data={chartData} margin={{ top: 12, right: 24, bottom: 22, left: 10 }}>
          <CartesianGrid stroke="#334155" strokeDasharray="3 3" />
          <XAxis dataKey="label" stroke="#94a3b8" minTickGap={28} />
          <YAxis yAxisId="rent" stroke="#22c55e" tickFormatter={(value: number) => `$${value}`} />
          <YAxis yAxisId="count" orientation="right" stroke="#a78bfa" allowDecimals={false} />
          <Tooltip contentStyle={{ background: "#0f172a", borderColor: "#475569", borderRadius: 10 }} />
          <Bar yAxisId="count" dataKey="lodgement_count" name="Lodgements" fill="#8b5cf6" opacity={0.28} />
          <Line yAxisId="rent" dataKey="median_weekly_rent" name="Median weekly rent" stroke="#22c55e" strokeWidth={3} dot={false} />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}
