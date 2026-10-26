from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.schemas.ai import (
    ChatRequest, ChatResponse, AIHealthResponse, ResearchWorkflowRequest, ResearchWorkflowResponse, Citation
)
from backend.app.services.rag_service import RAGService
from backend.app.services.ollama_client import ollama_client
from backend.app.services.search_service import SearchService
from backend.app.models.scheme import CertificationScheme

router = APIRouter(prefix="/ai", tags=["AI Copilot & Research Navigator"])

@router.get("/health", response_model=AIHealthResponse)
async def get_ai_health():
    data = await ollama_client.check_health()
    return AIHealthResponse(**data)

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest, db: Session = Depends(get_db)):
    result = await RAGService.process_chat(
        db=db,
        query=req.message,
        conversation_id=req.conversation_id
    )
    return ChatResponse(**result)

@router.post("/navigator", response_model=ResearchWorkflowResponse)
def certification_navigator_endpoint(req: ResearchWorkflowRequest, db: Session = Depends(get_db)):
    """
    Executes a comprehensive, multi-step certification discovery workflow for a product:
    1. Identifies relevant Indian Standards.
    2. Determines applicable Quality Control Orders (QCO) and mandatory enforcement status.
    3. Identifies applicable Certification Scheme (Scheme-I vs Scheme-II CRS).
    4. Finds accredited testing laboratories and testing scopes.
    5. Generates structured evidentiary distinctions (verified facts vs unresolved questions).
    """
    product = req.product_name.strip()
    entities = RAGService.extract_entities(f"{product} {req.category or ''} {req.intended_use or ''}")
    context_data, citations = RAGService.retrieve_context(db, entities)

    stds = context_data.get("standards", [])
    qcos = context_data.get("qcos", [])
    labs = context_data.get("laboratories", [])

    # Determine primary scheme
    is_electronic = any("electronics" in s["title"].lower() or "battery" in s["title"].lower() or "it" in s["title"].lower() for s in stds)
    scheme_code = "SCHEME_II" if is_electronic else "SCHEME_I"
    scheme_obj = db.query(CertificationScheme).filter(CertificationScheme.code == scheme_code).first()
    scheme_dict = None
    if scheme_obj:
        scheme_dict = {
            "code": scheme_obj.code,
            "name": scheme_obj.name,
            "mark_name": scheme_obj.mark_name,
            "factory_audit_required": scheme_obj.factory_audit_required,
            "sample_testing_required": scheme_obj.sample_testing_required,
            "typical_timeline_weeks": scheme_obj.typical_timeline_weeks,
            "guidance_url": scheme_obj.guidance_url,
            "documentation_requirements": scheme_obj.documentation_requirements
        }

    verified_facts = []
    inferred = []
    unresolved = []

    if stds:
        verified_facts.append(f"Identified {len(stds)} relevant Indian Standard(s): {', '.join([s['is_number'] for s in stds])}.")
    else:
        unresolved.append("No direct Indian Standard matched this exact product description in the current catalogue.")

    if qcos:
        verified_facts.append(f"Product is covered by mandatory Quality Control Order: {qcos[0]['order_number']} issued by {qcos[0]['ministry']} (Status: {qcos[0]['status']}).")
        inferred.append("Certification is mandatory prior to commercial production, import, or sale in India under Section 16 of the BIS Act 2016.")
    else:
        inferred.append("No active mandatory QCO order found in database; certification may currently be voluntary unless covered by sector-specific exemptions.")

    if not req.intended_use:
        unresolved.append("Intended use (domestic household vs commercial / industrial) was not specified; certain QCO exemptions apply solely to industrial components.")

    unresolved.append("Confirm electrical rating (voltage, wattage, phase) or mechanical load specifications to identify specific sub-parts of the standard.")

    # Suggested checklist draft
    suggested_tasks = [
        {"stage": "Documentation", "title": f"Review technical specifications against {stds[0]['is_number'] if stds else 'Indian Standards'}", "is_mandatory": True},
        {"stage": "Documentation", "title": "Prepare Factory Layout & Machinery List", "is_mandatory": True},
        {"stage": "Pre-Testing", "title": f"Submit sample units to accredited lab ({labs[0]['name'] if labs else 'BIS Recognized Lab'})", "is_mandatory": True},
        {"stage": "Factory Audit", "title": "Set up in-house testing equipment per Scheme of Inspection and Testing (SIT)", "is_mandatory": scheme_code == "SCHEME_I"},
        {"stage": "Application Submission", "title": "File online application on e-BIS Manakonline portal", "is_mandatory": True},
        {"stage": "Grant of Licence", "title": f"Receive BIS Licence / Registration and apply {scheme_obj.mark_name if scheme_obj else 'Standard Mark'} on packaging", "is_mandatory": True}
    ]

    return ResearchWorkflowResponse(
        product_name=product,
        potentially_relevant_standards=stds,
        certification_scheme=scheme_dict,
        mandatory_qco_findings=qcos,
        verified_facts=verified_facts,
        inferred_relationships=inferred,
        unresolved_questions=unresolved,
        recommended_laboratories=labs,
        suggested_checklist=suggested_tasks,
        citations=citations
    )
