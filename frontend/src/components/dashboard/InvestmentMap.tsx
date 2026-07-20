import "leaflet/dist/leaflet.css";

import { CircleMarker, MapContainer, Popup, TileLayer } from "react-leaflet";

import { formatCurrency, formatPercent } from "../../lib/formatters";
import type { InvestmentScore } from "../../types/investment";

function scoreColour(score: number) {
  if (score >= 75) return "#34d399";
  if (score >= 60) return "#fbbf24";
  return "#38bdf8";
}

export function InvestmentMap({ results }: { results: InvestmentScore[] }) {
  return (
    <div className="h-[32rem] overflow-hidden rounded-xl border border-slate-700 bg-slate-950">
      <MapContainer
        center={[-32.4, 147.2]}
        zoom={6}
        scrollWheelZoom
        className="h-full w-full"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {results.map((item) => (
          <CircleMarker
            key={item.locality}
            center={[item.latitude, item.longitude]}
            radius={Math.max(5, Math.min(12, item.investment_score / 9))}
            pathOptions={{
              color: "#0f172a",
              fillColor: scoreColour(item.investment_score),
              fillOpacity: 0.82,
              weight: 1.5,
            }}
          >
            <Popup>
              <div className="min-w-48 text-slate-900">
                <strong>{item.locality}</strong>
                <div>Score: {item.investment_score.toFixed(1)}/100</div>
                <div>Price: {formatCurrency(item.median_sale_price)}</div>
                <div>Yield: {formatPercent(item.gross_yield_pct)}</div>
                <div>Population growth: {formatPercent(item.population_growth_5y_pct)}</div>
              </div>
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  );
}
