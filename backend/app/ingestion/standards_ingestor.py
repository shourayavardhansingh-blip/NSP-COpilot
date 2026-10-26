from datetime import datetime
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from backend.app.models.standard import Standard, StandardRelationship
from backend.app.services.search_service import normalize_is_number
from backend.app.ingestion.base import BaseIngestor

class StandardsIngestor(BaseIngestor):
    def __init__(self, db: Session):
        super().__init__(
            db=db,
            dataset_name="Standards Catalogue",
            source_portal="BIS Know Your Standard Portal",
            base_url="https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/knowyourstandards/indian_standards/"
        )

    def ingest_records(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        run = self.start_run()
        try:
            # High-performance bulk in-memory index
            existing_standards = {s.normalized_is: s for s in self.db.query(Standard).all()}
            existing_relationships = {
                (r.standard_id, r.related_is_number, r.relationship_type)
                for r in self.db.query(
                    StandardRelationship.standard_id,
                    StandardRelationship.related_is_number,
                    StandardRelationship.relationship_type
                ).all()
            }

            batch_counter = 0
            pending_relationships = []

            for item in records:
                self.processed += 1
                is_num = item.get("is_number", "").strip()
                title = item.get("title", "").strip()

                if not is_num or not title:
                    self.rejected += 1
                    self.errors.append(f"Row {self.processed}: Missing required 'is_number' or 'title'")
                    continue

                norm_is = normalize_is_number(is_num)
                existing = existing_standards.get(norm_is)

                pub_year = item.get("publication_year")
                if pub_year and isinstance(pub_year, str) and pub_year.isdigit():
                    pub_year = int(pub_year)
                elif not isinstance(pub_year, int):
                    pub_year = None

                is_fixture = bool(item.get("is_fixture", False))

                if existing:
                    existing.title = title
                    existing.division = item.get("division", existing.division)
                    existing.technical_committee = item.get("technical_committee", existing.technical_committee)
                    existing.publication_year = pub_year or existing.publication_year
                    existing.status = item.get("status", existing.status)
                    existing.scope_abstract = item.get("scope_abstract", existing.scope_abstract)
                    existing.source_url = item.get("source_url", existing.source_url)
                    existing.is_fixture = is_fixture
                    existing.verification_date = datetime.utcnow()
                    target_std = existing
                else:
                    new_std = Standard(
                        is_number=is_num,
                        normalized_is=norm_is,
                        title=title,
                        division=item.get("division"),
                        technical_committee=item.get("technical_committee"),
                        publication_year=pub_year,
                        status=item.get("status", "Current"),
                        scope_abstract=item.get("scope_abstract"),
                        source_url=item.get("source_url"),
                        is_fixture=is_fixture,
                        verification_date=datetime.utcnow()
                    )
                    self.db.add(new_std)
                    existing_standards[norm_is] = new_std
                    target_std = new_std

                # Queue relationships
                if "relationships" in item and isinstance(item["relationships"], list):
                    for rel in item["relationships"]:
                        rel_num = rel.get("related_is_number", "").strip()
                        rel_type = rel.get("relationship_type", "refers_to")
                        desc = rel.get("description")
                        if rel_num:
                            pending_relationships.append((target_std, rel_num, rel_type, desc))

                self.upserted += 1
                batch_counter += 1

                # Flush in chunks of 500 for memory efficiency
                if batch_counter >= 500:
                    self.db.flush()
                    batch_counter = 0

            self.db.flush()

            # Process queued relationships now that all standards have IDs
            for target_std, rel_num, rel_type, desc in pending_relationships:
                rel_key = (target_std.id, rel_num, rel_type)
                if rel_key not in existing_relationships:
                    new_rel = StandardRelationship(
                        standard_id=target_std.id,
                        related_is_number=rel_num,
                        relationship_type=rel_type,
                        description=desc
                    )
                    self.db.add(new_rel)
                    existing_relationships.add(rel_key)

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
