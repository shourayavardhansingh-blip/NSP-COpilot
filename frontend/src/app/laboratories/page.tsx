"use client";

import { useEffect, useState } from "react";
import {
  FlaskConical,
  Search,
  MapPin,
  Phone,
  Mail,
  ExternalLink,
  Navigation as NavIcon,
  Filter,
  ShieldCheck,
  Calendar,
  X
} from "lucide-react";
import { fetchLaboratories, fetchLaboratoryDetail } from "@/lib/api";
import { LaboratorySummary, LaboratoryDetail } from "@/lib/types";

const STATES = [
  "All States",
  "Delhi",
  "Uttar Pradesh",
  "Maharashtra",
  "Karnataka",
  "Gujarat",
  "Tamil Nadu",
  "Haryana",
  "West Bengal"
];

export default function LaboratoriesPage() {
  const [labs, setLabs] = useState<LaboratorySummary[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);

  // Filters
  const [query, setQuery] = useState("");
  const [stateFilter, setStateFilter] = useState("All States");
  const [standardFilter, setStandardFilter] = useState("");

  // Geolocation
  const [userCoords, setUserCoords] = useState<{ lat: number; lon: number } | null>(null);
  const [geoLocating, setGeoLocating] = useState(false);
  const [geoError, setGeoError] = useState<string | null>(null);

  // Detail Modal
  const [selectedLab, setSelectedLab] = useState<LaboratoryDetail | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);

  const loadData = () => {
    setLoading(true);
    fetchLaboratories({
      q: query || undefined,
      state: stateFilter !== "All States" ? stateFilter : undefined,
      standard_is: standardFilter || undefined,
      user_lat: userCoords?.lat,
      user_lon: userCoords?.lon,
      limit: 50,
    })
      .then((res) => {
        setLabs(res.items);
        setTotal(res.total);
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadData();
  }, [stateFilter, standardFilter, userCoords]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    loadData();
  };

  const requestGeolocation = () => {
    if (!navigator.geolocation) {
      setGeoError("Geolocation is not supported by your browser.");
      return;
    }

    setGeoLocating(true);
    setGeoError(null);
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setUserCoords({
          lat: pos.coords.latitude,
          lon: pos.coords.longitude,
        });
        setGeoLocating(false);
      },
      (err) => {
        setGeoError("Location permission denied or unavailable. You can filter by City or State manually.");
        setGeoLocating(false);
      },
      { timeout: 10000 }
    );
  };

  const openDetail = (id: number) => {
    setDetailLoading(true);
    fetchLaboratoryDetail(id)
      .then((data) => setSelectedLab(data))
      .catch((err) => console.error(err))
      .finally(() => setDetailLoading(false));
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <FlaskConical className="w-6 h-6 text-emerald-500" /> Testing Laboratories Directory
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Search verified BIS Central, Regional, and recognized partner testing facilities with distance calculation
          </p>
        </div>

        {/* Search */}
        <form onSubmit={handleSearchSubmit} className="flex gap-2 w-full md:w-96">
          <div className="relative flex-1">
            <Search className="absolute left-3.5 top-3 w-4 h-4 text-slate-400" />
            <input
              type="text"
              placeholder="Search lab name, city, or pincode..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>
          <button
            type="submit"
            className="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-medium transition-colors"
          >
            Search
          </button>
        </form>
      </div>

      {/* Filter and Location Controls */}
      <div className="flex flex-wrap items-center gap-3 text-xs">
        <span className="text-slate-400 font-medium flex items-center gap-1">
          <Filter className="w-3.5 h-3.5" /> Filters:
        </span>

        {/* State Filter */}
        <select
          value={stateFilter}
          onChange={(e) => setStateFilter(e.target.value)}
          className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 focus:outline-none focus:ring-1 focus:ring-emerald-500"
        >
          {STATES.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>

        {/* Standard IS input */}
        <input
          type="text"
          placeholder="Filter by IS (e.g. IS 302)..."
          value={standardFilter}
          onChange={(e) => setStandardFilter(e.target.value)}
          className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 placeholder-slate-500 text-xs w-44 focus:outline-none focus:ring-1 focus:ring-emerald-500"
        />

        {/* Geolocation Trigger */}
        <button
          onClick={requestGeolocation}
          disabled={geoLocating}
          className={`px-3 py-1.5 rounded-lg border flex items-center gap-1.5 transition-colors ${
            userCoords
              ? "bg-emerald-500/20 border-emerald-500/40 text-emerald-300"
              : "bg-slate-900 border-slate-800 text-slate-400 hover:text-white"
          }`}
        >
          <NavIcon className="w-3.5 h-3.5" />
          {geoLocating ? "Locating..." : userCoords ? "Distance Sorted (GPS Active)" : "Find Closest to Me"}
        </button>

        {userCoords && (
          <button
            onClick={() => setUserCoords(null)}
            className="text-slate-500 hover:text-slate-300 transition-colors"
          >
            Clear GPS
          </button>
        )}

        <span className="ml-auto text-slate-500">
          Showing {labs.length} of {total} recognized facilities
        </span>
      </div>

      {geoError && (
        <div className="p-3 rounded-lg bg-amber-500/10 border border-amber-500/20 text-xs text-amber-300">
          {geoError}
        </div>
      )}

      {/* Grid of Laboratories */}
      {loading ? (
        <div className="p-12 text-center text-slate-400 text-sm">Loading testing laboratories...</div>
      ) : labs.length === 0 ? (
        <div className="p-12 text-center text-slate-400 text-sm bg-slate-900 rounded-xl border border-slate-800">
          No testing laboratories found matching the filter criteria.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {labs.map((lab) => (
            <div
              key={lab.id}
              onClick={() => openDetail(lab.id)}
              className="p-6 rounded-2xl bg-slate-900 border border-slate-800 hover:border-emerald-500/40 hover:bg-slate-850 cursor-pointer transition-all shadow-sm flex flex-col justify-between space-y-4"
            >
              <div className="space-y-2">
                <div className="flex items-center justify-between text-xs">
                  <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-800 text-slate-300 border border-slate-700">
                    {lab.lab_code}
                  </span>
                  {lab.distance_km !== null && lab.distance_km !== undefined && (
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                      {lab.distance_km} km away
                    </span>
                  )}
                </div>

                <h3 className="text-base font-bold text-white leading-snug line-clamp-2">{lab.name}</h3>
                <div className="flex items-start gap-1.5 text-xs text-slate-400">
                  <MapPin className="w-3.5 h-3.5 text-slate-500 shrink-0 mt-0.5" />
                  <span className="line-clamp-2">{lab.address}</span>
                </div>
              </div>

              <div className="pt-3 border-t border-slate-800/80 space-y-2 text-xs">
                <div className="flex items-center justify-between text-slate-400">
                  <span>Recognition Status:</span>
                  <span className="text-emerald-400 font-semibold">{lab.status}</span>
                </div>

                <div className="flex items-center justify-between text-slate-400">
                  <span>Accredited Scopes:</span>
                  <span className="font-semibold text-slate-200">{lab.scope_count} Indian Standards</span>
                </div>

                {lab.phone && (
                  <div className="flex items-center gap-1.5 text-slate-400 pt-1">
                    <Phone className="w-3 h-3 text-slate-500" />
                    <span>{lab.phone}</span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Lab Detail Modal */}
      {selectedLab && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto shadow-2xl p-6 md:p-8 space-y-6">
            <div className="flex items-start justify-between border-b border-slate-800 pb-4">
              <div>
                <span className="px-2.5 py-0.5 rounded text-xs font-bold bg-slate-800 text-slate-300">
                  {selectedLab.lab_code}
                </span>
                <h2 className="text-xl font-bold text-white mt-1.5">{selectedLab.name}</h2>
                <div className="flex items-center gap-2 text-xs text-slate-400 mt-1">
                  <span>{selectedLab.lab_type}</span>
                  <span>•</span>
                  <span className="text-emerald-400 font-semibold">{selectedLab.status}</span>
                </div>
              </div>
              <button
                onClick={() => setSelectedLab(null)}
                className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Address & Contact Info */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs bg-slate-950 p-4 rounded-xl border border-slate-800">
              <div className="space-y-1">
                <div className="font-semibold text-slate-300 flex items-center gap-1.5">
                  <MapPin className="w-3.5 h-3.5 text-slate-500" /> Facility Address
                </div>
                <div className="text-slate-400">{selectedLab.address}</div>
                <div className="text-slate-400">{selectedLab.city}, {selectedLab.state} - {selectedLab.pincode}</div>
              </div>
              <div className="space-y-1">
                <div className="font-semibold text-slate-300">Contact Details</div>
                {selectedLab.contact_person && <div className="text-slate-400">Officer: {selectedLab.contact_person}</div>}
                {selectedLab.phone && <div className="text-slate-400">Phone: {selectedLab.phone}</div>}
                {selectedLab.email && <div className="text-slate-400">Email: {selectedLab.email}</div>}
                {selectedLab.recognition_valid_until && (
                  <div className="text-amber-400 pt-1">Valid Until: {selectedLab.recognition_valid_until}</div>
                )}
              </div>
            </div>

            {/* Accredited Scopes */}
            <div>
              <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                <FlaskConical className="w-3.5 h-3.5 text-emerald-400" /> Accredited Indian Standard Scopes ({selectedLab.scopes.length})
              </h4>
              <div className="space-y-2 max-h-60 overflow-y-auto">
                {selectedLab.scopes.map((scope) => (
                  <div key={scope.id} className="p-3 rounded-lg bg-slate-950 border border-slate-800 text-xs space-y-1">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-blue-400">{scope.is_number}</span>
                      <span className="text-slate-500 text-[11px]">{scope.product_category || "Testing Scope"}</span>
                    </div>
                    <div className="text-slate-300 font-medium">{scope.standard_title}</div>
                    {scope.testing_capability && (
                      <div className="text-slate-400 text-[11px]">Capability: {scope.testing_capability}</div>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Official Source Link */}
            <div className="pt-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-500">
              <span>Verified via BIS LIMS Directory</span>
              {selectedLab.source_url && (
                <a
                  href={selectedLab.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-medium flex items-center gap-1.5 transition-colors"
                >
                  View Laboratory Portal <ExternalLink className="w-3.5 h-3.5" />
                </a>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
