import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any

from core.enums import GenderType

logger = logging.getLogger(__name__)


@dataclass
class VoiceProfile:
    id: str
    name: str
    vendor: str
    language: str
    gender: GenderType
    
    def __post_init__(self):
        logger.debug("Inicializando VoiceProfile: %s (%s)", self.name, self.gender)
        
        if not self.id.strip():
            logger.error("ID do perfil de voz está vazio")
            raise ValueError("O campo 'id' não pode estar vazio.")
        if not self.name.strip():
            logger.error("Nome do perfil de voz está vazio")
            raise ValueError("O campo 'name' não pode estar vazio.")
        if not self.vendor.strip():
            logger.error("Vendor do perfil de voz está vazio")
            raise ValueError("O campo 'vendor' não pode estar vazio.")
        if not self.language.strip():
            logger.error("Idioma do perfil de voz está vazio")
            raise ValueError("O campo 'language' não pode estar vazio.")
        if not isinstance(self.gender, GenderType):
            logger.error("Gênero inválido: %s", self.gender)
            raise TypeError(f"'gender' deve ser uma instância de GenderType, recebido: {type(self.gender)}")
        
    def to_dict(self) -> Dict[str, Any]:
        data = {
            "id": self.id,
            "name": self.name,
            "vendor": self.vendor,
            "language": self.language,
            "gender": self.gender.value
        }
        logger.debug("Serializando VoiceProfile para dict: %s", data)
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "VoiceProfile":
        logger.debug("Criando VoiceProfile a partir de dict: %s", data)
        return cls(
            id=data["id"],
            name=data["name"],
            gender=GenderType.safe(data["gender"]),
            language=data["language"],
            vendor=data["vendor"]
        )
