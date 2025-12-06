import argparse
from pathlib import Path
from typing import Optional

import questionary

from pmm_kit.core.banner import print_banner, print_divider
from pmm_kit.core.files import check_environment, init_project_structure
from pmm_kit.core.logger import console, log_error, log_info, log_step, log_success
from pmm_kit.core.update import check_for_updates


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
    console.print("    [cyan]--force[/cyan]           Initialize in non-empty directory\n")

    console.print("[bold]pmm check[/bold]")
    console.print("  Check environment and dependencies\n")

    console.print("[bold]pmm update[/bold]")
    console.print("  Check for updates and install latest version\n")

    console.print("[bold]pmm help[/bold]")
    console.print("  Show this help message\n")

    print_divider()

    console.print("\n[bold cyan]SLASH COMMANDS (use inside project with AI assistant):[/bold cyan]\n")

    commands = [
        ("/pmm.constitution", "Define brand voice, strategy, and guidelines"),
        ("/pmm.research", "Synthesize research into insights and assumptions"),
        ("/pmm.commdoc", "Create comprehensive launch communication document"),
        ("/pmm.gtm", "Generate go-to-market plan from CommDoc"),
        ("/pmm.narrative", "Build narrative playbook with story arc"),
        ("/pmm.sales-playbook", "Create sales battlecard and talk tracks"),
        ("/pmm.sales-enablement", "Generate sales enablement materials"),
        ("/pmm.success-report", "Post-launch retrospective and results"),
        ("/pmm.changelog", "Customer-facing changelog entries"),
    ]

    for cmd, desc in commands:
        console.print(f"  [cyan]{cmd:<22}[/cyan] {desc}")

    console.print("\n")
    print_divider()

    console.print("\n[bold cyan]WORKFLOW:[/bold cyan]\n")
    console.print("  1. [bold]pmm init[/bold] \"Your Project Name\"")
    console.print("  2. [bold]cd[/bold] your-project-name")
    console.print("  3. [bold]claude-code .[/bold]  (or open in your AI IDE)")
    console.print("  4. Start with [cyan]/pmm.constitution[/cyan]")
    console.print("  5. Then [cyan]/pmm.commdoc[/cyan] and other commands as needed\n")

    print_divider()
    console.print()


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
    subparsers = parser.add_subparsers(dest="command", required=True)

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

    # check
    subparsers.add_parser("check", help="Check environment (git, config, optional AI CLIs)")

    # update
    subparsers.add_parser("update", help="Check for updates and install latest version")

    # help
    subparsers.add_parser("help", help="Show detailed help and available slash commands")

    args = parser.parse_args()

    if args.command == "init":
        print_banner()

        log_step("┌─────────────────────────────────────────────────┐")
        log_step("│  Initializing New Project                       │")
        log_step("└─────────────────────────────────────────────────┘\n")

        console.print(f"[bold cyan]→[/bold cyan] Project name: [bold]{args.name}[/bold]")
        if args.project_id:
            console.print(f"[bold cyan]→[/bold cyan] Project ID: [bold]{args.project_id}[/bold]")
        console.print()

        ai_provider = args.ai_provider
        if not ai_provider:
            ai_provider = choose_ai_provider()

        try:
            repo_root = Path(__file__).resolve().parents[2]
            init_project_structure(
                repo_root=repo_root,
                project_name=args.name,
                project_id=args.project_id,
                use_here=args.here,
                ai_provider=ai_provider,
                init_git=not args.no_git,
                force=args.force,
            )
        except Exception as e:
            console.print()
            log_error(f"Error during init: {e}")
            console.print()
    elif args.command == "check":
        print_banner()
        repo_root = Path(__file__).resolve().parents[2]
        check_environment(repo_root)
    elif args.command == "update":
        print_banner()
        repo_root = Path(__file__).resolve().parents[2]
        check_for_updates(repo_root)
    elif args.command == "help":
        print_banner()
        print_help_screen()
