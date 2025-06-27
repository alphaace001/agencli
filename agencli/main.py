import typer
from rich.console import Console

from agencli import ui
from agencli.constants import APP_NAME, APP_VERSION

app = typer.Typer(help=f"{APP_NAME} - Your agenctic CLI developer")
console = Console()


@app.command()
def main(
    version: bool = typer.Option(False, "--version", "-v", help="Show version and exit")
):
    """Entry point for the agencli application."""
    if version:
        console.print(f"{APP_NAME} version {APP_VERSION}")
        return

    ui.banner()


@app.command()
def greet(name: str, age: int = 18):
    """Greet the user with their name and age."""
    typer.echo(f"Hello {name}, you are {age} years old!")


if __name__ == "__main__":
    app()
