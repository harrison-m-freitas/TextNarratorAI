import logging
from dataclasses import dataclass
from typing import Optional

from core.enums import CharacterType, GenderType
from core.models.voice_profile import VoiceProfile

logger = logging.getLogger(__name__)


@dataclass
class Character:
    name: str
    type: CharacterType
    gender: GenderType = GenderType.UNKNOWN
    voice: Optional[VoiceProfile] = None
    
    def __post_init__(self):
        logger.debug("Inicializando Character: name=%s, type=%s, gender=%s", self.name, self.type, self.gender)

        if not self.name.strip():
            logger.error("Nome do personagem está vazio.")
            raise ValueError("O campo 'name' do personagem não pode estar vazio.")

        if not isinstance(self.type, CharacterType):
            logger.error("Tipo de personagem inválido: %s", type(self.type))
            raise TypeError(f"O campo 'type' deve ser CharacterType, recebido: {type(self.type)}")

        if not isinstance(self.gender, GenderType):
            logger.error("Gênero inválido: %s", type(self.gender))
            raise TypeError(f"O campo 'gender' deve ser GenderType, recebido: {type(self.gender)}")

        if self.voice and not isinstance(self.voice, VoiceProfile):
            logger.error("VoiceProfile inválido: %s", type(self.voice))
            raise TypeError(f"O campo 'voice' deve ser VoiceProfile ou None, recebido: {type(self.voice)}")


    def assign_voice(self, profile: VoiceProfile):
        if (profile.gender != self.gender and profile.gender != GenderType.UNKNOWN) or not isinstance(profile, VoiceProfile):
            logger.error("Gênero da voz (%s) não corresponde ao personagem (%s)", profile.gender, self.gender)
            raise ValueError("Gênero da voice_profile não coincide com o do personagem")
        logger.debug("Atribuindo voz ao personagem '%s': voice_id=%s", self.name, profile.id)
        self.voice = profile
        
    def to_dict(self) -> dict:
        data = {
            "name": self.name,
            "type": self.type.value,
            "gender": self.gender.value,
            "voice": self.voice.to_dict() if self.voice else None,
        }
        logger.debug("Serializando Character '%s' para dict.", self.name)
        return data
        
    @classmethod
    def from_dict(cls, data: dict) -> "Character":
        logger.debug("Criando Character a partir de dict: %s", data.get("name", "[sem nome]"))
        return cls(
            name=data["name"],
            type=CharacterType.safe(data["type"]),
            gender=GenderType.safe(data["gender"]),
            voice=VoiceProfile.from_dict(data["voice"]) if data.get("voice") else None
        )
