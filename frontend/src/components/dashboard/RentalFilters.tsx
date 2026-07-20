interface RentalFiltersProps {
  dwellingType: string;
  bedrooms: string;
  onDwellingTypeChange: (value: string) => void;
  onBedroomsChange: (value: string) => void;
}

export function RentalFilters({
  dwellingType,
  bedrooms,
  onDwellingTypeChange,
  onBedroomsChange,
}: RentalFiltersProps) {
  return (
    <div className="flex flex-wrap gap-3">
      <select value={dwellingType} onChange={(event) => onDwellingTypeChange(event.target.value)} className="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100">
        <option value="">All residential rentals</option>
        <option value="F">Flat / unit</option>
        <option value="H">House</option>
        <option value="T">Terrace / townhouse</option>
      </select>
      <select value={bedrooms} onChange={(event) => onBedroomsChange(event.target.value)} className="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100">
        <option value="">All bedrooms</option>
        {[0, 1, 2, 3, 4, 5].map((bedroom) => <option key={bedroom} value={bedroom}>{bedroom === 0 ? "Studio / 0" : `${bedroom} bedroom${bedroom === 1 ? "" : "s"}`}</option>)}
      </select>
    </div>
  );
}
