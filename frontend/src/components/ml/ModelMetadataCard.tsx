import React from "react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Database, GitBranch, Cpu, ShieldCheck } from "lucide-react";

interface ModelMetadataProps {
  modelName: string;
  modelVersion: string;
  algorithm: string;
  taskType: string;
  target?: string;
  featureCount: number;
  endpoint: string;
  validationStatus: string;
  keyMetric?: { label: string; value: string };
}

export function ModelMetadataCard({
  modelName,
  modelVersion,
  algorithm,
  taskType,
  target,
  featureCount,
  endpoint,
  validationStatus,
  keyMetric,
}: ModelMetadataProps) {
  return (
    <Card className="border-border bg-surface-primary">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Cpu className="h-4 w-4 text-accent" />
            <CardTitle className="text-xs uppercase tracking-wider text-text-secondary">Model Specifications</CardTitle>
          </div>
          <Badge variant="outline" className="text-[10px] font-mono">
            {modelVersion}
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-2.5 text-xs">
        <div className="flex items-center justify-between border-b border-border/50 pb-1.5">
          <span className="text-text-muted">Model ID:</span>
          <span className="font-mono text-text-primary">{modelName}</span>
        </div>
        <div className="flex items-center justify-between border-b border-border/50 pb-1.5">
          <span className="text-text-muted">Algorithm:</span>
          <span className="font-semibold text-text-primary">{algorithm}</span>
        </div>
        <div className="flex items-center justify-between border-b border-border/50 pb-1.5">
          <span className="text-text-muted">Task Type:</span>
          <span className="text-text-secondary">{taskType}</span>
        </div>
        {target && (
          <div className="flex items-center justify-between border-b border-border/50 pb-1.5">
            <span className="text-text-muted">Target Variable:</span>
            <span className="font-mono text-accent">{target}</span>
          </div>
        )}
        <div className="flex items-center justify-between border-b border-border/50 pb-1.5">
          <span className="text-text-muted">Input Features:</span>
          <span className="font-medium text-text-primary">{featureCount} features</span>
        </div>
        <div className="flex items-center justify-between border-b border-border/50 pb-1.5">
          <span className="text-text-muted">FastAPI Route:</span>
          <span className="font-mono text-[10px] text-text-secondary">{endpoint}</span>
        </div>
        {keyMetric && (
          <div className="flex items-center justify-between border-b border-border/50 pb-1.5">
            <span className="text-text-muted">{keyMetric.label}:</span>
            <span className="font-mono font-bold text-status-success">{keyMetric.value}</span>
          </div>
        )}
        <div className="flex items-center justify-between pt-0.5">
          <span className="text-text-muted">Audit Status:</span>
          <Badge variant="success" className="text-[10px] gap-1">
            <ShieldCheck className="h-3 w-3" />
            <span>{validationStatus}</span>
          </Badge>
        </div>
      </CardContent>
    </Card>
  );
}
