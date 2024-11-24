import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

from src.models.base import Base

# from src.models.role import Role


class Role(str, enum.Enum):
    EMPLOYER = "employer"
    EMPLOYEE = "employee"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(Role), nullable=False)
    # Relationship with Task
    tasks = relationship("Task", back_populates="assignee")
