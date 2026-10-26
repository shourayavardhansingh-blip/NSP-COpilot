from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class StandardRelationshipSchema(BaseModel):
    id: int
    related_is_number: str
    relationship_type: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

class StandardBase(BaseModel):
    is_number: str
    title: str
    division: Optional[str] = None
    technical_committee: Optional[str] = None
    publication_year: Optional[int] = None
    status: str = "Current"
    scope_abstract: Optional[str] = None
    source_url: Optional[str] = None
    is_fixture: bool = False

class StandardCreate(StandardBase):
    pass

class StandardSummary(BaseModel):
    id: int
    is_number: str
    normalized_is: str
    title: str
    division: Optional[str] = None
    publication_year: Optional[int] = None
    status: str
    is_fixture: bool
    source_url: Optional[str] = None
    has_qco: bool = False
    lab_count: int = 0

    class Config:
        from_attributes = True

class StandardDetail(StandardBase):
    id: int
    normalized_is: str
    verification_date: datetime
    created_at: datetime
    updated_at: datetime
    relationships: List[StandardRelationshipSchema] = []
    applicable_qcos: List[dict] = []
    accredited_labs: List[dict] = []

    class Config:
        from_attributes = True

class StandardSearchResponse(BaseModel):
    total: int
    page: int
    limit: int
    items: List[StandardSummary]
