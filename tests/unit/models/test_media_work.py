import pytest
from core.models.media_work import MediaWork
from core.models.chapter import Chapter

def test_media_work_valid_creation(sample_media_work):
    assert sample_media_work.id == "obra01"
    assert sample_media_work.title.startswith("Urban")
    assert sample_media_work.chapters[0].id == "cap01"

def test_media_work_add_chapter_success(sample_media_work):    
    chapter = Chapter(id="cap02", work_id="obra01", title="Capítulo 2")
    sample_media_work.add_chapter(chapter)
    assert len(sample_media_work.chapters) == 2
    assert sample_media_work.chapters[1].id == "cap02"

def test_media_work_to_dict_and_from_dict(sample_media_work, sample_media_work_dict):
    d = sample_media_work.to_dict()
    assert d["title"] == "Urban Strengthening System"
    assert isinstance(d["chapters"], list)
    assert d["chapters"][0]["id"] == "cap01"
    assert d == sample_media_work_dict
    
    clone = MediaWork.from_dict(d)
    assert clone.id == "obra01"
    assert clone.chapters[0].id == "cap01"

# ===== Validações =====

def test_media_work_empty_fields_raise():
    with pytest.raises(ValueError):
        MediaWork(id="", title="Alguma obra")

    with pytest.raises(ValueError):
        MediaWork(id="w", title=" ")

    with pytest.raises(TypeError):
        MediaWork(id="w", title="T", original_language=123)

    with pytest.raises(TypeError):
        MediaWork(id="w", title="T", chapters="não é lista")

def test_media_work_invalid_chapter_type():
    with pytest.raises(TypeError):
        MediaWork(id="w", title="T", chapters=["isso não é chapter"])

def test_media_work_add_chapter_wrong_work_id():
    work = MediaWork(id="w01", title="Obra")
    chapter = Chapter(id="c01", work_id="diferente", title="Capítulo")
    with pytest.raises(ValueError):
        work.add_chapter(chapter)
