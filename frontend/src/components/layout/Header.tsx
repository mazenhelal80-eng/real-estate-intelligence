"use client";

import React from "react";
import { useQuery } from "@tanstack/react-query";
import { checkHealth } from "@/lib/api";
import { Badge } from "@/components/ui/Badge";
import { Server, Activity } from "lucide-react";

interface HeaderProps {
  title: string;
  subtitle?: string;
}

export function Header({ title, subtitle }: HeaderProps) {
  const { data: health, isSuccess, isError } = useQuery({
    queryKey: ["healthCheck"],
    queryFn: checkHealth,
    refetchInterval: 15000,
    retry: 1,
  });

  return (
    <header className="sticky top-0 z-30 flex h-16 w-full items-center justify-between border-b border-border bg-surface-primary/95 px-6 backdrop-blur-sm">
      <div>
        <h2 className="text-base font-semibold text-text-primary tracking-tight">{title}</h2>
        {subtitle && <p className="text-xs text-text-secondary">{subtitle}</p>}
      </div>

      <div className="flex items-center gap-3">
        {isSuccess ? (
          <Badge variant="success" className="gap-1.5 py-1">
            <span className="h-1.5 w-1.5 rounded-full bg-status-success animate-pulse" />
            <Server className="h-3 w-3" />
            <span>FastAPI Live (v{health.version})</span>
          </Badge>
        ) : isError ? (
          <Badge variant="danger" className="gap-1.5 py-1">
            <span className="h-1.5 w-1.5 rounded-full bg-status-danger" />
            <span>FastAPI Offline</span>
          </Badge>
        ) : (
          <Badge variant="outline" className="gap-1.5 py-1">
            <Activity className="h-3 w-3 animate-spin text-text-muted" />
            <span>Checking API...</span>
          </Badge>
        )}
      </div>
    </header>
  );
}
