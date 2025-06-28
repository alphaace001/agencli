"""Debug logging configration for the Agencli."""

import logging
from agencli.ui.messages import muted as ui_muted


class UILogHandler(logging.Handler):
    """
    A logging handler that outputs messages to the UI's muted function
    """

    def __init__(self, ui_muted_function):
        super().__init__()
        self.ui_muted_function = ui_muted_function

    def emit(self, record):
        log_entry = self.format(record)

        self.ui_muted_function(log_entry)


def setup_logging(debug_enabled: bool):
    """Configure logging to output to the UI's muted function"""

    ui_log_formatter = logging.Formatter("⚙︎ %(levelname)s: %(message)s")

    if not any(isinstance(handler, UILogHandler) for handler in logging.root.handlers):
        ui_handler = UILogHandler(ui_muted)
        ui_handler.setLevel(logging.DEBUG)
        ui_handler.setFormatter(ui_log_formatter)
        logging.root.addHandler(ui_handler)

    ignored_modules = [
        "httpcore",
        "httpx",
        "urllib3",
        "asyncio",
        "markdown_it",
    ]

    for module in ignored_modules:
        logging.getLogger(module).setLevel(logging.WARNING)

    if debug_enabled:
        logging.root.setLevel(logging.DEBUG)
    else:
        logging.root.setLevel(logging.INFO)
