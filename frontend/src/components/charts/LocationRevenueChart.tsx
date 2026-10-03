"use client";

import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { VERIFIED_LOCATIONS } from "@/lib/verified_data";
import { formatEGP } from "@/lib/utils";

export function LocationRevenueChart() {
  const chartData = VERIFIED_LOCATIONS.slice(0, 7).map((loc) => ({
    location: loc.location,
    revenue: loc.revenue_egp,
    deals: loc.deals_count,
  }));

  return (
    <div className="h-52 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={chartData}
          layout="vertical"
          margin={{ top: 5, right: 20, left: 40, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#263247" horizontal={false} />
          <XAxis
            type="number"
            stroke="#A8B3C2"
            fontSize={10}
            tickFormatter={(val) => `${(val / 1_000_000_000).toFixed(1)}B`}
          />
          <YAxis dataKey="location" type="category" stroke="#A8B3C2" fontSize={11} tickLine={false} />
          <Tooltip
            contentStyle={{
              backgroundColor: "#111827",
              borderColor: "#263247",
              borderRadius: "8px",
              color: "#F8FAFC",
              fontSize: "12px",
            }}
            formatter={(val: any) => [formatEGP(Number(val) || 0), "Revenue"]}
          />
          <Bar dataKey="revenue" fill="#6366F1" radius={[0, 4, 4, 0]} name="Closed Revenue" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
