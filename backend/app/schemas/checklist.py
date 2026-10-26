from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel

class ChecklistTaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    stage: str = "Documentation"
    is_mandatory: bool = False
    is_completed: bool = False
    order_index: int = 0
    notes: Optional[str] = None
    source_citation: Optional[str] = None

class ChecklistTaskCreate(ChecklistTaskBase):
    pass

class ChecklistTaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    stage: Optional[str] = None
    is_mandatory: Optional[bool] = None
    is_completed: Optional[bool] = None
    order_index: Optional[int] = None
    notes: Optional[str] = None
    source_citation: Optional[str] = None

class ChecklistTaskSchema(ChecklistTaskBase):
    id: str
    checklist_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ChecklistBase(BaseModel):
    title: str
    product_name: str
    standard_number: Optional[str] = None
    scheme_code: Optional[str] = None
    notes: Optional[str] = None
    status: str = "In Progress"

class ChecklistCreate(ChecklistBase):
    tasks: Optional[List[ChecklistTaskCreate]] = []

class ChecklistUpdate(BaseModel):
    title: Optional[str] = None
    product_name: Optional[str] = None
    standard_number: Optional[str] = None
    scheme_code: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None

class ChecklistSummary(ChecklistBase):
    id: str
    total_tasks: int = 0
    completed_tasks: int = 0
    completion_percentage: float = 0.0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ChecklistDetail(ChecklistBase):
    id: str
    created_at: datetime
    updated_at: datetime
    total_tasks: int = 0
    completed_tasks: int = 0
    completion_percentage: float = 0.0
    tasks: List[ChecklistTaskSchema] = []

    class Config:
        from_attributes = True

class GenerateChecklistRequest(BaseModel):
    product_name: str
    standard_number: Optional[str] = None
    scheme_code: Optional[str] = "SCHEME_I"
    target_notes: Optional[str] = None
