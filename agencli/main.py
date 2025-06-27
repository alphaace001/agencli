import typer
from agencli.constants import APP_NAME

app = typer.Typer(help=f"{APP_NAME} - Your agenctic CLI developer")


@app.command()
def greet(name: str, age: int = 18):
    """Greet someone with their name and age."""
    typer.echo(f"Hello {name}, you are {age} years old!")
    
@app.command()
def wish(name: str, age: int = 18):
    """Greet someone with their name and age."""
    typer.echo(f"Hello {name}, you are {age} years old!")


if __name__ == "__main__":
    app()
