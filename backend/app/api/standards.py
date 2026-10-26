from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.services.search_service import SearchService, normalize_is_number
from backend.app.schemas.standard import StandardSearchResponse, StandardDetail

router = APIRouter(prefix="/standards", tags=["Indian Standards"])

@router.get("", response_model=StandardSearchResponse)
def list_standards(
    q: Optional[str] = Query(None, description="Search by IS number, title, division, or keyword"),
    division: Optional[str] = Query(None, description="Filter by Division (e.g., ETD, CED, MED, LITD)"),
    status: Optional[str] = Query(None, description="Filter by Status (Current, Revised, Withdrawn)"),
    has_qco: Optional[bool] = Query(None, description="Filter by mandatory QCO applicability"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    total, items = SearchService.search_standards(
        db=db,
        query=q,
        division=division,
        status=status,
        has_qco=has_qco,
        page=page,
        limit=limit
    )
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": items
    }

@router.get("/{standard_id}", response_model=StandardDetail)
def get_standard(standard_id: int, db: Session = Depends(get_db)):
    data = SearchService.get_standard_detail(db, standard_id)
    if not data:
        raise HTTPException(status_code=404, detail=f"Standard with ID {standard_id} not found.")
    return data

@router.get("/lookup/{is_number}")
def lookup_standard_by_number(is_number: str, db: Session = Depends(get_db)):
    """Fast-path lookup for exact or normalized standard number."""
    norm = normalize_is_number(is_number)
    total, items = SearchService.search_standards(db, query=norm, limit=1)
    if total == 0:
        raise HTTPException(status_code=404, detail=f"No Indian Standard found matching '{is_number}'")
    return SearchService.get_standard_detail(db, items[0]["id"])
