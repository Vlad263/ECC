
from __future__ import annotations

from typing import Any, Dict, List

from google.adk.agents import SequentialAgent
from google.adk.tools import google_search

from agents.base_agent import create_llm_agent
from models import LONG_TERM_GOALS


# -------------------------------------------------------------------
# Simple function tools (can later be swapped for MCP / real APIs)
# -------------------------------------------------------------------

def get_open_loops() -> Dict[str, Any]:
    """
    Returns a simulated view of current 'open loops' in the user's life.
    Replace with real data (Sheets, Notion, etc.) later.
    """
    return {
        "status": "success",
        "open_loops": [
            {
                "id": "OL-001",
                "description": "Finalize ECC capstone repo + Kaggle writeup",
                "area": "ECC Product",
                "deadline": "this_week",
            },
            {
                "id": "OL-002",
                "description": "Design 3-tier AI consulting offer with pricing",
                "area": "Consulting Business",
                "deadline": "this_month",
            },
            {
                "id": "OL-003",
                "description": "Stabilize daily deep work + training block",
                "area": "Discipline / Personal OS",
                "deadline": "this_week",
            },
        ],
    }


def log_action_items(action_items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    For now: just prints tasks to stdout.
    In a real system, push them to DB / Sheets / task manager.
    """
    print("=== [ECC LOG] Action items recorded ===")
    for item in action_items:
        print(
            f"- [{item.get('priority', '?')}] {item.get('title')} "
            f"(day={item.get('day')}, area={item.get('area')})"
        )
    print("=======================================")

    return {
        "status": "success",
        "logged_count": len(action_items),
    }


# -------------------------------------------------------------------
# 1) KnowledgeCaptureAgent
# -------------------------------------------------------------------

knowledge_capture_agent = create_llm_agent(
    name="KnowledgeCaptureAgent",
    description=(
        "Reads raw weekly context (notes, thoughts, meeting summaries) and "
        "extracts only the information that matters for execution and strategy."
    ),
    instruction=(
        "You are an executive knowledge capture agent.\n"
        "\n"
        "You receive raw text from the user: mixed notes, meeting summaries, "
        "ideas, worries, and to-dos.\n"
        "\n"
        "Your job is to extract ONLY what matters for planning and execution.\n"
        "Use these strategic areas:\n"
        "- A: AI consulting / revenue engine.\n"
        "- C: ECC product.\n"
        "- D: Discipline / personal OS.\n"
        "- other: everything else.\n"
        "\n"
        "You may call the `get_open_loops` tool to enrich your understanding.\n"
        "\n"
        "Return STRICT JSON inside a Markdown ```json code block with exactly "
        "this structure:\n"
        "```json\n"
        "{\n"
        '  \"goals\": [ {\"id\": \"A|C|D|other\", \"summary\": \"...\" } ],\n"
        '  \"decisions\": [ {\"summary\": \"...\", \"area\": \"A|C|D|other\" } ],\n"
        '  \"action_items\": [\n"
        '    {\"title\": \"...\", \"area\": \"A|C|D|other\", \"due_hint\": \"today|this_week|this_month|later\"}\n"
        "  ],\n"
        '  \"risks\": [ {\"summary\": \"...\", \"area\": \"A|C|D|other\" } ],\n"
        '  \"notes\": [\"... important contextual notes ...\"]\n"
        "}\n"
        "```\n"
        "\n"
        "Rules:\n"
        "- Ignore noise and small talk.\n"
        "- If something is unclear, put it into `notes` instead of hallucinating.\n"
    ),
    tools=[google_search, get_open_loops],
    output_key="ecc_knowledge",
)

# -------------------------------------------------------------------
# 2) StrategicPlannerAgent
# -------------------------------------------------------------------

strategic_planner_agent = create_llm_agent(
    name="StrategicPlannerAgent",
    description=(
        "Converts captured knowledge + long-term goals into a sharp 1-week plan."
    ),
    instruction=(
        "You are a PHD-level Chief Strategy Officer for a solo founder.\n"
        "\n"
        "INPUT:\n"
        "- `ecc_knowledge` from the previous agent.\n"
        "- Long-term goals (A, C, D) are:\n"
        f"{LONG_TERM_GOALS}\n"
        "\n"
        "GOAL:\n"
        "- Design a one-week execution plan that moves the user 5 steps ahead.\n"
        "- Balance A (consulting), C (ECC), D (discipline).\n"
        "- Ruthlessly cut low-leverage tasks.\n"
        "\n"
        "OUTPUT: STRICT JSON in a ```json code block:\n"
        "```json\n"
        "{\n"
        '  \"week_theme\": \"One clear sentence.\",\n'
        '  \"non_negotiables\": [\n'
        '    {\"goal_id\": \"A|C|D\", \"title\": \"...\", \"why_now\": \"...\"}\n'
        "  ],\n"
        '  \"plan_by_day\": {\n'
        '    \"monday\": [\n'
        '      {\"title\": \"...\", \"goal_id\": \"A|C|D|other\", \"block_hint\": \"morning|afternoon|evening\"}\n'
        "    ],\n"
        '    \"tuesday\": [ ... ],\n'
        '    \"wednesday\": [ ... ],\n'
        '    \"thursday\": [ ... ],\n'
        '    \"friday\": [ ... ]\n'
        "  }\n"
        "}\n"
        "```\n"
        "\n"
        "Assume 3–5 hours of deep work per weekday. Prioritize clarity, not volume.\n"
    ),
    tools=[google_search],
    output_key="ecc_plan",
)

# -------------------------------------------------------------------
# 3) PriorityAgent
# -------------------------------------------------------------------

priority_agent = create_llm_agent(
    name="PriorityAgent",
    description=(
        "Turns the weekly plan into an execution-ready task list with P1/P2/P3."
    ),
    instruction=(
        "You are an operations and execution specialist.\n"
        "\n"
        "INPUT:\n"
        "- `ecc_plan` with `plan_by_day`.\n"
        "\n"
        "GOAL:\n"
        "- For each planned item, assign:\n"
        "  * priority: P1 / P2 / P3\n"
        "  * time_estimate_hours (0.5–3.0)\n"
        "  * area: Consulting | ECC | Discipline | Other\n"
        "  * short rationale.\n"
        "\n"
        "PRIORITY RULES:\n"
        "- P1 = moves a strategic needle this week.\n"
        "- P2 = important but can slip.\n"
        "- P3 = nice-to-have / admin.\n"
        "\n"
        "OUTPUT: STRICT JSON in a ```json code block:\n"
        "```json\n"
        "{\n"
        '  \"prioritized_tasks\": [\n'
        "    {\n"
        '      \"title\": \"...\",\n'
        '      \"goal_id\": \"A|C|D|other\",\n'
        '      \"day\": \"monday|tuesday|wednesday|thursday|friday\",\n'
        '      \"block_hint\": \"morning|afternoon|evening\",\n'
        '      \"priority\": \"P1|P2|P3\",\n'
        '      \"time_estimate_hours\": 1.5,\n'
        '      \"rationale\": \"...\",\n'
        '      \"area\": \"Consulting|ECC|Discipline|Other\"\n'
        "    }\n"
        "  ]\n"
        "}\n"
        "```\n"
        "\n"
        "After generating the JSON, call the `log_action_items` tool with the\n"
        "list of `prioritized_tasks`.\n"
    ),
    tools=[log_action_items],
    output_key="ecc_prioritized_plan",
)

# -------------------------------------------------------------------
# 4) AccountabilityAgent
# -------------------------------------------------------------------

accountability_agent = create_llm_agent(
    name="AccountabilityAgent",
    description="Produces the final Executive Command Center (ECC) briefing.",
    instruction=(
        "You are an executive coach + Chief of Staff.\n"
        "\n"
        "INPUT:\n"
        "- `ecc_prioritized_plan` with `prioritized_tasks`.\n"
        "- Long-term goals A, C, D.\n"
        "\n"
        "OUTPUT (Markdown, NOT JSON):\n"
        "1. **Week Theme** – 1 sentence.\n"
        "2. **Top 3 P1 Tasks for Today** – bullet list.\n"
        "3. **Key Risks / Bottlenecks** – bullet list.\n"
        "4. **Discipline Check** – 2–3 bullets on focus/energy/consistency.\n"
        "5. **One Hard Question** – a direct question the user must answer.\n"
        "\n"
        "Tone: direct, professional, zero fluff.\n"
    ),
    tools=[],
)

# -------------------------------------------------------------------
# 5) Workflow agent
# -------------------------------------------------------------------

ecc_workflow_agent = SequentialAgent(
    name="ECCWorkflow",
    description=(
        "End-to-end ECC workflow: capture knowledge → plan → prioritize → briefing."
    ),
    sub_agents=[
        knowledge_capture_agent,
        strategic_planner_agent,
        priority_agent,
        accountability_agent,
    ],
)

# This is what you'd expose if you deploy with ADK / Agent Engine.
root_agent = ecc_workflow_agent
