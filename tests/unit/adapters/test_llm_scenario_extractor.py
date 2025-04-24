import pytest
import json
from unittest.mock import Mock

from core.enums import SegmentType
from core.models.segment import Segment
from core.models.line import Line
from core.models.chapter import Chapter
from core.models.llm import LLMResponse
from core.models.scenario import Scenario
from adapters.extractor.llm_scenario_extractor import LLMScenarioExtractor


@pytest.fixture
def mock_prompt_template():
    template = Mock()
    template.build_messages.return_value = ["mock_message"]
    return template


@pytest.fixture
def mock_llm_client():
    client = Mock()
    client.chat.return_value = LLMResponse(
        text='''
        {
            "scenarios": [
                {
                    "index": 0,
                    "text": "Uma sala escura com cortinas vermelhas.",
                    "location": "Sala de Treinamento",
                    "characters": ["Ye Hong"]
                }
            ]
        }
        ''',
        usage=None,
        raw=None
    )
    return client

@pytest.fixture
def dummy_chapter_with_narration():
    segment = Segment(
        segment_index=0,
        line_number=0,
        text="Texto original",
        translated_text="Descrição do lugar.",
        segment_type=SegmentType.NARRATION
    )
    line = Line(original_text="Linha original", segments=[segment])
    return Chapter(id="ch1", work_id="w1", title="Capítulo 1", lines=[line])


def test_extract_scenarios_success(mock_llm_client, mock_prompt_template, dummy_chapter_with_narration):
    chapter = dummy_chapter_with_narration
    extractor = LLMScenarioExtractor(llm_client=mock_llm_client, prompt_template=mock_prompt_template)
    scenarios = extractor.extract(chapter)
    assert len(scenarios) == 1
    assert isinstance(scenarios[0], Scenario)
    assert scenarios[0].location == "Sala de Treinamento"
    assert scenarios[0].characters == ["Ye Hong"]

def test_extract_scenarios_empty_when_no_narration(mock_llm_client, mock_prompt_template):
    line = Line(original_text="Sem narração", segments=[])
    chapter = Chapter(id="ch1", work_id="w1", title="Capítulo 1", lines=[line])

    extractor = LLMScenarioExtractor(llm_client=mock_llm_client, prompt_template=mock_prompt_template)
    scenarios = extractor.extract(chapter)

    assert scenarios == []
    mock_llm_client.chat.assert_not_called()


def test_extract_scenarios_invalid_json(mock_prompt_template):
    mock_llm = Mock()
    mock_llm.chat.return_value = LLMResponse(
        text="resposta inválida sem json",
        usage=None,
        raw=None
    )

    segment = Segment(
        segment_index=0,
        line_number=0,
        text="Texto original",
        translated_text="Texto traduzido.",
        segment_type=SegmentType.NARRATION
    )
    line = Line(original_text="Linha", segments=[segment])
    chapter = Chapter(id="ch1", work_id="w1", title="Capítulo 1", lines=[line])

    extractor = LLMScenarioExtractor(llm_client=mock_llm, prompt_template=mock_prompt_template)

    with pytest.raises(Exception):
        extractor.extract(chapter)

def test_llm_chat_raises_exception(dummy_chapter_with_narration):
    mock_llm = Mock()
    mock_llm.chat.side_effect = RuntimeError("Falha simulada na LLM")
    mock_prompt = Mock()
    mock_prompt.build_messages.return_value = ["mensagem simulada"]

    extractor = LLMScenarioExtractor(llm_client=mock_llm, prompt_template=mock_prompt)

    with pytest.raises(RuntimeError, match="Falha simulada na LLM"):
        extractor.extract(dummy_chapter_with_narration)


def test_scenarios_data_not_a_list(dummy_chapter_with_narration):
    mock_llm = Mock()
    mock_llm.chat.return_value = LLMResponse(
        text=json.dumps({"scenarios": "isto_nao_e_uma_lista"}),
        usage=None,
        raw=None
    )
    mock_prompt = Mock()
    mock_prompt.build_messages.return_value = ["mensagem simulada"]

    extractor = LLMScenarioExtractor(llm_client=mock_llm, prompt_template=mock_prompt)

    with pytest.raises(ValueError, match="Esperava 'scenarios' como lista"):
        extractor.extract(dummy_chapter_with_narration)
