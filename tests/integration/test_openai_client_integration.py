import os
import pytest

from core.models.llm import LLMMessage, LLMRole
from adapters.llm.openai_client import OpenAIClient


@pytest.mark.integration
def test_openai_client_integration_simple_math():
    """
    Integração real com a API da OpenAI para verificar que:
    - O cliente autentica corretamente
    - Envia mensagens no formato esperado
    - Recebe resposta não vazia
    - Preenche usage e raw adequadamente
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY não está definido; pulando teste de integração")

    client = OpenAIClient(api_key=api_key, model="gpt-3.5-turbo")
    messages = [
        LLMMessage(role=LLMRole.USER, content="Qual é a soma de 2 + 2?")
    ]

    response = client.chat(
        messages,
        temperature=0.0,
        max_tokens=50,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    assert isinstance(response.text, str)
    assert response.text.strip() != ""
    assert "4" in response.text

    assert response.usage is not None
    assert response.usage.prompt_tokens > 0
    assert response.usage.completion_tokens >= 0
    assert response.usage.total_tokens == response.usage.prompt_tokens + response.usage.completion_tokens

    assert isinstance(response.raw, dict)
    assert "choices" in response.raw
