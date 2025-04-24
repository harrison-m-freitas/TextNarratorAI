import pytest

from core.enums import (
    SegmentType, CharacterType, 
    GenderType, EmotionType,
    LLMRole
)


@pytest.mark.parametrize("enum_cls, valid_values", [
    (SegmentType, [e.value for e in SegmentType]),
    (CharacterType, [e.value for e in CharacterType]),
    (GenderType, [e.value for e in GenderType]),
    (EmotionType, [e.value for e in EmotionType]),
    (LLMRole, [e.value for e in LLMRole]),
])
def test_list_returns_all_values(enum_cls, valid_values):
    values = enum_cls.list()
    assert isinstance(values, list)
    assert set(values) == set(valid_values)
    
@pytest.mark.parametrize("enum_cls, valid_value", [
    (SegmentType, "narration"),
    (SegmentType, "dialogue"),
    (SegmentType, "highlight"),
    (CharacterType, "narrator"),
    (CharacterType, "protagonist"),
    (CharacterType, "supporting_male"),
    (CharacterType, "supporting_female"),
    (CharacterType, "system"),
    (CharacterType, "unknown"),
    (GenderType, "male"),
    (GenderType, "female"),
    (GenderType, "unknown"),
    (EmotionType, "neutral"),
    (EmotionType, "joy"),
    (EmotionType, "anger"),
    (EmotionType, "surprise"),
    (EmotionType, "hesitation"),
    (EmotionType, "shout"),
    (LLMRole, "system"),
    (LLMRole, "user"),
    (LLMRole, "assistant"),
    (LLMRole, "function"),
])
def test_is_valid_accepts_known_values(enum_cls, valid_value):
    assert enum_cls.is_valid(valid_value) is True
    
@pytest.mark.parametrize("enum_cls, invalid_value", [
    (SegmentType, "xyz"),
    (CharacterType, ""),
    (GenderType, "other"),
    (EmotionType, "happy"),
    (LLMRole, "foo")
])
def test_is_valid_rejects_unknown_values(enum_cls, invalid_value):
    assert enum_cls.is_valid(invalid_value) is False
    
@pytest.mark.parametrize("enum_cls, valid_value, expected_member", [
    (SegmentType, "dialogue", SegmentType.DIALOGUE),
    (CharacterType, "protagonist", CharacterType.PROTAGONIST),
    (GenderType, "female", GenderType.FEMALE),
    (EmotionType, "surprise", EmotionType.SURPRISE),
    (LLMRole, "assistant", LLMRole.ASSISTANT)
])
def test_safe_returns_enum_for_valid(enum_cls, valid_value, expected_member):
    assert enum_cls.safe(valid_value) is expected_member
    
@pytest.mark.parametrize("enum_cls, invalid_value, default_member", [
    (SegmentType, "foo", SegmentType.NARRATION),
    (CharacterType, "foo", CharacterType.UNKNOWN),
    (GenderType, "foo", GenderType.UNKNOWN),
    (EmotionType, "foo", EmotionType.NEUTRAL),
    (LLMRole, "foo", LLMRole.SYSTEM)
])
def test_safe_fallbacks_to_default(enum_cls, invalid_value, default_member):
    assert enum_cls.safe(invalid_value) is default_member    
    
@pytest.mark.parametrize("enum_cls, invalid_value, explicit_default", [
    (SegmentType, "foo", SegmentType.DIALOGUE),
    (CharacterType, "foo", CharacterType.SYSTEM),
    (GenderType, "foo", GenderType.MALE),
    (EmotionType, "foo", EmotionType.JOY),
    (LLMRole, "foo", LLMRole.ASSISTANT)
])
def test_safe_respects_explicit_default(enum_cls, invalid_value, explicit_default):
    assert enum_cls.safe(invalid_value, default=explicit_default) is explicit_default
    
@pytest.mark.parametrize("enum_member", [
    SegmentType.NARRATION,
    SegmentType.DIALOGUE,
    CharacterType.PROTAGONIST,
    CharacterType.SYSTEM,
    GenderType.MALE,
    GenderType.UNKNOWN,
    EmotionType.JOY,
    EmotionType.SHOUT,
    LLMRole.SYSTEM,
    LLMRole.USER
])
def test_str_returns_value(enum_member):
    assert str(enum_member) == enum_member.value
    