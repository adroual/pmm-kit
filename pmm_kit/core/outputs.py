import re
from pathlib import Path
from typing import Any, Dict

from .config import load_project_yaml


def notion_url_to_page_id(url: str) -> str:
    """Extract Notion page ID from URL and format as UUID (8-4-4-4-12).

    The page ID is the last 32 hex characters in the URL path (ignoring dashes).
    """
    # Strip query params and fragment
    path = url.split("?")[0].split("#")[0].rstrip("/")
    # Extract last 32 hex chars (may contain dashes)
    raw = path.split("/")[-1].split("-")[-1] if "-" in path.split("/")[-1] else path.split("/")[-1]
    # Remove any remaining dashes and take last 32 hex chars
    hex_chars = re.sub(r"[^0-9a-fA-F]", "", raw)
    if len(hex_chars) < 32:
        # Try extracting from entire last path segment
        last_segment = path.split("/")[-1]
        hex_chars = re.sub(r"[^0-9a-fA-F]", "", last_segment)

    if len(hex_chars) < 32:
        raise ValueError(f"Could not extract 32 hex chars from URL: {url}")

    h = hex_chars[-32:]
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"


def stage_for_publish(project_dir: Path, spec_type: str, content: str) -> Path:
    """Write content to .pmm-kit/publish/<spec-type>.md for Notion publishing."""
    publish_dir = project_dir / ".pmm-kit" / "publish"
    publish_dir.mkdir(parents=True, exist_ok=True)
    out = publish_dir / f"{spec_type}.md"
    out.write_text(content, encoding="utf-8")
    return out


def get_output_config(project_dir: Path, spec_type: str) -> Dict[str, Any]:
    """Return output config for a spec type from project.yaml.

    Defaults to {"format": "markdown"} if not configured.
    """
    data = load_project_yaml(project_dir)
    outputs = data.get("outputs", {})
    return outputs.get(spec_type, {"format": "markdown"})
