import os
import logging
from typing import List, Optional
from openai import OpenAI, OpenAIError

from core.interfaces.llm import ILLMClient
from core.models.llm import LLMMessage, LLMResponse, LLMUsage

logger = logging.getLogger(__name__)


class OpenAIClient(ILLMClient):
    """
    Implementação de ILLMClient usando OpenAI.
    """
    
    def __init__(
        self,
        api_key: str = None,
        model: str = "gpt-4o",
        timeout: Optional[int] = None
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key, timeout=timeout)
        self.model = model
        logger.info("OpenAIClient inicializando com modelo '%s'", self.model)
        
    def chat(
        self,
        messages: List[LLMMessage],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0
    ) -> LLMResponse:
        payload = [msg.to_dict() for msg in messages]
        logger.debug("Enviando %d mensagens para o modelo '%s'", len(payload), self.model)
        
        try: 
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=payload,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty
            )
            logger.debug("Resposta da OpenAI recebida com sucesso.")
        except OpenAIError as e:
            logger.exception("Erro durante requisição à OpenAI")
            raise RuntimeError(f"[OpenAIClient.chat] Error: {e}")
        
        choice = resp.choices[0].message
        usage = None
        if hasattr(resp, "usage"):
            usage = LLMUsage(
                prompt_tokens=resp.usage.prompt_tokens,
                completion_tokens=resp.usage.completion_tokens,
                total_tokens=resp.usage.total_tokens
            )
            logger.info("Uso de tokens - Prompt: %d, Completion: %d, Total: %d",
                        usage.prompt_tokens, usage.completion_tokens, usage.total_tokens)
    
        return LLMResponse(
            text=choice.content.strip(),
            usage=usage,
            raw=resp.to_dict()
        )
