from pydantic import BaseModel
from typing import Optional

class StudentParentBase(BaseModel):
    school_id: int
    reg_no: int
    parent_id: int
    relation: Optional[str] = None

class StudentParentCreate(StudentParentBase):
    pass

class StudentParentOut(StudentParentBase):
    student_parent_id: int

    model_config = {"from_attributes": True}