import abc
from datetime import datetime
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from backend.app.models.provenance import OfficialSource, IngestionRun

class BaseIngestor(abc.ABC):
    def __init__(self, db: Session, dataset_name: str, source_portal: str, base_url: str):
        self.db = db
        self.dataset_name = dataset_name
        self.source_portal = source_portal
        self.base_url = base_url
        self.processed = 0
        self.upserted = 0
        self.rejected = 0
        self.errors: List[str] = []

    def get_or_create_source(self) -> OfficialSource:
        source = self.db.query(OfficialSource).filter(OfficialSource.name == self.source_portal).first()
        if not source:
            source = OfficialSource(
                name=self.source_portal,
                portal_type=self.dataset_name,
                base_url=self.base_url,
                licensing_terms="Public Government Data / Bureau of Indian Standards & Gazette of India Notifications",
                update_frequency="Weekly",
                status="Active"
            )
            self.db.add(source)
            self.db.commit()
            self.db.refresh(source)
        return source

    def start_run(self) -> IngestionRun:
        source = self.get_or_create_source()
        run = IngestionRun(
            source_id=source.id,
            dataset_name=self.dataset_name,
            status="Running",
            records_processed=0,
            records_upserted=0,
            records_rejected=0,
            started_at=datetime.utcnow()
        )
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)
        return run

    def finish_run(self, run: IngestionRun, status: str = "Completed", error_message: str = None):
        run.status = status
        run.records_processed = self.processed
        run.records_upserted = self.upserted
        run.records_rejected = self.rejected
        run.finished_at = datetime.utcnow()
        if error_message or self.errors:
            run.error_message = error_message or "\n".join(self.errors[:10])

        if run.source:
            run.source.last_polled_at = datetime.utcnow()
            if status == "Completed":
                run.source.last_success_at = datetime.utcnow()

        self.db.commit()

    @abc.abstractmethod
    def ingest_records(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Subclasses implement parsing, normalization, validation, and idempotent upserts."""
        pass
