import type { TopSale } from "../../types/property";

interface TopSalesTableProps {
  sales: TopSale[];
}

export function TopSalesTable({ sales }: TopSalesTableProps) {
  return (
    <section className="mt-10">
      <h2 className="mb-4 text-2xl font-semibold">
        Top Property Sales
      </h2>

      <div className="overflow-hidden rounded-xl border border-slate-700">
        <table className="w-full border-collapse">
          <thead className="bg-slate-800">
            <tr>
              <th className="p-4 text-left">Locality</th>
              <th className="p-4 text-left">Address</th>
              <th className="p-4 text-right">Sale Price</th>
              <th className="p-4 text-left">Contract Date</th>
            </tr>
          </thead>

          <tbody>
            {sales.map((sale) => (
              <tr
                key={`${sale.locality}-${sale.street_name}-${sale.house_number}`}
                className="border-t border-slate-700"
              >
                <td className="p-4">{sale.locality}</td>

                <td className="p-4">
                  {sale.house_number} {sale.street_name}
                </td>

                <td className="p-4 text-right">
                  ${sale.purchase_price?.toLocaleString()}
                </td>

                <td className="p-4">
                  {sale.contract_date}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}