"use client";

import React from "react";
import { Shell } from "@/components/layout/Shell";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { LocationRevenueChart } from "@/components/charts/LocationRevenueChart";
import { RevenueTrendChart } from "@/components/charts/RevenueTrendChart";
import { VERIFIED_LOCATIONS, VERIFIED_PROPERTY_TYPES, DATASET_METRICS } from "@/lib/verified_data";
import { formatEGP, formatNumber } from "@/lib/utils";

export default function MarketAnalyticsPage() {
  return (
    <Shell
      title="Market Analytics & Geographic Performance"
      subtitle="Verified Phase 2 macroeconomic breakdowns and asset type distributions"
    >
      <div className="flex flex-wrap items-center justify-between gap-2.5 rounded-lg border border-border/70 bg-surface-primary/80 px-3.5 py-2 text-xs">
        <Badge variant="outline" className="text-xs">
          Source: Phase 2 Analytical Checkpoint (DuckDB & Pandas Reconciliation)
        </Badge>
        <span className="text-xs text-text-muted">Reconciled across 7,937 closed deals & 10 geographic corridors</span>
      </div>

      <div className="grid grid-cols-1 gap-3.5 sm:grid-cols-2 lg:grid-cols-4">
        <Card className="p-3.5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-text-secondary">Closed Deal Capital</span>
            <Badge variant="outline">Verified</Badge>
          </div>
          <div className="mt-1.5 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-text-primary tracking-tight">
              {formatEGP(DATASET_METRICS.closedDealsRevenueEgp)}
            </span>
          </div>
          <p className="mt-0.5 text-[11px] text-text-muted">
            Across 7,937 closed sales transactions
          </p>
        </Card>

        <Card className="p-3.5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-text-secondary">Top Regional Hub</span>
            <Badge variant="success">New Cairo</Badge>
          </div>
          <div className="mt-1.5 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-text-primary tracking-tight">
              {formatEGP(12425511200)}
            </span>
          </div>
          <p className="mt-0.5 text-[11px] text-text-muted">
            25.4% of total closed deal capital
          </p>
        </Card>

        <Card className="p-3.5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-text-secondary">Peak Asset Price / m²</span>
            <Badge variant="warning">Villas</Badge>
          </div>
          <div className="mt-1.5 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-text-primary tracking-tight">
              {formatEGP(53200)}/m²
            </span>
          </div>
          <p className="mt-0.5 text-[11px] text-text-muted">
            18.82M EGP average villa transaction size
          </p>
        </Card>

        <Card className="p-3.5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-text-secondary">Geographic Scope</span>
            <Badge variant="info">10 Hubs</Badge>
          </div>
          <div className="mt-1.5 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-text-primary tracking-tight">
              10 Hubs
            </span>
          </div>
          <p className="mt-0.5 text-[11px] text-text-muted">
            Greater Cairo, Alexandria, and Delta corridors
          </p>
        </Card>
      </div>

      <div>
        <div className="mb-2.5 flex items-center justify-between">
          <div>
            <h3 className="text-sm font-semibold tracking-tight text-text-primary">
              Market Findings & Evidence
            </h3>
            <p className="text-xs text-text-secondary">
              Core structural patterns extracted from reconciled transaction and inventory data
            </p>
          </div>
          <Badge variant="outline" className="text-[10px]">
            Analytical Synthesis
          </Badge>
        </div>

        <div className="grid grid-cols-1 gap-3.5 md:grid-cols-3">
          <Card className="p-3.5 space-y-2 border-l-2 border-l-accent">
            <div className="flex items-center justify-between">
              <Badge variant="info" className="text-[9px]">Regional Dominance</Badge>
              <span className="text-[10px] font-mono text-text-muted">44.1% Share</span>
            </div>
            <h4 className="text-xs font-bold text-text-primary">
              New Cairo & Sheikh Zayed capture 44.1% of closed transaction revenue
            </h4>
            <p className="text-[11px] text-text-secondary leading-relaxed">
              New Cairo (12.43B EGP, 1,246 deals) and Sheikh Zayed (9.16B EGP, 1,237 deals) comprise 21.59B EGP, anchoring institutional developer activity.
            </p>
          </Card>

          <Card className="p-3.5 space-y-2 border-l-2 border-l-status-warning">
            <div className="flex items-center justify-between">
              <Badge variant="warning" className="text-[9px]">Pricing Divergence</Badge>
              <span className="text-[10px] font-mono text-text-muted">3.9x Multiple</span>
            </div>
            <h4 className="text-xs font-bold text-text-primary">
              Regional deal sizes exhibit a sharp 3.9x geographic spread
            </h4>
            <p className="text-[11px] text-text-secondary leading-relaxed">
              Prime New Cairo transactions average 9.97M EGP per deal compared to 2.56M EGP in Mansoura and 2.82M EGP in Obour, highlighting stark regional purchasing power gaps.
            </p>
          </Card>

          <Card className="p-3.5 space-y-2 border-l-2 border-l-status-success">
            <div className="flex items-center justify-between">
              <Badge variant="success" className="text-[9px]">Asset Economics</Badge>
              <span className="text-[10px] font-mono text-text-muted">+21.5% Premium</span>
            </div>
            <h4 className="text-xs font-bold text-text-primary">
              Retail & Villa assets achieve peak square-meter pricing power
            </h4>
            <p className="text-[11px] text-text-secondary leading-relaxed">
              Villas reach 53,200 EGP/m² and Retail commands 51,200 EGP/m², exceeding standard apartments (42,150 EGP/m²) by 21.5% to 26.2%.
            </p>
          </Card>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Top Revenue Hubs by City</CardTitle>
              <Badge variant="outline">Verified Dataset Analytics</Badge>
            </div>
            <CardDescription>
              Closed transaction revenue concentration across major Egyptian urban corridors
            </CardDescription>
          </CardHeader>
          <CardContent>
            <LocationRevenueChart />
            <div className="mt-3 rounded-lg border border-border/70 bg-surface-secondary/50 p-2.5 text-xs text-text-secondary">
              <span className="font-semibold text-text-primary">Evidence: </span>
              Top 3 urban corridors (New Cairo, Sheikh Zayed, New Capital) capture 29.94B EGP (59.3% of all gross deal capital), leaving secondary regional centers with under 7% each.
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Quarterly Inflow vs. Net Margin</CardTitle>
              <Badge variant="outline">Verified Dataset Analytics</Badge>
            </div>
            <CardDescription>
              Operating performance trajectory across residential, commercial, and coastal sectors
            </CardDescription>
          </CardHeader>
          <CardContent>
            <RevenueTrendChart />
            <div className="mt-3 rounded-lg border border-border/70 bg-surface-secondary/50 p-2.5 text-xs text-text-secondary">
              <span className="font-semibold text-text-primary">Evidence: </span>
              Consistent expansion from 1.28B EGP (Q1 2024) to 2.48B EGP (Q3 2026) with net profit margins sustained above 94% reflects robust absorption and pricing retention.
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Property Type Economics (Drill-Down)</CardTitle>
            <CardDescription>Average price per square meter and inventory volume by asset class</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-border text-text-muted">
                    <th className="pb-1.5 font-medium">Asset Class</th>
                    <th className="pb-1.5 font-medium">Inventory Units</th>
                    <th className="pb-1.5 font-medium">Avg Price / m²</th>
                    <th className="pb-1.5 font-medium">Avg Unit Valuation</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border/60 text-text-secondary">
                  {VERIFIED_PROPERTY_TYPES.map((t) => (
                    <tr key={t.property_type} className="hover:bg-surface-secondary/40">
                      <td className="py-1.5 font-semibold text-text-primary">{t.property_type}</td>
                      <td className="py-1.5">{formatNumber(t.units_count)}</td>
                      <td className="py-1.5 font-mono text-accent">{formatEGP(t.avg_price_per_sqm)}</td>
                      <td className="py-1.5 font-mono">{formatEGP(t.avg_price_egp)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Regional Revenue Distribution Matrix (Drill-Down)</CardTitle>
            <CardDescription>Deal volume, average transaction size, and regional share</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-border text-text-muted">
                    <th className="pb-1.5 font-medium">Location</th>
                    <th className="pb-1.5 font-medium">Closed Revenue</th>
                    <th className="pb-1.5 font-medium">Deals</th>
                    <th className="pb-1.5 font-medium">Avg Deal Size</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border/60 text-text-secondary">
                  {VERIFIED_LOCATIONS.slice(0, 6).map((l) => (
                    <tr key={l.location} className="hover:bg-surface-secondary/40">
                      <td className="py-1.5 font-semibold text-text-primary">{l.location}</td>
                      <td className="py-1.5 font-mono text-text-primary">{formatEGP(l.revenue_egp)}</td>
                      <td className="py-1.5">{formatNumber(l.deals_count)}</td>
                      <td className="py-1.5 font-mono text-accent">{formatEGP(l.avg_deal_price_egp)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      </div>
    </Shell>
  );
}
