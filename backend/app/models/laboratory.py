from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, Date, ForeignKey, Index
from sqlalchemy.orm import relationship
from backend.app.database import Base

class TestingLaboratory(Base):
    __tablename__ = "testing_laboratories"

    id = Column(Integer, primary_key=True, index=True)
    lab_code = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    address = Column(Text, nullable=False)
    city = Column(String(100), nullable=False, index=True)
    district = Column(String(100), nullable=True)
    state = Column(String(100), nullable=False, index=True)
    pincode = Column(String(20), nullable=True, index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    contact_person = Column(String(150), nullable=True)
    phone = Column(String(100), nullable=True)
    email = Column(String(150), nullable=True)
    lab_type = Column(String(50), default="BIS Recognized", nullable=False)  # BIS Central Lab, BIS Recognized, NABL Partner Lab
    status = Column(String(50), default="Recognized", nullable=False, index=True)  # Recognized, Renewal Pending, Suspended
    recognition_valid_until = Column(Date, nullable=True)
    source_url = Column(String(500), nullable=True)
    is_fixture = Column(Boolean, default=False, nullable=False, index=True)
    last_verified_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    scopes = relationship("LaboratoryScope", back_populates="laboratory", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_labs_state_city", "state", "city"),
    )

class LaboratoryScope(Base):
    __tablename__ = "laboratory_scopes"

    id = Column(Integer, primary_key=True, index=True)
    laboratory_id = Column(Integer, ForeignKey("testing_laboratories.id", ondelete="CASCADE"), nullable=False, index=True)
    standard_id = Column(Integer, ForeignKey("standards.id", ondelete="CASCADE"), nullable=False, index=True)
    product_category = Column(String(150), nullable=True)
    testing_capability = Column(Text, nullable=True)  # Complete scope or specific test methods
    valid_until = Column(Date, nullable=True)

    laboratory = relationship("TestingLaboratory", back_populates="scopes")
    standard = relationship("Standard", back_populates="lab_scopes")
