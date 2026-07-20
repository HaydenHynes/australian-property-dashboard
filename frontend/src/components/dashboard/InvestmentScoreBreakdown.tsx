import type { ScoreComponent } from "../../types/investment";

function componentValue(component: ScoreComponent) {
  return component.key === "evidence"
    ? `${component.raw_value.toFixed(0)}/100 evidence`
    : `${component.raw_value > 0 ? "+" : ""}${component.raw_value.toFixed(1)}%`;
}

export function InvestmentScoreBreakdown({
  components,
}: {
  components: ScoreComponent[];
}) {
  return (
    <div className="grid gap-3 lg:grid-cols-2">
      {components.map((component) => (
        <article key={component.key} className="rounded-lg border border-slate-700 bg-slate-950/55 p-4">
          <div className="flex items-start justify-between gap-4">
            <div>
              <p className="font-semibold text-slate-100">{component.label}</p>
              <p className="mt-1 text-xs text-slate-500">{component.explanation}</p>
            </div>
            <p className="shrink-0 text-right text-sm text-slate-300">
              {component.weight_pct.toFixed(0)}% weight
            </p>
          </div>
          <div className="mt-4 h-2 overflow-hidden rounded-full bg-slate-800">
            <div
              className="h-full rounded-full bg-gradient-to-r from-cyan-500 to-emerald-400"
              style={{ width: `${Math.min(Math.max(component.percentile_score, 0), 100)}%` }}
            />
          </div>
          <div className="mt-2 flex justify-between text-xs text-slate-400">
            <span>{componentValue(component)}</span>
            <span>
              {component.percentile_score.toFixed(0)}th percentile · {component.contribution.toFixed(1)} pts
            </span>
          </div>
        </article>
      ))}
    </div>
  );
}
