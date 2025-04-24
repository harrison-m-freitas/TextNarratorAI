import logging
from dataclasses import dataclass, field
from typing import List

from core.models.line import Line
from core.models.scenario import Scenario

logger = logging.getLogger(__name__)


@dataclass
class Chapter:
    """
    Cada instância representa um capítulo pertencente a uma obra.
    """
    id: str
    work_id: str                    
    title: str
    lines: List[Line] = field(default_factory=list)
    scenarios: List[Scenario] = field(default_factory=list)
       
    def __post_init__(self):
        logger.debug("Inicializando Chapter: id=%s, title=%s", self.id, self.title)

        if not self.id.strip():
            logger.error("ID do capítulo está vazio.")
            raise ValueError("O campo 'id' do capítulo não pode estar vazio.")

        if not self.work_id.strip():
            logger.error("work_id do capítulo está vazio.")
            raise ValueError("O campo 'work_id' do capítulo não pode estar vazio.")

        if not self.title.strip():
            logger.error("Título do capítulo está vazio.")
            raise ValueError("O campo 'title' do capítulo não pode estar vazio.")

        if not isinstance(self.lines, list):
            logger.error("O campo 'lines' deve ser uma lista, recebido: %s", type(self.lines))
            raise TypeError("'lines' deve ser uma lista de instâncias de Line.")

        if not isinstance(self.scenarios, list):
            logger.error("O campo 'scenarios' deve ser uma lista, recebido: %s", type(self.scenarios))
            raise TypeError("'scenarios' deve ser uma lista de instâncias de Scenario.")

        for line in self.lines:
            if not isinstance(line, Line):
                logger.error("Item inválido em 'lines': %s", type(line))
                raise TypeError("Todos os itens de 'lines' devem ser instâncias de Line.")

        for scenario in self.scenarios:
            if not isinstance(scenario, Scenario):
                logger.error("Item inválido em 'scenarios': %s", type(scenario))
                raise TypeError("Todos os itens de 'scenarios' devem ser instâncias de Scenario.")

    def add_line(self, line: Line):
        if not isinstance(line, Line):
            logger.error("Tentando adicionar linha inválida: %s", type(line))
            raise TypeError("line deve ser uma instância de Line")
        logger.debug("Adicionando linha ao capítulo %s: %s", self.id, line.original_text[:30])
        self.lines.append(line)

    def add_scenario(self, scenario: Scenario):
        logger.debug("Adicionando cenário ao capítulo %s", self.id)
        if not isinstance(scenario, Scenario):
            logger.error("Tentando adicionar cenário inválido: %s", type(scenario))
            raise TypeError("scenario deve ser uma instância de Scenario")
        self.scenarios.append(scenario)

    def to_dict(self) -> dict:
        data = {
            "id": self.id,
            "work_id": self.work_id,
            "title": self.title,
            "lines": [ln.to_dict() for ln in self.lines],
            "scenarios": [sc.to_dict() for sc in self.scenarios],
        }
        logger.debug("Serializando Chapter '%s' para dict", self.id)
        return data
        
    @classmethod
    def from_dict(cls, data) -> "Chapter":
        logger.debug("Criando Chapter a partir de dict: %s", data.get("id", "[sem id]"))
        return cls(
            id=data.get("id"),
            work_id=data.get("work_id"),
            title=data.get("title"),
            lines=[Line.from_dict(ln) for ln in data.get("lines", [])],
            scenarios=[Scenario.from_dict(sc) for sc in data.get("scenarios", [])]
        )
