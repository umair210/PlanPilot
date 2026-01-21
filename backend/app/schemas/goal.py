from datetime import datetime, date
from pydantic import BaseModel, Field
from typing import Literal


ExperienceLevel = Literal["beginner", "intermediate", "advanced"]
PlanStyle = Literal["fast_mvp", "balanced", "high_quality"]


class GoalCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=10, max_length=5000)
    deadline: date | None = None
    hours_per_week: int | None = Field(default=None, ge=1, le=80)
    experience_level: ExperienceLevel = "intermediate"
    style: PlanStyle = "fast_mvp"


class GoalRead(BaseModel):
    id: str
    title: str
    description: str
    deadline: date | None
    hours_per_week: int | None
    experience_level: ExperienceLevel
    style: PlanStyle
    created_at: datetime

    class Config:
        from_attributes = True
