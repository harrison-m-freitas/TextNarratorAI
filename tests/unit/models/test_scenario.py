import pytest
from core.models.scenario import Scenario

def test_scenario_valid_creation(sample_scenario):
    assert sample_scenario.index == 0
    assert "Cenário" in sample_scenario.text
    assert sample_scenario.location == "Sala 18"
    assert isinstance(sample_scenario.characters, list)
    assert "Ye Hong" in sample_scenario.characters

def test_scenario_empty_characters_defaults_to_empty_list():
    s = Scenario(index=1, text="Biblioteca abandonada", location="Bloco C", characters=None)
    assert s.characters == []

def test_scenario_to_dict():
    s = Scenario(index=2, text="Refeitório movimentado", location="Bloco Central", characters=["João"])
    d = s.to_dict()
    assert d["index"] == 2
    assert d["text"].startswith("Refeitório")
    assert d["location"] == "Bloco Central"
    assert d["characters"] == ["João"]

def test_scenario_from_dict(sample_scenario_dict):
    data = sample_scenario_dict.copy()
    s = Scenario.from_dict(data)
    assert isinstance(s, Scenario)
    assert s.text.startswith("Cenário")
    assert "Srta. Zhang" in s.characters

# ===== Validações =====

@pytest.mark.parametrize("index", [-1, -100])
def test_scenario_invalid_index(index):
    with pytest.raises(ValueError):
        Scenario(index=index, text="Texto", location="Aqui")

@pytest.mark.parametrize("text", ["", "   "])
def test_scenario_empty_text_raises(text):
    with pytest.raises(ValueError):
        Scenario(index=0, text=text, location="Qualquer")

def test_scenario_invalid_characters_type():
    with pytest.raises(TypeError):
        Scenario(index=0, text="Lugar", location=None, characters="Ye Hong")

def test_scenario_invalid_characters_element_type():
    with pytest.raises(TypeError):
        Scenario(index=0, text="Lugar", location=None, characters=["Ye Hong", 123])
