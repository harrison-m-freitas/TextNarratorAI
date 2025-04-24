from .base import BaseStrEnum

class CharacterType(BaseStrEnum):
    UNKNOWN = "unknown"
    NARRATOR = "narrator"
    PROTAGONIST = "protagonist"
    SUPPORTING_MALE = "supporting_male"
    SUPPORTING_FEMALE = "supporting_female"
    SYSTEM = "system"
