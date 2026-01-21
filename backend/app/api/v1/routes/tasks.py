from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.task import TaskCreate, TaskPatch, TaskRead
from app.services.task_service import create_task, patch_task, delete_task

router = APIRouter()


@router.post("", response_model=TaskRead)
async def create_task_endpoint(payload: TaskCreate, db: AsyncSession = Depends(get_db)):
    task = await create_task(db, payload, created_by="user")
    return TaskRead.model_validate(task)


@router.patch("/{task_id}", response_model=TaskRead)
async def patch_task_endpoint(task_id: str, payload: TaskPatch, db: AsyncSession = Depends(get_db)):
    task = await patch_task(db, task_id, payload)
    return TaskRead.model_validate(task)


@router.delete("/{task_id}")
async def delete_task_endpoint(task_id: str, db: AsyncSession = Depends(get_db)):
    await delete_task(db, task_id)
    return {"deleted": True}
