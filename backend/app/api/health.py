from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.app.database import get_db
from backend.app.services.ollama_client import ollama_client
from backend.app.config import settings

router = APIRouter(prefix="/health", tags=["Health & Diagnostics"])

@router.get("")
async def get_health(db: Session = Depends(get_db)):
    # 1. DB check
    db_status = "healthy"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    # 2. AI runtime check
    ai_health = await ollama_client.check_health()

    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": db_status,
        "ai_engine": ai_health
    }
