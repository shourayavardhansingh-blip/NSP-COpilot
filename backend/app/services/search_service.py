import re
import math
from typing import Optional, List, Tuple
from sqlalchemy import or_, func, desc
from sqlalchemy.orm import Session
from backend.app.models.standard import Standard, StandardRelationship
from backend.app.models.qco import QCO, QCOStandardLink
from backend.app.models.laboratory import TestingLaboratory, LaboratoryScope

def normalize_is_number(is_str: str) -> str:
    """
    Normalizes standard numbers for resilient exact and fuzzy matching.
    Examples:
    'IS 302 (Part 1): 2008' -> 'IS302-1:2008'
    'is302' -> 'IS302'
    '302' -> 'IS302'
    'IS 16046 (Part 1)' -> 'IS16046-1'
    """
    if not is_str:
        return ""
    s = is_str.upper().strip()
    # Normalize 'PART 1' or 'PART-1' or '(PART 1)' to '-1'
    s = re.sub(r'[\(\[\{]?\s*PART\s*[:\-]?\s*(\d+)\s*[\)\]\}]?', r'-\1', s, flags=re.IGNORECASE)
    # Remove all spaces and periods
    s = re.sub(r'[\s\.\-]+', '', s)
    # Ensure IS prefix
    if not s.startswith("IS"):
        s = "IS" + s
    return s

def calculate_haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate great-circle distance between two points in km."""
    R = 6371.0  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 1)

class SearchService:
    @staticmethod
    def search_standards(
        db: Session,
        query: Optional[str] = None,
        division: Optional[str] = None,
        status: Optional[str] = None,
        has_qco: Optional[bool] = None,
        page: int = 1,
        limit: int = 20
    ) -> Tuple[int, List[dict]]:
        stmt = db.query(Standard)

        if division:
            stmt = stmt.filter(Standard.division.ilike(f"%{division}%"))
        
        if status:
            stmt = stmt.filter(Standard.status.ilike(status))

        if has_qco is not None:
            if has_qco:
                stmt = stmt.filter(Standard.qco_links.any())
            else:
                stmt = stmt.filter(~Standard.qco_links.any())

        if query:
            clean_q = query.strip()
            norm_q = normalize_is_number(clean_q)
            
            # Prioritize exact normalized IS match, then prefix, then title contains
            stmt = stmt.filter(
                or_(
                    Standard.normalized_is.ilike(f"%{norm_q}%"),
                    Standard.is_number.ilike(f"%{clean_q}%"),
                    Standard.title.ilike(f"%{clean_q}%"),
                    Standard.division.ilike(f"%{clean_q}%"),
                    Standard.scope_abstract.ilike(f"%{clean_q}%")
                )
            )

        total = stmt.count()
        standards = stmt.order_by(Standard.is_number).offset((page - 1) * limit).limit(limit).all()

        results = []
        for s in standards:
            qco_count = len(s.qco_links)
            lab_count = len(s.lab_scopes)
            results.append({
                "id": s.id,
                "is_number": s.is_number,
                "normalized_is": s.normalized_is,
                "title": s.title,
                "division": s.division,
                "publication_year": s.publication_year,
                "status": s.status,
                "is_fixture": s.is_fixture,
                "source_url": s.source_url,
                "has_qco": qco_count > 0,
                "lab_count": lab_count
            })

        return total, results

    @staticmethod
    def get_standard_detail(db: Session, standard_id: int) -> Optional[dict]:
        s = db.query(Standard).filter(Standard.id == standard_id).first()
        if not s:
            return None

        # Build relationships
        rel_list = [
            {
                "id": r.id,
                "related_is_number": r.related_is_number,
                "relationship_type": r.relationship_type,
                "description": r.description
            } for r in s.relationships
        ]

        # Build QCO links
        qco_list = [
            {
                "qco_id": link.qco.id,
                "order_number": link.qco.order_number,
                "title": link.qco.title,
                "issuing_ministry": link.qco.issuing_ministry,
                "status": link.qco.status,
                "enforcement_date": str(link.qco.enforcement_date) if link.qco.enforcement_date else None,
                "official_url": link.qco.official_url,
                "exemption_notes": link.exemption_notes
            } for link in s.qco_links
        ]

        # Build accredited labs
        lab_list = [
            {
                "lab_id": scope.laboratory.id,
                "lab_code": scope.laboratory.lab_code,
                "lab_name": scope.laboratory.name,
                "city": scope.laboratory.city,
                "state": scope.laboratory.state,
                "status": scope.laboratory.status,
                "testing_capability": scope.testing_capability,
                "valid_until": str(scope.valid_until) if scope.valid_until else None,
                "source_url": scope.laboratory.source_url
            } for scope in s.lab_scopes
        ]

        return {
            "id": s.id,
            "is_number": s.is_number,
            "normalized_is": s.normalized_is,
            "title": s.title,
            "division": s.division,
            "technical_committee": s.technical_committee,
            "publication_year": s.publication_year,
            "status": s.status,
            "scope_abstract": s.scope_abstract,
            "source_url": s.source_url,
            "is_fixture": s.is_fixture,
            "verification_date": s.verification_date,
            "created_at": s.created_at,
            "updated_at": s.updated_at,
            "relationships": rel_list,
            "applicable_qcos": qco_list,
            "accredited_labs": lab_list
        }

    @staticmethod
    def search_qcos(
        db: Session,
        query: Optional[str] = None,
        ministry: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        limit: int = 20
    ) -> Tuple[int, List[dict]]:
        stmt = db.query(QCO)

        if ministry:
            stmt = stmt.filter(QCO.issuing_ministry.ilike(f"%{ministry}%"))

        if status:
            stmt = stmt.filter(QCO.status.ilike(status))

        if query:
            clean_q = query.strip()
            stmt = stmt.filter(
                or_(
                    QCO.order_number.ilike(f"%{clean_q}%"),
                    QCO.title.ilike(f"%{clean_q}%"),
                    QCO.product_category.ilike(f"%{clean_q}%"),
                    QCO.notes.ilike(f"%{clean_q}%"),
                    QCO.standards.any(QCOStandardLink.standard.has(Standard.is_number.ilike(f"%{clean_q}%")))
                )
            )

        total = stmt.count()
        qcos = stmt.order_by(desc(QCO.gazette_date)).offset((page - 1) * limit).limit(limit).all()

        results = []
        for q in qcos:
            results.append({
                "id": q.id,
                "order_number": q.order_number,
                "title": q.title,
                "issuing_ministry": q.issuing_ministry,
                "product_category": q.product_category,
                "gazette_date": q.gazette_date,
                "enforcement_date": q.enforcement_date,
                "status": q.status,
                "official_url": q.official_url,
                "notes": q.notes,
                "is_fixture": q.is_fixture,
                "standard_count": len(q.standards),
                "amendment_count": len(q.amendments),
                "last_verified_at": q.last_verified_at
            })

        return total, results

    @staticmethod
    def get_qco_detail(db: Session, qco_id: int) -> Optional[dict]:
        q = db.query(QCO).filter(QCO.id == qco_id).first()
        if not q:
            return None

        std_links = [
            {
                "standard_id": link.standard.id,
                "is_number": link.standard.is_number,
                "title": link.standard.title,
                "applicable_date": link.applicable_date,
                "exemption_notes": link.exemption_notes
            } for link in q.standards
        ]

        amendments = [
            {
                "id": a.id,
                "amendment_number": a.amendment_number,
                "gazette_notification": a.gazette_notification,
                "notification_date": a.notification_date,
                "effective_date": a.effective_date,
                "summary": a.summary,
                "source_url": a.source_url
            } for a in q.amendments
        ]

        return {
            "id": q.id,
            "order_number": q.order_number,
            "title": q.title,
            "issuing_ministry": q.issuing_ministry,
            "product_category": q.product_category,
            "gazette_date": q.gazette_date,
            "enforcement_date": q.enforcement_date,
            "status": q.status,
            "official_url": q.official_url,
            "notes": q.notes,
            "is_fixture": q.is_fixture,
            "last_verified_at": q.last_verified_at,
            "created_at": q.created_at,
            "updated_at": q.updated_at,
            "standards": std_links,
            "amendments": amendments
        }

    @staticmethod
    def search_laboratories(
        db: Session,
        query: Optional[str] = None,
        state: Optional[str] = None,
        city: Optional[str] = None,
        status: Optional[str] = None,
        standard_is: Optional[str] = None,
        user_lat: Optional[float] = None,
        user_lon: Optional[float] = None,
        page: int = 1,
        limit: int = 20
    ) -> Tuple[int, List[dict]]:
        stmt = db.query(TestingLaboratory)

        if state:
            stmt = stmt.filter(TestingLaboratory.state.ilike(f"%{state}%"))

        if city:
            stmt = stmt.filter(TestingLaboratory.city.ilike(f"%{city}%"))

        if status:
            stmt = stmt.filter(TestingLaboratory.status.ilike(status))

        if standard_is:
            clean_is = standard_is.strip()
            norm_is = normalize_is_number(clean_is)
            stmt = stmt.filter(
                TestingLaboratory.scopes.any(
                    LaboratoryScope.standard.has(
                        or_(
                            Standard.normalized_is.ilike(f"%{norm_is}%"),
                            Standard.is_number.ilike(f"%{clean_is}%")
                        )
                    )
                )
            )

        if query:
            clean_q = query.strip()
            stmt = stmt.filter(
                or_(
                    TestingLaboratory.name.ilike(f"%{clean_q}%"),
                    TestingLaboratory.lab_code.ilike(f"%{clean_q}%"),
                    TestingLaboratory.city.ilike(f"%{clean_q}%"),
                    TestingLaboratory.state.ilike(f"%{clean_q}%"),
                    TestingLaboratory.pincode.ilike(f"%{clean_q}%"),
                    TestingLaboratory.address.ilike(f"%{clean_q}%")
                )
            )

        total = stmt.count()
        labs = stmt.all()

        results = []
        for lab in labs:
            dist = None
            if user_lat is not None and user_lon is not None and lab.latitude and lab.longitude:
                dist = calculate_haversine_distance(user_lat, user_lon, lab.latitude, lab.longitude)

            results.append({
                "id": lab.id,
                "lab_code": lab.lab_code,
                "name": lab.name,
                "address": lab.address,
                "city": lab.city,
                "district": lab.district,
                "state": lab.state,
                "pincode": lab.pincode,
                "latitude": lab.latitude,
                "longitude": lab.longitude,
                "contact_person": lab.contact_person,
                "phone": lab.phone,
                "email": lab.email,
                "lab_type": lab.lab_type,
                "status": lab.status,
                "recognition_valid_until": lab.recognition_valid_until,
                "source_url": lab.source_url,
                "is_fixture": lab.is_fixture,
                "distance_km": dist,
                "scope_count": len(lab.scopes),
                "last_verified_at": lab.last_verified_at
            })

        # Sort by distance if location provided, else by name
        if user_lat is not None and user_lon is not None:
            results.sort(key=lambda x: (x["distance_km"] is None, x["distance_km"]))
        else:
            results.sort(key=lambda x: x["name"])

        # Manual slice for pagination
        start = (page - 1) * limit
        end = start + limit
        paginated = results[start:end]

        return total, paginated
