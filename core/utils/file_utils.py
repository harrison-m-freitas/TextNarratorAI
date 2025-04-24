import json
import hashlib
from pathlib import Path
from typing import Any, List, Union


def compute_checksum(text: Union[str, bytes], algo: str = "sha256") -> str:
    """
    Retorna o hash (hex) de um texto ou bytes.
    """
    h = hashlib.new(algo)
    if isinstance(text, str):
        text = text.encode("utf-8")
    h.update(text)
    return h.hexdigest()


def load_json(path: Path) -> Any:
    """
    Lê um arquivo JSON e retorna o objeto Python.
    """
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: Any, indent: int = 2) -> None:
    """
    Salva um objeto Python como JSON.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=indent), encoding="utf-8")


def read_text_lines(path: Path) -> List[str]:
    """
    Lê um arquivo texto e retorna lista de linhas (stripped).
    """
    return [line.rstrip("\n") for line in path.open(encoding="utf-8")]


def write_text(path: Path, text: str) -> None:
    """
    Grava um texto num arquivo, criando pastas se necessário.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
