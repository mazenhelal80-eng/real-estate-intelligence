import type { Metadata } from "next";
import "./globals.css";
import { QueryProvider } from "@/components/providers/QueryProvider";

export const metadata: Metadata = {
  title: "Real Estate Intelligence & AI Decision Engine",
  description: "Enterprise portfolio intelligence platform built by Mazen Helal",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="antialiased bg-background text-text-primary">
        <QueryProvider>{children}</QueryProvider>
      </body>
    </html>
  );
}
