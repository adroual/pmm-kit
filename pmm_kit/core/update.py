"""Update functionality for PMM-Kit."""

import subprocess
import sys
from pathlib import Path

from .logger import console, log_error, log_info, log_step, log_success, log_warning


def is_editable_install(repo_root: Path) -> bool:
    """Check if this is an editable/development install."""
    # Check if we're in a git repo
    git_dir = repo_root / ".git"
    return git_dir.exists()


def get_current_version() -> str:
    """Get the current installed version of pmm-kit."""
    try:
        from importlib.metadata import version
        return version("pmm-kit")
    except Exception:
        return "unknown"


def check_for_updates(repo_root: Path) -> None:
    """Check for updates and offer to install them."""
    log_step("\n┌─────────────────────────────────────────────────┐")
    log_step("│  PMM-Kit Update Check                           │")
    log_step("└─────────────────────────────────────────────────┘\n")

    current_version = get_current_version()
    console.print(f"[bold cyan]Current version:[/bold cyan] {current_version}\n")

    if is_editable_install(repo_root):
        log_info("Detected editable/development install\n")

        # Check git status
        try:
            # Fetch latest from remote
            console.print("[dim]Fetching latest changes from GitHub...[/dim]")
            subprocess.run(
                ["git", "fetch", "origin"],
                cwd=str(repo_root),
                check=True,
                capture_output=True,
            )

            # Check if behind
            result = subprocess.run(
                ["git", "rev-list", "--count", "HEAD..origin/main"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
            )

            commits_behind = int(result.stdout.strip()) if result.stdout.strip() else 0

            if commits_behind == 0:
                log_success("✓ You're already on the latest version!\n")
                return
            else:
                log_warning(f"⚠ You are {commits_behind} commit(s) behind origin/main\n")

                console.print("[bold cyan]Would you like to update?[/bold cyan]")
                console.print("  This will run: [dim]git pull origin main[/dim]\n")

                response = input("Update now? [y/N]: ").strip().lower()

                if response == 'y':
                    console.print("\n[dim]Pulling latest changes...[/dim]")
                    subprocess.run(
                        ["git", "pull", "origin", "main"],
                        cwd=str(repo_root),
                        check=True,
                    )
                    log_success("\n✓ Successfully updated to latest version!")
                    log_info("Changes will take effect immediately (editable install)\n")
                else:
                    log_info("Update cancelled\n")

        except subprocess.CalledProcessError as e:
            log_error(f"Git error: {e}")
        except Exception as e:
            log_error(f"Error checking for updates: {e}")

    else:
        # Regular install — force reinstall from GitHub
        log_info("Updating PMM-Kit from GitHub...\n")

        try:
            console.print("[dim]Running: uv cache clean && uv tool install pmm-kit --force --from git+https://github.com/adroual/pmm-kit.git[/dim]\n")

            subprocess.run(
                ["uv", "cache", "clean"],
                check=True,
                capture_output=True,
            )

            subprocess.run(
                [
                    "uv", "tool", "install", "pmm-kit",
                    "--force",
                    "--from", "git+https://github.com/adroual/pmm-kit.git",
                ],
                check=True,
            )

            new_version = get_current_version()
            log_success(f"\n✓ Successfully updated to v{new_version}!")
            log_info("Run [bold]pmm help[/bold] to see what's new.\n")

        except FileNotFoundError:
            log_error("uv is not installed. Install it first:\n")
            console.print("  [cyan]brew install uv[/cyan]\n")
        except subprocess.CalledProcessError as e:
            log_error(f"Update failed: {e}")
            log_info("\nYou can try manually:\n")
            console.print("  [dim]uv cache clean[/dim]")
            console.print("  [dim]uv tool install pmm-kit --force --from git+https://github.com/adroual/pmm-kit.git[/dim]\n")
