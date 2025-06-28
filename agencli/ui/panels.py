from rich.console import Console

console = Console()


class Colors:
    """Define color styles for the console output."""

    primary = "medium_purple1"
    secondary = "medium_purple3"
    muted = "grey62"
    error = "red"
    success = "bold green"
    warning = "orange1"
    tool_data = "bright_blue"


colors = Colors()

# Track last output type for consistent spacing
_last_output = None  # "status","panel","user_input or None"


def _prepare_to_print(new_type: str):
    """Adds a blank line if needed based on context."""
    if _last_output is None or _last_output == "user_input":
        return

    # Add space when switching from a panel to a status message
    if _last_output is None or _last_output == "panel":
        console.print()
    # Add space when switching from status to a panel, or panel to panel.
    elif new_type == "panel" and (_last_output == "status" or _last_output == "panel"):
        console.print()
