from datetime import datetime
from typing import List, Optional

from fastapi import Depends
from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.database import get_db
from src.models.task import Task
from src.models.user import Role, User
from src.schemas.task import TaskResponse, TaskStatus, TaskUpdate


async def create_task_service(
    task_data: dict,
    db: AsyncSession = Depends(get_db),
) -> List[TaskResponse]:
    # Convert timezone-aware datetime to naive datetime
    if task_data.due_date and task_data.due_date.tzinfo is not None:
        task_data.due_date = task_data.due_date.replace(tzinfo=None)

    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status or "Pending",
        assignee_id=task_data.assignee_id,
        due_date=task_data.due_date,
        created_at=datetime.utcnow(),
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


async def list_tasks_service(
    db: AsyncSession,
    status: Optional[TaskStatus] = None,
    assignee_id: Optional[int] = None,
    sort_by: str = "created_at",
    order: str = "asc",
    limit: int = 10,
    offset: int = 0,
) -> List[TaskResponse]:
    """
    Service to list tasks with optional filters, sorting, and pagination.
    Returns a list of TaskResponse objects.
    """
    # Base query with eager loading of assignee
    query = select(Task).options(joinedload(Task.assignee))

    # Apply filters
    if status:
        query = query.where(Task.status == status.value)
    if assignee_id:
        query = query.where(Task.assignee_id == assignee_id)

    # Apply sorting
    if sort_by == "created_at":
        query = query.order_by(
            Task.created_at.asc() if order == "asc" else Task.created_at.desc()
        )
    elif sort_by == "due_date":
        query = query.order_by(
            Task.due_date.asc() if order == "asc" else Task.due_date.desc()
        )

    # Apply pagination
    query = query.offset(offset).limit(limit)

    # Execute the query
    result = await db.execute(query)
    tasks = result.scalars().all()

    # Serialize tasks into TaskResponse
    return [TaskResponse.from_orm(task) for task in tasks]


async def update_task_status_service(
    task_id: int, status: TaskUpdate, db: AsyncSession
):
    task = await db.get(Task, task_id)
    if not task:
        return {"error": "Task not found"}
    task.status = status.status
    await db.commit()
    await db.refresh(task)
    return task


async def get_employee_task_summary(db: AsyncSession):
    # Build the query
    results = await db.execute(
        db.query(
            User.id.label("employee_id"),
            User.username.label("employee_name"),
            func.count(Task.id).label("total_tasks"),
            func.sum(case([(Task.status == "Completed", 1)], else_=0)).label(
                "completed_tasks"
            ),
        )
        .join(Task, Task.assignee_id == User.id, isouter=True)
        .filter(User.role == Role.EMPLOYEE)
        .group_by(User.id, User.username)
        .order_by(User.username)
    )

    # Fetch all rows as a list of dictionaries
    return [
        {
            "employee_id": row.employee_id,
            "employee_name": row.employee_name,
            "total_tasks": row.total_tasks,
            "completed_tasks": row.completed_tasks,
        }
        for row in results.fetchall()
    ]
