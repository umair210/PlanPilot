from pydantic import BaseModel, Field
from typing import List


class AITask(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=3, max_length=2000)
    estimate_minutes: int = Field(ge=5, le=8 * 60)
    priority: int = Field(ge=1, le=5)
    acceptance_criteria: List[str] = Field(default_factory=list, max_length=6)


class AIPhase(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    objective: str = Field(min_length=3, max_length=2000)

    # REQUIRED: remove default_factory so it must exist in schema + output
    tasks: List[AITask] = Field(min_length=1, max_length=12)


class AIPlan(BaseModel):
    goal_summary: str = Field(min_length=3, max_length=500)
    assumptions: List[str] = Field(default_factory=list, max_length=8)
    phases: List[AIPhase] = Field(min_length=1, max_length=8)


class AIExplicitConstraints(BaseModel):
    deadline: str
    hours_per_week: float | None
    experience_level: str
    style: str


class AIRephrasedGoal(BaseModel):
    normalized_title: str = Field(min_length=3, max_length=200)
    normalized_description: str = Field(min_length=3, max_length=5000)
    explicit_constraints: AIExplicitConstraints
    must_include: List[str] = Field(default_factory=list, max_length=12)
    avoid: List[str] = Field(default_factory=list, max_length=12)
    clarifying_questions: List[str] = Field(default_factory=list, max_length=8)
