from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class Citation(BaseModel):
    title: str
    identifier: str
    source_type: str  # Standard, QCO, Laboratory, Scheme, Gazette
    source_url: Optional[str] = None
    verification_date: Optional[str] = None
    is_fixture: bool = False
    evidence_text: Optional[str] = None

class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str
    stream: bool = False

class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    citations: List[Citation] = []
    model_name: str
    latency_ms: int
    is_fallback: bool = False
    identified_standards: List[str] = []
    identified_qcos: List[str] = []

class AIHealthResponse(BaseModel):
    status: str  # healthy, degraded, unavailable
    ollama_reachable: bool
    configured_model: str
    available_models: List[str] = []
    fallback_mode_active: bool
    diagnostic_message: str

class ResearchWorkflowRequest(BaseModel):
    product_name: str
    category: Optional[str] = None
    industry: Optional[str] = None
    intended_use: Optional[str] = None
    country_of_origin: Optional[str] = "India"

class ResearchWorkflowResponse(BaseModel):
    product_name: str
    potentially_relevant_standards: List[Dict[str, Any]] = []
    certification_scheme: Optional[Dict[str, Any]] = None
    mandatory_qco_findings: List[Dict[str, Any]] = []
    verified_facts: List[str] = []
    inferred_relationships: List[str] = []
    unresolved_questions: List[str] = []
    recommended_laboratories: List[Dict[str, Any]] = []
    suggested_checklist: List[Dict[str, Any]] = []
    citations: List[Citation] = []
