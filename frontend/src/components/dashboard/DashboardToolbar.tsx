interface DashboardToolbarProps {
  searchTerm: string;
  onSearchTermChange: (value: string) => void;
  topSalesLimit: number;
  onTopSalesLimitChange: (value: number) => void;
  propertyType: string;
  onPropertyTypeChange: (value: string) => void;
  contractYear: string;
  onContractYearChange: (value: string) => void;
  availableYears: number[];
  onClear: () => void;
}

export function DashboardToolbar({
  searchTerm,
  onSearchTermChange,
  topSalesLimit,
  onTopSalesLimitChange,
  propertyType,
  onPropertyTypeChange,
  contractYear,
  onContractYearChange,
  availableYears,
  onClear,
}: DashboardToolbarProps) {
  return (
    <section className="mt-8 flex flex-col gap-4 rounded-xl border border-slate-700 bg-slate-900 p-4 md:flex-row md:items-center md:justify-between">
      <div>
        <label className="mb-2 block text-sm font-medium text-slate-300">
          Search locality
        </label>
        <input
          value={searchTerm}
          onChange={(event) => onSearchTermChange(event.target.value)}
          placeholder="e.g. Sydney"
          className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-2 text-slate-100 outline-none focus:border-sky-400 md:w-72"
        />
      </div>

      <div>
        <label className="mb-2 block text-sm font-medium text-slate-300">
          Top sales shown
        </label>
        <select
          value={topSalesLimit}
          onChange={(event) => onTopSalesLimitChange(Number(event.target.value))}
          className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-2 text-slate-100 outline-none focus:border-sky-400 md:w-40"
        >
          <option value={5}>Top 5</option>
          <option value={10}>Top 10</option>
          <option value={20}>Top 20</option>
        </select>
      </div>
      <div>
        <label className="mb-2 block text-sm font-medium text-slate-300">
          Property type
        </label>
        <select
          value={propertyType}
          onChange={(event) => onPropertyTypeChange(event.target.value)}
          className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-2 text-slate-100 outline-none focus:border-sky-400 md:w-44"
        >
          <option value="">All</option>
          <option value="R">Residence</option>
          <option value="V">Vacant</option>
          <option value="3">Other</option>
        </select>
      </div>
      <div>
        <label className="mb-2 block text-sm font-medium text-slate-300">
          Contract year
        </label>
        <select
          value={contractYear}
          onChange={(event) => onContractYearChange(event.target.value)}
          className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-2 text-slate-100 outline-none focus:border-sky-400 md:w-36"
        >
          <option value="">All</option>
          {availableYears.map((year) => (
            <option key={year} value={year}>{year}</option>
          ))}
        </select>
      </div>
      <button
        type="button"
        onClick={onClear}
        className="mt-auto rounded-lg border border-slate-600 px-4 py-2 font-medium text-slate-200 transition hover:border-sky-400 hover:text-white"
      >
        Clear filters
      </button>
    </section>
  );
}
