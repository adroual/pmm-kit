"""ASCII art and banner utilities for PMM-Kit."""

from importlib.metadata import version as get_version

from rich.console import Console

console = Console()


def get_pmm_version() -> str:
    """Get the installed version of pmm-kit."""
    try:
        return get_version("pmm-kit")
    except Exception:
        return "0.2.0"


def get_banner() -> str:
    """Generate the banner with current version."""
    ver = get_pmm_version()
    return f"""[bold cyan]
╔═════════════════════════════════════════════════╗
║                                                 ║
║    ██████╗ ███╗   ███╗███╗   ███╗              ║
║    ██╔══██╗████╗ ████║████╗ ████║              ║
║    ██████╔╝██╔████╔██║██╔████╔██║              ║
║    ██╔═══╝ ██║╚██╔╝██║██║╚██╔╝██║              ║
║    ██║     ██║ ╚═╝ ██║██║ ╚═╝ ██║              ║
║    ╚═╝     ╚═╝     ╚═╝╚═╝     ╚═╝              ║
║                                                 ║
║         K I T   •   v{ver:<10}                 ║
║    [dim]Spec-Driven Product Marketing CLI[/dim]            ║
║                                                 ║
╚═════════════════════════════════════════════════╝[/bold cyan]
"""


def print_banner() -> None:
    """Print the PMM-Kit banner."""
    console.print(get_banner())


def print_divider() -> None:
    """Print a simple divider line."""
    console.print("[dim]───────────────────────────────────────────────────[/dim]")
