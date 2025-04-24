from abc import ABC, abstractmethod
from typing import Dict, Any


class IManifestAdapter(ABC):
    """
    Interface para ler e gravar o manifest de capítulos processados
    de uma obra, contendo checksums ou versões.
    """

    @abstractmethod
    def load(self, work_id: str) -> Dict[str, Any]:
        """
        Retorna um dict com ao menos a chave 'chapters',
        mapeando chapter_id → checksum (ou metadata).
        Se não existir, retorna {'chapters': {}}.
        """

    @abstractmethod
    def save(self, work_id: str, manifest: Dict[str, Any]) -> None:
        """
        Persiste o manifest para a obra.
        """
