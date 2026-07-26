import json
import time
from typing import Any, Dict, List, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import structlog

from app.ai.exceptions import AIConnectionError, ModelUnavailableError
from app.config.settings import settings

logger = structlog.get_logger("ai.ollama_client")


class OllamaClient:
    """
    Minimal Ollama HTTP client with timeout and retry handling.
    """

    def __init__(
        self,
        host: Optional[str] = None,
        model: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: int = 2,
    ) -> None:
        self.host = (host or settings.OLLAMA_HOST).rstrip("/")
        self.model = model or settings.OLLAMA_MODEL
        self.timeout = timeout or settings.OLLAMA_TIMEOUT
        self.max_retries = max_retries

    def health_check(self) -> bool:
        try:
            self.list_models()
            return True
        except AIConnectionError:
            return False

    def list_models(self) -> List[str]:
        response = self._request("GET", "/api/tags")
        models = response.get("models", [])
        return [model.get("name", "") for model in models if model.get("name")]

    def chat_completion(self, prompt: str, model: Optional[str] = None) -> str:
        selected_model = model or self.model
        logger.info(
            "Ollama chat completion started",
            model=selected_model,
            prompt_length=len(prompt),
        )
        start = time.perf_counter()
        response = self._request(
            "POST",
            "/api/generate",
            payload={
                "model": selected_model,
                "prompt": prompt,
                "stream": False,
            },
        )
        latency = time.perf_counter() - start
        logger.info(
            "Ollama chat completion completed",
            model=selected_model,
            latency=latency,
        )
        result = response.get("response")
        if not isinstance(result, str):
            raise AIConnectionError("Ollama response did not include text output")
        return result

    def run_inference(self, prompt: str, model: Optional[str] = None) -> str:
        return self.chat_completion(prompt, model=model)

    def ensure_model_available(self, model: Optional[str] = None) -> None:
        selected_model = model or self.model
        models = self.list_models()
        available_names = {name.split(":")[0] for name in models} | set(models)
        if selected_model not in available_names:
            raise ModelUnavailableError(
                f"Ollama model is unavailable: {selected_model}"
            )

    def _request(
        self, method: str, path: str, payload: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        url = f"{self.host}{path}"
        body = json.dumps(payload).encode("utf-8") if payload is not None else None
        request = Request(
            url,
            data=body,
            method=method,
            headers={"Content-Type": "application/json"},
        )

        last_error: Optional[Exception] = None
        for attempt in range(self.max_retries + 1):
            try:
                with urlopen(request, timeout=self.timeout) as response:
                    return json.loads(response.read().decode("utf-8"))
            except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
                last_error = exc
                logger.warning(
                    "Ollama request failed",
                    path=path,
                    attempt=attempt + 1,
                    error=str(exc),
                )
                if attempt < self.max_retries:
                    time.sleep(0.1 * (attempt + 1))

        raise AIConnectionError(f"Ollama request failed: {last_error}") from last_error
