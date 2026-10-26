from datetime import datetime
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from backend.app.models.scheme import CertificationScheme
from backend.app.ingestion.base import BaseIngestor

class SchemesIngestor(BaseIngestor):
    def __init__(self, db: Session):
        super().__init__(
            db=db,
            dataset_name="Certification Schemes",
            source_portal="BIS Conformity Assessment Regulations",
            base_url="https://www.bis.gov.in/product-certification/conformity-assessment-regulations/"
        )

    def ingest_records(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        run = self.start_run()
        try:
            for item in records:
                self.processed += 1
                code = item.get("code", "").strip()
                name = item.get("name", "").strip()

                if not code or not name:
                    self.rejected += 1
                    self.errors.append(f"Row {self.processed}: Missing required 'code' or 'name'")
                    continue

                existing = self.db.query(CertificationScheme).filter(CertificationScheme.code == code).first()
                if existing:
                    existing.name = name
                    existing.description = item.get("description", existing.description)
                    existing.governing_act = item.get("governing_act", existing.governing_act)
                    existing.mark_name = item.get("mark_name", existing.mark_name)
                    existing.typical_timeline_weeks = item.get("typical_timeline_weeks", existing.typical_timeline_weeks)
                    existing.factory_audit_required = bool(item.get("factory_audit_required", True))
                    existing.sample_testing_required = bool(item.get("sample_testing_required", True))
                    existing.surveillance_frequency = item.get("surveillance_frequency", existing.surveillance_frequency)
                    existing.documentation_requirements = item.get("documentation_requirements", existing.documentation_requirements)
                    existing.guidance_url = item.get("guidance_url", existing.guidance_url)
                else:
                    new_scheme = CertificationScheme(
                        code=code,
                        name=name,
                        description=item.get("description", ""),
                        governing_act=item.get("governing_act"),
                        mark_name=item.get("mark_name", "Standard Mark"),
                        typical_timeline_weeks=item.get("typical_timeline_weeks"),
                        factory_audit_required=bool(item.get("factory_audit_required", True)),
                        sample_testing_required=bool(item.get("sample_testing_required", True)),
                        surveillance_frequency=item.get("surveillance_frequency"),
                        documentation_requirements=item.get("documentation_requirements"),
                        guidance_url=item.get("guidance_url")
                    )
                    self.db.add(new_scheme)

                self.upserted += 1

            self.db.commit()
            self.finish_run(run, status="Completed")
        except Exception as e:
            self.db.rollback()
            self.finish_run(run, status="Failed", error_message=str(e))
            raise e

        return {
            "processed": self.processed,
            "upserted": self.upserted,
            "rejected": self.rejected,
            "errors": self.errors
        }
