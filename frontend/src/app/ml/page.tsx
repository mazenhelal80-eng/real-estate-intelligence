"use client";

import React, { useState } from "react";
import { Shell } from "@/components/layout/Shell";
import { PricePredictionCard } from "@/components/ml/PricePredictionCard";
import { LeadConversionCard } from "@/components/ml/LeadConversionCard";
import { CustomerClusteringCard } from "@/components/ml/CustomerClusteringCard";
import { PropertyAnomalyCard } from "@/components/ml/PropertyAnomalyCard";
import { CashFlowForecastCard } from "@/components/ml/CashFlowForecastCard";
import { Badge } from "@/components/ui/Badge";
import { Cpu, Target, Users, ShieldAlert, TrendingUp, Layers } from "lucide-react";

export default function MLIntelligencePage() {
  const [activeTab, setActiveTab] = useState<string>("price");

  const tabs = [
    { id: "price", label: "Valuation Studio", icon: Cpu },
    { id: "lead", label: "Lead Conversion", icon: Target },
    { id: "segmentation", label: "Customer Discovery", icon: Users },
    { id: "anomaly", label: "Anomaly Detection", icon: ShieldAlert },
    { id: "forecast", label: "Cash Flow Forecast", icon: TrendingUp },
    { id: "all", label: "All 5 Capabilities", icon: Layers },
  ];

  return (
    <Shell
      title="ML Valuation Studio"
      subtitle="AI-powered property valuation and model diagnostics"
    >
      <div className="space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-2.5 rounded-lg border border-border/70 bg-surface-primary/80 px-3.5 py-1.5 backdrop-blur-sm text-xs">
          <div className="flex flex-wrap items-center gap-2">
            <Badge variant="success" className="gap-1.5 text-xs font-semibold">
              <span className="h-2 w-2 rounded-full bg-status-success animate-pulse" aria-hidden="true" />
              FastAPI Live (v1.0.0)
            </Badge>
            <Badge variant="outline" className="text-xs">
              Random Forest Regression
            </Badge>
            <Badge variant="outline" className="text-xs">
              Model v1
            </Badge>
            <Badge variant="outline" className="text-xs text-status-success">
              R² 0.9692
            </Badge>
            <Badge variant="outline" className="text-xs text-accent">
              Holdout MAE 547.3K EGP
            </Badge>
          </div>
          <div className="text-[11px] text-text-muted">
            Built by <span className="font-semibold text-text-secondary">Mazen Helal</span> • AI Engineer & Full-Stack AI Developer
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-2 border-b border-border/80 pb-2.5">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 rounded-lg border px-3 py-1.5 text-xs font-medium transition-colors ${
                  isActive
                    ? "border-accent bg-accent/20 text-accent font-semibold"
                    : "border-border bg-surface-secondary text-text-secondary hover:text-text-primary"
                }`}
              >
                <Icon className="h-3.5 w-3.5" aria-hidden="true" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        <div className="space-y-4">
          {(activeTab === "all" || activeTab === "price") && (
            <section>
              <PricePredictionCard />
            </section>
          )}

          {(activeTab === "all" || activeTab === "lead") && (
            <section>
              <LeadConversionCard />
            </section>
          )}

          {(activeTab === "all" || activeTab === "segmentation") && (
            <section>
              <CustomerClusteringCard />
            </section>
          )}

          {(activeTab === "all" || activeTab === "anomaly") && (
            <section>
              <PropertyAnomalyCard />
            </section>
          )}

          {(activeTab === "all" || activeTab === "forecast") && (
            <section>
              <CashFlowForecastCard />
            </section>
          )}
        </div>

        <details className="group rounded-lg border border-border/60 bg-surface-secondary/20 p-3.5 transition-colors hover:border-border">
          <summary className="flex cursor-pointer list-none items-center justify-between text-xs font-semibold uppercase tracking-wider text-text-muted hover:text-text-secondary select-none">
            <div className="flex items-center gap-2">
              <Layers className="h-4 w-4 text-accent" aria-hidden="true" />
              <span>Technical Architecture & Data Lineage</span>
            </div>
            <span className="text-[11px] text-accent font-mono transition-transform group-open:rotate-180">
              ▼
            </span>
          </summary>
          <div className="mt-3.5 pt-3 border-t border-border/50">
            <div className="grid grid-cols-1 gap-2 sm:grid-cols-5 text-center text-xs">
              <div className="rounded border border-border/50 bg-surface-primary/70 p-2">
                <span className="block text-[10px] text-text-muted">Phase 1</span>
                <span className="font-semibold text-text-primary">Data Foundation</span>
                <p className="mt-0.5 text-[10px] text-text-secondary">10 Verified CSVs</p>
              </div>
              <div className="rounded border border-border/50 bg-surface-primary/70 p-2">
                <span className="block text-[10px] text-text-muted">Phase 2</span>
                <span className="font-semibold text-text-primary">Feature Engineering</span>
                <p className="mt-0.5 text-[10px] text-text-secondary">Track 1, 2, 3 Schemas</p>
              </div>
              <div className="rounded border border-border/50 bg-surface-primary/70 p-2">
                <span className="block text-[10px] text-text-muted">Phase 3</span>
                <span className="font-semibold text-text-primary">Model Packaging</span>
                <p className="mt-0.5 text-[10px] text-text-secondary">5 Joblib Artifacts</p>
              </div>
              <div className="rounded border border-border/50 bg-surface-primary/70 p-2">
                <span className="block text-[10px] text-text-muted">Phase 4</span>
                <span className="font-semibold text-text-primary">FastAPI Service</span>
                <p className="mt-0.5 text-[10px] text-text-secondary">6 Typed REST Routes</p>
              </div>
              <div className="rounded border border-accent/40 bg-accent/15 p-2">
                <span className="block text-[10px] text-accent">Phase 5</span>
                <span className="font-semibold text-text-primary">Intelligence Studio</span>
                <p className="mt-0.5 text-[10px] text-text-secondary">Real-Time Decisions</p>
              </div>
            </div>
          </div>
        </details>
      </div>
    </Shell>
  );
}
