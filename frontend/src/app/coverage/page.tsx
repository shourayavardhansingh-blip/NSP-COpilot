"use client";

import { useEffect, useState } from "react";
import {
  Database,
  ShieldCheck,
  AlertTriangle,
  Layers,
  FileCheck,
  FlaskConical,
  CheckCircle2,
  Calendar,
  AlertCircle
} from "lucide-react";
import { fetchCoverageDashboard } from "@/lib/api";
import { CoverageDashboardResponse } from "@/lib/types";

export default function CoveragePage() {
  const [data, setData] = useState<CoverageDashboardResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCoverageDashboard()
      .then(setData)
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  const stats = data?.stats;

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      {/* Header */}
      <div className="pb-4 border-b border-slate-800">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <Database className="w-6 h-6 text-blue-500" /> Data Coverage & Governance Dashboard
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Audit database completeness, ingestion batch statistics, dataset freshness, and statutory boundaries
        </p>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="p-6 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
          <div className="text-xs uppercase tracking-wider text-slate-400 font-medium">Verified Standards</div>
          <div className="text-3xl font-extrabold text-white">{stats?.verified_standards || 0}</div>
          <div className="text-[11px] text-slate-500">
            {stats?.fixture_standards === 0 ? "0 Test Fixtures (100% Official)" : `${stats?.fixture_standards} Sample Fixtures`}
          </div>
        </div>

        <div className="p-6 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
          <div className="text-xs uppercase tracking-wider text-slate-400 font-medium">Quality Control Orders</div>
          <div className="text-3xl font-extrabold text-amber-400">{stats?.total_qcos || 0}</div>
          <div className="text-[11px] text-slate-500">
            {stats?.active_qcos || 0} Active Decrees with Gazette Links
          </div>
        </div>

        <div className="p-6 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
          <div className="text-xs uppercase tracking-wider text-slate-400 font-medium">Testing Laboratories</div>
          <div className="text-3xl font-extrabold text-emerald-400">{stats?.total_laboratories || 0}</div>
          <div className="text-[11px] text-slate-500">
            {stats?.total_scopes_mapped || 0} Tested Standard Scopes Mapped
          </div>
        </div>

        <div className="p-6 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
          <div className="text-xs uppercase tracking-wider text-slate-400 font-medium">Dataset Freshness</div>
          <div className="text-base font-bold text-slate-200">
            {stats?.dataset_freshness_date?.slice(0, 10) || "Current"}
          </div>
          <div className="text-[11px] text-emerald-400 flex items-center gap-1 font-medium">
            <CheckCircle2 className="w-3.5 h-3.5" /> Synchronized with Gazette
          </div>
        </div>
      </div>

      {/* Coverage Gaps & Boundaries */}
      <div className="p-6 md:p-8 rounded-2xl bg-slate-900 border border-slate-800 space-y-4">
        <div className="flex items-center gap-2">
          <AlertCircle className="w-5 h-5 text-amber-400" />
          <h2 className="text-lg font-bold text-white">Coverage Limits & Legal Boundaries</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {(data?.coverage_gaps || []).map((gap, idx) => (
            <div key={idx} className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2 text-xs">
              <div className="flex items-center justify-between">
                <span className="font-bold text-amber-300">{gap.category}</span>
                <span className="px-2 py-0.5 rounded text-[10px] bg-slate-800 text-slate-400">{gap.status}</span>
              </div>
              <p className="text-slate-300 leading-relaxed">{gap.description}</p>
              <div className="pt-2 border-t border-slate-800/80 text-[11px] text-slate-400">
                <strong>Platform Action:</strong> {gap.action_required}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Ingestion Batch Runs */}
      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-4">
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <Layers className="w-5 h-5 text-blue-400" /> Ingestion Audit Trail & Ingestion Runs
        </h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-950 text-slate-400 uppercase tracking-wider text-[11px] border-b border-slate-800">
              <tr>
                <th className="py-3 px-4">Dataset Name</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4">Records Processed</th>
                <th className="py-3 px-4">Upserted</th>
                <th className="py-3 px-4">Rejected</th>
                <th className="py-3 px-4">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {(data?.recent_ingestion_runs || []).map((run) => (
                <tr key={run.id} className="hover:bg-slate-850/60">
                  <td className="py-3 px-4 font-semibold text-white">{run.dataset_name}</td>
                  <td className="py-3 px-4">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300">
                      {run.status}
                    </span>
                  </td>
                  <td className="py-3 px-4">{run.records_processed}</td>
                  <td className="py-3 px-4 text-emerald-400 font-semibold">{run.records_upserted}</td>
                  <td className="py-3 px-4 text-slate-500">{run.records_rejected}</td>
                  <td className="py-3 px-4 text-slate-400">{run.started_at?.slice(0, 19).replace("T", " ")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
