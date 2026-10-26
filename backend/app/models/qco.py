from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Date, ForeignKey, Index
from sqlalchemy.orm import relationship
from backend.app.database import Base

class QCO(Base):
    __tablename__ = "qcos"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(150), unique=True, nullable=False, index=True)
    title = Column(String(500), nullable=False, index=True)
    issuing_ministry = Column(String(200), nullable=False, index=True)  # DPIIT, MeitY, Ministry of Heavy Industries, Ministry of Steel, etc.
    product_category = Column(String(200), nullable=True, index=True)
    gazette_date = Column(Date, nullable=True, index=True)
    enforcement_date = Column(Date, nullable=True, index=True)
    status = Column(String(50), default="In Force", nullable=False, index=True)  # In Force, Upcoming, Superseded, Draft
    official_url = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
    is_fixture = Column(Boolean, default=False, nullable=False, index=True)
    last_verified_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    standards = relationship("QCOStandardLink", back_populates="qco", cascade="all, delete-orphan")
    amendments = relationship("QCOAmendment", back_populates="qco", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_qco_ministry_status", "issuing_ministry", "status"),
    )

class QCOStandardLink(Base):
    __tablename__ = "qco_standard_links"

    id = Column(Integer, primary_key=True, index=True)
    qco_id = Column(Integer, ForeignKey("qcos.id", ondelete="CASCADE"), nullable=False, index=True)
    standard_id = Column(Integer, ForeignKey("standards.id", ondelete="CASCADE"), nullable=False, index=True)
    applicable_date = Column(Date, nullable=True)
    exemption_notes = Column(Text, nullable=True)

    qco = relationship("QCO", back_populates="standards")
    standard = relationship("Standard", back_populates="qco_links")

class QCOAmendment(Base):
    __tablename__ = "qco_amendments"

    id = Column(Integer, primary_key=True, index=True)
    qco_id = Column(Integer, ForeignKey("qcos.id", ondelete="CASCADE"), nullable=False, index=True)
    amendment_number = Column(String(100), nullable=False)
    gazette_notification = Column(String(200), nullable=True)
    notification_date = Column(Date, nullable=True)
    effective_date = Column(Date, nullable=True)
    summary = Column(Text, nullable=False)
    source_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    qco = relationship("QCO", back_populates="amendments")
