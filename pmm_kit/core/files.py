import datetime
import shutil
import subprocess
import sys
from importlib import resources
from pathlib import Path
from typing import Optional

from rich.progress import Progress, SpinnerColumn, TextColumn

from .config import load_global_config, save_project_yaml
from .logger import console, log_error, log_info, log_step, log_success, log_warning
from .slugify import slugify


def get_package_root() -> Path:
    """Get the package root directory for accessing config and memory files.

    Works for both editable installs and packaged installs.
    """
    # Try to find the actual package location
    import pmm_kit
    package_path = Path(pmm_kit.__file__).parent

    # Check if we're in an editable install (has .git in parent directories)
    current = package_path
    for _ in range(5):  # Check up to 5 levels up
        if (current / ".git").exists():
            # Found git repo - this is an editable install
            return current
        current = current.parent

    # Not an editable install - check if config/memory are in package data directory
    if (package_path / "data" / "config").exists():
        return package_path / "data"

    # Check if config/memory are siblings to package
    if (package_path.parent / "config").exists():
        return package_path.parent

    # Otherwise assume they're in the package parent (installed location)
    return package_path.parent


def is_packaged_install(repo_root: Path) -> bool:
    """Check if this is a packaged install (vs editable/dev install)."""
    # If there's no .git directory in repo_root, it's a packaged install
    return not (repo_root / ".git").exists()


def init_project_structure(
    repo_root: Path,
    project_name: str,
    project_id: Optional[str],
    use_here: bool,
    ai_provider: Optional[str],
    init_git: bool,
    force: bool,
    project_type: str = "feature",
    output_destination: str = "markdown",
    notion_properties: Optional[dict] = None,
) -> Path:
    cfg = load_global_config(repo_root)

    if not project_id:
        project_id = slugify(project_name)

    if use_here:
        project_dir = Path.cwd()
    else:
        # For packaged installs, create projects in current working directory
        # For dev installs, create in repo_root/projects
        if is_packaged_install(repo_root):
            projects_root = Path.cwd() / "projects"
        else:
            projects_root = repo_root / "projects"

        projects_root.mkdir(exist_ok=True)
        project_dir = projects_root / project_id

    if project_dir.exists() and any(project_dir.iterdir()) and not force:
        raise RuntimeError(
            f"Directory '{project_dir}' is not empty. Use --force to initialize anyway."
        )

    project_dir.mkdir(parents=True, exist_ok=True)

    log_step("\n┌─────────────────────────────────────────────────┐")
    log_step("│  Creating project structure...                  │")
    log_step("└─────────────────────────────────────────────────┘\n")

    templates_root = repo_root / "config" / "templates"
    memory_root = repo_root / "memory"

    created_files = []

    def copy_template(template_name: str, dest_name: str) -> None:
        src = templates_root / template_name
        dest = project_dir / dest_name
        if src.exists():
            dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            created_files.append(dest_name)

    # Base files - conditional based on project type
    if project_type == "narrative":
        # Narrative projects: no commdoc (reads from linked projects)
        copy_template("narrative-README.template.md", "README_PROJECT.md")
        copy_template("linked-projects.template.md", "linked-projects.md")
        copy_template("gtm-plan.template.md", "gtm-plan.md")
        copy_template("narrative.template.md", "narrative-playbook.md")
        copy_template("success-report.template.md", "success-report.md")
    else:
        # Feature projects: full template set
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
            created_files.append(f"input/{name}")

    # Imports folder for /pmm.import workflow
    imports_dir = input_dir / "imports"
    imports_dir.mkdir(exist_ok=True)
    imports_readme = imports_dir / "README.md"
    if not imports_readme.exists():
        imports_readme.write_text(
            """# Imports Folder

Place existing marketing documents here for import into your CommDoc.

## Supported Formats

- **PDF** (.pdf) - Slide decks, presentations, reports
- **Markdown** (.md) - Existing documentation
- **HTML** (.html) - Web content, saved pages
- **Text** (.txt) - Plain text documents

## How to Use

1. Drop your existing documents into this folder
2. Run `/pmm.import` in your AI assistant
3. Review the updated `commdoc.md`
4. Check `import-log.md` for details on what was imported

## Tips

- Rename files descriptively (e.g., `q4-positioning-deck.pdf`)
- Remove duplicates before importing
- The import process will not delete your source files
""",
            encoding="utf-8",
        )
        created_files.append("input/imports/README.md")

    # Copy memory prompts to .claude/commands/ for slash command support
    claude_commands_dir = project_dir / ".claude" / "commands"
    claude_commands_dir.mkdir(parents=True, exist_ok=True)

    # Try multiple locations for memory files (handles various install scenarios)
    memory_locations = [
        memory_root,  # Standard location from get_package_root()
        Path(__file__).parent.parent / "data" / "memory",  # Relative to this file
        Path(__file__).parent.parent.parent / "memory",  # Dev install structure
    ]

    memory_files_copied = False
    for memory_location in memory_locations:
        if memory_location.exists():
            memory_files = list(memory_location.glob("pmm.*.md"))
            if memory_files:
                for memory_file in memory_files:
                    dest = claude_commands_dir / memory_file.name
                    shutil.copy2(memory_file, dest)
                    created_files.append(f".claude/commands/{memory_file.name}")
                memory_files_copied = True
                break

    # Fallback: try using importlib.resources (most reliable for package data)
    if not memory_files_copied:
        try:
            # Python 3.9+ approach
            memory_pkg = resources.files("pmm_kit.data.memory")
            for item in memory_pkg.iterdir():
                if item.name.startswith("pmm.") and item.name.endswith(".md"):
                    dest = claude_commands_dir / item.name
                    dest.write_text(item.read_text(encoding="utf-8"), encoding="utf-8")
                    created_files.append(f".claude/commands/{item.name}")
                    memory_files_copied = True
        except Exception:
            pass  # importlib.resources approach failed, will show warning below

    if not memory_files_copied:
        log_warning("Could not find slash command templates. Slash commands will not be available.")
        log_warning("You may need to reinstall pmm-kit: uv tool install pmm-kit --force --from git+https://github.com/adroual/pmm-kit.git")

    # Project YAML
    created_at = datetime.datetime.utcnow().isoformat() + "Z"
    project_data = {
        "id": project_id,
        "name": project_name,
        "type": project_type,
        "created_at": created_at,
        "ai_provider": ai_provider or cfg.get("default_ai_provider"),
        "markets": [],
        "segments": [],
        "objectives": [],
        "status": "draft",
    }
    # Add linked_projects array for narrative projects
    if project_type == "narrative":
        project_data["linked_projects"] = []

    # Add outputs config — spec types vary by project type
    output_format = output_destination
    if project_type == "narrative":
        project_data["outputs"] = {
            "narrative": {"format": output_format},
            "gtm-package": {"format": output_format},
            "success-report": {"format": output_format},
        }
    else:
        project_data["outputs"] = {
            "commdoc": {"format": output_format},
            "narrative": {"format": output_format},
            "gtm-package": {"format": output_format},
            "sales-playbook": {"format": output_format},
            "sales-enablement": {"format": output_format},
            "changelog": {"format": output_format},
            "success-report": {"format": output_format},
        }

    # Save Notion properties if provided (for /pmm.scaffold to use)
    if notion_properties:
        project_data["notion_properties"] = notion_properties

    save_project_yaml(project_dir, project_data)
    created_files.append("project.yaml")

    # Initialize git if requested
    if init_git:
        if not (project_dir / ".git").exists():
            try:
                subprocess.run(
                    ["git", "init"], cwd=str(project_dir), check=True, capture_output=True
                )
                log_success("Initialized git repository")
            except Exception as e:
                log_error(f"Could not initialize git: {e}")

        gitignore = project_dir / ".gitignore"
        if not gitignore.exists():
            gitignore.write_text(
                "# pmm-kit\n__pycache__/\n.env\n.vscode/\n.idea/\n.pmm-kit/\n",
                encoding="utf-8",
            )
            created_files.append(".gitignore")

    # Print beautiful success screen
    print_success_screen(project_name, project_dir, project_id, ai_provider, created_files, project_type, output_destination)

    return project_dir


def print_success_screen(
    project_name: str,
    project_dir: Path,
    project_id: str,
    ai_provider: Optional[str],
    created_files: list[str],
    project_type: str = "feature",
    output_destination: str = "markdown",
) -> None:
    """Print a beautiful success screen after project creation."""
    console.print("\n")
    log_success("[bold]Project created successfully![/bold]\n")

    # Project location
    console.print("[bold cyan]📁 Project location:[/bold cyan]")
    console.print(f"   [dim]{project_dir}[/dim]\n")

    # Files created
    console.print("[bold cyan]📋 Files created:[/bold cyan]")
    for f in sorted(created_files):
        log_success(f)
    console.print()

    # AI provider
    if ai_provider:
        console.print(f"[bold cyan]🤖 AI assistant:[/bold cyan] [green]{ai_provider}[/green]\n")

    # Output destination
    if output_destination in ("notion", "both"):
        label = "Notion + Local files" if output_destination == "both" else "Notion pages"
        console.print(f"[bold cyan]📤 Output destination:[/bold cyan] [green]{label}[/green]")
        notion_yaml_path = Path(__file__).parent.parent.parent / "config" / "notion.yaml"
        if not notion_yaml_path.exists():
            console.print("[dim]   You'll need your Notion database URL for setup.[/dim]")
        console.print("[yellow]   → Run /pmm.scaffold in Claude Code to create your Notion pages[/yellow]\n")
    else:
        console.print("[bold cyan]📤 Output destination:[/bold cyan] [green]Local Markdown files[/green]\n")

    # Project type indicator
    if project_type == "narrative":
        console.print("[bold magenta]📚 Project type:[/bold magenta] [magenta]Narrative Bundle[/magenta]\n")

    # Next steps
    console.print("[bold yellow]🚀 Next steps:[/bold yellow]\n")
    console.print(f"   [bold]1.[/bold] cd {project_id if project_id else project_dir}")
    console.print("   ")
    console.print("   [bold]2.[/bold] Open this folder in Claude Code:")
    console.print("      [dim]claude-code .[/dim]")
    console.print("   ")

    if project_type == "narrative":
        # Narrative project workflow
        console.print("   [bold]3.[/bold] Available slash commands:")
        console.print("\n      [bold]Narrative workflow:[/bold]")
        console.print("      [cyan]/pmm.link[/cyan]            - Link a feature project")
        console.print("      [cyan]/pmm.sync[/cyan]            - Sync content from linked projects")
        console.print("      [cyan]/pmm.narrative[/cyan]       - Build unified narrative")
        console.print("\n      [bold]Supporting commands:[/bold]")
        console.print("      [cyan]/pmm.constitution[/cyan]   - Define brand voice & strategy")
        console.print("      [cyan]/pmm.research[/cyan]       - Synthesize research insights")
        console.print("      [cyan]/pmm.gtm[/cyan]            - Generate consolidated GTM plan")
        console.print("      [cyan]/pmm.success-report[/cyan] - Post-launch report\n")

        console.print("[bold green]💡 Recommended workflow:[/bold green]")
        console.print("   [dim]1. Start with[/dim] [cyan]/pmm.constitution[/cyan] [dim]to establish brand voice[/dim]")
        console.print("   [dim]2. Run[/dim] [cyan]/pmm.link ../project-a[/cyan] [dim]to link feature projects[/dim]")
        console.print("   [dim]3. Run[/dim] [cyan]/pmm.sync[/cyan] [dim]to pull content from linked projects[/dim]")
        console.print("   [dim]4. Run[/dim] [cyan]/pmm.narrative[/cyan] [dim]to create unified story[/dim]\n")
    else:
        # Feature project workflow (default)
        console.print("   [bold]3.[/bold] Available slash commands:")
        console.print("\n      [bold]Workflow orchestration:[/bold]")
        console.print("      [cyan]/pmm.plan[/cyan]           - Create strategic plan")
        console.print("      [cyan]/pmm.tasks[/cyan]          - Generate actionable task list")
        console.print("      [cyan]/pmm.execute[/cyan]        - Execute tasks interactively")
        console.print("\n      [bold]Core documents:[/bold]")
        console.print("      [cyan]/pmm.constitution[/cyan]   - Define brand voice & strategy")
        console.print("      [cyan]/pmm.research[/cyan]       - Synthesize research insights")
        console.print("      [cyan]/pmm.commdoc[/cyan]        - Create launch CommDoc")
        console.print("      [cyan]/pmm.import[/cyan]         - Import existing documents")
        console.print("      [cyan]/pmm.gtm[/cyan]            - Generate GTM plan")
        console.print("      [cyan]/pmm.narrative[/cyan]      - Build narrative playbook")
        console.print("\n      [bold]Enablement & launch:[/bold]")
        console.print("      [cyan]/pmm.sales-playbook[/cyan]    - Sales battlecard")
        console.print("      [cyan]/pmm.sales-enablement[/cyan]  - Sales enablement")
        console.print("      [cyan]/pmm.changelog[/cyan]         - Customer changelog")
        console.print("      [cyan]/pmm.success-report[/cyan]    - Post-launch report\n")

        console.print("[bold green]💡 Recommended workflow:[/bold green]")
        console.print("   [dim]1. Start with[/dim] [cyan]/pmm.constitution[/cyan] [dim]to establish brand voice[/dim]")
        console.print("   [dim]2. Run[/dim] [cyan]/pmm.plan[/cyan] [dim]to define your strategic approach[/dim]")
        console.print("   [dim]3. Run[/dim] [cyan]/pmm.tasks[/cyan] [dim]to generate your task list[/dim]")
        console.print("   [dim]4. Run[/dim] [cyan]/pmm.execute[/cyan] [dim]to execute tasks interactively[/dim]\n")
        console.print("   [bold yellow]Or[/bold yellow] [dim]run commands manually:[/dim] [cyan]/pmm.research[/cyan] [dim]→[/dim] [cyan]/pmm.commdoc[/cyan] [dim]→[/dim] [cyan]/pmm.gtm[/cyan]\n")

    console.print("[dim]───────────────────────────────────────────────────[/dim]")
    console.print("[bold green]Happy shipping! 🎉[/bold green]\n")


def check_environment(repo_root: Path) -> None:
    """Check the development environment."""
    log_step("\n┌─────────────────────────────────────────────────┐")
    log_step("│  Environment Check                              │")
    log_step("└─────────────────────────────────────────────────┘\n")

    # Git
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        log_success("git is installed")
    except Exception:
        log_error("git is not available on PATH")

    # Config
    cfg_path = repo_root / "config" / "pmm.config.yaml"
    if cfg_path.exists():
        log_success(f"Found config at {cfg_path}")
    else:
        log_warning("No config/pmm.config.yaml found, using defaults")

    # Optional: check for common AI CLIs
    console.print("\n[bold cyan]AI CLI Detection (optional):[/bold cyan]")
    for cmd in ["claude", "gemini", "codex", "opencode", "cursor", "copilot"]:
        try:
            subprocess.run([cmd, "--help"], check=True, capture_output=True)
            log_success(f"{cmd} CLI detected")
        except Exception:
            log_info(f"{cmd} CLI not detected")

    console.print("\n")
    log_success("[bold]Environment check complete![/bold]\n")


def install_global_commands() -> None:
    """Install PMM slash commands globally to ~/.claude/commands/."""
    log_step("\n┌─────────────────────────────────────────────────┐")
    log_step("│  Installing Global Slash Commands               │")
    log_step("└─────────────────────────────────────────────────┘\n")

    # Determine global commands directory
    global_commands_dir = Path.home() / ".claude" / "commands"
    global_commands_dir.mkdir(parents=True, exist_ok=True)

    console.print(f"[bold cyan]📁 Target directory:[/bold cyan] {global_commands_dir}\n")

    # Find memory files using multiple fallback methods
    memory_locations = [
        Path(__file__).parent.parent / "data" / "memory",  # Package data location
        get_package_root() / "memory",  # From get_package_root
        Path(__file__).parent.parent.parent / "memory",  # Dev install structure
    ]

    memory_files = []
    source_location = None
    for memory_location in memory_locations:
        if memory_location.exists():
            files = list(memory_location.glob("pmm.*.md"))
            if files:
                memory_files = files
                source_location = memory_location
                break

    # Fallback: try importlib.resources
    if not memory_files:
        try:
            memory_pkg = resources.files("pmm_kit.data.memory")
            temp_files = []
            for item in memory_pkg.iterdir():
                if item.name.startswith("pmm.") and item.name.endswith(".md"):
                    temp_files.append(item)
            if temp_files:
                # Copy from resources
                console.print("[dim]Using importlib.resources...[/dim]\n")
                for item in temp_files:
                    dest = global_commands_dir / item.name
                    dest.write_text(item.read_text(encoding="utf-8"), encoding="utf-8")
                    log_success(f"Installed {item.name}")
                console.print()
                log_success(f"[bold]Installed {len(temp_files)} slash commands globally![/bold]")
                console.print("\n[bold green]✓ PMM commands are now available in all Claude Code projects.[/bold green]")
                console.print("[dim]Try typing /pmm. in Claude Code to see available commands.[/dim]\n")
                return
        except Exception:
            pass

    if not memory_files:
        log_error("Could not find slash command templates!")
        log_warning("Try reinstalling pmm-kit:")
        console.print("  uv cache clean")
        console.print("  uv tool install pmm-kit --force --from git+https://github.com/adroual/pmm-kit.git\n")
        return

    # Copy files to global directory
    console.print(f"[dim]Source: {source_location}[/dim]\n")
    for memory_file in sorted(memory_files):
        dest = global_commands_dir / memory_file.name
        shutil.copy2(memory_file, dest)
        log_success(f"Installed {memory_file.name}")

    console.print()
    log_success(f"[bold]Installed {len(memory_files)} slash commands globally![/bold]")
    console.print("\n[bold green]✓ PMM commands are now available in all Claude Code projects.[/bold green]")
    console.print("[dim]Try typing /pmm. in Claude Code to see available commands.[/dim]\n")
