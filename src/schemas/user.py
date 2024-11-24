import enum
from typing import Optional

from pydantic import BaseModel


class RoleEnum(str, enum.Enum):
    EMPLOYER = "employer"
    EMPLOYEE = "employee"


class UserCreate(BaseModel):
    username: str
    password: str
    role: RoleEnum

    class Config:
        schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "securepassword123",
                "role": "employee",
            }
        }
