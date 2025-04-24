import json
import pytest
from jsonschema import validate

from core.models.llm import LLMMessage
from core.enums.llm_role import LLMRole
from adapters.prompts.pipeline_prompt import PipelinePrompt
from adapters.prompts.scenario_extraction_prompt import ScenarioExtractionPrompt
from tests.schemas.llm_response_schema import (
    pipeline_response_schema,
    scenario_response_schema
)

# ---------- Fixtures ----------

@pytest.fixture
def narration_payload():
    return {
        "narration_text": (
            "A escola estava vazia e as luzes fracas tremeluziam. "
            "Do lado de fora, trovões ecoavam pelo céu escuro."
        )
    }


@pytest.fixture
def structured_payload():
    return [
        {"line_number": 1, "text": "Ye Hong entrou na sala."},
        {"line_number": 2, "text": "\"Quem está aí?\""},
        {"line_number": 3, "text": "Ding! Habilidade em inglês +1..."}
    ]


# ---------- Helpers ----------

def assert_llm_message(message: LLMMessage, expected_role: LLMRole, contains: str):
    assert isinstance(message, LLMMessage)
    assert message.role == expected_role
    assert contains.lower() in message.content.lower()
    assert message.content.strip() != ""

# ---------- PipelinePrompt ----------

def test_pipeline_prompt_build_messages(structured_payload):
    prompt = PipelinePrompt()
    messages = prompt.build_messages(structured_payload)
    
    assert isinstance(messages, list)
    assert len(messages) == 2
    
    system_msg, user_msg = messages
    
    assert_llm_message(system_msg, LLMRole.SYSTEM, "tradução")
    assert_llm_message(user_msg, LLMRole.USER, '"line_number"')
    
    parsed = json.loads(user_msg.content)
    assert parsed == structured_payload
    
# ---------- ScenarioExtractionPrompt ----------

def test_scenario_extraction_prompt_build_messages(narration_payload):
    prompt = ScenarioExtractionPrompt()
    messages = prompt.build_messages(narration_payload)

    assert isinstance(messages, list)
    assert len(messages) == 2

    system_msg, user_msg = messages

    assert_llm_message(system_msg, LLMRole.SYSTEM, "descrição de cenários")
    assert_llm_message(user_msg, LLMRole.USER, narration_payload["narration_text"])
    assert user_msg.content == narration_payload["narration_text"]