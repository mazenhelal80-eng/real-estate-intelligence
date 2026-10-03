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
import { VERIFIED_DEVELOPERS } from "@/lib/verified_data";

export function DeveloperBarChart() {
  const chartData = VERIFIED_DEVELOPERS.map((dev) => ({
    name: dev.developer_name.replace(" Properties", "").replace(" Legacy", "").replace(" Prime", "").replace(" Group", ""),
    units: dev.total_units,
    projects: dev.active_projects,
  }));

  return (
    <div className="h-52 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={chartData} margin={{ top: 10, right: 10, left: 10, bottom: 25 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#263247" vertical={false} />
          <XAxis dataKey="name" stroke="#A8B3C2" fontSize={10} angle={-25} textAnchor="end" tickLine={false} />
          <YAxis stroke="#A8B3C2" fontSize={11} tickLine={false} />
          <Tooltip
            contentStyle={{
              backgroundColor: "#111827",
              borderColor: "#263247",
              borderRadius: "8px",
              color: "#F8FAFC",
              fontSize: "12px",
            }}
          />
          <Bar dataKey="units" fill="#1877F2" radius={[4, 4, 0, 0]} name="Units Launched" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
