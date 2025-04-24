from abc import ABC, abstractmethod
from typing import Dict, Any, List

from core.models.llm import LLMMessage


class IPromptTemplate(ABC):
    """
    Template genérico para prompts de LLM: encapsula
    a construção de mensagens 'system' e 'user'.
    """

    @abstractmethod
    def build_messages(self, payload: Dict[str, Any]) -> List[LLMMessage]:
        """
        Gera a lista de LLMMessage (system + user + opcionalmente others)
        a partir de um payload específico.
        
        Exemplo de payload para pipeline:
          {"lines": [{"line_number":1,"text":"..."}, ...], "metadata": {...}}
        """
    