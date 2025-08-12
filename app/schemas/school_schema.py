from pydantic import BaseModel

class SchoolBase(BaseModel):
    school_name: str

class SchoolCreate(SchoolBase):
    pass

class SchoolOut(SchoolBase):
    school_id: int

    model_config = {"from_attributes": True}  