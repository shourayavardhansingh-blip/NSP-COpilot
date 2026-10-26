import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.app.config import settings
from backend.app.database import engine, Base, SessionLocal
from backend.app.ingestion.runner import run_seed_ingestion
from backend.app.models.standard import Standard
from backend.app.api import api_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("bis_copilot")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables exist and seed if empty
    logger.info("Initializing BIS Copilot relational database...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        count = db.query(Standard).count()
        if count == 0:
            logger.info("Database empty on startup. Triggering initial seed ingestion...")
            run_seed_ingestion(db)
        else:
            logger.info(f"Database online with {count} Indian Standards.")
    finally:
        db.close()
    
    yield
    logger.info("BIS Copilot backend service shutting down.")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Professional AI-Powered BIS Information and Compliance Platform",
    lifespan=lifespan
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Safe Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error on {request.method} {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An error occurred while processing the regulatory query. Details have been logged safely."
        }
    )

# Include API Router
app.include_router(api_router)

@app.get("/")
def root_endpoint():
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs_url": "/docs",
        "api_root": "/api",
        "status": "operational"
    }
