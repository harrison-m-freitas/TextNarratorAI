import json
import logging
from typing import List, Dict, Any, Optional

from core.interfaces.llm import IBlockProcessor, IPromptTemplate, ILLMClient
from core.models.line import Line
from core.models.llm import LLMMessage, LLMResponse
from core.models.segment import Segment
from core.repositories.character_repository import CharacterRepository

logger = logging.getLogger(__name__)


class LLMPipelineProcessor(IBlockProcessor):
    """
    Processa blocos de Line em Segment usando uma LLM por meio de:
      - IPromptTemplate: constrói as mensagens
      - ILLMClient: executa a chamada à LLM
    """
    
    def __init__(
        self,
        llm_client: ILLMClient,
        prompt_template: IPromptTemplate,
        character_repository: CharacterRepository,
        *, 
        chunk_size: int = 10,
        temperature: float = 0.3,
        max_tokens: Optional[int] = None,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0
    ):
        self.llm = llm_client
        self.template = prompt_template
        self.char_repo = character_repository
        self.chunk_size = chunk_size
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        
    def process(
        self,
        lines: List[Line],
        *,
        chunk_size: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Segment]:
        logger.info(
            "Iniciando processamento de %d linhas com chunk_size=%d", 
            len(lines), chunk_size or self.chunk_size
        )
        size = chunk_size or self.chunk_size
        all_segments: List[Segment] = []
        
        for i in range(0, len(lines), size):
            block = lines[i : i + size]
            logger.debug("Processando bloco de linhas %d até %d", i, i + size)
            
            payload: Dict[str, Any] = {
                "lines": [
                    {"line_number": ln.line_number, "text": ln.original_text}
                    for ln in block
                ]
            }
            if metadata:
                payload["metadata"] = metadata
                
            messages: List[LLMMessage] = self.template.build_messages(payload)
            logger.debug("Mensagens construídas: %s", messages)
            
            try:
                response: LLMResponse = self.llm.chat(
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    top_p=self.top_p,
                    frequency_penalty=self.frequency_penalty,
                    presence_penalty=self.presence_penalty
                )
                logger.debug("Resposta recebida da LLM: %s", response.text[:1000] + "..." if len(response.text) > 1000 else response.text)
            except Exception as e:
                logger.exception("Erro ao chamar a LLM: %s", str(e))
                raise
        
            try:
                data = json.loads(response.text)
                segments_data = data.get("segments", [])
                logger.info("Foram retornados %d segmentos pela LLM", len(segments_data))
            except json.JSONDecodeError as e:
                logger.exception("Erro ao fazer o parse do JSON retornado pela LLM: %s", str(e))
                raise
            
            for obj in segments_data:
                seg = Segment.from_dict(obj)
                
                character = self.char_repo.upsert(
                    name=obj.get("speaker", "Narrador"),
                    character_type=obj.get("character_type", "unknown"),
                    gender=obj.get("gender", "unknown")
                )

                logger.debug("Personagem processado: %s (%s, %s)", character.name, character.type, character.gender)
                seg.character = character
                all_segments.append(seg)
            
        all_segments.sort(key=lambda s: (s.line_number, s.segment_index))
        logger.info("Processamento finalizado. Total de segmentos: %d", len(all_segments))
        return all_segments
