import argparse
from pathlib import Path
from typing import Optional

import questionary

from pmm_kit.core.files import check_environment, init_project_structure
from pmm_kit.core.logger import log_error, log_info


PMM_ASCII = r"""
╔══════════════════════════════════════╗
║         P M M  •  K I T              ║
║   Spec-Driven Go-To-Market CLI       ║
╚══════════════════════════════════════╝
"""


def choose_ai_provider(default: Optional[str] = None) -> Optional[str]:
    choices = [
        "copilot  (GitHub Copilot)",
        "claude   (Claude Code)",
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
        "Choose your AI assistant:",
        choices=choices,
        default=default_choice,
    ).ask()

    if not answer or answer.startswith("none"):
        return None
    return answer.split()[0]  # first token is the id


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

    args = parser.parse_args()

    if args.command == "init":
        print(PMM_ASCII)
        log_info(f"Creating new project: {args.name}")

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
            if ai_provider:
                log_info(f"AI assistant set to: {ai_provider}")
            else:
                log_info("No AI assistant selected yet. You can still use /pmm commands with your editor.")
        except Exception as e:
            log_error(f"Error during init: {e}")
    elif args.command == "check":
        print(PMM_ASCII)
        repo_root = Path(__file__).resolve().parents[2]
        check_environment(repo_root)
