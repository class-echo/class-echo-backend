from pydantic import BaseModel

class TeacherClassSubjectBase(BaseModel):
    school_id: int
    teacher_id: int
    class_section_id: int
    subject_id: int

class TeacherClassSubjectCreate(TeacherClassSubjectBase):
    pass

class TeacherClassSubjectOut(TeacherClassSubjectBase):
    teacher_class_subjects: int

    model_config = {"from_attributes": True}
