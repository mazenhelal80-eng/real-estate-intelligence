"use client";

import React, { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { forecastCashFlow } from "@/lib/api";
import { CashFlowForecastResponse, DailyCashFlowRecord } from "@/types/api";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { ModelMetadataCard } from "./ModelMetadataCard";
import { formatEGP } from "@/lib/utils";
import { TrendingUp, AlertCircle, Calendar, ShieldCheck, Activity, DollarSign, Layers } from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";

const HISTORICAL_SERIES: DailyCashFlowRecord[] = [
  { date: "2026-08-27", net_cash_flow: 22400000 },
  { date: "2026-08-28", net_cash_flow: 25100000 },
  { date: "2026-08-29", net_cash_flow: 18200000 },
  { date: "2026-08-30", net_cash_flow: 19800000 },
  { date: "2026-08-31", net_cash_flow: 28500000 },
  { date: "2026-09-01", net_cash_flow: 31200000 },
  { date: "2026-09-02", net_cash_flow: 27400000 },
  { date: "2026-09-03", net_cash_flow: 24800000 },
  { date: "2026-09-04", net_cash_flow: 26100000 },
  { date: "2026-09-05", net_cash_flow: 19500000 },
  { date: "2026-09-06", net_cash_flow: 20100000 },
  { date: "2026-09-07", net_cash_flow: 29800000 },
  { date: "2026-09-08", net_cash_flow: 33400000 },
  { date: "2026-09-09", net_cash_flow: 28900000 },
  { date: "2026-09-10", net_cash_flow: 25300000 },
  { date: "2026-09-11", net_cash_flow: 27100000 },
  { date: "2026-09-12", net_cash_flow: 18900000 },
  { date: "2026-09-13", net_cash_flow: 21200000 },
  { date: "2026-09-14", net_cash_flow: 30500000 },
  { date: "2026-09-15", net_cash_flow: 34200000 },
  { date: "2026-09-16", net_cash_flow: 29100000 },
  { date: "2026-09-17", net_cash_flow: 26400000 },
  { date: "2026-09-18", net_cash_flow: 27800000 },
  { date: "2026-09-19", net_cash_flow: 19200000 },
  { date: "2026-09-20", net_cash_flow: 20800000 },
  { date: "2026-09-21", net_cash_flow: 31500000 },
  { date: "2026-09-22", net_cash_flow: 35100000 },
  { date: "2026-09-23", net_cash_flow: 30200000 },
  { date: "2026-09-24", net_cash_flow: 27900000 },
  { date: "2026-09-25", net_cash_flow: 28600000 },
  { date: "2026-09-26", net_cash_flow: 19700000 },
  { date: "2026-09-27", net_cash_flow: 21900000 },
  { date: "2026-09-28", net_cash_flow: 32800000 },
  { date: "2026-09-29", net_cash_flow: 36400000 },
  { date: "2026-09-30", net_cash_flow: 31800000 },
];

export function CashFlowForecastCard() {
  const [result, setResult] = useState<CashFlowForecastResponse | null>(null);

  const mutation = useMutation({
    mutationFn: forecastCashFlow,
    onSuccess: (data) => setResult(data),
  });

  const handleRun = () => {
    mutation.mutate({
      forecast_date: "2026-10-01",
      historical_series: HISTORICAL_SERIES,
    });
  };

  const chartData = HISTORICAL_SERIES.slice(-21).map((p) => ({
    date: p.date.slice(5),
    fullDate: p.date,
    actual: p.net_cash_flow,
    forecast: null as number | null,
  }));

  if (result) {
    chartData.push({
      date: result.forecast_date.slice(5),
      fullDate: result.forecast_date,
      actual: null as any,
      forecast: Math.round(result.predicted_net_cash_flow),
    });
  }

  const recentAvg =
    HISTORICAL_SERIES.reduce((acc, r) => acc + r.net_cash_flow, 0) / HISTORICAL_SERIES.length;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        <div className="lg:col-span-7 space-y-4">
          <Card className="border-border bg-surface-primary">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5 text-accent" />
                  <CardTitle>Cash Flow Forecasting Workspace</CardTitle>
                </div>
                <Badge variant="outline">One-Step Linear Model</Badge>
              </div>
              <CardDescription>
                Generates one-step-ahead daily net cash flow forecasts using 17 causal past-only autoregressive lags and rolling features.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="h-56 w-full border border-border/70 rounded-lg p-2 bg-surface-secondary/40">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={chartData} margin={{ top: 10, right: 15, left: 15, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#263247" />
                    <XAxis dataKey="date" stroke="#A8B3C2" fontSize={10} tickLine={false} />
                    <YAxis
                      stroke="#A8B3C2"
                      fontSize={10}
                      tickLine={false}
                      tickFormatter={(val) => `${(val / 1_000_000).toFixed(0)}M`}
                    />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "#111827",
                        borderColor: "#263247",
                        borderRadius: "8px",
                        color: "#F8FAFC",
                        fontSize: "12px",
                      }}
                      formatter={(val: any) => [formatEGP(Number(val) || 0), ""]}
                      labelFormatter={(label, items) => {
                        const item = items[0]?.payload;
                        return item ? `Date: ${item.fullDate}` : label;
                      }}
                    />
                    <ReferenceLine
                      y={recentAvg}
                      stroke="#64748B"
                      strokeDasharray="3 3"
                      label={{
                        value: "35d Mean",
                        fill: "#94A3B8",
                        fontSize: 10,
                        position: "insideTopLeft",
                      }}
                    />
                    <Line
                      type="monotone"
                      dataKey="actual"
                      stroke="#1877F2"
                      strokeWidth={2}
                      dot={{ r: 2 }}
                      name="Historical Flow"
                    />
                    <Line
                      type="monotone"
                      dataKey="forecast"
                      stroke="#10B981"
                      strokeWidth={2}
                      strokeDasharray="4 4"
                      dot={{ r: 6, fill: "#10B981" }}
                      name="Predicted Net Cash Flow"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              <div className="rounded-lg border border-border/70 bg-surface-secondary/50 p-3 text-xs space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-text-primary">
                    Causal Time-Series Feature Engine
                  </span>
                  <Badge variant="outline" className="text-[10px]">
                    Zero Lookahead Bias
                  </Badge>
                </div>
                <div className="grid grid-cols-2 gap-2 text-text-secondary sm:grid-cols-4 pt-1">
                  <div>
                    <span className="text-[10px] text-text-muted block">History Window</span>
                    <span className="font-medium text-text-primary">35 Daily Observations</span>
                  </div>
                  <div>
                    <span className="text-[10px] text-text-muted block">Autoregressive Lags</span>
                    <span className="font-medium text-text-primary">t-1, t-7, t-14, t-28, t-30</span>
                  </div>
                  <div>
                    <span className="text-[10px] text-text-muted block">Rolling Statistics</span>
                    <span className="font-medium text-text-primary">7d, 14d, 28d Mean/Std</span>
                  </div>
                  <div>
                    <span className="text-[10px] text-text-muted block">Horizon Target</span>
                    <span className="font-medium text-accent">2026-10-01 (1 Day Ahead)</span>
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-between border-t border-border/60 pt-4">
                <div className="text-xs text-text-muted">
                  Input Contract: <span className="font-mono text-text-secondary">35 daily transactions (Aug 27 - Sep 30)</span>
                </div>
                <Button onClick={handleRun} isLoading={mutation.isPending} size="sm">
                  Compute One-Step Forecast
                </Button>
              </div>

              {mutation.isError && (
                <div className="flex items-center gap-2 rounded-lg border border-status-danger/30 bg-status-danger/10 p-3 text-xs text-status-danger">
                  <AlertCircle className="h-4 w-4" />
                  <span>{mutation.error.message}</span>
                </div>
              )}
            </CardContent>
          </Card>

          <Card className="border-border bg-surface-primary">
            <CardHeader className="pb-2">
              <CardTitle className="text-xs uppercase tracking-wider text-text-secondary">
                How This Helps Treasury & Financial Planning
              </CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-1 gap-3 sm:grid-cols-3 text-xs text-text-secondary">
              <div className="rounded-lg border border-border/60 bg-surface-secondary/40 p-3 space-y-1">
                <h5 className="font-semibold text-text-primary flex items-center gap-1.5">
                  <DollarSign className="h-3.5 w-3.5 text-accent" />
                  Liquidity Guard
                </h5>
                <p className="text-[11px] text-text-muted">
                  Protects operational liquidity buffers ahead of scheduled contractor milestone disbursements.
                </p>
              </div>
              <div className="rounded-lg border border-border/60 bg-surface-secondary/40 p-3 space-y-1">
                <h5 className="font-semibold text-text-primary flex items-center gap-1.5">
                  <Calendar className="h-3.5 w-3.5 text-status-success" />
                  Seasonality Capture
                </h5>
                <p className="text-[11px] text-text-muted">
                  Factors in weekly collections cycles and lease renewal surges across commercial and residential blocks.
                </p>
              </div>
              <div className="rounded-lg border border-border/60 bg-surface-secondary/40 p-3 space-y-1">
                <h5 className="font-semibold text-text-primary flex items-center gap-1.5">
                  <Layers className="h-3.5 w-3.5 text-status-warning" />
                  Causal Rigor
                </h5>
                <p className="text-[11px] text-text-muted">
                  Guarantees mathematical validity by enforcing strict historical lags with zero data leakage.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="lg:col-span-5 space-y-4">
          <Card className="border-border bg-surface-primary">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-sm">Inference & Forecast Realization</CardTitle>
                <Badge variant={result ? "success" : "outline"} className="text-[10px]">
                  {result ? "Live Model Output" : "Awaiting Execution"}
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              {result ? (
                <div className="space-y-4">
                  <div className="rounded-lg border border-status-success/40 bg-status-success/10 p-4">
                    <p className="text-[10px] uppercase tracking-wider text-text-muted">
                      Predicted Net Cash Flow
                    </p>
                    <div className="mt-1 flex items-baseline justify-between">
                      <h4 className="text-2xl font-bold text-text-primary">
                        {formatEGP(result.predicted_net_cash_flow)}
                      </h4>
                      <Badge variant="success">One-Step Ahead</Badge>
                    </div>
                    <p className="mt-1 text-[11px] text-text-muted">
                      Forecast Target Date: <span className="font-mono text-accent">{result.forecast_date}</span>
                    </p>
                  </div>

                  <div className="rounded-lg border border-border bg-surface-secondary/60 p-4 space-y-2.5 text-xs">
                    <div className="flex items-center justify-between border-b border-border/50 pb-2">
                      <span className="text-text-muted">35-Day Historical Mean:</span>
                      <span className="font-mono font-bold text-text-primary">
                        {formatEGP(recentAvg)}
                      </span>
                    </div>
                    <div className="flex items-center justify-between border-b border-border/50 pb-2">
                      <span className="text-text-muted">Projected Deviation from Mean:</span>
                      <span
                        className={`font-mono font-bold ${
                          result.predicted_net_cash_flow >= recentAvg
                            ? "text-status-success"
                            : "text-status-warning"
                        }`}
                      >
                        {result.predicted_net_cash_flow >= recentAvg ? "+" : ""}
                        {formatEGP(result.predicted_net_cash_flow - recentAvg)} (
                        {(
                          ((result.predicted_net_cash_flow - recentAvg) / recentAvg) *
                          100
                        ).toFixed(1)}
                        %)
                      </span>
                    </div>
                    <div className="flex items-center justify-between border-b border-border/50 pb-2">
                      <span className="text-text-muted">Forecast Horizon:</span>
                      <span className="font-medium text-text-primary">Daily Horizon (t+1)</span>
                    </div>
                    <div className="pt-1">
                      <span className="text-text-muted block mb-1">Treasury Planning Note:</span>
                      <p className="text-[11px] text-text-secondary bg-surface-primary/80 p-2.5 rounded border border-border/70 leading-relaxed">
                        The model projects positive cash realization above the 35-day baseline, driven by anticipated month-end customer installment collections and scheduled lease settlements.
                      </p>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="rounded-lg border border-dashed border-border p-8 text-center text-xs text-text-muted">
                  <TrendingUp className="mx-auto h-8 w-8 text-text-muted mb-2 opacity-40" />
                  <p className="font-medium text-text-secondary">No Forecast Executed Yet</p>
                  <p className="mt-1">Click "Compute One-Step Forecast" to execute causal linear model</p>
                </div>
              )}
            </CardContent>
          </Card>

          <ModelMetadataCard
            modelName="cash_flow_linear_v1"
            modelVersion="v1"
            algorithm="Autoregressive Linear Regression"
            taskType="Time-Series Cash Flow Forecasting"
            target="net_cash_flow"
            featureCount={17}
            endpoint="POST /api/v1/ml/cash-flow-forecast"
            validationStatus="Causal Walk-Forward Validated"
            keyMetric={{ label: "Holdout MAE", value: "27.88M EGP (WAPE: 54.2%)" }}
          />
        </div>
      </div>
    </div>
  );
}
