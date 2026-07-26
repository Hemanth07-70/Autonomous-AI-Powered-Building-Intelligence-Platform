import json
from urllib.error import URLError

import pytest

from app.ai.client import OllamaClient
from app.ai.exceptions import AIConnectionError, ModelUnavailableError


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self):
        return json.dumps(self._payload).encode("utf-8")


def test_list_models(monkeypatch):
    def fake_urlopen(request, timeout):
        return FakeResponse({"models": [{"name": "qwen3:latest"}]})

    monkeypatch.setattr("app.ai.client.urlopen", fake_urlopen)
    client = OllamaClient(host="http://ollama.test", model="qwen3", timeout=1)

    assert client.list_models() == ["qwen3:latest"]


def test_run_inference(monkeypatch):
    def fake_urlopen(request, timeout):
        return FakeResponse({"response": '{"goal_type":"HVAC"}'})

    monkeypatch.setattr("app.ai.client.urlopen", fake_urlopen)
    client = OllamaClient(host="http://ollama.test", model="qwen3", timeout=1)

    assert client.run_inference("prompt") == '{"goal_type":"HVAC"}'


def test_chat_completion(monkeypatch):
    def fake_urlopen(request, timeout):
        return FakeResponse({"response": '{"goal_type":"HVAC"}'})

    monkeypatch.setattr("app.ai.client.urlopen", fake_urlopen)
    client = OllamaClient(host="http://ollama.test", model="qwen3", timeout=1)

    assert client.chat_completion("prompt") == '{"goal_type":"HVAC"}'


def test_health_check_false_on_connection_error(monkeypatch):
    def fake_urlopen(request, timeout):
        raise URLError("offline")

    monkeypatch.setattr("app.ai.client.urlopen", fake_urlopen)
    client = OllamaClient(
        host="http://ollama.test",
        model="qwen3",
        timeout=1,
        max_retries=0,
    )

    assert client.health_check() is False


def test_connection_error_after_retries(monkeypatch):
    def fake_urlopen(request, timeout):
        raise URLError("offline")

    monkeypatch.setattr("app.ai.client.urlopen", fake_urlopen)
    client = OllamaClient(
        host="http://ollama.test",
        model="qwen3",
        timeout=1,
        max_retries=0,
    )

    with pytest.raises(AIConnectionError):
        client.list_models()


def test_model_unavailable(monkeypatch):
    def fake_urlopen(request, timeout):
        return FakeResponse({"models": [{"name": "llama3:latest"}]})

    monkeypatch.setattr("app.ai.client.urlopen", fake_urlopen)
    client = OllamaClient(host="http://ollama.test", model="qwen3", timeout=1)

    with pytest.raises(ModelUnavailableError):
        client.ensure_model_available()
