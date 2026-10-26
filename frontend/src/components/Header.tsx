"use client";

import { useEffect, useState } from "react";
import { fetchHealth } from "@/lib/api";
import { ShieldAlert, Cpu, Database, CheckCircle2, AlertTriangle, XCircle } from "lucide-react";

export default function Header() {
  const [health, setHealth] = useState<any>(null);

  useEffect(() => {
    fetchHealth()
      .then(setHealth)
      .catch((err) => console.error("Health check error", err));
  }, []);

  const aiStatus = health?.ai_engine?.status || "checking";
  const dbStatus = health?.database || "checking";

  return (
    <header className="h-16 border-b border-slate-800 bg-slate-900/60 backdrop-blur px-8 flex items-center justify-between sticky top-0 z-20">
      <div className="flex items-center gap-3 text-xs text-slate-400">
        <span className="font-semibold text-slate-200">Regulatory Advisory Notice:</span>
        <span className="hidden md:inline text-slate-400">
          Independent compliance platform. For statutory licensing, verify records on official BIS portals.
        </span>
      </div>

      <div className="flex items-center gap-4 text-xs">
        {/* Database Badge */}
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-slate-800 border border-slate-700">
          <Database className="w-3.5 h-3.5 text-blue-400" />
          <span className="text-slate-300">DB:</span>
          {dbStatus === "healthy" ? (
            <span className="text-emerald-400 font-medium flex items-center gap-1">
              <CheckCircle2 className="w-3 h-3" /> Online
            </span>
          ) : (
            <span className="text-amber-400 font-medium flex items-center gap-1">
              <AlertTriangle className="w-3 h-3" /> Syncing
            </span>
          )}
        </div>

        {/* AI Badge */}
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-slate-800 border border-slate-700">
          <Cpu className="w-3.5 h-3.5 text-purple-400" />
          <span className="text-slate-300">AI:</span>
          {aiStatus === "healthy" ? (
            <span className="text-emerald-400 font-medium flex items-center gap-1">
              <CheckCircle2 className="w-3 h-3" /> Ollama Active
            </span>
          ) : (
            <span className="text-amber-400 font-medium flex items-center gap-1" title={health?.ai_engine?.diagnostic_message}>
              <CheckCircle2 className="w-3 h-3" /> Fast-Path RAG
            </span>
          )}
        </div>
      </div>
    </header>
  );
}
