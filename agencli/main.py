import sys
import logging
import asyncio

import typer
from rich.console import Console

from agencli import ui
from agencli.config import (
    ConfigError,
    ConfigValidationError,
    config_exists,
    set_env_vars,
    ensure_config_structure,
    validate_config_structure,
)
from agencli.setup import run_setup
from agencli.constants import APP_NAME, APP_VERSION
from agencli.session import session
from agencli.utils.logger import setup_logging


app = typer.Typer(help=f"{APP_NAME} - Your agenctic CLI developer")
console = Console()
log = logging.getLogger(__name__)


def setup_and_run_event_loop(coro):
    """Create and run event loop with proper cleanup"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(coro)
    finally:
        loop.close()


@app.command()
def main(
    version: bool = typer.Option(
        False, "--version", "-v", help="Show version and exit"
    ),
    debug: bool = typer.Option(False, "--debug", help="Enable debug logging to file"),
):
    """Entry point for the agencli application."""
    if version:
        console.print(f"{APP_NAME} version {APP_VERSION}")
        return

    if debug:
        session.debug_enabled = True

    setup_logging(debug_enabled=debug)

    ui.banner()

    # Check if config exists, run setup if needed
    if not config_exists():
        console.print()
        config = run_setup()
        # Apply env vars from newly created config
        set_env_vars(config.get("env", {}))
    else:
        try:
            config = ensure_config_structure()
            validate_config_structure(config)
            set_env_vars(config.get("env", {}))
        except ConfigError as e:
            ui.error("Configuration error", str(e))
            sys.exit(1)
        except ConfigValidationError as e:
            ui.error("Invalid configuration", str(e))
            sys.exit(1)
        except Exception as e:
            ui.error("Failed to load configuration", str(e))
            sys.exit(1)

    session.init(config, config["default_model"])
    log.info("Session initialized with model: %s", session.current_model)

    # create event loop manually to avoid asyncio.run's signal handling
    setup_and_run_event_loop(repl())


@app.command()
def greet(name: str, age: int = 18):
    """Greet the user with their name and age."""
    typer.echo(f"Hello {name}, you are {age} years old!")


if __name__ == "__main__":
    app()
