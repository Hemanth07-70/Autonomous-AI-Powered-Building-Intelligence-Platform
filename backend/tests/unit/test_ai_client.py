import pytest
import httpx
from unittest.mock import AsyncMock, patch

from app.ai.client import NvidiaClient
from app.ai.exceptions import AIConnectionError, ModelUnavailableError


class FakeResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError("error", request=None, response=self)


@pytest.fixture
def client():
    return NvidiaClient(
        api_key="test-key",
        base_url="https://test",
        model="test-model",
        timeout=1,
        max_retries=0,
    )


def test_list_models(client):
    assert client.list_models() == ["test-model"]


@patch("httpx.AsyncClient.post", new_callable=AsyncMock)
def test_chat_completion(mock_post, client):
    mock_post.return_value = FakeResponse({
        "id": "123",
        "choices": [{"message": {"content": '{"goal_type":"HVAC"}'}}],
        "usage": {"total_tokens": 100}
    })

    result = client.chat_completion("prompt")
    assert result == '{"goal_type":"HVAC"}'


@patch("httpx.AsyncClient.post", new_callable=AsyncMock)
def test_run_inference(mock_post, client):
    mock_post.return_value = FakeResponse({
        "id": "123",
        "choices": [{"message": {"content": '{"goal_type":"HVAC"}'}}],
        "usage": {"total_tokens": 100}
    })

    result = client.run_inference("prompt")
    assert result == '{"goal_type":"HVAC"}'


@patch("httpx.AsyncClient.post", new_callable=AsyncMock)
def test_health_check_false_on_connection_error(mock_post, client):
    client.api_key = None
    assert client.health_check() is False


@patch("httpx.AsyncClient.post", new_callable=AsyncMock)
def test_connection_error_after_retries(mock_post, client):
    mock_post.side_effect = httpx.RequestError("offline")

    with pytest.raises(AIConnectionError):
        client.chat_completion("prompt")


def test_model_unavailable(client):
    client.api_key = None
    with pytest.raises(AIConnectionError):
        client.ensure_model_available()
