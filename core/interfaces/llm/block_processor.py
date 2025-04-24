from abc import ABC, abstractmethod
from typing import List, Dict, Any

from core.models.line import Line
from core.models.segment import Segment


class IBlockProcessor(ABC):
    """
    Interface para processar blocos de Linhas 
    em Segments completos (traduzidos, segmentados, classificados e com emoção).
    """

    @abstractmethod
    def process(
        self,
        lines: List[Line],
        *,
        chunk_size: int = None,
        metadata: Dict[str, Any] = None
    ) -> List[Segment]:
        """
        - lines: lista de Line (com line_number e original_text).  
        - chunk_size: quantas lines enviar por requisição (fallback interno se None).  
        - metadata: dados adicionais a injetar no prompt (ex: work_id, chapter_id).  
        Retorna lista de Segment completos.
        """
