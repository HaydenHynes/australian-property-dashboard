import type { TopSale } from "../../types/property";
import { formatCurrency, formatDate } from "../../lib/formatters";

interface TopSalesTableProps {
  sales: TopSale[];
  loading: boolean;
}

export function TopSalesTable({ sales, loading }: TopSalesTableProps) {
  return (
    <section className="mt-10">
      <h2 className="mb-4 text-2xl font-semibold">
        Recent Comparable Sales
      </h2>
      {loading && (
        <div className="overflow-x-auto rounded-xl border border-slate-700">
          <div className="h-12 animate-pulse bg-slate-800" />
          {[1, 2, 3, 4, 5].map((item) => (
            <div
              key={item}
              className="h-14 animate-pulse border-t border-slate-700 bg-slate-900"
            />
          ))}
        </div>
      )}
      {!loading && sales.length === 0 && (
        <div className="rounded-xl border border-slate-700 bg-slate-900 p-8 text-center">
          <p className="text-lg font-semibold text-slate-100">No property sales found</p>
          <p className="mt-2 text-sm text-slate-400">
            Try adjusting the locality search, property type, or top results filter.
          </p>
        </div>
      )}
      {!loading && sales.length > 0 && (
        <div className="overflow-hidden rounded-xl border border-slate-700">
          <table className="w-full border-collapse">
            <thead className="bg-slate-800 text-slate-200">
              <tr>
                <th className="p-4 text-left font-semibold tracking-wide uppercase text-sm">Locality</th>
                <th className="p-4 text-left font-semibold tracking-wide uppercase text-sm">Address</th>
                <th className="p-4 text-left font-semibold tracking-wide uppercase text-sm">Sale Price</th>
                <th className="p-4 text-left font-semibold tracking-wide uppercase text-sm">Contract Date</th>
              </tr>
            </thead>

            <tbody>
              {sales.map((sale) => (
                <tr
                  key={`${sale.locality}-${sale.street_name}-${sale.house_number}-${sale.contract_date}`}
                  className="
                    border-t
                    border-slate-700
                    odd:bg-slate-900
                    even:bg-slate-950
                    hover:bg-sky-900/30
                    transition-colors
                  "
                >
                  <td className="p-4">{sale.locality}</td>

                  <td className="p-4">
                    {sale.house_number} {sale.street_name}
                  </td>

                  <td className="p-4 text-right">
                    {formatCurrency(sale.purchase_price)}
                  </td>

                  <td className="p-4">
                    {formatDate(sale.contract_date)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
