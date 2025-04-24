from abc import ABC, abstractmethod
from typing import List, Optional

from core.models.llm import LLMMessage, LLMResponse


class ILLMClient(ABC):
    """
    Interface genérica para comunicação via chat com qualquer LLM.
    """

    @abstractmethod
    def chat(
        self, 
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0
    ) -> LLMResponse:
        """
        Envia uma lista de mensagens e retorna um LLMResponse contendo
        o texto da resposta, uso de tokens e o payload bruto.
        """
