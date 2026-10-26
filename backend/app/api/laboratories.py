from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.services.search_service import SearchService
from backend.app.schemas.laboratory import LaboratorySearchResponse, LaboratoryDetail
from backend.app.models.laboratory import TestingLaboratory

router = APIRouter(prefix="/laboratories", tags=["Testing Laboratories"])

@router.get("", response_model=LaboratorySearchResponse)
def list_laboratories(
    q: Optional[str] = Query(None, description="Search by Lab name, code, or keyword"),
    state: Optional[str] = Query(None, description="Filter by State"),
    city: Optional[str] = Query(None, description="Filter by City"),
    status: Optional[str] = Query(None, description="Filter by Status (Recognized, Renewal Pending)"),
    standard_is: Optional[str] = Query(None, description="Filter by accredited Indian Standard (e.g., IS 302, IS 16046)"),
    user_lat: Optional[float] = Query(None, description="User latitude for distance calculation"),
    user_lon: Optional[float] = Query(None, description="User longitude for distance calculation"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    total, items = SearchService.search_laboratories(
        db=db,
        query=q,
        state=state,
        city=city,
        status=status,
        standard_is=standard_is,
        user_lat=user_lat,
        user_lon=user_lon,
        page=page,
        limit=limit
    )
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": items
    }

@router.get("/{lab_id}", response_model=LaboratoryDetail)
def get_laboratory(lab_id: int, db: Session = Depends(get_db)):
    lab = db.query(TestingLaboratory).filter(TestingLaboratory.id == lab_id).first()
    if not lab:
        raise HTTPException(status_code=404, detail=f"Laboratory with ID {lab_id} not found.")

    scopes = [
        {
            "id": s.id,
            "standard_id": s.standard.id,
            "is_number": s.standard.is_number,
            "standard_title": s.standard.title,
            "product_category": s.product_category,
            "testing_capability": s.testing_capability,
            "valid_until": s.valid_until
        } for s in lab.scopes
    ]

    return {
        "id": lab.id,
        "lab_code": lab.lab_code,
        "name": lab.name,
        "address": lab.address,
        "city": lab.city,
        "district": lab.district,
        "state": lab.state,
        "pincode": lab.pincode,
        "latitude": lab.latitude,
        "longitude": lab.longitude,
        "contact_person": lab.contact_person,
        "phone": lab.phone,
        "email": lab.email,
        "lab_type": lab.lab_type,
        "status": lab.status,
        "recognition_valid_until": lab.recognition_valid_until,
        "source_url": lab.source_url,
        "is_fixture": lab.is_fixture,
        "last_verified_at": lab.last_verified_at,
        "created_at": lab.created_at,
        "updated_at": lab.updated_at,
        "scopes": scopes
    }
