import pytest
from core.models.chapter import Chapter
from core.models.line import Line

def test_chapter_valid_creation(sample_chapter):
    chapter = sample_chapter
    assert chapter.id == "cap01"
    assert chapter.title.startswith("Capítulo")
    assert len(chapter.lines) == 1
    assert isinstance(chapter.lines[0], Line)
    
def test_chapter_to_dict(sample_chapter):
    chapter = sample_chapter
    d = chapter.to_dict()
    assert d["id"] == "cap01"
    assert isinstance(d["lines"], list)
    assert isinstance(d["scenarios"], list)
    assert d["lines"][0]["original_text"] == "Linha de entrada original"

def test_chapter_from_dict(sample_chapter_dict, sample_line, sample_scenario):
    raw = sample_chapter_dict.copy()
    chapter = Chapter.from_dict(raw)
    assert isinstance(chapter, Chapter)
    assert chapter.id == "cap01"
    assert chapter.lines[0].original_text == sample_line.original_text
    assert chapter.scenarios[0].location == sample_scenario.location

def test_chapter_add_line_and_scenario(sample_chapter, sample_line, sample_scenario):
    chapter = sample_chapter
    chapter.add_line(sample_line)
    chapter.add_scenario(sample_scenario)
    assert len(chapter.lines) == 2
    assert len(chapter.scenarios) == 2

# ----- Validações -----

@pytest.mark.parametrize("field,value", [
    ("id", ""),
    ("work_id", " "),
    ("title", " "),
])
def test_chapter_missing_required_fields(field, value, sample_chapter_dict):
    kwargs = sample_chapter_dict.copy()
    kwargs[field] = value
    with pytest.raises(ValueError):
        Chapter(**kwargs)

def test_chapter_invalid_line_type():
    with pytest.raises(TypeError):
        Chapter(id="c1", work_id="w1", title="Capítulo", lines="linha errada", scenarios=[])
    
    with pytest.raises(TypeError):
        Chapter(id="c1", work_id="w1", title="Capítulo", lines=["linha errada"], scenarios=[])

def test_chapter_invalid_scenario_type():
    with pytest.raises(TypeError):
        Chapter(id="c1", work_id="w1", title="Capítulo", lines=[], scenarios="não é scenario")
    
    with pytest.raises(TypeError):
        Chapter(id="c1", work_id="w1", title="Capítulo", lines=[], scenarios=["não é scenario"])

def test_chapter_add_invalid_line():
    chapter = Chapter(id="c1", work_id="w1", title="Capítulo")
    with pytest.raises(TypeError):
        chapter.add_line("isso não é uma Line")

def test_chapter_add_invalid_scenario():
    chapter = Chapter(id="c1", work_id="w1", title="Capítulo")
    with pytest.raises(TypeError):
        chapter.add_scenario(123)
