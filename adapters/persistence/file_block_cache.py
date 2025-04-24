import json
from pathlib import Path
from typing import List, Dict, Any, Optional

from core.interfaces.repository import IBlockCache


class FileBlockCache(IBlockCache):
    """
    Persiste cada chunk de resposta LLM em
    data/store/{work_id}/blocks/{chapter_id}/block_{i}.json
    """

    def __init__(self, store_dir: Path):
        self.store_dir = store_dir / "blocks"

    def _path_for(
        self,
        work_id: str,
        chapter_id: str,
        block_index: int
    ) -> Path:
        return self.store_dir / work_id / chapter_id / f"block_{block_index}.json"

    def load_block(
        self,
        work_id: str,
        chapter_id: str,
        block_index: int
    ) -> Optional[List[Dict[str, Any]]]:
        p = self._path_for(work_id, chapter_id, block_index)
        if not p.exists():
            return None
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None

    def save_block(
        self,
        work_id: str,
        chapter_id: str,
        block_index: int,
        data: List[Dict[str, Any]]
    ) -> None:
        p = self._path_for(work_id, chapter_id, block_index)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
