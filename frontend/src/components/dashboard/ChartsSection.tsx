import type { PropertyTypeSales, SalesByLocality } from "../../types/property";
import { PropertyTypeChart } from "./PropertyTypeChart";
import { SalesByLocalityChart } from "./SalesByLocalityChart";

interface ChartsSectionProps {
  salesByLocality: SalesByLocality[];
  propertyTypeSales: PropertyTypeSales[];
  loading: boolean;
}

export function ChartsSection({
  salesByLocality,
  propertyTypeSales,
  loading,
}: ChartsSectionProps) {
  if (loading) {
    return (
      <section className="grid gap-6 lg:grid-cols-2">
        <div className="h-96 animate-pulse rounded-xl border border-slate-700 bg-slate-900" />
        <div className="h-96 animate-pulse rounded-xl border border-slate-700 bg-slate-900" />
      </section>
    );
  }
  return (
    <section className="grid gap-6 lg:grid-cols-2">
      <SalesByLocalityChart data={salesByLocality} />
      <PropertyTypeChart data={propertyTypeSales} />
    </section>
  );
}