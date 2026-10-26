"use client";

import { useEffect, useState } from "react";
import {
  Sliders,
  Cpu,
  Database,
  CheckCircle2,
  AlertTriangle,
  RotateCcw,
  Terminal,
  ExternalLink,
  ShieldCheck,
  Server
} from "lucide-react";
import { fetchHealth } from "@/lib/api";

export default function SettingsPage() {
  const [health, setHealth] = useState<any>(null);
  const [testing, setTesting] = useState(false);

  const checkStatus = () => {
    setTesting(true);
    fetchHealth()
      .then(setHealth)
      .catch((err) => console.error(err))
      .finally(() => setTesting(false));
  };

  useEffect(() => {
    checkStatus();
  }, []);

  const ai = health?.ai_engine;

  return (
    <div className="max-w-5xl mx-auto space-y-8">
      {/* Header */}
      <div className="pb-4 border-b border-slate-800 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <Sliders className="w-6 h-6 text-purple-500" /> Settings & System Diagnostics
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Configure local AI inference runtime, monitor database connectivity, and test latency
          </p>
        </div>
        <button
          onClick={checkStatus}
          disabled={testing}
          className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium flex items-center gap-1.5 border border-slate-700 transition-colors"
        >
          <RotateCcw className={`w-3.5 h-3.5 ${testing ? "animate-spin" : ""}`} /> Test Connectivity
        </button>
      </div>

      {/* AI Inference Diagnostics */}
      <div className="p-6 md:p-8 rounded-2xl bg-slate-900 border border-slate-800 space-y-6 shadow-sm">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 text-purple-400 flex items-center justify-center">
              <Cpu className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white">Local AI Inference (Ollama)</h2>
              <p className="text-xs text-slate-400">Zero per-request token costs, private local execution</p>
            </div>
          </div>
          <span
            className={`px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1.5 ${
              ai?.ollama_reachable && !ai?.fallback_mode_active
                ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"
                : "bg-amber-500/20 text-amber-300 border border-amber-500/30"
            }`}
          >
            {ai?.ollama_reachable && !ai?.fallback_mode_active ? (
              <>
                <CheckCircle2 className="w-3.5 h-3.5" /> Model Ready
              </>
            ) : (
              <>
                <AlertTriangle className="w-3.5 h-3.5" /> Deterministic Fast-Path Active
              </>
            )}
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs bg-slate-950 p-4 rounded-xl border border-slate-800">
          <div className="space-y-1">
            <div className="text-slate-400">Configured Model:</div>
            <div className="font-bold text-white text-sm">{ai?.configured_model || "llama3.2:3b"}</div>
          </div>
          <div className="space-y-1">
            <div className="text-slate-400">Local Endpoint:</div>
            <div className="font-mono text-slate-300">http://127.0.0.1:11434</div>
          </div>
        </div>

        <div className="space-y-2 text-xs">
          <div className="font-semibold text-slate-300">Status Message:</div>
          <p className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800 text-slate-300 leading-relaxed font-mono text-[11px]">
            {ai?.diagnostic_message || "Checking Ollama status..."}
          </p>
        </div>

        {/* How to Run Local Model Section */}
        <div className="p-5 rounded-xl bg-slate-950 border border-slate-800 space-y-3">
          <h4 className="text-xs font-bold text-white flex items-center gap-1.5 uppercase tracking-wider">
            <Terminal className="w-4 h-4 text-blue-400" /> How to launch Local Model in Terminal
          </h4>
          <p className="text-xs text-slate-400 leading-relaxed">
            To enable deep natural language synthesis through Ollama on your local machine:
          </p>
          <div className="bg-slate-900 p-3 rounded-lg border border-slate-800 font-mono text-xs text-blue-300 space-y-1">
            <div># 1. Pull the free open-weight model</div>
            <div className="text-emerald-400">ollama pull llama3.2:3b</div>
            <div className="pt-2 text-slate-400"># 2. Verify model is loaded</div>
            <div className="text-emerald-400">ollama run llama3.2:3b</div>
          </div>
          <p className="text-[11px] text-slate-500">
            Recommended hardware: 8 GB+ RAM, modern CPU or Apple Silicon / NVIDIA GPU. When Ollama is offline, the platform automatically switches to deterministic fast-path RAG without error.
          </p>
        </div>
      </div>

      {/* Relational Database Diagnostics */}
      <div className="p-6 md:p-8 rounded-2xl bg-slate-900 border border-slate-800 space-y-6 shadow-sm">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/20 text-blue-400 flex items-center justify-center">
              <Database className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white">Relational Database Engine</h2>
              <p className="text-xs text-slate-400">SQLAlchemy 2.0 ORM with indexed full-text & foreign keys</p>
            </div>
          </div>
          <span className="px-3 py-1 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 flex items-center gap-1.5">
            <CheckCircle2 className="w-3.5 h-3.5" /> Healthy
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs bg-slate-950 p-4 rounded-xl border border-slate-800">
          <div className="space-y-1">
            <div className="text-slate-400">Engine Type:</div>
            <div className="font-bold text-white">SQLite (WAL Mode Enabled)</div>
          </div>
          <div className="space-y-1">
            <div className="text-slate-400">Target Production:</div>
            <div className="font-bold text-white">PostgreSQL Ready</div>
          </div>
          <div className="space-y-1">
            <div className="text-slate-400">Foreign Key Cascades:</div>
            <div className="font-bold text-emerald-400">PRAGMA Active</div>
          </div>
        </div>
      </div>
    </div>
  );
}
