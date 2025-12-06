"""ASCII art and banner utilities for PMM-Kit."""

from rich.console import Console

console = Console()


PMM_BANNER = """[bold cyan]
╔═════════════════════════════════════════════════╗
║                                                 ║
║    ██████╗ ███╗   ███╗███╗   ███╗              ║
║    ██╔══██╗████╗ ████║████╗ ████║              ║
║    ██████╔╝██╔████╔██║██╔████╔██║              ║
║    ██╔═══╝ ██║╚██╔╝██║██║╚██╔╝██║              ║
║    ██║     ██║ ╚═╝ ██║██║ ╚═╝ ██║              ║
║    ╚═╝     ╚═╝     ╚═╝╚═╝     ╚═╝              ║
║                                                 ║
║         K I T   •   v0.1.0                      ║
║    [dim]Spec-Driven Product Marketing CLI[/dim]            ║
║                                                 ║
╚═════════════════════════════════════════════════╝[/bold cyan]
"""


def print_banner() -> None:
    """Print the PMM-Kit banner."""
    console.print(PMM_BANNER)


def print_divider() -> None:
    """Print a simple divider line."""
    console.print("[dim]───────────────────────────────────────────────────[/dim]")
