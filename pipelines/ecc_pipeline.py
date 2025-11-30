
import asyncio
from typing import Optional

from google.adk.runners import InMemoryRunner
from google.genai import types

from agents.ecc_agents import ecc_workflow_agent
from core.config import APP_NAME


def create_runner() -> InMemoryRunner:
    """
    Create an in-memory runner for the ECC workflow.
    """
    return InMemoryRunner(agent=ecc_workflow_agent, app_name=APP_NAME)


def create_session(runner: InMemoryRunner, user_id: str = "vlad"):
    """
    Convenience wrapper to create an ADK session.
    """
    return asyncio.run(
        runner.session_service.create_session(app_name=APP_NAME, user_id=user_id)
    )


def run_ecc_once(
    runner: InMemoryRunner,
    session_id: str,
    user_message: str,
) -> str:
    """
    Sends a single message through the ECC workflow and returns the final text
    (the AccountabilityAgent briefing).
    """
    content = types.Content(
        role="user",
        parts=[types.Part.from_text(text=user_message)],
    )

    final_text = ""

    for event in runner.run(
        user_id="vlad",
        session_id=session_id,
        new_message=content,
    ):
        if event.content and event.content.parts:
            text = event.content.parts[0].text or ""
            final_text = text  # last assistant event is the final briefing

    return final_text


def demo_input() -> str:
    """
    Example context to feed into ECC for tests / demo.
    """
    return """
    This week I must:
    - Finish the ECC Kaggle capstone and GitHub repo (non-negotiable).
    - Design the first version of my AI consulting offer with 3 pricing tiers.
    - Keep morning workouts and at least 2h deep work on ECC for 4 days.
    - I keep getting distracted in the evenings by social media.
    - There is one potential client asking about an AI agent for operations.
    """
