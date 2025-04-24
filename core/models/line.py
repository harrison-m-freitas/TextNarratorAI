import logging
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

from core.models.segment import Segment

logger = logging.getLogger(__name__)


@dataclass
class Line:
    original_text: str
    translated_text: Optional[str] = None
    segments: List[Segment] = field(default_factory=list)
    line_number: int = field(default=-1)
    
    def __post_init__(self):
        logger.debug("Inicializando Line: #%d - \"%s...\"", self.line_number, self.original_text[:50])

        if not self.original_text.strip():
            logger.error("O campo 'original_text' está vazio.")
            raise ValueError("O campo 'original_text' não pode estar vazio.")

        if not isinstance(self.segments, list):
            logger.error("Campo 'segments' deve ser uma lista, mas recebeu %s", type(self.segments))
            raise TypeError("O campo 'segments' deve ser uma lista.")

        for seg in self.segments:
            if not isinstance(seg, Segment):
                logger.error("Item inválido em 'segments': %s", type(seg))
                raise TypeError("Todos os itens de 'segments' devem ser instâncias de Segment.")

        if not isinstance(self.line_number, int) or self.line_number < -1:
            logger.error("Valor inválido para 'line_number': %s", self.line_number)
            raise ValueError("O campo 'line_number' deve ser um inteiro maior ou igual a -1.")

    
    def to_dict(self) -> dict:
        data = {
            "original_text": self.original_text,
            "translated_text": self.translated_text,
            "segments": [seg.to_dict() for seg in self.segments],
            "line_number": self.line_number
        }
        logger.debug("Serializando Line #%d para dict", self.line_number)
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Line":
        logger.debug("Criando Line a partir de dict: line_number=%s", data.get("line_number", -1))
        return cls(
            original_text=data["original_text"],
            translated_text=data.get("translated_text"),
            segments=[Segment.from_dict(s) for s in data.get("segments", [])],
            line_number=data.get("line_number", -1)
        )
