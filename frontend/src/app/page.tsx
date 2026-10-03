"use client";

import React from "react";
import Link from "next/link";
import { Shell } from "@/components/layout/Shell";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { DATASET_METRICS } from "@/lib/verified_data";
import { formatEGP, formatNumber, formatPercent } from "@/lib/utils";
import { RevenueTrendChart } from "@/components/charts/RevenueTrendChart";
import {
  TrendingUp,
  Building2,
  Users,
  Target,
  Cpu,
  ShieldAlert,
  ArrowUpRight,
  Database,
} from "lucide-react";

export default function DashboardPage() {
  return (
    <Shell
      title="Executive Intelligence Dashboard"
      subtitle="Synthesized real estate analytics and machine learning inference engine"
    >
      <div className="flex flex-wrap items-center justify-between gap-2.5 rounded-lg border border-border/70 bg-surface-primary/80 px-3.5 py-2 text-xs">
        <div className="flex flex-wrap items-center gap-2">
          <Badge variant="success" className="gap-1.5 font-semibold">
            <span className="h-1.5 w-1.5 rounded-full bg-status-success animate-pulse" aria-hidden="true" />
            Verified Q3 2026 Analytical Checkpoint
          </Badge>
          <Badge variant="outline">Greater Cairo & Coastal Expansion Corridors</Badge>
        </div>
        <span className="text-[11px] text-text-muted">
          Dataset Lineage: DuckDB & SQL Reconciliation • 47/47 Rules Validated
        </span>
      </div>

      <div className="grid grid-cols-1 gap-3.5 sm:grid-cols-2 lg:grid-cols-4">
        <Card className="p-3.5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-text-secondary">Total Inventory</span>
            <Badge variant="outline">Verified</Badge>
          </div>
          <div className="mt-1.5 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-text-primary tracking-tight">
              {formatNumber(DATASET_METRICS.totalUnits)} Units
            </span>
          </div>
          <p className="mt-0.5 text-[11px] text-text-muted">
            Across 20 prime compounds by 8 developers
          </p>
        </Card>

        <Card className="p-3.5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-text-secondary">Average Deal Price</span>
            <Badge variant="outline">Verified</Badge>
          </div>
          <div className="mt-1.5 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-text-primary tracking-tight">
              {formatEGP(DATASET_METRICS.averageDealPriceEgp)}
            </span>
          </div>
          <p className="mt-0.5 text-[11px] text-text-muted">
            Baseline across 7,937 closed transactions
          </p>
        </Card>

        <Card className="p-3.5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-text-secondary">Gross Deal Revenue</span>
            <Badge variant="success">94.7% Margin</Badge>
          </div>
          <div className="mt-1.5 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-status-success tracking-tight">
              {formatEGP(DATASET_METRICS.grossRevenueEgp)}
            </span>
          </div>
          <p className="mt-0.5 text-[11px] text-text-muted">
            {formatEGP(DATASET_METRICS.netOperatingIncomeEgp)} net operating income
          </p>
        </Card>

        <Card className="p-3.5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-text-secondary">Lead Conversion</span>
            <Badge variant="info">Evaluated</Badge>
          </div>
          <div className="mt-1.5 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-text-primary tracking-tight">
              {formatPercent(DATASET_METRICS.conversionRate)}
            </span>
          </div>
          <p className="mt-0.5 text-[11px] text-text-muted">
            59,778 ML-ready leads evaluated (0.50 threshold)
          </p>
        </Card>
      </div>

      <div>
        <div className="mb-2.5 flex items-center justify-between">
          <div>
            <h3 className="text-sm font-semibold tracking-tight text-text-primary">
              Key Market Insights
            </h3>
            <p className="text-xs text-text-secondary">
              Strategic findings derived directly from verified transaction datasets
            </p>
          </div>
          <Badge variant="outline" className="text-[10px]">
            Statement + Evidence
          </Badge>
        </div>

        <div className="grid grid-cols-1 gap-3.5 md:grid-cols-3">
          <Card className="p-3.5 space-y-2 border-l-2 border-l-accent">
            <div className="flex items-center justify-between">
              <span className="text-[11px] font-semibold uppercase tracking-wider text-accent">
                Developer Concentration
              </span>
              <Badge variant="outline" className="text-[9px]">50% Volume</Badge>
            </div>
            <h4 className="text-xs font-bold text-text-primary">
              Two developers control 50.0% of cataloged portfolio inventory
            </h4>
            <p className="text-[11px] text-text-secondary leading-relaxed">
              Palm Hills Legacy (1,250 units) and Mountain View East (1,250 units) represent 2,500 of the 5,000 units across 10 active projects.
            </p>
          </Card>

          <Card className="p-3.5 space-y-2 border-l-2 border-l-status-success">
            <div className="flex items-center justify-between">
              <span className="text-[11px] font-semibold uppercase tracking-wider text-status-success">
                Geographic Capital Flow
              </span>
              <Badge variant="outline" className="text-[9px]">59.3% Share</Badge>
            </div>
            <h4 className="text-xs font-bold text-text-primary">
              Over 59% of transaction capital is concentrated in three corridors
            </h4>
            <p className="text-[11px] text-text-secondary leading-relaxed">
              New Cairo (12.43B EGP), Sheikh Zayed (9.16B EGP), and New Capital (8.35B EGP) generated 29.94B EGP across 3,695 closed deals.
            </p>
          </Card>

          <Card className="p-3.5 space-y-2 border-l-2 border-l-status-warning">
            <div className="flex items-center justify-between">
              <span className="text-[11px] font-semibold uppercase tracking-wider text-status-warning">
                Asset Pricing Spread
              </span>
              <Badge variant="outline" className="text-[9px]">4.2x Spread</Badge>
            </div>
            <h4 className="text-xs font-bold text-text-primary">
              Luxury villas carry a 4.2x price multiple over standard apartments
            </h4>
            <p className="text-[11px] text-text-secondary leading-relaxed">
              Villas average 18.82M EGP (53,200 EGP/m²) versus apartments averaging 4.46M EGP (42,150 EGP/m²), defining the high-net-worth tier.
            </p>
          </Card>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Market Capital Inflow & Net Profit Trajectory</CardTitle>
                <CardDescription>
                  Quarterly gross deal revenue vs. net operating profit across 11 reconciled quarters (Q1 2024 – Q3 2026)
                </CardDescription>
              </div>
              <Badge variant="outline" className="text-[10px]">
                Macroeconomic Series
              </Badge>
            </div>
          </CardHeader>
          <CardContent>
            <RevenueTrendChart />
            <div className="mt-3 rounded-lg border border-border/70 bg-surface-secondary/50 p-2.5 text-xs text-text-secondary">
              <span className="font-semibold text-text-primary">Decision Context: </span>
              Quarterly inflow expanded from 1.28B EGP to 2.48B EGP (+94.1%) while operating expenses remained capped under 5.3% of revenue, demonstrating sustained operational leverage and strong cash coverage.
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Dataset Architecture</CardTitle>
              <Badge variant="outline">Immutable</Badge>
            </div>
            <CardDescription>Audited baseline parameters backing all decision layers</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2 text-xs">
              <div className="flex items-center justify-between border-b border-border/60 pb-1.5">
                <span className="text-text-secondary flex items-center gap-2">
                  <Building2 className="h-3.5 w-3.5 text-accent" />
                  Units Cataloged
                </span>
                <span className="font-semibold text-text-primary">
                  {formatNumber(DATASET_METRICS.totalUnits)}
                </span>
              </div>
              <div className="flex items-center justify-between border-b border-border/60 pb-1.5">
                <span className="text-text-secondary flex items-center gap-2">
                  <Database className="h-3.5 w-3.5 text-accent" />
                  Projects Tracked
                </span>
                <span className="font-semibold text-text-primary">
                  {DATASET_METRICS.totalProjects}
                </span>
              </div>
              <div className="flex items-center justify-between border-b border-border/60 pb-1.5">
                <span className="text-text-secondary flex items-center gap-2">
                  <Users className="h-3.5 w-3.5 text-accent" />
                  Processed Customers
                </span>
                <span className="font-semibold text-text-primary">
                  {formatNumber(DATASET_METRICS.processedCustomers)}
                </span>
              </div>
              <div className="flex items-center justify-between border-b border-border/60 pb-1.5">
                <span className="text-text-secondary flex items-center gap-2">
                  <Target className="h-3.5 w-3.5 text-accent" />
                  ML-Ready Leads
                </span>
                <span className="font-semibold text-text-primary">
                  {formatNumber(DATASET_METRICS.mlReadyLeads)}
                </span>
              </div>
              <div className="flex items-center justify-between pt-0.5">
                <span className="text-text-secondary flex items-center gap-2">
                  <ShieldAlert className="h-3.5 w-3.5 text-status-success" />
                  Data Quality Checks
                </span>
                <Badge variant="success">47/47 Passed</Badge>
              </div>
            </div>

            <div className="mt-3.5 rounded-lg border border-accent/30 bg-accent/10 p-2.5 text-[11px] text-text-secondary">
              <span className="font-semibold text-accent">Quality Guarantee: </span>
              Analytical joins across deals, units, and customers produced zero row duplication and verified conservation of total portfolio revenue.
            </div>
          </CardContent>
        </Card>
      </div>

      <Card className="p-4">
        <div className="mb-2 flex items-center justify-between">
          <h3 className="text-xs font-semibold uppercase tracking-wider text-text-secondary">
            Strategic Decision Context (What This Means)
          </h3>
          <Badge variant="outline" className="text-[10px]">Executive Summary</Badge>
        </div>
        <div className="grid grid-cols-1 gap-3 md:grid-cols-3 text-xs">
          <div className="rounded-lg border border-border/60 bg-surface-secondary/40 p-3 space-y-1">
            <span className="font-semibold text-text-primary">1. Tiered Pricing Discipline</span>
            <p className="text-[11px] text-text-secondary leading-relaxed">
              Orascom Development commands the top average price at 10.76M EGP, closely followed by Mountain View (9.68M EGP) and Palm Hills (9.51M EGP), establishing clear market differentiation.
            </p>
          </div>
          <div className="rounded-lg border border-border/60 bg-surface-secondary/40 p-3 space-y-1">
            <span className="font-semibold text-text-primary">2. Geographic Disparity (3.9x)</span>
            <p className="text-[11px] text-text-secondary leading-relaxed">
              Prime New Cairo transactions average 9.97M EGP compared to 2.56M EGP in Mansoura, requiring localized underwriting models rather than generalized national assumptions.
            </p>
          </div>
          <div className="rounded-lg border border-border/60 bg-surface-secondary/40 p-3 space-y-1">
            <span className="font-semibold text-text-primary">3. Predictive Modeling Feasibility</span>
            <p className="text-[11px] text-text-secondary leading-relaxed">
              A stable 13.2% lead conversion baseline and 50B EGP closed transaction base validate the accuracy bounds for price regression and rolling cash flow projections.
            </p>
          </div>
        </div>
      </Card>

      <div>
        <div className="mb-3 flex items-center justify-between">
          <div>
            <h3 className="text-sm font-semibold tracking-tight text-text-primary">
              Active Machine Learning Services
            </h3>
            <p className="text-xs text-text-secondary">
              Five validated models serving real-time predictions through FastAPI
            </p>
          </div>
          <Link
            href="/ml"
            className="flex items-center gap-1 text-xs font-medium text-accent hover:underline"
          >
            <span>Open ML Studio</span>
            <ArrowUpRight className="h-3.5 w-3.5" />
          </Link>
        </div>

        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
          <Card variant="interactive" className="p-3.5">
            <div className="flex items-center justify-between">
              <Cpu className="h-4 w-4 text-accent" />
              <Badge variant="info" className="text-[10px]">Regression</Badge>
            </div>
            <h4 className="mt-2 text-xs font-semibold text-text-primary">Price Prediction</h4>
            <p className="mt-1 text-[11px] text-text-secondary">
              Validated Random Forest regression model on 37 unit features
            </p>
            <p className="mt-2 text-[10px] font-mono text-text-muted">property_price_rf_v1</p>
          </Card>

          <Card variant="interactive" className="p-3.5">
            <div className="flex items-center justify-between">
              <Target className="h-4 w-4 text-status-success" />
              <Badge variant="success" className="text-[10px]">Classification</Badge>
            </div>
            <h4 className="mt-2 text-xs font-semibold text-text-primary">Lead Conversion</h4>
            <p className="mt-1 text-[11px] text-text-secondary">
              Logistic Regression with validated 0.50 frozen decision threshold
            </p>
            <p className="mt-2 text-[10px] font-mono text-text-muted">lead_conversion_lr_v1</p>
          </Card>

          <Card variant="interactive" className="p-3.5">
            <div className="flex items-center justify-between">
              <Users className="h-4 w-4 text-status-warning" />
              <Badge variant="warning" className="text-[10px]">Clustering</Badge>
            </div>
            <h4 className="mt-2 text-xs font-semibold text-text-primary">Customer Segmentation</h4>
            <p className="mt-1 text-[11px] text-text-secondary">
              K-Means 4-cluster model partitioning behavioral profiles
            </p>
            <p className="mt-2 text-[10px] font-mono text-text-muted">customer_kmeans_v1</p>
          </Card>

          <Card variant="interactive" className="p-3.5">
            <div className="flex items-center justify-between">
              <ShieldAlert className="h-4 w-4 text-status-danger" />
              <Badge variant="danger" className="text-[10px]">Anomaly</Badge>
            </div>
            <h4 className="mt-2 text-xs font-semibold text-text-primary">Property Anomalies</h4>
            <p className="mt-1 text-[11px] text-text-secondary">
              Isolation Forest detecting physical and valuation outliers
            </p>
            <p className="mt-2 text-[10px] font-mono text-text-muted">property_anomaly_iforest_v1</p>
          </Card>

          <Card variant="interactive" className="p-3.5">
            <div className="flex items-center justify-between">
              <TrendingUp className="h-4 w-4 text-status-info" />
              <Badge variant="info" className="text-[10px]">Time Series</Badge>
            </div>
            <h4 className="mt-2 text-xs font-semibold text-text-primary">Cash Flow Forecast</h4>
            <p className="mt-1 text-[11px] text-text-secondary">
              One-step-ahead daily rolling forecast with causal lag features
            </p>
            <p className="mt-2 text-[10px] font-mono text-text-muted">cash_flow_linear_v1</p>
          </Card>
        </div>
      </div>
    </Shell>
  );
}
