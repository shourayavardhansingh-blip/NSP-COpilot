import csv
import io
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from backend.app.models.checklist import Checklist, ChecklistTask
from backend.app.schemas.checklist import (
    ChecklistCreate, ChecklistUpdate, ChecklistTaskCreate, ChecklistTaskUpdate
)

class ChecklistService:
    @staticmethod
    def list_checklists(db: Session) -> List[dict]:
        checklists = db.query(Checklist).order_by(Checklist.updated_at.desc()).all()
        results = []
        for c in checklists:
            total_tasks = len(c.tasks)
            completed_tasks = sum(1 for t in c.tasks if t.is_completed)
            pct = round((completed_tasks / total_tasks * 100.0), 1) if total_tasks > 0 else 0.0
            results.append({
                "id": c.id,
                "title": c.title,
                "product_name": c.product_name,
                "standard_number": c.standard_number,
                "scheme_code": c.scheme_code,
                "notes": c.notes,
                "status": c.status,
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "completion_percentage": pct,
                "created_at": c.created_at,
                "updated_at": c.updated_at
            })
        return results

    @staticmethod
    def get_checklist(db: Session, checklist_id: str) -> Optional[dict]:
        c = db.query(Checklist).filter(Checklist.id == checklist_id).first()
        if not c:
            return None

        tasks = sorted(c.tasks, key=lambda t: t.order_index)
        total_tasks = len(tasks)
        completed_tasks = sum(1 for t in tasks if t.is_completed)
        pct = round((completed_tasks / total_tasks * 100.0), 1) if total_tasks > 0 else 0.0

        return {
            "id": c.id,
            "title": c.title,
            "product_name": c.product_name,
            "standard_number": c.standard_number,
            "scheme_code": c.scheme_code,
            "notes": c.notes,
            "status": c.status,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "completion_percentage": pct,
            "created_at": c.created_at,
            "updated_at": c.updated_at,
            "tasks": [
                {
                    "id": t.id,
                    "checklist_id": t.checklist_id,
                    "title": t.title,
                    "description": t.description,
                    "stage": t.stage,
                    "is_mandatory": t.is_mandatory,
                    "is_completed": t.is_completed,
                    "order_index": t.order_index,
                    "notes": t.notes,
                    "source_citation": t.source_citation,
                    "created_at": t.created_at,
                    "updated_at": t.updated_at
                } for t in tasks
            ]
        }

    @staticmethod
    def create_checklist(db: Session, data: ChecklistCreate) -> dict:
        c = Checklist(
            title=data.title,
            product_name=data.product_name,
            standard_number=data.standard_number,
            scheme_code=data.scheme_code,
            notes=data.notes,
            status=data.status
        )
        db.add(c)
        db.flush()

        if data.tasks:
            for idx, task_data in enumerate(data.tasks):
                task = ChecklistTask(
                    checklist_id=c.id,
                    title=task_data.title,
                    description=task_data.description,
                    stage=task_data.stage,
                    is_mandatory=task_data.is_mandatory,
                    is_completed=task_data.is_completed,
                    order_index=task_data.order_index if task_data.order_index is not None else idx,
                    notes=task_data.notes,
                    source_citation=task_data.source_citation
                )
                db.add(task)

        db.commit()
        return ChecklistService.get_checklist(db, c.id)

    @staticmethod
    def update_checklist(db: Session, checklist_id: str, data: ChecklistUpdate) -> Optional[dict]:
        c = db.query(Checklist).filter(Checklist.id == checklist_id).first()
        if not c:
            return None

        update_dict = data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(c, field, value)

        db.commit()
        return ChecklistService.get_checklist(db, checklist_id)

    @staticmethod
    def delete_checklist(db: Session, checklist_id: str) -> bool:
        c = db.query(Checklist).filter(Checklist.id == checklist_id).first()
        if not c:
            return False
        db.delete(c)
        db.commit()
        return True

    @staticmethod
    def add_task(db: Session, checklist_id: str, data: ChecklistTaskCreate) -> Optional[dict]:
        c = db.query(Checklist).filter(Checklist.id == checklist_id).first()
        if not c:
            return None

        max_index = max([t.order_index for t in c.tasks], default=-1)
        task = ChecklistTask(
            checklist_id=checklist_id,
            title=data.title,
            description=data.description,
            stage=data.stage,
            is_mandatory=data.is_mandatory,
            is_completed=data.is_completed,
            order_index=data.order_index if data.order_index is not None else max_index + 1,
            notes=data.notes,
            source_citation=data.source_citation
        )
        db.add(task)
        db.commit()
        return ChecklistService.get_checklist(db, checklist_id)

    @staticmethod
    def update_task(db: Session, checklist_id: str, task_id: str, data: ChecklistTaskUpdate) -> Optional[dict]:
        task = db.query(ChecklistTask).filter(
            ChecklistTask.id == task_id,
            ChecklistTask.checklist_id == checklist_id
        ).first()
        if not task:
            return None

        update_dict = data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(task, field, value)

        db.commit()
        return ChecklistService.get_checklist(db, checklist_id)

    @staticmethod
    def delete_task(db: Session, checklist_id: str, task_id: str) -> bool:
        task = db.query(ChecklistTask).filter(
            ChecklistTask.id == task_id,
            ChecklistTask.checklist_id == checklist_id
        ).first()
        if not task:
            return False
        db.delete(task)
        db.commit()
        return True

    @staticmethod
    def generate_default_checklist(
        db: Session,
        product_name: str,
        standard_number: Optional[str] = None,
        scheme_code: str = "SCHEME_I"
    ) -> dict:
        """
        Generates a standard compliant checklist based on BIS Scheme rules.
        """
        is_scheme_ii = (scheme_code == "SCHEME_II" or "CRS" in str(scheme_code))
        std_ref = f" under {standard_number}" if standard_number else ""

        tasks = [
            # 1. Documentation
            ChecklistTaskCreate(
                title=f"Identify applicable Indian Standard{std_ref}",
                description="Confirm product scope, technical ratings, and applicable gazette QCO orders.",
                stage="Documentation",
                is_mandatory=True,
                order_index=0,
                source_citation="BIS Act 2016 Section 13 / e-BIS Portal"
            ),
            ChecklistTaskCreate(
                title="Prepare Technical Construction File (TCF)",
                description="Assemble bill of materials, circuit diagrams, component specifications, and user manual.",
                stage="Documentation",
                is_mandatory=True,
                order_index=1,
                source_citation="BIS Product Certification Scheme Documentation Guidelines"
            ),
            # 2. Testing
            ChecklistTaskCreate(
                title="Identify accredited testing laboratory",
                description="Select a BIS-recognized laboratory with verified scope for sample testing.",
                stage="Pre-Testing",
                is_mandatory=True,
                order_index=2,
                source_citation="BIS LIMS Portal (lims.bis.gov.in)"
            ),
            ChecklistTaskCreate(
                title="Submit test samples and obtain Type Test Report",
                description="Submit physical production samples for safety and performance testing to the standard.",
                stage="Pre-Testing",
                is_mandatory=True,
                order_index=3,
                source_citation="Scheme-I Guidelines for Laboratory Testing"
            ),
        ]

        if not is_scheme_ii:
            # Scheme-I requires factory audit & in-house test equipment
            tasks.extend([
                ChecklistTaskCreate(
                    title="Install in-house test equipment and calibration records",
                    description="Ensure all required testing apparatus specified in Scheme of Inspection and Testing (SIT) are calibrated and operational.",
                    stage="Factory Audit",
                    is_mandatory=True,
                    order_index=4,
                    source_citation="BIS Scheme of Inspection and Testing (SIT)"
                ),
                ChecklistTaskCreate(
                    title="Appoint qualified Quality Control personnel",
                    description="Maintain dedicated technical staff responsible for routine and lot inspection.",
                    stage="Factory Audit",
                    is_mandatory=True,
                    order_index=5,
                    source_citation="BIS Licensing Regulations"
                ),
                ChecklistTaskCreate(
                    title="Facilitate BIS Officer Factory Inspection",
                    description="Host BIS certification officer for on-site verification of manufacturing process and counter-testing of samples.",
                    stage="Factory Audit",
                    is_mandatory=True,
                    order_index=6,
                    source_citation="BIS General Guidelines for Factory Inspection"
                )
            ])

        # Application and Grant
        tasks.extend([
            ChecklistTaskCreate(
                title="Submit Application on Manakonline Portal",
                description="Complete Form-V online application, upload documents, and submit statutory application fee.",
                stage="Application Submission",
                is_mandatory=True,
                order_index=7,
                source_citation="manakonline.in e-BIS Portal"
            ),
            ChecklistTaskCreate(
                title="Grant of BIS Licence / Registration",
                description="Receive CM/L (Certification Marks Licence) or Registration Number; sign performance agreement.",
                stage="Grant of Licence",
                is_mandatory=True,
                order_index=8,
                source_citation="BIS Conformity Assessment Regulations"
            ),
            ChecklistTaskCreate(
                title="Procure Standard Mark / ISI artwork and begin compliant labelling",
                description="Affix Standard Mark with licence number on product packaging and user documentation according to marking guidelines.",
                stage="Grant of Licence",
                is_mandatory=True,
                order_index=9,
                source_citation="BIS Guidelines for Affixing ISI/CRS Mark"
            )
        ])

        payload = ChecklistCreate(
            title=f"Compliance Roadmap for {product_name}",
            product_name=product_name,
            standard_number=standard_number,
            scheme_code=scheme_code,
            notes=f"Auto-generated compliance checklist for {product_name} conforming to {scheme_code} requirements.",
            status="In Progress",
            tasks=tasks
        )

        return ChecklistService.create_checklist(db, payload)

    @staticmethod
    def export_csv(db: Session, checklist_id: str) -> Optional[str]:
        data = ChecklistService.get_checklist(db, checklist_id)
        if not data:
            return None

        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)

        # Header metadata
        writer.writerow(["Checklist Title", data["title"]])
        writer.writerow(["Product Name", data["product_name"]])
        writer.writerow(["Indian Standard", data["standard_number"] or "N/A"])
        writer.writerow(["Certification Scheme", data["scheme_code"] or "N/A"])
        writer.writerow(["Total Tasks", data["total_tasks"]])
        writer.writerow(["Completed Tasks", data["completed_tasks"]])
        writer.writerow(["Completion %", f"{data['completion_percentage']}%"])
        writer.writerow([])

        # Table columns
        writer.writerow([
            "Order", "Stage", "Task Title", "Description", "Mandatory?", "Status", "Source Citation", "Notes"
        ])

        for t in data["tasks"]:
            writer.writerow([
                t["order_index"] + 1,
                t["stage"],
                t["title"],
                t["description"] or "",
                "Mandatory" if t["is_mandatory"] else "Recommended",
                "Completed" if t["is_completed"] else "Pending",
                t["source_citation"] or "",
                t["notes"] or ""
            ])

        return output.getvalue()
