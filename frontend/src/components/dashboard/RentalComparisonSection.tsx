import { useState } from "react";

import { compareRentals } from "../../api/rental";
import { formatCurrency, formatPercent } from "../../lib/formatters";
import type { RentalProfile } from "../../types/rental";

export function RentalComparisonSection() {
  const [input, setInput] = useState("Newcastle, Parramatta");
  const [results, setResults] = useState<RentalProfile[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const compare = async () => {
    const localities = input.split(",").map((item) => item.trim()).filter(Boolean).slice(0, 4);
    if (localities.length < 2) {
      setError("Enter between two and four comma-separated localities.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      setResults(await compareRentals(localities));
    } catch {
      setError("The comparison could not be loaded. Check the locality names.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="mt-10 rounded-xl border border-slate-700 bg-slate-900 p-6">
      <p className="text-xs font-bold uppercase tracking-[0.16em] text-violet-400">Compare</p>
      <h2 className="mt-1 text-2xl font-semibold">Rental suburb comparison</h2>
      <p className="mt-2 text-sm text-slate-400">Compare two to four exact locality names using the same three-month rental window.</p>
      <div className="mt-5 flex flex-col gap-3 sm:flex-row">
        <input value={input} onChange={(event) => setInput(event.target.value)} className="min-w-0 flex-1 rounded-lg border border-slate-700 bg-slate-950 px-4 py-2 text-slate-100" placeholder="Newcastle, Parramatta" />
        <button type="button" onClick={compare} disabled={loading} className="rounded-lg bg-violet-500 px-5 py-2 font-semibold text-white transition hover:bg-violet-400 disabled:opacity-50">
          {loading ? "Comparing…" : "Compare suburbs"}
        </button>
      </div>
      {error && <p className="mt-3 text-sm text-red-300">{error}</p>}
      {results.length > 0 && (
        <div className="mt-6 overflow-x-auto rounded-lg border border-slate-700">
          <table className="w-full min-w-[760px]">
            <thead className="bg-slate-800 text-left text-xs uppercase tracking-wide text-slate-300">
              <tr>{["Locality", "Median rent", "Median price", "Gross yield", "Rent growth", "Samples", "Confidence"].map((label) => <th key={label} className="p-3">{label}</th>)}</tr>
            </thead>
            <tbody>
              {results.map((item) => (
                <tr key={item.locality} className="border-t border-slate-700">
                  <td className="p-3 font-semibold">{item.locality}<span className="block text-xs font-normal text-slate-500">{item.postcodes.join(", ")}</span></td>
                  <td className="p-3">{formatCurrency(item.median_weekly_rent)}/wk</td>
                  <td className="p-3">{formatCurrency(item.median_sale_price)}</td>
                  <td className="p-3 font-semibold text-emerald-400">{formatPercent(item.gross_yield_pct)}</td>
                  <td className="p-3">{formatPercent(item.rent_growth_1y_pct)}</td>
                  <td className="p-3">{item.lodgement_count.toLocaleString()}</td>
                  <td className="p-3 capitalize">{item.confidence}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
