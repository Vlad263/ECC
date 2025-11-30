
from typing import Any, Callable, Iterable, Optional

from google.adk.agents import Agent
from google.genai import types

from core.config import MODEL_NAME, RETRY_OPTIONS


def create_llm_agent(
    *,
    name: str,
    description: str,
    instruction: str,
    tools: Optional[Iterable[Callable[..., Any]]] = None,
    output_key: Optional[str] = None,
) -> Agent:
    """
    Factory for LLM-based agents with shared model + retry config.
    """
    tools = list(tools) if tools is not None else []

    return Agent(
        name=name,
        model=MODEL_NAME,
        description=description,
        instruction=instruction,
        tools=tools,
        output_key=output_key,
        generate_content_config=types.GenerateContentConfig(
            http_options=types.HttpOptions(retry_options=RETRY_OPTIONS)
        ),
    )
