/* eslint-disable react-hooks/set-state-in-effect -- effect resets remote request state */
import { useEffect, useState } from "react";
import { Download, StarOff } from "lucide-react";

import { compareInvestments } from "../../api/investment";
import { formatCurrency, formatPercent } from "../../lib/formatters";
import { downloadRankingReport } from "../../lib/investmentReports";
import type { InvestmentScore } from "../../types/investment";

interface Props {
  watchlist: string[];
  onToggleWatchlist: (locality: string) => void;
}

export function InvestmentWatchlistSection({ watchlist, onToggleWatchlist }: Props) {
  const [results, setResults] = useState<InvestmentScore[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let active = true;
    if (watchlist.length === 0) {
      setResults([]);
      return;
    }
    setLoading(true);
    compareInvestments(watchlist)
      .then((data) => active && setResults(data))
      .catch(() => active && setResults([]))
      .finally(() => active && setLoading(false));
    return () => { active = false; };
  }, [watchlist]);

  return (
    <section className="mt-10 rounded-xl border border-violet-500/25 bg-slate-900 p-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.16em] text-violet-400">Saved locally</p>
          <h2 className="mt-1 text-2xl font-semibold">Investment watchlist</h2>
          <p className="mt-2 text-sm text-slate-400">Saved in this browser only. No account or personal data is sent to the server.</p>
        </div>
        <button type="button" disabled={results.length === 0} onClick={() => downloadRankingReport("property-investment-watchlist.csv", results)} className="inline-flex items-center justify-center gap-2 rounded-lg border border-slate-600 px-4 py-2 text-sm font-semibold hover:border-violet-400 disabled:opacity-40"><Download className="h-4 w-4" /> Download watchlist</button>
      </div>

      {watchlist.length === 0 ? (
        <p className="mt-5 rounded-lg border border-dashed border-slate-700 p-6 text-center text-slate-400">Save a locality from its profile or the ranking table to start your watchlist.</p>
      ) : loading ? (
        <div className="mt-5 h-36 animate-pulse rounded-lg bg-slate-800" />
      ) : (
        <div className="mt-5 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {watchlist.map((locality) => {
            const item = results.find((result) => result.locality === locality);
            return (
              <article key={locality} className="rounded-lg border border-slate-700 bg-slate-950/55 p-5">
                <div className="flex items-start justify-between gap-4">
                  <div><h3 className="font-semibold">{locality}</h3><p className="mt-1 text-xs text-slate-500">{item?.postcodes.join(", ") ?? "Score not available"}</p></div>
                  <button type="button" onClick={() => onToggleWatchlist(locality)} className="rounded-md border border-slate-600 p-2 hover:border-red-400" aria-label={`Remove ${locality} from watchlist`}><StarOff className="h-4 w-4" /></button>
                </div>
                {item && <div className="mt-5 grid grid-cols-3 gap-3 text-sm"><div><p className="text-slate-500">Score</p><p className="mt-1 font-semibold text-cyan-300">{item.investment_score.toFixed(1)}</p></div><div><p className="text-slate-500">Price</p><p className="mt-1 font-semibold">{formatCurrency(item.median_sale_price)}</p></div><div><p className="text-slate-500">Yield</p><p className="mt-1 font-semibold text-emerald-400">{formatPercent(item.gross_yield_pct)}</p></div></div>}
              </article>
            );
          })}
        </div>
      )}
    </section>
  );
}
