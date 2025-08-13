from pydantic import BaseModel
from typing import Optional

class SubjectBase(BaseModel):
    school_id: int
    subject_name: str

class SubjectCreate(SubjectBase):
    pass

class SubjectOut(SubjectBase):
    subject_id: int

    model_config = {"from_attributes": True}
