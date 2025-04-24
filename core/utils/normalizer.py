import re
import unicodedata


def normalize_work_id(title: str) -> str:
    """
    Converte um título de obra em work_id padronizado:
    - minúsculas
    - sem acentos
    - só a-z0-9 e underscore
    """
    normalized = unicodedata.normalize("NFKD", title)
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "_", ascii_only.lower()).strip("_")
    return slug


def format_chapter_id(index: int, padding: int = 3) -> str:
    """
    Formata um número de capítulo com zeros à esquerda.
    Ex: index=5, padding=3 → '005'
    """
    return str(index).zfill(padding)


def safe_filename(name: str, replace_with: str = "_") -> str:
    """
    Remove caracteres inválidos de nomes de arquivo.
    Mantém letras, números, underscore, hífen e ponto.
    """
    filename = unicodedata.normalize("NFKD", name)
    filename = filename.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^A-Za-z0-9._-]", replace_with, filename)
