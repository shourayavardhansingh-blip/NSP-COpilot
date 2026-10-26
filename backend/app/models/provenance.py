from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base

class OfficialSource(Base):
    __tablename__ = "official_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    portal_type = Column(String(100), nullable=False)  # Standards Portal, LIMS Lab Directory, e-BIS, DPIIT Gazette, CRS Portal
    base_url = Column(String(500), nullable=False)
    licensing_terms = Column(Text, nullable=True)
    update_frequency = Column(String(100), default="Weekly", nullable=False)
    last_polled_at = Column(DateTime, nullable=True)
    last_success_at = Column(DateTime, nullable=True)
    status = Column(String(50), default="Active", nullable=False)  # Active, Degraded, Offline, Manual Only
    notes = Column(Text, nullable=True)

    ingestion_runs = relationship("IngestionRun", back_populates="source", cascade="all, delete-orphan")

class IngestionRun(Base):
    __tablename__ = "ingestion_runs"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("official_sources.id", ondelete="SET NULL"), nullable=True)
    dataset_name = Column(String(100), nullable=False)
    status = Column(String(50), default="Running", nullable=False)  # Running, Completed, Failed, Partial
    records_processed = Column(Integer, default=0, nullable=False)
    records_upserted = Column(Integer, default=0, nullable=False)
    records_rejected = Column(Integer, default=0, nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    finished_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    provenance_details = Column(Text, nullable=True)

    source = relationship("OfficialSource", back_populates="ingestion_runs")
