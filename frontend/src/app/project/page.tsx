"use client";

import React from "react";
import { Shell } from "@/components/layout/Shell";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import {
  Database,
  LineChart,
  Binary,
  Package,
  Layers,
  Server,
  LayoutDashboard,
  CheckCircle2,
  ShieldCheck,
} from "lucide-react";

export default function ProjectPage() {
  const steps = [
    { title: "Phase 1: Data Foundation", desc: "13 relational schemas, raw immutable CSV storage, SHA-256 integrity validation.", icon: Database },
    { title: "Phase 2: Analytics & SQL", desc: "Dual reconciliation between DuckDB SQL & Pandas across 47 financial & operational KPIs.", icon: LineChart },
    { title: "Phase 3: Feature Engineering", desc: "Leakage-free transformers, target leakage barriers, and ML-ready matrices.", icon: Binary },
    { title: "Phase 4: ML Modeling Tracks", desc: "Regression, audited Classification (T=0.50), K-Means, Isolation Forest, Causal Time Series.", icon: Layers },
    { title: "Phase 5: Model Packaging", desc: "Joblib serialization, explicit metadata contracts, reproducible artifact directories.", icon: Package },
    { title: "Phase 6: ML Services Layer", desc: "In-memory artifact caching, contract validation, and clean Python inference functions.", icon: Server },
    { title: "Phase 7: FastAPI Integration", desc: "Pydantic v2 schemas, REST endpoints under /api/v1/ml/*, and interactive Swagger docs.", icon: Server },
    { title: "Phase 8: Frontend SaaS UI", desc: "Next.js App Router, TypeScript, Tailwind CSS, Recharts, and TanStack Query.", icon: LayoutDashboard },
  ];

  return (
    <Shell
      title="System Architecture & Engineering Lifecycle"
      subtitle="End-to-end Machine Learning and Decision Intelligence platform architecture"
    >
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>End-to-End Production Pipeline</CardTitle>
            <CardDescription>
              Architectural flow from raw data ingestion through machine learning serving to frontend presentation
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {steps.map((s, idx) => {
                const Icon = s.icon;
                return (
                  <div key={s.title} className="flex items-start gap-4 rounded-lg border border-border bg-surface-secondary/40 p-3.5">
                    <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-accent/15 text-accent">
                      <Icon className="h-4 w-4" />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <h4 className="text-xs font-semibold text-text-primary">{s.title}</h4>
                        <span className="text-[10px] font-mono text-text-muted">Step 0{idx + 1}</span>
                      </div>
                      <p className="mt-0.5 text-xs text-text-secondary">{s.desc}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>

        <div className="space-y-6">
          <Card className="border-accent/40 bg-surface-primary">
            <CardHeader>
              <div className="flex items-center gap-2">
                <ShieldCheck className="h-5 w-5 text-accent" />
                <CardTitle>Authorship & Engineering</CardTitle>
              </div>
              <CardDescription>Sole system designer & developer</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="rounded-lg border border-border bg-surface-secondary/70 p-4">
                <p className="text-xs uppercase tracking-wider text-text-muted">Built By</p>
                <h3 className="text-base font-bold text-text-primary mt-0.5">Mazen Helal</h3>
                <p className="text-xs font-medium text-accent">AI Engineer & Full-Stack AI Developer</p>
              </div>

              <div className="space-y-2 text-xs text-text-secondary">
                <div className="flex items-start gap-2">
                  <CheckCircle2 className="h-4 w-4 text-status-success shrink-0 mt-0.5" />
                  <span>Strict zero data-leakage boundaries on all feature engineering pipelines</span>
                </div>
                <div className="flex items-start gap-2">
                  <CheckCircle2 className="h-4 w-4 text-status-success shrink-0 mt-0.5" />
                  <span>Audited classification decision threshold frozen at 0.50 (OOF F1 maximized)</span>
                </div>
                <div className="flex items-start gap-2">
                  <CheckCircle2 className="h-4 w-4 text-status-success shrink-0 mt-0.5" />
                  <span>Strictly causal rolling features (past t-1 only) for cash flow forecasting</span>
                </div>
                <div className="flex items-start gap-2">
                  <CheckCircle2 className="h-4 w-4 text-status-success shrink-0 mt-0.5" />
                  <span>Dual data verification across DuckDB SQL and Pandas dataframes</span>
                </div>
                <div className="flex items-start gap-2">
                  <CheckCircle2 className="h-4 w-4 text-status-success shrink-0 mt-0.5" />
                  <span>41/41 automated tests covering analytics, packaging, services, and FastAPI</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Core Technology Stack</CardTitle>
              <CardDescription>Production-grade tools powering the engine</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {[
                  "Python 3.14",
                  "Scikit-Learn 1.9",
                  "Pandas 3.0",
                  "DuckDB",
                  "FastAPI",
                  "Pydantic v2",
                  "Uvicorn",
                  "Joblib",
                  "Next.js 15",
                  "React 19",
                  "TypeScript",
                  "Tailwind CSS",
                  "Recharts",
                  "TanStack Query",
                  "Lucide React",
                ].map((tech) => (
                  <Badge key={tech} variant="outline" className="text-xs">
                    {tech}
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </Shell>
  );
}
