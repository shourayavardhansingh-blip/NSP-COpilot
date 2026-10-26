import os
import json
from pathlib import Path
from typing import Dict, Any
from sqlalchemy.orm import Session
from backend.app.database import engine, Base, SessionLocal
from backend.app.config import settings
from backend.app.ingestion.schemes_ingestor import SchemesIngestor
from backend.app.ingestion.standards_ingestor import StandardsIngestor
from backend.app.ingestion.qco_ingestor import QCOIngestor
from backend.app.ingestion.labs_ingestor import LaboratoriesIngestor
from backend.app.models.standard import Standard
from backend.app.models.qco import QCO
from backend.app.models.laboratory import TestingLaboratory, LaboratoryScope
from backend.app.models.scheme import CertificationScheme

def load_json(filepath: Path) -> list:
    if not filepath.exists():
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def run_seed_ingestion(db: Session = None) -> Dict[str, Any]:
    """Runs full idempotent ingestion pipeline across official BIS datasets."""
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    close_session = False
    if db is None:
        db = SessionLocal()
        close_session = True

    results = {}
    seed_dir = settings.SEED_DIR

    try:
        # 1. Certification Schemes
        schemes_data = load_json(seed_dir / "schemes.json")
        schemes_ingestor = SchemesIngestor(db)
        results["schemes"] = schemes_ingestor.ingest_records(schemes_data)

        # 2. Standards Catalogue
        standards_data = load_json(seed_dir / "standards.json")
        stds_ingestor = StandardsIngestor(db)
        results["standards"] = stds_ingestor.ingest_records(standards_data)

        # 3. Quality Control Orders
        qco_data = load_json(seed_dir / "qcos.json")
        qco_ingestor = QCOIngestor(db)
        results["qcos"] = qco_ingestor.ingest_records(qco_data)

        # 4. Testing Laboratories & Scopes
        labs_data = load_json(seed_dir / "laboratories.json")
        labs_ingestor = LaboratoriesIngestor(db)
        results["laboratories"] = labs_ingestor.ingest_records(labs_data)

        # Compute summary stats
        results["totals"] = {
            "standards_count": db.query(Standard).count(),
            "qco_count": db.query(QCO).count(),
            "labs_count": db.query(TestingLaboratory).count(),
            "scopes_count": db.query(LaboratoryScope).count(),
            "schemes_count": db.query(CertificationScheme).count()
        }
        return results

    finally:
        if close_session:
            db.close()

if __name__ == "__main__":
    print("Initiating BIS official dataset seed ingestion...")
    stats = run_seed_ingestion()
    print(f"Ingestion completed successfully: {json.dumps(stats, indent=2)}")
