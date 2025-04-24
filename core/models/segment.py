import logging
from dataclasses import dataclass
from typing import Optional, Dict, Any

from core.enums import SegmentType, EmotionType
from core.models.character import Character

logger = logging.getLogger(__name__)


@dataclass
class Segment:
    segment_index: int
    line_number: int
    text: str
    translated_text: Optional[str] = None
    segment_type: SegmentType = SegmentType.NARRATION
    speaker_hint: Optional[str] = None
    character: Optional[Character] = None
    emotion: Optional[EmotionType] = None
    
    def __post_init__(self):
        logger.debug("Inicializando Segment: linha=%s índice=%s tipo=%s", self.line_number, self.segment_index, self.segment_type)
        
        if not isinstance(self.segment_index, int) or self.segment_index < 0:
            logger.error("segment_index inválido: %s", self.segment_index)
            raise ValueError("segment_index deve ser um inteiro não-negativo")

        if not isinstance(self.line_number, int) or self.line_number < 0:
            logger.error("line_number inválido: %s", self.line_number)
            raise ValueError("line_number deve ser um inteiro não-negativo")

        if not self.text.strip():
            logger.error("Texto do segmento está vazio.")
            raise ValueError("O campo 'text' não pode estar vazio")
        
        if not isinstance(self.segment_type, SegmentType):
            logger.error("Tipo de segmento inválido: %s", self.segment_type)
            raise TypeError(f"'segment_type' deve ser uma instância de SegmentType, recebido: {type(self.segment_type)}")
        
        if self.emotion and not isinstance(self.emotion, EmotionType):
            raise TypeError(f"'emotion' deve ser uma instância de EmotionType ou None, recebido: {type(self.emotion)}")
        
        if self.character and not isinstance(self.character, Character):
            raise TypeError(f"'character' deve ser uma instância de Character ou None, recebido: {type(self.character)}")
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Segment":
        """
        Factory que cria um Segment a partir de um dict vindo da LLM.
        Espera as chaves:
          - segment_index (int)
          - line_number (int)
          - original_text (str)
          - translated_text (str)
          - segment_type (str: one of SegmentType)
          - speaker (str)
          - emotion (str)
        """
        logger.debug("Criando Segment a partir de dict: %s", data)
        original_text = data.get("text", data.get("original_text", ""))
        return cls(
            segment_index=data["segment_index"],
            line_number=data["line_number"],
            text=original_text,
            translated_text=data["translated_text"],
            segment_type=SegmentType.safe(data["segment_type"]),
            speaker_hint=data.get("speaker", "Narrador"),
            emotion=EmotionType.safe(data.get("emotion")),
            character=Character.from_dict(data.get("character")) if data.get("character") else None
        )

    def to_dict(self) -> dict:
        data = {
            "segment_index": self.segment_index,
            "line_number": self.line_number,
            "text": self.text,
            "translated_text": self.translated_text,
            "segment_type": self.segment_type.value,
            "speaker_hint": self.speaker_hint,
            "character": self.character.to_dict() if self.character else None,
            "emotion": self.emotion.value,
        }
        logger.debug("Serializando Segment para dict: %s", data)
        return data
