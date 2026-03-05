import argparse
import subprocess
import sys
from pathlib import Path
from typing import Optional

import questionary

import yaml

from pmm_kit.core.banner import print_banner, print_divider
from pmm_kit.core.files import check_environment, get_package_root, init_project_structure, install_global_commands
from pmm_kit.core.logger import console, log_error, log_info, log_step, log_success, log_warning
from pmm_kit.core.update import check_for_updates


def is_first_run() -> bool:
    """Check if this is the first time running pmm-kit (no global commands installed)."""
    global_commands_dir = Path.home() / ".claude" / "commands"
    if not global_commands_dir.exists():
        return True
    pmm_commands = list(global_commands_dir.glob("pmm.*.md"))
    return len(pmm_commands) == 0


def run_onboarding() -> None:
    """Run the first-time user onboarding flow."""
    print_banner()

    console.print("\n[bold green]🎉 Welcome to PMM-Kit![/bold green]")
    console.print("[dim]The AI-powered Product Marketing workspace[/dim]\n")

    print_divider()

    console.print("\n[bold cyan]Let's get you set up in 2 quick steps:[/bold cyan]\n")

    # Step 1: Install commands
    console.print("[bold]Step 1 of 2:[/bold] Install slash commands for Claude Code\n")
    console.print("[dim]This makes /pmm.* commands available in all your projects.[/dim]\n")

    proceed = questionary.confirm(
        "Install PMM slash commands now?",
        default=True,
        style=questionary.Style([
            ('question', 'fg:cyan bold'),
            ('pointer', 'fg:cyan bold'),
        ])
    ).ask()

    if proceed:
        console.print()
        install_global_commands()
    else:
        console.print()
        log_info("Skipped. You can run [bold]pmm install-commands[/bold] later.\n")

    # Step 2: Create first project
    print_divider()
    console.print("\n[bold]Step 2 of 2:[/bold] Create your first PMM project\n")

    create_project = questionary.confirm(
        "Create a new project now?",
        default=True,
        style=questionary.Style([
            ('question', 'fg:cyan bold'),
            ('pointer', 'fg:cyan bold'),
        ])
    ).ask()

    if create_project:
        console.print()
        project_name = questionary.text(
            "Project name:",
            style=questionary.Style([
                ('question', 'fg:cyan bold'),
            ])
        ).ask()

        if project_name and project_name.strip():
            console.print()
            ai_provider = choose_ai_provider()
            output_destination = choose_output_destination()

            notion_properties = None
            if output_destination in ("notion", "both"):
                repo_root = get_package_root()
                notion_properties = prompt_notion_properties(repo_root)
                if notion_properties is None:
                    console.print("[dim]No saved Notion mapping found. Run /pmm.scaffold in Claude Code.[/dim]\n")

            try:
                repo_root = get_package_root()
                project_dir = init_project_structure(
                    repo_root=repo_root,
                    project_name=project_name.strip(),
                    project_id=None,
                    use_here=False,
                    ai_provider=ai_provider,
                    init_git=True,
                    force=False,
                    project_type="feature",
                    output_destination=output_destination,
                    notion_properties=notion_properties,
                )

                # Auto-open Claude Code if claude was selected
                if ai_provider == "claude" and project_dir:
                    console.print("[bold cyan]🚀 Opening Claude Code...[/bold cyan]\n")
                    try:
                        subprocess.run(["claude", str(project_dir)], check=False)
                    except FileNotFoundError:
                        log_warning("Claude Code CLI not found. Install it from: https://claude.ai/code")
                        log_info(f"You can manually open the project: claude {project_dir}")
            except Exception as e:
                log_error(f"Error creating project: {e}")
        else:
            log_info("No project name provided. Skipping project creation.\n")
    else:
        console.print()
        log_info("You can create a project anytime with: [bold]pmm init \"Project Name\"[/bold]\n")

    # Final message
    print_divider()
    console.print("\n[bold green]✓ Setup complete![/bold green]")
    console.print("\n[bold cyan]Quick reference:[/bold cyan]")
    console.print("  [bold]pmm init[/bold] \"Name\"     Create a new project")
    console.print("  [bold]pmm help[/bold]            Show all commands")
    console.print("  [bold]/pmm.constitution[/bold]   Start with brand voice (in Claude Code)")
    console.print("  [bold]/pmm.commdoc[/bold]        Create your CommDoc (in Claude Code)\n")


def print_help_screen() -> None:
    """Print comprehensive help information."""
    log_step("\n┌─────────────────────────────────────────────────┐")
    log_step("│  PMM-Kit Help                                   │")
    log_step("└─────────────────────────────────────────────────┘\n")

    console.print("[bold cyan]COMMANDS:[/bold cyan]\n")

    console.print("[bold]pmm init[/bold] \"Project Name\"")
    console.print("  Initialize a new PMM project workspace")
    console.print("  [dim]Options:[/dim]")
    console.print("    [cyan]--id[/cyan] ID           Custom project ID/slug")
    console.print("    [cyan]--ai[/cyan] PROVIDER     AI provider (claude, gemini, copilot, cursor)")
    console.print("    [cyan]--here[/cyan]            Use current directory")
    console.print("    [cyan]--no-git[/cyan]          Skip git initialization")
    console.print("    [cyan]--force[/cyan]           Initialize in non-empty directory")
    console.print("    [cyan]--type[/cyan] TYPE       Project type: feature (default) or narrative")
    console.print("    [cyan]--output[/cyan] DEST     Output: markdown (default), notion, or both\n")

    console.print("[bold]pmm check[/bold]")
    console.print("  Check environment and dependencies\n")

    console.print("[bold]pmm update[/bold]")
    console.print("  Check for updates and install latest version\n")

    console.print("[bold]pmm install-commands[/bold]")
    console.print("  Install PMM slash commands globally for Claude Code")
    console.print("  [dim](Makes /pmm.* commands available in ALL projects)[/dim]\n")

    console.print("[bold]pmm setup[/bold]")
    console.print("  Run the interactive setup wizard\n")

    console.print("[bold]pmm help[/bold]")
    console.print("  Show this help message\n")

    print_divider()

    console.print("\n[bold cyan]SLASH COMMANDS (use inside project with AI assistant):[/bold cyan]\n")

    console.print("  [bold]Workflow orchestration:[/bold]")
    workflow_commands = [
        ("/pmm.plan", "Create strategic plan with launch scope and success criteria"),
        ("/pmm.tasks", "Generate phased task list from strategic plan"),
        ("/pmm.execute", "Execute tasks interactively with dependency checking"),
    ]
    for cmd, desc in workflow_commands:
        console.print(f"  [cyan]{cmd:<24}[/cyan] {desc}")

    console.print("\n  [bold]Core documents:[/bold]")
    core_commands = [
        ("/pmm.constitution", "Define brand voice, strategy, and guidelines"),
        ("/pmm.research", "Synthesize research into insights and assumptions"),
        ("/pmm.commdoc", "Create comprehensive launch communication document"),
        ("/pmm.import", "Import existing docs into CommDoc"),
        ("/pmm.gtm", "Generate go-to-market plan from CommDoc"),
        ("/pmm.narrative", "Build narrative playbook with story arc"),
    ]
    for cmd, desc in core_commands:
        console.print(f"  [cyan]{cmd:<24}[/cyan] {desc}")

    console.print("\n  [bold]Enablement & launch:[/bold]")
    enablement_commands = [
        ("/pmm.sales-playbook", "Create sales battlecard and talk tracks"),
        ("/pmm.sales-enablement", "Generate sales enablement materials"),
        ("/pmm.changelog", "Customer-facing changelog entries"),
        ("/pmm.success-report", "Post-launch retrospective and results"),
    ]
    for cmd, desc in enablement_commands:
        console.print(f"  [cyan]{cmd:<24}[/cyan] {desc}")

    console.print("\n  [bold]Notion integration:[/bold]")
    notion_commands = [
        ("/pmm.scaffold", "Create Notion pages and wire URLs into project config"),
        ("/pmm.publish", "Publish specs to Notion pages via MCP"),
    ]
    for cmd, desc in notion_commands:
        console.print(f"  [cyan]{cmd:<24}[/cyan] {desc}")

    console.print("\n  [bold]Narrative project commands:[/bold]")
    narrative_commands = [
        ("/pmm.link", "Link a feature project to narrative bundle"),
        ("/pmm.sync", "Sync content from linked projects"),
    ]
    for cmd, desc in narrative_commands:
        console.print(f"  [cyan]{cmd:<24}[/cyan] {desc}")

    console.print("\n")
    print_divider()

    console.print("\n[bold cyan]WORKFLOW:[/bold cyan]\n")
    console.print("  1. [bold]pmm init[/bold] \"Your Project Name\"")
    console.print("  2. [bold]cd[/bold] your-project-name")
    console.print("  3. [bold]claude .[/bold]  (or open in your AI IDE)")
    console.print("  4. Start with [cyan]/pmm.constitution[/cyan]")
    console.print("  5. Run [cyan]/pmm.plan[/cyan] → [cyan]/pmm.tasks[/cyan] → [cyan]/pmm.execute[/cyan]")
    console.print("     [dim]Or run commands manually: /pmm.research → /pmm.commdoc → /pmm.gtm[/dim]\n")

    print_divider()
    console.print()


def choose_output_destination() -> str:
    """Interactive output destination selection."""
    log_step("\n┌─────────────────────────────────────────────────┐")
    log_step("│  Where should your specs live?                  │")
    log_step("└─────────────────────────────────────────────────┘\n")

    choices = [
        "markdown  (Local files only) - Default",
        "notion    (Notion pages via MCP)",
        "both      (Local files + Notion)",
    ]

    answer = questionary.select(
        "Select output destination:",
        choices=choices,
        default=choices[0],
        style=questionary.Style([
            ('question', 'fg:cyan bold'),
            ('pointer', 'fg:cyan bold'),
            ('highlighted', 'fg:cyan bold'),
        ])
    ).ask()

    if answer is None:
        sys.exit(1)

    destination = answer.split()[0]
    console.print()
    log_success(f"Selected: {destination}\n")
    return destination


def prompt_notion_properties(repo_root: Path) -> Optional[dict]:
    """Ask for project-specific Notion properties from saved mapping.

    Returns property values dict, or None if no notion.yaml exists.
    """
    notion_yaml_path = repo_root / "config" / "notion.yaml"
    if not notion_yaml_path.exists():
        return None

    try:
        with notion_yaml_path.open("r", encoding="utf-8") as f:
            notion_config = yaml.safe_load(f) or {}
    except Exception:
        return None

    notion = notion_config.get("notion", {})
    property_mapping = notion.get("property_mapping", {})
    prompt_props = property_mapping.get("prompt", [])

    if not prompt_props:
        return None

    log_step("\n┌─────────────────────────────────────────────────┐")
    log_step("│  Notion Project Properties                      │")
    log_step("└─────────────────────────────────────────────────┘\n")

    console.print("[dim]These values will be used when creating your Notion pages.[/dim]\n")

    values = {}
    for prop in prompt_props:
        prop_name = prop.get("property", "")
        prop_type = prop.get("type", "text")
        options = prop.get("options", [])

        if prop_type in ("select",) and options:
            answer = questionary.select(
                f"{prop_name}:",
                choices=options,
                style=questionary.Style([
                    ('question', 'fg:cyan bold'),
                    ('pointer', 'fg:cyan bold'),
                    ('highlighted', 'fg:cyan bold'),
                ])
            ).ask()
            if answer is None:
                sys.exit(1)
            values[prop_name] = answer
        elif prop_type in ("multi_select",) and options:
            answer = questionary.checkbox(
                f"{prop_name}:",
                choices=options,
                style=questionary.Style([
                    ('question', 'fg:cyan bold'),
                    ('pointer', 'fg:cyan bold'),
                    ('highlighted', 'fg:cyan bold'),
                ])
            ).ask()
            if answer is None:
                sys.exit(1)
            values[prop_name] = answer
        elif prop_type == "date":
            answer = questionary.text(
                f"{prop_name} (YYYY-MM-DD):",
                style=questionary.Style([
                    ('question', 'fg:cyan bold'),
                ])
            ).ask()
            if answer is None:
                sys.exit(1)
            values[prop_name] = answer if answer.strip() else None
        else:
            answer = questionary.text(
                f"{prop_name}:",
                style=questionary.Style([
                    ('question', 'fg:cyan bold'),
                ])
            ).ask()
            if answer is None:
                sys.exit(1)
            values[prop_name] = answer if answer.strip() else None

    console.print()
    log_success("Notion properties saved.\n")
    return values


def choose_ai_provider(default: Optional[str] = None) -> Optional[str]:
    """Interactive AI provider selection with beautiful formatting."""
    log_step("\n┌─────────────────────────────────────────────────┐")
    log_step("│  Choose AI Assistant                            │")
    log_step("└─────────────────────────────────────────────────┘\n")

    choices = [
        "claude   (Claude Code) - Recommended",
        "copilot  (GitHub Copilot)",
        "gemini   (Gemini CLI)",
        "cursor   (Cursor)",
        "opencode (OpenCode)",
        "openai   (OpenAI / codex-style)",
        "none     (I will configure later)",
    ]
    if default:
        # best-effort preselect
        for c in choices:
            if c.startswith(default):
                default_choice = c
                break
        else:
            default_choice = None
    else:
        default_choice = None

    answer = questionary.select(
        "Select your preferred AI coding assistant:",
        choices=choices,
        default=default_choice,
        style=questionary.Style([
            ('question', 'fg:cyan bold'),
            ('pointer', 'fg:cyan bold'),
            ('highlighted', 'fg:cyan bold'),
        ])
    ).ask()

    if not answer or answer.startswith("none"):
        console.print()
        log_info("No AI assistant selected. You can configure this later.\n")
        return None

    provider = answer.split()[0]  # first token is the id
    console.print()
    log_success(f"Selected: {provider}\n")
    return provider


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="pmm",
        description="pmm-kit — Spec-driven Product Marketing CLI",
    )
    subparsers = parser.add_subparsers(dest="command", required=False)

    # init
    init_parser = subparsers.add_parser("init", help="Initialize a new PMM project")
    init_parser.add_argument("name", help="Project name, e.g. 'Tap to Pay — Employee Access'")
    init_parser.add_argument("--id", dest="project_id", help="Optional project ID/slug")
    init_parser.add_argument(
        "--here", action="store_true", help="Use current directory instead of creating a new folder"
    )
    init_parser.add_argument(
        "--ai",
        dest="ai_provider",
        help="AI provider (claude, gemini, copilot, cursor, opencode, openai). "
             "If omitted, an interactive selector will be shown.",
    )
    init_parser.add_argument(
        "--no-git", action="store_true", help="Do not initialize a git repository in the project directory"
    )
    init_parser.add_argument(
        "--force",
        action="store_true",
        help="Allow initializing in a non-empty directory",
    )
    init_parser.add_argument(
        "--type",
        dest="project_type",
        choices=["feature", "narrative"],
        default="feature",
        help="Project type: 'feature' (default) for single launches, 'narrative' for bundling multiple features",
    )
    init_parser.add_argument(
        "--output",
        dest="output_destination",
        choices=["markdown", "notion", "both"],
        default=None,
        help="Output destination: 'markdown' (default), 'notion' (Notion pages via MCP), or 'both'",
    )

    # check
    subparsers.add_parser("check", help="Check environment (git, config, optional AI CLIs)")

    # update
    subparsers.add_parser("update", help="Check for updates and install latest version")

    # install-commands
    subparsers.add_parser("install-commands", help="Install PMM slash commands globally for Claude Code")

    # setup
    subparsers.add_parser("setup", help="Run the interactive setup wizard")

    # help
    subparsers.add_parser("help", help="Show detailed help and available slash commands")

    args = parser.parse_args()

    # No command provided - check if first run or show help
    if args.command is None:
        if is_first_run():
            run_onboarding()
        else:
            print_banner()
            console.print("[dim]Run [bold]pmm help[/bold] for available commands or [bold]pmm init \"Name\"[/bold] to start a project.[/dim]\n")
        return

    if args.command == "setup":
        run_onboarding()
        return

    if args.command == "init":
        print_banner()

        log_step("┌─────────────────────────────────────────────────┐")
        log_step("│  Initializing New Project                       │")
        log_step("└─────────────────────────────────────────────────┘\n")

        console.print(f"[bold cyan]→[/bold cyan] Project name: [bold]{args.name}[/bold]")
        if args.project_id:
            console.print(f"[bold cyan]→[/bold cyan] Project ID: [bold]{args.project_id}[/bold]")
        if args.project_type != "feature":
            console.print(f"[bold cyan]→[/bold cyan] Project type: [bold]{args.project_type}[/bold]")
        if args.output_destination:
            console.print(f"[bold cyan]→[/bold cyan] Output: [bold]{args.output_destination}[/bold]")
        console.print()

        ai_provider = args.ai_provider
        if not ai_provider:
            ai_provider = choose_ai_provider()

        output_destination = args.output_destination
        if not output_destination:
            output_destination = choose_output_destination()

        # If Notion output selected and notion.yaml exists, prompt for properties
        notion_properties = None
        if output_destination in ("notion", "both"):
            repo_root = get_package_root()
            notion_properties = prompt_notion_properties(repo_root)
            if notion_properties is None:
                console.print("[dim]No saved Notion mapping found (config/notion.yaml).[/dim]")
                console.print("[dim]Run /pmm.scaffold in Claude Code to set up your Notion database.[/dim]\n")

        try:
            repo_root = get_package_root()
            project_dir = init_project_structure(
                repo_root=repo_root,
                project_name=args.name,
                project_id=args.project_id,
                use_here=args.here,
                ai_provider=ai_provider,
                init_git=not args.no_git,
                force=args.force,
                project_type=args.project_type,
                output_destination=output_destination,
                notion_properties=notion_properties,
            )

            # Auto-open Claude Code if claude was selected
            if ai_provider == "claude" and project_dir:
                console.print("[bold cyan]🚀 Opening Claude Code...[/bold cyan]\n")
                try:
                    subprocess.run(["claude", str(project_dir)], check=False)
                except FileNotFoundError:
                    log_warning("Claude Code CLI not found. Install it from: https://claude.ai/code")
                    log_info(f"You can manually open the project: claude {project_dir}")
        except Exception as e:
            console.print()
            log_error(f"Error during init: {e}")
            console.print()
    elif args.command == "check":
        print_banner()
        repo_root = get_package_root()
        check_environment(repo_root)
    elif args.command == "update":
        print_banner()
        repo_root = get_package_root()
        check_for_updates(repo_root)
    elif args.command == "install-commands":
        print_banner()
        install_global_commands()
    elif args.command == "help":
        print_banner()
        print_help_screen()
