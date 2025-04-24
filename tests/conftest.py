import sys
import json
import shutil
import pytest
import logging.config
from pathlib import Path
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).resolve().parent.parent))

from config.logging_config import LOGGING

from core.enums import GenderType, CharacterType, SegmentType, EmotionType, LLMRole
from core.interfaces.llm import ILLMClient

from core.models.audio_segment import AudioSegment, ChapterAudio
from core.models.chapter import Chapter
from core.models.character import Character
from core.models.line import Line
from core.models.llm import LLMMessage, LLMResponse, LLMUsage
from core.models.media_work import MediaWork
from core.models.scenario import Scenario
from core.models.segment import Segment
from core.models.voice_profile import VoiceProfile

from core.repositories.character_repository import CharacterRepository
from core.utils.file_utils import save_json


@pytest.fixture(autouse="True")
def tmp_project_root(tmp_path, monkeypatch):
    """
    Change CWD to a temporary directory for all tests,
    so that data/input, data/store, data/output live under tmp_path.
    """
    monkeypatch.chdir(tmp_path)
    return tmp_path

@pytest.fixture
def base_input(tmp_project_root):
    p = tmp_project_root / "data" / "input"
    p.mkdir(parents=True, exist_ok=True)
    return p

@pytest.fixture
def base_store(tmp_project_root):
    p = tmp_project_root / "data" / "store"
    p.mkdir(parents=True, exist_ok=True)
    return p

@pytest.fixture
def base_output(tmp_project_root):
    p = tmp_project_root / "data" / "output"
    p.mkdir(parents=True, exist_ok=True)
    return p

@pytest.fixture
def work_id():
    return "test_work"

@pytest.fixture
def sample_metadata(base_input, work_id):
    md = {
        "title": "Test Work",
        "original_language": "en",
        "author": "Tester",
        "tags": ["test", "example"]
    }
    save_json(base_input / work_id / "metadata.json", md)
    return md

@pytest.fixture
def chapters_dir(base_input, work_id):
    d = base_input / work_id / "chapters"
    d.mkdir(parent=True, exist_ok=True)
    return d

@pytest.fixture
def char_repo():
    return CharacterRepository()

class StubLLMClient(ILLMClient):
    """
    A simple stub of ILLMClient that always returns the given JSON text.
    """
    def __init__(self, response_text: str, usage: LLMUsage = None):
        self._response = response_text
        self._usage = usage

    def chat(self, messages, **kwargs) -> LLMResponse:
        return LLMResponse(text=self._response, usage=self._usage, raw=json.loads(self._response))

@pytest.fixture
def stub_llm_client():
    """
    Factory fixture to produce a StubLLMClient with given response.
    Usage:
        client = stub_llm_client(json_text)
    """
    def _factory(response_text: str):
        return StubLLMClient(response_text)
    return _factory

@pytest.fixture
def dummy_lines():
    """
    Returns a small list of Line instances for block-processor tests.
    """
    return [
        Line(line_number=1, original_text="Primeira linha."),
        Line(line_number=2, original_text="Segunda linha.")
    ]

@pytest.fixture
def dummy_segment_dicts():
    """
    Returns a sample list of dicts as LLM JSON payload for Segment.from_dict.
    """
    return [
        {
            "segment_index": 0,
            "line_number": 1,
            "original_text": "Primeira linha.",
            "translated_text": "Primeira linha.",
            "segment_type": "narration",
            "speaker": "Narrador",
            "character_type": "narrator",
            "gender": "unknown",
            "emotion": "neutral"
        },
        {
            "segment_index": 1,
            "line_number": 1,
            "original_text": "\"Olá!\"",
            "translated_text": "\"Olá!\"",
            "segment_type": "dialogue",
            "speaker": "Test",
            "character_type": "protagonist",
            "gender": "male",
            "emotion": "joy"
        }
    ]

def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow")
    config.addinivalue_line("markers", "e2e: mark test as end-to-end")

@pytest.fixture(scope="session", autouse=True)
def configure_logging_once():
    load_dotenv(override=True)
    logging.config.dictConfig(LOGGING)
    
@pytest.fixture(scope="session", autouse=True)
def silence_httpcore_logs():
    logging.getLogger("httpcore").setLevel(logging.CRITICAL)
    
        
# ---------------------- SAMPLES ----------------------

# ===== AudioSegment =====

@pytest.fixture
def sample_audio_segment(sample_segment: Segment, sample_voice_profile: VoiceProfile, tmp_path) -> AudioSegment:
    file_path = tmp_path / "audio.mp3"
    file_path.write_text("dummy audio")
    return AudioSegment(
        segment=sample_segment,
        file_path=file_path,
        voice=sample_voice_profile
    )
    
@pytest.fixture
def sample_audio_segment_dict(sample_segment_dict: dict, sample_voice_profile_dict: dict, tmp_path) -> dict:
    file_path = tmp_path / "audio.mp3"
    file_path.write_text("dummy audio")
    return {
        "segment": sample_segment_dict,
        "voice": sample_voice_profile_dict,
        "file_path": file_path,
    }
    

# ===== Chapter =====

@pytest.fixture
def sample_chapter(sample_line: Line, sample_scenario: Scenario) -> Chapter:
    return Chapter(
        id="cap01",
        work_id="obra01",
        title="Capítulo 1",
        lines=[sample_line],
        scenarios=[sample_scenario]
    )

@pytest.fixture
def sample_chapter_dict(sample_line_dict: dict, sample_scenario_dict: dict) -> dict:
    return {
        "id": "cap01",
        "work_id": "obra01",
        "title": "Capítulo 1",
        "lines": [sample_line_dict],
        "scenarios": [sample_scenario_dict],
    }


# ===== ChapterAudio =====

@pytest.fixture
def sample_chapter_audio(sample_audio_segment: AudioSegment) -> ChapterAudio:
    audio = ChapterAudio(chapter_id="cap01")
    audio.add_segment(sample_audio_segment)
    return audio

@pytest.fixture
def sample_chapter_audio_dict(sample_audio_segment_dict: dict) -> dict:
    return {
        "chapter_id": "cap01",
        "segments": [sample_audio_segment_dict],
    }
    
# ===== Character =====

@pytest.fixture
def sample_character(sample_voice_profile_male: VoiceProfile) -> Character:
    return Character(
        name="Ye Hong",
        type=CharacterType.PROTAGONIST,
        gender=GenderType.MALE,
        voice=sample_voice_profile_male
    )

@pytest.fixture
def sample_character_dict(sample_voice_profile_male_dict: dict) -> dict:
    return {
        "name": "Ye Hong",
        "type": CharacterType.PROTAGONIST,
        "gender": GenderType.MALE,
        "voice": sample_voice_profile_male_dict
    }


# ===== Line =====

@pytest.fixture
def sample_line(sample_segment: Segment) -> Line:
    return Line(
        original_text="Linha de entrada original",
        translated_text="Linha traduzida",
        segments=[sample_segment],
        line_number=1
    )
    
@pytest.fixture
def sample_line_dict(sample_segment_dict: dict) -> dict:
    return {
        "original_text": "Linha de entrada original",
        "translated_text": "Linha traduzida",
        "segments": [sample_segment_dict],
        "line_number": 1
    }

# ===== LLMMessage =====

@pytest.fixture
def sample_llm_message() -> LLMMessage:
    return LLMMessage(
        role=LLMRole.USER,
        content="Traduz esse parágrafo, por favor.",
        name="usuário1"
    )
    
@pytest.fixture
def sample_llm_message_dict() -> dict:
    return {
        "role": LLMRole.USER,
        "content": "Traduz esse parágrafo, por favor.",
        "name": "usuário1"
    }

# ===== LLMUsage =====

@pytest.fixture
def sample_llm_usage() -> LLMUsage:
    return LLMUsage(
        prompt_tokens=100,
        completion_tokens=150,
        total_tokens=250
    )

@pytest.fixture
def sample_llm_usage_dict() -> dict:
    return {
        "prompt_tokens": 100,
        "completion_tokens": 150,
        "total_tokens": 250,
    }

# ===== LLMResponse =====

@pytest.fixture
def sample_llm_response(sample_llm_usage) -> LLMResponse:
    return LLMResponse(
        text="Texto traduzido com sucesso.",
        usage=sample_llm_usage,
        raw={"example": "response"}
    )
    
@pytest.fixture
def sample_llm_response_dict(sample_llm_usage_dict) -> dict:
    return {
        "text": "Texto traduzido com sucesso.",
        "usage": sample_llm_usage_dict,
        "raw": {"example": "response"}
    }

# ===== MediaWork =====

@pytest.fixture
def sample_media_work(sample_chapter) -> MediaWork:
    return MediaWork(
        id="obra01",
        title="Urban Strengthening System",
        author="Zheng Yan",
        original_language="zh-CN",
        description="Uma obra de cultivo moderno com sistema.",
        chapters=[sample_chapter]
    )
    
@pytest.fixture
def sample_media_work_dict(sample_chapter_dict) -> dict:
    return {
        "id": "obra01",
        "title": "Urban Strengthening System",
        "author": "Zheng Yan",
        "original_language": "zh-CN",
        "description": "Uma obra de cultivo moderno com sistema.",
        "chapters": [sample_chapter_dict],
    }

# ===== Scenario =====

@pytest.fixture
def sample_scenario() -> Scenario:
    return Scenario(
        index=0,
        text="Cenário detalhado",
        location="Sala 18",
        characters=["Ye Hong", "Srta. Zhang"]
    )

@pytest.fixture
def sample_scenario_dict() -> dict:
    return {
        "index": 0,
        "text": "Cenário detalhado",
        "location": "Sala 18",
        "characters": ["Ye Hong", "Srta. Zhang"]
    }

# ===== Segment =====

@pytest.fixture
def sample_segment(sample_character: Character) -> Segment:
    return Segment(
        segment_index=0,
        line_number=1,
        text="Texto original",
        translated_text="Texto traduzido",
        segment_type=SegmentType.DIALOGUE,
        speaker_hint="Ye Hong",
        character=sample_character,
        emotion=EmotionType.JOY
    )

@pytest.fixture
def sample_segment_dict(sample_character_dict: dict) -> dict:
    return {
        "segment_index": 0,
        "line_number": 1,
        "text": "Texto original",
        "translated_text": "Texto traduzido",
        "segment_type": SegmentType.DIALOGUE,
        "speaker_hint": "Ye Hong",
        "character": sample_character_dict,
        "emotion": EmotionType.JOY
    }

# ===== VoiceProfile =====

@pytest.fixture
def sample_voice_profile() -> VoiceProfile:
    return VoiceProfile(
        id="vp01",
        name="Padrão Feminina",
        vendor="ElevenLabs",
        language="pt-BR",
        gender=GenderType.FEMALE
    )
    
@pytest.fixture
def sample_voice_profile_male() -> VoiceProfile:
    return VoiceProfile(
        id="vp02",
        name="Padrão Masculino",
        vendor="ElevenLabs",
        language="pt-BR",
        gender=GenderType.MALE
    )
    
@pytest.fixture
def sample_voice_profile_dict() -> dict:
    return {
        "id": "vp01",
        "name": "Padrão Feminina",
        "vendor": "ElevenLabs",
        "language": "pt-BR",
        "gender": GenderType.FEMALE
    }

@pytest.fixture
def sample_voice_profile_male_dict() -> dict:
    return {
        "id": "vp02",
        "name": "Padrão Masculino",
        "vendor": "ElevenLabs",
        "language": "pt-BR",
        "gender": GenderType.MALE
    }