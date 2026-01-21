from fastapi import APIRouter
from app.api.v1.routes import goals, tasks, phases

api_router = APIRouter()
api_router.include_router(goals.router, prefix="/goals", tags=["goals"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(phases.router, prefix="/phases", tags=["phases"])
