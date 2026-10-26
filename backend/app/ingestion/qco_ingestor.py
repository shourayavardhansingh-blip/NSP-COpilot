from datetime import datetime, date
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from backend.app.models.qco import QCO, QCOStandardLink, QCOAmendment
from backend.app.models.standard import Standard
from backend.app.services.search_service import normalize_is_number
from backend.app.ingestion.base import BaseIngestor

class QCOIngestor(BaseIngestor):
    def __init__(self, db: Session):
        super().__init__(
            db=db,
            dataset_name="Quality Control Orders",
            source_portal="DPIIT & Gazette of India QCO Repository",
            base_url="https://dpiit.gov.in/technical-regulations/quality-control-orders"
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
                order_num = item.get("order_number", "").strip()
                title = item.get("title", "").strip()
                ministry = item.get("issuing_ministry", "").strip()

                if not order_num or not title or not ministry:
                    self.rejected += 1
                    self.errors.append(f"Row {self.processed}: Missing required 'order_number', 'title', or 'issuing_ministry'")
                    continue

                gazette_dt = self._parse_date(item.get("gazette_date"))
                enforce_dt = self._parse_date(item.get("enforcement_date"))
                is_fixture = bool(item.get("is_fixture", False))

                existing = self.db.query(QCO).filter(QCO.order_number == order_num).first()
                if existing:
                    existing.title = title
                    existing.issuing_ministry = ministry
                    existing.product_category = item.get("product_category", existing.product_category)
                    existing.gazette_date = gazette_dt or existing.gazette_date
                    existing.enforcement_date = enforce_dt or existing.enforcement_date
                    existing.status = item.get("status", existing.status)
                    existing.official_url = item.get("official_url", existing.official_url)
                    existing.notes = item.get("notes", existing.notes)
                    existing.is_fixture = is_fixture
                    existing.last_verified_at = datetime.utcnow()
                    target_qco = existing
                else:
                    new_qco = QCO(
                        order_number=order_num,
                        title=title,
                        issuing_ministry=ministry,
                        product_category=item.get("product_category"),
                        gazette_date=gazette_dt,
                        enforcement_date=enforce_dt,
                        status=item.get("status", "In Force"),
                        official_url=item.get("official_url"),
                        notes=item.get("notes"),
                        is_fixture=is_fixture,
                        last_verified_at=datetime.utcnow()
                    )
                    self.db.add(new_qco)
                    self.db.flush()
                    target_qco = new_qco

                # Link Standards
                if "standards" in item and isinstance(item["standards"], list):
                    for std_ref in item["standards"]:
                        is_str = std_ref if isinstance(std_ref, str) else std_ref.get("is_number")
                        if not is_str:
                            continue
                        norm = normalize_is_number(is_str)
                        std = self.db.query(Standard).filter(
                            (Standard.normalized_is == norm) | (Standard.is_number == is_str)
                        ).first()
                        if std:
                            existing_link = self.db.query(QCOStandardLink).filter(
                                QCOStandardLink.qco_id == target_qco.id,
                                QCOStandardLink.standard_id == std.id
                            ).first()
                            if not existing_link:
                                new_link = QCOStandardLink(
                                    qco_id=target_qco.id,
                                    standard_id=std.id,
                                    applicable_date=enforce_dt,
                                    exemption_notes=std_ref.get("exemption_notes") if isinstance(std_ref, dict) else None
                                )
                                self.db.add(new_link)

                # Add amendments if provided
                if "amendments" in item and isinstance(item["amendments"], list):
                    for amd in item["amendments"]:
                        amd_num = amd.get("amendment_number")
                        if amd_num:
                            exists_amd = self.db.query(QCOAmendment).filter(
                                QCOAmendment.qco_id == target_qco.id,
                                QCOAmendment.amendment_number == amd_num
                            ).first()
                            if not exists_amd:
                                new_amd = QCOAmendment(
                                    qco_id=target_qco.id,
                                    amendment_number=amd_num,
                                    gazette_notification=amd.get("gazette_notification"),
                                    notification_date=self._parse_date(amd.get("notification_date")),
                                    effective_date=self._parse_date(amd.get("effective_date")),
                                    summary=amd.get("summary", "Order amendment notification"),
                                    source_url=amd.get("source_url")
                                )
                                self.db.add(new_amd)

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
