```python
import os
import time
from typing import Optional, List, Dict, Any

import httpx

from backend.app.config import settings


class OllamaClient:
    """
    Backward-compatible client that uses the Groq API.

    Keeping the class and instance names unchanged allows existing
    imports such as `from backend.app.ollama_client import ollama_client`
    to continue working.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout: Optional[float] = None,
    ):
        self.base_url = (
            base_url
            or os.getenv(
                "GROQ_BASE_URL",
                "https://api.groq.com/openai/v1",
            )
        ).rstrip("/")

        self.model = model or os.getenv(
            "GROQ_MODEL",
            "llama-3.3-70b-versatile",
        )

        self.api_key = os.getenv("GROQ_API_KEY", "")
        self.timeout = timeout or float(
            os.getenv("GROQ_TIMEOUT_SECONDS", "60")
        )

    async def check_health(self) -> Dict[str, Any]:
        """Check whether Groq credentials and API access are configured."""

        if not self.api_key:
            return {
                "status": "unavailable",
                "ollama_reachable": False,
                "configured_model": self.model,
                "available_models": [],
                "fallback_mode_active": True,
                "diagnostic_message": (
                    "GROQ_API_KEY is missing from the backend environment."
                ),
            }

        try:
            timeout = httpx.Timeout(10.0)

            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(
                    f"{self.base_url}/models",
                    headers={
                        "Authorization": f"Bearer {self.api_key}"
                    },
                )

            if response.status_code == 200:
                data = response.json()
                models = [
                    item.get("id", "")
                    for item in data.get("data", [])
                ]

                model_found = self.model in models

                return {
                    "status": "healthy" if model_found else "degraded",
                    "ollama_reachable": True,
                    "configured_model": self.model,
                    "available_models": models,
                    "fallback_mode_active": not model_found,
                    "diagnostic_message": (
                        "Groq API connected and configured model is available."
                        if model_found
                        else (
                            f"Groq API is reachable, but model "
                            f"'{self.model}' was not found in the available "
                            "model list. Check the Groq Console for supported "
                            "models available to your account."
                        )
                    ),
                }

            return {
                "status": "unavailable",
                "ollama_reachable": False,
                "configured_model": self.model,
                "available_models": [],
                "fallback_mode_active": True,
                "diagnostic_message": (
                    f"Groq API returned HTTP {response.status_code}."
                ),
            }

        except Exception as exc:
            return {
                "status": "unavailable",
                "ollama_reachable": False,
                "configured_model": self.model,
                "available_models": [],
                "fallback_mode_active": True,
                "diagnostic_message": (
                    f"Groq health check failed: {type(exc).__name__}"
                ),
            }

    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.2,
    ) -> Dict[str, Any]:
        """Send a chat completion request to Groq."""

        start_time = time.time()

        if not self.api_key:
            return {
                "content": "",
                "latency_ms": 0,
                "model": self.model,
                "success": False,
                "error": "GROQ_API_KEY is not configured.",
            }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": False,
        }

        try:
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(self.timeout)
            ) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json=payload,
                )

                response.raise_for_status()
                data = response.json()

                content = (
                    data.get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "")
                )

                return {
                    "content": content,
                    "latency_ms": int(
                        (time.time() - start_time) * 1000
                    ),
                    "model": self.model,
                    "success": bool(conten
```
