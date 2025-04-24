import pytest
from unittest.mock import MagicMock, patch
from openai import OpenAIError

from core.models.llm import LLMMessage, LLMRole
from adapters.llm.openai_client import OpenAIClient


@pytest.fixture
def mock_openai_response():
    return MagicMock(
        choices=[MagicMock(message=MagicMock(content="Resposta gerada."))],
        usage=MagicMock(
            prompt_tokens=10,
            completion_tokens=20,
            total_tokens=30
        ),
        to_dict=lambda: {"mock": "yes"}
    )


def test_openai_client_chat_success(mock_openai_response):
    messages = [LLMMessage(role=LLMRole.USER, content="Qual o sentido da vida?")]
        
    with patch("adapters.llm.openai_client.OpenAI") as mock_openai:
        mock_instance = mock_openai.return_value
        mock_instance.chat.completions.create.return_value = mock_openai_response
        client = OpenAIClient(api_key="test")
        response = client.chat(messages)

    assert response.text == "Resposta gerada."
    assert response.usage.total_tokens == 30
    assert isinstance(response.raw, dict)


def test_openai_client_chat_raises_runtime_error():
    client = OpenAIClient(api_key="fake-key", model="gpt-3.5-turbo")
    message = LLMMessage(role=LLMRole.USER, content="Teste de exceção")

    with patch.object(client.client.chat.completions, "create", side_effect=OpenAIError("Erro simulado")):
        with pytest.raises(RuntimeError, match=r"\[OpenAIClient.chat\] Error: Erro simulado"):
            client.chat([message])


def test_openai_client_without_usage():
    client = OpenAIClient(api_key="test-key", model="gpt-4o")

    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Resposta"))]
    mock_response.to_dict.return_value = {"choices": [{"message": {"content": "Resposta"}}]}
    del mock_response.usage 

    with patch.object(client.client.chat.completions, "create", return_value=mock_response):
        message = LLMMessage(role=LLMRole.USER, content="Olá, tudo bem?")
        response = client.chat([message])

    assert response.text == "Resposta"
    assert response.usage is None
    assert isinstance(response.raw, dict)