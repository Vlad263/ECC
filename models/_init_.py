
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Literal, Optional


class GoalID(str, Enum):
    A = "A"  # AI consulting / revenue engine
    C = "C"  # ECC product
    D = "D"  # Discipline / personal OS
    OTHER = "other"


@dataclass
class StrategicGoal:
    id: GoalID
    name: str
    description: str
    time_horizon: str


LONG_TERM_GOALS: Dict[GoalID, StrategicGoal] = {
    GoalID.A: StrategicGoal(
        id=GoalID.A,
        name="AI Consulting Revenue Engine",
        description="Build and scale an AI consulting + agent-building business.",
        time_horizon="12–24 months",
    ),
    GoalID.C: StrategicGoal(
        id=GoalID.C,
        name="Executive Command Center (ECC) Product",
        description="Turn ECC into a repeatable, sellable strategic assistant product.",
        time_horizon="12–24 months",
    ),
    GoalID.D: StrategicGoal(
        id=GoalID.D,
        name="Discipline & Personal Operating System",
        description="Maintain elite discipline in health, learning, and execution.",
        time_horizon="ongoing",
    ),
}

# ----- Outputs of KnowledgeCaptureAgent -----

@dataclass
class CapturedGoal:
    id: GoalID
    summary: str


@dataclass
class CapturedDecision:
    summary: str
    area: GoalID


@dataclass
class CapturedActionItem:
    title: str
    area: GoalID
    due_hint: Literal["today", "this_week", "this_month", "later"]


@dataclass
class CapturedRisk:
    summary: str
    area: GoalID


@dataclass
class CapturedKnowledge:
    goals: List[CapturedGoal] = field(default_factory=list)
    decisions: List[CapturedDecision] = field(default_factory=list)
    action_items: List[CapturedActionItem] = field(default_factory=list)
    risks: List[CapturedRisk] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)


# ----- Outputs of PriorityAgent -----

@dataclass
class PrioritizedTask:
    title: str
    goal_id: GoalID
    day: Literal["monday", "tuesday", "wednesday", "thursday", "friday"]
    block_hint: Literal["morning", "afternoon", "evening"]
    priority: Literal["P1", "P2", "P3"]
    time_estimate_hours: float
    rationale: str
    area: str  # e.g. "Consulting", "ECC", "Discipline", "Other"


@dataclass
class PrioritizedPlan:
    prioritized_tasks: List[PrioritizedTask]
