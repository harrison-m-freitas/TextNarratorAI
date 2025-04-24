from abc import ABC, abstractmethod
from typing import List

from core.models.line import Line


class ITextLoader(ABC):
    """
    Responsável por ler um arquivo .txt e produzir uma lista de Line.
    """

    @abstractmethod
    def load(self, file_path: str) -> List[Line]:
        """
        Carrega o arquivo em `file_path` e retorna uma lista de Lines
        com `original_text` e `line_number` preenchidos.
        """
