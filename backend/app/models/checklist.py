import uuid
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Date, ForeignKey, Index
from sqlalchemy.orm import relationship
from backend.app.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Checklist(Base):
    __tablename__ = "checklists"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(200), nullable=False)
    product_name = Column(String(200), nullable=False)
    standard_number = Column(String(100), nullable=True)
    scheme_code = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    status = Column(String(50), default="In Progress", nullable=False)  # In Progress, Completed, Archived
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    tasks = relationship("ChecklistTask", back_populates="checklist", cascade="all, delete-orphan", order_by="ChecklistTask.order_index")

class ChecklistTask(Base):
    __tablename__ = "checklist_tasks"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    checklist_id = Column(String(36), ForeignKey("checklists.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    stage = Column(String(100), default="Documentation", nullable=False)  # Documentation, Pre-Testing, Factory Audit, Application Submission, Grant of Licence
    is_mandatory = Column(Boolean, default=False, nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)
    order_index = Column(Integer, default=0, nullable=False)
    notes = Column(Text, nullable=True)
    source_citation = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    checklist = relationship("Checklist", back_populates="tasks")

    __table_args__ = (
        Index("ix_tasks_checklist_order", "checklist_id", "order_index"),
    )
