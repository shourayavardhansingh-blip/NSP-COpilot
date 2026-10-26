"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Bot,
  Search,
  Compass,
  FlaskConical,
  FileCheck,
  CheckSquare,
  Globe2,
  Database,
  Sliders,
  ShieldCheck,
} from "lucide-react";

const navItems = [
  { name: "Overview", href: "/", icon: LayoutDashboard },
  { name: "AI Assistant", href: "/assistant", icon: Bot },
  { name: "Standard Explorer", href: "/standards", icon: Search },
  { name: "Certification Navigator", href: "/navigator", icon: Compass },
  { name: "Testing Laboratories", href: "/laboratories", icon: FlaskConical },
  { name: "QCO Explorer", href: "/qco", icon: FileCheck },
  { name: "Checklist Maker", href: "/checklists", icon: CheckSquare },
  { name: "Official Sources", href: "/sources", icon: Globe2 },
  { name: "Data Coverage", href: "/coverage", icon: Database },
  { name: "Settings & AI Health", href: "/settings", icon: Sliders },
];

export default function Navigation() {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col h-screen sticky top-0">
      <div className="p-5 border-b border-slate-800 flex items-center space-x-3">
        <div className="w-10 h-10 rounded-lg bg-blue-600 flex items-center justify-center text-white shadow-md shadow-blue-500/20">
          <ShieldCheck className="w-6 h-6" />
        </div>
        <div>
          <h1 className="font-bold text-base tracking-tight text-white flex items-center gap-1.5">
            BIS AI Copilot
            <span className="text-[10px] uppercase font-semibold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 border border-blue-500/30">
              v1.0
            </span>
          </h1>
          <p className="text-xs text-slate-400">Industrial Intelligence</p>
        </div>
      </div>

      <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href || (item.href !== "/" && pathname.startsWith(item.href));

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? "bg-blue-600 text-white shadow-sm"
                  : "text-slate-300 hover:bg-slate-800/70 hover:text-white"
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? "text-white" : "text-slate-400"}`} />
              {item.name}
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-slate-800 text-xs text-slate-500 bg-slate-950/40">
        <div className="flex items-center gap-2 mb-1.5">
          <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          <span className="text-slate-300 font-medium">Relational Engine Live</span>
        </div>
        <p className="text-[11px] leading-relaxed">
          Grounding queries across official Indian Standards & Gazette QCOs.
        </p>
      </div>
    </aside>
  );
}
