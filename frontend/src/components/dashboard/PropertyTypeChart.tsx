import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import type { PropertyTypeSales } from "../../types/property";

interface PropertyTypeChartProps {
  data: PropertyTypeSales[];
}

const COLORS = ["#38bdf8", "#22c55e", "#f59e0b"];

function getPropertyTypeLabel(type: string | null): string {
  if (type === "R") return "Residence";
  if (type === "V") return "Vacant";
  if (type === "3") return "Other";

  return "Unknown";
}

export function PropertyTypeChart({ data }: PropertyTypeChartProps) {
  const chartData = data.map((item) => ({
    ...item,
    label: getPropertyTypeLabel(item.property_type),
  }));

  return (
    <section className="mt-10 rounded-xl border border-slate-700 bg-slate-900 p-6">
      <h2 className="mb-6 text-2xl font-semibold">Property Type Distribution</h2>

      <div className="h-80 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={chartData}
              dataKey="sales_count"
              nameKey="label"
              cx="50%"
              cy="50%"
              outerRadius={110}
              label
            >
              {chartData.map((entry, index) => (
                <Cell
                  key={entry.property_type ?? "unknown"}
                  fill={COLORS[index % COLORS.length]}
                />
              ))}
            </Pie>

            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-4 flex flex-wrap gap-4">
        {chartData.map((item, index) => (
          <div key={item.property_type ?? "unknown"} className="flex items-center gap-2">
            <span
              className="h-3 w-3 rounded-full"
              style={{ backgroundColor: COLORS[index % COLORS.length] }}
            />
            <span className="text-sm text-slate-300">
              {item.label}: {item.sales_count}
            </span>
          </div>
        ))}
      </div>
    </section>
  );
}