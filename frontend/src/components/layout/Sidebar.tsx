"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  BarChart3,
  Building2,
  Cpu,
  FolderGit2,
  Home,
  PieChart,
  Users,
} from "lucide-react";
import { cn } from "@/lib/utils";

const NAV_ITEMS = [
  { href: "/", label: "Dashboard", icon: Home },
  { href: "/properties", label: "Properties", icon: Building2 },
  { href: "/ml", label: "ML Intelligence", icon: Cpu },
  { href: "/market", label: "Market Analytics", icon: BarChart3 },
  { href: "/customers", label: "Customers", icon: Users },
  { href: "/developers", label: "Developers", icon: PieChart },
  { href: "/project", label: "Project & Architecture", icon: FolderGit2 },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed inset-y-0 left-0 z-40 flex w-64 flex-col border-r border-border bg-surface-primary">
      <div className="flex h-16 items-center gap-3 border-b border-border px-5">
        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-accent/20 text-accent font-bold text-lg">
          R
        </div>
        <div>
          <h1 className="text-sm font-semibold tracking-tight text-text-primary">
            REAL ESTATE INTEL
          </h1>
          <p className="text-[10px] uppercase tracking-wider text-text-secondary">
            AI Decision Engine
          </p>
        </div>
      </div>

      <nav className="flex-1 space-y-1.5 overflow-y-auto px-3 py-4">
        {NAV_ITEMS.map((item) => {
          const isActive = pathname === item.href;
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 rounded-lg px-3 py-2.5 text-xs font-medium transition-colors",
                isActive
                  ? "bg-accent/15 text-accent font-semibold"
                  : "text-text-secondary hover:bg-surface-secondary hover:text-text-primary"
              )}
            >
              <Icon className={cn("h-4 w-4", isActive ? "text-accent" : "text-text-secondary")} />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      <div className="border-t border-border p-4 bg-surface-secondary/40">
        <div className="rounded-lg border border-border/80 bg-surface-primary/70 p-3">
          <p className="text-[10px] font-medium uppercase tracking-wider text-text-muted">
            Built by
          </p>
          <p className="mt-0.5 text-xs font-semibold text-text-primary">
            Mazen Helal
          </p>
          <p className="text-[10px] text-text-secondary">
            AI Engineer & Full-Stack AI Developer
          </p>
        </div>
      </div>
    </aside>
  );
}
