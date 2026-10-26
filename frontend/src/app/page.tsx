"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  Search,
  Bot,
  ShieldCheck,
  FileCheck,
  FlaskConical,
  CheckSquare,
  ArrowRight,
  Sparkles,
  ExternalLink,
  Clock,
  Layers
} from "lucide-react";
import { fetchCoverageDashboard, fetchStandards, fetchQCOs } from "@/lib/api";
import { CoverageStats, StandardSummary, QCOSummary } from "@/lib/types";

export default function OverviewPage() {
  const router = useRouter();
  const [stats, setStats] = useState<CoverageStats | null>(null);
  const [recentStandards, setRecentStandards] = useState<StandardSummary[]>([]);
  const [recentQCOs, setRecentQCOs] = useState<QCOSummary[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetchCoverageDashboard().then((res) => setStats(res.stats)),
      fetchStandards({ limit: 4 }).then((res) => setRecentStandards(res.items)),
      fetchQCOs({ limit: 4 }).then((res) => setRecentQCOs(res.items)),
    ])
      .catch((err) => console.error("Error loading dashboard data", err))
      .finally(() => setLoading(false));
  }, []);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    router.push(`/standards?q=${encodeURIComponent(searchQuery.trim())}`);
  };

  return (
    <div className="max-w-7xl mx-auto space-y-10">
      {/* Hero & Quick Search */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-slate-900 via-slate-900 to-blue-950 border border-slate-800 p-8 md:p-12 shadow-2xl">
        <div className="relative z-10 max-w-3xl space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-semibold uppercase tracking-wider">
            <Sparkles className="w-3.5 h-3.5" /> Bureau of Indian Standards Intelligence Platform
          </div>
          <h1 className="text-3xl md:text-5xl font-extrabold tracking-tight text-white leading-tight">
            Navigate BIS Compliance, Standards & QCOs with Precision
          </h1>
          <p className="text-slate-300 text-base md:text-lg leading-relaxed">
            Search verified Indian Standards (IS), cross-reference mandatory Quality Control Orders, discover accredited testing laboratories, and formulate production-ready compliance workflows.
          </p>

          {/* Search Bar */}
          <form onSubmit={handleSearchSubmit} className="pt-4 flex flex-col sm:flex-row gap-3 max-w-2xl">
            <div className="relative flex-1">
              <Search className="absolute left-4 top-3.5 w-5 h-5 text-slate-400" />
              <input
                type="text"
                placeholder="Search by IS number (e.g. IS 302), product, or industry..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-12 pr-4 py-3 rounded-xl bg-slate-950/80 border border-slate-700 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm shadow-inner"
              />
            </div>
            <button
              type="submit"
              className="px-6 py-3 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-medium text-sm transition-colors shadow-lg shadow-blue-600/30 flex items-center justify-center gap-2"
            >
              Search Records <ArrowRight className="w-4 h-4" />
            </button>
          </form>

          {/* Query Suggestion Pills */}
          <div className="pt-2 flex flex-wrap gap-2 text-xs text-slate-400">
            <span>Popular:</span>
            {[
              { label: "IS 302 (Water Heaters)", query: "IS 302" },
              { label: "Toys QCO", query: "Toys" },
              { label: "IS 16046 (Lithium Batteries)", query: "IS 16046" },
              { label: "TMT Steel Bars", query: "IS 1786" },
              { label: "Solar PV Modules", query: "IS 14286" }
            ].map((p) => (
              <button
                key={p.label}
                onClick={() => router.push(`/standards?q=${encodeURIComponent(p.query)}`)}
                className="px-2.5 py-1 rounded-md bg-slate-800/80 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700/60 transition-colors"
              >
                {p.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Metrics Row (Real Data from DB) */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="p-6 rounded-xl bg-slate-900 border border-slate-800 flex flex-col justify-between shadow-sm">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium uppercase tracking-wider mb-2">
            <span>Standards Indexed</span>
            <Layers className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-3xl font-bold text-white">
            {loading ? "..." : stats?.total_standards || 0}
          </div>
          <div className="text-xs text-emerald-400 mt-2 flex items-center gap-1 font-medium">
            <ShieldCheck className="w-3.5 h-3.5" /> 100% Verified Official Records
          </div>
        </div>

        <div className="p-6 rounded-xl bg-slate-900 border border-slate-800 flex flex-col justify-between shadow-sm">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium uppercase tracking-wider mb-2">
            <span>Active QCO Orders</span>
            <FileCheck className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-3xl font-bold text-white">
            {loading ? "..." : stats?.active_qcos || 0}
          </div>
          <div className="text-xs text-slate-400 mt-2">
            Mandatory Certification Decrees
          </div>
        </div>

        <div className="p-6 rounded-xl bg-slate-900 border border-slate-800 flex flex-col justify-between shadow-sm">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium uppercase tracking-wider mb-2">
            <span>Recognized Labs</span>
            <FlaskConical className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-3xl font-bold text-white">
            {loading ? "..." : stats?.total_laboratories || 0}
          </div>
          <div className="text-xs text-slate-400 mt-2">
            {stats?.total_scopes_mapped || 0} Standard Scopes Mapped
          </div>
        </div>

        <div className="p-6 rounded-xl bg-slate-900 border border-slate-800 flex flex-col justify-between shadow-sm">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium uppercase tracking-wider mb-2">
            <span>Certification Schemes</span>
            <ShieldCheck className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-3xl font-bold text-white">
            {loading ? "..." : stats?.total_schemes || 0}
          </div>
          <div className="text-xs text-slate-400 mt-2">
            Scheme I (ISI) & Scheme II (CRS)
          </div>
        </div>
      </div>

      {/* Primary Workflow Cards */}
      <div>
        <h2 className="text-xl font-bold text-white mb-4">Core Workflows & Tools</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link
            href="/assistant"
            className="group p-6 rounded-xl bg-slate-900 border border-slate-800 hover:border-blue-500/50 hover:bg-slate-850 transition-all shadow-sm flex flex-col justify-between"
          >
            <div>
              <div className="w-12 h-12 rounded-xl bg-blue-500/10 border border-blue-500/20 text-blue-400 flex items-center justify-center mb-4 group-hover:scale-105 transition-transform">
                <Bot className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-white group-hover:text-blue-400 transition-colors">
                AI Regulatory Assistant
              </h3>
              <p className="text-sm text-slate-400 mt-2 leading-relaxed">
                Ask questions in plain language about household appliances, electronics, toys, or machinery and receive grounded answers backed by official citations.
              </p>
            </div>
            <div className="flex items-center gap-2 text-sm font-medium text-blue-400 mt-6 group-hover:translate-x-1 transition-transform">
              Launch Assistant <ArrowRight className="w-4 h-4" />
            </div>
          </Link>

          <Link
            href="/navigator"
            className="group p-6 rounded-xl bg-slate-900 border border-slate-800 hover:border-emerald-500/50 hover:bg-slate-850 transition-all shadow-sm flex flex-col justify-between"
          >
            <div>
              <div className="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 flex items-center justify-center mb-4 group-hover:scale-105 transition-transform">
                <ShieldCheck className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-white group-hover:text-emerald-400 transition-colors">
                Certification Navigator
              </h3>
              <p className="text-sm text-slate-400 mt-2 leading-relaxed">
                Step-by-step product evaluation: identify Indian Standards, check mandatory QCO applicability, determine scheme type, and generate compliance checklists.
              </p>
            </div>
            <div className="flex items-center gap-2 text-sm font-medium text-emerald-400 mt-6 group-hover:translate-x-1 transition-transform">
              Start Product Audit <ArrowRight className="w-4 h-4" />
            </div>
          </Link>

          <Link
            href="/checklists"
            className="group p-6 rounded-xl bg-slate-900 border border-slate-800 hover:border-purple-500/50 hover:bg-slate-850 transition-all shadow-sm flex flex-col justify-between"
          >
            <div>
              <div className="w-12 h-12 rounded-xl bg-purple-500/10 border border-purple-500/20 text-purple-400 flex items-center justify-center mb-4 group-hover:scale-105 transition-transform">
                <CheckSquare className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-white group-hover:text-purple-400 transition-colors">
                Compliance Project Tracker
              </h3>
              <p className="text-sm text-slate-400 mt-2 leading-relaxed">
                Create persistent project checklists, track documentation and testing milestones, monitor completion percentages, and export audit sheets to CSV.
              </p>
            </div>
            <div className="flex items-center gap-2 text-sm font-medium text-purple-400 mt-6 group-hover:translate-x-1 transition-transform">
              Manage Checklists <ArrowRight className="w-4 h-4" />
            </div>
          </Link>
        </div>
      </div>

      {/* Dual Column: Verified Standards & Gazette QCOs */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Verified Indian Standards */}
        <div className="p-6 rounded-xl bg-slate-900 border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Layers className="w-5 h-5 text-blue-400" /> Indexed Indian Standards
            </h2>
            <Link href="/standards" className="text-xs text-blue-400 hover:text-blue-300 font-medium">
              View All ({stats?.total_standards || 0}) →
            </Link>
          </div>
          <div className="space-y-3">
            {recentStandards.map((std) => (
              <Link
                key={std.id}
                href={`/standards?id=${std.id}`}
                className="block p-3.5 rounded-lg bg-slate-950/60 hover:bg-slate-800/80 border border-slate-800/80 transition-colors"
              >
                <div className="flex items-center justify-between text-xs mb-1">
                  <span className="font-bold text-blue-400">{std.is_number}</span>
                  {std.has_qco && (
                    <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-amber-500/20 text-amber-300 border border-amber-500/30">
                      Mandatory QCO
                    </span>
                  )}
                </div>
                <div className="text-sm font-medium text-slate-200 line-clamp-1">{std.title}</div>
                <div className="text-xs text-slate-500 mt-1 flex items-center gap-3">
                  <span>{std.division || "Electrotechnical"}</span>
                  <span>•</span>
                  <span>{std.lab_count} Testing Labs</span>
                </div>
              </Link>
            ))}
          </div>
        </div>

        {/* Gazette Quality Control Orders */}
        <div className="p-6 rounded-xl bg-slate-900 border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <FileCheck className="w-5 h-5 text-amber-400" /> Quality Control Orders (QCO)
            </h2>
            <Link href="/qco" className="text-xs text-blue-400 hover:text-blue-300 font-medium">
              View All ({stats?.total_qcos || 0}) →
            </Link>
          </div>
          <div className="space-y-3">
            {recentQCOs.map((q) => (
              <div
                key={q.id}
                className="p-3.5 rounded-lg bg-slate-950/60 border border-slate-800/80 space-y-1.5"
              >
                <div className="flex items-center justify-between text-xs">
                  <span className="font-semibold text-slate-300">{q.order_number}</span>
                  <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                    {q.status}
                  </span>
                </div>
                <div className="text-sm font-medium text-slate-200">{q.title}</div>
                <div className="text-xs text-slate-500 flex items-center justify-between pt-1">
                  <span>{q.issuing_ministry}</span>
                  {q.enforcement_date && <span>Enforced: {q.enforcement_date}</span>}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
