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

                existing = self.db.query(TestingLaboratory).filter(TestingLaboratory.lab_code == lab_code).first()
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
                    self.db.flush()
                    target_lab = new_lab

                # Ingest testing scopes
                if "scopes" in item and isinstance(item["scopes"], list):
                    for scope in item["scopes"]:
                        is_str = scope if isinstance(scope, str) else scope.get("is_number")
                        if not is_str:
                            continue
                        norm = normalize_is_number(is_str)
                        std = self.db.query(Standard).filter(
                            (Standard.normalized_is == norm) | (Standard.is_number == is_str)
                        ).first()
                        if std:
                            existing_scope = self.db.query(LaboratoryScope).filter(
                                LaboratoryScope.laboratory_id == target_lab.id,
                                LaboratoryScope.standard_id == std.id
                            ).first()
                            if not existing_scope:
                                new_scope = LaboratoryScope(
                                    laboratory_id=target_lab.id,
                                    standard_id=std.id,
                                    product_category=scope.get("product_category") if isinstance(scope, dict) else None,
                                    testing_capability=scope.get("testing_capability", "Complete Testing Scope") if isinstance(scope, dict) else "Complete Scope",
                                    valid_until=valid_until
                                )
                                self.db.add(new_scope)

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
