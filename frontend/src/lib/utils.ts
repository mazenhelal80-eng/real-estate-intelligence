import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatEGP(value: number): string {
  if (value >= 1_000_000_000) {
    return `${(value / 1_000_000_000).toFixed(2)}B EGP`;
  }
  if (value >= 1_000_000) {
    return `${(value / 1_000_000).toFixed(2)}M EGP`;
  }
  if (value >= 1_000) {
    return `${(value / 1_000).toFixed(1)}K EGP`;
  }
  return `${new Intl.NumberFormat("en-EG", { maximumFractionDigits: 0 }).format(value)} EGP`;
}

export function formatNumber(value: number): string {
  return new Intl.NumberFormat("en-US").format(value);
}

export function formatPercent(value: number): string {
  return `${(value * 100).toFixed(1)}%`;
}
