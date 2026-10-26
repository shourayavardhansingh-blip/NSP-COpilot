import {
  StandardSummary, StandardDetail, QCOSummary, QCODetail,
  LaboratorySummary, LaboratoryDetail, CertificationScheme,
  ChecklistSummary, ChecklistDetail, ChecklistTask,
  ChatResponse, AIHealth, CoverageDashboardResponse, ResearchWorkflowResponse
} from "./types";

const API_BASE = "/api";

export async function fetchHealth(): Promise<{ status: string; database: string; ai_engine: AIHealth }> {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error("Failed to fetch system health");
  return res.json();
}

export async function fetchStandards(params?: {
  q?: string;
  division?: string;
  status?: string;
  has_qco?: boolean;
  page?: number;
  limit?: number;
}): Promise<{ total: number; page: number; limit: number; items: StandardSummary[] }> {
  const query = new URLSearchParams();
  if (params?.q) query.set("q", params.q);
  if (params?.division) query.set("division", params.division);
  if (params?.status) query.set("status", params.status);
  if (params?.has_qco !== undefined) query.set("has_qco", String(params.has_qco));
  if (params?.page) query.set("page", String(params.page));
  if (params?.limit) query.set("limit", String(params.limit));

  const res = await fetch(`${API_BASE}/standards?${query.toString()}`);
  if (!res.ok) throw new Error("Failed to fetch standards");
  return res.json();
}

export async function fetchStandardDetail(id: number | string): Promise<StandardDetail> {
  const res = await fetch(`${API_BASE}/standards/${id}`);
  if (!res.ok) throw new Error("Failed to fetch standard details");
  return res.json();
}

export async function fetchQCOs(params?: {
  q?: string;
  ministry?: string;
  status?: string;
  page?: number;
  limit?: number;
}): Promise<{ total: number; page: number; limit: number; items: QCOSummary[] }> {
  const query = new URLSearchParams();
  if (params?.q) query.set("q", params.q);
  if (params?.ministry) query.set("ministry", params.ministry);
  if (params?.status) query.set("status", params.status);
  if (params?.page) query.set("page", String(params.page));
  if (params?.limit) query.set("limit", String(params.limit));

  const res = await fetch(`${API_BASE}/qco?${query.toString()}`);
  if (!res.ok) throw new Error("Failed to fetch QCOs");
  return res.json();
}

export async function fetchQCODetail(id: number | string): Promise<QCODetail> {
  const res = await fetch(`${API_BASE}/qco/${id}`);
  if (!res.ok) throw new Error("Failed to fetch QCO details");
  return res.json();
}

export async function fetchLaboratories(params?: {
  q?: string;
  state?: string;
  city?: string;
  status?: string;
  standard_is?: string;
  user_lat?: number;
  user_lon?: number;
  page?: number;
  limit?: number;
}): Promise<{ total: number; page: number; limit: number; items: LaboratorySummary[] }> {
  const query = new URLSearchParams();
  if (params?.q) query.set("q", params.q);
  if (params?.state) query.set("state", params.state);
  if (params?.city) query.set("city", params.city);
  if (params?.status) query.set("status", params.status);
  if (params?.standard_is) query.set("standard_is", params.standard_is);
  if (params?.user_lat !== undefined) query.set("user_lat", String(params.user_lat));
  if (params?.user_lon !== undefined) query.set("user_lon", String(params.user_lon));
  if (params?.page) query.set("page", String(params.page));
  if (params?.limit) query.set("limit", String(params.limit));

  const res = await fetch(`${API_BASE}/laboratories?${query.toString()}`);
  if (!res.ok) throw new Error("Failed to fetch laboratories");
  return res.json();
}

export async function fetchLaboratoryDetail(id: number | string): Promise<LaboratoryDetail> {
  const res = await fetch(`${API_BASE}/laboratories/${id}`);
  if (!res.ok) throw new Error("Failed to fetch laboratory details");
  return res.json();
}

export async function fetchSchemes(): Promise<CertificationScheme[]> {
  const res = await fetch(`${API_BASE}/schemes`);
  if (!res.ok) throw new Error("Failed to fetch certification schemes");
  return res.json();
}

export async function fetchChecklists(): Promise<ChecklistSummary[]> {
  const res = await fetch(`${API_BASE}/checklists`);
  if (!res.ok) throw new Error("Failed to fetch checklists");
  return res.json();
}

export async function fetchChecklistDetail(id: string): Promise<ChecklistDetail> {
  const res = await fetch(`${API_BASE}/checklists/${id}`);
  if (!res.ok) throw new Error("Failed to fetch checklist");
  return res.json();
}

export async function createChecklist(data: {
  title: string;
  product_name: string;
  standard_number?: string;
  scheme_code?: string;
  notes?: string;
}): Promise<ChecklistDetail> {
  const res = await fetch(`${API_BASE}/checklists`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create checklist");
  return res.json();
}

export async function generateChecklist(data: {
  product_name: string;
  standard_number?: string;
  scheme_code?: string;
}): Promise<ChecklistDetail> {
  const res = await fetch(`${API_BASE}/checklists/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to generate checklist");
  return res.json();
}

export async function addTaskToChecklist(checklistId: string, task: {
  title: string;
  description?: string;
  stage: string;
  is_mandatory?: boolean;
}): Promise<ChecklistDetail> {
  const res = await fetch(`${API_BASE}/checklists/${checklistId}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(task),
  });
  if (!res.ok) throw new Error("Failed to add task");
  return res.json();
}

export async function updateTask(checklistId: string, taskId: string, updates: Partial<ChecklistTask>): Promise<ChecklistDetail> {
  const res = await fetch(`${API_BASE}/checklists/${checklistId}/tasks/${taskId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(updates),
  });
  if (!res.ok) throw new Error("Failed to update task");
  return res.json();
}

export async function deleteTask(checklistId: string, taskId: string): Promise<{ status: string }> {
  const res = await fetch(`${API_BASE}/checklists/${checklistId}/tasks/${taskId}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete task");
  return res.json();
}

export async function deleteChecklist(checklistId: string): Promise<{ status: string }> {
  const res = await fetch(`${API_BASE}/checklists/${checklistId}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete checklist");
  return res.json();
}

export async function sendChatMessage(message: string, conversationId?: string): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/ai/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, conversation_id: conversationId }),
  });
  if (!res.ok) throw new Error("Failed to process chat query");
  return res.json();
}

export async function runNavigatorResearch(data: {
  product_name: string;
  category?: string;
  intended_use?: string;
}): Promise<ResearchWorkflowResponse> {
  const res = await fetch(`${API_BASE}/ai/navigator`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to execute research navigator");
  return res.json();
}

export async function fetchCoverageDashboard(): Promise<CoverageDashboardResponse> {
  const res = await fetch(`${API_BASE}/stats/coverage`);
  if (!res.ok) throw new Error("Failed to fetch coverage dashboard");
  return res.json();
}
