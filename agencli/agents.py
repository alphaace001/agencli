from pathlib import Path

from pydantic_ai import Agent

from agencli.session import session
from agencli.tools import TOOLS


def _get_prompt(name: str) -> str:
    try:
        prompt_path = Path(__file__).parent / "prompts" / f"{name}.txt"
        return prompt_path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return f"Error: Prompt file '{name}.txt' not found"


def get_or_create_agent():
    if session.current_model not in session.agents:
        base_agent = Agent(
            model=session.current_model,
            system_prompt=_get_prompt("system"),
            tools=TOOLS,
            mcp_server=load_mcp_servers(),
            deps_type=ToolDeps,
        )
        session.agents[session.current_model] = MCPAgent(base_agent)
    return session.agents[session.current_model]
