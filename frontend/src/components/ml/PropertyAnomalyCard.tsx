"use client";

import React, { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { detectPropertyAnomaly } from "@/lib/api";
import { PropertyAnomalyRequest, PropertyAnomalyResponse } from "@/types/api";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { ModelMetadataCard } from "./ModelMetadataCard";
import { formatEGP } from "@/lib/utils";
import { ShieldAlert, AlertCircle, CheckCircle2, ShieldCheck, HelpCircle, Activity, Zap } from "lucide-react";

interface AnomalyPreset {
  name: string;
  category: string;
  expectedFlag: number;
  description: string;
  features: PropertyAnomalyRequest;
}

const PRESETS: Record<string, AnomalyPreset> = {
  "Standard Unit (Normal Inlier)": {
    name: "Standard Unit (Normal Inlier)",
    category: "Baseline Residential",
    expectedFlag: 0,
    description: "Typical Cairo residential unit with standard price per sqm (60,190 EGP) and 9.8% rental yield.",
    features: {
      area_sqm: 168,
      bedrooms: 4,
      bathrooms: 2,
      floor_number: 7,
      base_price_egp: 10112000,
      expected_rent_monthly_egp: 83100,
      price_per_sqm: 60190,
      property_age: 0,
      rental_yield: 0.098,
      room_density: 0.035,
      popularity_score: 9.26,
    },
  },
  "Luxury Outlier (UNT_0059)": {
    name: "Luxury Outlier (UNT_0059)",
    category: "Extreme Valuation",
    expectedFlag: 1,
    description: "High-valuation villa with 33.3M EGP valuation and 94,925 EGP/m², exhibiting features evaluated as an outlier by the model.",
    features: {
      area_sqm: 351,
      bedrooms: 5,
      bathrooms: 4,
      floor_number: 0,
      base_price_egp: 33319000,
      expected_rent_monthly_egp: 240000,
      price_per_sqm: 94925,
      property_age: 1,
      rental_yield: 0.086,
      room_density: 0.025,
      popularity_score: 9.39,
    },
  },
  "Mismatched Yield Anomaly": {
    name: "Mismatched Yield Anomaly",
    category: "Distorted Metrics",
    expectedFlag: 1,
    description: "Property profile with 5M EGP base price and 350K monthly rent (84% rental yield), presenting an unusual feature pattern relative to typical distributions.",
    features: {
      area_sqm: 500,
      bedrooms: 7,
      bathrooms: 6,
      floor_number: 0,
      base_price_egp: 5000000,
      expected_rent_monthly_egp: 350000,
      price_per_sqm: 10000,
      property_age: 0,
      rental_yield: 0.84,
      room_density: 0.014,
      popularity_score: 9.5,
    },
  },
  "Custom Valuation Spec": {
    name: "Custom Valuation Spec",
    category: "User Scenario",
    expectedFlag: 0,
    description: "Custom user-configurable property attributes for interactive sensitivity analysis.",
    features: {
      area_sqm: 200,
      bedrooms: 3,
      bathrooms: 2,
      floor_number: 3,
      base_price_egp: 12000000,
      expected_rent_monthly_egp: 95000,
      price_per_sqm: 60000,
      property_age: 1,
      rental_yield: 0.095,
      room_density: 0.025,
      popularity_score: 9.0,
    },
  },
};

export function PropertyAnomalyCard() {
  const [selectedPresetName, setSelectedPresetName] = useState<string>("Standard Unit (Normal Inlier)");
  const [formData, setFormData] = useState<PropertyAnomalyRequest>(
    PRESETS["Standard Unit (Normal Inlier)"].features
  );
  const [result, setResult] = useState<PropertyAnomalyResponse | null>(null);

  const currentPreset = PRESETS[selectedPresetName];

  const mutation = useMutation({
    mutationFn: detectPropertyAnomaly,
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

  const isAnomaly = result ? result.anomaly_flag === 1 : false;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        <div className="lg:col-span-7 space-y-4">
          <Card className="border-border bg-surface-primary">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <ShieldAlert className="h-5 w-5 text-accent" aria-hidden="true" />
                  <CardTitle>Property Anomaly Detection Workspace</CardTitle>
                </div>
                <Badge variant="outline">Isolation Forest (c=0.01)</Badge>
              </div>
              <CardDescription>
                Detects spatial, structural, and financial anomalies via scikit-learn Isolation Forest decision function.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <span className="text-xs text-text-secondary">Property Benchmark Preset:</span>
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
                  <Badge variant="outline" className="text-[10px]">
                    {currentPreset.category}
                  </Badge>
                </div>
                <p className="text-[11px] text-text-muted">
                  {currentPreset.description}
                </p>
              </div>

              <div className="grid grid-cols-2 gap-3 text-xs md:grid-cols-4">
                <div className="space-y-1">
                  <span className="text-text-secondary">Base Price (EGP)</span>
                  <input
                    type="number"
                    value={formData.base_price_egp}
                    onChange={(e) => setFormData({ ...formData, base_price_egp: Number(e.target.value) })}
                    className="w-full rounded border border-border bg-surface-secondary px-2.5 py-1.5 text-text-primary font-mono"
                  />
                </div>
                <div className="space-y-1">
                  <span className="text-text-secondary">Area (m²)</span>
                  <input
                    type="number"
                    value={formData.area_sqm}
                    onChange={(e) => setFormData({ ...formData, area_sqm: Number(e.target.value) })}
                    className="w-full rounded border border-border bg-surface-secondary px-2.5 py-1.5 text-text-primary font-mono"
                  />
                </div>
                <div className="space-y-1">
                  <span className="text-text-secondary">Price / m² (EGP)</span>
                  <input
                    type="number"
                    value={formData.price_per_sqm}
                    onChange={(e) => setFormData({ ...formData, price_per_sqm: Number(e.target.value) })}
                    className="w-full rounded border border-border bg-surface-secondary px-2.5 py-1.5 text-text-primary font-mono"
                  />
                </div>
                <div className="space-y-1">
                  <span className="text-text-secondary">Monthly Rent (EGP)</span>
                  <input
                    type="number"
                    value={formData.expected_rent_monthly_egp}
                    onChange={(e) =>
                      setFormData({ ...formData, expected_rent_monthly_egp: Number(e.target.value) })
                    }
                    className="w-full rounded border border-border bg-surface-secondary px-2.5 py-1.5 text-text-primary font-mono"
                  />
                </div>
              </div>

              <div className="flex items-center justify-between border-t border-border/60 pt-4">
                <div className="text-xs text-text-muted">
                  Mathematical Contract: <span className="font-mono text-text-secondary">0 = Normal • 1 = Anomaly</span>
                </div>
                <Button onClick={handleRun} isLoading={mutation.isPending} size="sm">
                  Run Anomaly Inspection
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
                  <ShieldCheck className="h-3.5 w-3.5 text-accent" aria-hidden="true" />
                  Pattern Detection
                </h5>
                <p className="text-[11px] text-text-muted">
                  Identifies property attribute combinations that deviate significantly from typical feature patterns.
                </p>
              </div>
              <div className="rounded-lg border border-border/60 bg-surface-secondary/40 p-3 space-y-1">
                <h5 className="font-semibold text-text-primary flex items-center gap-1.5">
                  <Activity className="h-3.5 w-3.5 text-status-success" aria-hidden="true" />
                  Outlier Identification
                </h5>
                <p className="text-[11px] text-text-muted">
                  Flags atypical unit feature patterns for manual valuation review.
                </p>
              </div>
              <div className="rounded-lg border border-border/60 bg-surface-secondary/40 p-3 space-y-1">
                <h5 className="font-semibold text-text-primary flex items-center gap-1.5">
                  <Zap className="h-3.5 w-3.5 text-status-warning" aria-hidden="true" />
                  Yield Comparison
                </h5>
                <p className="text-[11px] text-text-muted">
                  Highlights unusual price-to-area and rental yield relationships.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="lg:col-span-5 space-y-4">
          <Card className="border-border bg-surface-primary">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-sm">Inference & Anomaly Score</CardTitle>
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
                      isAnomaly
                        ? "border-status-danger/40 bg-status-danger/10"
                        : "border-status-success/40 bg-status-success/10"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-[10px] uppercase tracking-wider text-text-muted">
                          Evaluation Status
                        </p>
                        <h4 className="text-lg font-bold text-text-primary mt-0.5">
                          {isAnomaly ? "Statistical Anomaly (Outlier)" : "Normal Inlier"}
                        </h4>
                      </div>
                      <Badge variant={isAnomaly ? "danger" : "success"} className="gap-1">
                        {isAnomaly ? (
                          <AlertCircle className="h-3.5 w-3.5" aria-hidden="true" />
                        ) : (
                          <CheckCircle2 className="h-3.5 w-3.5" aria-hidden="true" />
                        )}
                        <span>Flag = {result.anomaly_flag}</span>
                      </Badge>
                    </div>

                    <div className="mt-3 flex items-baseline justify-between border-t border-border/50 pt-2 text-xs">
                      <span className="text-text-muted">Isolation Forest Score:</span>
                      <span
                        className={`font-mono font-bold text-sm ${
                          isAnomaly ? "text-status-danger" : "text-status-success"
                        }`}
                      >
                        {result.anomaly_score >= 0 ? "+" : ""}
                        {result.anomaly_score.toFixed(4)}
                      </span>
                    </div>
                  </div>

                  <div className="rounded-lg border border-border bg-surface-secondary/60 p-4 space-y-2.5 text-xs">
                    <div className="flex items-center justify-between border-b border-border/50 pb-2">
                      <span className="text-text-muted">Decision Boundary:</span>
                      <span className="font-mono text-text-primary">Score &lt; 0 → Outlier (1)</span>
                    </div>
                    <div className="flex items-center justify-between border-b border-border/50 pb-2">
                      <span className="text-text-muted">Contamination Calibrated:</span>
                      <span className="font-mono font-bold text-text-primary">1.0% (c=0.01)</span>
                    </div>
                    <div className="flex items-center justify-between border-b border-border/50 pb-2">
                      <span className="text-text-muted">Sample Isolation Depth:</span>
                      <span className="font-semibold text-text-primary">
                        {isAnomaly ? "Shallow Tree Cut (Few Splits)" : "Deep Tree Cut (Nominal Cluster)"}
                      </span>
                    </div>
                    <div className="pt-1">
                      <span className="text-text-muted block mb-1">Model Interpretation:</span>
                      <p className="text-[11px] text-text-secondary bg-surface-primary/80 p-2.5 rounded border border-border/70 leading-relaxed">
                        {isAnomaly
                          ? "Statistical Anomaly Detected (Flag = 1). This property contains a feature pattern that is unusual relative to patterns observed by the model."
                          : "Normal Inlier (Flag = 0). The property's feature pattern is consistent with patterns observed by the model."}
                      </p>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="rounded-lg border border-dashed border-border p-8 text-center text-xs text-text-muted">
                  <ShieldAlert className="mx-auto h-8 w-8 text-text-muted mb-2 opacity-40" aria-hidden="true" />
                  <p className="font-medium text-text-secondary">No Scan Executed Yet</p>
                  <p className="mt-1">Click "Run Anomaly Inspection" to execute Isolation Forest</p>
                </div>
              )}
            </CardContent>
          </Card>

          <ModelMetadataCard
            modelName="property_anomaly_iforest_v1"
            modelVersion="v1"
            algorithm="Isolation Forest (100 Trees, c=0.01)"
            taskType="Unsupervised Anomaly Detection"
            featureCount={11}
            endpoint="POST /api/v1/ml/property-anomaly"
            validationStatus="Contamination Calibrated (0.01)"
            keyMetric={{ label: "Outlier Threshold", value: "Flag 1 if Score < 0" }}
          />
        </div>
      </div>
    </div>
  );
}
