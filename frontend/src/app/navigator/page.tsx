"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import {
  Compass,
  ArrowRight,
  ShieldCheck,
  FileCheck,
  FlaskConical,
  CheckSquare,
  AlertTriangle,
  HelpCircle,
  Sparkles,
  ExternalLink,
  Layers
} from "lucide-react";
import { runNavigatorResearch, generateChecklist } from "@/lib/api";
import { ResearchWorkflowResponse } from "@/lib/types";

export default function NavigatorPage() {
  const router = useRouter();
  const [productName, setProductName] = useState("");
  const [category, setCategory] = useState("");
  const [intendedUse, setIntendedUse] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ResearchWorkflowResponse | null>(null);
  const [checklistGenerating, setChecklistGenerating] = useState(false);

  const handleAudit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!productName.trim() || loading) return;

    setLoading(true);
    try {
      const data = await runNavigatorResearch({
        product_name: productName.trim(),
        category: category.trim() || undefined,
        intended_use: intendedUse.trim() || undefined,
      });
      setResult(data);
    } catch (err) {
      console.error("Error executing navigator research", err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateChecklist = async () => {
    if (!result) return;
    setChecklistGenerating(true);
    try {
      const stdNum = result.potentially_relevant_standards[0]?.is_number;
      const scheme = result.certification_scheme?.code || "SCHEME_I";

      const checklist = await generateChecklist({
        product_name: result.product_name,
        standard_number: stdNum,
        scheme_code: scheme,
      });
      router.push(`/checklists?id=${checklist.id}`);
    } catch (err) {
      console.error("Failed to generate checklist", err);
    } finally {
      setChecklistGenerating(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Title */}
      <div className="pb-4 border-b border-slate-800">
        <h1 className="text-2xl font-bold text-white flex items-center gap-2">
          <Compass className="w-6 h-6 text-emerald-500" /> BIS Certification Navigator
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          End-to-end product compliance pathway: identify standards, check QCO mandates, determine scheme type, and prepare checklists.
        </p>
      </div>

      {/* Product Input Card */}
      <div className="p-6 md:p-8 rounded-2xl bg-slate-900 border border-slate-800 shadow-md">
        <form onSubmit={handleAudit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-1.5 md:col-span-1">
              <label className="text-xs font-semibold text-slate-300">
                Product Name or Description <span className="text-red-400">*</span>
              </label>
              <input
                type="text"
                required
                placeholder="e.g. Electric Storage Water Heater, Solar PV Module"
                value={productName}
                onChange={(e) => setProductName(e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-300">Product Category / Industry</label>
              <input
                type="text"
                placeholder="e.g. Household Electrical, Electronics, Solar Energy"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-300">Intended Application</label>
              <input
                type="text"
                placeholder="e.g. Domestic residential, Commercial, Industrial"
                value={intendedUse}
                onChange={(e) => setIntendedUse(e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-between pt-2 gap-3">
            <div className="flex flex-wrap gap-2 text-xs text-slate-400">
              <span>Quick Examples:</span>
              {[
                "Storage Water Heater (Geyser)",
                "Lithium Ion Power Bank",
                "Crystalline Solar PV Module",
                "TMT Steel Bar Fe 500D",
                "Non-Electric Wooden Toy"
              ].map((ex) => (
                <button
                  type="button"
                  key={ex}
                  onClick={() => {
                    setProductName(ex);
                    setCategory("General Industrial");
                  }}
                  className="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
                >
                  {ex}
                </button>
              ))}
            </div>

            <button
              type="submit"
              disabled={loading || !productName.trim()}
              className="px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-medium text-sm transition-colors shadow-lg shadow-emerald-600/20 flex items-center gap-2 disabled:opacity-50"
            >
              {loading ? "Analyzing Database..." : "Analyze Certification Pathway"}
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </form>
      </div>

      {/* Results Workflow */}
      {result && (
        <div className="space-y-8 animate-in fade-in-50 duration-300">
          {/* Summary Banner */}
          <div className="p-6 rounded-2xl bg-gradient-to-r from-slate-900 to-slate-850 border border-slate-800 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div>
              <div className="text-xs uppercase tracking-wider text-emerald-400 font-bold flex items-center gap-1.5">
                <Sparkles className="w-4 h-4" /> Comprehensive Regulatory Finding
              </div>
              <h2 className="text-2xl font-bold text-white mt-1">
                Compliance Roadmap for: {result.product_name}
              </h2>
            </div>
            <button
              onClick={handleGenerateChecklist}
              disabled={checklistGenerating}
              className="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-medium text-sm transition-colors flex items-center gap-2 shadow-lg shadow-blue-600/30 shrink-0"
            >
              <CheckSquare className="w-4 h-4" />
              {checklistGenerating ? "Creating Project..." : "Generate Project Checklist"}
            </button>
          </div>

          {/* 3 Column Grid: Scheme / QCO / Standards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* 1. Certification Scheme */}
            <div className="p-6 rounded-xl bg-slate-900 border border-slate-800 space-y-3">
              <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-purple-400">
                <ShieldCheck className="w-4 h-4" /> Certification Scheme
              </div>
              <h3 className="text-lg font-bold text-white">
                {result.certification_scheme?.name || "Scheme-I (ISI Mark)"}
              </h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                {result.certification_scheme?.description}
              </p>
              <div className="pt-3 border-t border-slate-800 space-y-1.5 text-xs text-slate-300">
                <div className="flex justify-between">
                  <span className="text-slate-500">Mark Name:</span>
                  <span className="font-semibold text-white">{result.certification_scheme?.mark_name}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Factory Audit:</span>
                  <span className={result.certification_scheme?.factory_audit_required ? "text-amber-400 font-semibold" : "text-slate-400"}>
                    {result.certification_scheme?.factory_audit_required ? "Mandatory On-Site" : "Exempt (Self-Declaration)"}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Typical Timeline:</span>
                  <span>{result.certification_scheme?.typical_timeline_weeks || 8} Weeks</span>
                </div>
              </div>
            </div>

            {/* 2. Mandatory QCO Order */}
            <div className="p-6 rounded-xl bg-slate-900 border border-slate-800 space-y-3">
              <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-amber-400">
                <FileCheck className="w-4 h-4" /> Quality Control Order (QCO)
              </div>
              {result.mandatory_qco_findings.length > 0 ? (
                <>
                  <div className="inline-block px-2.5 py-0.5 rounded text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">
                    Mandatory Certification Order In Force
                  </div>
                  <h3 className="text-sm font-bold text-white">
                    {result.mandatory_qco_findings[0].title}
                  </h3>
                  <div className="text-xs text-slate-400 space-y-1">
                    <div><strong>Order:</strong> {result.mandatory_qco_findings[0].order_number}</div>
                    <div><strong>Issuing Ministry:</strong> {result.mandatory_qco_findings[0].ministry}</div>
                    <div><strong>Status:</strong> {result.mandatory_qco_findings[0].status}</div>
                  </div>
                  {result.mandatory_qco_findings[0].official_url && (
                    <a
                      href={result.mandatory_qco_findings[0].official_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 text-xs text-blue-400 hover:underline pt-2"
                    >
                      View Gazette Order <ExternalLink className="w-3 h-3" />
                    </a>
                  )}
                </>
              ) : (
                <>
                  <div className="inline-block px-2.5 py-0.5 rounded text-xs font-bold bg-slate-800 text-slate-300">
                    Voluntary Certification / No QCO
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    No active mandatory Quality Control Order is currently linked to this classification in the database.
                  </p>
                </>
              )}
            </div>

            {/* 3. Applicable Indian Standards */}
            <div className="p-6 rounded-xl bg-slate-900 border border-slate-800 space-y-3">
              <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-blue-400">
                <Layers className="w-4 h-4" /> Applicable Standards ({result.potentially_relevant_standards.length})
              </div>
              <div className="space-y-2 max-h-56 overflow-y-auto">
                {result.potentially_relevant_standards.map((s, idx) => (
                  <div key={idx} className="p-2.5 rounded-lg bg-slate-950 border border-slate-800 text-xs space-y-1">
                    <div className="font-bold text-blue-400">{s.is_number}</div>
                    <div className="text-slate-300 line-clamp-2">{s.title}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Evidentiary Distinction (Verified Facts vs Unresolved Questions) */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-6 rounded-xl bg-slate-900 border border-slate-800 space-y-3">
              <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-400 flex items-center gap-1.5">
                <ShieldCheck className="w-4 h-4" /> Verified Facts from Records
              </h4>
              <ul className="space-y-2 text-xs text-slate-300">
                {result.verified_facts.map((fact, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <span className="text-emerald-500 font-bold">•</span>
                    <span>{fact}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="p-6 rounded-xl bg-slate-900 border border-slate-800 space-y-3">
              <h4 className="text-xs font-bold uppercase tracking-wider text-blue-400 flex items-center gap-1.5">
                <Sparkles className="w-4 h-4" /> Inferred Compliance Steps
              </h4>
              <ul className="space-y-2 text-xs text-slate-300">
                {result.inferred_relationships.map((inf, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <span className="text-blue-500 font-bold">•</span>
                    <span>{inf}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="p-6 rounded-xl bg-slate-900 border border-slate-800 space-y-3">
              <h4 className="text-xs font-bold uppercase tracking-wider text-amber-400 flex items-center gap-1.5">
                <HelpCircle className="w-4 h-4" /> Unresolved Technical Conditions
              </h4>
              <ul className="space-y-2 text-xs text-slate-300">
                {result.unresolved_questions.map((q, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <span className="text-amber-500 font-bold">•</span>
                    <span>{q}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Accredited Labs */}
          {result.recommended_laboratories.length > 0 && (
            <div className="p-6 rounded-xl bg-slate-900 border border-slate-800">
              <h3 className="text-base font-bold text-white mb-4 flex items-center gap-2">
                <FlaskConical className="w-5 h-5 text-emerald-400" /> Accredited Testing Facilities for this Scope
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {result.recommended_laboratories.map((lab, idx) => (
                  <div key={idx} className="p-4 rounded-xl bg-slate-950 border border-slate-800 text-xs space-y-2">
                    <div className="font-bold text-slate-200">{lab.name}</div>
                    <div className="text-slate-400">{lab.city}, {lab.state}</div>
                    <div className="text-[11px] text-emerald-400">Lab Code: {lab.lab_code}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
