/* eslint-disable react-hooks/set-state-in-effect -- effect resets remote request state */
import { useEffect, useState } from "react";
import { BadgeDollarSign, ChartNoAxesCombined, CircleGauge, ReceiptText } from "lucide-react";

import { getRentalProfile, getRentalTrend } from "../../api/rental";
import { formatCurrency, formatPercent } from "../../lib/formatters";
import type { RentalProfile, RentalTrendPoint } from "../../types/rental";
import { RentalFilters } from "./RentalFilters";
import { RentalTrendChart } from "./RentalTrendChart";

export function RentalAnalysisSection({ locality }: { locality: string }) {
  const [dwellingType, setDwellingType] = useState("");
  const [bedrooms, setBedrooms] = useState("");
  const [profile, setProfile] = useState<RentalProfile | null>(null);
  const [trend, setTrend] = useState<RentalTrendPoint[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    if (locality.trim().length < 2) return;
    setLoading(true);
    setError(null);
    Promise.all([
      getRentalProfile(locality, { dwellingType, bedrooms }),
      getRentalTrend(locality, { dwellingType, bedrooms }),
    ])
      .then(([profileData, trendData]) => {
        if (!active) return;
        setProfile(profileData);
        setTrend(trendData);
      })
      .catch(() => active && setError("Rental data could not be loaded for this locality."))
      .finally(() => active && setLoading(false));
    return () => { active = false; };
  }, [locality, dwellingType, bedrooms]);

  if (locality.trim().length < 2) {
    return (
      <section className="mt-10 rounded-xl border border-emerald-500/25 bg-emerald-950/10 p-8 text-center">
        <h2 className="text-2xl font-semibold">Rental investment analysis</h2>
        <p className="mt-2 text-slate-400">Search an exact NSW locality to view median rent, gross yield and rental trends.</p>
      </section>
    );
  }
  if (loading) return <div className="mt-10 h-[34rem] animate-pulse rounded-xl border border-slate-700 bg-slate-900" />;
  if (error || !profile || profile.median_weekly_rent === null) {
    return <p className="mt-10 rounded-xl border border-amber-500/30 bg-amber-950/20 p-6 text-amber-100">{error ?? "No mapped rental data was found for this exact locality."}</p>;
  }

  const cards = [
    { label: "Median weekly rent", value: formatCurrency(profile.median_weekly_rent), icon: ReceiptText },
    { label: "Gross rental yield", value: formatPercent(profile.gross_yield_pct), icon: BadgeDollarSign },
    { label: "Annual rent growth", value: formatPercent(profile.rent_growth_1y_pct), icon: ChartNoAxesCombined },
    { label: "Recent lodgements", value: profile.lodgement_count.toLocaleString(), icon: CircleGauge },
  ];

  return (
    <section className="mt-10 rounded-xl border border-emerald-500/25 bg-slate-900 p-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.16em] text-emerald-400">Rental investment</p>
          <h2 className="mt-1 text-3xl font-semibold">{profile.locality} rental market</h2>
          <p className="mt-2 text-sm text-slate-400">Postcode{profile.postcodes.length === 1 ? "" : "s"} {profile.postcodes.join(", ")} · {profile.confidence} confidence</p>
        </div>
        <RentalFilters dwellingType={dwellingType} bedrooms={bedrooms} onDwellingTypeChange={setDwellingType} onBedroomsChange={setBedrooms} />
      </div>
      <div className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {cards.map(({ label, value, icon: Icon }) => (
          <div key={label} className="rounded-lg border border-slate-700 bg-slate-950/60 p-5">
            <Icon className="h-5 w-5 text-emerald-400" />
            <p className="mt-4 text-sm text-slate-400">{label}</p>
            <p className="mt-1 text-2xl font-semibold">{value}</p>
          </div>
        ))}
      </div>
      <div className="mt-6 rounded-lg border border-slate-700 bg-slate-950/35 p-4">
        <p className="mb-4 text-sm text-slate-400">Middle 50% rent range: {formatCurrency(profile.lower_quartile_rent)}–{formatCurrency(profile.upper_quartile_rent)}</p>
        <RentalTrendChart data={trend} />
      </div>
      <p className="mt-4 text-xs text-slate-500">Gross yield = median weekly rent × 52 ÷ median residential sale price. It excludes expenses and uses postcode rental data mapped to the locality.</p>
    </section>
  );
}
