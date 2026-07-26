import asyncio
from typing import Any, Dict, List, Optional
import httpx
import structlog

from app.ai.exceptions import AIConnectionError, ModelUnavailableError
from app.config.settings import settings

logger = structlog.get_logger("ai.nvidia_client")

class NvidiaClient:
    """
    NVIDIA Cloud AI HTTP client utilizing httpx.AsyncClient with timeout and retry handling.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: int = 2,
    ) -> None:
        self.api_key = api_key or settings.NVIDIA_API_KEY
        self.base_url = (base_url or settings.NVIDIA_BASE_URL).rstrip("/")
        self.model = model or settings.NVIDIA_MODEL
        self.timeout = timeout or settings.AI_TIMEOUT
        self.max_retries = max_retries

    def health_check(self) -> bool:
        try:
            self.ensure_model_available(self.model)
            return True
        except AIConnectionError:
            return False

    def list_models(self) -> List[str]:
        # Return a static list or fetch from API if there's a compatible /models endpoint.
        # For simplicity with NVIDIA API, we just list the configured model.
        return [self.model]

    def chat_completion(self, prompt: str, model: Optional[str] = None) -> str:
        return asyncio.run(self._async_chat_completion(prompt, model))

    async def _async_chat_completion(self, prompt: str, model: Optional[str] = None) -> str:
        selected_model = model or self.model
        logger.info(
            "NVIDIA chat completion started",
            provider=settings.AI_PROVIDER,
            model=selected_model,
            prompt_length=len(prompt),
        )

        payload = {
            "model": selected_model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": settings.AI_TEMPERATURE,
            "max_tokens": settings.AI_MAX_TOKENS,
            "stream": False,
        }

        start_time = asyncio.get_event_loop().time()
        
        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(
                        f"{self.base_url}/chat/completions",
                        json=payload,
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json"
                        },
                    )
                    
                    if response.status_code == 401:
                        raise AIConnectionError("NVIDIA API: Unauthorized (401)")
                    elif response.status_code == 429:
                        raise AIConnectionError("NVIDIA API: Rate Limit Exceeded (429)")
                    elif response.status_code >= 500:
                        raise AIConnectionError(f"NVIDIA API: Server Error ({response.status_code})")
                    
                    response.raise_for_status()
                    data = response.json()
                    
                    latency = asyncio.get_event_loop().time() - start_time
                    usage = data.get("usage", {})
                    
                    logger.info(
                        "NVIDIA chat completion completed",
                        provider=settings.AI_PROVIDER,
                        model=selected_model,
                        latency=latency,
                        total_tokens=usage.get("total_tokens"),
                        request_id=data.get("id")
                    )
                    
                    choices = data.get("choices", [])
                    if not choices:
                        raise AIConnectionError("NVIDIA API returned no choices.")
                        
                    return choices[0].get("message", {}).get("content", "")

            except (httpx.RequestError, httpx.HTTPStatusError, AIConnectionError) as exc:
                last_error = exc
                logger.warning(
                    "NVIDIA request failed",
                    attempt=attempt + 1,
                    error=str(exc),
                )
                if attempt < self.max_retries:
                    await asyncio.sleep(0.5 * (attempt + 1))
                    
        raise AIConnectionError(f"NVIDIA request failed after retries: {last_error}") from last_error

    def run_inference(self, prompt: str, model: Optional[str] = None) -> str:
        return self.chat_completion(prompt, model=model)

    def ensure_model_available(self, model: Optional[str] = None) -> None:
        # NVIDIA API will reject invalid models on inference.
        # We assume the configured model is available unless an inference call fails with 404/400.
        # This avoids an extra models list fetch that might not match exactly.
        if not self.api_key:
            raise AIConnectionError("NVIDIA_API_KEY is missing.")
