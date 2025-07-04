from pydantic_ai import Tool

from agencli.tools.find import find
from agencli.tools.git import git_add, git_commit
from agencli.tools.grep import grep
from agencli.tools.list import list_directory
from agencli.tools.read_file import read_file
from agencli.tools.run_command import run_command
from agencli.tools.update_file import update_file
from agencli.tools.write_file import write_file


def create_tools():
    """Create Tool instances for all tools"""
    return [
        Tool(read_file),
        Tool(write_file),
        Tool(update_file),
        Tool(grep),
        Tool(find),
        Tool(list_directory),
        Tool(run_command),
        Tool(git_add),
        Tool(git_commit),
    ]
