export interface Citation {
  title: string;
  identifier: string;
  source_type: string;
  source_url?: string;
  verification_date?: string;
  is_fixture: boolean;
  evidence_text?: string;
}

export interface ChatResponse {
  conversation_id: string;
  response: string;
  citations: Citation[];
  model_name: string;
  latency_ms: number;
  is_fallback: boolean;
  identified_standards: string[];
  identified_qcos: string[];
}

export interface AIHealth {
  status: "healthy" | "degraded" | "unavailable";
  ollama_reachable: boolean;
  configured_model: string;
  available_models: string[];
  fallback_mode_active: boolean;
  diagnostic_message: string;
}

export interface StandardSummary {
  id: number;
  is_number: string;
  normalized_is: string;
  title: string;
  division?: string;
  publication_year?: number;
  status: string;
  is_fixture: boolean;
  source_url?: string;
  has_qco: boolean;
  lab_count: number;
}

export interface StandardDetail extends StandardSummary {
  technical_committee?: string;
  scope_abstract?: string;
  verification_date: string;
  relationships: Array<{
    id: number;
    related_is_number: string;
    relationship_type: string;
    description?: string;
  }>;
  applicable_qcos: Array<{
    qco_id: number;
    order_number: string;
    title: string;
    issuing_ministry: string;
    status: string;
    enforcement_date?: string;
    official_url?: string;
    exemption_notes?: string;
  }>;
  accredited_labs: Array<{
    lab_id: number;
    lab_code: string;
    lab_name: string;
    city: string;
    state: string;
    status: string;
    testing_capability?: string;
    valid_until?: string;
    source_url?: string;
  }>;
}

export interface QCOSummary {
  id: number;
  order_number: string;
  title: string;
  issuing_ministry: string;
  product_category?: string;
  gazette_date?: string;
  enforcement_date?: string;
  status: string;
  official_url?: string;
  notes?: string;
  is_fixture: boolean;
  standard_count: number;
  amendment_count: number;
  last_verified_at: string;
}

export interface QCODetail extends QCOSummary {
  standards: Array<{
    standard_id: number;
    is_number: string;
    title: string;
    applicable_date?: string;
    exemption_notes?: string;
  }>;
  amendments: Array<{
    id: number;
    amendment_number: string;
    gazette_notification?: string;
    notification_date?: string;
    effective_date?: string;
    summary: string;
    source_url?: string;
  }>;
}

export interface LaboratorySummary {
  id: number;
  lab_code: string;
  name: string;
  address: string;
  city: string;
  district?: string;
  state: string;
  pincode?: string;
  latitude?: number;
  longitude?: number;
  contact_person?: string;
  phone?: string;
  email?: string;
  lab_type: string;
  status: string;
  recognition_valid_until?: string;
  source_url?: string;
  is_fixture: boolean;
  distance_km?: number;
  scope_count: number;
  last_verified_at: string;
}

export interface LaboratoryDetail extends LaboratorySummary {
  scopes: Array<{
    id: number;
    standard_id: number;
    is_number: string;
    standard_title: string;
    product_category?: string;
    testing_capability?: string;
    valid_until?: string;
  }>;
}

export interface CertificationScheme {
  id: number;
  code: string;
  name: string;
  description: string;
  governing_act?: string;
  mark_name: string;
  typical_timeline_weeks?: number;
  factory_audit_required: boolean;
  sample_testing_required: boolean;
  surveillance_frequency?: string;
  documentation_requirements?: string;
  guidance_url?: string;
}

export interface ChecklistTask {
  id: string;
  checklist_id: string;
  title: string;
  description?: string;
  stage: string;
  is_mandatory: boolean;
  is_completed: boolean;
  order_index: number;
  notes?: string;
  source_citation?: string;
}

export interface ChecklistSummary {
  id: string;
  title: string;
  product_name: string;
  standard_number?: string;
  scheme_code?: string;
  notes?: string;
  status: string;
  total_tasks: number;
  completed_tasks: number;
  completion_percentage: number;
  created_at: string;
  updated_at: string;
}

export interface ChecklistDetail extends ChecklistSummary {
  tasks: ChecklistTask[];
}

export interface CoverageStats {
  total_standards: number;
  verified_standards: number;
  fixture_standards: number;
  total_qcos: number;
  verified_qcos: number;
  active_qcos: number;
  total_laboratories: number;
  verified_laboratories: number;
  total_scopes_mapped: number;
  total_schemes: number;
  total_official_sources: number;
  dataset_freshness_date?: string;
  last_ingestion_run?: {
    dataset?: string;
    status?: string;
    records_upserted: number;
    finished_at?: string;
  };
  ai_status: string;
  ai_model: string;
}

export interface CoverageDashboardResponse {
  stats: CoverageStats;
  sources: Array<{
    id: number;
    name: string;
    portal_type: string;
    base_url: string;
    licensing_terms?: string;
    update_frequency: string;
    status: string;
    last_polled_at?: string;
    last_success_at?: string;
  }>;
  recent_ingestion_runs: Array<{
    id: number;
    dataset_name: string;
    status: string;
    records_processed: number;
    records_upserted: number;
    records_rejected: number;
    started_at: string;
    finished_at?: string;
    error_message?: string;
  }>;
  coverage_gaps: Array<{
    category: string;
    official_source: string;
    status: string;
    description: string;
    action_required: string;
  }>;
}

export interface ResearchWorkflowResponse {
  product_name: string;
  potentially_relevant_standards: any[];
  certification_scheme?: CertificationScheme;
  mandatory_qco_findings: any[];
  verified_facts: string[];
  inferred_relationships: string[];
  unresolved_questions: string[];
  recommended_laboratories: any[];
  suggested_checklist: any[];
  citations: Citation[];
}
