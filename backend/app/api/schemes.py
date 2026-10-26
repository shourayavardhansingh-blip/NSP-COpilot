from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.scheme import CertificationScheme

router = APIRouter(prefix="/schemes", tags=["Certification Schemes"])

@router.get("")
def list_schemes(db: Session = Depends(get_db)):
    schemes = db.query(CertificationScheme).order_by(CertificationScheme.id).all()
    return [
        {
            "id": s.id,
            "code": s.code,
            "name": s.name,
            "description": s.description,
            "governing_act": s.governing_act,
            "mark_name": s.mark_name,
            "typical_timeline_weeks": s.typical_timeline_weeks,
            "factory_audit_required": s.factory_audit_required,
            "sample_testing_required": s.sample_testing_required,
            "surveillance_frequency": s.surveillance_frequency,
            "documentation_requirements": s.documentation_requirements,
            "guidance_url": s.guidance_url
        } for s in schemes
    ]

@router.get("/{code}")
def get_scheme_by_code(code: str, db: Session = Depends(get_db)):
    s = db.query(CertificationScheme).filter(CertificationScheme.code.ilike(code)).first()
    if not s:
        raise HTTPException(status_code=404, detail=f"Certification Scheme '{code}' not found.")
    return {
        "id": s.id,
        "code": s.code,
        "name": s.name,
        "description": s.description,
        "governing_act": s.governing_act,
        "mark_name": s.mark_name,
        "typical_timeline_weeks": s.typical_timeline_weeks,
        "factory_audit_required": s.factory_audit_required,
        "sample_testing_required": s.sample_testing_required,
        "surveillance_frequency": s.surveillance_frequency,
        "documentation_requirements": s.documentation_requirements,
        "guidance_url": s.guidance_url
    }
