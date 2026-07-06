interface DashboardToolbarProps {
  searchTerm: string;
  onSearchTermChange: (value: string) => void;
  topSalesLimit: number;
  onTopSalesLimitChange: (value: number) => void;
}

export function DashboardToolbar({
  searchTerm,
  onSearchTermChange,
  topSalesLimit,
  onTopSalesLimitChange,
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
    </section>
  );
}