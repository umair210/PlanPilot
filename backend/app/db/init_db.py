from app.db.session import engine
from app.db.base import Base

# ensure models are imported so Base.metadata is populated
from app.models.goal import Goal
from app.models.phase import Phase
from app.models.task import Task


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
