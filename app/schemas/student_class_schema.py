from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class StudentClassBase(BaseModel):
    school_id: int
    reg_no: int
    class_section_id: int

class StudentClassCreate(StudentClassBase):
    pass

class StudentClassOut(StudentClassBase):
    student_class_id: int

    model_config = {"from_attributes": True}
