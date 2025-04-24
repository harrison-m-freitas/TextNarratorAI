import pytest
from core.models.character import Character
from core.enums import CharacterType, GenderType

def test_character_valid_creation(sample_character, sample_voice_profile_male):
    c = sample_character
    assert c.name == "Ye Hong"
    assert c.type == CharacterType.PROTAGONIST
    assert c.gender == GenderType.MALE
    assert c.voice is sample_voice_profile_male

def test_character_to_dict(sample_voice_profile):
    c = Character(
        name="Ana",
        type=CharacterType.SUPPORTING_FEMALE,
        gender=GenderType.FEMALE,
        voice=sample_voice_profile
    )
    d = c.to_dict()
    assert d["name"] == "Ana"
    assert d["type"] == "supporting_female"
    assert d["gender"] == "female"
    assert "voice" in d and isinstance(d["voice"], dict)

def test_character_from_dict(sample_character_dict):
    data = sample_character_dict.copy()
    c = Character.from_dict(data)
    assert isinstance(c, Character)
    assert c.name == "Ye Hong"
    assert c.type == CharacterType.PROTAGONIST
    assert c.gender == GenderType.MALE
    assert c.voice.name == "Padrão Masculino"

def test_character_assign_voice(sample_voice_profile):
    c = Character(
        name="Ana",
        type=CharacterType.SUPPORTING_FEMALE,
        gender=GenderType.FEMALE,
        voice=None
    )
    c.assign_voice(sample_voice_profile)
    assert c.voice == sample_voice_profile

# ----- Validações -----

def test_character_assign_voice_gender_mismatch(sample_character, sample_voice_profile):
    with pytest.raises(ValueError):
        sample_character.assign_voice(sample_voice_profile)

@pytest.mark.parametrize("name", ["", "   "])
def test_character_invalid_name(name):
    with pytest.raises(ValueError):
        Character(name=name, type=CharacterType.PROTAGONIST, gender=GenderType.MALE)

def test_character_invalid_type():
    with pytest.raises(TypeError):
        Character(name="X", type="not-a-valid-type", gender=GenderType.MALE)

def test_character_invalid_gender():
    with pytest.raises(TypeError):
        Character(name="X", type=CharacterType.PROTAGONIST, gender="female")

def test_character_invalid_voice_type():
    with pytest.raises(TypeError):
        Character(name="X", type=CharacterType.PROTAGONIST, gender=GenderType.MALE, voice="not-a-voice")
