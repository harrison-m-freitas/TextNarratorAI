import json
from pathlib import Path
from typing import Dict, Any

from core.interfaces.repository import IManifestAdapter


class FileManifestAdapter(IManifestAdapter):
    """
    Persiste o manifest em data/store/{work_id}/manifest.json
    """

    def __init__(self, store_dir: Path):
        self.store_dir = store_dir

    def _path_for(self, work_id: str) -> Path:
        return self.store_dir / work_id / "manifest.json"

    def load(self, work_id: str) -> Dict[str, Any]:
        p = self._path_for(work_id)
        if not p.exists():
            return {"chapters": {}}
        raw = p.read_text(encoding="utf-8")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return {"chapters": {}}
        return {"chapters": data.get("chapters", {})}

    def save(self, work_id: str, manifest: Dict[str, Any]) -> None:
        p = self._path_for(work_id)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
