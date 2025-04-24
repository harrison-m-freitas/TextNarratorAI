import chardet
import logging
from pathlib import Path
from typing import List

from core.interfaces.input import ITextLoader
from core.models.line import Line

logger = logging.getLogger(__name__)


class FileTextLoader(ITextLoader):
    """
    Adapter que lê arquivos .txt locais, detecta codificação e retorna linhas numeradas.
    """

    def load(self, file_path: str) -> List[Line]:
        path = Path(file_path)
        raw = path.read_bytes()
        logger.debug("Arquivo lido: %s (%d bytes)", path.name, len(raw))

        try:
            text = raw.decode("utf-8")
            logger.info("Arquivo '%s' decodificado com UTF-8 com sucesso", path.name)
        except UnicodeDecodeError:
            detection = chardet.detect(raw)
            encoding = detection.get("encoding") or "utf-8"
            confidence = detection.get("confidence", 0.0)
            logger.warning("UTF-8 falhou para '%s', detectado encoding '%s' (confiança %.2f)", path.name, encoding, confidence)
            text = raw.decode(encoding, errors="replace")

        lines: List[Line] = []
        for idx, line in enumerate(text.splitlines()):
            if line.strip():
                lines.append(Line(original_text=line, line_number=idx))
        
        logger.debug("Total de linhas válidas carregadas: %d", len(lines))
        return lines
