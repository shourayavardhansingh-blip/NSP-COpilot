"use client";

import { useEffect, useState } from "react";
import { Globe2, ExternalLink, ShieldCheck, CheckCircle2, Clock, BookOpen, AlertCircle } from "lucide-react";

interface SourceItem {
  id: number;
  name: string;
  portal_type: string;
  base_url: string;
  licensing_terms?: string;
  update_frequency: string;
  status: string;
  last_polled_at?: string;
  last_success_at?: string;
  notes?: string;
}

export default function SourcesPage() {
  const [sources, setSources] = useState<SourceItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/sources")
      .then((res) => res.json())
      .then((data) => setSources(data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div className="pb-4 border-b border-slate-800">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <Globe2 className="w-6 h-6 text-blue-500" /> Official Sources & Data Provenance
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Traceable directory of official Bureau of Indian Standards portals, Gazette repositories, and legal reuse parameters
        </p>
      </div>

      {/* Advisory Banner */}
      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 flex items-start gap-4">
        <ShieldCheck className="w-6 h-6 text-emerald-400 shrink-0 mt-0.5" />
        <div className="text-xs text-slate-300 space-y-1 leading-relaxed">
          <div className="font-bold text-white text-sm">Authoritative Provenance Policy</div>
          <p>
            BIS AI Copilot indexes metadata, publicly permitted scopes, gazette Quality Control Orders, and laboratory recognition directories published by Government of India authorities.
            Full standard specifications (formulas, technical drawings, test step sequences) remain the exclusive intellectual property of the Bureau of Indian Standards.
          </p>
        </div>
      </div>

      {/* Sources Grid */}
      {loading ? (
        <div className="p-12 text-center text-slate-400 text-sm">Loading official source repositories...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {sources.map((src) => (
            <div
              key={src.id}
              className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-sm flex flex-col justify-between space-y-4"
            >
              <div className="space-y-2">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-semibold text-blue-400">{src.portal_type}</span>
                  <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 flex items-center gap-1">
                    <CheckCircle2 className="w-3 h-3" /> {src.status}
                  </span>
                </div>
                <h3 className="text-lg font-bold text-white">{src.name}</h3>
                <p className="text-xs text-slate-400 leading-relaxed">
                  {src.licensing_terms || "Public Government Data under Ministry Guidelines"}
                </p>
              </div>

              <div className="pt-3 border-t border-slate-800/80 space-y-2 text-xs">
                <div className="flex items-center justify-between text-slate-400">
                  <span className="flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5 text-slate-500" /> Polling Cadence:
                  </span>
                  <span className="font-semibold text-slate-300">{src.update_frequency}</span>
                </div>
                {src.last_success_at && (
                  <div className="text-[11px] text-slate-500">
                    Last Verified: {src.last_success_at.slice(0, 10)}
                  </div>
                )}
                <a
                  href={src.base_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="pt-2 text-blue-400 hover:text-blue-300 hover:underline inline-flex items-center gap-1 font-medium"
                >
                  Visit Official Source Portal <ExternalLink className="w-3.5 h-3.5" />
                </a>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
