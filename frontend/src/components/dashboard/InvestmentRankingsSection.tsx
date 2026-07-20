/* eslint-disable react-hooks/exhaustive-deps, react-hooks/set-state-in-effect -- initial ranking request runs once */
import { useEffect, useState } from "react";
import { Download, MapPinned, Star, StarOff } from "lucide-react";

import { getInvestmentRankings } from "../../api/investment";
import { formatCurrency, formatPercent } from "../../lib/formatters";
import { downloadRankingReport } from "../../lib/investmentReports";
import type { InvestmentScore, RankingSort } from "../../types/investment";
import { InvestmentMap } from "./InvestmentMap";

interface Props {
  isSaved: (locality: string) => boolean;
  onToggleWatchlist: (locality: string) => void;
}

export function InvestmentRankingsSection({ isSaved, onToggleWatchlist }: Props) {
  const [maxPrice, setMaxPrice] = useState(1_000_000);
  const [minYield, setMinYield] = useState(3);
  const [minScore, setMinScore] = useState(50);
  const [search, setSearch] = useState("");
  const [sort, setSort] = useState<RankingSort>("score");
  const [results, setResults] = useState<InvestmentScore[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const runRanking = async () => {
    setLoading(true);
    setError(null);
    try {
      setResults(await getInvestmentRankings({
        maxPrice,
        minYield,
        minScore,
        search,
        sort,
        limit: 150,
      }));
    } catch {
      setError("Investment rankings could not be loaded.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { void runRanking(); }, []);

  return (
    <section className="mt-10 rounded-xl border border-slate-700 bg-slate-900 p-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.16em] text-emerald-400">Rank and map</p>
          <h2 className="mt-1 text-3xl font-semibold">NSW investment opportunity explorer</h2>
          <p className="mt-2 max-w-3xl text-sm text-slate-400">Filter eligible localities, inspect their score on the map and download the visible ranking as an auditable CSV report.</p>
        </div>
        <button type="button" disabled={results.length === 0} onClick={() => downloadRankingReport("nsw-investment-ranking.csv", results)} className="inline-flex items-center justify-center gap-2 rounded-lg border border-slate-600 px-4 py-2 text-sm font-semibold hover:border-emerald-400 disabled:opacity-40">
          <Download className="h-4 w-4" /> Download ranking
        </button>
      </div>

      <div className="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-6">
        <label className="text-sm text-slate-300">Maximum price<input type="number" min={100000} step={50000} value={maxPrice} onChange={(event) => setMaxPrice(Number(event.target.value))} className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2" /></label>
        <label className="text-sm text-slate-300">Minimum yield %<input type="number" min={0} max={20} step={0.25} value={minYield} onChange={(event) => setMinYield(Number(event.target.value))} className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2" /></label>
        <label className="text-sm text-slate-300">Minimum score<input type="number" min={0} max={100} step={5} value={minScore} onChange={(event) => setMinScore(Number(event.target.value))} className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2" /></label>
        <label className="text-sm text-slate-300">Search locality<input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="e.g. Dubbo" className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2" /></label>
        <label className="text-sm text-slate-300">Rank by<select value={sort} onChange={(event) => setSort(event.target.value as RankingSort)} className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2"><option value="score">Overall score</option><option value="yield">Gross yield</option><option value="price_growth">Price growth</option><option value="rent_growth">Rent growth</option><option value="population_growth">Population growth</option><option value="income_growth">Income growth</option></select></label>
        <button type="button" onClick={runRanking} disabled={loading} className="mt-auto rounded-lg bg-emerald-500 px-5 py-2 font-semibold text-slate-950 transition hover:bg-emerald-400 disabled:opacity-50">{loading ? "Ranking…" : "Update ranking"}</button>
      </div>

      {error && <p className="mt-4 rounded-lg border border-red-500/30 bg-red-950/20 p-4 text-red-200">{error}</p>}
      {!error && !loading && results.length === 0 && <p className="mt-4 rounded-lg border border-amber-500/25 bg-amber-950/20 p-4 text-amber-100">No eligible localities match these filters.</p>}

      {results.length > 0 && (
        <>
          <div className="mt-7 flex items-center gap-2 text-sm text-slate-400"><MapPinned className="h-4 w-4 text-emerald-400" /> {results.length} eligible localities shown · green markers score 75+</div>
          <div className="mt-3"><InvestmentMap results={results} /></div>
          <div className="mt-6 overflow-x-auto rounded-lg border border-slate-700">
            <table className="w-full min-w-[1120px]">
              <thead className="bg-slate-800 text-left text-xs uppercase tracking-wide text-slate-300">
                <tr>{["Rank", "Locality", "Score", "Median price", "Gross yield", "Price growth", "Rent growth", "Population growth", "Income growth", "Evidence", "Watchlist"].map((label) => <th key={label} className="p-3">{label}</th>)}</tr>
              </thead>
              <tbody>
                {results.map((item, index) => (
                  <tr key={item.locality} className="border-t border-slate-700 hover:bg-slate-800/40">
                    <td className="p-3 text-slate-400">{index + 1}</td>
                    <td className="p-3 font-semibold">{item.locality}<span className="block text-xs font-normal text-slate-500">{item.postcodes.join(", ")}</span></td>
                    <td className="p-3"><span className="rounded-full bg-cyan-500/15 px-3 py-1 font-bold text-cyan-300">{item.investment_score.toFixed(1)}</span></td>
                    <td className="p-3">{formatCurrency(item.median_sale_price)}</td>
                    <td className="p-3 font-semibold text-emerald-400">{formatPercent(item.gross_yield_pct)}</td>
                    <td className="p-3">{formatPercent(item.price_growth_5y_annualised_pct)} p.a.</td>
                    <td className="p-3">{formatPercent(item.rent_growth_1y_pct)}</td>
                    <td className="p-3">{formatPercent(item.population_growth_5y_pct)}</td>
                    <td className="p-3">{formatPercent(item.income_growth_5y_pct)}</td>
                    <td className="p-3 text-sm text-slate-300">{item.rental_count.toLocaleString()} rents<br />{item.sales_count.toLocaleString()} sales</td>
                    <td className="p-3"><button type="button" onClick={() => onToggleWatchlist(item.locality)} className="rounded-md border border-slate-600 p-2 hover:border-cyan-400" aria-label={`${isSaved(item.locality) ? "Remove" : "Add"} ${item.locality} ${isSaved(item.locality) ? "from" : "to"} watchlist`}>{isSaved(item.locality) ? <StarOff className="h-4 w-4" /> : <Star className="h-4 w-4" />}</button></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
      <p className="mt-4 text-xs text-slate-500">Scores are percentile-based across 1,050 eligible NSW localities and refresh when the score snapshot is rebuilt. High rank does not account for vacancy, expenses, planning risk, property condition or financing.</p>
    </section>
  );
}
