from datetime import datetime, date
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from backend.app.models.laboratory import TestingLaboratory, LaboratoryScope
from backend.app.models.standard import Standard
from backend.app.services.search_service import normalize_is_number
from backend.app.ingestion.base import BaseIngestor

class LaboratoriesIngestor(BaseIngestor):
    def __init__(self, db: Session):
        super().__init__(
            db=db,
            dataset_name="Testing Laboratories Directory",
            source_portal="BIS LIMS Laboratory Directory",
            base_url="https://lims.bis.gov.in/"
        )

    def _parse_date(self, val) -> date:
        if isinstance(val, date):
            return val
        if isinstance(val, str) and val.strip():
            try:
                return datetime.strptime(val.strip(), "%Y-%m-%d").date()
            except ValueError:
                try:
                    return datetime.strptime(val.strip(), "%d-%m-%Y").date()
                except ValueError:
                    return None
        return None

    def ingest_records(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        run = self.start_run()
        try:
            # Pre-load existing labs and standards for high-performance in-memory lookups
            existing_labs = {l.lab_code: l for l in self.db.query(TestingLaboratory).all()}
            standards_by_norm = {s.normalized_is: s.id for s in self.db.query(Standard.normalized_is, Standard.id).all()}
            existing_scopes = {
                (s.laboratory_id, s.standard_id)
                for s in self.db.query(LaboratoryScope.laboratory_id, LaboratoryScope.standard_id).all()
            }

            batch_counter = 0
            pending_scopes = []

            for item in records:
                self.processed += 1
                lab_code = item.get("lab_code", "").strip()
                name = item.get("name", "").strip()
                city = item.get("city", "").strip()
                state = item.get("state", "").strip()

                if not lab_code or not name or not city or not state:
                    self.rejected += 1
                    self.errors.append(f"Row {self.processed}: Missing required 'lab_code', 'name', 'city', or 'state'")
                    continue

                valid_until = self._parse_date(item.get("recognition_valid_until"))
                is_fixture = bool(item.get("is_fixture", False))

                existing = existing_labs.get(lab_code)
                if existing:
                    existing.name = name
                    existing.address = item.get("address", existing.address)
                    existing.city = city
                    existing.district = item.get("district", existing.district)
                    existing.state = state
                    existing.pincode = item.get("pincode", existing.pincode)
                    existing.latitude = item.get("latitude", existing.latitude)
                    existing.longitude = item.get("longitude", existing.longitude)
                    existing.contact_person = item.get("contact_person", existing.contact_person)
                    existing.phone = item.get("phone", existing.phone)
                    existing.email = item.get("email", existing.email)
                    existing.lab_type = item.get("lab_type", existing.lab_type)
                    existing.status = item.get("status", existing.status)
                    existing.recognition_valid_until = valid_until or existing.recognition_valid_until
                    existing.source_url = item.get("source_url", existing.source_url)
                    existing.is_fixture = is_fixture
                    existing.last_verified_at = datetime.utcnow()
                    target_lab = existing
                else:
                    new_lab = TestingLaboratory(
                        lab_code=lab_code,
                        name=name,
                        address=item.get("address", f"{city}, {state}"),
                        city=city,
                        district=item.get("district"),
                        state=state,
                        pincode=item.get("pincode"),
                        latitude=item.get("latitude"),
                        longitude=item.get("longitude"),
                        contact_person=item.get("contact_person"),
                        phone=item.get("phone"),
                        email=item.get("email"),
                        lab_type=item.get("lab_type", "BIS Recognized"),
                        status=item.get("status", "Recognized"),
                        recognition_valid_until=valid_until,
                        source_url=item.get("source_url"),
                        is_fixture=is_fixture,
                        last_verified_at=datetime.utcnow()
                    )
                    self.db.add(new_lab)
                    existing_labs[lab_code] = new_lab
                    target_lab = new_lab

                # Queue testing scopes
                if "scopes" in item and isinstance(item["scopes"], list):
                    for scope in item["scopes"]:
                        is_str = scope if isinstance(scope, str) else scope.get("is_number")
                        if not is_str:
                            continue
                        norm = normalize_is_number(is_str)
                        std_id = standards_by_norm.get(norm)
                        if std_id:
                            pending_scopes.append((target_lab, std_id, scope, valid_until))

                self.upserted += 1
                batch_counter += 1
                if batch_counter >= 100:
                    self.db.flush()
                    batch_counter = 0

            self.db.flush()

            # Process queued scopes
            for target_lab, std_id, scope, valid_until in pending_scopes:
                scope_key = (target_lab.id, std_id)
                if scope_key not in existing_scopes:
                    new_scope = LaboratoryScope(
                        laboratory_id=target_lab.id,
                        standard_id=std_id,
                        product_category=scope.get("product_category") if isinstance(scope, dict) else None,
                        testing_capability=scope.get("testing_capability", "Complete Testing Scope") if isinstance(scope, dict) else "Complete Scope",
                        valid_until=valid_until
                    )
                    self.db.add(new_scope)
                    existing_scopes.add(scope_key)

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
