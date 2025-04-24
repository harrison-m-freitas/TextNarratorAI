from abc import ABC, abstractmethod
from typing import List, Dict

from core.models.chapter import Chapter
from core.models.scenario import Scenario


class IScenarioExtractor(ABC):
    """
    Responsável por extrair descrições de cenários de um Chapter.
    """

    @abstractmethod
    def extract(self, chapter: Chapter) -> List[Scenario]:
        """
        Recebe um Chapter completo e retorna uma lista de descrições
        dos cenários principais.
        """
