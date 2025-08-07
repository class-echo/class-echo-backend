from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StudentBase(BaseModel):
    f_name: str 
    l_name: str
    address: Optional[str] = None
    admit_date: Optional[datetime] = None
    leave_date: Optional[datetime] = None

class StudentCreate(StudentBase):
    school_id: int

class StudentUpdate(StudentBase):
    pass

class StudentOut(StudentBase):
    reg_no: int
    school_id: int
    created_at: Optional[datetime]

    model_config = {"from_attributes": True} #  Without from_attributes=True, an error is raised, because Pydantic would expect a dictionary, not a SQLAlchemy object.


