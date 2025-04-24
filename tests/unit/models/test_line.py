import pytest
from core.enums import SegmentType
from core.models.line import Line

def test_line_valid_creation(sample_line):
    line = sample_line
    assert line.original_text.startswith("Linha")
    assert line.translated_text == "Linha traduzida"
    assert len(line.segments) == 1
    assert line.line_number == 1

def test_line_without_segments():
    line = Line(original_text="Texto simples")
    assert line.segments == []
    assert line.line_number == -1

def test_line_to_dict(sample_line):
    line = sample_line
    d = line.to_dict()
    assert d["original_text"] == "Linha de entrada original"
    assert d["translated_text"] == "Linha traduzida"
    assert d["line_number"] == 1
    assert isinstance(d["segments"], list)
    assert d["segments"][0]["segment_type"] == "dialogue"

def test_line_from_dict(sample_line_dict):
    line = Line.from_dict(sample_line_dict)
    assert isinstance(line, Line)
    assert line.line_number == 1
    assert len(line.segments) == 1
    assert line.segments[0].segment_type == SegmentType.DIALOGUE

# # ----- Validações -----

def test_line_invalid_original_text():
    with pytest.raises(ValueError):
        Line(original_text="   ")

def test_line_invalid_segments_type():
    with pytest.raises(TypeError):
        Line(original_text="OK", segments="isso não é uma lista")

def test_line_invalid_segment_items():
    with pytest.raises(TypeError):
        Line(original_text="OK", segments=["isso não é Segment"])

def test_line_invalid_line_number():
    with pytest.raises(ValueError):
        Line(original_text="OK", line_number=-2)
