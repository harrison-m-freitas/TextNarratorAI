import pytest
import json
from unittest.mock import MagicMock

from core.enums import LLMRole
from core.models.line import Line
from core.models.llm import LLMMessage, LLMResponse

from adapters.analyzer.llm_pipeline_processor import LLMPipelineProcessor


@pytest.fixture
def fake_lines():
    return [
        Line(original_text="Texto 1", line_number=0),
        Line(original_text="Texto 2", line_number=1),
    ]

@pytest.fixture
def processor(sample_character):
    llm_client = MagicMock()
    prompt_template = MagicMock()
    character_repo = MagicMock()
    character_repo.upsert.return_value = sample_character

    return LLMPipelineProcessor(
        llm_client=llm_client,
        prompt_template=prompt_template,
        character_repository=character_repo,
        chunk_size=2
    )

def test_process_basic_success(processor, fake_lines, sample_character):
    processor.template.build_messages.return_value = [LLMMessage(role=LLMRole.USER, content="msg")]
    response_text = json.dumps({
        "segments": [
            {
                "segment_index": 0,
                "line_number": 0,
                "text": "Segmento traduzido",
                "translated_text": "Segmento traduzido",
                "segment_type": "narration",
                "speaker": sample_character.name,
                "character_type": sample_character.type.value,
                "gender": sample_character.gender.value
            }
        ]
    })
    processor.llm.chat.return_value = LLMResponse(text=response_text)

    # Act
    segments = processor.process(fake_lines)

    # Assert
    assert len(segments) == 1
    segment = segments[0]
    assert segment.line_number == 0
    assert segment.segment_index == 0
    assert segment.character.name == sample_character.name
    processor.template.build_messages.assert_called_once()
    processor.llm.chat.assert_called_once()


def test_process_with_metadata(processor, fake_lines):
    processor.template.build_messages.return_value = [LLMMessage(role=LLMRole.USER, content="msg")]
    response_text = json.dumps({"segments": []})
    processor.llm.chat.return_value = LLMResponse(text=response_text)

    result = processor.process(fake_lines, metadata={"lang": "pt"})
    assert result == []


def test_process_invalid_json(processor, fake_lines):
    processor.template.build_messages.return_value = [LLMMessage(role=LLMRole.USER, content="msg")]
    processor.llm.chat.return_value = LLMResponse(text="{not a valid json")

    with pytest.raises(json.JSONDecodeError):
        processor.process(fake_lines)


def test_llm_exception_is_raised(processor, fake_lines):
    processor.template.build_messages.return_value = [LLMMessage(role=LLMRole.USER, content="msg")]
    processor.llm.chat.side_effect = RuntimeError("LLM error")

    with pytest.raises(RuntimeError):
        processor.process(fake_lines)
