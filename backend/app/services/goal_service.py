from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.goal import Goal
from app.models.phase import Phase
from app.models.task import Task
from app.schemas.goal import GoalCreate


async def create_goal(db: AsyncSession, payload: GoalCreate) -> Goal:
    goal = Goal(
        title=payload.title,
        description=payload.description,
        deadline=payload.deadline,
        hours_per_week=payload.hours_per_week,
        experience_level=payload.experience_level,
        style=payload.style,
    )
    db.add(goal)
    await db.commit()
    await db.refresh(goal)
    return goal


async def get_goal(db: AsyncSession, goal_id: str) -> Goal:
    res = await db.execute(select(Goal).where(Goal.id == goal_id))
    goal = res.scalar_one_or_none()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal


async def get_goal_detail(db: AsyncSession, goal_id: str):
    goal = await get_goal(db, goal_id)

    phases_res = await db.execute(select(Phase).where(Phase.goal_id == goal_id).order_by(Phase.order_index))
    tasks_res = await db.execute(select(Task).where(Task.goal_id == goal_id).order_by(Task.order_index))

    phases = list(phases_res.scalars().all())
    tasks = list(tasks_res.scalars().all())
    return goal, phases, tasks


async def clear_plan(db: AsyncSession, goal_id: str) -> None:
    # delete tasks then phases (or rely on cascade if you query objects)
    tasks_res = await db.execute(select(Task).where(Task.goal_id == goal_id))
    for t in tasks_res.scalars().all():
        await db.delete(t)

    phases_res = await db.execute(select(Phase).where(Phase.goal_id == goal_id))
    for p in phases_res.scalars().all():
        await db.delete(p)

    await db.commit()
