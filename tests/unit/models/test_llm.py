import pytest
from core.enums.llm_role import LLMRole
from core.models.llm import LLMMessage, LLMUsage, LLMResponse


# ========== LLMMessage ==========

def test_llm_message_valid(sample_llm_message):
    assert sample_llm_message.role == LLMRole.USER
    assert sample_llm_message.content == "Traduz esse parágrafo, por favor."

def test_llm_message_with_name():
    msg = LLMMessage(role=LLMRole.ASSISTANT, content="Resposta", name="Bot")
    assert msg.name == "Bot"
    assert msg.role == "assistant"
    
def test_llm_message_to_dict(sample_llm_message):
    data = sample_llm_message.to_dict()
    assert data['role'] == 'user'
    assert data['content'] == 'Traduz esse parágrafo, por favor.'
    assert data['name'] == 'usuário1'
    
def test_to_dict_without_name():
    message = LLMMessage(role=LLMRole.USER, content="Hello", name=None)
    result = message.to_dict()
    assert result == {"role": "user", "content": "Hello"}
    assert "name" not in result
    
def test_llm_message_from_dict():
    data = {"role": "user", "content": "Teste", "name": "n"}
    msg = LLMMessage.from_dict(data)
    assert msg.name == "n"
    assert msg.role == LLMRole.USER
    
# ----- Validações -----

def test_llm_message_invalid_role():
    with pytest.raises(ValueError):
        LLMMessage(role="usuário", content="oi")

def test_llm_message_empty_content():
    with pytest.raises(ValueError):
        LLMMessage(role=LLMRole.SYSTEM, content="  ")

# ========== LLMUsage ==========

def test_llm_usage_valid(sample_llm_usage):
    assert sample_llm_usage.prompt_tokens == 100
    assert sample_llm_usage.total_tokens == 250

def test_llm_usage_to_dict(sample_llm_usage):
    data = sample_llm_usage.to_dict()
    
    assert data['prompt_tokens'] == 100
    assert data['total_tokens'] == 250
    
def test_llm_usage_from_dict(sample_llm_usage_dict):
    d = sample_llm_usage_dict.copy()
    usage = LLMUsage.from_dict(d)
    assert usage.total_tokens == 250
    assert usage.completion_tokens == 150
    assert usage.prompt_tokens == 100
    
# ----- Validações -----

def test_llm_usage_invalid_negative():
    with pytest.raises(ValueError):
        LLMUsage(prompt_tokens=-1, completion_tokens=5, total_tokens=4)

def test_llm_usage_invalid_sum():
    with pytest.raises(ValueError):
        LLMUsage(prompt_tokens=5, completion_tokens=10, total_tokens=12)

# ========== LLMResponse ==========

def test_llm_response_valid(sample_llm_response):
    resp = sample_llm_response
    assert resp.text.startswith("Texto")
    assert resp.usage.total_tokens == 250
    assert resp.raw == {"example": "response"}
    
def test_llm_response_to_dict(sample_llm_response):
    data = sample_llm_response.to_dict()
    
    assert data['text'].startswith("Texto")
    assert data['usage']['total_tokens'] == 250
    assert data['raw'] == {"example": "response"}

def test_llm_response_from_dict(sample_llm_response_dict):
    d = sample_llm_response_dict.copy()
    r = LLMResponse.from_dict(d)
    assert r.text == "Texto traduzido com sucesso."
    assert isinstance(r.usage, LLMUsage)
    assert r.raw["example"] == "response"

# ----- Validações -----

def test_llm_response_empty_text():
    with pytest.raises(ValueError):
        LLMResponse(text="   ")

def test_llm_response_invalid_usage_type():
    with pytest.raises(TypeError):
        LLMResponse(text="ok", usage="not usage")

def test_llm_response_invalid_raw_type():
    with pytest.raises(TypeError):
        LLMResponse(text="ok", raw=["isso não é um dict"])
