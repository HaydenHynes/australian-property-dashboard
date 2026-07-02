import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { SalesByLocality } from "../../types/property";

interface SalesByLocalityChartProps {
  data: SalesByLocality[];
}

export function SalesByLocalityChart({ data }: SalesByLocalityChartProps) {
  return (
    <section className="mt-10 rounded-xl border border-slate-700 bg-slate-900 p-6">
      <h2 className="mb-6 text-2xl font-semibold">Sales by Locality</h2>

      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{
              top: 20,
              right: 30,
              left: 30,
              bottom: 60,
            }}
          >
            <CartesianGrid stroke="#334155" strokeDasharray="3 3" />

            <XAxis
              dataKey="locality"
              stroke="#94a3b8"
              interval={0}
              angle={-35}
              textAnchor="end"
              height={80}
              padding={{ left: 25, right: 25 }}
            />

            <YAxis allowDecimals={false} stroke="#94a3b8" />

            <Tooltip />

            <Bar
              dataKey="sales_count"
              fill="#38bdf8"
              radius={[8, 8, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}