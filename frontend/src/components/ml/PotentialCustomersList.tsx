"use client";

import React, { useState, useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { getCustomersBySegment } from "@/lib/api";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Skeleton } from "@/components/ui/Skeleton";
import { Button } from "@/components/ui/Button";
import { formatEGP, formatNumber } from "@/lib/utils";
import {
  Users,
  AlertCircle,
  Database,
  MapPin,
  Search,
  Filter,
  ArrowUpDown,
  ChevronLeft,
  ChevronRight,
  RotateCcw,
} from "lucide-react";

interface PotentialCustomersListProps {
  clusterId: number;
  clusterName: string;
}

const CUSTOMER_TYPES = ["All", "Investor", "End User", "Business", "Landlord"];
const CUSTOMER_TIERS = ["All", "Platinum", "Gold", "Silver", "Bronze"];
const LOCATIONS = [
  "All",
  "New Cairo",
  "Sheikh Zayed",
  "New Capital",
  "Maadi",
  "Alexandria",
  "6th of October",
  "El Shorouk",
  "Nasr City",
  "Mansoura",
  "Obour",
];
const FREQUENCIES = ["All", "High", "Medium", "Low"];

const PAGE_SIZE = 25;

export function PotentialCustomersList({ clusterId, clusterName }: PotentialCustomersListProps) {
  const [searchQuery, setSearchQuery] = useState("");
  const [typeFilter, setTypeFilter] = useState("All");
  const [tierFilter, setTierFilter] = useState("All");
  const [locationFilter, setLocationFilter] = useState("All");
  const [frequencyFilter, setFrequencyFilter] = useState("All");
  const [sortBy, setSortBy] = useState<"budget" | "income" | "id">("budget");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");
  const [currentPage, setCurrentPage] = useState(1);

  const { data: rawCustomers, isLoading, isError, error } = useQuery({
    queryKey: ["segmentCustomers", clusterId],
    queryFn: () => getCustomersBySegment(clusterId, 3600),
  });

  const resetFilters = () => {
    setSearchQuery("");
    setTypeFilter("All");
    setTierFilter("All");
    setLocationFilter("All");
    setFrequencyFilter("All");
    setSortBy("budget");
    setSortOrder("desc");
    setCurrentPage(1);
  };

  const hasActiveFilters =
    searchQuery.trim() !== "" ||
    typeFilter !== "All" ||
    tierFilter !== "All" ||
    locationFilter !== "All" ||
    frequencyFilter !== "All";

  const filteredAndSortedCustomers = useMemo(() => {
    if (!rawCustomers) return [];

    let list = rawCustomers.filter((c) => {
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const idMatch = c.customer_id?.toLowerCase().includes(q);
        const typeMatch = c.customer_type?.toLowerCase().includes(q);
        const locMatch = c.preferred_location?.toLowerCase().includes(q);
        if (!idMatch && !typeMatch && !locMatch) return false;
      }
      if (typeFilter !== "All" && c.customer_type !== typeFilter) return false;
      if (tierFilter !== "All" && c.customer_tier !== tierFilter) return false;
      if (locationFilter !== "All" && c.preferred_location !== locationFilter) return false;
      if (frequencyFilter !== "All" && c.interaction_frequency !== frequencyFilter) return false;
      return true;
    });

    list.sort((a, b) => {
      let comparison = 0;
      if (sortBy === "budget") {
        comparison = (a.budget_max_egp || 0) - (b.budget_max_egp || 0);
      } else if (sortBy === "income") {
        comparison = (a.monthly_income_egp || 0) - (b.monthly_income_egp || 0);
      } else if (sortBy === "id") {
        comparison = (a.customer_id || "").localeCompare(b.customer_id || "");
      }
      return sortOrder === "asc" ? comparison : -comparison;
    });

    return list;
  }, [rawCustomers, searchQuery, typeFilter, tierFilter, locationFilter, frequencyFilter, sortBy, sortOrder]);

  const totalSegmentCount = rawCustomers ? rawCustomers.length : 0;
  const filteredCount = filteredAndSortedCustomers.length;
  const totalPages = Math.max(1, Math.ceil(filteredCount / PAGE_SIZE));
  const safePage = Math.min(currentPage, totalPages);
  const startIndex = (safePage - 1) * PAGE_SIZE;
  const displayedCustomers = filteredAndSortedCustomers.slice(startIndex, startIndex + PAGE_SIZE);

  return (
    <Card className="border-border bg-surface-primary mt-6">
      <CardHeader className="pb-3 border-b border-border/60">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <div className="flex items-center gap-2">
              <Users className="h-4 w-4 text-accent" aria-hidden="true" />
              <CardTitle className="text-sm font-bold">Customers Matching This Segment</CardTitle>
            </div>
            <CardDescription className="text-xs mt-0.5">
              Customers whose recorded behavioral and financial attributes match the active segment.
            </CardDescription>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <Badge variant="outline" className="text-xs font-mono">
              Active Segment: <span className="font-semibold text-text-primary ml-1">{clusterName}</span>
            </Badge>
            <Badge variant="info" className="text-xs font-mono">
              Cluster: {clusterId}
            </Badge>
            <Badge variant="outline" className="text-xs font-mono border-border text-text-muted">
              <Database className="h-3 w-3 text-accent mr-1 inline" aria-hidden="true" />
              Live CRM Records
            </Badge>
          </div>
        </div>

        <div className="mt-3.5 grid grid-cols-2 gap-3 sm:grid-cols-4">
          <div className="rounded-lg border border-border/70 bg-surface-secondary/50 p-2.5">
            <span className="block text-[11px] text-text-muted">Segment Population</span>
            <span className="text-base font-bold text-text-primary font-mono">
              {formatNumber(totalSegmentCount)}
            </span>
            <span className="block text-[10px] text-text-muted">Total active cluster cohort</span>
          </div>
          <div className="rounded-lg border border-border/70 bg-surface-secondary/50 p-2.5">
            <span className="block text-[11px] text-text-muted">Current CRM Results</span>
            <span className="text-base font-bold text-accent font-mono">
              {formatNumber(filteredCount)}
            </span>
            <span className="block text-[10px] text-text-muted">Matching active criteria</span>
          </div>
          <div className="rounded-lg border border-border/70 bg-surface-secondary/50 p-2.5">
            <span className="block text-[11px] text-text-muted">Current View</span>
            <span className="text-base font-bold text-text-primary font-mono">
              {filteredCount > 0 ? `${startIndex + 1}–${Math.min(startIndex + PAGE_SIZE, filteredCount)}` : "0"}
            </span>
            <span className="block text-[10px] text-text-muted">Profiles currently shown</span>
          </div>
          <div className="rounded-lg border border-border/70 bg-surface-secondary/50 p-2.5">
            <span className="block text-[11px] text-text-muted">Pagination</span>
            <span className="text-base font-bold text-text-primary font-mono">
              {safePage} / {totalPages}
            </span>
            <span className="block text-[10px] text-text-muted">Pages available</span>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-4 pt-4">
        <div className="space-y-3 rounded-lg border border-border/70 bg-surface-secondary/40 p-3">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="relative min-w-[240px] flex-1">
              <Search className="absolute left-2.5 top-2.5 h-3.5 w-3.5 text-text-muted" aria-hidden="true" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => {
                  setSearchQuery(e.target.value);
                  setCurrentPage(1);
                }}
                placeholder="Search by Customer ID, type, or market..."
                className="w-full rounded-md border border-border bg-surface-primary pl-8 pr-3 py-1.5 text-xs text-text-primary placeholder:text-text-muted focus:border-accent focus:outline-none"
              />
            </div>

            <div className="flex items-center gap-2">
              <div className="flex items-center gap-1 text-xs text-text-muted">
                <ArrowUpDown className="h-3.5 w-3.5" aria-hidden="true" />
                <span>Sort:</span>
              </div>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as "budget" | "income" | "id")}
                className="rounded-md border border-border bg-surface-primary px-2.5 py-1.5 text-xs text-text-secondary focus:border-accent focus:outline-none"
              >
                <option value="budget">Max Budget</option>
                <option value="income">Monthly Income</option>
                <option value="id">Customer ID</option>
              </select>
              <button
                type="button"
                onClick={() => setSortOrder(sortOrder === "asc" ? "desc" : "asc")}
                className="rounded-md border border-border bg-surface-primary px-2 py-1.5 text-xs text-text-secondary hover:text-text-primary"
                title="Toggle sort direction"
              >
                {sortOrder === "desc" ? "High → Low" : "Low → High"}
              </button>
              {hasActiveFilters && (
                <button
                  type="button"
                  onClick={resetFilters}
                  className="flex items-center gap-1 rounded-md border border-border bg-surface-primary px-2.5 py-1.5 text-xs text-status-warning hover:bg-surface-secondary"
                >
                  <RotateCcw className="h-3 w-3" aria-hidden="true" />
                  <span>Reset</span>
                </button>
              )}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-2 sm:grid-cols-4 text-xs">
            <div className="space-y-1">
              <label className="text-[11px] text-text-muted">Customer Type</label>
              <select
                value={typeFilter}
                onChange={(e) => {
                  setTypeFilter(e.target.value);
                  setCurrentPage(1);
                }}
                className="w-full rounded-md border border-border bg-surface-primary px-2 py-1.5 text-xs text-text-secondary focus:border-accent focus:outline-none"
              >
                {CUSTOMER_TYPES.map((t) => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-[11px] text-text-muted">Customer Tier</label>
              <select
                value={tierFilter}
                onChange={(e) => {
                  setTierFilter(e.target.value);
                  setCurrentPage(1);
                }}
                className="w-full rounded-md border border-border bg-surface-primary px-2 py-1.5 text-xs text-text-secondary focus:border-accent focus:outline-none"
              >
                {CUSTOMER_TIERS.map((t) => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-[11px] text-text-muted">Preferred Market</label>
              <select
                value={locationFilter}
                onChange={(e) => {
                  setLocationFilter(e.target.value);
                  setCurrentPage(1);
                }}
                className="w-full rounded-md border border-border bg-surface-primary px-2 py-1.5 text-xs text-text-secondary focus:border-accent focus:outline-none"
              >
                {LOCATIONS.map((loc) => (
                  <option key={loc} value={loc}>
                    {loc}
                  </option>
                ))}
              </select>
            </div>

            <div className="space-y-1">
              <label className="text-[11px] text-text-muted">Interaction Level</label>
              <select
                value={frequencyFilter}
                onChange={(e) => {
                  setFrequencyFilter(e.target.value);
                  setCurrentPage(1);
                }}
                className="w-full rounded-md border border-border bg-surface-primary px-2 py-1.5 text-xs text-text-secondary focus:border-accent focus:outline-none"
              >
                {FREQUENCIES.map((f) => (
                  <option key={f} value={f}>
                    {f}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2 pt-1 border-t border-border/40 text-[11px]">
            <span className="text-text-muted flex items-center gap-1">
              <Filter className="h-3 w-3" aria-hidden="true" />
              Active Filters:
            </span>
            <span className="rounded bg-surface-primary border border-border px-2 py-0.5 text-text-secondary font-mono">
              Segment: {clusterName}
            </span>
            <span className="rounded bg-surface-primary border border-border px-2 py-0.5 text-text-secondary font-mono">
              Cluster: {clusterId}
            </span>
            {typeFilter !== "All" && (
              <span className="rounded bg-accent/20 border border-accent/40 px-2 py-0.5 text-accent font-semibold">
                Type: {typeFilter}
              </span>
            )}
            {tierFilter !== "All" && (
              <span className="rounded bg-accent/20 border border-accent/40 px-2 py-0.5 text-accent font-semibold">
                Tier: {tierFilter}
              </span>
            )}
            {locationFilter !== "All" && (
              <span className="rounded bg-accent/20 border border-accent/40 px-2 py-0.5 text-accent font-semibold">
                Market: {locationFilter}
              </span>
            )}
            {frequencyFilter !== "All" && (
              <span className="rounded bg-accent/20 border border-accent/40 px-2 py-0.5 text-accent font-semibold">
                Interaction: {frequencyFilter}
              </span>
            )}
            {searchQuery.trim() !== "" && (
              <span className="rounded bg-accent/20 border border-accent/40 px-2 py-0.5 text-accent font-semibold">
                Query: "{searchQuery}"
              </span>
            )}
          </div>
        </div>

        {isLoading && (
          <div className="space-y-2">
            <Skeleton className="h-9 w-full" />
            <Skeleton className="h-9 w-full" />
            <Skeleton className="h-9 w-full" />
            <Skeleton className="h-9 w-full" />
          </div>
        )}

        {isError && (
          <div className="flex items-center gap-2 rounded-lg border border-status-danger/30 bg-status-danger/10 p-3 text-xs text-status-danger">
            <AlertCircle className="h-4 w-4" aria-hidden="true" />
            <span>{error instanceof Error ? error.message : "Failed to load matching customers"}</span>
          </div>
        )}

        {!isLoading && !isError && displayedCustomers.length > 0 && (
          <div className="space-y-3">
            <div className="overflow-x-auto rounded-lg border border-border/80">
              <table className="w-full text-left text-xs">
                <thead className="bg-surface-secondary/70 border-b border-border text-text-muted">
                  <tr>
                    <th className="py-2.5 px-3 font-semibold">Customer ID</th>
                    <th className="py-2.5 px-3 font-semibold">Type</th>
                    <th className="py-2.5 px-3 font-semibold">Tier</th>
                    <th className="py-2.5 px-3 font-semibold">Budget Range</th>
                    <th className="py-2.5 px-3 font-semibold">Monthly Income</th>
                    <th className="py-2.5 px-3 font-semibold">Interactions</th>
                    <th className="py-2.5 px-3 font-semibold">Preferred Market</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border/50 text-text-secondary">
                  {displayedCustomers.map((c) => (
                    <tr key={c.customer_id} className="hover:bg-surface-secondary/40 transition-colors">
                      <td className="py-2.5 px-3 font-mono font-semibold text-accent">{c.customer_id || "—"}</td>
                      <td className="py-2.5 px-3 text-text-primary">{c.customer_type || "—"}</td>
                      <td className="py-2.5 px-3">
                        <Badge
                          variant={
                            c.customer_tier === "Platinum"
                              ? "info"
                              : c.customer_tier === "Gold"
                              ? "warning"
                              : "outline"
                          }
                          className="text-[10px] py-0 px-2"
                        >
                          {c.customer_tier || "—"}
                        </Badge>
                      </td>
                      <td className="py-2.5 px-3 font-mono text-text-primary">
                        {formatEGP(c.budget_min_egp)} – {formatEGP(c.budget_max_egp)}
                      </td>
                      <td className="py-2.5 px-3 font-mono">{formatEGP(c.monthly_income_egp)}</td>
                      <td className="py-2.5 px-3">
                        <span className="capitalize">{c.interaction_frequency || "—"}</span>
                      </td>
                      <td className="py-2.5 px-3 text-text-muted">
                        <div className="flex items-center gap-1.5">
                          <MapPin className="h-3 w-3 text-text-muted shrink-0" aria-hidden="true" />
                          <span>{c.preferred_location || "—"}</span>
                          <span className="text-text-muted"> • </span>
                          <span>{c.preferred_property_type || "—"}</span>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="flex flex-wrap items-center justify-between gap-3 pt-2 text-xs text-text-muted">
              <div>
                Showing <span className="font-mono text-text-primary">{startIndex + 1}</span>–
                <span className="font-mono text-text-primary">{Math.min(startIndex + PAGE_SIZE, filteredCount)}</span> of{" "}
                <span className="font-mono text-text-primary">{formatNumber(filteredCount)}</span> matching records
                {filteredCount !== totalSegmentCount && (
                  <span> (filtered from {formatNumber(totalSegmentCount)} total segment profiles)</span>
                )}
              </div>

              <div className="flex items-center gap-2">
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                  disabled={safePage <= 1}
                  className="gap-1 text-xs"
                >
                  <ChevronLeft className="h-3.5 w-3.5" aria-hidden="true" />
                  <span>Previous</span>
                </Button>
                <span className="text-xs text-text-secondary font-mono px-2">
                  Page {safePage} of {totalPages}
                </span>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
                  disabled={safePage >= totalPages}
                  className="gap-1 text-xs"
                >
                  <span>Next</span>
                  <ChevronRight className="h-3.5 w-3.5" aria-hidden="true" />
                </Button>
              </div>
            </div>
          </div>
        )}

        {!isLoading && !isError && displayedCustomers.length === 0 && (
          <div className="rounded-lg border border-dashed border-border p-8 text-center text-xs text-text-muted">
            <Users className="mx-auto h-8 w-8 text-text-muted mb-2 opacity-40" aria-hidden="true" />
            <p className="font-medium text-text-secondary">No matching customer records found</p>
            <p className="mt-1">
              No profiles in {clusterName} match the currently applied search and filters.
            </p>
            <Button size="sm" variant="outline" onClick={resetFilters} className="mt-3 gap-1.5">
              <RotateCcw className="h-3.5 w-3.5" aria-hidden="true" />
              <span>Reset Filters</span>
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
