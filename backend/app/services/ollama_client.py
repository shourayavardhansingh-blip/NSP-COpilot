
import os
import time
from typing import Optional, List, Dict, Any

import httpx


class OllamaClient:
    """
    Backward-compatible client that uses Groq's OpenAI-compatible API.
    The existing class name is retained to avoid breaking imports elsewhere.
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

        self.timeout = timeout or float(
            os.getenv("GROQ_TIMEOUT_SECONDS", "60")
        )

    async def check_health(self) -> Dict[str, Any]:
        """Check whether Groq credentials and API access are working."""

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            return {
                "status": "unavailable",
                "ollama_reachable": False,
                "configured_model": self.model,
                "available_models": [],
                "fallback_mode_active": True,
                "diagnostic_message": (
                    "GROQ_API_KEY is not configured."
                ),
            }

        try:
            timeout = httpx.Timeout(10.0, connect=5.0)

            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(
                    f"{self.base_url}/models",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                    },
                )

            if response.status_code != 200:
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

            models_data = response.json().get("data", [])
            models = [
                item.get("id", "")
                for item in models_data
                if item.get("id")
            ]

            model_found = self.model in models

            return {
                "status": "healthy" if model_found else "degraded",
                "ollama_reachable": True,
                "configured_model": self.model,
                "available_models": models,
                "fallback_mode_active": not model_found,
                "diagnostic_message": (
                    "Groq API connected successfully."
                    if model_found
                    else (
                        "Groq API connected, but the configured model "
                        "was not found. Check GROQ_MODEL in Render."
                    )
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
        """Send a chat request to Groq and return the generated answer."""

        start_time = time.time()
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            return {
                "content": "",
                "latency_ms": int((time.time() - start_time) * 1000),
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
            timeout = httpx.Timeout(
                self.timeout,
                connect=10.0,
            )

            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                    json=payload,
                )

                response.raise_for_status()
                data = response.json()

            choices = data.get("choices", [])
            content = (
                choices[0].get("message", {}).get("content", "")
                if choices
                else ""
            )

            if not content:
                raise ValueError("Groq returned an empty response.")

            return {
                "content": content,
                "latency_ms": int((time.time() - start_time) * 1000),
                "model": data.get("model", self.model),
                "success": True,
            }

        except httpx.HTTPStatusError as exc:
            status_code = exc.response.status_code

            if status_code == 401:
                error = "Groq API authentication failed. Check the API key."
            elif status_code == 429:
                error = "Groq rate limit or quota reached. Try again later."
            else:
                error = f"Groq API returned HTTP {status_code}."

            return {
                "content": "",
                "latency_ms": int((time.time() - start_time) * 1000),
                "model": self.model,
                "success": False,
                "error": error,
            }

        except Exception as exc:
            return {
                "content": "",
                "latency_ms": int((time.time() - start_time) * 1000),
                "model": self.model,
                "success": False,
                "error": f"Groq request failed: {type(exc).__name__}",
            }


# Keep the existing import name so other backend modules remain compatible.
ollama_client = OllamaClient()


