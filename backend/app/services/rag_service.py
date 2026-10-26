import re
import json
import time
from typing import List, Dict, Any, Tuple, Optional
from sqlalchemy.orm import Session
from backend.app.models.standard import Standard
from backend.app.models.qco import QCO, QCOStandardLink
from backend.app.models.laboratory import TestingLaboratory, LaboratoryScope
from backend.app.models.scheme import CertificationScheme
from backend.app.models.conversation import Conversation, ChatMessage
from backend.app.schemas.ai import Citation
from backend.app.services.search_service import normalize_is_number, SearchService
from backend.app.services.ollama_client import ollama_client

SYSTEM_PROMPT = """You are the BIS AI Copilot — an expert industrial compliance and standards navigation assistant for the Bureau of Indian Standards (BIS) regulatory framework.

CRITICAL OPERATIONAL RULES:
1. ONLY make factual assertions that are directly grounded in the retrieved database records provided in the context.
2. NEVER invent or hallucinate Indian Standard numbers (IS XXXX), gazette numbers, dates, fees, or laboratory names.
3. If an Indian Standard exists for a product, DO NOT assume certification is mandatory unless an official Quality Control Order (QCO) explicitly mandates it in the context.
4. Clearly distinguish between:
   - VERIFIED FACTS: Direct statements from the official records.
   - INFERRED RELATIONSHIPS: Logical application steps or potential testing scopes.
   - UNRESOLVED QUESTIONS: Key specifications (e.g. voltage, wattage, industrial vs domestic) needed to finalize applicability.
5. Emphasize that this platform provides decision intelligence and compliance assistance, but is NOT an official BIS certifying body. The user must verify final specifications via official BIS portals (manakonline.in / bis.gov.in).
6. Format your response cleanly using markdown with clear headings, bullet points, and source citations.
"""

class RAGService:
    @staticmethod
    def extract_entities(query: str) -> Dict[str, Any]:
        """Extracts potential IS numbers, product keywords, and ministries from natural language query."""
        # Find potential IS numbers like IS 302, IS 16046, IS 694, IS1293
        is_pattern = r'\bIS\s*[:\-]?\s*(\d+)(?:\s*(?:\(Part\s*(\d+)\)|-?\s*(\d+)))?(?:\s*[:\-]?\s*(\d{4}))?'
        matches = re.finditer(is_pattern, query, re.IGNORECASE)
        found_is = []
        for m in matches:
            found_is.append(m.group(0))

        # Known common product keywords
        products = []
        lowered = query.lower()
        product_terms = [
            "household electrical", "geyser", "water heater", "iron", "room heater",
            "solar", "solar panel", "photovoltaic", "pv module", "inverter",
            "battery", "lithium", "power bank", "ups",
            "toy", "toys", "electronic toys",
            "cement", "portland", "steel", "tmt bar", "structural steel",
            "plywood", "helmet", "two wheeler helmet",
            "led", "lamp", "cfl", "lighting", "cable", "wire", "pvc wire",
            "packaged drinking water", "mineral water", "gas stove", "lpg"
        ]
        for term in product_terms:
            if term in lowered:
                products.append(term)

        return {
            "standards": found_is,
            "products": products,
            "raw_query": query
        }

    @staticmethod
    def retrieve_context(db: Session, entities: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[Citation]]:
        """Retrieves matching standards, QCOs, schemes, and laboratories from relational DB."""
        retrieved_standards = []
        retrieved_qcos = []
        retrieved_labs = []
        citations: List[Citation] = []
        seen_identifiers = set()

        # 1. Match IS numbers
        for is_term in entities["standards"]:
            norm = normalize_is_number(is_term)
            stds = db.query(Standard).filter(
                (Standard.normalized_is.ilike(f"%{norm}%")) |
                (Standard.is_number.ilike(f"%{is_term}%"))
            ).limit(5).all()
            for s in stds:
                if s.is_number not in seen_identifiers:
                    seen_identifiers.add(s.is_number)
                    retrieved_standards.append(s)
                    citations.append(Citation(
                        title=s.title,
                        identifier=s.is_number,
                        source_type="Standard",
                        source_url=s.source_url or f"https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/knowyourstandards/indian_standards/isdetails/{s.id}",
                        verification_date=s.verification_date.strftime("%Y-%m-%d"),
                        is_fixture=s.is_fixture,
                        evidence_text=s.scope_abstract
                    ))

        # 2. Match products / general query
        search_terms = entities["products"] if entities["products"] else [entities["raw_query"]]
        for term in search_terms:
            total, std_results = SearchService.search_standards(db, query=term, limit=4)
            for item in std_results:
                if item["is_number"] not in seen_identifiers:
                    seen_identifiers.add(item["is_number"])
                    std_obj = db.query(Standard).filter(Standard.id == item["id"]).first()
                    if std_obj:
                        retrieved_standards.append(std_obj)
                        citations.append(Citation(
                            title=std_obj.title,
                            identifier=std_obj.is_number,
                            source_type="Standard",
                            source_url=std_obj.source_url,
                            verification_date=std_obj.verification_date.strftime("%Y-%m-%d"),
                            is_fixture=std_obj.is_fixture,
                            evidence_text=std_obj.scope_abstract
                        ))

            # Query QCOs
            total_q, qco_results = SearchService.search_qcos(db, query=term, limit=3)
            for q in qco_results:
                if q["order_number"] not in seen_identifiers:
                    seen_identifiers.add(q["order_number"])
                    qco_obj = db.query(QCO).filter(QCO.id == q["id"]).first()
                    if qco_obj:
                        retrieved_qcos.append(qco_obj)
                        citations.append(Citation(
                            title=qco_obj.title,
                            identifier=qco_obj.order_number,
                            source_type="QCO",
                            source_url=qco_obj.official_url or "https://www.bis.gov.in/product-certification/products-under-compulsory-certification/",
                            verification_date=qco_obj.last_verified_at.strftime("%Y-%m-%d"),
                            is_fixture=qco_obj.is_fixture,
                            evidence_text=f"Issuing Ministry: {qco_obj.issuing_ministry}. Status: {qco_obj.status}. Enforcement: {qco_obj.enforcement_date}"
                        ))

        # Also pull QCOs linked to any retrieved standards
        for s in retrieved_standards:
            for link in s.qco_links:
                q = link.qco
                if q.order_number not in seen_identifiers:
                    seen_identifiers.add(q.order_number)
                    retrieved_qcos.append(q)
                    citations.append(Citation(
                        title=q.title,
                        identifier=q.order_number,
                        source_type="QCO",
                        source_url=q.official_url,
                        verification_date=q.last_verified_at.strftime("%Y-%m-%d"),
                        is_fixture=q.is_fixture,
                        evidence_text=f"Mandates compliance to {s.is_number} under {q.issuing_ministry}."
                    ))

            # Pull accredited labs for standard
            for scope in s.lab_scopes:
                lab = scope.laboratory
                if lab.lab_code not in seen_identifiers:
                    seen_identifiers.add(lab.lab_code)
                    retrieved_labs.append((lab, scope))
                    citations.append(Citation(
                        title=lab.name,
                        identifier=lab.lab_code,
                        source_type="Laboratory",
                        source_url=lab.source_url or "https://lims.bis.gov.in/",
                        verification_date=lab.last_verified_at.strftime("%Y-%m-%d"),
                        is_fixture=lab.is_fixture,
                        evidence_text=f"Accredited in {lab.city}, {lab.state} for testing {s.is_number}."
                    ))

        # Build context package
        context_data = {
            "standards": [
                {
                    "is_number": s.is_number,
                    "title": s.title,
                    "division": s.division,
                    "status": s.status,
                    "scope": s.scope_abstract,
                    "source_url": s.source_url,
                    "is_fixture": s.is_fixture
                } for s in retrieved_standards
            ],
            "qcos": [
                {
                    "order_number": q.order_number,
                    "title": q.title,
                    "ministry": q.issuing_ministry,
                    "status": q.status,
                    "enforcement_date": str(q.enforcement_date),
                    "notes": q.notes,
                    "official_url": q.official_url,
                    "is_fixture": q.is_fixture
                } for q in retrieved_qcos
            ],
            "laboratories": [
                {
                    "name": lab.name,
                    "lab_code": lab.lab_code,
                    "city": lab.city,
                    "state": lab.state,
                    "contact_phone": lab.phone,
                    "status": lab.status,
                    "tested_standard": scope.standard.is_number
                } for lab, scope in retrieved_labs[:5]
            ]
        }

        return context_data, citations

    @staticmethod
    def build_deterministic_response(
        query: str,
        context: Dict[str, Any],
        citations: List[Citation]
    ) -> str:
        """
        Synthesizes a high-quality, strictly grounded compliance explanation
        directly from retrieved database records when Ollama is offline or in fallback mode.
        """
        standards = context.get("standards", [])
        qcos = context.get("qcos", [])
        labs = context.get("laboratories", [])

        if not standards and not qcos:
            return f"""### BIS Research Findings for: "{query}"

> [!NOTE]
> No direct Indian Standard or Quality Control Order records matched your exact search query in the current indexed database.

#### Recommended Next Steps:
1. **Try related industry terms**: Search by product category (e.g. *Household electrical appliances*, *Solar PV*, *Steel bars*, *Toys*, *Cables*).
2. **Search by IS number directly**: Use the [Standard Explorer](file:///standards) to look up numbers like `IS 302`, `IS 694`, or `IS 16046`.
3. **Verify official BIS portal**: Check the live [BIS Know Your Standard Portal](https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/knowyourstandards/indian_standards/) or [e-BIS](https://www.manakonline.in/).
"""

        lines = [f"### Compliance Intelligence & Research Summary\n"]
        lines.append(f"**Query Analyzed**: *{query}*\n")

        # 1. Relevant Standards
        if standards:
            lines.append("#### 1. Relevant Indian Standards (IS)")
            for s in standards:
                fix_badge = " *(Sample Fixture)*" if s.get("is_fixture") else " *(Verified Official Record)*"
                lines.append(f"- **{s['is_number']}**: {s['title']}{fix_badge}")
                if s.get("scope"):
                    lines.append(f"  - **Scope**: {s['scope']}")
                if s.get("source_url"):
                    lines.append(f"  - **Official Reference**: [{s['is_number']} on BIS Portal]({s['source_url']})")
            lines.append("")

        # 2. QCO and Mandatory Applicability
        lines.append("#### 2. Quality Control Orders (QCO) & Legal Applicability")
        if qcos:
            for q in qcos:
                status_note = f"**Status**: {q['status']} (Enforcement Date: {q['enforcement_date']})"
                lines.append(f"- **{q['order_number']}** — *{q['title']}*")
                lines.append(f"  - **Issuing Ministry**: {q['ministry']}")
                lines.append(f"  - {status_note}")
                if q.get("notes"):
                    lines.append(f"  - **Applicability & Conditions**: {q['notes']}")
                if q.get("official_url"):
                    lines.append(f"  - **Official Gazette Link**: [View Notification]({q['official_url']})")
            lines.append("\n> [!IMPORTANT]\n> Under Section 16 of the BIS Act 2016, products covered by an active QCO are subject to **mandatory certification**. Manufacturing, importing, storing, or selling non-certified products violates the Act.")
        else:
            lines.append("- **No Active QCO Mandate Found in DB**: While an Indian Standard exists, our current database does not show an active mandatory Quality Control Order for this specific classification.")
            lines.append("- **Voluntary Certification**: In the absence of a mandatory QCO, manufacturers may obtain the standard ISI Mark voluntarily under Scheme-I for market credibility.")
        lines.append("")

        # 3. Applicable Certification Schemes
        lines.append("#### 3. Certification Scheme & Workflow")
        if any("electronics" in s["title"].lower() or "it" in s["title"].lower() or "battery" in s["title"].lower() for s in standards):
            lines.append("- **Primary Scheme**: **Scheme-II (Compulsory Registration Scheme - CRS)** administered by BIS & MeitY.")
            lines.append("- **Mark**: Standard Mark with Registration Number (R-XXXXXXXX).")
            lines.append("- **Key Requirement**: Self-declaration of conformity based on laboratory test report from a BIS-recognized testing lab. No initial factory audit is required for Scheme-II.")
        else:
            lines.append("- **Primary Scheme**: **Scheme-I (ISI Mark - Product Certification Scheme)**.")
            lines.append("- **Mark**: Standard ISI Mark with Licence Number (CM/L-XXXXXXXX).")
            lines.append("- **Key Requirement**: Requires factory audit of manufacturing process, in-house testing equipment, quality personnel, and independent laboratory testing.")
        lines.append("")

        # 4. Testing Laboratories
        if labs:
            lines.append("#### 4. Accredited Testing Laboratories")
            lines.append("The following accredited testing facilities in our directory maintain recognized scope for this standard:")
            for l in labs:
                lines.append(f"- **{l['name']}** ({l['city']}, {l['state']}) — Lab Code: `{l['lab_code']}` | Status: {l['status']}")
            lines.append("\nUse the [Testing Laboratories Directory](file:///laboratories) to locate facilities closest to your manufacturing plant.")
            lines.append("")

        # 5. Verified Facts vs Assumptions
        lines.append("#### 5. Evidentiary Distinctions")
        lines.append("- **Verified Facts**: The Indian Standards and QCO gazettes cited above are confirmed in the regulatory records.")
        lines.append("- **Assumptions & Conditions**: Final mandatory status depends on specific product ratings (e.g. voltage rating, domestic vs commercial use, wattage). Always verify exemptions in the latest gazette amendments.")
        lines.append("")

        return "\n".join(lines)

    @classmethod
    async def process_chat(
        cls,
        db: Session,
        query: str,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Main chat orchestration pipeline with RAG, Ollama local model, and deterministic fallback."""
        start_time = time.time()

        # Manage conversation record
        conv = None
        if conversation_id:
            conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conv:
            conv = Conversation(title=query[:60])
            db.add(conv)
            db.commit()
            db.refresh(conv)

        # Record user message
        user_msg = ChatMessage(
            conversation_id=conv.id,
            role="user",
            content=query
        )
        db.add(user_msg)
        db.commit()

        # Step 1: Entity Extraction & DB Retrieval
        entities = cls.extract_entities(query)
        context_data, citations = cls.retrieve_context(db, entities)

        # Step 2: Check Ollama availability
        ollama_status = await ollama_client.check_health()
        use_ollama = ollama_status["ollama_reachable"] and not ollama_status["fallback_mode_active"]

        generated_text = ""
        model_name = "Deterministic-RAG-Engine (Local Grounded)"
        is_fallback = True

        if use_ollama:
            # Build prompt with bounded context
            context_str = json.dumps(context_data, indent=2)
            user_prompt = f"""Retrieved Regulatory Records from Database:
{context_str}

User Question:
{query}

Provide a comprehensive, authoritative response following all operational rules. State verified facts, QCO mandates, certification schemes, and practical next steps."""

            chat_res = await ollama_client.chat([
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ])

            if chat_res["success"] and chat_res["content"].strip():
                generated_text = chat_res["content"]
                model_name = chat_res["model"]
                is_fallback = False
            else:
                # Ollama failed during inference, use deterministic fallback
                generated_text = cls.build_deterministic_response(query, context_data, citations)
        else:
            # Fast deterministic RAG path
            generated_text = cls.build_deterministic_response(query, context_data, citations)

        latency_ms = int((time.time() - start_time) * 1000)

        # Save assistant message with citations
        citations_json = json.dumps([c.model_dump() for c in citations])
        asst_msg = ChatMessage(
            conversation_id=conv.id,
            role="assistant",
            content=generated_text,
            citations_json=citations_json,
            model_name=model_name,
            latency_ms=latency_ms,
            is_fallback=1 if is_fallback else 0
        )
        db.add(asst_msg)
        db.commit()

        return {
            "conversation_id": conv.id,
            "response": generated_text,
            "citations": citations,
            "model_name": model_name,
            "latency_ms": latency_ms,
            "is_fallback": is_fallback,
            "identified_standards": [s["is_number"] for s in context_data.get("standards", [])],
            "identified_qcos": [q["order_number"] for q in context_data.get("qcos", [])]
        }
