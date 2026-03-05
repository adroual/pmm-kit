from pathlib import Path
from typing import Any, Dict

import yaml

DEFAULT_CONFIG = {
    "default_ai_provider": None,
}


def load_global_config(repo_root: Path) -> Dict[str, Any]:
    cfg_path = repo_root / "config" / "pmm.config.yaml"
    if not cfg_path.exists():
        return DEFAULT_CONFIG.copy()
    with cfg_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    merged = DEFAULT_CONFIG.copy()
    merged.update(data)
    return merged


def load_project_yaml(project_dir: Path) -> Dict[str, Any]:
    yaml_path = project_dir / "project.yaml"
    if not yaml_path.exists():
        return {}
    with yaml_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def save_project_yaml(project_dir: Path, project_data: Dict[str, Any]) -> None:
    yaml_path = project_dir / "project.yaml"
    with yaml_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(project_data, f, sort_keys=False, allow_unicode=True)
