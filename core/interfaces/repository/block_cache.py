from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class IBlockCache(ABC):
    """
    Interface para cache de respostas de blocos de LLM,
    de modo que não seja necessário reprocessar o mesmo chunk.
    """

    @abstractmethod
    def load_block(
        self,
        work_id: str,
        chapter_id: str,
        block_index: int
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Retorna a lista de dicts (raw segments) para o bloco
        se existir no cache, ou None caso contrário.
        """

    @abstractmethod
    def save_block(
        self,
        work_id: str,
        chapter_id: str,
        block_index: int,
        data: List[Dict[str, Any]]
    ) -> None:
        """
        Persiste a lista de dicts (raw segments) no cache.
        """
