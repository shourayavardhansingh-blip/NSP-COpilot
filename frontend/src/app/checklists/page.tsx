"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import {
  CheckSquare,
  Plus,
  Trash2,
  Download,
  Printer,
  CheckCircle2,
  Circle,
  FileText,
  Sparkles,
  ExternalLink,
  ChevronRight,
  Edit2
} from "lucide-react";
import {
  fetchChecklists,
  fetchChecklistDetail,
  createChecklist,
  updateTask,
  addTaskToChecklist,
  deleteTask,
  deleteChecklist
} from "@/lib/api";
import { ChecklistSummary, ChecklistDetail, ChecklistTask } from "@/lib/types";

function ChecklistsContent() {
  const searchParams = useSearchParams();
  const initialChecklistId = searchParams.get("id");

  const [checklists, setChecklists] = useState<ChecklistSummary[]>([]);
  const [selectedChecklist, setSelectedChecklist] = useState<ChecklistDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [filterMode, setFilterMode] = useState<"all" | "pending" | "completed">("all");

  // Create Modal State
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newTitle, setNewTitle] = useState("");
  const [newProduct, setNewProduct] = useState("");
  const [newStandard, setNewStandard] = useState("");
  const [newScheme, setNewScheme] = useState("SCHEME_I");

  // Add Task Input State
  const [newTaskTitle, setNewTaskTitle] = useState("");
  const [newTaskStage, setNewTaskStage] = useState("Documentation");
  const [isTaskMandatory, setIsTaskMandatory] = useState(true);

  const loadChecklists = (selectId?: string) => {
    setLoading(true);
    fetchChecklists()
      .then((data) => {
        setChecklists(data);
        const targetId = selectId || initialChecklistId || (data.length > 0 ? data[0].id : null);
        if (targetId) {
          fetchChecklistDetail(targetId).then(setSelectedChecklist);
        } else {
          setSelectedChecklist(null);
        }
      })
      .catch((err) => console.error("Error loading checklists", err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadChecklists();
  }, []);

  const handleSelectChecklist = (id: string) => {
    fetchChecklistDetail(id).then(setSelectedChecklist);
  };

  const handleCreateChecklist = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim() || !newProduct.trim()) return;

    try {
      const created = await createChecklist({
        title: newTitle.trim(),
        product_name: newProduct.trim(),
        standard_number: newStandard.trim() || undefined,
        scheme_code: newScheme,
      });
      setShowCreateModal(false);
      setNewTitle("");
      setNewProduct("");
      setNewStandard("");
      loadChecklists(created.id);
    } catch (err) {
      console.error(err);
    }
  };

  const handleToggleTask = async (task: ChecklistTask) => {
    if (!selectedChecklist) return;
    try {
      const updated = await updateTask(selectedChecklist.id, task.id, {
        is_completed: !task.is_completed,
      });
      setSelectedChecklist(updated);
      setChecklists((prev) =>
        prev.map((c) => (c.id === updated.id ? { ...c, completed_tasks: updated.completed_tasks, completion_percentage: updated.completion_percentage } : c))
      );
    } catch (err) {
      console.error("Failed to toggle task", err);
    }
  };

  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedChecklist || !newTaskTitle.trim()) return;

    try {
      const updated = await addTaskToChecklist(selectedChecklist.id, {
        title: newTaskTitle.trim(),
        stage: newTaskStage,
        is_mandatory: isTaskMandatory,
      });
      setSelectedChecklist(updated);
      setNewTaskTitle("");
      setChecklists((prev) =>
        prev.map((c) => (c.id === updated.id ? { ...c, total_tasks: updated.total_tasks } : c))
      );
    } catch (err) {
      console.error("Failed to add task", err);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    if (!selectedChecklist) return;
    try {
      await deleteTask(selectedChecklist.id, taskId);
      const updated = await fetchChecklistDetail(selectedChecklist.id);
      setSelectedChecklist(updated);
      setChecklists((prev) =>
        prev.map((c) => (c.id === updated.id ? { ...c, total_tasks: updated.total_tasks, completed_tasks: updated.completed_tasks } : c))
      );
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteChecklist = async (id: string) => {
    if (!confirm("Are you sure you want to delete this checklist?")) return;
    try {
      await deleteChecklist(id);
      loadChecklists();
    } catch (err) {
      console.error(err);
    }
  };

  const filteredTasks = (selectedChecklist?.tasks || []).filter((task) => {
    if (filterMode === "pending") return !task.is_completed;
    if (filterMode === "completed") return task.is_completed;
    return true;
  });

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <CheckSquare className="w-6 h-6 text-purple-500" /> Compliance Checklist Maker
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Build and track persistent audit projects, documentation milestones, factory readiness, and lab testing
          </p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-sm font-medium transition-colors flex items-center gap-2 shadow-lg shadow-purple-600/30"
        >
          <Plus className="w-4 h-4" /> New Compliance Project
        </button>
      </div>

      {/* Main Split Layout: Sidebar of Checklists + Active Checklist View */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 items-start">
        {/* Checklist Sidebar List */}
        <div className="rounded-2xl border border-slate-800 bg-slate-900 p-4 space-y-3">
          <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider px-2">
            Saved Projects ({checklists.length})
          </div>
          {checklists.length === 0 ? (
            <div className="p-6 text-center text-xs text-slate-500">
              No compliance projects created yet. Click "New Compliance Project" or use the Certification Navigator.
            </div>
          ) : (
            <div className="space-y-1.5">
              {checklists.map((c) => {
                const isSelected = selectedChecklist?.id === c.id;
                return (
                  <div
                    key={c.id}
                    onClick={() => handleSelectChecklist(c.id)}
                    className={`p-3.5 rounded-xl cursor-pointer transition-all border ${
                      isSelected
                        ? "bg-slate-800 border-purple-500/50 shadow-sm"
                        : "bg-slate-950/40 border-slate-800/80 hover:bg-slate-800/50 text-slate-300"
                    }`}
                  >
                    <div className="font-bold text-sm text-white line-clamp-1">{c.title}</div>
                    <div className="text-xs text-slate-400 mt-0.5">{c.product_name}</div>
                    <div className="mt-2.5 flex items-center justify-between text-[11px] text-slate-500">
                      <span>{c.completed_tasks}/{c.total_tasks} Tasks</span>
                      <span className="font-semibold text-purple-400">{c.completion_percentage}%</span>
                    </div>
                    {/* Mini progress bar */}
                    <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden mt-1.5">
                      <div
                        className="bg-purple-500 h-full transition-all duration-300"
                        style={{ width: `${c.completion_percentage}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Active Checklist Detail View */}
        <div className="lg:col-span-3 space-y-6">
          {selectedChecklist ? (
            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6 md:p-8 space-y-6 shadow-md">
              {/* Project Header Info */}
              <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-6 border-b border-slate-800">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="px-2.5 py-0.5 rounded text-xs font-semibold bg-purple-500/20 text-purple-300 border border-purple-500/30">
                      {selectedChecklist.scheme_code || "SCHEME_I"}
                    </span>
                    {selectedChecklist.standard_number && (
                      <span className="px-2.5 py-0.5 rounded text-xs font-semibold bg-blue-500/20 text-blue-300 border border-blue-500/30">
                        {selectedChecklist.standard_number}
                      </span>
                    )}
                  </div>
                  <h2 className="text-2xl font-bold text-white">{selectedChecklist.title}</h2>
                  <p className="text-xs text-slate-400">Target Product: {selectedChecklist.product_name}</p>
                </div>

                <div className="flex items-center gap-2">
                  <a
                    href={`/api/checklists/${selectedChecklist.id}/export/csv`}
                    download
                    className="px-3.5 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium flex items-center gap-1.5 border border-slate-700 transition-colors"
                  >
                    <Download className="w-3.5 h-3.5" /> Export CSV
                  </a>
                  <button
                    onClick={() => window.print()}
                    className="px-3.5 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium flex items-center gap-1.5 border border-slate-700 transition-colors"
                  >
                    <Printer className="w-3.5 h-3.5" /> Print
                  </button>
                  <button
                    onClick={() => handleDeleteChecklist(selectedChecklist.id)}
                    className="p-2 rounded-lg bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/30 transition-colors"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>

              {/* Progress Bar & Filter Tabs */}
              <div className="space-y-3 bg-slate-950 p-4 rounded-xl border border-slate-800">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-semibold text-slate-300">
                    Completion Status: {selectedChecklist.completed_tasks} of {selectedChecklist.total_tasks} Tasks Finished
                  </span>
                  <span className="font-extrabold text-purple-400 text-sm">
                    {selectedChecklist.completion_percentage}%
                  </span>
                </div>
                <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden">
                  <div
                    className="bg-gradient-to-r from-purple-500 to-blue-500 h-full transition-all duration-300"
                    style={{ width: `${selectedChecklist.completion_percentage}%` }}
                  />
                </div>
              </div>

              {/* Filter Tabs */}
              <div className="flex items-center gap-2 border-b border-slate-800 pb-2 text-xs">
                {(["all", "pending", "completed"] as const).map((mode) => (
                  <button
                    key={mode}
                    onClick={() => setFilterMode(mode)}
                    className={`px-3 py-1.5 rounded-lg capitalize transition-colors font-medium ${
                      filterMode === mode
                        ? "bg-purple-600 text-white"
                        : "text-slate-400 hover:text-white hover:bg-slate-800"
                    }`}
                  >
                    {mode} ({mode === "all" ? selectedChecklist.tasks.length : mode === "pending" ? selectedChecklist.total_tasks - selectedChecklist.completed_tasks : selectedChecklist.completed_tasks})
                  </button>
                ))}
              </div>

              {/* Task Items List */}
              <div className="space-y-3">
                {filteredTasks.length === 0 ? (
                  <div className="p-8 text-center text-xs text-slate-500">
                    No tasks found in this view.
                  </div>
                ) : (
                  filteredTasks.map((t) => (
                    <div
                      key={t.id}
                      className={`p-4 rounded-xl border transition-colors flex items-start gap-3.5 ${
                        t.is_completed
                          ? "bg-slate-950/40 border-slate-800/60 opacity-70"
                          : "bg-slate-950 border-slate-800"
                      }`}
                    >
                      <button
                        onClick={() => handleToggleTask(t)}
                        className="mt-0.5 text-slate-400 hover:text-purple-400 transition-colors shrink-0"
                      >
                        {t.is_completed ? (
                          <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                        ) : (
                          <Circle className="w-5 h-5" />
                        )}
                      </button>

                      <div className="flex-1 space-y-1">
                        <div className="flex items-center gap-2">
                          <span className={`font-semibold text-sm ${t.is_completed ? "line-through text-slate-400" : "text-white"}`}>
                            {t.title}
                          </span>
                          <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-800 text-slate-400">
                            {t.stage}
                          </span>
                          {t.is_mandatory && (
                            <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-amber-500/20 text-amber-300">
                              Mandatory
                            </span>
                          )}
                        </div>
                        {t.description && (
                          <p className="text-xs text-slate-400 leading-relaxed">{t.description}</p>
                        )}
                        {t.source_citation && (
                          <div className="text-[11px] text-blue-400 flex items-center gap-1 pt-1 font-medium">
                            <FileText className="w-3 h-3" /> Source: {t.source_citation}
                          </div>
                        )}
                      </div>

                      <button
                        onClick={() => handleDeleteTask(t.id)}
                        className="p-1 rounded text-slate-600 hover:text-red-400 transition-colors shrink-0"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  ))
                )}
              </div>

              {/* Add New Task Form */}
              <form onSubmit={handleAddTask} className="pt-4 border-t border-slate-800 flex flex-col sm:flex-row gap-3">
                <input
                  type="text"
                  placeholder="Add custom compliance task..."
                  value={newTaskTitle}
                  onChange={(e) => setNewTaskTitle(e.target.value)}
                  className="flex-1 px-3.5 py-2 rounded-xl bg-slate-950 border border-slate-700 text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-1 focus:ring-purple-500"
                />
                <select
                  value={newTaskStage}
                  onChange={(e) => setNewTaskStage(e.target.value)}
                  className="px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-slate-300 text-xs focus:outline-none"
                >
                  <option value="Documentation">Documentation</option>
                  <option value="Pre-Testing">Pre-Testing</option>
                  <option value="Factory Audit">Factory Audit</option>
                  <option value="Application Submission">Application Submission</option>
                  <option value="Grant of Licence">Grant of Licence</option>
                </select>
                <button
                  type="submit"
                  disabled={!newTaskTitle.trim()}
                  className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-semibold flex items-center gap-1.5 transition-colors disabled:opacity-50"
                >
                  <Plus className="w-3.5 h-3.5" /> Add Task
                </button>
              </form>
            </div>
          ) : (
            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-12 text-center text-slate-400">
              Select or create a compliance project to begin tracking tasks.
            </div>
          )}
        </div>
      </div>

      {/* New Project Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-md w-full p-6 space-y-4 shadow-2xl">
            <h3 className="text-lg font-bold text-white">Create New Compliance Project</h3>
            <form onSubmit={handleCreateChecklist} className="space-y-3">
              <div>
                <label className="text-xs text-slate-400">Project Title</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Geyser 15L ISI Certification 2026"
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white text-sm focus:outline-none mt-1"
                />
              </div>
              <div>
                <label className="text-xs text-slate-400">Product Name</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Electric Storage Water Heater"
                  value={newProduct}
                  onChange={(e) => setNewProduct(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white text-sm focus:outline-none mt-1"
                />
              </div>
              <div>
                <label className="text-xs text-slate-400">Indian Standard (Optional)</label>
                <input
                  type="text"
                  placeholder="e.g. IS 302 (Part 2/Sec 21)"
                  value={newStandard}
                  onChange={(e) => setNewStandard(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white text-sm focus:outline-none mt-1"
                />
              </div>
              <div>
                <label className="text-xs text-slate-400">Certification Scheme</label>
                <select
                  value={newScheme}
                  onChange={(e) => setNewScheme(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-slate-200 text-sm focus:outline-none mt-1"
                >
                  <option value="SCHEME_I">Scheme-I (ISI Mark - Product Certification)</option>
                  <option value="SCHEME_II">Scheme-II (CRS - Compulsory Registration)</option>
                  <option value="SCHEME_IV">Scheme-IV (Certificate of Conformity)</option>
                </select>
              </div>

              <div className="flex justify-end gap-2 pt-3">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-4 py-2 rounded-lg bg-slate-800 text-slate-300 text-xs font-medium"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-lg bg-purple-600 hover:bg-purple-500 text-white text-xs font-semibold"
                >
                  Create Project
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}


export default function ChecklistsPage() {
  return (
    <Suspense fallback={<div className="p-12 text-center text-slate-400">Loading Checklist Maker...</div>}>
      <ChecklistsContent />
    </Suspense>
  );
}
