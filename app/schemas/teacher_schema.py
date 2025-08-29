from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class TeacherBase(BaseModel):
    school_id: int
    teacher_name: str
    email: EmailStr

class TeacherCreate(TeacherBase):
    pass

class TeacherOut(TeacherBase):
    teacher_id: int
    created_at: Optional[datetime]

    model_config = {"from_attributes": True}
