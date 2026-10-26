from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.services.search_service import SearchService
from backend.app.schemas.qco import QCOSearchResponse, QCODetail

router = APIRouter(prefix="/qco", tags=["Quality Control Orders"])

@router.get("", response_model=QCOSearchResponse)
def list_qcos(
    q: Optional[str] = Query(None, description="Search by Order number, title, standard, or keyword"),
    ministry: Optional[str] = Query(None, description="Filter by Issuing Ministry (e.g. DPIIT, MeitY, Steel)"),
    status: Optional[str] = Query(None, description="Filter by status (In Force, Upcoming, Superseded)"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    total, items = SearchService.search_qcos(
        db=db,
        query=q,
        ministry=ministry,
        status=status,
        page=page,
        limit=limit
    )
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": items
    }

@router.get("/{qco_id}", response_model=QCODetail)
def get_qco(qco_id: int, db: Session = Depends(get_db)):
    data = SearchService.get_qco_detail(db, qco_id)
    if not data:
        raise HTTPException(status_code=404, detail=f"Quality Control Order with ID {qco_id} not found.")
    return data
