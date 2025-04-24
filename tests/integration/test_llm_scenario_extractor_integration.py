import os
import pytest

from core.models.chapter import Chapter
from core.models.line import Line
from core.models.segment import Segment
from core.enums import SegmentType

from adapters.extractor.llm_scenario_extractor import LLMScenarioExtractor
from adapters.llm.openai_client import OpenAIClient
from adapters.prompts.scenario_extraction_prompt import ScenarioExtractionPrompt


@pytest.mark.integration
def test_llm_scenario_extractor_with_openai():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY não está definido.")

    segment = Segment(
        segment_index=0,
        line_number=0,
        text="O céu estava escuro e nuvens cobriam toda a cidade.",
        translated_text="The sky was dark and clouds covered the entire city.",
        segment_type=SegmentType.NARRATION
    )
    line = Line(original_text="...", translated_text=segment.translated_text, segments=[segment], line_number=0)
    chapter = Chapter(id="c1", work_id="w1", title="Capítulo 1", lines=[line])

    client = OpenAIClient(api_key=api_key, model="gpt-3.5-turbo")
    prompt = ScenarioExtractionPrompt()

    extractor = LLMScenarioExtractor(llm_client=client, prompt_template=prompt)

    scenarios = extractor.extract(chapter)

    assert isinstance(scenarios, list)
    assert len(scenarios) >= 1
    assert all(s.index >= 0 for s in scenarios)
    assert all(isinstance(s.text, str) and s.text for s in scenarios)
    
    
