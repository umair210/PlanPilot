from pydantic import BaseModel, Field
from typing import Literal


TaskStatus = Literal["todo", "done"]


class TaskCreate(BaseModel):
    goal_id: str
    phase_id: str | None = None
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=3, max_length=5000)
    estimate_minutes: int = Field(default=30, ge=5, le=8 * 60)
    priority: int = Field(default=3, ge=1, le=5)


class TaskPatch(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=200)
    description: str | None = Field(default=None, min_length=3, max_length=5000)
    estimate_minutes: int | None = Field(default=None, ge=5, le=8 * 60)
    priority: int | None = Field(default=None, ge=1, le=5)
    status: TaskStatus | None = None
    phase_id: str | None = None
    order_index: int | None = None


class TaskRead(BaseModel):
    id: str
    goal_id: str
    phase_id: str | None
    parent_task_id: str | None
    title: str
    description: str
    estimate_minutes: int
    priority: int
    status: TaskStatus
    order_index: int
    created_by: str

    class Config:
        from_attributes = True
