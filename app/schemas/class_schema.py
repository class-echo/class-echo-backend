from pydantic import BaseModel

class ClassBase(BaseModel):
    class_name: str
    school_id: int

class ClassCreate(ClassBase):
    pass

class ClassOut(ClassBase):
    class_id: int

    model_config = {"from_attributes": True} 
