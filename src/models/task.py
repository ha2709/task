from sqlalchemy import Column, DateTime, Enum, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.models.base import Base


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(
        String, default="Pending", index=True
    )  #   Pending, In Progress, Completed
    assignee_id = Column(Integer, ForeignKey("users.id"), index=True)
    assignee = relationship("User", back_populates="tasks", lazy="joined")
    created_at = Column(
        DateTime,
        default=func.now(),
    )
    due_date = Column(DateTime)

    __table_args__ = (Index("ix_tasks_status_assignee", "status", "assignee_id"),)
