import uuid
from datetime import datetime, date
from sqlalchemy import String, DateTime, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Goal(Base):
    __tablename__ = "goals"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)

    deadline: Mapped[date | None] = mapped_column(Date, nullable=True)
    hours_per_week: Mapped[int | None] = mapped_column(Integer, nullable=True)
    experience_level: Mapped[str] = mapped_column(String(32), nullable=False)
    style: Mapped[str] = mapped_column(String(32), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    phases = relationship("Phase", back_populates="goal", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="goal", cascade="all, delete-orphan")
