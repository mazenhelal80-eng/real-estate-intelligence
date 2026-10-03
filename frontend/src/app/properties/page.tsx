"use client";

import React, { useState } from "react";
import { Shell } from "@/components/layout/Shell";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { SAMPLE_REAL_PROPERTIES } from "@/lib/verified_data";
import { PropertyRecord } from "@/types/analytics";
import { formatEGP, formatNumber } from "@/lib/utils";
import { predictPropertyPrice, detectPropertyAnomaly } from "@/lib/api";
import { PricePredictionRequest, PropertyAnomalyRequest } from "@/types/api";
import { Building2, Cpu, ShieldAlert, CheckCircle2, AlertCircle } from "lucide-react";

export default function PropertiesPage() {
  const [selectedType, setSelectedType] = useState<string>("All");
  const [activeUnit, setActiveUnit] = useState<PropertyRecord | null>(null);
  const [intelLoading, setIntelLoading] = useState<boolean>(false);
  const [priceResult, setPriceResult] = useState<{ predicted: number; model: string } | null>(null);
  const [anomalyResult, setAnomalyResult] = useState<{ flag: number; score: number } | null>(null);
  const [intelError, setIntelError] = useState<string | null>(null);

  const filteredProperties = SAMPLE_REAL_PROPERTIES.filter((p) =>
    selectedType === "All" ? true : p.property_type === selectedType
  );

  const runIntelligence = async (unit: PropertyRecord) => {
    setActiveUnit(unit);
    setIntelLoading(true);
    setIntelError(null);
    setPriceResult(null);
    setAnomalyResult(null);

    const pricePayload: PricePredictionRequest = {
      area_sqm: unit.area_sqm,
      bedrooms: unit.bedrooms,
      bathrooms: unit.bathrooms,
      floor_number: unit.floor_number,
      property_age: 1,
      room_density: unit.bedrooms / unit.area_sqm,
      popularity_score: unit.popularity_score,
      property_type_Apartment: unit.property_type === "Apartment" ? 1 : 0,
      property_type_Chalet: unit.property_type === "Chalet" ? 1 : 0,
      property_type_Office: 0,
      property_type_Retail: 0,
      property_type_Townhouse: unit.property_type === "Townhouse" ? 1 : 0,
      property_type_Villa: unit.property_type === "Villa" ? 1 : 0,
      "finishing_type_Core & Shell": unit.finishing_type === "Core & Shell" ? 1 : 0,
      "finishing_type_Fully Finished": unit.finishing_type === "Fully Finished" ? 1 : 0,
      "finishing_type_Semi Finished": unit.finishing_type === "Semi Finished" ? 1 : 0,
      "finishing_type_Ultra Super Lux": unit.finishing_type === "Ultra Super Lux" ? 1 : 0,
      "location_6th of October": unit.location === "6th of October" ? 1 : 0,
      location_Alexandria: unit.location === "Alexandria" ? 1 : 0,
      "location_El Shorouk": unit.location === "El Shorouk" ? 1 : 0,
      location_Maadi: unit.location === "Maadi" ? 1 : 0,
      location_Mansoura: 0,
      "location_Nasr City": 0,
      "location_New Cairo": unit.location === "New Cairo" ? 1 : 0,
      "location_New Capital": unit.location === "New Capital" ? 1 : 0,
      location_Obour: 0,
      "location_Sheikh Zayed": unit.location === "Sheikh Zayed" ? 1 : 0,
      "developer_name_Emaar Misr Prime": unit.developer_name.includes("Emaar") ? 1 : 0,
      "developer_name_Hassan Allam Properties": unit.developer_name.includes("Hassan Allam") ? 1 : 0,
      "developer_name_Misr Italia Urban": unit.developer_name.includes("Misr Italia") ? 1 : 0,
      "developer_name_Mountain View East": unit.developer_name.includes("Mountain View") ? 1 : 0,
      "developer_name_Orascom Development": unit.developer_name.includes("Orascom") ? 1 : 0,
      "developer_name_Palm Hills Legacy": unit.developer_name.includes("Palm Hills") ? 1 : 0,
      "developer_name_Sodic Prestige": unit.developer_name.includes("Sodic") ? 1 : 0,
      "developer_name_Talaat Moustafa Group": unit.developer_name.includes("Talaat Moustafa") ? 1 : 0,
      construction_status_Planning: unit.construction_status === "Planning" ? 1 : 0,
      "construction_status_Under Construction": unit.construction_status === "Under Construction" ? 1 : 0,
    };

    const anomalyPayload: PropertyAnomalyRequest = {
      area_sqm: unit.area_sqm,
      bedrooms: unit.bedrooms,
      bathrooms: unit.bathrooms,
      floor_number: unit.floor_number,
      base_price_egp: unit.base_price_egp,
      expected_rent_monthly_egp: unit.expected_rent_monthly_egp,
      price_per_sqm: unit.base_price_egp / unit.area_sqm,
      property_age: 1,
      rental_yield: (unit.expected_rent_monthly_egp * 12) / unit.base_price_egp,
      room_density: unit.bedrooms / unit.area_sqm,
      popularity_score: unit.popularity_score,
    };

    try {
      const [priceRes, anomalyRes] = await Promise.all([
        predictPropertyPrice(pricePayload),
        detectPropertyAnomaly(anomalyPayload),
      ]);
      setPriceResult({ predicted: priceRes.predicted_price_egp, model: priceRes.model_name });
      setAnomalyResult({ flag: anomalyRes.anomaly_flag, score: anomalyRes.anomaly_score });
    } catch (err: any) {
      setIntelError(err.message || "Failed to execute ML services");
    } finally {
      setIntelLoading(false);
    }
  };

  return (
    <Shell
      title="Property Directory & Unit Intelligence"
      subtitle="Sample unit records connected directly to live regression and anomaly ML services"
    >
      <div className="flex flex-wrap items-center justify-between gap-2.5 rounded-lg border border-border/70 bg-surface-primary/80 px-3.5 py-2 text-xs">
        <div className="flex flex-wrap items-center gap-2">
          <Badge variant="outline" className="text-xs">
            Portfolio Sample: 6 Real Verified Units (from 5,000 Cataloged)
          </Badge>
          <Badge variant="info">Price Range: 4.65M – 33.32M EGP</Badge>
        </div>
        <span className="text-xs text-text-muted">
          5 Cities • 5 Institutional Developers • Direct FastAPI ML Link
        </span>
      </div>

      <div className="flex items-center justify-between border-b border-border/80 pb-2.5">
        <div className="flex items-center gap-2">
          <span className="text-xs text-text-secondary">Property Type:</span>
          {["All", "Apartment", "Townhouse", "Villa", "Chalet"].map((t) => (
            <button
              key={t}
              onClick={() => setSelectedType(t)}
              className={`rounded-md border px-2.5 py-1 text-xs transition-colors ${
                selectedType === t
                  ? "border-accent bg-accent/20 text-accent font-semibold"
                  : "border-border bg-surface-secondary text-text-secondary hover:text-text-primary"
              }`}
            >
              {t}
            </button>
          ))}
        </div>
        <Badge variant="outline" className="text-xs">
          Showing {filteredProperties.length} Verified Units
        </Badge>
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <div className="lg:col-span-2 space-y-3">
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            {filteredProperties.map((p) => {
              const isSelected = activeUnit?.unit_id === p.unit_id;
              const grossYield = ((p.expected_rent_monthly_egp * 12) / p.base_price_egp) * 100;
              return (
                <Card
                  key={p.unit_id}
                  variant="interactive"
                  className={`p-3.5 cursor-pointer transition-all ${
                    isSelected ? "border-accent ring-1 ring-accent" : ""
                  }`}
                  onClick={() => runIntelligence(p)}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-xs font-semibold text-accent">{p.unit_id}</span>
                    <div className="flex items-center gap-1.5">
                      <Badge variant="outline" className="text-[10px]">{p.property_type}</Badge>
                      <Badge variant="success" className="text-[10px]">{grossYield.toFixed(1)}% Yield</Badge>
                    </div>
                  </div>
                  <h4 className="mt-1.5 text-xs font-bold text-text-primary">{p.project_name}</h4>
                  <p className="text-[11px] text-text-secondary">{p.developer_name} • {p.location}</p>

                  <div className="mt-2 grid grid-cols-3 gap-2 border-t border-border/60 pt-2 text-[11px] text-text-secondary">
                    <div>
                      <span>Area:</span> <span className="font-medium text-text-primary">{p.area_sqm} m²</span>
                    </div>
                    <div>
                      <span>Rooms:</span> <span className="font-medium text-text-primary">{p.bedrooms}B/{p.bathrooms}Ba</span>
                    </div>
                    <div>
                      <span>Floor:</span> <span className="font-medium text-text-primary">{p.floor_number}</span>
                    </div>
                  </div>

                  <div className="mt-2 flex items-center justify-between border-t border-border/60 pt-2">
                    <div>
                      <p className="text-[10px] text-text-muted">Listed Base Price</p>
                      <p className="text-xs font-bold text-text-primary">{formatEGP(p.base_price_egp)}</p>
                    </div>
                    <Button
                      size="sm"
                      variant={isSelected ? "primary" : "secondary"}
                      className="h-7 text-xs px-2.5"
                      onClick={(e) => {
                        e.stopPropagation();
                        runIntelligence(p);
                      }}
                    >
                      Run Intelligence
                    </Button>
                  </div>
                </Card>
              );
            })}
          </div>
        </div>

        <div className="space-y-4">
          <Card className="sticky top-20 border-border bg-surface-primary">
            <CardHeader>
              <div className="flex items-center gap-2">
                <Cpu className="h-5 w-5 text-accent" />
                <CardTitle>Unit Intelligence Engine</CardTitle>
              </div>
              <CardDescription>
                Live dual evaluation: Validated Random Forest Regression + Isolation Forest Anomaly Detection
              </CardDescription>
            </CardHeader>
            <CardContent>
              {activeUnit ? (
                <div className="space-y-4">
                  <div className="rounded-lg border border-border bg-surface-secondary/70 p-3">
                    <div className="flex items-center justify-between">
                      <span className="font-mono text-xs font-bold text-accent">{activeUnit.unit_id}</span>
                      <Badge variant="outline">{activeUnit.finishing_type}</Badge>
                    </div>
                    <p className="mt-1 text-xs font-semibold text-text-primary">{activeUnit.project_name}</p>
                    <p className="text-[11px] text-text-secondary">{activeUnit.developer_name} • {activeUnit.location}</p>
                    <div className="mt-2 text-xs">
                      <span className="text-text-muted">List Price: </span>
                      <span className="font-bold text-text-primary">{formatEGP(activeUnit.base_price_egp)}</span>
                    </div>
                  </div>

                  {intelLoading && (
                    <div className="flex items-center justify-center p-6 text-xs text-text-secondary">
                      <Cpu className="mr-2 h-4 w-4 animate-spin text-accent" />
                      <span>Querying FastAPI ML services...</span>
                    </div>
                  )}

                  {intelError && (
                    <div className="flex items-center gap-2 rounded-lg border border-status-danger/30 bg-status-danger/10 p-3 text-xs text-status-danger">
                      <AlertCircle className="h-4 w-4" />
                      <span>{intelError}</span>
                    </div>
                  )}

                  {priceResult && (
                    <div className="rounded-lg border border-accent/40 bg-accent/10 p-3.5 space-y-1">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-medium text-text-secondary">Predicted Valuation</span>
                        <Badge variant="info" className="text-[9px]">Validated Random Forest</Badge>
                      </div>
                      <p className="text-lg font-bold text-text-primary">
                        {formatEGP(priceResult.predicted)}
                      </p>
                      <div className="text-[11px] text-text-muted flex justify-between">
                        <span>List Variance:</span>
                        <span className="font-medium text-text-primary">
                          {((priceResult.predicted - activeUnit.base_price_egp) / activeUnit.base_price_egp * 100).toFixed(1)}%
                        </span>
                      </div>
                    </div>
                  )}

                  {anomalyResult && (
                    <div
                      className={`rounded-lg border p-3.5 space-y-1 ${
                        anomalyResult.flag === 1
                          ? "border-status-danger/40 bg-status-danger/10"
                          : "border-status-success/40 bg-status-success/10"
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-medium text-text-secondary">Anomaly Check</span>
                        <Badge variant={anomalyResult.flag === 1 ? "danger" : "success"} className="text-[9px]">
                          {anomalyResult.flag === 1 ? "Outlier (Flag 1)" : "Normal (Flag 0)"}
                        </Badge>
                      </div>
                      <p className="text-xs font-medium text-text-primary">
                        Isolation Forest Score: <span className="font-mono font-bold">{anomalyResult.score.toFixed(4)}</span>
                      </p>
                      <p className="text-[10px] text-text-muted">
                        {anomalyResult.flag === 1
                          ? "Valuation or physical density deviates significantly from compound peers"
                          : "Within normal expected parameter bounds for this asset cluster"}
                      </p>
                    </div>
                  )}
                </div>
              ) : (
                <div className="rounded-lg border border-dashed border-border p-8 text-center text-xs text-text-muted">
                  <Building2 className="mx-auto h-8 w-8 text-text-muted mb-2 opacity-50" />
                  <p className="font-medium text-text-secondary">No Unit Selected</p>
                  <p className="mt-1">Select any property record from the list to trigger live ML intelligence</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </Shell>
  );
}
