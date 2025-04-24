from typing import Dict, List, Union

from core.enums import CharacterType, GenderType
from core.models.character import Character


class CharacterRepository:
    """
    Armazena e gerencia personagens únicos por nome.
    Permite buscar, criar ou atualizar personagens conforme forem sendo identificados.
    """

    def __init__(self):
        self._characters: Dict[str, Character] = {}

    def get_or_create(self, name: str) -> Character:
        """
        Retorna o personagem existente com o nome dado ou cria um novo com tipo e gênero unknown.
        """
        key = name.strip().lower()
        if not key:
            raise ValueError("O nome do personagem não pode ser vazio")
        if key not in self._characters:
            self._characters[key] = Character(
                name=name.strip(),
                type=CharacterType.UNKNOWN,
                gender=GenderType.UNKNOWN,
                voice=None
            )
        return self._characters[key]

    def upsert(
        self,
        name: str,
        character_type: Union[CharacterType, str],
        gender: Union[GenderType, str]
    ) -> Character:
        """
        Retorna o Character existente ou novo, e atualiza seu type/gender,
        sempre validando e fazendo fallback para UNKNOWN em caso de valor inválido.
        """
        character = self.get_or_create(name)

        if isinstance(character_type, CharacterType):
            character.type = character_type
        else:
            ct = character_type.strip().lower()
            character.type = CharacterType(ct) if ct in CharacterType._value2member_map_ else CharacterType.UNKNOWN

        if isinstance(gender, GenderType):
            character.gender = gender
        else:
            gd = gender.strip().lower()
            character.gender = GenderType(gd) if gd in GenderType._value2member_map_ else GenderType.UNKNOWN

        return character

    def list(self) -> List[Character]:
        return list(self._characters.values())
    
    def exists(self, name: str) -> bool:
        return bool(name.strip()) and name.strip().lower() in self._characters
