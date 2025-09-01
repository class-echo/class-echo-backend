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
    password: Optional[str] = None  # make optional for Google signup


class UserResponse(UserBase):
    user_id: int
    oauth_provider: Optional[str] = None   
    oauth_sub: Optional[str] = None        

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    email: str
    password: str


class GoogleSignupRequest(BaseModel):
    id_token_str: str
    role: UserRole