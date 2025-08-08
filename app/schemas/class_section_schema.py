from pydantic import BaseModel

class ClassSectionBase(BaseModel):
    school_id: int
    class_id: int
    section_id: int

class ClassSectionCreate(ClassSectionBase):
    pass

class ClassSectionOut(ClassSectionBase):
    class_section_id: int

    model_config = {"from_attributes": True} 
