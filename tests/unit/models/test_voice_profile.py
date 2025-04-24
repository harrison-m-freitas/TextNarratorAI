import pytest
from core.enums.gender_type import GenderType
from core.models.voice_profile import VoiceProfile


def test_voice_profile_valid(sample_voice_profile):
    assert sample_voice_profile.id == "vp01"
    assert sample_voice_profile.name.startswith("Padrão")
    assert sample_voice_profile.vendor == "ElevenLabs"
    assert sample_voice_profile.language == "pt-BR"
    assert sample_voice_profile.gender == GenderType.FEMALE

def test_voice_profile_to_dict():
    vp = VoiceProfile(
        id="v2",
        name="Voz X",
        vendor="OpenVoice",
        language="en-US",
        gender=GenderType.MALE
    )
    d = vp.to_dict()
    assert d == {
        "id": "v2",
        "name": "Voz X",
        "vendor": "OpenVoice",
        "language": "en-US",
        "gender": "male"
    }

def test_voice_profile_from_dict_roundtrip():
    original = VoiceProfile(
        id="abc",
        name="Teste",
        vendor="TesteLab",
        language="ja-JP",
        gender=GenderType.UNKNOWN
    )
    clone = VoiceProfile.from_dict(original.to_dict())
    assert clone == original

# def test_validate_audio_file_found(tmp_path):
#     path = tmp_path / "audio.mp3"
#     path.write_text("dummy content")
#     vp = VoiceProfile(id="a", name="b", vendor="c", language="pt", gender=GenderType.MALE)
#     vp.validate_audio_file(path)  # não deve lançar exceção

# def test_validate_audio_file_not_found(tmp_path):
#     missing_path = tmp_path / "nope.wav"
#     vp = VoiceProfile(id="a", name="b", vendor="c", language="pt", gender=GenderType.MALE)
#     with pytest.raises(FileNotFoundError):
#         vp.validate_audio_file(missing_path)

# ===== Validações =====

@pytest.mark.parametrize("field,value", [
    ("id", ""),
    ("name", ""),
    ("vendor", ""),
    ("language", ""),
])
def test_voice_profile_invalid_string_fields(field, value, sample_voice_profile_dict):
    kwargs = sample_voice_profile_dict.copy()
    kwargs[field] = value
    with pytest.raises(ValueError) as e:
        VoiceProfile(**kwargs)
    assert field in str(e.value)

def test_voice_profile_invalid_gender_type():
    with pytest.raises(TypeError):
        VoiceProfile(
            id="v1",
            name="Inválida",
            vendor="XPTO",
            language="pt-BR",
            gender="female"
        )
