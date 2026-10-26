from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class CoverageStats(BaseModel):
    total_standards: int
    verified_standards: int
    fixture_standards: int
    
    total_qcos: int
    verified_qcos: int
    active_qcos: int
    
    total_laboratories: int
    verified_laboratories: int
    total_scopes_mapped: int
    
    total_schemes: int
    total_official_sources: int
    
    dataset_freshness_date: Optional[datetime] = None
    last_ingestion_run: Optional[Dict[str, Any]] = None
    
    ai_status: str
    ai_model: str

class CoverageGap(BaseModel):
    category: str
    official_source: str
    status: str
    description: str
    action_required: str

class CoverageDashboardResponse(BaseModel):
    stats: CoverageStats
    sources: List[Dict[str, Any]]
    recent_ingestion_runs: List[Dict[str, Any]]
    coverage_gaps: List[CoverageGap]
