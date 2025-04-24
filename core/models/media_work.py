import logging
from dataclasses import dataclass, field
from typing import List, Optional

from core.models.chapter import Chapter

logger = logging.getLogger(__name__)


@dataclass
class MediaWork:
    """
    Representa uma obra (livro, webnovel, manhua...).
    """
    id: str 
    title: str
    author: Optional[str] = None
    original_language: str = "und"
    description: Optional[str] = None
    chapters: List[Chapter] = field(default_factory=list)
    
    def __post_init__(self):
        logger.debug("Inicializando MediaWork: id=%s title=%s", self.id, self.title)

        if not self.id.strip():
            logger.error("ID da obra está vazio.")
            raise ValueError("O campo 'id' da obra não pode estar vazio.")
        if not self.title.strip():
            logger.error("Título da obra está vazio.")
            raise ValueError("O campo 'title' da obra não pode estar vazio.")
        if not isinstance(self.original_language, str):
            logger.error("Campo 'original_language' inválido: %s", type(self.original_language))
            raise TypeError("O campo 'original_language' deve ser uma string.")
        if not isinstance(self.chapters, list):
            logger.error("Campo 'chapters' deve ser uma lista: %s", type(self.chapters))
            raise TypeError("O campo 'chapters' deve ser uma lista.")
        for chapter in self.chapters:
            if not isinstance(chapter, Chapter):
                logger.error("Capítulo inválido encontrado na lista: %s", type(chapter))
                raise TypeError("Todos os itens em 'chapters' devem ser instâncias de Chapter.")

    def add_chapter(self, chapter: Chapter):
        if not isinstance(chapter, Chapter) or chapter.work_id != self.id :
            logger.error("Capítulo %s pertence à obra %s, não à %s", chapter.id, chapter.work_id, self.id)
            raise ValueError("Este capítulo não pertence a esta obra")
        logger.debug("Adicionando capítulo %s à obra %s", chapter.id, self.id)
        self.chapters.append(chapter)

    def to_dict(self) -> dict:
        data = {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "original_language": self.original_language,
            "description": self.description,
            "chapters": [c.to_dict() for c in self.chapters],
        }
        logger.debug("Serializando MediaWork para dict: %s", data)
        return data
        
    @classmethod
    def from_dict(cls, data) -> "MediaWork":
        logger.debug("Criando MediaWork a partir de dict: %s", data)
        return cls(
            id=data.get("id"),
            title=data.get("title"),
            author=data.get("author"),
            original_language=data.get("original_language"),
            description=data.get("description"),
            chapters=[Chapter.from_dict(chapter) for chapter in data.get("chapters", [])],
        )
