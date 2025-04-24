from typing import List, Dict, Any

from core.enums import LLMRole
from core.interfaces.llm import IPromptTemplate
from core.models.llm import LLMMessage


class ScenarioExtractionPrompt(IPromptTemplate):
    """
    Prompt para extrair cenários descritivos de um trecho narrativo traduzido.
    """

    SYSTEM_PROMPT = (
        "Você é um especialista em análise literária e descrição de cenários narrativos.\n\n"
        "Receberá um texto com trechos de narração retirados de um capítulo de uma obra literária.\n"
        "Seu objetivo é identificar e descrever os principais **cenários ou ambientes** que aparecem ao longo do texto.\n\n"
        "**Definição de cenário:**\n"
        "- Um lugar físico ou virtual onde ocorrem eventos.\n"
        "- Pode incluir salas de aula, cidades, ruas, casas, mundos fictícios ou até elementos como o clima e atmosfera.\n\n"
        "**Instruções:**\n"
        "1. Leia atentamente o texto enviado pelo usuário.\n"
        "2. Identifique os locais principais, espaços relevantes e ambientes distintos descritos ao longo do trecho.\n"
        "3. Para cada cenário detectado, forneça:\n"
        "   - Um **nome breve** ou título para o cenário (ex: 'Sala de Aula', 'Sonho de Ye Hong', 'Colégio Zhicai').\n"
        "   - Uma **descrição curta** (2 a 3 frases) com os principais detalhes perceptíveis, estilo, sensação, ou clima do lugar.\n\n"
        "   - (Opcional) Lista de nomes de personagens que aparecem nesse cenário.\n\n"
        "**Formato de retorno esperado:**\n"
        "```json\n"
        "{\n"
        "  \"scenarios\": [\n"
        "    {\n"
        "      \"index\": 0,\n"
        "      \"text\": \"Descrição do cenário...\",\n"
        "      \"location\": \"Nome do lugar (opcional)\",\n"
        "      \"characters\": [\"Ye Hong\", \"Zhang\"]\n"
        "    },\n"
        "    ...\n"
        "  ]\n"
        "}\n"
        "```\n\n"
        "**Observações:**\n"
        "- Não repita descrições idênticas.\n"
        "- Não invente cenários não mencionados ou implícitos no texto.\n"
        "- Foque em passagens narrativas. Ignore falas ou ações de personagens que não adicionem detalhes de espaço ou ambiente."
    )

    def build_messages(self, payload: Dict[str, Any]) -> List[LLMMessage]:
        narration_text = payload.get("narration_text", "")
        return [
            LLMMessage(role=LLMRole.SYSTEM, content=self.SYSTEM_PROMPT),
            LLMMessage(role=LLMRole.USER, content=narration_text)
        ]
