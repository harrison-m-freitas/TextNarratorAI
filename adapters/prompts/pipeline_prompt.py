import json
from typing import List, Dict, Any

from core.enums import LLMRole
from core.interfaces.llm import IPromptTemplate
from core.models.llm import LLMMessage


class PipelinePrompt(IPromptTemplate):
    """
    Prompt para o pipeline completo: tradução, segmentação,
    classificação de personagens e detecção de emoções.
    """
    
    SYSTEM_PROMPT = (
        "Você é um assistente especializado em análise literária, tradução, segmentação de texto, "
        "classificação de personagens e detecção de emoções.\n\n"
        "Você receberá um bloco com múltiplas linhas de uma obra literária."
        "Cada linha tem um número e um texto original (em outro idioma).\n\n"
        "Para **cada linha**, realize exatamente os seguintes passos:\n\n"
        "**1. Tradução:**\n"
        "- Traduza integralmente o texto para Português Brasileiro, mantendo o estilo original, "
        "naturalidade nas falas e coerência textual.\n\n"
        "**2. Segmentação:**\n"
        "- Separe claramente cada linha traduzida em segmentos distintos. Cada segmento deve ser classificado como:\n"
        "  - narration: texto descritivo ou narração das ações e eventos\n"
        "  - dialogue: falas normais dos personagens\n"
        "  - highlight: falas enfáticas (exclamações, interjeições, surpresas, ações dramáticas)\n\n"
        "**3. Classificação dos Personagens:**\n"
        "- Para cada segmento de diálogo ou destaque, identifique claramente quem está falando.\n"
        "- Para narração, use \"Narrador\". Para falas automáticas, use \"Sistema\".\n"
        "- character_type: narrator | protagonist | supporting_male | supporting_female | system | unknown\n"
        "- gender: male | female | unknown\n\n"
        "**4. Detecção de Emoção:**\n"
        "- Para cada segmento, identifique uma emoção predominante entre:\n"
        "  neutral | joy | anger | surprise | hesitation | shout\n\n"
        "**Retorno:**\n"
        "Retorne **um único JSON válido** com uma lista chamada 'segments'.\n\n"
        "**Formato esperado:**\n"
        "{\n"
        "  \"segments\": [\n"
        "    {\n"
        "      \"line_number\": int,\n"
        "      \"segment_index\": int,\n"
        "      \"original_text\": str,\n"
        "      \"translated_text\": str,\n"
        "      \"segment_type\": \"narration|dialogue|highlight\",\n"
        "      \"speaker\": str,\n"
        "      \"character_type\": \"narrator|protagonist|supporting_male|supporting_female|system|unknown\",\n"
        "      \"gender\": \"male|female|unknown\",\n"
        "      \"emotion\": \"neutral|joy|anger|surprise|hesitation|shout\"\n"
        "    },\n"
        "    ...\n"
        "  ]\n"
        "}\n\n"
        "**Observações:**\n"
        "- Preserve a ordem original das linhas e segmentos.\n"
        "- Nunca deixe campos vazios ou nulos. Preencha todos os valores com uma das opções listadas."
    )

    def build_messages(self, payload: Dict[str, Any]) -> List[LLMMessage]:
        return [
            LLMMessage(role=LLMRole.SYSTEM, content=self.SYSTEM_PROMPT),
            LLMMessage(role=LLMRole.USER, content=json.dumps(payload, ensure_ascii=False))
        ]
