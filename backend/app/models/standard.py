from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Standard(Base):
    __tablename__ = "standards"

    id = Column(Integer, primary_key=True, index=True)
    is_number = Column(String(100), unique=True, nullable=False, index=True)
    normalized_is = Column(String(100), nullable=False, index=True)
    title = Column(String(500), nullable=False, index=True)
    division = Column(String(100), nullable=True, index=True)  # e.g., CED, ETD, MED, TXD, FAD
    technical_committee = Column(String(150), nullable=True)
    publication_year = Column(Integer, nullable=True, index=True)
    status = Column(String(50), default="Current", nullable=False, index=True)  # Current, Revised, Withdrawn
    scope_abstract = Column(Text, nullable=True)  # Permitted public abstract/scope
    source_url = Column(String(500), nullable=True)
    verification_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_fixture = Column(Boolean, default=False, nullable=False, index=True)  # Distinguishes sample fixtures from verified imported data
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    relationships = relationship("StandardRelationship", back_populates="standard", cascade="all, delete-orphan")
    qco_links = relationship("QCOStandardLink", back_populates="standard", cascade="all, delete-orphan")
    lab_scopes = relationship("LaboratoryScope", back_populates="standard", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_standards_is_title", "normalized_is", "title"),
    )

class StandardRelationship(Base):
    __tablename__ = "standards_relationships"

    id = Column(Integer, primary_key=True, index=True)
    standard_id = Column(Integer, ForeignKey("standards.id", ondelete="CASCADE"), nullable=False, index=True)
    related_is_number = Column(String(100), nullable=False, index=True)
    relationship_type = Column(String(50), nullable=False)  # supersedes, superseded_by, refers_to, part_of, equivalent_to
    description = Column(String(255), nullable=True)

    standard = relationship("Standard", back_populates="relationships")
