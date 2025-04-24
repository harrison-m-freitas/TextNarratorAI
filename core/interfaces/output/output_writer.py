from abc import ABC, abstractmethod
from typing import Sequence

from core.models.chapter import Chapter
from core.models.audio_segment import ChapterAudio


class IOutputWriter(ABC):
    """
    Responsável por salvar em disco os resultados do processamento:
    texto organizado, áudios e cenários.
    """

    @abstractmethod
    def save(
        self,
        chapter: Chapter,
        audio: ChapterAudio,
        scenarios: Sequence[str]
    ) -> None:
        """
        Salva em `data/output/`:
        - arquivo JSON ou TXT com capítulo traduzido/classificado
        - arquivos de áudio gerados
        - arquivo de cenários
        """
