import os
from pathlib import Path
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent.parent

def get_cors_origins() -> list[str]:
    default_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]
    env_origins = os.getenv("CORS_ORIGINS", "").strip()
    if not env_origins:
        return default_origins
    
    # Support JSON array format e.g. ["https://my-app.vercel.app"]
    if env_origins.startswith("[") and env_origins.endswith("]"):
        try:
            import json
            parsed = json.loads(env_origins)
            if isinstance(parsed, list):
                return list(dict.fromkeys(default_origins + [str(o).strip() for o in parsed if o]))
        except Exception:
            pass
            
    # Support comma-separated format e.g. https://my-app.vercel.app,https://my-domain.com
    parts = [p.strip() for p in env_origins.split(",") if p.strip()]
    return list(dict.fromkeys(default_origins + parts))

class Settings(BaseModel):
    APP_NAME: str = "BIS AI Copilot"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/bis_copilot.db")
    
    # Ollama / Local AI
    OLLAMA_ENABLED: bool = os.getenv("OLLAMA_ENABLED", "false").lower() == "true"
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
    OLLAMA_TIMEOUT_SECONDS: float = float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "15.0"))
    AI_FALLBACK_ENABLED: bool = True
    
    # Security & CORS (retains localhost and merges any production domains)
    CORS_ORIGINS: list[str] = Field(default_factory=get_cors_origins)
    
    # Paths
    DATA_DIR: Path = BASE_DIR / "data"
    SEED_DIR: Path = BASE_DIR / "data" / "seed"
    IMPORTS_DIR: Path = BASE_DIR / "data" / "imports"

settings = Settings()
