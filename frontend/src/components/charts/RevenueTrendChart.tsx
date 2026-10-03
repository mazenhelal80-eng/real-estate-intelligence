"use client";

import React from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { VERIFIED_MONTHLY_TREND } from "@/lib/verified_data";
import { formatEGP } from "@/lib/utils";

export function RevenueTrendChart() {
  const chartData = VERIFIED_MONTHLY_TREND.map((item) => ({
    month: item.month,
    revenue: item.total_revenue_egp,
    profit: item.net_profit_egp,
  }));

  return (
    <div className="h-56 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={chartData} margin={{ top: 10, right: 10, left: 10, bottom: 0 }}>
          <defs>
            <linearGradient id="revenueGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#1877F2" stopOpacity={0.4} />
              <stop offset="95%" stopColor="#1877F2" stopOpacity={0.0} />
            </linearGradient>
            <linearGradient id="profitGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#10B981" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#10B981" stopOpacity={0.0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#263247" />
          <XAxis dataKey="month" stroke="#A8B3C2" fontSize={11} tickLine={false} />
          <YAxis
            stroke="#A8B3C2"
            fontSize={11}
            tickLine={false}
            tickFormatter={(val) => `${(val / 1_000_000_000).toFixed(1)}B`}
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
          />
          <Area
            type="monotone"
            dataKey="revenue"
            stroke="#1877F2"
            strokeWidth={2}
            fillOpacity={1}
            fill="url(#revenueGrad)"
            name="Gross Inflow"
          />
          <Area
            type="monotone"
            dataKey="profit"
            stroke="#10B981"
            strokeWidth={2}
            fillOpacity={1}
            fill="url(#profitGrad)"
            name="Net Operating Profit"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
