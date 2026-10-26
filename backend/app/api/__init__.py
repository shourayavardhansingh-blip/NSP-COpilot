from fastapi import APIRouter
from backend.app.api.health import router as health_router
from backend.app.api.standards import router as standards_router
from backend.app.api.qco import router as qco_router
from backend.app.api.laboratories import router as laboratories_router
from backend.app.api.schemes import router as schemes_router
from backend.app.api.checklists import router as checklists_router
from backend.app.api.ai import router as ai_router
from backend.app.api.stats import router as stats_router
from backend.app.api.sources import router as sources_router

api_router = APIRouter(prefix="/api")

api_router.include_router(health_router)
api_router.include_router(standards_router)
api_router.include_router(qco_router)
api_router.include_router(laboratories_router)
api_router.include_router(schemes_router)
api_router.include_router(checklists_router)
api_router.include_router(ai_router)
api_router.include_router(stats_router)
api_router.include_router(sources_router)
