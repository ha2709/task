from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    assignee_id: int
    due_date: Optional[datetime] = None
    status: Optional[str] = "Pending"

    class Config:
        schema_extra = {
            "example": {
                "title": "Finish API Documentation",
                "description": "Prepare and finalize the API documentation for the project.",
                "assignee_id": 1,
                "due_date": "2024-12-01T10:00:00",
            }
        }


class TaskStatus(str, Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


class TaskUpdate(BaseModel):
    status: str

    class Config:
        schema_extra = {"example": {"status": "In Progress"}}


class AssigneeResponse(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        orm_mode = True
        from_attributes = True


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: TaskStatus
    assignee_id: Optional[int]
    assignee: Optional[AssigneeResponse]
    created_at: Optional[datetime]
    due_date: Optional[datetime]

    class Config:
        orm_mode = True
        from_attributes = True
