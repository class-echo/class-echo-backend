from pydantic import BaseModel
from typing import Optional

class SubjectClassBase(BaseModel):
    school_id: int
    subject_id: int
    class_section_id: int

class SubjectClassCreate(SubjectClassBase):
    pass

class SubjectClassOut(SubjectClassBase):
    subject_class_id: int

    model_config = {"from_attributes": True}
