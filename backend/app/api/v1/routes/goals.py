from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.goal import GoalCreate, GoalRead
from app.schemas.phase import PhaseRead
from app.schemas.task import TaskRead
from app.services.goal_service import create_goal, get_goal_detail
from app.services.phase_service import generate_plan_for_goal

router = APIRouter()


@router.post("", response_model=GoalRead)
async def create_goal_endpoint(payload: GoalCreate, db: AsyncSession = Depends(get_db)):
    return await create_goal(db, payload)


@router.get("/{goal_id}")
async def get_goal_endpoint(goal_id: str, db: AsyncSession = Depends(get_db)):
    goal, phases, tasks = await get_goal_detail(db, goal_id)
    return {
        "goal": GoalRead.model_validate(goal),
        "phases": [PhaseRead.model_validate(p) for p in phases],
        "tasks": [TaskRead.model_validate(t) for t in tasks],
    }


@router.post("/{goal_id}/generate")
async def generate_goal_plan(
    goal_id: str,
    force: bool = Query(default=False),
    db: AsyncSession = Depends(get_db),
):
    goal, phases, tasks = await generate_plan_for_goal(db, goal_id, force=force)
    return {
        "goal": GoalRead.model_validate(goal),
        "phases": [PhaseRead.model_validate(p) for p in phases],
        "tasks": [TaskRead.model_validate(t) for t in tasks],
    }
