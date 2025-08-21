from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional


class UserRole(str, Enum):
    super_admin = "super_admin"
    school_admin = "school_admin"
    teacher = "teacher"
    student = "student"
    parent = "parent"


class UserBase(BaseModel):
    email: EmailStr
    role: UserRole
    school_id: Optional[int] = None


class UserCreate(UserBase):
    password: str  # plain password, will be hashed


class UserResponse(UserBase):
    user_id: int

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    email: str
    password: str