"use client";

import React, { useState } from "react";
import { Shell } from "@/components/layout/Shell";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { CustomerClusteringCard, CLUSTER_PROFILES, VERIFIED_ARCHETYPES } from "@/components/ml/CustomerClusteringCard";
import { Users, Crown, Award, Shield, UserCheck, Layers, Sparkles } from "lucide-react";

export default function CustomersPage() {
  const [selectedArchetype, setSelectedArchetype] = useState<string>("High-Net-Worth Investor");

  const tierOverviewCards = [
    {
      archetypeName: "High-Net-Worth Investor",
      tierLabel: "Platinum Tier",
      clusterLabel: "Cluster 1 • High-budget Investors",
      profilesCount: "2,260 Profiles (22.7%)",
      description: "High-net-worth portfolio allocators & luxury buyers",
      icon: Crown,
      accentColor: "text-amber-400",
      borderColor: "border-l-amber-400",
    },
    {
      archetypeName: "Mid-budget End User",
      tierLabel: "Gold Tier",
      clusterLabel: "Cluster 0 • Mid-budget End Users",
      profilesCount: "3,590 Profiles (36.0%)",
      description: "Middle-to-upper residential buyers & villa seekers",
      icon: Award,
      accentColor: "text-yellow-500",
      borderColor: "border-l-yellow-500",
    },
    {
      archetypeName: "Commercial Business Client",
      tierLabel: "Commercial Tier",
      clusterLabel: "Cluster 2 • Business Clients",
      profilesCount: "1,451 Profiles (14.6%)",
      description: "Corporate buyers & retail / office space allocators",
      icon: Shield,
      accentColor: "text-accent",
      borderColor: "border-l-accent",
    },
    {
      archetypeName: "Entry-Level First-Time Buyer",
      tierLabel: "Silver & Bronze Tier",
      clusterLabel: "Cluster 3 • Entry-level Buyers",
      profilesCount: "2,660 Profiles (26.7%)",
      description: "Value-conscious families & leasing tenants",
      icon: UserCheck,
      accentColor: "text-amber-700",
      borderColor: "border-l-amber-700",
    },
  ];

  return (
    <Shell
      title="Customer Intelligence & Profile Segmentation"
      subtitle="Behavioral profiling across verified customer records using live K-Means clustering"
    >
      <div className="space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-2.5 rounded-lg border border-border/70 bg-surface-primary/80 px-3.5 py-1.5 backdrop-blur-sm text-xs">
          <div className="flex flex-wrap items-center gap-2">
            <Badge variant="success" className="gap-1.5 text-xs font-semibold">
              <span className="h-2 w-2 rounded-full bg-status-success animate-pulse" aria-hidden="true" />
              FastAPI Live (v1.0.0)
            </Badge>
            <Badge variant="outline" className="text-xs">
              Model v1
            </Badge>
            <Badge variant="outline" className="text-xs font-mono">
              K-Means K=4
            </Badge>
            <Badge variant="outline" className="text-xs font-mono text-accent">
              16 Features
            </Badge>
            <Badge variant="outline" className="text-xs text-text-muted">
              9,961 Verified Records
            </Badge>
          </div>
          <div className="text-[11px] text-text-muted">
            Track 3 Unsupervised Clustering • Silhouette & Calinski-Harabasz Validated
          </div>
        </div>

        <div>
          <div className="mb-2 flex items-center justify-between">
            <div>
              <h3 className="text-xs font-semibold uppercase tracking-wider text-text-muted">
                Customer Segment Distribution & CRM Tier Alignment
              </h3>
              <p className="text-[11px] text-text-secondary">
                Click any segment card to activate its archetype in the Live Segmentation Engine below.
              </p>
            </div>
            <span className="text-[10px] text-text-muted font-mono">
              Total Population: 9,961 Profiles
            </span>
          </div>

          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4">
            {tierOverviewCards.map((card) => {
              const Icon = card.icon;
              const isSelected = selectedArchetype === card.archetypeName;
              return (
                <Card
                  key={card.archetypeName}
                  onClick={() => setSelectedArchetype(card.archetypeName)}
                  className={`cursor-pointer p-3.5 transition-all border-l-4 ${card.borderColor} ${
                    isSelected
                      ? "ring-2 ring-accent/60 bg-surface-secondary/70 shadow-sm"
                      : "hover:bg-surface-secondary/40 hover:border-border/90"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-text-primary">{card.tierLabel}</span>
                    <Icon className={`h-4 w-4 ${card.accentColor}`} aria-hidden="true" />
                  </div>
                  <span className="mt-1 block text-[11px] font-mono text-accent font-semibold">
                    {card.clusterLabel}
                  </span>
                  <p className="mt-1 text-base font-bold text-text-primary font-mono">{card.profilesCount}</p>
                  <p className="mt-0.5 text-[11px] text-text-muted leading-relaxed">{card.description}</p>
                  {isSelected && (
                    <div className="mt-2.5 flex items-center gap-1 text-[10px] font-semibold text-accent">
                      <Sparkles className="h-3 w-3" aria-hidden="true" />
                      <span>Active Workspace Segment</span>
                    </div>
                  )}
                </Card>
              );
            })}
          </div>
        </div>

        <div>
          <div className="mb-2.5 flex items-center justify-between">
            <div>
              <h3 className="text-sm font-semibold tracking-tight text-text-primary">
                Segment Behavioral Insights
              </h3>
              <p className="text-xs text-text-secondary">
                Strategic segmentation derived from customer transaction frequency, budgets, and location preferences
              </p>
            </div>
            <Badge variant="outline" className="text-[10px]">
              Cohort Intelligence
            </Badge>
          </div>

          <div className="grid grid-cols-1 gap-3.5 md:grid-cols-3">
            <Card className="p-3.5 space-y-2 border-l-2 border-l-amber-400">
              <div className="flex items-center justify-between">
                <Badge variant="warning" className="text-[9px]">Capital Profile</Badge>
                <span className="text-[10px] font-mono text-text-muted">44.9% Capital Base</span>
              </div>
              <h4 className="text-xs font-bold text-text-primary">
                Platinum & Gold cohorts anchor luxury villa and commercial absorption
              </h4>
              <p className="text-[11px] text-text-secondary leading-relaxed">
                4,472 customer records demonstrate purchasing capacity above 8M EGP, concentrated in New Cairo, Sheikh Zayed, and coastal developments.
              </p>
            </Card>

            <Card className="p-3.5 space-y-2 border-l-2 border-l-accent">
              <div className="flex items-center justify-between">
                <Badge variant="info" className="text-[9px]">Volume Core</Badge>
                <span className="text-[10px] font-mono text-text-muted">35.2% Volume Core</span>
              </div>
              <h4 className="text-xs font-bold text-text-primary">
                Silver tier forms the core residential sales engine
              </h4>
              <p className="text-[11px] text-text-secondary leading-relaxed">
                3,510 families with focused 4M–9M EGP budgets primarily seek 3–4 bedroom apartments in Sheikh Zayed, New Capital, and 6th of October.
              </p>
            </Card>

            <Card className="p-3.5 space-y-2 border-l-2 border-l-status-success">
              <div className="flex items-center justify-between">
                <Badge variant="success" className="text-[9px]">Leasing Demand</Badge>
                <span className="text-[10px] font-mono text-text-muted">19.9% Leasing Demand</span>
              </div>
              <h4 className="text-xs font-bold text-text-primary">
                Bronze tier sustains recurring rental occupancy yields
              </h4>
              <p className="text-[11px] text-text-secondary leading-relaxed">
                1,979 tenant profiles generate steady monthly cash flow across central mature hubs like Maadi and Nasr City, supporting property management returns.
              </p>
            </Card>
          </div>
        </div>

        <CustomerClusteringCard
          key={selectedArchetype}
          initialArchetype={selectedArchetype}
          onClusterResolved={(clusterId) => {
            const matchedArch = Object.keys(VERIFIED_ARCHETYPES).find(
              (k) => VERIFIED_ARCHETYPES[k].targetCluster === clusterId
            );
            if (matchedArch && matchedArch !== selectedArchetype) {
              setSelectedArchetype(matchedArch);
            }
          }}
        />

        <details className="group rounded-lg border border-border/60 bg-surface-secondary/20 p-3.5 transition-colors hover:border-border">
          <summary className="flex cursor-pointer list-none items-center justify-between text-xs font-semibold uppercase tracking-wider text-text-muted hover:text-text-secondary select-none">
            <div className="flex items-center gap-2">
              <Layers className="h-4 w-4 text-accent" aria-hidden="true" />
              <span>Historical Cluster Benchmarks & Statistical Distributions</span>
            </div>
            <span className="text-[11px] text-accent font-mono transition-transform group-open:rotate-180">
              ▼
            </span>
          </summary>
          <div className="mt-3.5 pt-3 border-t border-border/50">
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4 text-xs">
              {Object.values(CLUSTER_PROFILES).map((prof) => (
                <div key={prof.clusterId} className="rounded-lg border border-border/60 bg-surface-primary/70 p-3 space-y-1.5">
                  <div className="flex items-center justify-between">
                    <Badge variant="outline" className="font-mono text-[10px]">
                      Cluster {prof.clusterId}
                    </Badge>
                    <span className="text-[10px] text-text-muted font-mono">{prof.sharePct}%</span>
                  </div>
                  <h5 className="font-bold text-text-primary text-xs">{prof.title}</h5>
                  <p className="text-[11px] text-text-secondary leading-relaxed">{prof.description}</p>
                  <div className="pt-1 text-[10px] text-text-muted font-mono">
                    Dominant: {prof.dominantTier} • {prof.dominantType}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </details>
      </div>
    </Shell>
  );
}
