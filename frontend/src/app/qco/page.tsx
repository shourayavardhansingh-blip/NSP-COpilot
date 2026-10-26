"use client";

import { useEffect, useState } from "react";
import {
  FileCheck,
  Search,
  Filter,
  Calendar,
  ExternalLink,
  ChevronRight,
  ShieldAlert,
  History,
  X,
  Layers
} from "lucide-react";
import { fetchQCOs, fetchQCODetail } from "@/lib/api";
import { QCOSummary, QCODetail } from "@/lib/types";

const MINISTRIES = [
  "All Ministries",
  "DPIIT",
  "Ministry of Heavy Industries",
  "MeitY",
  "Ministry of Steel",
  "MoRTH",
  "MNRE"
];

export default function QCOPage() {
  const [qcos, setQcos] = useState<QCOSummary[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);

  // Filters
  const [query, setQuery] = useState("");
  const [ministry, setMinistry] = useState("All Ministries");

  // Detail Modal
  const [selectedQCO, setSelectedQCO] = useState<QCODetail | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);

  const loadData = () => {
    setLoading(true);
    fetchQCOs({
      q: query || undefined,
      ministry: ministry !== "All Ministries" ? ministry : undefined,
      limit: 50,
    })
      .then((res) => {
        setQcos(res.items);
        setTotal(res.total);
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadData();
  }, [ministry]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    loadData();
  };

  const openDetail = (id: number) => {
    setDetailLoading(true);
    fetchQCODetail(id)
      .then((data) => setSelectedQCO(data))
      .catch((err) => console.error(err))
      .finally(() => setDetailLoading(false));
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <FileCheck className="w-6 h-6 text-amber-500" /> Quality Control Orders (QCO)
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Track mandatory GoI statutory decrees, enforcement milestones, and gazette amendments
          </p>
        </div>

        {/* Search */}
        <form onSubmit={handleSearchSubmit} className="flex gap-2 w-full md:w-96">
          <div className="relative flex-1">
            <Search className="absolute left-3.5 top-3 w-4 h-4 text-slate-400" />
            <input
              type="text"
              placeholder="Search order number, ministry, or standard..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500"
            />
          </div>
          <button
            type="submit"
            className="px-4 py-2 rounded-lg bg-amber-600 hover:bg-amber-500 text-white text-sm font-medium transition-colors"
          >
            Search
          </button>
        </form>
      </div>

      {/* Filter Row */}
      <div className="flex flex-wrap items-center gap-3 text-xs">
        <span className="text-slate-400 font-medium flex items-center gap-1">
          <Filter className="w-3.5 h-3.5" /> Issuing Ministry:
        </span>
        <select
          value={ministry}
          onChange={(e) => setMinistry(e.target.value)}
          className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 focus:outline-none focus:ring-1 focus:ring-amber-500"
        >
          {MINISTRIES.map((m) => (
            <option key={m} value={m}>
              {m}
            </option>
          ))}
        </select>

        <span className="ml-auto text-slate-500">
          Showing {qcos.length} of {total} orders
        </span>
      </div>

      {/* QCO List Cards */}
      {loading ? (
        <div className="p-12 text-center text-slate-400 text-sm">Loading Quality Control Orders...</div>
      ) : qcos.length === 0 ? (
        <div className="p-12 text-center text-slate-400 text-sm bg-slate-900 rounded-xl border border-slate-800">
          No Quality Control Orders found matching this filter.
        </div>
      ) : (
        <div className="space-y-4">
          {qcos.map((q) => (
            <div
              key={q.id}
              onClick={() => openDetail(q.id)}
              className="p-6 rounded-2xl bg-slate-900 border border-slate-800 hover:border-amber-500/40 hover:bg-slate-850 cursor-pointer transition-all shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4"
            >
              <div className="space-y-2 flex-1">
                <div className="flex items-center gap-2.5">
                  <span className="font-extrabold text-amber-400 text-base">{q.order_number}</span>
                  <span className="px-2.5 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                    {q.status}
                  </span>
                  {q.amendment_count > 0 && (
                    <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-800 text-slate-300 flex items-center gap-1">
                      <History className="w-3 h-3" /> {q.amendment_count} Amendments
                    </span>
                  )}
                </div>

                <h3 className="text-slate-100 font-bold text-base leading-snug">{q.title}</h3>

                <div className="flex flex-wrap items-center gap-4 text-xs text-slate-400 pt-1">
                  <span>Ministry: {q.issuing_ministry}</span>
                  <span>•</span>
                  <span>Category: {q.product_category || "General"}</span>
                  {q.enforcement_date && (
                    <>
                      <span>•</span>
                      <span className="text-amber-300 font-medium flex items-center gap-1">
                        <Calendar className="w-3.5 h-3.5" /> Enforcement: {q.enforcement_date}
                      </span>
                    </>
                  )}
                </div>
              </div>

              <ChevronRight className="w-5 h-5 text-slate-600 shrink-0" />
            </div>
          ))}
        </div>
      )}

      {/* QCO Detail Modal with Amendments Timeline */}
      {selectedQCO && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto shadow-2xl p-6 md:p-8 space-y-6">
            <div className="flex items-start justify-between border-b border-slate-800 pb-4">
              <div>
                <span className="px-2.5 py-0.5 rounded text-xs font-bold bg-amber-500/20 text-amber-300">
                  {selectedQCO.order_number}
                </span>
                <h2 className="text-xl font-bold text-white mt-1.5">{selectedQCO.title}</h2>
                <div className="text-xs text-slate-400 mt-1">
                  Issuing Authority: {selectedQCO.issuing_ministry}
                </div>
              </div>
              <button
                onClick={() => setSelectedQCO(null)}
                className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Notes & Summary */}
            {selectedQCO.notes && (
              <div className="space-y-2">
                <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Decree Scope & Provisions
                </h4>
                <p className="text-xs text-slate-300 leading-relaxed bg-slate-950 p-4 rounded-xl border border-slate-800">
                  {selectedQCO.notes}
                </p>
              </div>
            )}

            {/* Mandated Standards */}
            <div>
              <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                <Layers className="w-3.5 h-3.5 text-blue-400" /> Mandated Indian Standards ({selectedQCO.standards.length})
              </h4>
              <div className="space-y-2">
                {selectedQCO.standards.map((s) => (
                  <div key={s.standard_id} className="p-3 rounded-lg bg-slate-950 border border-slate-800 text-xs space-y-1">
                    <div className="font-bold text-blue-400">{s.is_number}</div>
                    <div className="text-slate-300 font-medium">{s.title}</div>
                    {s.exemption_notes && (
                      <div className="text-amber-400 text-[11px] pt-0.5">Note: {s.exemption_notes}</div>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Amendments Timeline */}
            <div>
              <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                <History className="w-3.5 h-3.5 text-purple-400" /> Gazette Amendments & Enforcement Extensions
              </h4>
              {selectedQCO.amendments.length === 0 ? (
                <div className="text-xs text-slate-400 bg-slate-950 p-3 rounded-lg border border-slate-800">
                  No post-publication amendments or revision orders recorded. Original notification remains in full force.
                </div>
              ) : (
                <div className="space-y-2">
                  {selectedQCO.amendments.map((a) => (
                    <div key={a.id} className="p-3.5 rounded-xl bg-purple-500/10 border border-purple-500/20 text-xs space-y-1">
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-purple-300">{a.amendment_number}</span>
                        {a.notification_date && <span className="text-slate-400">{a.notification_date}</span>}
                      </div>
                      <p className="text-slate-300 leading-relaxed">{a.summary}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Official Gazette Link */}
            <div className="pt-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-500">
              <span>Section 16, BIS Act 2016 Enforcement</span>
              {selectedQCO.official_url && (
                <a
                  href={selectedQCO.official_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-4 py-2 rounded-lg bg-amber-600 hover:bg-amber-500 text-white font-medium flex items-center gap-1.5 transition-colors"
                >
                  View Gazette PDF <ExternalLink className="w-3.5 h-3.5" />
                </a>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
