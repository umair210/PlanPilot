from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskPatch


async def create_task(db: AsyncSession, payload: TaskCreate, created_by: str = "user", parent_task_id: str | None = None) -> Task:
    task = Task(
        goal_id=payload.goal_id,
        phase_id=payload.phase_id,
        title=payload.title,
        description=payload.description,
        estimate_minutes=payload.estimate_minutes,
        priority=payload.priority,
        status="todo",
        order_index=0,
        created_by=created_by,
        parent_task_id=parent_task_id,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def patch_task(db: AsyncSession, task_id: str, payload: TaskPatch) -> Task:
    res = await db.execute(select(Task).where(Task.id == task_id))
    task = res.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(task, k, v)

    await db.commit()
    await db.refresh(task)
    return task


async def delete_task(db: AsyncSession, task_id: str) -> None:
    res = await db.execute(select(Task).where(Task.id == task_id))
    task = res.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(task)
    await db.commit()
