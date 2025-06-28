from rich.console import Console
from rich.padding import Padding

from agencli.constants import APP_VERSION
from agencli.ui.panels import colors

console = Console()

BANNER = """
 █████╗  ██████╗ ███████╗███╗   ██╗ ██████╗██╗     ██╗
██╔══██╗██╔════╝ ██╔════╝████╗  ██║██╔════╝██║     ██║
███████║██║  ███╗█████╗  ██╔██╗ ██║██║     ██║     ██║
██╔══██║██║   ██║██╔══╝  ██║╚██╗██║██║     ██║     ██║
██║  ██║╚██████╔╝███████╗██║ ╚████║╚██████╗███████╗██║
╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═╝"""


def banner():
    """Display the application banner."""
    console.clear()
    banner_padding = Padding(BANNER, (1, 0, 0, 2))
    version_padding = Padding(f"v{APP_VERSION}", (0, 0, 1, 2))
    console.print(banner_padding, style=colors.primary)
    console.print(version_padding, style=colors.muted)
