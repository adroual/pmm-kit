import datetime
import subprocess
from pathlib import Path
from typing import Optional

from .config import load_global_config, save_project_yaml
from .logger import log_error, log_info
from .slugify import slugify


def init_project_structure(
    repo_root: Path,
    project_name: str,
    project_id: Optional[str],
    use_here: bool,
    ai_provider: Optional[str],
    init_git: bool,
    force: bool,
) -> Path:
    cfg = load_global_config(repo_root)

    if not project_id:
        project_id = slugify(project_name)

    if use_here:
        project_dir = Path.cwd()
    else:
        projects_root = repo_root / "projects"
        projects_root.mkdir(exist_ok=True)
        project_dir = projects_root / project_id

    if project_dir.exists() and any(project_dir.iterdir()) and not force:
        raise RuntimeError(
            f"Directory '{project_dir}' is not empty. Use --force to initialize anyway."
        )

    project_dir.mkdir(parents=True, exist_ok=True)

    templates_root = repo_root / "config" / "templates"

    def copy_template(template_name: str, dest_name: str) -> None:
        src = templates_root / template_name
        dest = project_dir / dest_name
        if src.exists():
            dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    # Base files
    copy_template("README_PROJECT.template.md", "README_PROJECT.md")
    copy_template("commdoc.template.md", "commdoc.md")
    copy_template("gtm-plan.template.md", "gtm-plan.md")
    copy_template("narrative.template.md", "narrative-playbook.md")
    copy_template("sales-playbook.template.md", "sales-playbook.md")
    copy_template("sales-enablement.template.md", "sales-enablement.md")
    copy_template("success-report.template.md", "success-report.md")
    copy_template("changelog.template.md", "changelog.md")

    # Input folder
    input_dir = project_dir / "input"
    input_dir.mkdir(exist_ok=True)
    for name in ["notes.md", "research.md", "competitors.md"]:
        p = input_dir / name
        if not p.exists():
            p.write_text(f"# {name.replace('.md', '').title()}\n\n", encoding="utf-8")

    # Project YAML
    created_at = datetime.datetime.utcnow().isoformat() + "Z"
    project_data = {
        "id": project_id,
        "name": project_name,
        "created_at": created_at,
        "ai_provider": ai_provider or cfg.get("default_ai_provider"),
        "markets": [],
        "segments": [],
        "objectives": [],
        "status": "draft",
    }
    save_project_yaml(project_dir, project_data)

    # Initialize git if requested
    if init_git:
        if not (project_dir / ".git").exists():
            try:
                subprocess.run(["git", "init"], cwd=str(project_dir), check=True)
                log_info("Initialized git repository.")
            except Exception as e:
                log_error(f"Could not initialize git: {e}")

        gitignore = project_dir / ".gitignore"
        if not gitignore.exists():
            gitignore.write_text(
                "# pmm-kit\n__pycache__/\n.env\n.vscode/\n.idea/\n",
                encoding="utf-8",
            )

    log_info(f"Project '{project_name}' created at {project_dir}")
    log_info(
        "Next steps:\n"
        f"  1. cd {project_dir}\n"
        "  2. Open this folder in your AI agent (Claude Code, Gemini, etc.)\n"
        "  3. Run /pmm.constitution then /pmm.commdoc to bootstrap your CommDoc."
    )
    return project_dir


def check_environment(repo_root: Path) -> None:
    log_info("Checking environment...")

    # Git
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        log_info("✔ git is installed.")
    except Exception:
        log_error("✘ git is not available on PATH.")

    # Config
    cfg_path = repo_root / "config" / "pmm.config.yaml"
    if cfg_path.exists():
        log_info(f"✔ Found config at {cfg_path}")
    else:
        log_info("ℹ No config/pmm.config.yaml found, using defaults.")

    # Optional: check for common AI CLIs
    for cmd in ["claude", "gemini", "codex", "opencode", "cursor", "copilot"]:
        try:
            subprocess.run([cmd, "--help"], check=True, capture_output=True)
            log_info(f"✔ {cmd} CLI detected.")
        except Exception:
            log_info(f"ℹ {cmd} CLI not detected (optional).")

    log_info("Done.")
