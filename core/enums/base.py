from enum import Enum
from typing import Type, TypeVar, List, Optional

T = TypeVar("T", bound="BaseStrEnum")


class BaseStrEnum(str, Enum):
    """
    Enum base com utilitários adicionais para enums string-based.
    Permite conversão segura, listagem de valores e checagem.
    """

    def __str__(self) -> str:
        return self.value

    @classmethod
    def list(cls: Type[T]) -> List[str]:
        """
        Retorna todos os valores possíveis como lista de strings.
        """
        return [e.value for e in cls]

    @classmethod
    def is_valid(cls: Type[T], value: str) -> bool:
        """
        Verifica se o valor é válido para este Enum.
        """
        return value in cls._value2member_map_

    @classmethod
    def safe(cls: Type[T], value: str, default: Optional[T] = None) -> T:
        """
        Retorna o membro correspondente ao valor, ou um valor padrão se inválido.
        Se nenhum valor padrão for passado, retorna o primeiro membro.
        """
        try:
            return cls(value)
        except ValueError:
            return default or list(cls)[0]
