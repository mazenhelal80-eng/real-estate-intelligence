"use client";

import React from "react";
import { Sidebar } from "./Sidebar";
import { Header } from "./Header";

interface ShellProps {
  children: React.ReactNode;
  title: string;
  subtitle?: string;
}

export function Shell({ children, title, subtitle }: ShellProps) {
  return (
    <div className="min-h-screen bg-background text-text-primary flex">
      <Sidebar />
      <div className="flex flex-1 flex-col pl-64">
        <Header title={title} subtitle={subtitle} />
        <main className="flex-1 p-5 space-y-4 md:p-6 md:space-y-5 overflow-x-hidden">
          {children}
        </main>
      </div>
    </div>
  );
}
