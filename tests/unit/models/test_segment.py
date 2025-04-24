import pytest
from core.models.segment import Segment
from core.enums import SegmentType, EmotionType

def test_segment_valid_creation(sample_segment):
    assert sample_segment.segment_index == 0
    assert sample_segment.line_number == 1
    assert sample_segment.segment_type == SegmentType.DIALOGUE
    assert sample_segment.character.name == "Ye Hong"
    assert sample_segment.emotion == EmotionType.JOY

def test_segment_to_dict(sample_character):    
    seg = Segment(
        segment_index=1,
        line_number=10,
        text="Texto",
        translated_text="Texto traduzido",
        segment_type=SegmentType.HIGHLIGHT,
        speaker_hint="Sistema",
        character=sample_character,
        emotion=EmotionType.SURPRISE
    )
    d = seg.to_dict()
    assert d["segment_index"] == 1
    assert d["segment_type"] == "highlight"
    assert d["emotion"] == "surprise"
    assert d["character"]["name"] == "Ye Hong"

def test_segment_from_dict(sample_segment_dict):
    seg = Segment.from_dict(sample_segment_dict)
    assert isinstance(seg, Segment)
    assert seg.segment_index == 0
    assert seg.line_number == 1
    assert seg.segment_type == SegmentType.DIALOGUE
    assert seg.emotion == EmotionType.JOY
    assert seg.character.name == "Ye Hong"
    
# ===== Validações =====

def test_segment_post_init_validation_errors():
    with pytest.raises(ValueError):
        Segment(segment_index=-1, line_number=1, text="x")

    with pytest.raises(ValueError):
        Segment(segment_index=0, line_number=-5, text="x")

    with pytest.raises(ValueError):
        Segment(segment_index=0, line_number=1, text="")

    with pytest.raises(TypeError):
        Segment(segment_index=0, line_number=1, text="x", segment_type="dialogue")

    with pytest.raises(TypeError):
        Segment(segment_index=0, line_number=1, text="x", emotion="joy")

    with pytest.raises(TypeError):
        Segment(segment_index=0, line_number=1, text="x", character="not a character")
