"use client";

import React from "react";
import { Shell } from "@/components/layout/Shell";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { DeveloperBarChart } from "@/components/charts/DeveloperBarChart";
import { VERIFIED_DEVELOPERS, DATASET_METRICS } from "@/lib/verified_data";
import { formatEGP, formatNumber } from "@/lib/utils";

export default function DevelopersPage() {
  return (
    <Shell
      title="Developer & Project Performance Matrix"
      subtitle="Verified unit launch volumes, active developments, and pricing across 8 institutional developers"
    >
      <div className="flex flex-wrap items-center justify-between gap-2.5 rounded-lg border border-border/70 bg-surface-primary/80 px-3.5 py-2 text-xs">
        <Badge variant="outline" className="text-xs">
          Source: Phase 2 Analytical Checkpoint (DuckDB & Pandas Reconciliation)
        </Badge>
        <span className="text-xs text-text-muted">Reconciled across 8 institutional developers & 20 active compounds</span>
      </div>

      <div className="grid grid-cols-1 gap-3.5 sm:grid-cols-2 lg:grid-cols-4">
        <Card className="p-3.5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-text-secondary">Tracked Developers</span>
            <Badge variant="outline">Verified</Badge>
          </div>
          <div className="mt-1.5 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-text-primary tracking-tight">
              8 Partners
            </span>
          </div>
          <p className="mt-0.5 text-[11px] text-text-muted">
            Across 20 active development compounds
          </p>
        </Card>

        <Card className="p-3.5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-text-secondary">Portfolio Inventory</span>
            <Badge variant="outline">Verified</Badge>
          </div>
          <div className="mt-1.5 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-text-primary tracking-tight">
              {formatNumber(DATASET_METRICS.totalUnits)} Units
            </span>
          </div>
          <p className="mt-0.5 text-[11px] text-text-muted">
            100% cataloged and feature-engineered
          </p>
        </Card>

        <Card className="p-3.5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-text-secondary">Peak Average Price</span>
            <Badge variant="warning">Orascom</Badge>
          </div>
          <div className="mt-1.5 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-text-primary tracking-tight">
              {formatEGP(10763802)}
            </span>
          </div>
          <p className="mt-0.5 text-[11px] text-text-muted">
            Top average valuation in current dataset
          </p>
        </Card>

        <Card className="p-3.5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-text-secondary">Top Portfolio Share</span>
            <Badge variant="info">Palm Hills / MV</Badge>
          </div>
          <div className="mt-1.5 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-text-primary tracking-tight">
              25.0%
            </span>
          </div>
          <p className="mt-0.5 text-[11px] text-text-muted">
            1,250 units each across 5 compounds
          </p>
        </Card>
      </div>

      <div>
        <div className="mb-2.5 flex items-center justify-between">
          <div>
            <h3 className="text-sm font-semibold tracking-tight text-text-primary">
              Developer Insights & Market Positioning
            </h3>
            <p className="text-xs text-text-secondary">
              Strategic segmentation extracted from developer pricing, volumes, and footprint
            </p>
          </div>
          <Badge variant="outline" className="text-[10px]">
            Comparative Intelligence
          </Badge>
        </div>

        <div className="grid grid-cols-1 gap-3.5 md:grid-cols-3">
          <Card className="p-3.5 space-y-2 border-l-2 border-l-warning">
            <div className="flex items-center justify-between">
              <Badge variant="warning" className="text-[9px]">Valuation Leader</Badge>
              <span className="text-[10px] font-mono text-text-muted">10.76M EGP Avg</span>
            </div>
            <h4 className="text-xs font-bold text-text-primary">
              Orascom Development records highest average property valuation
            </h4>
            <p className="text-[11px] text-text-secondary leading-relaxed">
              With an average unit price of 10.76M EGP in New Cairo, Orascom exceeds the overall market baseline (6.17M EGP) by 74.4%, leading the premium tier.
            </p>
          </Card>

          <Card className="p-3.5 space-y-2 border-l-2 border-l-accent">
            <div className="flex items-center justify-between">
              <Badge variant="info" className="text-[9px]">Volume Dominance</Badge>
              <span className="text-[10px] font-mono text-text-muted">50.0% Portfolio</span>
            </div>
            <h4 className="text-xs font-bold text-text-primary">
              Palm Hills & Mountain View supply 50.0% of total cataloged inventory
            </h4>
            <p className="text-[11px] text-text-secondary leading-relaxed">
              Palm Hills Legacy (1,250 units) and Mountain View East (1,250 units) each command 25.0% of inventory across 10 active projects in East and West Cairo.
            </p>
          </Card>

          <Card className="p-3.5 space-y-2 border-l-2 border-l-status-success">
            <div className="flex items-center justify-between">
              <Badge variant="success" className="text-[9px]">Price Dispersion</Badge>
              <span className="text-[10px] font-mono text-text-muted">3.8x Spread</span>
            </div>
            <h4 className="text-xs font-bold text-text-primary">
              Developer price levels exhibit a wide 3.8x market differentiation
            </h4>
            <p className="text-[11px] text-text-secondary leading-relaxed">
              Average prices span from Misr Italia Urban (2.82M EGP) and Sodic Prestige (3.07M EGP) up to luxury developers exceeding 9.5M EGP.
            </p>
          </Card>
        </div>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Unit Launches by Developer (Volume Evidence)</CardTitle>
              <CardDescription>Verified inventory cataloged across 20 prime development projects</CardDescription>
            </div>
            <Badge variant="outline">Verified Dataset Analytics</Badge>
          </div>
        </CardHeader>
        <CardContent>
          <DeveloperBarChart />
          <div className="mt-3 rounded-lg border border-border/70 bg-surface-secondary/50 p-2.5 text-xs text-text-secondary">
            <span className="font-semibold text-text-primary">Evidence: </span>
            Portfolio inventory is bifurcated between mega-community developers launching 1,250 units each and boutique developments with focused allocations of 250 to 500 units.
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Institutional Developer Leaderboard (Drill-Down)</CardTitle>
              <CardDescription>Project density, launch footprint, market share, and average asset value</CardDescription>
            </div>
            <Badge variant="outline">8 Tracked Entities</Badge>
          </div>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-border text-text-muted">
                  <th className="pb-1.5 font-medium">Developer</th>
                  <th className="pb-1.5 font-medium">Projects</th>
                  <th className="pb-1.5 font-medium">Cataloged Units</th>
                  <th className="pb-1.5 font-medium">Portfolio Share</th>
                  <th className="pb-1.5 font-medium">Core Footprint</th>
                  <th className="pb-1.5 font-medium">Average Unit Price</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border/60 text-text-secondary">
                {VERIFIED_DEVELOPERS.map((d) => (
                  <tr key={d.developer_name} className="hover:bg-surface-secondary/40">
                    <td className="py-2 font-semibold text-text-primary">{d.developer_name}</td>
                    <td className="py-2">{d.active_projects}</td>
                    <td className="py-2">{formatNumber(d.total_units)}</td>
                    <td className="py-2 font-mono text-text-secondary">{((d.total_units / DATASET_METRICS.totalUnits) * 100).toFixed(1)}%</td>
                    <td className="py-2 text-text-muted">{d.location}</td>
                    <td className="py-2 font-mono font-bold text-accent">{formatEGP(d.avg_price_egp)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </Shell>
  );
}
