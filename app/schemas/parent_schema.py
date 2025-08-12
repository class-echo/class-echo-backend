from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class ParentBase(BaseModel):
    school_id: int
    first_name: str
    last_name: str
    phone: str
    email: EmailStr
    address: str

class ParentCreate(ParentBase):
    pass

class ParentOut(ParentBase):
    parent_id: int
    created_at: datetime

    model_config = {"from_attributes": True}