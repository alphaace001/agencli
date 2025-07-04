from rich.console import Console

from agencli.ui import panels

colors = panels.Colors()
console = Console()


def info(message: str):
    """Display an information message"""
    panels._prepare_to_print("status")
    console.print(f"ℹ {message}", style=colors.primary)
    panels._last_output = "status"


def muted(message: str, spaces: int = 0):
    """Display a muted message."""
    panels._prepare_to_print("status")
    console.print(f"{' ' * spaces}{message}", style=colors.muted)
    panels._last_output = "status"


def error(message: str, detail: str = None):
    """Display an error message."""
    panels._prepare_to_print("status")
    if detail:
        console.print(f"✗ {message}: {detail}", style=colors.error)
    else:
        console.print(f"✗ {message}", style=colors.error)
    panels._last_output = "status"
