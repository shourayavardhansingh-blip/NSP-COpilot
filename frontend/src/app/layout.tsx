import type { Metadata } from "next";
import "./globals.css";
import Navigation from "@/components/Navigation";
import Header from "@/components/Header";

export const metadata: Metadata = {
  title: "BIS AI Copilot — Bureau of Indian Standards Intelligence",
  description: "Enterprise compliance, standards discovery, and research platform for Bureau of Indian Standards (BIS) regulations.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-slate-950 text-slate-100 flex min-h-screen antialiased selection:bg-blue-600 selection:text-white">
        <Navigation />
        <div className="flex-1 flex flex-col min-w-0">
          <Header />
          <main className="flex-1 overflow-y-auto p-8">{children}</main>
        </div>
      </body>
    </html>
  );
}
