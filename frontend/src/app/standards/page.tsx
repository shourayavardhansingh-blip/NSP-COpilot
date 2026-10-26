"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import {
  Search,
  Filter,
  Layers,
  FileCheck,
  FlaskConical,
  ExternalLink,
  ChevronRight,
  ShieldCheck,
  X,
  Info
} from "lucide-react";
import { fetchStandards, fetchStandardDetail } from "@/lib/api";
import { StandardSummary, StandardDetail } from "@/lib/types";

const DIVISIONS = [
  { label: "All Divisions", value: "" },
  { label: "Electrotechnical (ETD)", value: "ETD" },
  { label: "Civil Engineering (CED)", value: "CED" },
  { label: "Mechanical Engineering (MED)", value: "MED" },
  { label: "Electronics & IT (LITD)", value: "LITD" },
  { label: "Food & Agriculture (FAD)", value: "FAD" },
  { label: "Metallurgical Engineering (MTD)", value: "MTD" },
];

function StandardsExplorerContent() {
  const searchParams = useSearchParams();
  const initialQuery = searchParams.get("q") || "";
  const initialId = searchParams.get("id");

  const [query, setQuery] = useState(initialQuery);
  const [division, setDivision] = useState("");
  const [hasQCO, setHasQCO] = useState<boolean | undefined>(undefined);
  const [standards, setStandards] = useState<StandardSummary[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);

  // Selected Standard Drawer
  const [selectedStandard, setSelectedStandard] = useState<StandardDetail | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);

  const loadData = () => {
    setLoading(true);
    fetchStandards({
      q: query || undefined,
      division: division || undefined,
      has_qco: hasQCO,
      limit: 50,
    })
      .then((res) => {
        setStandards(res.items);
        setTotal(res.total);
      })
      .catch((err) => console.error("Error fetching standards", err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadData();
  }, [division, hasQCO]);

  useEffect(() => {
    if (initialId) {
      openDetail(Number(initialId));
    }
  }, [initialId]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    loadData();
  };

  const openDetail = (id: number) => {
    setDetailLoading(true);
    fetchStandardDetail(id)
      .then((data) => setSelectedStandard(data))
      .catch((err) => console.error(err))
      .finally(() => setDetailLoading(false));
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Title & Filter Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <Layers className="w-6 h-6 text-blue-500" /> Standard Explorer
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Search Indian Standards catalogue with intelligent number normalization and QCO cross-referencing
          </p>
        </div>

        {/* Search Input */}
        <form onSubmit={handleSearchSubmit} className="flex gap-2 w-full md:w-96">
          <div className="relative flex-1">
            <Search className="absolute left-3.5 top-3 w-4 h-4 text-slate-400" />
            <input
              type="text"
              placeholder="Search IS number, title, or keyword..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <button
            type="submit"
            className="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium transition-colors"
          >
            Search
          </button>
        </form>
      </div>

      {/* Filters Pill Row */}
      <div className="flex flex-wrap items-center gap-2 text-xs">
        <span className="text-slate-400 flex items-center gap-1 font-medium mr-2">
          <Filter className="w-3.5 h-3.5" /> Filters:
        </span>

        {/* Division Filter */}
        <select
          value={division}
          onChange={(e) => setDivision(e.target.value)}
          className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 focus:outline-none focus:ring-1 focus:ring-blue-500"
        >
          {DIVISIONS.map((d) => (
            <option key={d.value} value={d.value}>
              {d.label}
            </option>
          ))}
        </select>

        {/* QCO Mandatory Filter */}
        <button
          onClick={() => setHasQCO(hasQCO === true ? undefined : true)}
          className={`px-3 py-1.5 rounded-lg border transition-colors ${
            hasQCO === true
              ? "bg-amber-500/20 border-amber-500/40 text-amber-300"
              : "bg-slate-900 border-slate-800 text-slate-400 hover:text-white"
          }`}
        >
          Mandatory QCO Only
        </button>

        {/* Reset button */}
        {(query || division || hasQCO !== undefined) && (
          <button
            onClick={() => {
              setQuery("");
              setDivision("");
              setHasQCO(undefined);
              fetchStandards({ limit: 50 }).then((res) => {
                setStandards(res.items);
                setTotal(res.total);
              });
            }}
            className="px-2.5 py-1.5 text-slate-400 hover:text-white transition-colors"
          >
            Clear Filters
          </button>
        )}

        <span className="ml-auto text-slate-500">
          Showing {standards.length} of {total} records
        </span>
      </div>

      {/* Standards List / Table */}
      <div className="rounded-xl border border-slate-800 bg-slate-900 overflow-hidden shadow-sm">
        {loading ? (
          <div className="p-12 text-center text-slate-400 text-sm">
            Searching Indian Standards catalogue...
          </div>
        ) : standards.length === 0 ? (
          <div className="p-12 text-center space-y-2">
            <p className="text-base text-slate-300 font-semibold">No Indian Standards matched your query</p>
            <p className="text-xs text-slate-500">Try searching with a broader product name or IS number prefix (e.g. IS 302, 694).</p>
          </div>
        ) : (
          <div className="divide-y divide-slate-800">
            {standards.map((std) => (
              <div
                key={std.id}
                onClick={() => openDetail(std.id)}
                className="p-5 hover:bg-slate-850 cursor-pointer transition-colors flex items-center justify-between gap-4"
              >
                <div className="space-y-1.5 flex-1">
                  <div className="flex items-center gap-2.5">
                    <span className="font-bold text-blue-400 text-base">{std.is_number}</span>
                    <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-slate-800 text-slate-300 border border-slate-700">
                      {std.status}
                    </span>
                    {std.has_qco && (
                      <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-amber-500/20 text-amber-300 border border-amber-500/30 flex items-center gap-1">
                        <FileCheck className="w-3 h-3" /> Mandatory QCO
                      </span>
                    )}
                  </div>
                  <h3 className="text-slate-200 text-sm font-medium">{std.title}</h3>
                  <div className="flex flex-wrap items-center gap-3 text-xs text-slate-400 pt-1">
                    <span>Division: {std.division || "N/A"}</span>
                    <span>•</span>
                    <span>Year: {std.publication_year || "Current"}</span>
                    <span>•</span>
                    <span className="text-emerald-400 flex items-center gap-1">
                      <FlaskConical className="w-3.5 h-3.5" /> {std.lab_count} Accredited Labs
                    </span>
                  </div>
                </div>
                <ChevronRight className="w-5 h-5 text-slate-600 shrink-0" />
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Detail Modal / Drawer */}
      {selectedStandard && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto shadow-2xl p-6 md:p-8 space-y-6">
            {/* Modal Header */}
            <div className="flex items-start justify-between border-b border-slate-800 pb-4">
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-extrabold text-xl text-blue-400">{selectedStandard.is_number}</span>
                  <span className="px-2.5 py-0.5 rounded text-xs font-semibold bg-slate-800 text-slate-300">
                    {selectedStandard.status}
                  </span>
                </div>
                <h2 className="text-lg font-bold text-white mt-1">{selectedStandard.title}</h2>
              </div>
              <button
                onClick={() => setSelectedStandard(null)}
                className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Scope / Permitted Abstract */}
            {selectedStandard.scope_abstract && (
              <div className="space-y-2">
                <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                  <Info className="w-3.5 h-3.5 text-blue-400" /> Permitted Scope & Abstract
                </h4>
                <p className="text-sm text-slate-300 leading-relaxed bg-slate-950 p-4 rounded-xl border border-slate-800">
                  {selectedStandard.scope_abstract}
                </p>
              </div>
            )}

            {/* Mandatory QCO Section */}
            <div>
              <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                <FileCheck className="w-3.5 h-3.5 text-amber-400" /> Applicable Quality Control Orders
              </h4>
              {selectedStandard.applicable_qcos.length === 0 ? (
                <div className="text-xs text-slate-400 bg-slate-950/40 p-3 rounded-lg border border-slate-800">
                  No active mandatory QCO mandate recorded in database. Voluntary ISI certification may be applied.
                </div>
              ) : (
                <div className="space-y-2">
                  {selectedStandard.applicable_qcos.map((q) => (
                    <div key={q.qco_id} className="p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-xs space-y-1">
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-amber-300">{q.order_number}</span>
                        <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-amber-500/20 text-amber-300">
                          {q.status}
                        </span>
                      </div>
                      <div className="text-slate-200 font-medium">{q.title}</div>
                      <div className="text-slate-400 text-[11px]">
                        Ministry: {q.issuing_ministry} {q.enforcement_date && `• Enforced: ${q.enforcement_date}`}
                      </div>
                      {q.official_url && (
                        <a
                          href={q.official_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-1 text-blue-400 hover:underline pt-1"
                        >
                          View Official Gazette Notification <ExternalLink className="w-3 h-3" />
                        </a>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Accredited Labs Section */}
            <div>
              <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                <FlaskConical className="w-3.5 h-3.5 text-emerald-400" /> Accredited Testing Facilities ({selectedStandard.accredited_labs.length})
              </h4>
              {selectedStandard.accredited_labs.length === 0 ? (
                <div className="text-xs text-slate-400 bg-slate-950/40 p-3 rounded-lg border border-slate-800">
                  No testing laboratories with mapped scope recorded in local database. Check BIS LIMS directory.
                </div>
              ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {selectedStandard.accredited_labs.map((lab) => (
                    <div key={lab.lab_id} className="p-3 rounded-xl bg-slate-950 border border-slate-800 text-xs space-y-1">
                      <div className="font-semibold text-slate-200">{lab.lab_name}</div>
                      <div className="text-slate-400">{lab.city}, {lab.state}</div>
                      <div className="text-[11px] text-emerald-400 font-medium">Status: {lab.status}</div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Source Reference & Legal Notice */}
            <div className="pt-4 border-t border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-500">
              <span>Verified Record: {selectedStandard.verification_date?.slice(0, 10)}</span>
              {selectedStandard.source_url && (
                <a
                  href={selectedStandard.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-medium flex items-center gap-1.5 transition-colors"
                >
                  Open Official BIS Portal <ExternalLink className="w-3.5 h-3.5" />
                </a>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}


export default function StandardsPage() {
  return (
    <Suspense fallback={<div className="p-12 text-center text-slate-400">Loading Standard Explorer...</div>}>
      <StandardsExplorerContent />
    </Suspense>
  );
}
