import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class Scenario:
    index: int
    text: str
    location: Optional[str]
    characters: Optional[list[str]] = None
    
    def __post_init__(self):
        logger.debug("Inicializando Scenario(index=%s, location=%s)", self.index, self.location)
        
        if not isinstance(self.index, int) or self.index < 0:
            logger.error("Índice inválido: %s", self.index)
            raise ValueError("O campo 'index' deve ser um inteiro não-negativo.")
        
        if not self.text.strip():
            logger.error("Texto do cenário está vazio.")
            raise ValueError("O campo 'text' não pode estar vazio.")
        
        if self.characters is None:
            self.characters = []
        elif not isinstance(self.characters, list):
            logger.error("Campo 'characters' não é uma lista: %s", type(self.characters))
            raise TypeError("O campo 'characters' deve ser uma lista de strings.")
        elif not all(isinstance(c, str) for c in self.characters):
            logger.error("Lista de 'characters' contém valores não-string: %s", self.characters)
            raise TypeError("Todos os elementos de 'characters' devem ser strings.")
    
    def to_dict(self) -> dict:
        data = {
            "index": self.index,
            "text": self.text,
            "location": self.location,
            "characters": self.characters or [],
        }
        logger.debug("Serializando Scenario para dict: %s", data)
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Scenario":
        logger.debug("Criando Scenario a partir de dict: %s", data)
        return cls(
            index=data["index"],
            text=data["text"],
            location=data.get("location"),
            characters=data.get("characters", []),
        )
