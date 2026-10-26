from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.provenance import OfficialSource

router = APIRouter(prefix="/sources", tags=["Official Sources & Provenance"])

@router.get("")
def list_official_sources(db: Session = Depends(get_db)):
    sources = db.query(OfficialSource).order_by(OfficialSource.id).all()
    return [
        {
            "id": s.id,
            "name": s.name,
            "portal_type": s.portal_type,
            "base_url": s.base_url,
            "licensing_terms": s.licensing_terms,
            "update_frequency": s.update_frequency,
            "status": s.status,
            "last_polled_at": s.last_polled_at.isoformat() if s.last_polled_at else None,
            "last_success_at": s.last_success_at.isoformat() if s.last_success_at else None,
            "notes": s.notes
        } for s in sources
    ]
