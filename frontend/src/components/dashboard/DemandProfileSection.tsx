/* eslint-disable react-hooks/set-state-in-effect -- effect resets remote request state */
import { useEffect, useState } from "react";
import { Download, Star, StarOff, UsersRound, WalletCards } from "lucide-react";

import {
  getDemographicProfile,
  getInvestmentProfile,
} from "../../api/investment";
import { formatCurrency, formatPercent } from "../../lib/formatters";
import { downloadSuburbReport } from "../../lib/investmentReports";
import type {
  DemographicProfile,
  InvestmentScore,
} from "../../types/investment";
import { InvestmentScoreBreakdown } from "./InvestmentScoreBreakdown";

interface Props {
  locality: string;
  saved: boolean;
  onToggleWatchlist: (locality: string) => void;
}

export function DemandProfileSection({ locality, saved, onToggleWatchlist }: Props) {
  const [demographics, setDemographics] = useState<DemographicProfile | null>(null);
  const [score, setScore] = useState<InvestmentScore | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    if (locality.trim().length < 2) {
      setDemographics(null);
      setScore(null);
      return;
    }
    setLoading(true);
    setError(null);
    Promise.allSettled([
      getDemographicProfile(locality),
      getInvestmentProfile(locality),
    ]).then(([demographicResult, scoreResult]) => {
      if (!active) return;
      const demographicValue = demographicResult.status === "fulfilled" ? demographicResult.value : null;
      const scoreValue = scoreResult.status === "fulfilled" ? scoreResult.value : null;
      setDemographics(demographicValue);
      setScore(scoreValue);
      if (!demographicValue) setError("No mapped ABS Census data was found for this exact locality.");
      setLoading(false);
    });
    return () => { active = false; };
  }, [locality]);

  if (locality.trim().length < 2) {
    return (
      <section className="rounded-xl border border-cyan-500/25 bg-cyan-950/10 p-8 text-center">
        <h2 className="text-2xl font-semibold">Demand and investment score</h2>
        <p className="mt-2 text-slate-400">Search an exact NSW locality to add population, household income and an explainable investment score.</p>
      </section>
    );
  }
  if (loading) return <div className="h-[32rem] animate-pulse rounded-xl border border-slate-700 bg-slate-900" />;
  if (error || !demographics) {
    return <p className="rounded-xl border border-amber-500/30 bg-amber-950/20 p-6 text-amber-100">{error}</p>;
  }

  return (
    <section className="rounded-xl border border-cyan-500/25 bg-slate-900 p-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.16em] text-cyan-400">Demand signals</p>
          <h2 className="mt-1 text-3xl font-semibold">{demographics.locality} investment profile</h2>
          <p className="mt-2 text-sm text-slate-400">
            ABS Postal Area{demographics.postcodes.length === 1 ? "" : "s"} {demographics.postcodes.join(", ")} · Census 2016–2021
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <button type="button" onClick={() => onToggleWatchlist(demographics.locality)} className="inline-flex items-center gap-2 rounded-lg border border-slate-600 px-4 py-2 text-sm font-semibold hover:border-cyan-400">
            {saved ? <StarOff className="h-4 w-4" /> : <Star className="h-4 w-4" />}
            {saved ? "Remove from watchlist" : "Save to watchlist"}
          </button>
          <button type="button" onClick={() => downloadSuburbReport(demographics.locality, demographics, score)} className="inline-flex items-center gap-2 rounded-lg bg-cyan-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-cyan-400">
            <Download className="h-4 w-4" /> Download report
          </button>
        </div>
      </div>

      <div className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-5">
        <article className="rounded-lg border border-slate-700 bg-slate-950/55 p-5 xl:col-span-1">
          <p className="text-sm text-slate-400">Investment score</p>
          <p className="mt-2 text-4xl font-semibold text-cyan-300">{score ? score.investment_score.toFixed(1) : "N/A"}</p>
          <p className="mt-1 text-xs text-slate-500">Relative score out of 100</p>
        </article>
        <article className="rounded-lg border border-slate-700 bg-slate-950/55 p-5">
          <UsersRound className="h-5 w-5 text-cyan-400" />
          <p className="mt-4 text-sm text-slate-400">Population 2021</p>
          <p className="mt-1 text-2xl font-semibold">{demographics.population_2021.toLocaleString()}</p>
        </article>
        <article className="rounded-lg border border-slate-700 bg-slate-950/55 p-5">
          <p className="text-sm text-slate-400">Population growth</p>
          <p className="mt-4 text-2xl font-semibold text-emerald-400">{formatPercent(demographics.population_growth_5y_pct)}</p>
          <p className="mt-1 text-xs text-slate-500">2016–2021 total</p>
        </article>
        <article className="rounded-lg border border-slate-700 bg-slate-950/55 p-5">
          <WalletCards className="h-5 w-5 text-violet-400" />
          <p className="mt-4 text-sm text-slate-400">Household income</p>
          <p className="mt-1 text-2xl font-semibold">{formatCurrency(demographics.median_household_income_2021)}/wk</p>
        </article>
        <article className="rounded-lg border border-slate-700 bg-slate-950/55 p-5">
          <p className="text-sm text-slate-400">Income growth</p>
          <p className="mt-4 text-2xl font-semibold text-emerald-400">{formatPercent(demographics.income_growth_5y_pct)}</p>
          <p className="mt-1 text-xs text-slate-500">Nominal, 2016–2021</p>
        </article>
      </div>

      {score ? (
        <div className="mt-6">
          <h3 className="mb-3 text-lg font-semibold">Why this score?</h3>
          <InvestmentScoreBreakdown components={score.components} />
        </div>
      ) : (
        <p className="mt-6 rounded-lg border border-amber-500/25 bg-amber-950/20 p-4 text-sm text-amber-100">
          Demographics are available, but this locality does not meet the minimum sales, rental and five-year history requirements for a score.
        </p>
      )}
      <p className="mt-4 text-xs text-slate-500">Population and income describe the mapped ABS Postal Area, not an exact suburb boundary. The score is a transparent screening aid, not a forecast or recommendation.</p>
    </section>
  );
}
