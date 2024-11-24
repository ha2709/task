import os

import pytest
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from ..database import get_db
from ..models import Task, base

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
# Test database URL (use an in-memory SQLite for isolated tests)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Set up a test database engine
test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool, echo=False)
TestSessionLocal = sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)


# Override the get_db dependency
async def override_get_db():
    async with TestSessionLocal() as session:
        yield session


# Fixture to set up and tear down the database
@pytest.fixture(autouse=True)
async def setup_test_database():
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(base.metadata.create_all)
    yield
    # Drop tables
    async with test_engine.begin() as conn:
        await conn.run_sync(base.metadata.drop_all)


# Test database connection
@pytest.mark.asyncio
async def test_database_connection():
    async with TestSessionLocal() as session:
        assert session is not None
        assert isinstance(session, AsyncSession)


# Test task creation
@pytest.mark.asyncio
async def test_task_creation():
    async with TestSessionLocal() as session:
        # Create a sample task
        new_task = Task(
            title="Test Task",
            description="This is a test task",
            status="Pending",
            assignee_id=1,
        )
        session.add(new_task)
        await session.commit()
        await session.refresh(new_task)

        # Verify task is created
        assert new_task.id is not None
        assert new_task.title == "Test Task"
