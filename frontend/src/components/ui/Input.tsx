import React from "react";
import { cn } from "@/lib/utils";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export function Input({ className, label, error, id, ...props }: InputProps) {
  const inputId = id || (label ? label.toLowerCase().replace(/\s+/g, "-") : undefined);

  return (
    <div className="w-full space-y-1.5">
      {label && (
        <label htmlFor={inputId} className="block text-xs font-medium text-text-secondary">
          {label}
        </label>
      )}
      <input
        id={inputId}
        className={cn(
          "w-full rounded-lg border border-border bg-surface-secondary px-3 py-2 text-sm text-text-primary placeholder-text-muted transition-colors focus:border-accent focus:outline-none focus:ring-1 focus:ring-accent disabled:opacity-50",
          error && "border-status-danger focus:border-status-danger focus:ring-status-danger",
          className
        )}
        {...props}
      />
      {error && <p className="text-xs text-status-danger">{error}</p>}
    </div>
  );
}
