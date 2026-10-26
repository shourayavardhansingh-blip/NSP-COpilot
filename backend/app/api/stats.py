from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.standard import Standard
from backend.app.models.qco import QCO
from backend.app.models.laboratory import TestingLaboratory, LaboratoryScope
from backend.app.models.scheme import CertificationScheme
from backend.app.models.provenance import OfficialSource, IngestionRun
from backend.app.schemas.stats import CoverageDashboardResponse, CoverageStats, CoverageGap
from backend.app.services.ollama_client import ollama_client

router = APIRouter(prefix="/stats", tags=["Data Coverage & Governance"])

@router.get("/coverage", response_model=CoverageDashboardResponse)
async def get_coverage_dashboard(db: Session = Depends(get_db)):
    # Standards
    total_stds = db.query(Standard).count()
    verified_stds = db.query(Standard).filter(Standard.is_fixture == False).count()
    fixture_stds = db.query(Standard).filter(Standard.is_fixture == True).count()

    # QCOs
    total_qcos = db.query(QCO).count()
    verified_qcos = db.query(QCO).filter(QCO.is_fixture == False).count()
    active_qcos = db.query(QCO).filter(QCO.status == "In Force").count()

    # Labs
    total_labs = db.query(TestingLaboratory).count()
    verified_labs = db.query(TestingLaboratory).filter(TestingLaboratory.is_fixture == False).count()
    total_scopes = db.query(LaboratoryScope).count()

    # Schemes & Sources
    total_schemes = db.query(CertificationScheme).count()
    sources = db.query(OfficialSource).all()
    total_sources = len(sources)

    # Ingestion Runs
    recent_runs = db.query(IngestionRun).order_by(IngestionRun.started_at.desc()).limit(10).all()
    last_successful = db.query(IngestionRun).filter(IngestionRun.status == "Completed").order_by(IngestionRun.finished_at.desc()).first()

    # AI Status
    ai_health = await ollama_client.check_health()

    stats = CoverageStats(
        total_standards=total_stds,
        verified_standards=verified_stds,
        fixture_standards=fixture_stds,
        total_qcos=total_qcos,
        verified_qcos=verified_qcos,
        active_qcos=active_qcos,
        total_laboratories=total_labs,
        verified_laboratories=verified_labs,
        total_scopes_mapped=total_scopes,
        total_schemes=total_schemes,
        total_official_sources=total_sources,
        dataset_freshness_date=last_successful.finished_at if last_successful else datetime.utcnow(),
        last_ingestion_run={
            "dataset": last_successful.dataset_name if last_successful else None,
            "status": last_successful.status if last_successful else None,
            "records_upserted": last_successful.records_upserted if last_successful else 0,
            "finished_at": last_successful.finished_at.isoformat() if last_successful and last_successful.finished_at else None
        } if last_successful else None,
        ai_status=ai_health["status"],
        ai_model=ai_health["configured_model"]
    )

    sources_list = [
        {
            "id": s.id,
            "name": s.name,
            "portal_type": s.portal_type,
            "base_url": s.base_url,
            "licensing_terms": s.licensing_terms,
            "update_frequency": s.update_frequency,
            "status": s.status,
            "last_polled_at": s.last_polled_at.isoformat() if s.last_polled_at else None,
            "last_success_at": s.last_success_at.isoformat() if s.last_success_at else None
        } for s in sources
    ]

    runs_list = [
        {
            "id": r.id,
            "dataset_name": r.dataset_name,
            "status": r.status,
            "records_processed": r.records_processed,
            "records_upserted": r.records_upserted,
            "records_rejected": r.records_rejected,
            "started_at": r.started_at.isoformat() if r.started_at else None,
            "finished_at": r.finished_at.isoformat() if r.finished_at else None,
            "error_message": r.error_message
        } for r in recent_runs
    ]

    coverage_gaps = [
        CoverageGap(
            category="Full Text Standard Specifications",
            official_source="BIS Sales Portal (standardsbis.bsbedge.com)",
            status="Licensing Restricted",
            description="Complete full-text Indian Standard specifications (clauses, figures, formulas) are copyrighted by Bureau of Indian Standards and sold under proprietary licence.",
            action_required="Platform intentionally indexes scopes, titles, test methods, and official URLs. Does not pirate copyrighted PDF standards."
        ),
        CoverageGap(
            category="Dynamic Live Laboratory Testing Backlog",
            official_source="BIS LIMS Internal Testing Queue",
            status="Partial Coverage",
            description="LIMS public directory provides accredited scopes and contact records, but real-time queue length / sample test backlog is restricted to internal BIS applicants.",
            action_required="Platform displays published validity dates and recommends direct laboratory inquiries for turnaround times."
        ),
        CoverageGap(
            category="Weekly Gazette QCO Amendments",
            official_source="e-Gazette of India (egazette.gov.in)",
            status="Automated / Semi-Automated Feed",
            description="Extraordinary Gazette notifications issued under Section 16 of BIS Act are published weekly across disparate ministries (DPIIT, Steel, MeitY, MHI).",
            action_required="Incremental QCO connector polls gazette repository and records amendment histories with date provenance."
        )
    ]

    return CoverageDashboardResponse(
        stats=stats,
        sources=sources_list,
        recent_ingestion_runs=runs_list,
        coverage_gaps=coverage_gaps
    )
