import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.models import base, task, user

load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL")
print(10, DATABASE_URL)
# Create the database engine
async_engine = create_async_engine(DATABASE_URL, poolclass=NullPool, echo=True)

# Create a sessionmaker for async sessions
AsyncSessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


# Dependency to get a database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
