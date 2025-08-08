from pydantic import BaseModel

class SectionBase(BaseModel):
    section_name: str
    school_id: int

class SectionCreate(SectionBase):
    pass

class SectionOut(SectionBase):
    section_id: int

    model_config = {"from_attributes": True} 
