import pytest
from core.enums import CharacterType, GenderType
from core.models.character import Character
from core.repositories.character_repository import CharacterRepository

# === get_or_create ===

def test_get_or_create_creates_new(char_repo):
    character = char_repo.get_or_create("Ye Hong")
    assert isinstance(character, Character)
    assert character.name == "Ye Hong"
    assert character.type == CharacterType.UNKNOWN
    assert character.gender == GenderType.UNKNOWN
    assert char_repo.exists("Ye Hong")


def test_get_or_create_returns_existing(char_repo):
    first = char_repo.get_or_create("Zhang")
    second = char_repo.get_or_create("Zhang")
    assert first is second


def test_get_or_create_strips_and_normalizes_case(char_repo):
    c1 = char_repo.get_or_create("  Zhang ")
    c2 = char_repo.get_or_create("zhang")
    assert c1 is c2


def test_get_or_create_raises_on_empty(char_repo):
    with pytest.raises(ValueError):
        char_repo.get_or_create("   ")


# === upsert ===

def test_upsert_creates_and_sets_type_gender_enum(char_repo):
    character = char_repo.upsert("Nova", CharacterType.PROTAGONIST, GenderType.FEMALE)
    assert character.name == "Nova"
    assert character.type == CharacterType.PROTAGONIST
    assert character.gender == GenderType.FEMALE


def test_upsert_accepts_string_inputs(char_repo):
    character = char_repo.upsert("Bot", "supporting_male", "male")
    assert character.type == CharacterType.SUPPORTING_MALE
    assert character.gender == GenderType.MALE


def test_upsert_fallbacks_on_invalid_values(char_repo):
    character = char_repo.upsert("Mistério", "invalido", "????")
    assert character.type == CharacterType.UNKNOWN
    assert character.gender == GenderType.UNKNOWN


# === exists ===

def test_exists_true_and_false(char_repo):
    assert not char_repo.exists("Zhang")
    char_repo.get_or_create("Zhang")
    assert char_repo.exists("zhang") is True


def test_exists_ignores_empty(char_repo):
    assert not char_repo.exists("   ")


# === list ===

def test_list_returns_all_characters(char_repo):
    char_repo.get_or_create("Ye")
    char_repo.get_or_create("Zhang")
    char_repo.get_or_create("Ye")  # já existe
    all_chars = char_repo.list()
    assert isinstance(all_chars, list)
    assert len(all_chars) == 2
    assert all(isinstance(c, Character) for c in all_chars)
