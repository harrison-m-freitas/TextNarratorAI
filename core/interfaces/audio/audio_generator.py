from abc import ABC, abstractmethod

from core.models.chapter import Chapter
from core.models.audio_segment import ChapterAudio


class IAudioGenerator(ABC):
    """
    Responsável por gerar arquivos de áudio a partir de um Chapter.
    """

    @abstractmethod
    def generate(self, chapter: Chapter) -> ChapterAudio:
        """
        Gera um ChapterAudio contendo AudioSegments para cada Line
        e retorna esse ChapterAudio.
        """
