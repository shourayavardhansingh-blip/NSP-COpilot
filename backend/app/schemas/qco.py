from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel

class QCOAmendmentSchema(BaseModel):
    id: int
    amendment_number: str
    gazette_notification: Optional[str] = None
    notification_date: Optional[date] = None
    effective_date: Optional[date] = None
    summary: str
    source_url: Optional[str] = None

    class Config:
        from_attributes = True

class QCOStandardLinkSchema(BaseModel):
    standard_id: int
    is_number: str
    title: str
    applicable_date: Optional[date] = None
    exemption_notes: Optional[str] = None

class QCOBase(BaseModel):
    order_number: str
    title: str
    issuing_ministry: str
    product_category: Optional[str] = None
    gazette_date: Optional[date] = None
    enforcement_date: Optional[date] = None
    status: str = "In Force"
    official_url: Optional[str] = None
    notes: Optional[str] = None
    is_fixture: bool = False

class QCOSummary(QCOBase):
    id: int
    standard_count: int = 0
    amendment_count: int = 0
    last_verified_at: datetime

    class Config:
        from_attributes = True

class QCODetail(QCOBase):
    id: int
    last_verified_at: datetime
    created_at: datetime
    updated_at: datetime
    standards: List[QCOStandardLinkSchema] = []
    amendments: List[QCOAmendmentSchema] = []

    class Config:
        from_attributes = True

class QCOSearchResponse(BaseModel):
    total: int
    page: int
    limit: int
    items: List[QCOSummary]
