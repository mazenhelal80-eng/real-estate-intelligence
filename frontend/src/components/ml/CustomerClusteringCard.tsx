"use client";

import React, { useState, useEffect } from "react";
import { useMutation } from "@tanstack/react-query";
import { segmentCustomer } from "@/lib/api";
import { CustomerSegmentationRequest, CustomerSegmentationResponse } from "@/types/api";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { PotentialCustomersList } from "./PotentialCustomersList";
import { ModelMetadataCard } from "./ModelMetadataCard";
import { formatEGP, formatNumber } from "@/lib/utils";
import {
  Users,
  AlertCircle,
  TrendingUp,
  Layers,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  Target,
  FileText,
} from "lucide-react";

export const CLUSTER_PROFILES: Record<
  number,
  {
    clusterId: number;
    title: string;
    dominantType: string;
    dominantTier: string;
    avgMaxBudget: number;
    avgIncome: number;
    sharePct: number;
    populationCount: number;
    description: string;
    actionStrategy: string;
    commercialContext: string;
  }
> = {
  0: {
    clusterId: 0,
    title: "Mid-budget End Users",
    dominantType: "End User",
    dominantTier: "Gold",
    avgMaxBudget: 11372630,
    avgIncome: 195339,
    sharePct: 36.04,
    populationCount: 3590,
    description: "Stable middle-to-upper income residential purchasers seeking 3–4 bedroom primary residences with structured financing.",
    actionStrategy: "Target ready-to-move apartments and townhouses in New Cairo and Sheikh Zayed with flexible 6–8 year payment schedules.",
    commercialContext: "Primary residential volume core for developer cash flow generation.",
  },
  1: {
    clusterId: 1,
    title: "High-budget Investors",
    dominantType: "Investor",
    dominantTier: "Platinum",
    avgMaxBudget: 26219773,
    avgIncome: 454313,
    sharePct: 22.69,
    populationCount: 2260,
    description: "High-net-worth portfolio allocators focused on standalone luxury villas, penthouses, and high-yield compound developments.",
    actionStrategy: "Prioritize off-market luxury releases, construction-linked milestone structures, and verified rental yield models.",
    commercialContext: "High-equity buyers driving luxury asset absorption and large transaction values.",
  },
  2: {
    clusterId: 2,
    title: "Commercial / High-income Business Clients",
    dominantType: "Business",
    dominantTier: "Gold & Platinum",
    avgMaxBudget: 12343980,
    avgIncome: 805831,
    sharePct: 14.57,
    populationCount: 1451,
    description: "Corporate entities and high-earning commercial buyers acquiring retail spaces, prime office units, and mixed-use properties.",
    actionStrategy: "Direct toward prime business districts in New Capital and Maadi with dedicated commercial parking and facilities.",
    commercialContext: "High-yield commercial absorption with rapid capitalization and low tenant turnover.",
  },
  3: {
    clusterId: 3,
    title: "Entry-level / Moderate-income End Users",
    dominantType: "End User",
    dominantTier: "Silver & Bronze",
    avgMaxBudget: 5468751,
    avgIncome: 158170,
    sharePct: 26.70,
    populationCount: 2660,
    description: "Value-conscious families and first-time buyers prioritizing budget discipline and extended installment horizons.",
    actionStrategy: "Highlight 2-bedroom units, long-term 7–10 year payment horizons, and emerging expansion corridors like El Shorouk.",
    commercialContext: "Entry-level volume buyers and long-term rental demand anchors.",
  },
};

export const SCALING_CONSTANTS = {
  means: {
    budget_min_egp: 7714230.802931433,
    budget_max_egp: 13306136.0473848,
    budget_spread_egp: 5591905.244453368,
    monthly_income_egp: 333100.08001204696,
    income_to_budget_ratio: 0.35088152795904026,
  },
  scales: {
    budget_min_egp: 4038394.136420703,
    budget_max_egp: 8540186.572288765,
    budget_spread_egp: 4872099.989698906,
    monthly_income_egp: 266190.97726471344,
    income_to_budget_ratio: 0.2888837154500372,
  },
};

export interface RawCustomerProfile {
  budgetMin: number;
  budgetMax: number;
  monthlyIncome: number;
  customerType: "Investor" | "End User" | "Business" | "Landlord";
  customerTier: "Platinum" | "Gold" | "Silver" | "Bronze";
  interactionFrequency: "High" | "Medium" | "Low";
}

export const VERIFIED_ARCHETYPES: Record<
  string,
  {
    name: string;
    targetCluster: number;
    description: string;
    profile: RawCustomerProfile;
  }
> = {
  "High-Net-Worth Investor": {
    name: "High-Net-Worth Investor",
    targetCluster: 1,
    description: "Substantial capital base seeking standalone luxury properties and high-yield asset portfolios.",
    profile: {
      budgetMin: 15000000,
      budgetMax: 35000000,
      monthlyIncome: 450000,
      customerType: "Investor",
      customerTier: "Platinum",
      interactionFrequency: "Medium",
    },
  },
  "Mid-budget End User": {
    name: "Mid-budget End User",
    targetCluster: 0,
    description: "Stable residential buyer focused on 3–4 bedroom primary residences with balanced financing horizons.",
    profile: {
      budgetMin: 7200000,
      budgetMax: 11400000,
      monthlyIncome: 195000,
      customerType: "End User",
      customerTier: "Gold",
      interactionFrequency: "Medium",
    },
  },
  "Commercial Business Client": {
    name: "Commercial Business Client",
    targetCluster: 2,
    description: "Corporate or professional entity acquiring retail, office, and mixed-use commercial inventory.",
    profile: {
      budgetMin: 8000000,
      budgetMax: 15000000,
      monthlyIncome: 850000,
      customerType: "Business",
      customerTier: "Gold",
      interactionFrequency: "High",
    },
  },
  "Entry-Level First-Time Buyer": {
    name: "Entry-Level First-Time Buyer",
    targetCluster: 3,
    description: "Value-conscious purchaser prioritizing budget discipline and extended installment plans.",
    profile: {
      budgetMin: 3700000,
      budgetMax: 5500000,
      monthlyIncome: 158000,
      customerType: "End User",
      customerTier: "Silver",
      interactionFrequency: "Medium",
    },
  },
};

export function transformToStandardizedFeatures(raw: RawCustomerProfile): CustomerSegmentationRequest {
  const spread = Math.max(0, raw.budgetMax - raw.budgetMin);
  const ratio = raw.budgetMax > 0 ? (raw.monthlyIncome * 12) / raw.budgetMax : 0;
  return {
    budget_min_egp: (raw.budgetMin - SCALING_CONSTANTS.means.budget_min_egp) / SCALING_CONSTANTS.scales.budget_min_egp,
    budget_max_egp: (raw.budgetMax - SCALING_CONSTANTS.means.budget_max_egp) / SCALING_CONSTANTS.scales.budget_max_egp,
    budget_spread_egp: (spread - SCALING_CONSTANTS.means.budget_spread_egp) / SCALING_CONSTANTS.scales.budget_spread_egp,
    monthly_income_egp: (raw.monthlyIncome - SCALING_CONSTANTS.means.monthly_income_egp) / SCALING_CONSTANTS.scales.monthly_income_egp,
    income_to_budget_ratio: (ratio - SCALING_CONSTANTS.means.income_to_budget_ratio) / SCALING_CONSTANTS.scales.income_to_budget_ratio,
    customer_type_Business: raw.customerType === "Business" ? 1.0 : 0.0,
    "customer_type_End User": raw.customerType === "End User" ? 1.0 : 0.0,
    customer_type_Investor: raw.customerType === "Investor" ? 1.0 : 0.0,
    customer_type_Landlord: raw.customerType === "Landlord" ? 1.0 : 0.0,
    customer_tier_Bronze: raw.customerTier === "Bronze" ? 1.0 : 0.0,
    customer_tier_Gold: raw.customerTier === "Gold" ? 1.0 : 0.0,
    customer_tier_Platinum: raw.customerTier === "Platinum" ? 1.0 : 0.0,
    customer_tier_Silver: raw.customerTier === "Silver" ? 1.0 : 0.0,
    interaction_frequency_High: raw.interactionFrequency === "High" ? 1.0 : 0.0,
    interaction_frequency_Low: raw.interactionFrequency === "Low" ? 1.0 : 0.0,
    interaction_frequency_Medium: raw.interactionFrequency === "Medium" ? 1.0 : 0.0,
  };
}

interface CustomerClusteringCardProps {
  initialArchetype?: string;
  onClusterResolved?: (clusterId: number) => void;
}

export function CustomerClusteringCard({ initialArchetype = "High-Net-Worth Investor", onClusterResolved }: CustomerClusteringCardProps) {
  const [selectedArchetypeName, setSelectedArchetypeName] = useState<string>(initialArchetype);
  const [currentProfile, setCurrentProfile] = useState<RawCustomerProfile>(
    VERIFIED_ARCHETYPES[initialArchetype]?.profile || VERIFIED_ARCHETYPES["High-Net-Worth Investor"].profile
  );
  const [result, setResult] = useState<CustomerSegmentationResponse | null>(null);

  const mutation = useMutation({
    mutationFn: segmentCustomer,
    onSuccess: (data) => {
      setResult(data);
      if (onClusterResolved) {
        onClusterResolved(data.cluster_id);
      }
    },
  });

  useEffect(() => {
    const payload = transformToStandardizedFeatures(currentProfile);
    mutation.mutate(payload);
  }, []);

  const handleArchetypeClick = (archetypeName: string) => {
    setSelectedArchetypeName(archetypeName);
    const newProfile = VERIFIED_ARCHETYPES[archetypeName].profile;
    setCurrentProfile(newProfile);
    const payload = transformToStandardizedFeatures(newProfile);
    mutation.mutate(payload);
  };

  const handleRunInference = () => {
    const payload = transformToStandardizedFeatures(currentProfile);
    mutation.mutate(payload);
  };

  const activeClusterId = result ? result.cluster_id : 1;
  const activeProfile = CLUSTER_PROFILES[activeClusterId] || CLUSTER_PROFILES[1];
  const calculatedSpread = Math.max(0, currentProfile.budgetMax - currentProfile.budgetMin);
  const calculatedRatio = currentProfile.budgetMax > 0 ? (currentProfile.monthlyIncome * 12) / currentProfile.budgetMax : 0;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        <div className="lg:col-span-7 space-y-4">
          <Card className="border-border bg-surface-primary">
            <CardHeader className="pb-3 border-b border-border/60">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <Users className="h-5 w-5 text-accent" aria-hidden="true" />
                  <CardTitle className="text-base font-bold">Live Segmentation Engine</CardTitle>
                </div>
                <div className="flex items-center gap-1.5">
                  <Badge variant="outline" className="text-xs font-mono">
                    K-Means (K=4)
                  </Badge>
                  <Badge variant="outline" className="text-xs font-mono">
                    16 Features
                  </Badge>
                </div>
              </div>
              <CardDescription className="text-xs mt-1">
                Define a customer profile and let the K-Means model assign the closest behavioral segment.
              </CardDescription>
            </CardHeader>

            <CardContent className="space-y-4 pt-4">
              <div>
                <span className="text-xs font-semibold text-text-secondary">Customer Profile Archetype:</span>
                <div className="mt-2 grid grid-cols-1 gap-2 sm:grid-cols-2">
                  {Object.keys(VERIFIED_ARCHETYPES).map((name) => {
                    const arch = VERIFIED_ARCHETYPES[name];
                    const isSelected = selectedArchetypeName === name;
                    return (
                      <button
                        key={name}
                        type="button"
                        onClick={() => handleArchetypeClick(name)}
                        className={`rounded-lg border p-2.5 text-left transition-all ${
                          isSelected
                            ? "border-accent bg-accent/20 text-accent font-semibold shadow-sm"
                            : "border-border bg-surface-secondary text-text-secondary hover:text-text-primary hover:border-border/90"
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-bold">{name}</span>
                          <span className="text-[10px] font-mono opacity-80">Cluster {arch.targetCluster}</span>
                        </div>
                        <p className="mt-1 text-[11px] text-text-muted line-clamp-2 leading-relaxed">
                          {arch.description}
                        </p>
                      </button>
                    );
                  })}
                </div>
              </div>

              <div className="rounded-lg border border-border/80 bg-surface-secondary/40 p-3.5 space-y-3">
                <span className="text-xs font-semibold text-text-primary block">Financial & Behavioral Inputs</span>
                
                <div className="grid grid-cols-1 gap-3 sm:grid-cols-3 text-xs">
                  <div className="space-y-1">
                    <label className="text-[11px] text-text-muted">Min Budget (EGP)</label>
                    <input
                      type="number"
                      value={currentProfile.budgetMin}
                      onChange={(e) => {
                        setSelectedArchetypeName("Custom");
                        setCurrentProfile({ ...currentProfile, budgetMin: Number(e.target.value) });
                      }}
                      className="w-full rounded border border-border bg-surface-primary px-2.5 py-1.5 font-mono text-text-primary text-xs focus:border-accent focus:outline-none"
                    />
                    <span className="text-[10px] text-text-muted font-mono block">
                      {formatEGP(currentProfile.budgetMin)}
                    </span>
                  </div>

                  <div className="space-y-1">
                    <label className="text-[11px] text-text-muted">Max Budget (EGP)</label>
                    <input
                      type="number"
                      value={currentProfile.budgetMax}
                      onChange={(e) => {
                        setSelectedArchetypeName("Custom");
                        setCurrentProfile({ ...currentProfile, budgetMax: Number(e.target.value) });
                      }}
                      className="w-full rounded border border-border bg-surface-primary px-2.5 py-1.5 font-mono text-text-primary text-xs focus:border-accent focus:outline-none"
                    />
                    <span className="text-[10px] text-text-muted font-mono block">
                      {formatEGP(currentProfile.budgetMax)}
                    </span>
                  </div>

                  <div className="space-y-1">
                    <label className="text-[11px] text-text-muted">Monthly Income (EGP)</label>
                    <input
                      type="number"
                      value={currentProfile.monthlyIncome}
                      onChange={(e) => {
                        setSelectedArchetypeName("Custom");
                        setCurrentProfile({ ...currentProfile, monthlyIncome: Number(e.target.value) });
                      }}
                      className="w-full rounded border border-border bg-surface-primary px-2.5 py-1.5 font-mono text-text-primary text-xs focus:border-accent focus:outline-none"
                    />
                    <span className="text-[10px] text-text-muted font-mono block">
                      {formatEGP(currentProfile.monthlyIncome)}
                    </span>
                  </div>
                </div>

                <div className="grid grid-cols-1 gap-3 sm:grid-cols-3 text-xs pt-1 border-t border-border/50">
                  <div className="space-y-1">
                    <label className="text-[11px] text-text-muted">Customer Type</label>
                    <select
                      value={currentProfile.customerType}
                      onChange={(e) => {
                        setSelectedArchetypeName("Custom");
                        setCurrentProfile({
                          ...currentProfile,
                          customerType: e.target.value as RawCustomerProfile["customerType"],
                        });
                      }}
                      className="w-full rounded border border-border bg-surface-primary px-2.5 py-1.5 text-text-primary text-xs focus:border-accent focus:outline-none"
                    >
                      <option value="Investor">Investor</option>
                      <option value="End User">End User</option>
                      <option value="Business">Business</option>
                      <option value="Landlord">Landlord</option>
                    </select>
                  </div>

                  <div className="space-y-1">
                    <label className="text-[11px] text-text-muted">Customer Tier</label>
                    <select
                      value={currentProfile.customerTier}
                      onChange={(e) => {
                        setSelectedArchetypeName("Custom");
                        setCurrentProfile({
                          ...currentProfile,
                          customerTier: e.target.value as RawCustomerProfile["customerTier"],
                        });
                      }}
                      className="w-full rounded border border-border bg-surface-primary px-2.5 py-1.5 text-text-primary text-xs focus:border-accent focus:outline-none"
                    >
                      <option value="Platinum">Platinum</option>
                      <option value="Gold">Gold</option>
                      <option value="Silver">Silver</option>
                      <option value="Bronze">Bronze</option>
                    </select>
                  </div>

                  <div className="space-y-1">
                    <label className="text-[11px] text-text-muted">Interaction Frequency</label>
                    <select
                      value={currentProfile.interactionFrequency}
                      onChange={(e) => {
                        setSelectedArchetypeName("Custom");
                        setCurrentProfile({
                          ...currentProfile,
                          interactionFrequency: e.target.value as RawCustomerProfile["interactionFrequency"],
                        });
                      }}
                      className="w-full rounded border border-border bg-surface-primary px-2.5 py-1.5 text-text-primary text-xs focus:border-accent focus:outline-none"
                    >
                      <option value="High">High</option>
                      <option value="Medium">Medium</option>
                      <option value="Low">Low</option>
                    </select>
                  </div>
                </div>

                <div className="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-border/50 text-[11px] text-text-muted font-mono">
                  <span>Computed Spread: <span className="text-text-primary">{formatEGP(calculatedSpread)}</span></span>
                  <span>Annualized Income/Budget Ratio: <span className="text-text-primary">{calculatedRatio.toFixed(3)}</span></span>
                </div>
              </div>

              <div className="flex flex-wrap items-center justify-between gap-3 border-t border-border/60 pt-3">
                <span className="text-xs text-text-muted">
                  Standardized via Track 3 StandardScaler pipeline to scikit-learn K-Means contract.
                </span>
                <Button onClick={handleRunInference} isLoading={mutation.isPending} size="sm" className="gap-1.5">
                  <Sparkles className="h-3.5 w-3.5" aria-hidden="true" />
                  <span>Run Segmentation</span>
                </Button>
              </div>

              {mutation.isError && (
                <div className="flex items-center gap-2 rounded-lg border border-status-danger/30 bg-status-danger/10 p-3 text-xs text-status-danger">
                  <AlertCircle className="h-4 w-4 shrink-0" aria-hidden="true" />
                  <span>{mutation.error.message}</span>
                </div>
              )}
            </CardContent>
          </Card>

          <Card className="border-border bg-surface-primary">
            <CardHeader className="pb-2">
              <CardTitle className="text-xs font-semibold uppercase tracking-wider text-text-secondary">
                Commercial Decision Context
              </CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-1 gap-3 sm:grid-cols-3 text-xs text-text-secondary">
              <div className="rounded-lg border border-border/60 bg-surface-secondary/40 p-3 space-y-1">
                <h5 className="font-semibold text-text-primary flex items-center gap-1.5">
                  <Target className="h-3.5 w-3.5 text-accent" aria-hidden="true" />
                  <span>Audience Alignment</span>
                </h5>
                <p className="text-[11px] text-text-muted leading-relaxed">
                  Identify customers whose purchasing profile aligns with available inventory before dispatching sales teams.
                </p>
              </div>
              <div className="rounded-lg border border-border/60 bg-surface-secondary/40 p-3 space-y-1">
                <h5 className="font-semibold text-text-primary flex items-center gap-1.5">
                  <TrendingUp className="h-3.5 w-3.5 text-status-success" aria-hidden="true" />
                  <span>Targeted Outreach</span>
                </h5>
                <p className="text-[11px] text-text-muted leading-relaxed">
                  Use segment membership to prioritize relevant customer groups and direct suitable marketing collateral.
                </p>
              </div>
              <div className="rounded-lg border border-border/60 bg-surface-secondary/40 p-3 space-y-1">
                <h5 className="font-semibold text-text-primary flex items-center gap-1.5">
                  <Layers className="h-3.5 w-3.5 text-status-warning" aria-hidden="true" />
                  <span>Capital Efficiency</span>
                </h5>
                <p className="text-[11px] text-text-muted leading-relaxed">
                  Match customer budget ranges with appropriate inventory tiers to prevent high-friction marketing.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="lg:col-span-5 space-y-4">
          <Card className="border-border bg-surface-primary">
            <CardHeader className="pb-3 border-b border-border/60">
              <div className="flex items-center justify-between">
                <CardTitle className="text-sm font-bold">Assigned Segment & Intelligence</CardTitle>
                <Badge variant={result ? "success" : "outline"} className="text-[10px]">
                  {result ? "Live Model Inference" : "Awaiting Execution"}
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-4 pt-4">
              <div className="rounded-lg border border-accent/40 bg-accent/10 p-4">
                <p className="text-[10px] uppercase tracking-wider text-text-muted">Live Inference Result</p>
                <div className="mt-1 flex items-baseline justify-between">
                  <h4 className="text-lg font-bold text-text-primary">{activeProfile.title}</h4>
                  <Badge variant="info" className="font-mono text-xs">
                    Cluster {activeProfile.clusterId}
                  </Badge>
                </div>
                <p className="mt-2 text-xs text-text-secondary leading-relaxed">
                  {activeProfile.description}
                </p>
              </div>

              <div className="rounded-lg border border-border bg-surface-secondary/60 p-3.5 space-y-2.5 text-xs">
                <div className="flex items-center justify-between border-b border-border/50 pb-2">
                  <span className="text-text-muted">Portfolio Share:</span>
                  <span className="font-bold text-text-primary">
                    {activeProfile.sharePct}% ({formatNumber(activeProfile.populationCount)} profiles)
                  </span>
                </div>
                <div className="flex items-center justify-between border-b border-border/50 pb-2">
                  <span className="text-text-muted">Dominant Customer Type:</span>
                  <span className="font-semibold text-text-primary">{activeProfile.dominantType}</span>
                </div>
                <div className="flex items-center justify-between border-b border-border/50 pb-2">
                  <span className="text-text-muted">Dominant Customer Tier:</span>
                  <span className="font-semibold text-text-primary">{activeProfile.dominantTier}</span>
                </div>
                <div className="flex items-center justify-between border-b border-border/50 pb-2">
                  <span className="text-text-muted">Average Max Budget:</span>
                  <span className="font-mono font-bold text-accent">{formatEGP(activeProfile.avgMaxBudget)}</span>
                </div>
                <div className="flex items-center justify-between border-b border-border/50 pb-2">
                  <span className="text-text-muted">Average Monthly Income:</span>
                  <span className="font-mono font-bold text-text-primary">{formatEGP(activeProfile.avgIncome)}</span>
                </div>
                <div className="pt-1">
                  <span className="text-text-muted block mb-1">Primary Commercial Context:</span>
                  <p className="text-[11px] text-text-secondary bg-surface-primary/80 p-2.5 rounded border border-border/70">
                    {activeProfile.commercialContext}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-border bg-surface-primary p-3.5 space-y-2">
            <h5 className="text-xs font-semibold text-text-primary flex items-center gap-1.5">
              <ShieldCheck className="h-4 w-4 text-status-success" aria-hidden="true" />
              <span>Model Technical Specifications</span>
            </h5>
            <div className="divide-y divide-border/60 text-xs">
              <div className="flex justify-between py-1.5">
                <span className="text-text-muted">Model ID</span>
                <span className="font-mono text-accent">customer_kmeans_v1</span>
              </div>
              <div className="flex justify-between py-1.5">
                <span className="text-text-muted">Algorithm</span>
                <span>K-Means Clustering (K=4)</span>
              </div>
              <div className="flex justify-between py-1.5">
                <span className="text-text-muted">Task Type</span>
                <span>Unsupervised Behavioral Segmentation</span>
              </div>
              <div className="flex justify-between py-1.5">
                <span className="text-text-muted">Input Features</span>
                <span className="font-mono">16 numerical features</span>
              </div>
              <div className="flex justify-between py-1.5">
                <span className="text-text-muted">Active Clusters</span>
                <span className="font-mono text-status-success">4 Distinct Clusters</span>
              </div>
              <div className="flex justify-between py-1.5">
                <span className="text-text-muted">FastAPI Route</span>
                <span className="font-mono">POST /api/v1/ml/customer-segmentation</span>
              </div>
              <div className="flex justify-between py-1.5">
                <span className="text-text-muted">Validation</span>
                <span>Silhouette & Calinski-Harabasz Validated</span>
              </div>
            </div>
          </Card>
        </div>
      </div>

      <PotentialCustomersList clusterId={activeClusterId} clusterName={activeProfile.title} />
    </div>
  );
}
