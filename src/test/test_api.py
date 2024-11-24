import os

import pytest
from dotenv import load_dotenv
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..main import app

load_dotenv()
# Override the get_db dependency in the app
app.dependency_overrides[get_db] = get_db
BASE_URL = os.getenv("BASE_URL")

from unittest.mock import AsyncMock

import pytest

from src.services import create_task_service


@pytest.mark.asyncio
async def test_create_task_service():
    # Mock database session
    mock_db = AsyncMock()

    # Input data
    task_data = {
        "title": "Test Task",
        "description": "Task for testing",
        "assignee_id": 1,
        "due_date": None,
        "status": "Pending",
    }

    # Call service function
    result = await create_task_service(task_data, mock_db)

    # Assertions
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    assert result.title == "Test Task"
    assert result.status == "Pending"


@pytest.mark.asyncio
async def test_create_task_endpoint():
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.post(
            "/task/",
            json={
                "title": "New Task",
                "description": "This is a test task",
                "assignee_id": 1,
                "due_date": "2024-12-01T10:00:00",
            },
        )
        print(29, response)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["title"] == "New Task"
        assert response_data["assignee_id"] == 1


@pytest.mark.asyncio
async def test_list_tasks_endpoint():
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        response = await client.get("/task/")
        assert response.status_code == 200
        response_data = response.json()
        assert isinstance(response_data, list)


@pytest.mark.asyncio
async def test_update_task_status_endpoint():
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        # Create a task first
        create_response = await client.post(
            "/tasks/",
            json={
                "title": "Another Task",
                "description": "Update status test",
                "assignee_id": 1,
                "due_date": "2024-12-01T10:00:00",
            },
        )
        task_id = create_response.json()["id"]

        # Update the task status
        update_response = await client.patch(
            f"/task/{task_id}/status", json={"status": "In Progress"}
        )
        assert update_response.status_code == 200
        updated_task = update_response.json()
        assert updated_task["status"] == "In Progress"
