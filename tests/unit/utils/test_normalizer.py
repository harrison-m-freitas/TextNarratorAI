import pytest
from core.utils.normalizer import (
    normalize_work_id,
    format_chapter_id,
    safe_filename
)

# ========== normalize_work_id ==========

@pytest.mark.parametrize("title,expected", [
    ("Urban Strengthening System", "urban_strengthening_system"),
    ("Ação & Vida!", "acao_vida"),
    (" Olá  Mundo! ", "ola_mundo"),
    ("My@Book#Name!", "my_book_name"),
    ("123_ABC", "123_abc"),
])
def test_normalize_work_id(title, expected):
    assert normalize_work_id(title) == expected


# ========== format_chapter_id ==========

@pytest.mark.parametrize("index,padding,expected", [
    (5, 3, "005"),
    (42, 4, "0042"),
    (0, 2, "00"),
    (1234, 2, "1234"),
])
def test_format_chapter_id(index, padding, expected):
    assert format_chapter_id(index, padding) == expected


# ========== safe_filename ==========

@pytest.mark.parametrize("name,expected", [
    ("meu_arquivo.txt", "meu_arquivo.txt"),
    ("com espaços.txt", "com_espacos.txt"),
    ("ãçõáéí.doc", "acoaei.doc"),
    ("~!@#$%^&*()[]{}", "_______________"),
])
def test_safe_filename_default(name, expected):
    assert safe_filename(name) == expected


def test_safe_filename_custom_replacement():
    name = "nome inválido.txt"
    result = safe_filename(name, replace_with="-")
    assert result == "nome-invalido.txt"