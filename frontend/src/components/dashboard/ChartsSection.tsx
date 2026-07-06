import type { PropertyTypeSales, SalesByLocality } from "../../types/property";
import { PropertyTypeChart } from "./PropertyTypeChart";
import { SalesByLocalityChart } from "./SalesByLocalityChart";

interface ChartsSectionProps {
  salesByLocality: SalesByLocality[];
  propertyTypeSales: PropertyTypeSales[];
}

export function ChartsSection({
  salesByLocality,
  propertyTypeSales,
}: ChartsSectionProps) {
  return (
    <section className="grid gap-6 lg:grid-cols-2">
      <SalesByLocalityChart data={salesByLocality} />
      <PropertyTypeChart data={propertyTypeSales} />
    </section>
  );
}