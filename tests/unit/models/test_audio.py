import pytest
from pathlib import Path
from core.models.audio_segment import AudioSegment, ChapterAudio
from core.models.segment import Segment
from core.models.character import Character
from core.models.voice_profile import VoiceProfile
from core.enums import SegmentType, EmotionType, CharacterType, GenderType

# ===== AudioSegment =====

def test_audio_segment_valid(sample_audio_segment):
    assert sample_audio_segment.segment.text == "Texto original"
    assert sample_audio_segment.voice.name == "Padrão Feminina"
    assert isinstance(sample_audio_segment.file_path, Path)

def test_audio_segment_to_dict(sample_audio_segment):
    d = sample_audio_segment.to_dict()
    assert d["voice"]["name"] == "Padrão Feminina"
    assert "file_path" in d
    assert isinstance(d["segment"], dict)

def test_audio_segment_from_dict(sample_audio_segment_dict):
    d = sample_audio_segment_dict.copy()
    seg = AudioSegment.from_dict(d)
    assert isinstance(seg, AudioSegment)
    assert seg.voice.name == "Padrão Feminina"
    assert isinstance(seg.file_path, Path)

# ----- Validações -----

def test_audio_segment_invalid_types(sample_segment, tmp_path):
    dummy_file = tmp_path / "x.mp3"
    dummy_file.write_text("a")

    with pytest.raises(TypeError):
        AudioSegment(segment="not segment", voice=VoiceProfile(id="v", name="n", vendor="v", language="pt", gender=GenderType.MALE), file_path=dummy_file)

    with pytest.raises(TypeError):
        AudioSegment(segment=sample_segment, voice="not voice", file_path=dummy_file)

    with pytest.raises(TypeError):
        AudioSegment(segment=sample_segment, voice=VoiceProfile(id="v", name="n", vendor="v", language="pt", gender=GenderType.MALE), file_path="not_path")

def test_audio_segment_validate_audio_file_not_found(sample_segment, sample_voice_profile):
    fake_path = Path("/caminho/para/audio/que/nao_existe.wav")
    with pytest.raises(FileNotFoundError):
        AudioSegment(segment=sample_segment, voice=sample_voice_profile, file_path=fake_path)

# ===== ChapterAudio =====

def test_chapter_audio_valid(sample_chapter_audio):
    audio = sample_chapter_audio
    assert audio.chapter_id == "cap01"
    assert len(audio.segments) == 1

def test_chapter_audio_add_segment(sample_audio_segment):
    chapter_audio = ChapterAudio(chapter_id="cap02")
    chapter_audio.add_segment(sample_audio_segment)
    assert len(chapter_audio.segments) == 1

def test_chapter_audio_to_dict(sample_audio_segment):
    audio = ChapterAudio(chapter_id="cap03", segments=[sample_audio_segment])
    d = audio.to_dict()
    assert d["chapter_id"] == "cap03"
    assert isinstance(d["segments"], list)

def test_chapter_audio_from_dict(sample_chapter_audio_dict):
    raw = sample_chapter_audio_dict.copy()
    cap = ChapterAudio.from_dict(raw)
    assert cap.chapter_id == "cap01"
    assert isinstance(cap.segments[0], AudioSegment)

# ----- Validações -----

def test_chapter_audio_invalid_types():
    with pytest.raises(ValueError):
        ChapterAudio(chapter_id=" ")

    with pytest.raises(TypeError):
        ChapterAudio(chapter_id="ch01", segments="não é lista")

    with pytest.raises(TypeError):
        ChapterAudio(chapter_id="ch01", segments=["item errado"])

def test_chapter_audio_invalid_add_segment():
    chapter_audio = ChapterAudio(chapter_id="cap02")
    with pytest.raises(TypeError):
        chapter_audio.add_segment("invalid_segment")
