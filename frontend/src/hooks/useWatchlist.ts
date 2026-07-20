import { useEffect, useState } from "react";

const STORAGE_KEY = "australian-property-dashboard-watchlist";

function readWatchlist(): string[] {
  try {
    const value = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? "[]");
    return Array.isArray(value)
      ? value.filter((item): item is string => typeof item === "string").slice(0, 20)
      : [];
  } catch {
    return [];
  }
}

export function useWatchlist() {
  const [watchlist, setWatchlist] = useState<string[]>(readWatchlist);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(watchlist));
  }, [watchlist]);

  const toggleWatchlist = (locality: string) => {
    const normalised = locality.trim().toUpperCase();
    setWatchlist((current) =>
      current.includes(normalised)
        ? current.filter((item) => item !== normalised)
        : [...current, normalised].slice(-20),
    );
  };

  return {
    watchlist,
    toggleWatchlist,
    isSaved: (locality: string) => watchlist.includes(locality.trim().toUpperCase()),
  };
}
