from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import text
from app.database import Base

class Teacher(Base):
    __tablename__ = "teachers"

    teacher_id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.school_id", ondelete="CASCADE"))
    teacher_name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text('now()'))

class TeacherClassSubject(Base):
    __tablename__ = "teacher_class_subjects"

    teacher_class_subjects = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.school_id", ondelete="CASCADE"))
    teacher_id = Column(Integer, ForeignKey("teachers.teacher_id", ondelete="CASCADE"))
    class_section_id = Column(Integer, ForeignKey("class_sections.class_section_id", ondelete="CASCADE"))
    subject_id = Column(Integer, ForeignKey("subjects.subject_id", ondelete="CASCADE"))
