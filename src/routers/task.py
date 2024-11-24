from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.schemas.task import TaskCreate, TaskStatus, TaskUpdate
from src.services.task import (
    create_task_service,
    get_employee_task_summary,
    list_tasks_service,
    update_task_status_service,
)
from src.utils.auth import get_current_user, require_role

router = APIRouter()


@router.post("")
async def create_task_endpoint(
    task: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_role("employer")),
):
    return await create_task_service(task, db)


@router.get("")
async def list_tasks(
    status: TaskStatus = None,
    assignee_id: int = None,
    sort_by: str = "created_at",
    order: str = "asc",
    limit: int = 10,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):

    tasks = await list_tasks_service(
        status=status,
        assignee_id=assignee_id,
        sort_by=sort_by,
        order=order,
        limit=limit,
        offset=offset,
        db=db,
    )
    return {"tasks": tasks, "limit": limit, "offset": offset}


@router.patch("{task_id}/status")
async def update_task_status_endpoint(
    task_id: int,
    status: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_role("employee")),
):
    return await update_task_status_service(task_id, status, db)


@router.get("/tasks/summary")
async def task_summary(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_role("employee")),
):
    return await get_employee_task_summary(db)
