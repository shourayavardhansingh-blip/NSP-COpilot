from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.schemas.checklist import (
    ChecklistCreate, ChecklistUpdate, ChecklistSummary, ChecklistDetail,
    ChecklistTaskCreate, ChecklistTaskUpdate, GenerateChecklistRequest
)
from backend.app.services.checklist_service import ChecklistService

router = APIRouter(prefix="/checklists", tags=["Checklist Maker & Projects"])

@router.get("", response_model=List[ChecklistSummary])
def list_checklists(db: Session = Depends(get_db)):
    return ChecklistService.list_checklists(db)

@router.post("", response_model=ChecklistDetail)
def create_checklist(data: ChecklistCreate, db: Session = Depends(get_db)):
    return ChecklistService.create_checklist(db, data)

@router.post("/generate", response_model=ChecklistDetail)
def generate_checklist(data: GenerateChecklistRequest, db: Session = Depends(get_db)):
    return ChecklistService.generate_default_checklist(
        db=db,
        product_name=data.product_name,
        standard_number=data.standard_number,
        scheme_code=data.scheme_code or "SCHEME_I"
    )

@router.get("/{checklist_id}", response_model=ChecklistDetail)
def get_checklist(checklist_id: str, db: Session = Depends(get_db)):
    item = ChecklistService.get_checklist(db, checklist_id)
    if not item:
        raise HTTPException(status_code=404, detail="Checklist not found.")
    return item

@router.patch("/{checklist_id}", response_model=ChecklistDetail)
def update_checklist(checklist_id: str, data: ChecklistUpdate, db: Session = Depends(get_db)):
    item = ChecklistService.update_checklist(db, checklist_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="Checklist not found.")
    return item

@router.delete("/{checklist_id}")
def delete_checklist(checklist_id: str, db: Session = Depends(get_db)):
    success = ChecklistService.delete_checklist(db, checklist_id)
    if not success:
        raise HTTPException(status_code=404, detail="Checklist not found.")
    return {"status": "success", "message": "Checklist deleted successfully."}

@router.get("/{checklist_id}/export/csv")
def export_checklist_csv(checklist_id: str, db: Session = Depends(get_db)):
    csv_content = ChecklistService.export_csv(db, checklist_id)
    if csv_content is None:
        raise HTTPException(status_code=404, detail="Checklist not found.")
    
    filename = f"bis_compliance_checklist_{checklist_id[:8]}.csv"
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.post("/{checklist_id}/tasks", response_model=ChecklistDetail)
def add_task(checklist_id: str, data: ChecklistTaskCreate, db: Session = Depends(get_db)):
    item = ChecklistService.add_task(db, checklist_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="Checklist not found.")
    return item

@router.patch("/{checklist_id}/tasks/{task_id}", response_model=ChecklistDetail)
def update_task(checklist_id: str, task_id: str, data: ChecklistTaskUpdate, db: Session = Depends(get_db)):
    item = ChecklistService.update_task(db, checklist_id, task_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="Checklist or Task not found.")
    return item

@router.delete("/{checklist_id}/tasks/{task_id}")
def delete_task(checklist_id: str, task_id: str, db: Session = Depends(get_db)):
    success = ChecklistService.delete_task(db, checklist_id, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Checklist or Task not found.")
    return {"status": "success", "message": "Task removed successfully."}
