from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


def log_info(msg: str) -> None:
    """Log info message in cyan."""
    console.print(f"[cyan]→[/cyan] {msg}")


def log_success(msg: str) -> None:
    """Log success message in green."""
    console.print(f"[green]✓[/green] {msg}")


def log_error(msg: str) -> None:
    """Log error message in red."""
    console.print(f"[red]✗[/red] {msg}")


def log_warning(msg: str) -> None:
    """Log warning message in yellow."""
    console.print(f"[yellow]⚠[/yellow] {msg}")


def log_step(msg: str) -> None:
    """Log a step in a process."""
    console.print(f"[bold cyan]{msg}[/bold cyan]")


def print_panel(content: str, title: str = "", border_style: str = "cyan") -> None:
    """Print content in a bordered panel."""
    console.print(Panel(content, title=title, border_style=border_style))


def print_box(lines: list[str], style: str = "cyan") -> None:
    """Print multiple lines in a simple box."""
    max_len = max(len(line) for line in lines) if lines else 0
    console.print(f"[{style}]┌{'─' * (max_len + 2)}┐[/{style}]")
    for line in lines:
        padding = max_len - len(line)
        console.print(f"[{style}]│[/{style}] {line}{' ' * padding} [{style}]│[/{style}]")
    console.print(f"[{style}]└{'─' * (max_len + 2)}┘[/{style}]")
