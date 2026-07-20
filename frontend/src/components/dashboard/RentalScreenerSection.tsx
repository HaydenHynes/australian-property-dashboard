import { useState } from "react";

import { screenRentals } from "../../api/rental";
import { formatCurrency, formatPercent } from "../../lib/formatters";
import type { RentalScreenResult } from "../../types/rental";

export function RentalScreenerSection() {
  const [maxPrice, setMaxPrice] = useState(1_000_000);
  const [minYield, setMinYield] = useState(4);
  const [minSamples, setMinSamples] = useState(30);
  const [dwellingType, setDwellingType] = useState("");
  const [results, setResults] = useState<RentalScreenResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const runScreen = async () => {
    setLoading(true);
    setError(null);
    try {
      setResults(await screenRentals({ maxPrice, minYield, minRentalCount: minSamples, dwellingType }));
    } catch {
      setError("The rental screener could not be loaded.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="mt-10 rounded-xl border border-slate-700 bg-slate-900 p-6">
      <p className="text-xs font-bold uppercase tracking-[0.16em] text-amber-400">Discover</p>
      <h2 className="mt-1 text-2xl font-semibold">Rental yield screener</h2>
      <p className="mt-2 text-sm text-slate-400">Screen localities by entry price, gross yield and minimum rental evidence.</p>
      <div className="mt-5 grid gap-4 md:grid-cols-2 xl:grid-cols-5">
        <label className="text-sm text-slate-300">Maximum price<input type="number" min={100000} step={50000} value={maxPrice} onChange={(event) => setMaxPrice(Number(event.target.value))} className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2" /></label>
        <label className="text-sm text-slate-300">Minimum yield %<input type="number" min={0} max={20} step={0.25} value={minYield} onChange={(event) => setMinYield(Number(event.target.value))} className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2" /></label>
        <label className="text-sm text-slate-300">Minimum rental samples<input type="number" min={5} step={5} value={minSamples} onChange={(event) => setMinSamples(Number(event.target.value))} className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2" /></label>
        <label className="text-sm text-slate-300">Rental type<select value={dwellingType} onChange={(event) => setDwellingType(event.target.value)} className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2"><option value="">All residential</option><option value="F">Flat / unit</option><option value="H">House</option><option value="T">Terrace / townhouse</option></select></label>
        <button type="button" onClick={runScreen} disabled={loading} className="mt-auto rounded-lg bg-amber-500 px-5 py-2 font-semibold text-slate-950 transition hover:bg-amber-400 disabled:opacity-50">{loading ? "Screening…" : "Run screener"}</button>
      </div>
      {error && <p className="mt-3 text-sm text-red-300">{error}</p>}
      {results.length > 0 && (
        <div className="mt-6 overflow-x-auto rounded-lg border border-slate-700">
          <table className="w-full min-w-[820px]">
            <thead className="bg-slate-800 text-left text-xs uppercase tracking-wide text-slate-300"><tr>{["Rank", "Locality", "Median rent", "Median price", "Gross yield", "Rental samples", "Sales", "Confidence"].map((label) => <th key={label} className="p-3">{label}</th>)}</tr></thead>
            <tbody>{results.map((item, index) => <tr key={item.locality} className="border-t border-slate-700"><td className="p-3 text-slate-400">{index + 1}</td><td className="p-3 font-semibold">{item.locality}<span className="block text-xs font-normal text-slate-500">{item.postcodes.join(", ")}</span></td><td className="p-3">{formatCurrency(item.median_weekly_rent)}/wk</td><td className="p-3">{formatCurrency(item.median_sale_price)}</td><td className="p-3 font-semibold text-emerald-400">{formatPercent(item.gross_yield_pct)}</td><td className="p-3">{item.rental_count.toLocaleString()}</td><td className="p-3">{item.sales_count.toLocaleString()}</td><td className="p-3 capitalize">{item.confidence}</td></tr>)}</tbody>
          </table>
        </div>
      )}
      <p className="mt-4 text-xs text-slate-500">Screening is indicative: rental statistics are postcode-based and may be shared by multiple localities. Gross yield excludes all ownership costs.</p>
    </section>
  );
}
