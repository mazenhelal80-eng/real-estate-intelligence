"use client";

import React, { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { predictPropertyPrice } from "@/lib/api";
import { PricePredictionRequest, PricePredictionResponse } from "@/types/api";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { ModelMetadataCard } from "./ModelMetadataCard";
import { formatEGP, formatNumber } from "@/lib/utils";
import { VERIFIED_PROPERTY_TYPES, VERIFIED_LOCATIONS } from "@/lib/verified_data";
import { Cpu, AlertCircle, CheckCircle2, TrendingUp, DollarSign, Layers, ShieldCheck, Info, FileText, ArrowRight, BarChart3, HelpCircle } from "lucide-react";

interface PropertyPreset {
  name: string;
  unitId?: string;
  propertyType: string;
  location: string;
  developer: string;
  finishing: string;
  areaSqm: number;
  bedrooms: number;
  bathrooms: number;
  propertyAge: number;
  actualPrice?: number;
  features: PricePredictionRequest;
}

const PRESETS: Record<string, PropertyPreset> = {
  "UNT_0204 (Townhouse • New Cairo)": {
    name: "UNT_0204 (Townhouse • New Cairo)",
    unitId: "UNT_0204",
    propertyType: "Townhouse",
    location: "New Cairo",
    developer: "Orascom Development",
    finishing: "Ultra Super Lux",
    areaSqm: 301,
    bedrooms: 5,
    bathrooms: 4,
    propertyAge: 2,
    actualPrice: 23110000,
    features: {
      area_sqm: 1.567763894626136,
      bedrooms: 1.7399050674678171,
      bathrooms: 1.5733841878448185,
      floor_number: -1.0673164284656975,
      property_age: -0.121071241296858,
      room_density: 0.1646358414803494,
      popularity_score: 1.118533590848275,
      property_type_Apartment: 0,
      property_type_Chalet: 0,
      property_type_Office: 0,
      property_type_Retail: 0,
      property_type_Townhouse: 1,
      property_type_Villa: 0,
      "finishing_type_Core & Shell": 0,
      "finishing_type_Fully Finished": 0,
      "finishing_type_Semi Finished": 0,
      "finishing_type_Ultra Super Lux": 1,
      "location_6th of October": 0,
      location_Alexandria: 0,
      "location_El Shorouk": 0,
      location_Maadi: 0,
      location_Mansoura: 0,
      "location_Nasr City": 0,
      "location_New Cairo": 1,
      "location_New Capital": 0,
      location_Obour: 0,
      "location_Sheikh Zayed": 0,
      "developer_name_Emaar Misr Prime": 0,
      "developer_name_Hassan Allam Properties": 0,
      "developer_name_Misr Italia Urban": 0,
      "developer_name_Mountain View East": 0,
      "developer_name_Orascom Development": 1,
      "developer_name_Palm Hills Legacy": 0,
      "developer_name_Sodic Prestige": 0,
      "developer_name_Talaat Moustafa Group": 0,
      construction_status_Planning: 1,
      "construction_status_Under Construction": 0,
    },
  },
  "UNT_1752 (Villa • El Shorouk)": {
    name: "UNT_1752 (Villa • El Shorouk)",
    unitId: "UNT_1752",
    propertyType: "Villa",
    location: "El Shorouk",
    developer: "Emaar Misr Prime",
    finishing: "Ultra Super Lux",
    areaSqm: 327,
    bedrooms: 4,
    bathrooms: 5,
    propertyAge: 3,
    actualPrice: 13699000,
    features: {
      area_sqm: 1.8596894789181595,
      bedrooms: 1.1802251100998018,
      bathrooms: 2.463181551252039,
      floor_number: -1.0673164284656975,
      property_age: 0.7255807957441083,
      room_density: 0.0056325107106176,
      popularity_score: -1.214053012244942,
      property_type_Apartment: 0,
      property_type_Chalet: 0,
      property_type_Office: 0,
      property_type_Retail: 0,
      property_type_Townhouse: 0,
      property_type_Villa: 1,
      "finishing_type_Core & Shell": 0,
      "finishing_type_Fully Finished": 0,
      "finishing_type_Semi Finished": 0,
      "finishing_type_Ultra Super Lux": 1,
      "location_6th of October": 0,
      location_Alexandria: 0,
      "location_El Shorouk": 1,
      location_Maadi: 0,
      location_Mansoura: 0,
      "location_Nasr City": 0,
      "location_New Cairo": 0,
      "location_New Capital": 0,
      location_Obour: 0,
      "location_Sheikh Zayed": 0,
      "developer_name_Emaar Misr Prime": 1,
      "developer_name_Hassan Allam Properties": 0,
      "developer_name_Misr Italia Urban": 0,
      "developer_name_Mountain View East": 0,
      "developer_name_Orascom Development": 0,
      "developer_name_Palm Hills Legacy": 0,
      "developer_name_Sodic Prestige": 0,
      "developer_name_Talaat Moustafa Group": 0,
      construction_status_Planning: 0,
      "construction_status_Under Construction": 1,
    },
  },
  "UNT_0428 (Apartment • Nasr City)": {
    name: "UNT_0428 (Apartment • Nasr City)",
    unitId: "UNT_0428",
    propertyType: "Apartment",
    location: "Nasr City",
    developer: "Mountain View East",
    finishing: "Fully Finished",
    areaSqm: 126,
    bedrooms: 2,
    bathrooms: 2,
    propertyAge: 3,
    actualPrice: 5413000,
    features: {
      area_sqm: 0.1867313227831016,
      bedrooms: -0.4988147620042436,
      bathrooms: 0.6835868244375976,
      floor_number: 0.2046864657232358,
      property_age: 0.7255807957441083,
      room_density: -0.3322412056200153,
      popularity_score: -0.7766930241649644,
      property_type_Apartment: 1,
      property_type_Chalet: 0,
      property_type_Office: 0,
      property_type_Retail: 0,
      property_type_Townhouse: 0,
      property_type_Villa: 0,
      "finishing_type_Core & Shell": 0,
      "finishing_type_Fully Finished": 1,
      "finishing_type_Semi Finished": 0,
      "finishing_type_Ultra Super Lux": 0,
      "location_6th of October": 0,
      location_Alexandria: 0,
      "location_El Shorouk": 0,
      location_Maadi: 0,
      location_Mansoura: 0,
      "location_Nasr City": 1,
      "location_New Cairo": 0,
      "location_New Capital": 0,
      location_Obour: 0,
      "location_Sheikh Zayed": 0,
      "developer_name_Emaar Misr Prime": 0,
      "developer_name_Hassan Allam Properties": 0,
      "developer_name_Misr Italia Urban": 0,
      "developer_name_Mountain View East": 1,
      "developer_name_Orascom Development": 0,
      "developer_name_Palm Hills Legacy": 0,
      "developer_name_Sodic Prestige": 0,
      "developer_name_Talaat Moustafa Group": 0,
      construction_status_Planning: 0,
      "construction_status_Under Construction": 1,
    },
  },
  "Custom Valuation Scenario": {
    name: "Custom Valuation Scenario",
    propertyType: "Townhouse",
    location: "New Cairo",
    developer: "Orascom Development",
    finishing: "Fully Finished",
    areaSqm: 280,
    bedrooms: 4,
    bathrooms: 3,
    propertyAge: 1,
    features: {
      area_sqm: 1.25,
      bedrooms: 1.18,
      bathrooms: 0.68,
      floor_number: -1.06,
      property_age: -0.96,
      room_density: 0.12,
      popularity_score: 0.85,
      property_type_Apartment: 0,
      property_type_Chalet: 0,
      property_type_Office: 0,
      property_type_Retail: 0,
      property_type_Townhouse: 1,
      property_type_Villa: 0,
      "finishing_type_Core & Shell": 0,
      "finishing_type_Fully Finished": 1,
      "finishing_type_Semi Finished": 0,
      "finishing_type_Ultra Super Lux": 0,
      "location_6th of October": 0,
      location_Alexandria: 0,
      "location_El Shorouk": 0,
      location_Maadi: 0,
      location_Mansoura: 0,
      "location_Nasr City": 0,
      "location_New Cairo": 1,
      "location_New Capital": 0,
      location_Obour: 0,
      "location_Sheikh Zayed": 0,
      "developer_name_Emaar Misr Prime": 0,
      "developer_name_Hassan Allam Properties": 0,
      "developer_name_Misr Italia Urban": 0,
      "developer_name_Mountain View East": 0,
      "developer_name_Orascom Development": 1,
      "developer_name_Palm Hills Legacy": 0,
      "developer_name_Sodic Prestige": 0,
      "developer_name_Talaat Moustafa Group": 0,
      construction_status_Planning: 1,
      "construction_status_Under Construction": 0,
    },
  },
};

export function PricePredictionCard() {
  const [selectedPresetName, setSelectedPresetName] = useState<string>("UNT_0204 (Townhouse • New Cairo)");
  const [formData, setFormData] = useState<PricePredictionRequest>(
    PRESETS["UNT_0204 (Townhouse • New Cairo)"].features
  );
  const [result, setResult] = useState<PricePredictionResponse | null>(null);

  const currentPreset = PRESETS[selectedPresetName];

  const typeStat = VERIFIED_PROPERTY_TYPES.find(
    (t) => t.property_type === currentPreset.propertyType
  ) || {
    property_type: currentPreset.propertyType,
    units_count: 0,
    avg_price_per_sqm: 0,
    avg_price_egp: 0,
  };

  const locationStat = VERIFIED_LOCATIONS.find(
    (l) => l.location === currentPreset.location
  ) || {
    location: currentPreset.location,
    revenue_egp: 0,
    deals_count: 0,
    avg_deal_price_egp: 0,
  };

  const mutation = useMutation({
    mutationFn: predictPropertyPrice,
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

  const actualPrice = currentPreset.actualPrice;
  const predictedPrice = result ? result.predicted_price_egp : null;
  const variance = actualPrice && predictedPrice ? predictedPrice - actualPrice : null;
  const variancePct = actualPrice && predictedPrice ? ((predictedPrice - actualPrice) / actualPrice) * 100 : null;

  const holdoutMae = 547300;
  const absVariance = variance !== null ? Math.abs(variance) : null;
  const maeMultiple = absVariance !== null ? (absVariance / holdoutMae).toFixed(2) : null;

  const maxComparisonVal = actualPrice && predictedPrice ? Math.max(actualPrice, predictedPrice) * 1.15 : 1;
  const actualBarWidth = actualPrice ? Math.min(100, Math.max(10, (actualPrice / maxComparisonVal) * 100)) : 0;
  const predictedBarWidth = predictedPrice ? Math.min(100, Math.max(10, (predictedPrice / maxComparisonVal) * 100)) : 0;

  const featureWeights = [
    { name: "Gross Area (area_sqm)", weight: 78.93, label: "78.9%", role: "Primary Value Driver" },
    { name: "Market Popularity Score", weight: 14.61, label: "14.6%", role: "Demand & Engagement" },
    { name: "Ultra Super Lux Finishing", weight: 1.05, label: "1.1%", role: "Finishing Premium" },
    { name: "Room Density (Beds / Area)", weight: 0.64, label: "0.6%", role: "Spatial Layout" },
    { name: "Floor Number", weight: 0.58, label: "0.6%", role: "Vertical Position" },
  ];

  return (
    <div className="space-y-5">
      <Card className="border-border bg-surface-primary p-4">
        <div className="flex flex-col gap-4">
          <div className="flex flex-wrap items-center justify-between gap-2 border-b border-border/70 pb-3">
            <div>
              <span className="text-xs font-semibold text-text-primary">Subject Property Selection:</span>
              <p className="text-[11px] text-text-muted">Select an audited benchmark listing or evaluate custom parameters</p>
            </div>
            <div className="flex flex-wrap gap-2">
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

          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 rounded-lg border border-border/70 bg-surface-secondary/50 p-3 text-xs">
            <div>
              <span className="text-[10px] uppercase text-text-muted block">Identifier & Type</span>
              <span className="font-semibold text-text-primary">{currentPreset.propertyType}</span>
              <p className="text-[11px] text-text-muted font-mono">{currentPreset.unitId || "Custom Model Scenario"}</p>
            </div>
            <div>
              <span className="text-[10px] uppercase text-text-muted block">Location Corridor</span>
              <span className="font-semibold text-text-primary">{currentPreset.location}</span>
              <p className="text-[11px] text-text-muted">{currentPreset.developer}</p>
            </div>
            <div>
              <span className="text-[10px] uppercase text-text-muted block">Area & Layout</span>
              <span className="font-semibold text-text-primary">{currentPreset.areaSqm} m²</span>
              <p className="text-[11px] text-text-muted">{currentPreset.bedrooms} Beds • {currentPreset.bathrooms} Baths</p>
            </div>
            <div>
              <span className="text-[10px] uppercase text-text-muted block">Finishing & Age</span>
              <span className="font-semibold text-text-primary">{currentPreset.finishing}</span>
              <p className="text-[11px] text-text-muted">Age: {currentPreset.propertyAge} years</p>
            </div>
          </div>

          <div className="flex flex-wrap items-center justify-between gap-3 pt-1">
            <div className="flex items-center gap-2 text-xs text-text-secondary">
              <Badge variant="outline" className="font-mono text-[10px]">37 Input Features</Badge>
              <span>Standardized ML-ready input schema (track1_pricing_train)</span>
            </div>
            <Button onClick={handleRun} isLoading={mutation.isPending} size="sm" className="px-4">
              <Cpu className="mr-1.5 h-3.5 w-3.5" />
              Run Valuation Model
            </Button>
          </div>

          {mutation.isError && (
            <div className="flex items-center gap-2 rounded-lg border border-status-danger/30 bg-status-danger/10 p-3 text-xs text-status-danger">
              <AlertCircle className="h-4 w-4" />
              <span>{mutation.error.message}</span>
            </div>
          )}
        </div>
      </Card>

      <div className="grid grid-cols-1 gap-3.5 sm:grid-cols-2 lg:grid-cols-4">
        <Card className="p-3.5 border-l-2 border-l-accent">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-text-secondary">Estimated Market Value</span>
            <Badge variant="info">Model Output</Badge>
          </div>
          <div className="mt-1.5 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-text-primary tracking-tight">
              {predictedPrice ? formatEGP(predictedPrice) : "—"}
            </span>
          </div>
          <p className="mt-0.5 text-[11px] text-text-muted">
            {result ? "Random Forest live prediction" : "Awaiting valuation run"}
          </p>
        </Card>

        <Card className="p-3.5 border-l-2 border-l-border">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-text-secondary">Recorded Base Price</span>
            <Badge variant="outline">Verified Record</Badge>
          </div>
          <div className="mt-1.5 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-text-primary tracking-tight">
              {actualPrice ? formatEGP(actualPrice) : "N/A (Simulated)"}
            </span>
          </div>
          <p className="mt-0.5 text-[11px] text-text-muted">
            {actualPrice ? "Historical transaction baseline" : "Custom parameters scenario"}
          </p>
        </Card>

        <Card className="p-3.5 border-l-2 border-l-status-warning">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-text-secondary">Price Gap</span>
            <Badge variant="outline">Valuation Variance</Badge>
          </div>
          <div className="mt-1.5 flex items-baseline gap-2">
            <span className={`text-2xl font-bold tracking-tight ${variance !== null && variance < 0 ? "text-status-warning" : variance !== null && variance > 0 ? "text-accent" : "text-text-primary"}`}>
              {variance !== null ? `${variance >= 0 ? "+" : ""}${formatEGP(variance)}` : "—"}
            </span>
          </div>
          <p className="mt-0.5 text-[11px] text-text-muted">
            Difference: Estimated vs. Recorded
          </p>
        </Card>

        <Card className="p-3.5 border-l-2 border-l-status-success">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-text-secondary">Relative Gap</span>
            <Badge variant="outline">Percentage Spread</Badge>
          </div>
          <div className="mt-1.5 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-text-primary tracking-tight">
              {variancePct !== null ? `${variancePct >= 0 ? "+" : ""}${variancePct.toFixed(1)}%` : "—"}
            </span>
          </div>
          <p className="mt-0.5 text-[11px] text-text-muted">
            Relative deviation from listed price
          </p>
        </Card>
      </div>

      <Card className="p-4">
        <div className="mb-3 flex items-center justify-between border-b border-border/60 pb-2">
          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-text-primary">
              Price Comparison Visual
            </h4>
            <p className="text-[11px] text-text-muted">Direct horizontal scale comparison of listed price against model valuation</p>
          </div>
          <Badge variant="outline" className="text-[10px]">Comparative Scale</Badge>
        </div>

        {actualPrice && predictedPrice ? (
          <div className="space-y-3 pt-1">
            <div className="space-y-1">
              <div className="flex items-center justify-between text-xs">
                <span className="font-medium text-text-secondary">Recorded Base Price</span>
                <span className="font-mono font-bold text-text-primary">{formatEGP(actualPrice)}</span>
              </div>
              <div className="h-6 w-full rounded-md bg-surface-secondary/80 overflow-hidden p-0.5">
                <div
                  className="h-full rounded bg-slate-400/40 border border-slate-300/40 transition-all duration-500"
                  style={{ width: `${actualBarWidth}%` }}
                />
              </div>
            </div>

            <div className="space-y-1">
              <div className="flex items-center justify-between text-xs">
                <span className="font-medium text-accent">Model Estimated Value</span>
                <span className="font-mono font-bold text-accent">{formatEGP(predictedPrice)}</span>
              </div>
              <div className="h-6 w-full rounded-md bg-surface-secondary/80 overflow-hidden p-0.5">
                <div
                  className="h-full rounded bg-accent/40 border border-accent transition-all duration-500"
                  style={{ width: `${predictedBarWidth}%` }}
                />
              </div>
            </div>
          </div>
        ) : (
          <div className="py-6 text-center text-xs text-text-muted">
            Execute a valuation run on a verified property benchmark to view the visual comparison scale.
          </div>
        )}
      </Card>

      <Card className="p-4">
        <div className="mb-2 flex items-center justify-between">
          <h4 className="text-xs font-semibold uppercase tracking-wider text-text-primary">
            Valuation Interpretation & Context
          </h4>
          <Badge variant="outline" className="text-[10px]">Statistical Assessment</Badge>
        </div>

        {actualPrice && predictedPrice && variance !== null && absVariance !== null ? (
          <div className="space-y-2 text-xs text-text-secondary leading-relaxed">
            <p className="bg-surface-secondary/50 p-3 rounded-lg border border-border/70">
              The recorded price of <span className="font-bold text-text-primary">{formatEGP(actualPrice)}</span> is{" "}
              <span className="font-bold text-text-primary">{Math.abs(Number(variancePct)).toFixed(1)}%</span>{" "}
              {variance < 0 ? "above" : "below"} the model's estimated fair valuation of{" "}
              <span className="font-bold text-text-primary">{formatEGP(predictedPrice)}</span>.
            </p>
            <div className="grid grid-cols-1 gap-2.5 sm:grid-cols-2 pt-1">
              <div className="rounded border border-border/60 bg-surface-secondary/30 p-2.5 space-y-1">
                <span className="font-semibold text-text-primary block">MAE Benchmark Context</span>
                <p className="text-[11px] text-text-muted">
                  Holdout MAE: <span className="font-mono text-text-secondary font-semibold">547.3K EGP</span>. The observed valuation gap of {formatEGP(absVariance)} represents approximately{" "}
                  <span className="font-mono font-bold text-text-primary">{maeMultiple}×</span> the model's holdout Mean Absolute Error.
                </p>
              </div>
              <div className="rounded border border-border/60 bg-surface-secondary/30 p-2.5 space-y-1">
                <span className="font-semibold text-text-primary block">Analytical Takeaway</span>
                <p className="text-[11px] text-text-muted">
                  {Number(maeMultiple) <= 1.0
                    ? "The observed variance falls within the model's baseline evaluation error margin, indicating strong algorithmic alignment."
                    : "The observed variance exceeds the model's baseline average evaluation error, which indicates listing-specific features or micro-location factors requiring supplementary appraisal context."}
                </p>
              </div>
            </div>
          </div>
        ) : (
          <p className="text-xs text-text-muted">
            Run a property valuation to generate the quantitative interpretation and MAE multiple analysis.
          </p>
        )}
      </Card>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card className="p-4 space-y-3">
          <div className="flex items-center justify-between border-b border-border/60 pb-2">
            <div>
              <h4 className="text-xs font-semibold uppercase tracking-wider text-text-primary">
                Model Feature Influence
              </h4>
              <p className="text-[11px] text-text-muted">Verified feature contribution across training partition</p>
            </div>
            <Badge variant="outline" className="text-[10px]">Global Weights</Badge>
          </div>

          <div className="space-y-2">
            {featureWeights.map((f) => (
              <div key={f.name} className="space-y-1">
                <div className="flex items-center justify-between text-[11px]">
                  <span className="font-medium text-text-secondary">{f.name}</span>
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] text-text-muted">{f.role}</span>
                    <span className="font-mono font-semibold text-text-primary">{f.label}</span>
                  </div>
                </div>
                <div className="h-2 w-full rounded-full bg-surface-secondary overflow-hidden">
                  <div className="h-full rounded-full bg-accent/60" style={{ width: `${f.weight}%` }} />
                </div>
              </div>
            ))}
          </div>

          <div className="rounded border border-border/60 bg-surface-secondary/40 p-2.5 text-[11px] text-text-muted space-y-1">
            <span className="font-semibold text-text-secondary block">Model Explainability Status</span>
            <p>
              Feature-level local explanation (SHAP / TreeExplainer per individual prediction) is not currently exposed by this model endpoint. Displayed weights reflect verified global training set importances.
            </p>
          </div>
        </Card>

        <Card className="p-4 space-y-3">
          <div className="flex items-center justify-between border-b border-border/60 pb-2">
            <div>
              <h4 className="text-xs font-semibold uppercase tracking-wider text-text-primary">
                Comparable Market Context
              </h4>
              <p className="text-[11px] text-text-muted">Reconciled Phase 2 macroeconomic benchmarks</p>
            </div>
            <Badge variant="outline" className="text-[10px]">Verified Baseline</Badge>
          </div>

          <div className="space-y-2.5 text-xs">
            <div className="flex items-center justify-between border-b border-border/50 pb-2">
              <span className="text-text-secondary">Subject Property Listed Price</span>
              <span className="font-mono font-bold text-text-primary">
                {actualPrice ? formatEGP(actualPrice) : "N/A"}
              </span>
            </div>
            <div className="flex items-center justify-between border-b border-border/50 pb-2">
              <span className="text-text-secondary">Asset Class Benchmark ({typeStat.property_type})</span>
              <span className="font-mono font-semibold text-accent">
                {typeStat.avg_price_egp > 0 ? formatEGP(typeStat.avg_price_egp) : "—"}
              </span>
            </div>
            <div className="flex items-center justify-between border-b border-border/50 pb-2">
              <span className="text-text-secondary">Asset Class Price / m²</span>
              <span className="font-mono text-text-primary">
                {typeStat.avg_price_per_sqm > 0 ? `${formatEGP(typeStat.avg_price_per_sqm)} / m²` : "—"}
              </span>
            </div>
            <div className="flex items-center justify-between border-b border-border/50 pb-2">
              <span className="text-text-secondary">Corridor Average Deal ({locationStat.location})</span>
              <span className="font-mono text-text-primary">
                {locationStat.avg_deal_price_egp > 0 ? formatEGP(locationStat.avg_deal_price_egp) : "—"}
              </span>
            </div>
          </div>

          <div className="rounded border border-border/60 bg-surface-secondary/40 p-2.5 text-[11px] text-text-muted space-y-1">
            <span className="font-semibold text-text-secondary block">Micro-Comparable Scope</span>
            <p>
              Automated micro-radius property matching engine is not currently connected to the live prediction route. Macro benchmarks are derived from verified Phase 2 analytical checkpoints.
            </p>
          </div>
        </Card>
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card className="p-4 space-y-3">
          <div className="flex items-center justify-between border-b border-border/60 pb-2">
            <div>
              <h4 className="text-xs font-semibold uppercase tracking-wider text-text-primary">
                Model Reliability & Diagnostics
              </h4>
              <p className="text-[11px] text-text-muted">Holdout test set evaluation parameters</p>
            </div>
            <Badge variant="success" className="text-[10px]">R² = 0.9692</Badge>
          </div>

          <div className="grid grid-cols-2 gap-3 text-xs">
            <div className="rounded border border-border/60 bg-surface-secondary/40 p-2.5">
              <span className="text-[10px] uppercase text-text-muted block">Holdout R² Score</span>
              <span className="text-lg font-bold text-text-primary">0.9692</span>
              <p className="text-[10px] text-text-muted mt-0.5">Explains 96.9% of valuation variance on 1,000 holdout units</p>
            </div>
            <div className="rounded border border-border/60 bg-surface-secondary/40 p-2.5">
              <span className="text-[10px] uppercase text-text-muted block">Holdout MAE</span>
              <span className="text-lg font-bold text-accent">547.3K EGP</span>
              <p className="text-[10px] text-text-muted mt-0.5">Average absolute error across holdout evaluation set</p>
            </div>
            <div className="rounded border border-border/60 bg-surface-secondary/40 p-2.5">
              <span className="text-[10px] uppercase text-text-muted block">Algorithm</span>
              <span className="font-semibold text-text-primary">Random Forest</span>
              <p className="text-[10px] text-text-muted mt-0.5">100 estimators, random_state=42</p>
            </div>
            <div className="rounded border border-border/60 bg-surface-secondary/40 p-2.5">
              <span className="text-[10px] uppercase text-text-muted block">Feature Count</span>
              <span className="font-semibold text-text-primary">37 Features</span>
              <p className="text-[10px] text-text-muted mt-0.5">Physical, location, and developer one-hots</p>
            </div>
          </div>

          <p className="text-[11px] text-text-muted leading-relaxed">
            Prediction estimates individual fair market value, while Model Validation reflects statistical stability across 1,000 holdout units. R² does not guarantee zero error on every individual listing.
          </p>
        </Card>

        <Card className="p-4 space-y-3">
          <div className="flex items-center justify-between border-b border-border/60 pb-2">
            <div>
              <h4 className="text-xs font-semibold uppercase tracking-wider text-text-primary">
                Prediction Audit Trail
              </h4>
              <p className="text-[11px] text-text-muted">Stateless inference integrity parameters</p>
            </div>
            <Badge variant="outline" className="text-[10px]">Verified Lineage</Badge>
          </div>

          <div className="space-y-2 text-xs">
            <div className="flex items-center justify-between border-b border-border/50 pb-1.5">
              <span className="text-text-muted">Model ID:</span>
              <span className="font-mono font-semibold text-text-primary">property_price_rf_v1</span>
            </div>
            <div className="flex items-center justify-between border-b border-border/50 pb-1.5">
              <span className="text-text-muted">Task Type:</span>
              <span className="text-text-primary">Supervised Property Valuation</span>
            </div>
            <div className="flex items-center justify-between border-b border-border/50 pb-1.5">
              <span className="text-text-muted">Target Variable:</span>
              <span className="font-mono text-accent">target_base_price_egp</span>
            </div>
            <div className="flex items-center justify-between border-b border-border/50 pb-1.5">
              <span className="text-text-muted">Active Endpoint:</span>
              <span className="font-mono text-text-primary">POST /api/v1/ml/price-prediction</span>
            </div>
            <div className="flex items-center justify-between border-b border-border/50 pb-1.5">
              <span className="text-text-muted">Validation Status:</span>
              <Badge variant="success" className="text-[10px]">Holdout Test Validated</Badge>
            </div>
          </div>

          <p className="text-[11px] text-text-muted leading-relaxed">
            Dynamic prediction UUID and timestamp tracking are managed at the API gateway layer and not persisted by the stateless inference endpoint.
          </p>
        </Card>
      </div>

      <Card className="p-4 space-y-3">
        <div className="flex items-center justify-between border-b border-border/60 pb-2">
          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-text-primary">
              Model Technical Specifications
            </h4>
            <p className="text-[11px] text-text-muted">Audited contract parameters from metadata.json</p>
          </div>
          <Badge variant="outline" className="text-[10px]">Contract Reference</Badge>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-border text-text-muted">
                <th className="pb-1.5 font-medium">Specification</th>
                <th className="pb-1.5 font-medium">Value</th>
                <th className="pb-1.5 font-medium">Description</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/60 text-text-secondary">
              <tr className="hover:bg-surface-secondary/40">
                <td className="py-1.5 font-semibold text-text-primary">Algorithm</td>
                <td className="py-1.5 font-mono text-accent">RandomForestRegressor</td>
                <td className="py-1.5 text-text-muted">100 estimators, random_state=42 (scikit-learn 1.9.1)</td>
              </tr>
              <tr className="hover:bg-surface-secondary/40">
                <td className="py-1.5 font-semibold text-text-primary">Task Type</td>
                <td className="py-1.5">Regression</td>
                <td className="py-1.5 text-text-muted">Continuous valuation estimation in EGP</td>
              </tr>
              <tr className="hover:bg-surface-secondary/40">
                <td className="py-1.5 font-semibold text-text-primary">Target Variable</td>
                <td className="py-1.5 font-mono">target_base_price_egp</td>
                <td className="py-1.5 text-text-muted">Base property listed transaction value</td>
              </tr>
              <tr className="hover:bg-surface-secondary/40">
                <td className="py-1.5 font-semibold text-text-primary">Input Features</td>
                <td className="py-1.5 font-mono">37 Features</td>
                <td className="py-1.5 text-text-muted">7 continuous + 30 one-hot spatial & developer attributes</td>
              </tr>
              <tr className="hover:bg-surface-secondary/40">
                <td className="py-1.5 font-semibold text-text-primary">Model Version</td>
                <td className="py-1.5 font-mono">v1</td>
                <td className="py-1.5 text-text-muted">Production frozen weights serialized via joblib</td>
              </tr>
              <tr className="hover:bg-surface-secondary/40">
                <td className="py-1.5 font-semibold text-text-primary">Holdout MAE</td>
                <td className="py-1.5 font-mono text-accent">547,300 EGP</td>
                <td className="py-1.5 text-text-muted">Mean absolute prediction error on 1,000 unseen test units</td>
              </tr>
              <tr className="hover:bg-surface-secondary/40">
                <td className="py-1.5 font-semibold text-text-primary">Holdout R²</td>
                <td className="py-1.5 font-mono text-status-success">0.9692</td>
                <td className="py-1.5 text-text-muted">Coefficient of determination on test partition</td>
              </tr>
              <tr className="hover:bg-surface-secondary/40">
                <td className="py-1.5 font-semibold text-text-primary">FastAPI Route</td>
                <td className="py-1.5 font-mono text-text-primary">POST /api/v1/ml/price-prediction</td>
                <td className="py-1.5 text-text-muted">Stateless REST contract accepting PricePredictionRequest</td>
              </tr>
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
