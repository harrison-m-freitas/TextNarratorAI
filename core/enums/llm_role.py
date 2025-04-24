from .base import BaseStrEnum


class LLMRole(BaseStrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"
