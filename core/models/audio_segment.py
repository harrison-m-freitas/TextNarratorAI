import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any

from core.models.segment import Segment
from core.models.voice_profile import VoiceProfile

logger = logging.getLogger(__name__)


@dataclass
class AudioSegment:
    segment: Segment
    voice: VoiceProfile
    file_path: Path

    def __post_init__(self):
        logger.debug("Inicializando AudioSegment: file_path=%s", self.file_path)

        if not isinstance(self.segment, Segment):
            logger.error("segment inválido: %s", type(self.segment))
            raise TypeError("O campo 'segment' deve ser uma instância de Segment.")
        
        if not isinstance(self.voice, VoiceProfile):
            logger.error("voice inválido: %s", type(self.voice))
            raise TypeError("O campo 'voice' deve ser uma instância de VoiceProfile.")
        
        if not isinstance(self.file_path, Path):
            logger.error("file_path inválido: %s", type(self.file_path))
            raise TypeError("O campo 'file_path' deve ser uma instância de pathlib.Path.")
        
        try:
            self.validate_audio_file(self.file_path)
        except FileNotFoundError as e:
            logger.warning("Validação falhou: %s", e)
            raise FileNotFoundError
            
    def validate_audio_file(self, path: Path):
        logger.debug("Validando arquivo de áudio: %s", path)
        if not path.exists() or not path.is_file():
            logger.warning("Arquivo de áudio não encontrado: %s", path)
            raise FileNotFoundError(f"Áudio não encontrado em {path}")

    def to_dict(self) -> dict:
        logger.debug("Serializando AudioSegment para dict: %s", self.file_path.name)
        return {
            "segment": self.segment.to_dict(),
            "voice": self.voice.to_dict(),
            "file_path": str(self.file_path),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AudioSegment":
        logger.debug("Criando AudioSegment a partir de dict.")
        return cls(
            segment=Segment.from_dict(data.get("segment")),
            voice=VoiceProfile.from_dict(data.get("voice")),
            file_path=Path(data.get("file_path"))
        )
        
@dataclass
class ChapterAudio:
    chapter_id: str
    segments: List[AudioSegment] = field(default_factory=list)

    def __post_init__(self):
        logger.debug("Inicializando ChapterAudio para capítulo: %s", self.chapter_id)

        if not self.chapter_id.strip():
            logger.error("chapter_id está vazio.")
            raise ValueError("O campo 'chapter_id' do capítulo não pode estar vazio.")
        
        if not isinstance(self.segments, list):
            logger.error("'segments' deve ser uma lista. Recebido: %s", type(self.segments))
            raise TypeError("'segments' deve ser uma lista.")
        
        for seg in self.segments:
            if not isinstance(seg, AudioSegment):
                logger.error("Item inválido em segments: %s", type(seg))
                raise TypeError("Todos os itens em 'segments' devem ser instâncias de AudioSegment.")

    def add_segment(self, segment: AudioSegment):
        logger.debug("Adicionando AudioSegment ao capítulo %s", self.chapter_id)
        if not isinstance(segment, AudioSegment):
            logger.error("Tipo inválido para segmento: %s", type(segment))
            raise TypeError("segment deve ser uma instância de AudioSegment.")
        self.segments.append(segment)

    def to_dict(self) -> dict:
        logger.debug("Serializando ChapterAudio para dict: capítulo %s", self.chapter_id)
        return {
            "chapter_id": self.chapter_id,
            "segments": [seg.to_dict() for seg in self.segments]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChapterAudio":
        logger.debug("Criando ChapterAudio a partir de dict: capítulo %s", data.get("chapter_id", ""))
        return cls(
            chapter_id=data.get("chapter_id", ""),
            segments=[AudioSegment.from_dict(seg) for seg in data.get("segments", [])]
        )
