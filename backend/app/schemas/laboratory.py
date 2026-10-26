from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel

class LaboratoryScopeSchema(BaseModel):
    id: int
    standard_id: int
    is_number: str
    standard_title: str
    product_category: Optional[str] = None
    testing_capability: Optional[str] = None
    valid_until: Optional[date] = None

class LaboratoryBase(BaseModel):
    lab_code: str
    name: str
    address: str
    city: str
    district: Optional[str] = None
    state: str
    pincode: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    lab_type: str = "BIS Recognized"
    status: str = "Recognized"
    recognition_valid_until: Optional[date] = None
    source_url: Optional[str] = None
    is_fixture: bool = False

class LaboratorySummary(LaboratoryBase):
    id: int
    distance_km: Optional[float] = None
    scope_count: int = 0
    last_verified_at: datetime

    class Config:
        from_attributes = True

class LaboratoryDetail(LaboratoryBase):
    id: int
    last_verified_at: datetime
    created_at: datetime
    updated_at: datetime
    scopes: List[LaboratoryScopeSchema] = []

    class Config:
        from_attributes = True

class LaboratorySearchResponse(BaseModel):
    total: int
    page: int
    limit: int
    items: List[LaboratorySummary]
