import logging
from dataclasses import dataclass
from typing import Dict, Any, Optional

from core.enums import LLMRole

logger = logging.getLogger(__name__)


@dataclass
class LLMMessage:
    role: LLMRole
    content: str
    name: Optional[str] = None
    
    def __post_init__(self):
        logger.debug("Inicializando LLMMessage com role=%s", self.role)
        if not isinstance(self.role, LLMRole):
            logger.error("Role inválido: %s", self.role)
            raise ValueError(f"Role inválido: {self.role}")
        if not self.content.strip():
            logger.error("Conteúdo da mensagem LLM está vazio.")
            raise ValueError("O conteúdo da mensagem não pode estar vazio")
    
    def to_dict(self) -> Dict[str, Any]:
        data = {
            "role": self.role,
            "content": self.content
        }
        if self.name:
            data["name"] = self.name
        logger.debug("Serializando LLMMessage: %s", data)
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LLMMessage":
        logger.debug("Criando LLMMessage a partir de dict: %s", data)
        return cls(
            role=LLMRole.safe(data["role"]),
            content=data["content"],
            name=data.get("name")
        )

@dataclass
class LLMUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

    def __post_init__(self):
        logger.debug(
            "LLMUsage: prompt=%d, completion=%d, total=%d",
            self.prompt_tokens, self.completion_tokens, self.total_tokens
        )
        if self.prompt_tokens < 0 or self.completion_tokens < 0 or self.total_tokens < 0:
            logger.error("Tokens negativos: %s", self)
            raise ValueError("Tokens não podem ser negativos")
        if self.total_tokens != self.prompt_tokens + self.completion_tokens:
            logger.error("Total de tokens inconsistente: %s", self)
            raise ValueError("total_tokens deve ser igual à soma de prompt_tokens e completion_tokens")
    
    def to_dict(self) -> Dict[str, Any]:
        data = {
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens
        }
        logger.debug("Serializando LLMUsage: %s", data)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LLMUsage":
        logger.debug("Criando LLMUsage a partir de dict: %s", data)
        return cls(
            prompt_tokens=data["prompt_tokens"],
            completion_tokens=data["completion_tokens"],
            total_tokens=data["total_tokens"]
        )

@dataclass
class LLMResponse:
    text: str
    usage: Optional[LLMMessage] = None
    raw: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        logger.debug("Inicializando LLMResponse com texto: %s...", self.text[:60])
        if not self.text.strip():
            logger.error("Resposta LLM vazia.")
            raise ValueError("A resposta não pode estar vazia")
        if self.usage and not isinstance(self.usage, LLMUsage):
            logger.error("Campo 'usage' inválido: %s", type(self.usage))
            raise TypeError("usage deve ser uma instância de LLMUsage ou None")
        if self.raw and not isinstance(self.raw, dict):
            logger.error("Campo 'raw' inválido: %s", type(self.raw))
            raise TypeError("raw deve ser um dicionário ou None")
    
    def to_dict(self) -> Dict[str, Any]:
        data = {
            "text": self.text,
            "usage": self.usage.to_dict() if self.usage else None,
            "raw": self.raw
        }
        logger.debug("Serializando LLMResponse: %s", data)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LLMResponse":
        logger.debug("Criando LLMResponse a partir de dict.")
        return cls(
            text=data["text"],
            usage=LLMUsage.from_dict(data["usage"]) if data.get("usage") else None,
            raw=data.get("raw")
        )