import uuid
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    goal_id: Mapped[str] = mapped_column(String, ForeignKey("goals.id"), nullable=False)
    phase_id: Mapped[str | None] = mapped_column(String, ForeignKey("phases.id"), nullable=True)

    parent_task_id: Mapped[str | None] = mapped_column(String, ForeignKey("tasks.id"), nullable=True)

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)

    estimate_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=30)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="todo")
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    created_by: Mapped[str] = mapped_column(String(16), nullable=False, default="ai")

    goal = relationship("Goal", back_populates="tasks")
    phase = relationship("Phase", back_populates="tasks")
