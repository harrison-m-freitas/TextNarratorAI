import os
import pytest

from core.enums import SegmentType
from core.models.line import Line
from core.models.segment import Segment
from core.repositories.character_repository import CharacterRepository

from adapters.llm.openai_client import OpenAIClient
from adapters.prompts.pipeline_prompt import PipelinePrompt
from adapters.analyzer.llm_pipeline_processor import LLMPipelineProcessor


@pytest.mark.integration
def test_llm_pipeline_processor_integration_with_openai():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY não está definido.")

    line = Line(
        line_number=0,
        original_text="He walked slowly through the silent forest.",
        translated_text="",
        segments=[]
    )

    client = OpenAIClient(api_key=api_key, model="gpt-3.5-turbo")
    prompt = PipelinePrompt()
    repository = CharacterRepository()

    processor = LLMPipelineProcessor(
        llm_client=client,
        prompt_template=prompt,
        character_repository=repository,
        chunk_size=1,
        temperature=0.0,
        max_tokens=200,
    )

    segments = processor.process([line])

    assert isinstance(segments, list)
    assert len(segments) > 0

    for seg in segments:
        assert isinstance(seg, Segment)
        assert seg.line_number == line.line_number
        assert seg.segment_type in SegmentType
        assert seg.text.strip()
        assert seg.character is not None
        assert seg.character.name.strip()
