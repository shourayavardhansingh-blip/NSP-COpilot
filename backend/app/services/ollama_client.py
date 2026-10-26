import time
import socket
from urllib.parse import urlparse
import httpx
from typing import Optional, List, Dict, Any
from backend.app.config import settings

def is_service_port_open(url: str, timeout: float = 0.1) -> bool:
    """Pre-flight socket check to avoid long OS-level SYN retransmission delays."""
    try:
        parsed = urlparse(url)
        host = parsed.hostname or "127.0.0.1"
        port = parsed.port or 11434
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            return s.connect_ex((host, port)) == 0
    except Exception:
        return False

class OllamaClient:
    def __init__(
        self,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout: Optional[float] = None
    ):
        self.base_url = (base_url or settings.OLLAMA_BASE_URL).rstrip("/")
        self.model = model or settings.OLLAMA_MODEL
        self.timeout = timeout or settings.OLLAMA_TIMEOUT_SECONDS

    async def check_health(self) -> Dict[str, Any]:
        """
        Pings Ollama service and checks available models with fast pre-flight probe.
        """
        if not settings.OLLAMA_ENABLED:
            return {
                "status": "unavailable",
                "ollama_reachable": False,
                "configured_model": self.model,
                "available_models": [],
                "fallback_mode_active": True,
                "diagnostic_message": f"Ollama local inference is currently disabled or offline (OLLAMA_ENABLED=false). Operating in Deterministic Fast-Path mode with grounded citations."
            }

        if not is_service_port_open(self.base_url, timeout=0.1):
            return {
                "status": "unavailable",
                "ollama_reachable": False,
                "configured_model": self.model,
                "available_models": [],
                "fallback_mode_active": True,
                "diagnostic_message": f"Ollama daemon is offline at {self.base_url}. Using deterministic fast-path compliance engine."
            }

        try:
            fast_timeout = httpx.Timeout(connect=1.0, read=2.0, write=1.0, pool=0.5)
            async with httpx.AsyncClient(timeout=fast_timeout) as client:
                res = await client.get(f"{self.base_url}/api/tags")
                if res.status_code == 200:
                    data = res.json()
                    models = [m.get("name") for m in data.get("models", [])]
                    model_found = any(self.model in m for m in models)
                    return {
                        "status": "healthy" if model_found else "degraded",
                        "ollama_reachable": True,
                        "configured_model": self.model,
                        "available_models": models,
                        "fallback_mode_active": not model_found,
                        "diagnostic_message": "Ollama service connected and operational." if model_found else f"Ollama reachable, but model '{self.model}' is not pulled yet. Run 'ollama pull {self.model}'."
                    }
        except Exception as e:
            return {
                "status": "unavailable",
                "ollama_reachable": False,
                "configured_model": self.model,
                "available_models": [],
                "fallback_mode_active": True,
                "diagnostic_message": f"Ollama health check error: {str(e)}"
            }

    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.2
    ) -> Dict[str, Any]:
        """
        Sends multi-turn chat messages to Ollama /api/chat.
        Returns generated content and latency.
        """
        start_time = time.time()
        if not settings.OLLAMA_ENABLED or not is_service_port_open(self.base_url, timeout=0.1):
            return {
                "content": "",
                "latency_ms": int((time.time() - start_time) * 1000),
                "model": self.model,
                "success": False,
                "error": "Ollama local inference runtime is offline or disabled"
            }

        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }

        try:
            chat_timeout = httpx.Timeout(connect=1.0, read=self.timeout, write=5.0, pool=1.0)
            async with httpx.AsyncClient(timeout=chat_timeout) as client:
                res = await client.post(url, json=payload)
                res.raise_for_status()
                data = res.json()
                content = data.get("message", {}).get("content", "")
                latency_ms = int((time.time() - start_time) * 1000)
                return {
                    "content": content,
                    "latency_ms": latency_ms,
                    "model": self.model,
                    "success": True
                }
        except Exception as e:
            latency_ms = int((time.time() - start_time) * 1000)
            return {
                "content": "",
                "latency_ms": latency_ms,
                "model": self.model,
                "success": False,
                "error": str(e)
            }

ollama_client = OllamaClient()
