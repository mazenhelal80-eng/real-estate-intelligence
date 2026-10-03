"use client";

import React, { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { predictLeadConversion } from "@/lib/api";
import { LeadConversionRequest, LeadConversionResponse } from "@/types/api";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { ModelMetadataCard } from "./ModelMetadataCard";
import { formatPercent, formatEGP } from "@/lib/utils";
import { Target, AlertCircle, CheckCircle2, TrendingUp, Users, Clock, ShieldCheck } from "lucide-react";

interface LeadPreset {
  name: string;
  leadScore: number;
  interactionCount: number;
  channel: string;
  tier: string;
  customerType: string;
  listingType: string;
  features: LeadConversionRequest;
}

const PRESETS: Record<string, LeadPreset> = {
  "High-Intent Qualified Lead (Score: 78.3)": {
    name: "High-Intent Qualified Lead (Score: 78.3)",
    leadScore: 78.3,
    interactionCount: 2,
    channel: "Walk-in",
    tier: "Silver",
    customerType: "End User",
    listingType: "Sale",
    features: {
      lead_score: 2.0538116591928253,
      interaction_count: 2.0,
      monthly_income_egp: -0.4875242201068537,
      budget_max_egp: -0.4633496179477073,
      budget_spread_egp: -0.2643676892680925,
      income_to_budget_ratio: -0.5093857407244206,
      listing_price_egp: 0.6836313795466594,
      "lead_source_Call Center": 0.0,
      lead_source_Facebook: 0.0,
      lead_source_Instagram: 0.0,
      "lead_source_Property Portal": 0.0,
      lead_source_Referral: 0.0,
      "lead_source_Walk-in": 1.0,
      lead_source_Website: 0.0,
      customer_type_Business: 0.0,
      "customer_type_End User": 1.0,
      customer_type_Investor: 0.0,
      customer_type_Landlord: 0.0,
      customer_tier_Bronze: 0.0,
      customer_tier_Gold: 0.0,
      customer_tier_Platinum: 0.0,
      customer_tier_Silver: 1.0,
      interaction_frequency_High: 1.0,
      interaction_frequency_Low: 0.0,
      interaction_frequency_Medium: 0.0,
      listing_type_Rent: 0.0,
      listing_type_Sale: 1.0,
    },
  },
  "Borderline Inactive Lead (Score: 49.7)": {
    name: "Borderline Inactive Lead (Score: 49.7)",
    leadScore: 49.7,
    interactionCount: 3,
    channel: "Walk-in",
    tier: "Silver",
    customerType: "End User",
    listingType: "Rent",
    features: {
      lead_score: 0.4798206278026907,
      interaction_count: 3.0,
      monthly_income_egp: -0.103148937206116,
      budget_max_egp: -0.5774103622286072,
      budget_spread_egp: -0.5057729260337448,
      income_to_budget_ratio: 0.5104432889750594,
      listing_price_egp: -0.5776277848895095,
      "lead_source_Call Center": 0.0,
      lead_source_Facebook: 0.0,
      lead_source_Instagram: 0.0,
      "lead_source_Property Portal": 0.0,
      lead_source_Referral: 0.0,
      "lead_source_Walk-in": 1.0,
      lead_source_Website: 0.0,
      customer_type_Business: 0.0,
      "customer_type_End User": 1.0,
      customer_type_Investor: 0.0,
      customer_type_Landlord: 0.0,
      customer_tier_Bronze: 0.0,
      customer_tier_Gold: 0.0,
      customer_tier_Platinum: 0.0,
      customer_tier_Silver: 1.0,
      interaction_frequency_High: 0.0,
      interaction_frequency_Low: 1.0,
      interaction_frequency_Medium: 0.0,
      listing_type_Rent: 1.0,
      listing_type_Sale: 0.0,
    },
  },
  "Cold Unqualified Lead (Score: 24.7)": {
    name: "Cold Unqualified Lead (Score: 24.7)",
    leadScore: 24.7,
    interactionCount: 1,
    channel: "Website",
    tier: "Bronze",
    customerType: "End User",
    listingType: "Sale",
    features: {
      lead_score: -0.9013452914798205,
      interaction_count: 1.0,
      monthly_income_egp: -0.4611995219500542,
      budget_max_egp: -0.8263151850082611,
      budget_spread_egp: -0.5928592388197464,
      income_to_budget_ratio: 0.0126905790076671,
      listing_price_egp: 1.04128683553797,
      "lead_source_Call Center": 0.0,
      lead_source_Facebook: 0.0,
      lead_source_Instagram: 0.0,
      "lead_source_Property Portal": 0.0,
      lead_source_Referral: 0.0,
      "lead_source_Walk-in": 0.0,
      lead_source_Website: 1.0,
      customer_type_Business: 0.0,
      "customer_type_End User": 1.0,
      customer_type_Investor: 0.0,
      customer_type_Landlord: 0.0,
      customer_tier_Bronze: 1.0,
      customer_tier_Gold: 0.0,
      customer_tier_Platinum: 0.0,
      customer_tier_Silver: 0.0,
      interaction_frequency_High: 0.0,
      interaction_frequency_Low: 0.0,
      interaction_frequency_Medium: 1.0,
      listing_type_Rent: 0.0,
      listing_type_Sale: 1.0,
    },
  },
  "Custom Scenario": {
    name: "Custom Scenario",
    leadScore: 65.0,
    interactionCount: 4,
    channel: "Property Portal",
    tier: "Gold",
    customerType: "End User",
    listingType: "Sale",
    features: {
      lead_score: 1.15,
      interaction_count: 4.0,
      monthly_income_egp: 0.25,
      budget_max_egp: 0.40,
      budget_spread_egp: 0.15,
      income_to_budget_ratio: 0.05,
      listing_price_egp: 0.35,
      "lead_source_Call Center": 0.0,
      lead_source_Facebook: 0.0,
      lead_source_Instagram: 0.0,
      "lead_source_Property Portal": 1.0,
      lead_source_Referral: 0.0,
      "lead_source_Walk-in": 0.0,
      lead_source_Website: 0.0,
      customer_type_Business: 0.0,
      "customer_type_End User": 1.0,
      customer_type_Investor: 0.0,
      customer_type_Landlord: 0.0,
      customer_tier_Bronze: 0.0,
      customer_tier_Gold: 1.0,
      customer_tier_Platinum: 0.0,
      customer_tier_Silver: 0.0,
      interaction_frequency_High: 1.0,
      interaction_frequency_Low: 0.0,
      interaction_frequency_Medium: 0.0,
      listing_type_Rent: 0.0,
      listing_type_Sale: 1.0,
    },
  },
};

export function LeadConversionCard() {
  const [selectedPresetName, setSelectedPresetName] = useState<string>(
    "High-Intent Qualified Lead (Score: 78.3)"
  );
  const [formData, setFormData] = useState<LeadConversionRequest>(
    PRESETS["High-Intent Qualified Lead (Score: 78.3)"].features
  );
  const [result, setResult] = useState<LeadConversionResponse | null>(null);

  const currentPreset = PRESETS[selectedPresetName];

  const mutation = useMutation({
    mutationFn: predictLeadConversion,
    onSuccess: (data) => setResult(data),
  });

  const handleSelectPreset = (name: string) => {
    setSelectedPresetName(name);
    setFormData(PRESETS[name].features);
    setResult(null);
  };

  const handleRun = () => {
    mutation.mutate(formData);
  };

  const probPercent = result ? Math.round(result.probability * 100) : 0;
  const isConverted = result ? result.prediction === 1 : false;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        <div className="lg:col-span-7 space-y-4">
          <Card className="border-border bg-surface-primary">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Target className="h-5 w-5 text-accent" aria-hidden="true" />
                  <CardTitle>Lead Conversion Probability Workspace</CardTitle>
                </div>
                <Badge variant="outline">Logistic Regression (C=10.0)</Badge>
              </div>
              <CardDescription>
                Calculates conversion probability against the frozen 0.50 threshold using 27 behavioral and demographic features.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <span className="text-xs text-text-secondary">Lead Archetype Preset:</span>
                <div className="mt-1.5 flex flex-wrap gap-2">
                  {Object.keys(PRESETS).map((name) => (
                    <button
                      key={name}
                      type="button"
                      onClick={() => handleSelectPreset(name)}
                      className={`rounded-md border px-2.5 py-1 text-xs transition-colors ${
                        selectedPresetName === name
                          ? "border-accent bg-accent/20 text-accent font-semibold"
                          : "border-border bg-surface-secondary text-text-secondary hover:text-text-primary"
                      }`}
                    >
                      {name}
                    </button>
                  ))}
                </div>
              </div>

              <div className="rounded-lg border border-border/70 bg-surface-secondary/50 p-3 text-xs space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-text-primary">
                    {currentPreset.name}
                  </span>
                  <Badge variant="outline" className="font-mono text-[10px]">
                    Lead Score: {currentPreset.leadScore} / 100
                  </Badge>
                </div>
                <div className="grid grid-cols-2 gap-2 text-text-secondary sm:grid-cols-4 pt-1">
                  <div>
                    <span className="text-[10px] text-text-muted block">Acquisition Source</span>
                    <span className="font-medium text-text-primary">{currentPreset.channel}</span>
                  </div>
                  <div>
                    <span className="text-[10px] text-text-muted block">Customer Tier</span>
                    <span className="font-medium text-text-primary">{currentPreset.tier}</span>
                  </div>
                  <div>
                    <span className="text-[10px] text-text-muted block">Customer Type</span>
                    <span className="font-medium text-text-primary">{currentPreset.customerType}</span>
                  </div>
                  <div>
                    <span className="text-[10px] text-text-muted block">Deal Focus</span>
                    <span className="font-medium text-text-primary">{currentPreset.listingType}</span>
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-between border-t border-border/60 pt-4">
                <div className="text-xs text-text-muted">
                  Decision Cutoff: <span className="font-mono text-text-secondary">P ≥ 0.50 → Converted</span>
                </div>
                <Button onClick={handleRun} isLoading={mutation.isPending} size="sm">
                  Evaluate Conversion Odds
                </Button>
              </div>

              {mutation.isError && (
                <div className="flex items-center gap-2 rounded-lg border border-status-danger/30 bg-status-danger/10 p-3 text-xs text-status-danger">
                  <AlertCircle className="h-4 w-4" aria-hidden="true" />
                  <span>{mutation.error.message}</span>
                </div>
              )}
            </CardContent>
          </Card>

          <Card className="border-border bg-surface-primary">
            <CardHeader className="pb-2">
              <CardTitle className="text-xs uppercase tracking-wider text-text-secondary">
                Model Evaluation Context
              </CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-1 gap-3 sm:grid-cols-3 text-xs text-text-secondary">
              <div className="rounded-lg border border-border/60 bg-surface-secondary/40 p-3 space-y-1">
                <h5 className="font-semibold text-text-primary flex items-center gap-1.5">
                  <Clock className="h-3.5 w-3.5 text-accent" aria-hidden="true" />
                  Conversion Propensity
                </h5>
                <p className="text-[11px] text-text-muted">
                  Quantifies lead conversion probability based on historical engagement patterns and buyer profile attributes.
                </p>
              </div>
              <div className="rounded-lg border border-border/60 bg-surface-secondary/40 p-3 space-y-1">
                <h5 className="font-semibold text-text-primary flex items-center gap-1.5">
                  <Users className="h-3.5 w-3.5 text-status-success" aria-hidden="true" />
                  Threshold Analysis
                </h5>
                <p className="text-[11px] text-text-muted">
                  Evaluates whether an inquiry meets the validated 0.50 probability cutoff for qualification.
                </p>
              </div>
              <div className="rounded-lg border border-border/60 bg-surface-secondary/40 p-3 space-y-1">
                <h5 className="font-semibold text-text-primary flex items-center gap-1.5">
                  <TrendingUp className="h-3.5 w-3.5 text-status-warning" aria-hidden="true" />
                  Pipeline Estimation
                </h5>
                <p className="text-[11px] text-text-muted">
                  Provides a statistical conversion likelihood score to support pipeline analysis.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="lg:col-span-5 space-y-4">
          <Card className="border-border bg-surface-primary">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-sm">Inference & Conversion Gauge</CardTitle>
                <Badge variant={result ? "success" : "outline"} className="text-[10px]">
                  {result ? "Live Model Output" : "Awaiting Execution"}
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              {result ? (
                <div className="space-y-4">
                  <div
                    className={`rounded-lg border p-4 ${
                      isConverted
                        ? "border-status-success/40 bg-status-success/10"
                        : "border-status-warning/40 bg-status-warning/10"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-[10px] uppercase tracking-wider text-text-muted">
                          Conversion Probability
                        </p>
                        <h4 className="text-2xl font-bold text-text-primary mt-0.5">
                          {formatPercent(result.probability)}
                        </h4>
                      </div>
                      <Badge variant={isConverted ? "success" : "warning"} className="gap-1">
                        {isConverted ? (
                          <CheckCircle2 className="h-3.5 w-3.5" aria-hidden="true" />
                        ) : (
                          <AlertCircle className="h-3.5 w-3.5" aria-hidden="true" />
                        )}
                        <span>{result.class_label}</span>
                      </Badge>
                    </div>

                    <div className="mt-4 space-y-1.5">
                      <div className="flex justify-between text-[11px] text-text-secondary">
                        <span>0%</span>
                        <span className="font-medium text-text-primary">
                          Cutoff: {formatPercent(result.threshold)}
                        </span>
                        <span>100%</span>
                      </div>
                      <div className="relative h-3 w-full overflow-hidden rounded-full bg-surface-secondary">
                        <div
                          className={`h-full transition-all duration-500 ${
                            isConverted ? "bg-status-success" : "bg-status-warning"
                          }`}
                          style={{ width: `${Math.min(100, Math.max(0, probPercent))}%` }}
                        />
                        <div
                          className="absolute top-0 bottom-0 w-0.5 bg-text-primary/70 z-10"
                          style={{ left: "50%" }}
                        />
                      </div>
                    </div>
                  </div>

                  <div className="rounded-lg border border-border bg-surface-secondary/60 p-4 space-y-2.5 text-xs">
                    <div className="flex items-center justify-between border-b border-border/50 pb-2">
                      <span className="text-text-muted">Decision Threshold:</span>
                      <span className="font-mono font-bold text-text-primary">0.50 (Frozen)</span>
                    </div>
                    <div className="flex items-center justify-between border-b border-border/50 pb-2">
                      <span className="text-text-muted">Predicted Classification:</span>
                      <span className="font-mono font-bold text-text-primary">
                        {result.prediction} ({result.class_label})
                      </span>
                    </div>
                    <div className="flex items-center justify-between border-b border-border/50 pb-2">
                      <span className="text-text-muted">Propensity Tier:</span>
                      <span className="font-semibold text-text-primary">
                        {result.probability >= 0.7
                          ? "Tier 1 — High Velocity"
                          : result.probability >= 0.5
                          ? "Tier 2 — Qualified Standard"
                          : result.probability >= 0.35
                          ? "Tier 3 — Borderline Nurture"
                          : "Tier 4 — Unqualified Cold"}
                      </span>
                    </div>
                    <div className="pt-1">
                      <span className="text-text-muted block mb-1">Model Interpretation:</span>
                      <p className="text-[11px] text-text-secondary bg-surface-primary/80 p-2.5 rounded border border-border/70 leading-relaxed">
                        {isConverted
                          ? "Predicted conversion probability meets or exceeds the 0.50 threshold, classifying this profile as Converted (Class 1) based on model criteria."
                          : "Predicted conversion probability sits below the 0.50 threshold, classifying this profile as Not Converted (Class 0) based on model criteria."}
                      </p>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="rounded-lg border border-dashed border-border p-8 text-center text-xs text-text-muted">
                  <Target className="mx-auto h-8 w-8 text-text-muted mb-2 opacity-40" aria-hidden="true" />
                  <p className="font-medium text-text-secondary">No Evaluation Run Yet</p>
                  <p className="mt-1">Click "Evaluate Conversion Odds" to execute logistic model</p>
                </div>
              )}
            </CardContent>
          </Card>

          <ModelMetadataCard
            modelName="lead_conversion_lr_v1"
            modelVersion="v1"
            algorithm="Regularized Logistic Regression (C=10.0)"
            taskType="Supervised Binary Classification"
            target="target_is_converted"
            featureCount={27}
            endpoint="POST /api/v1/ml/lead-conversion"
            validationStatus="Balanced Class Weights Validated"
            keyMetric={{ label: "Holdout Recall", value: "49.9% (PR-AUC: 0.181)" }}
          />
        </div>
      </div>
    </div>
  );
}
