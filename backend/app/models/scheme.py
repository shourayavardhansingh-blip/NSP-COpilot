from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from backend.app.database import Base

class CertificationScheme(Base):
    __tablename__ = "certification_schemes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)  # SCHEME_I, SCHEME_II (CRS), SCHEME_IV, SCHEME_X
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    governing_act = Column(String(200), nullable=True)  # BIS Act 2016, Rules 2018
    mark_name = Column(String(100), nullable=False)  # ISI Mark, CRS Standard Mark
    typical_timeline_weeks = Column(Integer, nullable=True)
    factory_audit_required = Column(Boolean, default=True, nullable=False)
    sample_testing_required = Column(Boolean, default=True, nullable=False)
    surveillance_frequency = Column(String(100), nullable=True)
    documentation_requirements = Column(Text, nullable=True)
    guidance_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
