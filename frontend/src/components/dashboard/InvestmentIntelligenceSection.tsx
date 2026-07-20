import { useWatchlist } from "../../hooks/useWatchlist";
import { DemandProfileSection } from "./DemandProfileSection";
import { InvestmentRankingsSection } from "./InvestmentRankingsSection";
import { InvestmentWatchlistSection } from "./InvestmentWatchlistSection";

export function InvestmentIntelligenceSection({ locality }: { locality: string }) {
  const { watchlist, toggleWatchlist, isSaved } = useWatchlist();

  return (
    <div className="mt-14 border-t border-slate-700 pt-10">
      <div className="mb-7">
        <p className="text-xs font-bold uppercase tracking-[0.18em] text-cyan-400">Milestone 3</p>
        <h2 className="mt-2 text-4xl font-semibold">Demand, ranking and research tools</h2>
        <p className="mt-3 max-w-3xl text-slate-400">Combine property prices, rental demand and ABS Census demographics in one explainable screening workflow.</p>
      </div>
      <DemandProfileSection locality={locality} saved={isSaved(locality)} onToggleWatchlist={toggleWatchlist} />
      <InvestmentRankingsSection isSaved={isSaved} onToggleWatchlist={toggleWatchlist} />
      <InvestmentWatchlistSection watchlist={watchlist} onToggleWatchlist={toggleWatchlist} />
    </div>
  );
}
