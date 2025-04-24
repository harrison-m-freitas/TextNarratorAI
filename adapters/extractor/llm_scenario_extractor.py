import json
import logging
from typing import List

from core.enums import SegmentType
from core.interfaces.extraction import IScenarioExtractor
from core.interfaces.llm import IPromptTemplate, ILLMClient
from core.models.chapter import Chapter
from core.models.scenario import Scenario

logger = logging.getLogger(__name__)


class LLMScenarioExtractor(IScenarioExtractor):
    """
    Usa uma única chamada à LLM para extrair os principais cenários
    de um capítulo, baseando-se nos segmentos de narração.
    """

    def __init__(self, llm_client: ILLMClient, prompt_template: IPromptTemplate):
        self.client = llm_client
        self.prompt = prompt_template

    def extract(self, chapter: Chapter) -> List[Scenario]:
        narration_text = "\n".join(
            seg.translated_text
            for line in chapter.lines
            for seg in line.segments
            if seg.segment_type == SegmentType.NARRATION
        ).strip()
        
        if not narration_text:
            logger.warning("Nenhum segmento de narração encontrado no capítulo '%s'.", chapter.id)
            return []

        logger.info("Extraindo cenários do capítulo '%s'...", chapter.id)
        messages = self.prompt.build_messages({"narration_text": narration_text})
        
        try:
            response = self.client.chat(messages)
            logger.debug("Resposta bruta da LLM: %s", response.text[:200] + "..." if len(response.text) > 200 else response.text)
        except Exception:
            logger.exception("Erro ao consultar a LLM para extração de cenários")
            raise

        try:
            data = json.loads(response.text)
            scenarios_data = data.get("scenarios", [])
            if not isinstance(scenarios_data, list):
                raise ValueError("Esperava 'scenarios' como lista")

            logger.info("Foram extraídos %d cenários", len(scenarios_data))
            return [Scenario.from_dict(sc) for sc in scenarios_data]
        except (json.JSONDecodeError, ValueError):
            logger.exception("Erro ao interpretar resposta da LLM na extração de cenários")
            raise
