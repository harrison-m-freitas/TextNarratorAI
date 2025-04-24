import pytest
from pathlib import Path
from adapters.loaders.file_text_loader import FileTextLoader
from core.models.line import Line

def test_file_text_loader_reads_lines(tmp_path):
    file = tmp_path / "sample.txt"
    content = "Linha 1\n\nLinha 2\n Linha 3 com espaço\n"
    file.write_text(content, encoding="utf-8")

    loader = FileTextLoader()
    lines = loader.load(str(file))

    assert isinstance(lines, list)
    assert all(isinstance(l, Line) for l in lines)
    assert len(lines) == 3  # Linha vazia ignorada

    assert lines[0].original_text == "Linha 1"
    assert lines[0].line_number == 0

    assert lines[1].original_text == "Linha 2"
    assert lines[1].line_number == 2

    assert lines[2].original_text.strip() == "Linha 3 com espaço"
    assert lines[2].line_number == 3


def test_file_text_loader_fallback(tmp_path):
    raw_bytes = b'\xff'
    file_path = tmp_path / "weird.txt"
    file_path.write_bytes(raw_bytes)

    loader = FileTextLoader()
    lines = loader.load(str(file_path))

    assert isinstance(lines, list) and len(lines) == 1
    line = lines[0]
    assert isinstance(line, Line)

    assert line.original_text == "ÿ"
    assert line.line_number == 0
